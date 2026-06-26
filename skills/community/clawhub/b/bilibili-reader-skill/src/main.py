"""主入口 — 串联所有模块，执行完整的视频总结流程"""

import random
import sys
import argparse
from pathlib import Path

from .config import Config
from .bilibili_api import BilibiliAPI, FavoriteFolder
from .summarizer import generate_summary
from .pdf_generator import generate_pdf
from .memory import Memory
from .progress import print_progress, calculate_progress, render_mini_progress
from .topic_graph import load_or_build_graph, TopicGraph


def _get_vector_store():
    """懒加载 VectorStore（避免 ChromaDB 不可用时启动报错）"""
    try:
        from .vector_store import get_vector_store, VectorStore
        return get_vector_store(Config.DATA_DIR)
    except ImportError:
        return None


def select_folder(folders: list[FavoriteFolder]) -> FavoriteFolder:
    """选择收藏夹（多个时询问用户）"""
    if len(folders) == 1:
        print(f"只有一个收藏夹: {folders[0].title} ({folders[0].media_count}个视频)")
        return folders[0]

    print("\n你的收藏夹列表:")
    for i, f in enumerate(folders, 1):
        print(f"  {i}. {f.title} ({f.media_count}个视频)")

    while True:
        try:
            choice = input("\n请选择收藏夹编号 (输入数字): ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(folders):
                return folders[idx]
            print(f"请输入 1-{len(folders)} 之间的数字")
        except ValueError:
            print("请输入有效的数字")
        except (EOFError, KeyboardInterrupt):
            print("\n已取消")
            sys.exit(0)


def _pick_next_video(
    api: BilibiliAPI,
    folder: FavoriteFolder,
    memory: Memory,
    data_dir: Path,
) -> FavoriteFolder:
    """
    基于学习路径 + 向量相似度选择下一个视频。
    优先级：Topic 依赖图 > 向量相似度 > 随机
    """
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

    if not all_videos:
        raise Exception(f"收藏夹 '{folder.title}' 中没有视频")

    unprocessed = [v for v in all_videos if not memory.is_processed(v.bvid)]

    if not unprocessed:
        raise Exception(f"收藏夹 '{folder.title}' 中的视频都已处理过")

    mastered_bvids = {v.bvid for v in memory.get_all_processed()}
    candidate_bvids = {v.bvid for v in unprocessed}

    # 1. 尝试 Topic 依赖图
    graph = load_or_build_graph(data_dir)
    path = graph.get_learning_path(
        mastered_bvids=mastered_bvids,
        candidate_bvids=candidate_bvids,
        max_results=1,
    )
    if path:
        recommended = path[0]
        target = next((v for v in unprocessed if v.bvid == recommended.bvid), None)
        if target:
            print(f"\n📚 基于知识图谱推荐: {target.title}")
            print(f"   💡 {recommended.reason}")
            return target

    # 2. 尝试向量相似度（推荐与已看视频相似的）
    vector_store = _get_vector_store()
    if vector_store is not None:
        processed_videos = memory.get_all_processed()
        if processed_videos:
            # 取最近处理的视频作为 query
            last = processed_videos[-1]
            results = vector_store.search(
                query=getattr(last, "summary_cn", "") or getattr(last, "title", ""),
                top_k=3,
                lang="cn",
            )
            for r in results:
                if r.bvid in candidate_bvids:
                    target = next(v for v in unprocessed if v.bvid == r.bvid)
                    print(f"\n🔍 基于语义相似推荐: {target.title}")
                    print(f"   💡 与「{last.title}」主题相关")
                    return target

    # 3. 随机 fallback
    chosen = random.choice(unprocessed)
    print(f"\n🎲 随机选中: {chosen.title}")
    return chosen


def _build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="B站收藏夹视频智能总结",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--search", "-s",
        metavar="QUERY",
        dest="search_query",
        help="在已处理的视频中搜索语义相关内容（需安装 chromadb）",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="显示向量库统计信息",
    )
    parser.add_argument(
        "--progress",
        action="store_true",
        help="查看收藏夹考古进度（成就系统）",
    )
    return parser


