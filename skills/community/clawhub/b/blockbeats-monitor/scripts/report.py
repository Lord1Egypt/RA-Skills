# 本文件负责把统计结果渲染为 Telegram 可发送的 Markdown 日报。

from datetime import timedelta

def format_report_date(window_end):
    report_day = (window_end - timedelta(days=1)).date()
    return "%s-%s-%s" % (report_day.year, report_day.month, report_day.day)


def format_delta(delta):
    if delta > 0:
        return "+%s次" % delta
    if delta < 0:
        return "%s次" % delta
    return "持平"


def _format_item_line(item):
    title = item.get("title") or "无标题"
    url = item.get("url") or "无链接"
    published_at = item.get("published_at") or "未知时间"
    return "- %s / %s / %s" % (title, url, published_at)


def render_report(window_start, window_end, summaries, important_items):
    """生成固定格式日报，正文不包含未确认的互动类指标。"""
    total_mentions = sum(summary["mention_count"] for summary in summaries)
    lines = [
        "📊 %s日 BlockBeats平台舆情日报" % format_report_date(window_end),
        "",
        "一：总体数据",
        "- 总提及：%s次" % total_mentions,
        "",
        "二：关键词热度排名",
    ]

    for index, summary in enumerate(summaries, start=1):
        lines.append(
            "%s. %s：提及总次数：%s次，与上个周期相比：%s"
            % (index, summary["group_name"], summary["mention_count"], format_delta(summary["delta"]))
        )
        lines.append("主要相关内容：")
        if summary["items"]:
            lines.extend(_format_item_line(item) for item in summary["items"])
        else:
            lines.append("- 暂无相关内容")
        lines.append("")

    lines.append("三：重要舆情")
    lines.append("昨日重点相关内容：")
    if important_items:
        for index, item in enumerate(important_items, start=1):
            group_names = "、".join(item.get("group_names") or [item.get("group_name", "未分类")])
            source_type = item.get("source_type") or "unknown"
            title = item.get("title") or "无标题"
            url = item.get("url") or "无链接"
            published_at = item.get("published_at") or "未知时间"
            lines.append("%s. %s / %s / %s / %s / %s" % (index, title, group_names, source_type, url, published_at))
    else:
        lines.append("1. 暂无重点相关内容")

    return "\n".join(lines).strip() + "\n"
