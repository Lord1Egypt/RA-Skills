"""
OCR 节点 v2 — 两条腿交叉验证 + 教学画面文字提取 + keyframe 截取
================================================================
v2.3 重构 (小哲分治+三路并行):
  核心改动:
    - depends=["assess","collect"] (不等transcribe! 前半段只需video_path)
    - 前3步(场景+采样+OCR)与transcribe并行, 交叉验证等segments ready
    - 逐帧OCR用 ThreadPoolExecutor(3) 批处理 → 2.4s降到~1s
    
  数据流:
    阶段A(并行): 场景检测 → 采样 → 截帧 → OCR引擎初始化 → 批量OCR
    阶段B(屏障): 等transcribe.segments ready → 交叉验证 → 合并时间轴
"""

import os, sys, json, time, subprocess, hashlib
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    from .frame_sampler_v2 import (
        detect_scenes, generate_sample_plan, capture_frames,
        compute_frame_change_score, SamplePlan,
    )
    from .ocr_engine_v2 import (
        create_ocr_engine, run_ocr, process_frame_full,
        precheck_subtitle_region, run_layout_analysis,
    )
    from .ocr_cross_validator import (
        OCRBlock, OCRTimelineFrame,
        classify_ocr_blocks, compute_teaching_focus_score,
        is_keyframe_worthy, select_best_keyframe,
        merge_ocr_to_subtitle_timeline,
    )
except ImportError:
    from frame_sampler_v2 import (
        detect_scenes, generate_sample_plan, capture_frames,
        compute_frame_change_score, SamplePlan,
    )
    from ocr_engine_v2 import (
        create_ocr_engine, run_ocr, process_frame_full,
        precheck_subtitle_region, run_layout_analysis,
    )
    from ocr_cross_validator import (
        OCRBlock, OCRTimelineFrame,
        classify_ocr_blocks, compute_teaching_focus_score,
        is_keyframe_worthy, select_best_keyframe,
        merge_ocr_to_subtitle_timeline,
    )


def node_ocr_v2(**kw) -> Dict:
    """
    OCR v2 节点入口 — 两阶段执行:
      A(与transcribe并行): 场景+采样+截帧+批量OCR
      B(屏障后): 交叉验证+合并(等transcribe.segments)
    
    输入:
      - collect: 采集结果(含 video_path, video_id)
      - assess: 评估结果(含路由)
      - transcribe: 转录结果(含 segments) — 可能尚未就绪!
      - speaker_knowledge: UP主知识库
      - environment: 环境配置
    """
    env = kw.get("environment", {})
    if isinstance(env, dict) and not env.get("enable_ocr", True):
        print(f"  [OCR v2] ⏭️ L0环境降级")
        return {"ocr_applied": False, "reason": "l0_disabled"}
    
    collect_result = kw.get("collect")
    transcribe_result = kw.get("transcribe", {})
    speaker_knowledge = kw.get("speaker_knowledge", kw.get("speaker_profile", {}))
    
    if not collect_result:
        return {"ocr_applied": False, "reason": "no_collect"}
    
    video_path = getattr(collect_result, "video_file", "")
    video_id = getattr(collect_result, "video_id", "")
    
    if not video_path or not os.path.exists(video_path):
        print(f"  [OCR v2] ⏭️ 无视频文件")
        return {"ocr_applied": False, "reason": "no_video"}
    
    print(f"  [OCR v2] 🎬 双通道采集: 场景检测 + OCR...", end="", flush=True)
    t_start = time.time()
    
    try:
        result = _run_ocr_pipeline(
            video_path=video_path,
            video_id=video_id,
            transcribe_result=transcribe_result,
            speaker_profile=speaker_knowledge,
            work_dir=kw.get("work_dir", f"/tmp/ocr_v2_{video_id[:8]}"),
        )
        
        elapsed = time.time() - t_start
        n_frames = len(result.get("ocr_frames", []))
        n_keyframes = len(result.get("teaching_keyframes", []))
        print(f" ✅ {n_frames}帧OCR | {n_keyframes}张说明画面 | {elapsed:.1f}s")
        
        return result
    
    except Exception as e:
        import traceback
        print(f" ⚠️ {e}")
        traceback.print_exc()
        return {"ocr_applied": False, "reason": str(e)}