def run(llm_caller=None, args=None):
    """
    执行完整的视频总结流程

    Args:
        llm_caller: LLM调用函数，接收prompt返回response_text
        args: argparse.Namespace 或 None
    """
    parsed_args = args or _build_argument_parser().parse_args([])

    # ── 搜索模式 ──
    if parsed_args.search_query:
        _run_search(parsed_args.search_query)
        return

    # ── 统计模式 ──
    if parsed_args.stats:
        _run_stats()
        return

    # ── 考古进度模式 ──
    if parsed_args.progress:
        _run_progress()
        return

    # ── 正常处理流程 ──
    return _run_process(llm_caller)


def _run_search(query: str):
    """语义搜索模式"""
    vector_store = _get_vector_store()
    if vector_store is None:
        print("❌ ChromaDB 未安装，无法进行语义搜索")
        print("  运行 pip install chromadb 安装后重试")
        return

    print(f"🔍 搜索: {query}")
    print("-" * 50)

    results = vector_store.search(query=query, top_k=5, lang="cn")
    if not results:
        print("未找到相关视频（可能尚未处理任何视频）")
        return

    for i, r in enumerate(results, 1):
        source_tag = "🔎" if r.source == "vector" else "📝"
        print(f"{i}. {source_tag} {r.title}")
        print(f"   体裁: {r.genre}  |  相似度: {r.score:.2f}")
        if r.tldr_cn:
            print(f"   {r.tldr_cn[:60]}{'...' if len(r.tldr_cn) > 60 else ''}")
        print()


def _run_stats():
    """显示向量库统计"""
    vector_store = _get_vector_store()
    if vector_store is None:
        print("ChromaDB 未安装")
        return

    stats = vector_store.stats()
    print("📊 向量库统计")
    print("-" * 50)
    print(f"  ChromaDB 可用: {'✅ 是' if stats['chroma_available'] else '❌ 否'}")
    print(f"  向量总数: {stats['total_vectors']}")
    print(f"  存储路径: {stats['persist_path']}")

    # Memory 统计
    memory = Memory(Config.DATA_DIR / "processed.json")
    print(f"  已处理视频: {memory.get_processed_count()}")


def _run_progress():
    """查看考古进度和成就"""
    Config.ensure_dirs()
    memory = Memory(Config.DATA_DIR / "processed.json")

    # 尝试获取收藏夹信息以计算百分比
    total_in_folder = 0
    folder_name = ""
    try:
        from .bilibili_api import BilibiliAPI
        api = BilibiliAPI(
            sessdata=Config.BILIBILI_SESSDATA,
            bili_jct=Config.BILIBILI_BILI_JCT,
            buvid3=Config.BILIBILI_BUVID3,
        )
        folders = api.get_favorites_list()
        if folders:
            # 默认显示第一个收藏夹的进度
            folder = folders[0]
            folder_name = folder.title
            total_in_folder = folder.media_count
    except Exception:
        pass

    print_progress(
        memory,
        folder_name=folder_name,
        total_in_folder=total_in_folder,
        data_dir=Config.DATA_DIR,
    )


