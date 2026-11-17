#!/usr/bin/env python3
"""
BiliYouTik2Brain — 命令行入口

用法:
  # 处理单个视频
  python -m biliyoutik2brain https://www.bilibili.com/video/BVxxx
  
  # 显示信息
  python -m biliyoutik2brain --info https://b23.tv/xxx
  
  # 只评论分析
  python -m biliyoutik2brain --comments https://www.bilibili.com/video/BVxxx
  
  # 列出合集（B站view API）
  python -m biliyoutik2brain --list-collection BVxxx
  
  # 列出已注册平台
  python -m biliyoutik2brain --list-platforms
  
  # 查看资源状态
  python -m biliyoutik2brain --status

  # 查看环境信息
  python -m biliyoutik2brain --env

  # 诊断调度器
  python -m biliyoutik2brain --diagnose

  # 技能自进化报告
  python -m biliyoutik2brain --evolve

  # 列出说话人
  python -m biliyoutik2brain --speakers

  # 搜索已处理视频
  python -m biliyoutik2brain --search "FVG 交易策略"
  python -m biliyoutik2brain --search "张聚贤 止损"
"""

import sys, json, os

from .core.pipeline import process
from .core.config import PlatformRegistry, _load_history
from .core.registry import _init_registry
from .platforms.bilibili import BilibiliExtractor


def _print_search_results(results, keyword: str):
    """格式化输出搜索结果"""
    if not results:
        print(f"\n😕 没有找到与「{keyword}」相关的结果。")
        print("   提示：试试用空格分隔多关键词，或者换一个更短的词。")
        return

    source_labels = {"transcript": "📝 转录", "knowledge": "📚 知识档案",
                     "speaker": "👤 说话人"}
    print(f"\n🔍 搜索「{keyword}」- 共 {len(results)} 条结果:\n")

    for i, r in enumerate(results[:15], 1):
        source_tag = source_labels.get(r.source, r.source)
        score_bar = "█" * max(1, int(r.score * 10))
        print(f"{'='*60}")
        print(f"  #{i}  {source_tag}  |  相关性: {score_bar} ({r.score:.2f})")
        print(f"  UP主: {r.uploader}")
        print(f"  标题: {r.title[:80]}")
        if r.date:
            print(f"  日期: {r.date}")
        if r.bvid:
            print(f"  BV号: {r.bvid}")
        if r.url:
            print(f"  链接: {r.url}")
        print(f"  ──")
        print(f"  {r.snippet[:200]}")
        if r.file_path:
            print(f"  📄 {os.path.basename(r.file_path)}")
        print()


def main():
    # 确保平台注册表初始化（避免导入时序问题）
    _init_registry()
    args = sys.argv[1:]
    
    if not args:
        print(__doc__)
        return
    
    if args[0] == "--list-platforms":
        platforms = PlatformRegistry.list_platforms()
        print("已注册平台适配器:")
        for p in platforms:
            print(f"  - {p.value}")
        return
    
    if args[0] == "--status":
        history = _load_history()
        print(f"云端历史任务: {len(history.get('cloud_tasks', []))} 条")
        print(f"估算容量: {history.get('estimated_capacity', '未知')}")
        print()
        # 列出转录存储
        storage = os.path.expanduser("~/openclaw/workspace/storage/transcripts")
        if os.path.exists(storage):
            files = [f for f in os.listdir(storage) if f.endswith(".md")]
            print(f"转录文件: {len(files)} 个")
        return
    
    if args[0] == "--search":
        keyword = " ".join(args[1:]) if len(args) > 1 else ""
        if not keyword:
            print("用法: python -m biliyoutik2brain --search <关键词>")
            print("示例: python -m biliyoutik2brain --search \"FVG 交易\"")
            return
        from .core.searcher import search
        results = search(keyword)
        _print_search_results(results, keyword)
        return
    
    if args[0] == "--env":
        from .core.env import print_profile
        print_profile()
        return
    
    if args[0] == "--evolve":
        from .core.self_evolve import report
        print(report())
        return
    
    if args[0] == "--dry-run":
        _dry_run_test()
        return
    
    if args[0] == "--diagnose":
        from .core.scheduler import diagnose
        diagnose()
        return
    
    if args[0] == "--speakers":
        from .core.speaker_knowledge import list_all_speakers
        speakers = list_all_speakers()
        if not speakers:
            print("还没有说话人记录。处理视频后自动积累。")
        else:
            print(f"已记录 {len(speakers)} 位说话人:\n")
            for s in speakers:
                ac = s.get('platforms', {})
                plat_str = ' | '.join(f"{p}:{u}" for p, u in ac.items()) if ac else '无平台'
                print(f"  👤 {s['key']} (real={s['real_name']})")
                print(f"     平台: {plat_str} | 视频: {s['video_count']} | 领域: {s['domain']}")
        return
    
    if args[0] == "--info":
        url = args[1]
        extractor_cls = PlatformRegistry.identify(url)
        platform_name = extractor_cls.platform.value if extractor_cls else "未知"
        print(f"URL: {url}")
        print(f"平台: {platform_name}")
        return
    
    if args[0] == "--comments":
        url = args[1]
        from .core.pipeline import collect
        collected = collect(url)
        if collected.comments.success:
            print(f"评论数: {collected.comments.total}")
            for ins in collected.comments.insights:
                print(f"  📊 {ins}")
        else:
            print(f"评论获取失败: {collected.comments.error}")
        return
    
    if args[0] == "--list-collection":
        bvid = args[1]
        episodes = BilibiliExtractor.list_collection(bvid)
        if not episodes:
            print("该视频不在合集中，或合集为空。")
        else:
            print(f"合集共 {len(episodes)} 集:\n")
            for i, ep in enumerate(episodes, 1):
                dur_m, dur_s = divmod(ep["duration"], 60)
                print(f"  {i:2d}. {ep['title']}")
                print(f"      BV: {ep['bvid']}  |  时长: {dur_m}:{dur_s:02d}")
        return
    
  # 默认: 完整处理 (v3.0新管线)
    url = args[0]
    _process_v3(url)


