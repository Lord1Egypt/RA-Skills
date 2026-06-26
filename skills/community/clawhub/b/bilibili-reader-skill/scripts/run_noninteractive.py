#!/usr/bin/env python3
"""非交互式视频总结脚本 — 绕过 main.py 的 input() 问题

用法: cd ~/.hermes/skills/media/bilibili-reader && .venv/bin/python scripts/run_noninteractive.py <收藏夹名称> [latest|random|search <keyword>|<bvid>]

参数:
  收藏夹名称     目标收藏夹标题（精确匹配）
  latest         最新收藏的未处理视频（收藏时间最近，默认）
  random         随机选一个未处理视频
  search <keyword> 搜索已总结记录和未处理视频
  <bvid>         指定 BV 号

示例:
  .venv/bin/python scripts/run_noninteractive.py 代码 latest
  .venv/bin/python scripts/run_noninteractive.py 代码 random
  .venv/bin/python scripts/run_noninteractive.py 代码 search python
  .venv/bin/python scripts/run_noninteractive.py 代码 BV1ZPttzhEDV
"""

import sys
import json
import random
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import Config
from src.bilibili_api import BilibiliAPI
from src.summarizer import generate_summary
from src.pdf_generator import generate_pdf
from src.memory import Memory
from src.progress import print_progress, calculate_progress, render_mini_progress
from src.topic_graph import load_or_build_graph


def _get_vector_store():
    """懒加载 VectorStore"""
    try:
        from src.vector_store import get_vector_store
        return get_vector_store(Config.DATA_DIR)
    except ImportError:
        return None


