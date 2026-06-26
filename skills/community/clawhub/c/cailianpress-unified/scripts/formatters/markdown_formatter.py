"""Markdown output formatter for CLS query results."""

from models.schemas import ClsQueryResult


def format_as_markdown(result: ClsQueryResult) -> str:
    """Format result as Markdown for documents/reports."""
    lines = [f"## 📡 财联社 {result.query_type.upper()} 查询结果", ""]
    lines.append(f"- **数量**: {result.count} 条")
    lines.append(f"- **来源**: {result.source_used}")
    lines.append(f"- **生成时间**: {result.generated_at}")
    lines.append("")

    if result.count == 0:
        if result.query_type == "red":
            lines.append("- 当前窗口内没有 `level=A/B` 的加红电报")
        else:
            lines.append("- 当前查询条件下无结果")
        return "\n".join(lines)

    for i, item in enumerate(result.items, 1):
        level_tag = "🔴" if item.is_red else "⚪"
        title = item.title or item.brief[:80] or "(无标题)"
        lines.append(f"### {i}. {level_tag} {title}")
        lines.append("")
        lines.append(f"- **时间**: {item.published_at}")
        lines.append(f"- **等级**: {item.level}")
        lines.append(f"- **阅读量**: {item.reading_num:,}")
        if item.brief:
            lines.append(f"- **摘要**: {item.brief[:160]}...")
        if result.query_type == "article" and item.content:
            lines.append(f"- **正文**: {item.content[:500]}...")
        if item.shareurl:
            lines.append(f"- **链接**: {item.shareurl}")
        lines.append("")

    return "\n".join(lines)