def _process_v3(url: str):
    """v3.0 置信度驱动管线: collect → ASR → confidence_pipeline → output → IMA"""
    from .core.pipeline import collect
    from .core.collector import CollectionResult, decide_strategy
    from .core.env import detect
    from .core.speaker_knowledge import format_context, format_asr_hints

    env = detect()
    print(f"🚀 v3.0管线启动 | {env.profile_summary}")

    # 1) 采集
    try:
        collected = collect(url)
    except Exception as e:
        print(f"\n❌ 采集失败: {e}")
        return

    video = collected.video if collected else None
    if not video or not video.video_id:
        print("\n❌ 无法获取视频信息")
        return
    print(f"\n📹 {video.title[:60]}")
    print(f"   UP主: {video.uploader} | 时长: {video.duration}s | 平台: {video.platform.value}")

    # 2) 采集策略决策
    subtitle_ok = collected.subtitle and collected.subtitle.success if hasattr(collected, 'subtitle') else False
    audio_ok = collected.audio and collected.audio.success and collected.audio.file_path if hasattr(collected, 'audio') else False
    
    from .core.collector import CollectionResult, decide_strategy
    cr = CollectionResult(
        url=url, video_title=video.title, uploader=video.uploader,
        duration_s=video.duration,
        subtitle_available=subtitle_ok,
        subtitle_text=collected.subtitle.text if subtitle_ok else "",
        audio_path=collected.audio.file_path if audio_ok else "",
    )
    strategy = decide_strategy(cr)
    print(f"   采集策略: {strategy} ({cr.strategy_reason})")

    # 3) 转录 (如有字幕则跳过)
    if strategy == "subtitle":
        from .core.asr import ASRResult
        asr_result = ASRResult(
            full_text=cr.subtitle_text,
            engine="api_subtitle",
            has_token_confidence=False,
        )
        print(f"   ✅ 使用API字幕: {len(cr.subtitle_text)}字")
    elif audio_ok:
        from .core.asr import transcribe, resolve_model_size
        # 根据环境选模型，如果本地没缓存会自动 fallback 到已缓存的
        preferred = "base" if env.cpu_cores >= 8 else "tiny"
        model_size = resolve_model_size(preferred)
        asr_result = transcribe(cr.audio_path, model_size=model_size)
    else:
        print("   ⚠️ 无音频源, 尝试从视频提取...")
        # 回退: 让bfs知道需要先下载视频
        print("   ℹ️ 请先用 yt-dlp 或 B站客户端下载视频音频")
        return
    
    # 4) 说话人上下文
    speaker_ctx = format_context(video.uploader, video.title)
    asr_hints = format_asr_hints(video.uploader)
    
    # 5) OCR 抽帧（与 ASR 并行，视频→画面文字→第二条信息通道）
    ocr_timeline = []
    video_path = getattr(collected, 'video_file', '') if collected else ''
    if video_path and os.path.exists(video_path):
        from .core.node_ocr_v2 import node_ocr_v2 as run_ocr_v2
        from dataclasses import dataclass
        # 构造 OCR v2 需要的上下文字典
        ocr_ctx = {
            "collect": collected,
            "transcribe": {
                "segments": getattr(asr_result, 'segments', []),
                "low_conf_words": getattr(asr_result, 'low_confidence_words', []),
            },
            "video_path": video_path,
            "video_id": video.video_id,
            "duration_s": video.duration,
        }
        ocr_result = run_ocr_v2(**ocr_ctx)
        ocr_timeline = ocr_result.get('ocr_timeline', [])
        if ocr_timeline:
            print(f"  [OCR] ✅ 提取 {len(ocr_timeline)} 段画面文字")
        elif ocr_result.get('ocr_applied'):
            print(f"  [OCR] ✅ OCR已完成，交叉验证中")
    
    # 6) 置信度驱动管线
    from .core.confidence_pipeline import process as pipeline_process
    pipeline_result = pipeline_process(
        asr_result=asr_result,
        video_title=video.title,
        uploader=video.uploader,
        speaker_context=speaker_ctx,
        correction_hints=asr_hints,
        ocr_timeline=ocr_timeline,
    )
    
    # 7) 三格式输出
    from .core.formatter import format_all as fmt_all
    from .core.speaker_knowledge import get_profile
    profile = get_profile(video.uploader)
    fmt_result = fmt_all(
        title=video.title, uploader=video.uploader, url=url,
        video_id=video.video_id,
        corrected_text=pipeline_result.full_text,
        analysis=pipeline_result.analysis.__dict__ if hasattr(pipeline_result.analysis, '__dict__') else {},
        corrections=pipeline_result.chunks[0].__dict__ if pipeline_result.chunks else {},
        error_categories=profile.get('error_categories', {}),
        low_conf_regions=asr_result.low_confidence_regions,
        domain=profile.get('domain', ''),
        pipeline_time=pipeline_result.elapsed_s,
    )
    
    # 7) IMA推送
    from .core.ima_bridge import push_to_ima
    push_to_ima(
        title=video.title, content=pipeline_result.full_text,
        keywords=pipeline_result.analysis.keywords if hasattr(pipeline_result.analysis, 'keywords') else [],
        uploader=video.uploader, url=url, domain=profile.get('domain', ''),
    )
    
    # 8) 更新说话人知识库 (含特征学习)
    from .core.speaker_knowledge import update_after_video
    update_after_video(
        speaker=video.uploader, video_title=video.title,
        bvid=video.video_id, video_duration=video.duration,
        analysis=pipeline_result.analysis.__dict__ if hasattr(pipeline_result.analysis, '__dict__') else {},
        corrected_text=pipeline_result.full_text,
        platform=video.platform.value if hasattr(video.platform, 'value') else '',
    )
    
    print(f"\n✅ v3.0处理完成: {pipeline_result.elapsed_s:.1f}s")
    print(f"   笔记: {os.path.basename(fmt_result.note)}")
    print(f"   卡片: {os.path.basename(fmt_result.card)}")
    if fmt_result.errors:
        print(f"   错题: {os.path.basename(fmt_result.errors)}")


