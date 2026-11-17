"""
BiliYouTik2Brain — 管线主入口

职责：
  1. process(url) — 主管线（Task Graph 版）: 槽位检查 → 构建图 → 执行 → 提取结果
  2. process_linear(url) — 线性管线（保留兼容）
"""

import os, sys, json, time
from typing import Dict, List, Tuple

from .schemas import (
    TranscriptionResult, VideoInfo, Platform, CollectResult,
)
from .config import (
    PlatformRegistry, assess_and_route, record_task, add_pending,
    record_completed,
)
from .slots import (
    acquire_light_slot, release_light_slot, queue_light, dequeue_light,
)
from .builder import build_pipeline_graph
from .node_collect import collect, _node_collect
from .node_transcribe import transcribe
from .node_save import save_result, _node_update_knowledge
from .speaker_knowledge import update_after_video


# ═══════════════════════════════════════════════════════════════
# 图结果提取
# ═══════════════════════════════════════════════════════════════

def _extract_context_from_graph(graph_result, url: str) -> TranscriptionResult:
    """从图执行结果提取 TranscriptionResult"""
    from .schemas import TranscriptionResult
    
    nodes = graph_result.node_results
    
    collected = getattr(nodes.get("collect"), "result", None)
    video = collected.video if collected else None
    
    assess_result = getattr(nodes.get("assess"), "result", {}) or {}
    route = assess_result.get("route", None)
    transcribe_result = getattr(nodes.get("transcribe"), "result", {}) or {}
    enhance_result = getattr(nodes.get("enhance"), "result", {}) or {}
    
    downstream_succeeded = bool(
        transcribe_result.get("text")
        or enhance_result.get("corrected_text")
        or enhance_result.get("analysis")
    )
    
    if assess_result.get("pending") and not downstream_succeeded:
        result = TranscriptionResult(video=video)
        result.error = f"pending:{assess_result.get('wf_id', 'unknown')}"
        return result
    
    save_node = nodes.get("save")
    if save_node and isinstance(save_node.result, TranscriptionResult):
        result = save_node.result
        result.video = video or result.video
    else:
        result = TranscriptionResult(video=video)
        result.raw_text = transcribe_result.get("text", "")
        result.model_used = f"faster-whisper-{getattr(route, 'model', 'base')}" if route else "faster-whisper-base"
        result.corrected_text = enhance_result.get("corrected_text", result.raw_text)
        result.analysis = enhance_result.get("analysis", {})
        result.duration_s = video.duration if video else 0
        result.segments = transcribe_result.get("segments", [])
        if collected:
            result.subtitle = collected.subtitle
            result.audio = collected.audio
            result.comments = collected.comments
    
    return result


# ═══════════════════════════════════════════════════════════════
# 主管线（Task Graph 版）
# ═══════════════════════════════════════════════════════════════

def process(url: str) -> TranscriptionResult:
    """主管线（v2 — Task Graph 版）
    
    流程：
      1. 并发槽位检查 → 槽位满则排队
      2. build_pipeline_graph(url) → 构建任务图
      3. graph.run() → 自动拓扑排序+逐层执行
      4. 提取结果
      5. 记录指标 + 释放槽位
      6. 检查队列中下一个任务
    """
    start = time.time()
    
    from .pipeline_graph import Graph
    
    print(f"\n[处理] {url}")
    
    # 0. 轻活槽位检查（安检门）
    if not acquire_light_slot():
        qid = queue_light(url)
        result = TranscriptionResult(
            video=VideoInfo(
                platform=Platform.UNKNOWN, video_id="", title="",
                duration=0, uploader="", uploader_id="", url=url,
            ),
            error=f"pending:{qid}",
        )
        result.pipeline_time_s = round(time.time() - start, 1)
        return result
    
    try:
        # 1. 构建任务图
        print(f"[管线] 构建任务图...")
        graph = build_pipeline_graph(url)
        
        # 2. 执行
        print(f"[管线] 开始执行...")
        graph_result = graph.run(context={"url": url})
        
        # 3. 提取结果
        result = _extract_context_from_graph(graph_result, url)
        result.pipeline_time_s = round(time.time() - start, 1)
        
        # 4. 输出摘要
        if result.error and result.error.startswith("pending:"):
            print(f"\n  ⏳ 任务排队中 (ID: {result.error})")
        else:
            nodes = graph_result.node_results
            assess_r = getattr(nodes.get("assess"), "result", {}) or {}
            route = assess_r.get("route", None)
            model_name = getattr(route, 'model', 'base') if route else 'base'
            record_task(result.duration_s, model_name, result.pipeline_time_s, 1.0)
            
            if nodes.get("update_knowledge") and nodes["update_knowledge"].status != "success":
                try:
                    _node_update_knowledge(
                        video=result.video,
                        corrected_text=result.corrected_text or "",
                        analysis=result.analysis or {},
                    )
                except Exception as e:
                    print(f"  [节点] ⚠️ 执行异常: {e}")
            
            print(f"\n  📊 管线摘要")
            print(graph_result.graph_summary)
            text = result.corrected_text or result.raw_text
            print(f"     文本: {len(text)} 字符" if text else "     文本: 空")
            if result.analysis and result.analysis.get("summary"):
                print(f"     分析: {result.analysis['summary'][:60]}...")
    finally:
        release_light_slot()
        record_completed(url)
        next_url = dequeue_light()
        if next_url:
            print(f"  [排队] ↳ 自动接续下一个: {next_url[:60]}...")
            process(next_url)
    
    return result


