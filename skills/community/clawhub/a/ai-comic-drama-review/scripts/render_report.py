#!/usr/bin/env python3
"""Validate an AI comic-drama review and render a standalone HTML report."""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = (
    "一、审核结论",
    "二、评分总览",
    "三、优先修改清单",
    "四、分项审核",
    "五、分集分场问题清单",
    "六、重点问题修改示范",
    "七、复审清单",
    "八、审核范围与限制",
)

CSS = r"""
:root {
  --ink: #172033;
  --muted: #667085;
  --paper: #ffffff;
  --canvas: #f3f5f9;
  --line: #e4e8ef;
  --accent: #e4573d;
  --accent-dark: #b93825;
  --navy: #18253d;
  --soft: #fff5f1;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  color: var(--ink);
  background: var(--canvas);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC",
    "Hiragino Sans GB", "Microsoft YaHei", "Noto Sans CJK SC", sans-serif;
  font-size: 16px;
  line-height: 1.75;
  -webkit-font-smoothing: antialiased;
}
.page { max-width: 1120px; margin: 0 auto; padding: 40px 24px 64px; }
.toolbar {
  display: flex; justify-content: space-between; align-items: center;
  gap: 16px; margin-bottom: 18px; color: var(--muted); font-size: 13px;
}
.brand { font-weight: 700; letter-spacing: .12em; color: var(--navy); }
.print-button {
  border: 1px solid var(--line); border-radius: 999px; padding: 7px 15px;
  color: var(--navy); background: var(--paper); cursor: pointer; font: inherit;
}
.print-button:hover { border-color: var(--accent); color: var(--accent-dark); }
.report {
  background: var(--paper); border: 1px solid var(--line); border-radius: 20px;
  padding: 52px 60px; box-shadow: 0 16px 48px rgba(23, 32, 51, .06);
  overflow: hidden;
}
h1, h2, h3, h4, h5 { color: var(--navy); line-height: 1.35; scroll-margin-top: 24px; }
h1 { font-size: clamp(28px, 4vw, 42px); margin: 0 0 30px; letter-spacing: -.02em; }
h2 {
  font-size: 25px; margin: 52px 0 20px; padding-top: 16px;
  border-top: 3px solid var(--navy);
}
h3 { font-size: 20px; margin: 36px 0 14px; }
h4 {
  font-size: 17px; margin: 28px 0 12px; padding: 12px 16px;
  background: var(--soft); border-left: 4px solid var(--accent); border-radius: 4px;
}
h5 {
  font-size: 16px; margin: 26px 0 12px; padding: 11px 14px;
  color: var(--accent-dark); background: #fafbfc; border: 1px solid var(--line);
  border-left: 4px solid var(--accent); border-radius: 4px;
}
p { margin: 12px 0; }
strong { color: #101828; }
a { color: var(--accent-dark); text-decoration-thickness: 1px; text-underline-offset: 3px; }
blockquote {
  margin: 24px 0; padding: 14px 20px; color: #5b4350;
  background: #fff8f5; border-left: 4px solid var(--accent); border-radius: 0 8px 8px 0;
}
blockquote p { margin: 0; }
ul, ol { padding-left: 1.5em; }
li { margin: 6px 0; }
li::marker { color: var(--accent); font-weight: 700; }
table {
  display: block; width: 100%; overflow-x: auto; margin: 20px 0 28px;
  border-spacing: 0; border-collapse: collapse; font-size: 14px; line-height: 1.55;
}
thead { background: var(--navy); color: white; }
th, td { min-width: 84px; padding: 11px 13px; border: 1px solid var(--line); text-align: left; vertical-align: top; }
th { font-weight: 650; border-color: var(--navy); }
tbody tr:nth-child(even) { background: #f8f9fc; }
tbody tr:hover { background: #fff7f3; }
code { padding: 2px 5px; background: #f1f3f7; border-radius: 4px; font-size: .9em; }
hr { border: 0; border-top: 1px solid var(--line); margin: 36px 0; }
.toc {
  margin: 0 0 28px; padding: 18px 24px; background: var(--navy);
  color: white; border-radius: 14px;
}
.toc summary { cursor: pointer; font-weight: 700; }
.toc ul { margin: 12px 0 0; columns: 2; column-gap: 36px; }
.toc li { break-inside: avoid; margin: 5px 0; }
.toc a { color: #f7f9fc; text-decoration: none; }
.toc a:hover { color: #ffc4b5; }
.toc .toc-h3 { font-size: 14px; margin-left: 12px; color: #cdd5e3; }
.footer { margin-top: 18px; text-align: center; color: var(--muted); font-size: 12px; }
@media (max-width: 720px) {
  .page { padding: 16px 10px 36px; }
  .report { padding: 28px 20px; border-radius: 14px; }
  .toolbar { padding: 0 6px; }
  .brand { letter-spacing: .06em; }
  h2 { margin-top: 40px; font-size: 22px; }
  .toc ul { columns: 1; }
  th, td { padding: 9px 10px; }
}
@media print {
  @page { size: A4; margin: 16mm 14mm; }
  body { background: white; font-size: 10.5pt; }
  .page { max-width: none; padding: 0; }
  .report { padding: 0; border: 0; border-radius: 0; box-shadow: none; overflow: visible; }
  .toolbar, .toc, .footer { display: none !important; }
  h1 { font-size: 24pt; }
  h2 { font-size: 17pt; break-after: avoid; }
  h3, h4 { break-after: avoid; }
  table { display: table; overflow: visible; font-size: 8.5pt; break-inside: auto; }
  tr, blockquote { break-inside: avoid; }
  a { color: inherit; text-decoration: none; }
}
"""