def _run_ocr_pipeline(
    video_path: str,
    video_id: str,
    transcribe_result: Dict,
    speaker_profile: Dict,
    work_dir: str,
) -> Dict:
    """OCR 管线主逻辑 — 两阶段执行"""
    
    os.makedirs(work_dir, exist_ok=True)
    frames_dir = os.path.join(work_dir, "frames")
    os.makedirs(frames_dir, exist_ok=True)
    keyframes_dir = os.path.join(work_dir, "keyframes")
    os.makedirs(keyframes_dir, exist_ok=True)
    
    # ═══════════════════════════════════════════════
    # 阶段A: 画面通道 (与transcribe并行,不需要segments)
    # ═══════════════════════════════════════════════
    
    # ── 步骤 1: 场景检测 ──
    scenes = detect_scenes(video_path)
    
    # ── 步骤 2: 生成采样计划 ──
    # transcribe 可能还没完成 — segments 可能是空的
    # 先用粗粒度的场景驱动采样，segments 用于后续交叉验证
    subtitle_segments = transcribe_result.get("segments", [])
    
    cap = cv2_module()
    fps = 30.0
    try:
        cap_obj = cap.VideoCapture(video_path)
        fps = cap_obj.get(cap.CAP_PROP_FPS) or 30
        cap_obj.release()
    except Exception:
        pass
    
    sample_plan = generate_sample_plan(
        scenes=scenes,
        subtitle_segments=subtitle_segments,
        speaker_profile=speaker_profile,
        fps=fps,
    )
    
    # ── 步骤 3: 截帧 ──
    frame_paths = capture_frames(
        video_path=video_path,
        sample_plan=sample_plan,
        output_dir=frames_dir,
        video_id=video_id,
    )
    
    # 建立时间戳→路径映射
    time_to_path = {}
    for i, plan in enumerate(sample_plan):
        if i < len(frame_paths):
            time_to_path[plan.timestamp_sec] = frame_paths[i]
    
    # ── 步骤 4: OCR 引擎初始化 ──
    engine, engine_name = create_ocr_engine(prefer_engine="rapidocr", lang="ch")
    if engine is None:
        return {"ocr_applied": False, "reason": "no_engine"}
    
    # ── 步骤 5: 批量OCR (三路并行,无需segments) ──
    # 逐帧OCR不需要transcription — 只在后续cross_validate时需要
    ocr_frames = []
    keyframe_paths = []
    subtitle_region = None
    
    # 准备帧输入
    frame_inputs = []
    for plan in sample_plan:
        ts = plan.timestamp_sec
        frame_path = time_to_path.get(ts)
        if frame_path and os.path.exists(frame_path):
            frame_inputs.append((ts, frame_path))
    
    # 三路并行OCR (小哲分治: 每路独立OCR, 最后归并)
    def _ocr_single(args):
        ts, fpath = args
        try:
            # 纯OCR (不含交叉验证 — 交叉验证需要segments)
            raw_result = process_frame_full(
                ocr_engine=engine,
                engine_name=engine_name,
                image_path=fpath,
                transcript_at_timestamp="",  # 空 — 先不做交叉验证
            )
            return ts, fpath, raw_result
        except Exception as e:
            print(f"    [OCR v2] 帧@{ts:.1f}s OCR失败: {e}")
            return ts, fpath, None
    
    print(f"", end="", flush=True)
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {pool.submit(_ocr_single, inp): inp for inp in frame_inputs}
        for future in as_completed(futures):
            ts, fpath, raw_result = future.result()
            if raw_result is None:
                continue
            
            # 延迟交叉验证: 等 segments ready 后再分类
            # 先存中间态
            ocr_frames.append(_RawFrameResult(ts, fpath, raw_result))
            
            # 首帧预检
            if subtitle_region is None and raw_result.get('subtitle_blocks'):
                subtitle_region = precheck_subtitle_region(
                    raw_result['all_blocks'], ""
                )
            
            # keyframe
            if raw_result.get('is_keyframe'):
                kf_path = os.path.join(
                    keyframes_dir, f"kf_{video_id[:8]}_{ts:.1f}s.jpg"
                )
                _copy_or_link(fpath, kf_path)
                keyframe_paths.append(kf_path)
    
    # 按时间戳排序
    ocr_frames.sort(key=lambda f: f.timestamp_sec)
    
    # ═══════════════════════════════════════════════
    # 阶段B: 交叉验证 (屏障: 等segments ready)
    # ═══════════════════════════════════════════════
    
    # 如果transcribe当时没完成,现在重新获取segments
    subtitle_segments = transcribe_result.get("segments", [])
    if not subtitle_segments:
        print(f"  [OCR v2] ⚠️ 无字幕段 — 跳过交叉验证,输出纯OCR结果")
    
    timeline_frames = []
    for raw in ocr_frames:
        transcript = _get_transcript_at_time(subtitle_segments, raw.timestamp_sec)
        
        # 如果有转录, 重做交叉验证
        if transcript and raw.raw_result:
            # 重新分类 (现在有转录了)
            from .ocr_cross_validator import classify_ocr_blocks
            blocks = raw.raw_result['all_blocks']
            if blocks:
                classified = classify_ocr_blocks(
                    blocks, transcript, subtitle_similarity_threshold=0.3,
                )
                # classify_ocr_blocks 返回 (subtitle_blocks, teaching_blocks)
                subtitle_blocks, teaching_blocks = classified
                blocks = subtitle_blocks + teaching_blocks
            else:
                subtitle_blocks = []
                teaching_blocks = []
            teaching_focus_score = compute_teaching_focus_score(blocks)
            if isinstance(teaching_focus_score, tuple):
                teaching_focus_score, teaching_focus_region = teaching_focus_score
            else:
                teaching_focus_region = None
        else:
            # 无转录 — 用纯OCR结果
            blocks = raw.raw_result.get('all_blocks', [])
            subtitle_blocks = raw.raw_result.get('subtitle_blocks', [])
            teaching_blocks = raw.raw_result.get('teaching_blocks', [])
            teaching_focus_score = raw.raw_result.get('teaching_focus_score', 0)
        
        timeline_frame = OCRTimelineFrame(
            timestamp_sec=raw.timestamp_sec,
            image_path=raw.image_path,
            blocks=blocks,
            subtitle_blocks=subtitle_blocks,
            teaching_blocks=teaching_blocks,
            teaching_focus_score=teaching_focus_score,
            teaching_focus_region=(
                teaching_focus_region if transcript and raw.raw_result
                else raw.raw_result.get('teaching_focus_region')
            ),
        )
        timeline_frames.append(timeline_frame)
    
    # ── 步骤 6: 合并到字幕时间轴 ──
    timeline_visual = merge_ocr_to_subtitle_timeline(
        subtitle_segments=subtitle_segments,
        ocr_frames=timeline_frames,
    )
    
    # ═══════════════════════════════════════════════
    # 结构化输出
    # ═══════════════════════════════════════════════
    return {
        "ocr_applied": True,
        "engine": engine_name,
        "has_teaching_text": any(
            len(list(f.teaching_blocks) if isinstance(f.teaching_blocks, (list, tuple)) else []) > 0
            for f in timeline_frames
        ),
        "ocr_frames": [
            {
                "timestamp_sec": f.timestamp_sec,
                "image_path": f.image_path,
                "block_count": len(f.blocks),
                "subtitle_count": len(f.subtitle_blocks),
                "teaching_count": len(f.teaching_blocks),
                "teaching_focus_score": f.teaching_focus_score,
                "teaching_focus_region": f.teaching_focus_region,
                "teaching_texts": [b.text for b in f.teaching_blocks],
            }
            for f in timeline_frames
        ],
        "timeline_visual": timeline_visual,
        "teaching_keyframes": keyframe_paths,
        "subtitle_region": subtitle_region,
        "stats": {
            "scenes_detected": len(scenes),
            "frames_sampled": len(sample_plan),
            "frames_captured": len(frame_paths),
            "frames_ocr": len(timeline_frames),
            "keyframes_selected": len(keyframe_paths),
        },
    }