def _run_process(llm_caller):
    """核心处理流程"""
    # 1. 验证配置
    missing = Config.validate()
    if missing:
        print(f"错误: 缺少配置项: {', '.join(missing)}")
        print("请在 .env 文件中配置B站Cookie")
        print("参考 .env.example")
        return None

    Config.ensure_dirs()

    # 2. 初始化模块
    api = BilibiliAPI(
        sessdata=Config.BILIBILI_SESSDATA,
        bili_jct=Config.BILIBILI_BILI_JCT,
        buvid3=Config.BILIBILI_BUVID3,
    )
    memory = Memory(Config.DATA_DIR / "processed.json")

    print("=" * 50)
    print("B站收藏夹视频智能总结")
    print("=" * 50)
    print(f"已处理视频: {memory.get_processed_count()} 个")

    # 3. 获取收藏夹
    print("\n正在获取收藏夹列表...")
    try:
        folders = api.get_favorites_list()
    except Exception as e:
        print(f"获取收藏夹失败: {e}")
        print("请检查Cookie是否正确且未过期")
        return None

    if not folders:
        print("没有找到收藏夹")
        return None

    # 4. 选择收藏夹
    folder = select_folder(folders)
    print(f"\n已选择: {folder.title}")

    # 5. 选择视频（学习路径 + 向量相似度 + 随机）
    print("\n正在选取下一个视频...")
    try:
        video = _pick_next_video(api, folder, memory, Config.DATA_DIR)
    except Exception as e:
        print(f"选取视频失败: {e}")
        return None

    print(f"  UP主: {video.owner}")
    remaining = sum(1 for v in api.get_videos_from_folder(folder.id, page_size=999) if not memory.is_processed(v.bvid))
    print(f"  剩余未处理: {remaining}/{folder.media_count}")

    # 6. 获取视频详细信息
    print("\n正在获取视频详情...")
    try:
        video_detail = api.get_video_detail(video.bvid)
    except Exception as e:
        print(f"获取视频详情失败: {e}")
        return None

    # 7. 获取字幕
    subtitles = []
    if video_detail.subtitle_url:
        print("正在下载字幕...")
        try:
            subtitles = api.get_subtitles(video_detail.subtitle_url)
            print(f"  获取到 {len(subtitles)} 条字幕")
        except Exception as e:
            print(f"  字幕获取失败: {e}")
    else:
        print("  该视频没有字幕")

    # 8. 获取高赞评论
    print("正在获取高赞评论...")
    try:
        comments = api.get_top_comments(video_detail.aid, limit=Config.MAX_COMMENTS)
        print(f"  获取到 {len(comments)} 条评论")
    except Exception as e:
        print(f"  评论获取失败: {e}")
        comments = []

    # 9. 获取弹幕
    print("正在获取弹幕...")
    try:
        danmakus = api.get_danmakus(video_detail.cid, limit=Config.MAX_DANMAKUS)
        print(f"  获取到 {len(danmakus)} 条弹幕")
    except Exception as e:
        print(f"  弹幕获取失败: {e}")
        danmakus = []

    # 10. 生成总结
    print("\n正在生成总结...")
    summary = generate_summary(
        video=video_detail,
        subtitles=subtitles,
        comments=comments,
        danmakus=danmakus,
        llm_caller=llm_caller,
    )

    # 11. 向量化（ChromaDB，懒加载）
    vector_store = _get_vector_store()
    if vector_store is not None:
        print("正在向量化...")
        try:
            vector_store.on_video_processed(summary, video.bvid, video.title)
            print("  ✅ 已存入向量库")
        except Exception as e:
            print(f"  向量化失败（不影响流程）: {e}")

    # 12. 注册 Topic 图谱
    if summary.my_analysis and hasattr(summary.my_analysis, "concepts"):
        graph = load_or_build_graph(Config.DATA_DIR)
        topic_names = [
            c.name for c in summary.my_analysis.concepts
            if hasattr(c, "name") and c.name
        ]
        if topic_names:
            graph.register_video(video.bvid, video.title, topic_names)
            if hasattr(summary, "prerequisites_cn") and summary.prerequisites_cn:
                graph.infer_dependencies_from_summary(video.bvid, summary.prerequisites_cn)
            graph.save(Config.DATA_DIR / "topic_graph.json")

    # 13. 记录已处理
    memory.mark_processed(video.bvid, video.title, summary=summary)
    print(f"已记录为已处理视频")

    # 14. 生成PDF
    print("正在生成PDF...")
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

    stats = memory.get_stats()
    print(f"累计处理: {stats['total_processed']} 个视频")

    # 15. 展示考古进度
    print_progress(
        memory,
        folder_name=folder.title,
        total_in_folder=folder.media_count,
        data_dir=Config.DATA_DIR,
    )

    # 16. 推送指令
    _print_delivery_instruction(pdf_path, summary.title_cn)

    return pdf_path


def _print_delivery_instruction(pdf_path: Path, title: str):
    """输出推送指令，供 agent 解析后投递到对应平台"""
    platform = Config.DELIVERY_PLATFORM.lower()
    if platform == "none" or not platform:
        return

    platform_names = {
        "wechat": "微信",
        "feishu": "飞书",
        "telegram": "Telegram",
        "discord": "Discord",
        "slack": "Slack",
        "whatsapp": "WhatsApp",
    }
    platform_cn = platform_names.get(platform, platform)

    print(f"\n{'='*50}")
    print(f"[DELIVERY] 请将以下内容推送到{platform_cn}:")
    print(f"[DELIVERY] 文件: {pdf_path}")
    print(f"[DELIVERY] 消息: B站视频总结已生成 —— {title}")
    print(f"[DELIVERY] 格式: 发送PDF文件 + 一句话TLDR摘要")
    print(f"{'='*50}")


if __name__ == "__main__":
    parser = _build_argument_parser()
    args = parser.parse_args()
    run(args=args)