# ═══════════════════════════════════════════════════════════════
# 旧版线性管线（保留兼容）
# ═══════════════════════════════════════════════════════════════

def process_linear(url: str) -> TranscriptionResult:
    """旧版线性管线"""
    start = time.time()
    result = None
    
    try:
        print(f"\n[1/4] 采集数据...")
        collected = collect(url)
        vi = collected.video
        print(f"  [视频] {vi.title}")
        print(f"  [时长] {vi.duration}s | UP主: {vi.uploader}")
        
        result = TranscriptionResult(video=vi)
        result.audio = collected.audio
        result.subtitle = collected.subtitle
        result.comments = collected.comments
        result.duration_s = vi.duration
        
        if not collected.audio.success:
            return result
        
        print(f"\n[2/4] 资源评估+预检...")
        route = assess_and_route(vi.duration, local_available=False)
        
        if route.target == "pending":
            print(f"\n  ⚠️ 算力不足: {route.reason}")
            wf_id = add_pending(url, vi.duration, route.estimated_workload,
                              notes=f"需要{route.required_cores}核/{route.required_ram_gb}GB")
            result = TranscriptionResult(video=vi)
            result.error = f"pending:{wf_id}"
            return result
        
        if collected.audio.file_path:
            from .assessor import assess_audio
            assmnt = assess_audio(collected.audio.file_path, vi.duration)
            route.model = assmnt["model"]
        print(f"  [路由] {route.target} | 模型: {route.model}")
        
        print(f"\n[3/4] 转录 (faster-whisper {route.model})...")
        method_str = "VAD智能分段" if route.use_vad else "直接转录"
        print(f"  [方法] {method_str}")
        tr = transcribe(collected.audio.file_path, vi.duration, route.model, use_vad=route.use_vad)
        result.raw_text = tr["text"]
        result.model_used = f"faster-whisper-{route.model}"
        
        if not result.raw_text.strip():
            print("  ⚠️ 转录结果为空（可能是纯音乐/环境音视频）")
        
        print(f"\n[4/4] LLM修复+结构化分析（提示词工程）...")
        
        st_text = ""
        st_segments = []
        if collected.subtitle.success:
            st_text = collected.subtitle.text
            st_segments = collected.subtitle.segments or []
        
        from .enhance_engine import enhance_and_analyze
        
        ea = enhance_and_analyze(
            result.raw_text,
            video_title=vi.title,
            uploader=vi.uploader,
            bvid=vi.video_id,
            low_conf_words=tr.get("low_conf_words", []),
            video_path=getattr(collected, "video_file", ""),
            raw_segments=tr.get("segments", []),
            subtitle_text=st_text,
            subtitle_segments=st_segments,
        )
        result.corrected_text = ea["corrected_text"]
        result.analysis = ea["analysis"]
        
        # P2
        unresolved = ea.get("_unresolved", [])
        if unresolved and vi.video_id:
            print(f"\n  [正反验证] 🔄 {len(unresolved)}词残留仍未修复")
            from .p2_decision import should_retranscribe
            p2_trigger, p2_debug = should_retranscribe(
                unresolved_words=unresolved,
                total_chars=len(result.corrected_text or ""),
                speech_segments=[], avg_quality=1.0, uploader=vi.uploader,
            )
            print(f"  [P2决策] 有效值={p2_debug['effective']:.4f}%, "
                  f"阈值={p2_debug['threshold']}%, "
                  f"触发={'✅' if p2_trigger else '❌'}")
        
        result.pipeline_time_s = round(time.time() - start, 1)
        filepath = save_result(result)
        print(f"\n  ✅ 已保存: {os.path.basename(filepath)} ({result.pipeline_time_s:.1f}s)")
        
        if result.corrected_text and result.analysis:
            update_after_video(
                speaker=vi.uploader, video_title=vi.title,
                bvid=vi.video_id, video_duration=vi.duration,
                analysis=result.analysis,
                corrected_text=result.corrected_text,
            )
        
        record_task(vi.duration, route.model, result.pipeline_time_s, 1.0)
        
    except Exception as e:
        if result is None:
            raise
        result.error = str(e)
        print(f"\n  ❌ 错误: {e}")
    
    result.pipeline_time_s = round(time.time() - start, 1)
    return result
