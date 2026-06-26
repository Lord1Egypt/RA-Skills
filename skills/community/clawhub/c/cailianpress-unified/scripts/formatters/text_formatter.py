"""Plain text output formatter for CLS query results."""

from models.schemas import ClsQueryResult


def format_as_text(result: ClsQueryResult) -> str:
    """Format result as plain text for terminal/Telegram."""
    lines = [f"[{result.query_type.upper()}] 共 {result.count} 条", ""]

    if result.count == 0:
        if result.query_type == "red":
            lines.append("当前窗口内没有 level=A/B 的加红电报。")
        else:
            lines.append("当前查询条件下无结果。")
        return "\n".join(lines)

    for item in result.items:
        level_tag = "🔴" if item.is_red else "⚪"
        title = item.title or item.brief[:60] or "(无标题)"
        lines.append(f"{level_tag} {item.published_at} | {title[:60]}")
        lines.append(f"   阅读: {item.reading_num:,} | 等级: {item.level}")
        if result.query_type == "article" and item.content:
            lines.append(f"   正文: {item.content[:300]}")
        lines.append("")

    return "\n".join(lines)