def main():
    if len(sys.argv) < 2:
        print("用法: python run_noninteractive.py <收藏夹名称> [random|<bvid>]")
        sys.exit(1)

    folder_name = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "latest"

    # 验证配置
    missing = Config.validate()
    if missing:
        print(f"错误: 缺少配置项: {', '.join(missing)}")
        sys.exit(1)

    Config.ensure_dirs()
    api = BilibiliAPI(
        sessdata=Config.BILIBILI_SESSDATA,
        bili_jct=Config.BILIBILI_BILI_JCT,
        buvid3=Config.BILIBILI_BUVID3,
    )
    memory = Memory(Config.DATA_DIR / "processed.json")

    print("=" * 50)
    print("B站收藏夹视频智能总结 (非交互模式)")
    print("=" * 50)

    # 获取收藏夹
    folders = api.get_favorites_list()
    folder = None
    for f in folders:
        if f.title == folder_name:
            folder = f
            break

    if not folder:
        print(f"错误: 找不到收藏夹 '{folder_name}'")
        print(f"可用收藏夹: {', '.join(f.title for f in folders)}")
        sys.exit(1)

    print(f"收藏夹: {folder.title} ({folder.media_count}个视频)")

    # 获取视频列表
    all_videos = []
    page = 1
    while True:
        videos = api.get_videos_from_folder(folder.id, page=page, page_size=20)
        if not videos:
            break
        all_videos.extend(videos)
        if len(videos) < 20:
            break
        page += 1

    # 选择视频
    if mode == "latest":
        unprocessed = [v for v in all_videos if not memory.is_processed(v.bvid)]
        if not unprocessed:
            print("所有视频都已处理过")
            sys.exit(0)
        video_brief = unprocessed[0]
        print(f"最新收藏: {video_brief.title} ({video_brief.bvid})")
    elif mode == "random":
        unprocessed = [v for v in all_videos if not memory.is_processed(v.bvid)]
        if not unprocessed:
            print("所有视频都已处理过")
            sys.exit(0)
        video_brief = random.choice(unprocessed)
        print(f"随机选中: {video_brief.title} ({video_brief.bvid})")
    elif mode == "search":
        keyword = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else ""
        if not keyword:
            print("错误: search 模式需要提供搜索关键词")
            print("用法: python run_noninteractive.py <收藏夹名称> search <keyword>")
            sys.exit(1)

        # 语义搜索（ChromaDB）
        vector_store = _get_vector_store()
        if vector_store is not None:
            print(f"\n语义搜索: {keyword}")
            results = vector_store.search(query=keyword, top_k=5, lang="cn")
            if results:
                print(f"向量库中找到 {len(results)} 个相关内容:")
                for r in results:
                    source_tag = "🔎" if r.source == "vector" else "📝"
                    print(f"  {source_tag} {r.title} (相似度: {r.score:.2f})")
                    if r.tldr_cn:
                        print(f"      {r.tldr_cn[:60]}")
            else:
                print("向量库中未找到匹配")

        # 关键词搜索（processed.json）
        memory_results = memory.search_by_keyword(keyword)
        if memory_results:
            print(f"\n已总结记录中找到 {len(memory_results)} 个匹配:")
            for v in memory_results:
                print(f"  [{v.genre}] {v.title} ({v.bvid})")
                if v.tldr_cn:
                    print(f"    TLDR: {v.tldr_cn}")
        else:
            print("\n已总结记录中没有匹配")

        # 搜索收藏夹未处理视频
        folder_matches = [
            v for v in all_videos
            if not memory.is_processed(v.bvid)
            and keyword.lower() in v.title.lower()
        ]
        if folder_matches:
            print(f"\n收藏夹未处理视频中找到 {len(folder_matches)} 个匹配:")
            for v in folder_matches[:10]:
                print(f"  {v.title} ({v.bvid}) - UP主: {v.owner}")

        sys.exit(0)
    else:
        video_brief = next((v for v in all_videos if v.bvid == mode), None)
        if not video_brief:
            print(f"错误: 收藏夹中找不到 {mode}")
            sys.exit(1)
        print(f"指定视频: {video_brief.title} ({video_brief.bvid})")

    # 获取详情
    print("\n获取视频详情...")
    video = api.get_video_detail(video_brief.bvid)

    # 字幕
    subtitles = []
    if video.subtitle_url:
        print("下载字幕...")
        try:
            subtitles = api.get_subtitles(video.subtitle_url)
            print(f"  获取到 {len(subtitles)} 条字幕")
        except Exception as e:
            print(f"  字幕获取失败: {e}")
    else:
        print("  该视频没有字幕（将基于简介和评论生成总结）")

    # 评论
    print("获取高赞评论...")
    try:
        comments = api.get_top_comments(video.aid, limit=Config.MAX_COMMENTS)
        print(f"  获取到 {len(comments)} 条评论")
    except Exception as e:
        print(f"  评论获取失败: {e}")
        comments = []

    # 弹幕
    print("获取弹幕...")
    try:
        danmakus = api.get_danmakus(video.cid, limit=Config.MAX_DANMAKUS)
        print(f"  获取到 {len(danmakus)} 条弹幕")
    except Exception as e:
        print(f"  弹幕获取失败: {e}")
        danmakus = []

    # 生成总结
    print("\n生成总结...")
    summary = generate_summary(
        video=video,
        subtitles=subtitles,
        comments=comments,
        danmakus=danmakus,
        llm_caller=None,  # 传入 LLM 函数可生成更好的总结
    )

    # 向量化（ChromaDB，懒加载）
    vector_store = _get_vector_store()
    if vector_store is not None:
        try:
            vector_store.on_video_processed(summary, video.bvid, video.title)
            print("  ✅ 已存入向量库")
        except Exception as e:
            print(f"  向量化失败（不影响流程）: {e}")

    # 注册 Topic 图谱
    if hasattr(summary, "my_analysis") and summary.my_analysis:
        concepts = getattr(summary.my_analysis, "concepts", [])
        if concepts:
            graph = load_or_build_graph(Config.DATA_DIR)
            topic_names = [
                c.name for c in concepts
                if hasattr(c, "name") and c.name
            ]
            graph.register_video(video.bvid, video.title, topic_names)
            if hasattr(summary, "prerequisites_cn") and summary.prerequisites_cn:
                graph.infer_dependencies_from_summary(video.bvid, summary.prerequisites_cn)
            graph.save(Config.DATA_DIR / "topic_graph.json")

    # 记录
    memory.mark_processed(video.bvid, video.title, summary=summary)
    print("已记录为已处理视频")

    # 生成 PDF
    print("生成PDF...")
    progress_stats = calculate_progress(
        memory,
        total_in_folder=folder.media_count,
        data_dir=Config.DATA_DIR,
    )
    progress_text = render_mini_progress(progress_stats)
    pdf_path = generate_pdf(
        summary,
        Config.OUTPUT_DIR,
        bvid=video.bvid,
        progress_text=progress_text,
    )
    print(f"\nPDF已生成: {pdf_path}")
    print(f"文件大小: {pdf_path.stat().st_size / 1024:.1f} KB")

    # 考古进度
    print_progress(
        memory,
        folder_name=folder.title,
        total_in_folder=folder.media_count,
        data_dir=Config.DATA_DIR,
    )

    # 推送指令
    platform = Config.DELIVERY_PLATFORM.lower()
    if platform and platform != "none":
        platform_names = {
            "wechat": "微信", "feishu": "飞书", "telegram": "Telegram",
            "discord": "Discord", "slack": "Slack", "whatsapp": "WhatsApp",
        }
        platform_cn = platform_names.get(platform, platform)
        print(f"\n{'='*50}")
        print(f"[DELIVERY] 请将以下内容推送到{platform_cn}:")
        print(f"[DELIVERY] 文件: {pdf_path}")
        print(f"[DELIVERY] 消息: B站视频总结已生成 —— {summary.title_cn}")
        print(f"[DELIVERY] 格式: 发送PDF文件 + 一句话TLDR摘要")
        print(f"{'='*50}")


if __name__ == "__main__":
    main()