def _dry_run_test():
    """干跑测试: 验证全链路逻辑而不调用外部API"""
    print("🧪 干跑测试 — 验证v3.0全链路")
    print("=" * 50)
    
    # 1) 环境检测
    from .core.env import detect
    env = detect()
    print(f"✅ env: {env.profile_summary}")
    
    # 2) 调度器
    from .core.scheduler import decide, prioritize, Task as STask
    tasks = [STask("test", "BV001", "FVG教程", 600),
             STask("test", "BV002", "缠论高级", 1800)]
    d = decide(tasks, env)
    print(f"✅ scheduler: {d.reason}")
    
    # 3) 搜索
    from .core.searcher import search
    results = search("FVG")
    print(f"✅ searcher: {len(results)} 条结果")
    
    # 4) 格式化器
    from .core.formatter import format_note
    note = format_note("测试", "张聚贤", "url", "文本"*5,
        {"summary": "测试摘要", "keywords": ["FVG"], "topics": ["交易"]})
    print(f"✅ formatter: {len(note)}字笔记")
    
    # 5) 说话人
    from .core.speaker_knowledge import format_asr_hints
    hints = format_asr_hints("测试") or "无"
    print(f"✅ speaker: {hints}")
    
    # 6) ASR检测
    from .core.asr import check_available
    eng = check_available()
    print(f"✅ asr: {eng or '无引擎(需pip install)'}")
    
    # 7) LLM检测
    from .core.llm import check_available as llm_check
    be = llm_check()
    print(f"✅ llm: {be}")
    
    print("=" * 50)
    print("✅ v3.0全链路干跑通过")


if __name__ == "__main__":
    main()