class ReportError(ValueError):
    """Raised when the Markdown report does not satisfy the delivery contract."""


def validate_markdown(markdown_text: str) -> None:
    if not markdown_text.strip():
        raise ReportError("Markdown 报告为空。")
    if not re.search(r"^#\s+\S", markdown_text, flags=re.MULTILINE):
        raise ReportError("Markdown 报告缺少一级标题。")
    placeholders = re.findall(r"\{\{[^{}]+\}\}", markdown_text)
    if placeholders:
        sample = "、".join(placeholders[:3])
        raise ReportError(f"报告仍有未替换的占位符：{sample}")
    missing = [
        section
        for section in REQUIRED_SECTIONS
        if not re.search(rf"^##\s+{re.escape(section)}\s*$", markdown_text, flags=re.MULTILINE)
    ]
    if missing:
        raise ReportError("报告缺少必需章节：" + "、".join(missing))


def render_markdown(markdown_text: str):
    try:
        from markdown_it import MarkdownIt
    except ImportError as exc:
        raise ReportError(
            "缺少 markdown-it-py。请使用已配置该依赖的 Python 环境运行转换脚本。"
        ) from exc

    parser = MarkdownIt(
        "commonmark", {"html": False, "linkify": False, "typographer": False}
    ).enable("table")
    tokens = parser.parse(markdown_text)
    headings = []
    section_number = 0
    for index, token in enumerate(tokens):
        if token.type != "heading_open":
            continue
        section_number += 1
        heading_id = f"section-{section_number}"
        token.attrSet("id", heading_id)
        inline = tokens[index + 1]
        headings.append((token.tag, heading_id, inline.content))
    return parser.renderer.render(tokens, parser.options, {}), headings


def build_toc(headings) -> str:
    items = []
    for tag, heading_id, label in headings:
        if tag not in {"h2", "h3"}:
            continue
        css_class = "toc-h3" if tag == "h3" else "toc-h2"
        items.append(
            f'<li class="{css_class}"><a href="#{heading_id}">{html.escape(label)}</a></li>'
        )
    if not items:
        return ""
    return (
        '<details class="toc" open><summary>报告目录</summary><ul>'
        + "".join(items)
        + "</ul></details>"
    )


def build_html(markdown_text: str, source_name: str, title_override: str | None) -> str:
    content, headings = render_markdown(markdown_text)
    first_title = next((label for tag, _, label in headings if tag == "h1"), "AI 漫剧剧本审核报告")
    title = title_override or first_title
    toc = build_toc(headings)
    document = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <title>{html.escape(title)}</title>
  <style>{CSS}</style>
</head>
<body>
  <main class="page">
    <div class="toolbar">
      <span class="brand">AI COMIC DRAMA · SCRIPT REVIEW</span>
      <button class="print-button" type="button" onclick="window.print()">打印 / 导出 PDF</button>
    </div>
    {toc}
    <article class="report">{content}</article>
    <div class="footer">离线 HTML 报告 · 内容来源：{html.escape(source_name)}</div>
  </main>
</body>
</html>
"""
    if "<article" not in document or "</html>" not in document:
        raise ReportError("HTML 生成失败，输出结构不完整。")
    return document


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="校验 AI 漫剧剧本 Markdown 审核报告，并生成可离线查看的 HTML。"
    )
    parser.add_argument("markdown", type=Path, help="最终 Markdown 报告路径")
    parser.add_argument("--output", "-o", type=Path, help="HTML 输出路径；默认与 Markdown 同名")
    parser.add_argument("--title", help="覆盖 HTML 文档标题，不改变报告正文")
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    source = args.markdown.expanduser().resolve()
    output = (args.output or source.with_suffix(".html")).expanduser().resolve()
    try:
        if not source.is_file():
            raise ReportError(f"找不到 Markdown 文件：{source}")
        if source.suffix.lower() not in {".md", ".markdown"}:
            raise ReportError("输入文件必须使用 .md 或 .markdown 扩展名。")
        if source == output:
            raise ReportError("HTML 输出路径不能与 Markdown 输入路径相同。")
        markdown_text = source.read_text(encoding="utf-8-sig")
        validate_markdown(markdown_text)
        document = build_html(markdown_text, source.name, args.title)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(document, encoding="utf-8")
    except (OSError, ReportError) as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 1
    print(f"HTML 报告已生成：{output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