def _get_transcript_at_time(
    segments: List[Dict],
    timestamp: float,
    padding_sec: float = 1.0,
) -> str:
    """获取 timestamp 时刻的转录文本"""
    texts = []
    for seg in segments:
        seg_start = getattr(seg, "start", 0) if not hasattr(seg, "get") else seg.get("start", 0)
        seg_end = getattr(seg, "end", 0) if not hasattr(seg, "get") else seg.get("end", 0)
        if seg_start - padding_sec <= timestamp <= seg_end + padding_sec:
            texts.append(getattr(seg, "text", "") if not hasattr(seg, "get") else seg.get("text", ""))
    return ' '.join(texts)


def _copy_or_link(src: str, dst: str):
    """复制或硬链接文件"""
    try:
        import shutil
        shutil.copy2(src, dst)
    except OSError:
        pass


def cv2_module():
    """延迟导入 cv2"""
    try:
        import cv2
        return cv2
    except ImportError:
        class FakeCV2:
            VideoCapture = lambda *a: type('obj', (), {
                'get': lambda s, p: 30,
                'set': lambda s, p, v: None,
                'read': lambda s: (False, None),
                'release': lambda s: None,
                'isOpened': lambda s: False,
            })()
            CAP_PROP_FPS = 5
        return FakeCV2()


class _RawFrameResult:
    """阶段A产出的中间帧结果 (OCR完成,交叉验证等segments)"""
    __slots__ = ('timestamp_sec', 'image_path', 'raw_result')
    
    def __init__(self, timestamp_sec: float, image_path: str, raw_result: dict):
        self.timestamp_sec = timestamp_sec
        self.image_path = image_path
        self.raw_result = raw_result
