"""分析模块

提供数据准备和报告生成功能。
"""

from typing import Any, Dict, List, Optional
from datetime import datetime

from .search import SearchRecord, SearchResult, get_post_detail, FeedDetail, DiscussDetail
from .utils import load_prompt, format_timestamp, get_tag_name


def prepare_summary(
    search_results: Dict[str, SearchResult],
    config: Dict[str, Any],
    fetch_details: bool = True
) -> Dict[str, Any]:
    """准备面经报告数据

    自动加载提示词模板并填充数据。

    Args:
        search_results: 搜索结果字典（关键词 -> SearchResult）
        config: 用户配置
        fetch_details: 是否获取帖子详情（正文内容）

    Returns:
        包含上下文、提示词和指令的字典
    """
    # 加载提示词模板
    prompt_template = load_prompt("report_summary")

    # 统计总帖子数
    total_count = sum(result.size for result in search_results.values())

    # 构建帖子数据
    posts_data = []
    for keyword, result in search_results.items():
        posts_data.append(f"\\n### 关键词: {keyword}\n")
        posts_data.append(f"找到 {result.size} 篇帖子（共 {result.total} 篇）\n")

        for idx, record in enumerate(result.records, 1):
            # 获取帖子详情
            detail = None
            if fetch_details:
                try:
                    detail = get_post_detail(record)
                except Exception:
                    pass

            post_info = format_post_record(record, idx, detail)
            posts_data.append(post_info)

    posts_text = "\n".join(posts_data)

    # 准备上下文数据
    context = {
        "keywords": ", ".join(search_results.keys()),
        "time_window_days": config.get("time_window_days", 7),
        "total_count": total_count,
        "search_results": {
            k: {
                "size": v.size,
                "total": v.total,
                "records": [
                    {
                        "title": r.title,
                        "rc_type": r.rc_type,
                        "uuid": r.uuid,
                        "content_id": r.content_id,
                        "created_at": r.created_at,
                        "view_count": r.view_count,
                        "like_count": r.like_count,
                        "comment_count": r.comment_count,
                        "company": r.company,
                        "job_title": r.job_title,
                    }
                    for r in v.records
                ]
            }
            for k, v in search_results.items()
        }
    }

    # 根据语言设置生成指令
    language = config.get("language", "zh")
    language_instruction = get_language_instruction(language)

    # 填充提示词
    prompt = prompt_template.format(
        keywords=context["keywords"],
        time_window_days=context["time_window_days"],
        total_count=total_count,
        posts_data=posts_text,
        language_instruction=language_instruction
    )

    return {
        "context": context,
        "prompt": prompt,
        "instruction": "请使用上述提示词和数据生成面经报告"
    }


def format_post_record(record: SearchRecord, index: int, detail: Optional[FeedDetail | DiscussDetail] = None) -> str:
    """格式化单条帖子记录

    Args:
        record: 搜索记录
        index: 序号
        detail: 帖子详情（可选）

    Returns:
        格式化的文本
    """
    lines = [
        f"\n**{index}. {record.title}**",
        f"- 类型: {'Feed动态' if record.rc_type == 201 else '讨论帖'}",
        f"- 发布时间: {format_timestamp(record.created_at)}",
        f"- 浏览/点赞/评论: {record.view_count} / {record.like_count} / {record.comment_count}",
    ]

    if record.company or record.job_title:
        auth_info = f"- 认证: {record.company}"
        if record.job_title:
            auth_info += f" - {record.job_title}"
        lines.append(auth_info)

    # 添加链接
    if record.rc_type == 201:
        lines.append(f"- 链接: https://www.nowcoder.com/feed/main/detail/{record.uuid}")
    else:
        lines.append(f"- 链接: https://www.nowcoder.com/discuss/{record.content_id}")

    # 添加正文内容
    if detail:
        content = detail.content if hasattr(detail, 'content') else ""
        if content:
            # 截断过长的内容（最多 5000 字符）
            if len(content) > 5000:
                content = content[:5000] + "\n...[内容已截断]"
            lines.append(f"\n**正文内容**:\n{content}")

    return "\n".join(lines)


def get_language_instruction(language: str) -> str:
    """获取语言设置指令

    Args:
        language: 语言代码

    Returns:
        语言指令文本
    """
    if language == "zh":
        return "\n**语言要求**: 请使用中文生成报告"
    elif language == "en":
        return "\n**语言要求**: Please generate the report in English"
    elif language == "bilingual":
        return "\n**语言要求**: 请生成双语报告（先中文后英文）"
    else:
        return "\n**语言要求**: 请使用中文生成报告"


def get_top_posts(
    search_results: Dict[str, SearchResult],
    top_n: int = 10,
    by: str = "view_count"
) -> List[SearchRecord]:
    """获取热门帖子

    Args:
        search_results: 搜索结果
        top_n: 返回数量
        by: 排序依据（view_count, like_count, comment_count）

    Returns:
        排序后的帖子列表
    """
    all_records = []
    for result in search_results.values():
        all_records.extend(result.records)

    # 排序
    if by == "view_count":
        all_records.sort(key=lambda r: r.view_count, reverse=True)
    elif by == "like_count":
        all_records.sort(key=lambda r: r.like_count, reverse=True)
    elif by == "comment_count":
        all_records.sort(key=lambda r: r.comment_count, reverse=True)

    return all_records[:top_n]


def calculate_statistics(search_results: Dict[str, SearchResult]) -> Dict[str, Any]:
    """计算统计数据

    Args:
        search_results: 搜索结果

    Returns:
        统计数据字典
    """
    all_records = []
    for result in search_results.values():
        all_records.extend(result.records)

    if not all_records:
        return {
            "total_posts": 0,
            "avg_view_count": 0,
            "avg_like_count": 0,
            "avg_comment_count": 0,
            "top_viewed": None,
            "top_liked": None,
        }

    # 计算平均值
    avg_view = sum(r.view_count for r in all_records) / len(all_records)
    avg_like = sum(r.like_count for r in all_records) / len(all_records)
    avg_comment = sum(r.comment_count for r in all_records) / len(all_records)

    # 找出最热门的帖子
    top_viewed = max(all_records, key=lambda r: r.view_count)
    top_liked = max(all_records, key=lambda r: r.like_count)

    return {
        "total_posts": len(all_records),
        "avg_view_count": int(avg_view),
        "avg_like_count": int(avg_like),
        "avg_comment_count": int(avg_comment),
        "top_viewed": {
            "title": top_viewed.title,
            "view_count": top_viewed.view_count,
        },
        "top_liked": {
            "title": top_liked.title,
            "like_count": top_liked.like_count,
        },
    }
