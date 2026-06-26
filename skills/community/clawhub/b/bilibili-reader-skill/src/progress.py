"""收藏夹考古 — 进度可视化 + 学习路径推荐"""

import random
from pathlib import Path
from dataclasses import dataclass, field
from .memory import Memory
from .topic_graph import TopicGraph, LearningPathItem, load_or_build_graph


@dataclass
class ProgressStats:
    total_processed: int = 0
    total_in_folder: int = 0
    percentage: float = 0.0
    genres: dict[str, int] = field(default_factory=dict)  # {genre_display: count}
    streak_days: int = 0
    top_genres: list[tuple[str, int]] = field(default_factory=list)
    topic_stats: dict = field(default_factory=dict)  # Topic 图谱统计


def calculate_progress(
    memory: Memory,
    total_in_folder: int = 0,
    data_dir: Path | None = None,
) -> ProgressStats:
    """计算进度统计"""
    processed = memory.get_all_processed()
    total = len(processed)

    # 统计体裁分布
    genres: dict[str, int] = {}
    for v in processed:
        g = v.genre or "📚 未知"
        genres[g] = genres.get(g, 0) + 1

    # 按数量排序
    top_genres = sorted(genres.items(), key=lambda x: x[1], reverse=True)

    # 计算百分比
    percentage = 0.0
    if total_in_folder > 0:
        percentage = (total / total_in_folder) * 100

    # Topic 图谱统计
    topic_stats = {}
    if data_dir:
        graph = load_or_build_graph(data_dir)
        topic_stats = graph.get_topic_stats()

    return ProgressStats(
        total_processed=total,
        total_in_folder=total_in_folder,
        percentage=percentage,
        genres=genres,
        top_genres=top_genres,
        topic_stats=topic_stats,
    )


def select_next_video(
    memory: Memory,
    folder_videos: list,
    data_dir: Path | None = None,
) -> dict | None:
    """
    基于学习路径推荐下一个视频，而非随机选择

    Args:
        memory: 记忆模块（已处理视频记录）
        folder_videos: 当前收藏夹所有视频的 VideoInfo 列表
        data_dir: 数据目录（用于加载 TopicGraph）

    Returns:
        推荐的下一个视频 dict，包含 title 和 reason
    """
    # 获取未处理的视频
    unprocessed = [v for v in folder_videos if not memory.is_processed(v.bvid)]
    if not unprocessed:
        return None

    mastered_bvids = {v.bvid for v in memory.get_all_processed()}
    candidate_bvids = {v.bvid for v in unprocessed}

    # 加载 TopicGraph
    if data_dir:
        graph = load_or_build_graph(data_dir)
        path = graph.get_learning_path(
            mastered_bvids=mastered_bvids,
            candidate_bvids=candidate_bvids,
            max_results=1,
        )
        if path:
            recommended = path[0]
            # 从 folder_videos 中找到对应 VideoInfo
            target = next((v for v in unprocessed if v.bvid == recommended.bvid), None)
            if target:
                return {
                    "bvid": target.bvid,
                    "title": getattr(target, "title", recommended.title),
                    "reason": recommended.reason,
                    "topic": recommended.topic,
                }

    # 冷启动 fallback：随机选择
    chosen = random.choice(unprocessed)
    return {
        "bvid": chosen.bvid,
        "title": getattr(chosen, "title", chosen.bvid),
        "reason": "随机选择（知识图谱尚无足够数据）",
        "topic": "",
    }


