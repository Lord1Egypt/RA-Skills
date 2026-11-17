"""
BiliYouTik2Brain — 评论分析节点

职责单一：调用 comment_analyzer 分析采集到的评论。
与 transcribe/ocr/bleep 并行执行，不卡主流程。
失败时 continue_on_error=True，不影响转录保存。
"""

from typing import Dict
from .schemas import CollectResult, CommentResult
from .comment_analyzer import analyze_comments, format_comments_report


def _node_comment_analyze(**kw) -> Dict:
    """节点：评论分析

    从 collect 结果中提取评论数据，进行语义级分析。
    """
    collect_result: CollectResult = kw.get("collect")
    if collect_result is None:
        print("  [评论] ⚠️ 无采集结果，跳过")
        return {"success": False, "error": "无采集结果"}

    comment_result: CommentResult = collect_result.comments
    if not comment_result or not comment_result.success:
        print("  [评论] ⚠️ 无评论数据，跳过")
        return {"success": False, "error": "无评论数据"}

    # 获取UP主信息用于识别UP主发言
    video = collect_result.video
    uploader_id = video.uploader_id if video else ""
    uploader = video.uploader if video else ""
    platform = video.platform.value if video else "unknown"

    print(f"  [评论] 🔍 分析 {comment_result.total} 条评论...")

    analysis = analyze_comments(
        comment_result=comment_result,
        platform=platform,
        up_author_id=uploader_id,
    )

    if analysis.get("success"):
        print(f"  [评论] ✅ 完成: {analysis['stats']['after_filter']}/{analysis['stats']['total_raw']}条保留"
              f"（过滤{analysis['stats']['filtered_out']}条）")
        if analysis.get("up_author_comments"):
            print(f"  [评论] 🎙️ UP主参与: {len(analysis['up_author_comments'])}条发言")
    else:
        print(f"  [评论] ⚠️ 分析失败: {analysis.get('error', '未知')}")

    # 生成报告文本（给 save 节点用）
    report = format_comments_report(analysis)

    return {
        "success": analysis.get("success", False),
        "analysis": analysis,
        "report": report,
        "insights": analysis.get("insights", []),
    }
