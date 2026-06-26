#!/usr/bin/env python3
"""
summarize_conversation.py — Condense a raw conversation into a clean summary.

This script is called by the agent AFTER it has produced a summarized version
of the conversation. It formats and structures the output before export.

Usage (called by agent, not directly by user):
    python3 summarize_conversation.py --input raw.md --output summary.md

The agent passes pre-summarized content via --content; this script handles
formatting/structuring only.
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime


SUMMARY_TEMPLATE = """# {title}

> 导出时间 / Exported at：{timestamp}
> 内容模式 / Mode：**精简摘要 · Condensed Summary**（已剔除冗余，提炼核心信息 · redundancy removed, key insights extracted）

---

{body}
"""

RAW_TEMPLATE = """# {title}

> 导出时间 / Exported at：{timestamp}
> 内容模式 / Mode：**完整对话 · Full Conversation**（原始记录，未经修改 · verbatim, unmodified）

---

{body}
"""


def format_for_export(content: str, mode: str = "raw", title: str = "对话导出") -> str:
    """Wrap content in export template."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    template = SUMMARY_TEMPLATE if mode == "summary" else RAW_TEMPLATE
    return template.format(title=title, timestamp=ts, body=content)


def main():
    parser = argparse.ArgumentParser(description="Format conversation for export")
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--content", help="Pre-processed content string")
    src.add_argument("--input", help="Input file path")
    parser.add_argument("--output", required=True, help="Output .md file path")
    parser.add_argument("--mode", choices=["raw", "summary"], default="raw",
                        help="raw = verbatim | summary = condensed")
    parser.add_argument("--title", default="对话导出", help="Document title")
    args = parser.parse_args()

    if args.input:
        content = Path(args.input).expanduser().read_text(encoding="utf-8")
    else:
        content = args.content

    formatted = format_for_export(content, args.mode, args.title)
    out = Path(args.output).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(formatted, encoding="utf-8")
    print(f"✅ 格式化完成：{out}")


if __name__ == "__main__":
    main()