def render_learning_path_banner(recommendation: dict) -> str:
    """渲染学习路径推荐横幅"""
    if not recommendation:
        return ""
    topic = recommendation.get("topic", "")
    topic_line = f"  📚 主题：{topic}" if topic else ""
    return f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🎯 学习路径推荐
  「{recommendation.get('title', '')}」
{topic_line}
  💡 理由：{recommendation.get('reason', '')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""


def render_progress(stats: ProgressStats, folder_name: str = "") -> str:
    """渲染命令行进度展示"""
    lines = []
    lines.append("")
    lines.append("=" * 50)
    lines.append("  🗺️  收藏夹考古进度")
    if folder_name:
        lines.append(f"  📁 收藏夹: {folder_name}")
    lines.append("=" * 50)

    # 进度条
    if stats.total_in_folder > 0:
        bar_width = 30
        filled = int(bar_width * stats.percentage / 100)
        empty = bar_width - filled
        bar = "█" * filled + "░" * empty
        lines.append(f"\n  {bar}  {stats.percentage:.0f}%")
        lines.append(f"  已消化 {stats.total_processed}/{stats.total_in_folder} 个视频")
    else:
        lines.append(f"\n  已消化 {stats.total_processed} 个视频")

    # Topic 图谱
    if stats.topic_stats and stats.topic_stats.get("total_topics", 0) > 0:
        lines.append(f"\n  🧠 Topic 图谱：{stats.topic_stats['total_topics']} 个主题，{stats.topic_stats['total_videos']} 部视频")
        top = stats.topic_stats.get("topic_list", [])[:5]
        if top:
            lines.append("  热门主题：")
            for item in top:
                lines.append(f"    · {item['name']} ({item['video_count']} 部)")

    # 体裁分布
    if stats.top_genres:
        lines.append("\n  📊 知识图谱:")
        max_count = stats.top_genres[0][1] if stats.top_genres else 1
        for genre, count in stats.top_genres:
            bar_len = int(15 * count / max_count) if max_count > 0 else 1
            bar = "█" * bar_len
            lines.append(f"    {genre:<16} {bar} {count}")

    # 成就系统
    achievements = _check_achievements(stats)
    if achievements:
        lines.append("\n  🏆 成就:")
        for ach in achievements:
            lines.append(f"    {ach}")

    lines.append("")
    lines.append("=" * 50)

    return "\n".join(lines)


def render_mini_progress(stats: ProgressStats) -> str:
    """渲染迷你进度条（用于PDF底部等空间有限的地方）"""
    if stats.total_in_folder > 0:
        bar_width = 20
        filled = int(bar_width * stats.percentage / 100)
        empty = bar_width - filled
        bar = "█" * filled + "░" * empty
        return f"收藏夹考古: {bar} {stats.percentage:.0f}% ({stats.total_processed}/{stats.total_in_folder})"
    return f"收藏夹考古: 已消化 {stats.total_processed} 个视频"


def _check_achievements(stats: ProgressStats) -> list[str]:
    """检查解锁的成就"""
    achievements = []
    total = stats.total_processed

    # 数量成就
    milestones = [
        (1, "🌱 初次发掘 — 消化了第一个视频"),
        (5, "🔍 考古新手 — 消化 5 个视频"),
        (10, "⛏️ 考古学徒 — 消化 10 个视频"),
        (25, "🗺️ 地图绘制者 — 消化 25 个视频"),
        (50, "🏛️ 知识守护者 — 消化 50 个视频"),
        (100, "👑 收藏夹征服者 — 消化 100 个视频"),
    ]
    for threshold, desc in milestones:
        if total >= threshold:
            achievements.append(desc)

    # 体裁成就
    genre_achievements = {
        "💻": ("🔧 技术工匠", "技术教程类消化 5+ 个"),
        "🎓": ("📖 学霸", "学科教育类消化 5+ 个"),
        "🗣️": ("🌍 语言达人", "语言学习类消化 5+ 个"),
        "🔬": ("🧪 深度思考者", "深度解析类消化 5+ 个"),
        "🧠": ("💡 方法论大师", "方法论类消化 5+ 个"),
        "💼": ("👔 职场达人", "职场技能类消化 5+ 个"),
        "🎨": ("🎨 创意工匠", "艺术创造类消化 5+ 个"),
        "📖": ("📚 知识管理师", "书籍拆解类消化 5+ 个"),
        "🛠️": ("🔧 生活达人", "生活技能类消化 5+ 个"),
    }
    for genre, count in stats.genres.items():
        for prefix, (name, req) in genre_achievements.items():
            if prefix in genre and count >= 5:
                achievements.append(f"{name} — {req}")

    # 多样性成就
    if len(stats.genres) >= 5:
        achievements.append("🌈 博览群书 — 覆盖 5+ 种体裁")
    if len(stats.genres) >= 8:
        achievements.append("🎯 全能选手 — 覆盖 8+ 种体裁")

    # Topic 图谱成就
    if stats.topic_stats.get("total_topics", 0) >= 10:
        achievements.append("🗺️ 图谱构建者 — 建立 10+ Topic 知识图谱")

    return achievements


def print_progress(
    memory: Memory,
    folder_name: str = "",
    total_in_folder: int = 0,
    data_dir: Path | None = None,
):
    """直接打印进度"""
    stats = calculate_progress(memory, total_in_folder, data_dir)
    print(render_progress(stats, folder_name))
