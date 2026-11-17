#!/usr/bin/env python3
"""Validate required structure for agent-readable Markdown outputs."""

from __future__ import annotations

import argparse
import difflib
from pathlib import Path
import re
import sys


REQUIRED_FRONTMATTER_FIELDS = [
    "summary",
    "search_terms",
    "use_when",
    "skip_when",
]
SECTION_HEADINGS = {
    "summary": (
        "Summary / 摘要",
        "Summary",
        # bilingual-compat: Legacy Chinese-only Summary heading.
        "摘要",
    ),
    "insight": ("Insight / 洞察", "Insight"),
    "details": ("Details / 详情", "Details"),
    "source_map": ("Source Map / 来源映射", "Source Map"),
}
SECTION_DISPLAY = {
    "summary": "Summary / 摘要",
    "insight": "Insight / 洞察",
    "details": "Details / 详情",
    "source_map": "Source Map / 来源映射",
}
REQUIRED_SECTIONS = ("summary", "insight", "details")
SOURCE_MAP_LINK_PATTERN = re.compile(r"^\s*-\s+\[\[Archived/[^\]\|#]+\]\]\s*$", re.MULTILINE)
CODE_REPO_SOURCE_MAP_PATTERN = re.compile(r"^\s*-\s+Source repository:\s+`[^`]+`\s*$", re.MULTILINE)
EMPTY_RELATED_INLINE_PATTERN = re.compile(r"^related:\s*\[\]\s*$", re.MULTILINE)
UNSIZED_OBSIDIAN_IMAGE_PATTERN = re.compile(r"!\[\[[^\]\|]+\]\]")
UNSIZED_MARKDOWN_IMAGE_PATTERN = re.compile(r"!\[[^\]\|]*\]\([^)]+\)")
MERGED_BOILERPLATE_HEADINGS = [
    # bilingual-compat: Legacy Chinese boilerplate heading meaning "Welcome to connect and collaborate."
    "欢迎交流与合作",
]
SUMMARY_SECTION_HEADINGS = {
    "Summary / 摘要",
    # bilingual-compat: Legacy Chinese-only heading meaning "Summary."
    "摘要",
    # bilingual-compat: Legacy Chinese-only heading meaning "Summary recap."
    "摘要总结",
    # bilingual-compat: Legacy Chinese-only heading meaning "Model summary."
    "模型总结",
    # bilingual-compat: Legacy Chinese-only heading meaning "Conclusion."
    "总结",
    # bilingual-compat: Legacy Chinese-only heading meaning "Key points."
    "要点",
    # bilingual-compat: Legacy Chinese-only heading meaning "Key takeaways."
    "关键要点",
    "Summary",
}
COVER_METADATA_PREFIXES = (
    # bilingual-compat: Legacy Chinese metadata label meaning "Title."
    "标题",
    # bilingual-compat: Legacy Chinese metadata label meaning "Link."
    "链接",
    # bilingual-compat: Legacy Chinese metadata label meaning "Publication date."
    "发布日期",
    # bilingual-compat: Legacy Chinese metadata label meaning "Total word count."
    "总字数",
    # bilingual-compat: Legacy Chinese metadata label meaning "Estimated reading time."
    "预估阅读时长",
    # bilingual-compat: Legacy Chinese metadata label meaning "Generated at."
    "生成时间",
    # bilingual-compat: Legacy Chinese metadata label meaning "Coverage duration."
    "覆盖时长",
    # bilingual-compat: Legacy Chinese metadata label meaning "Cache directory."
    "缓存目录",
)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str | None]:
    if not text.startswith("---\n"):
        return {}, "Missing YAML frontmatter block. / 缺少 YAML frontmatter 区块。"
    end = text.find("\n---", 4)
    if end == -1:
        return {}, "Unclosed YAML frontmatter block. / YAML frontmatter 区块未闭合。"
    raw = text[4:end]
    fields: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip() or line.startswith(" ") or line.startswith("-"):
            continue
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if match:
            fields[match.group(1)] = match.group(2)
    return fields, None


def frontmatter_text(text: str) -> str:
    if not text.startswith("---\n"):
        return ""
    end = text.find("\n---", 4)
    if end == -1:
        return text[4:]
    return text[4:end]


def is_code_repo_doc(fields: dict[str, str], text: str) -> bool:
    version = fields.get("version", "").strip().strip('"').strip("'")
    return version == "code-repo-v1" or "Asset type: `code_project`" in text


def has_empty_related(frontmatter: str) -> bool:
    if EMPTY_RELATED_INLINE_PATTERN.search(frontmatter):
        return True
    lines = frontmatter.splitlines()
    for index, line in enumerate(lines):
        if not re.match(r"^related:\s*$", line):
            continue
        next_line = lines[index + 1].strip() if index + 1 < len(lines) else ""
        if next_line == "[]" or not next_line.startswith("-"):
            return True
    return False


def heading_pattern(section: str) -> str:
    headings = SECTION_HEADINGS[section]
    return "(?:" + "|".join(re.escape(heading) for heading in headings) + ")"


def has_section(text: str, section: str) -> bool:
    pattern = rf"^##\s+{heading_pattern(section)}\s*$"
    return re.search(pattern, text, flags=re.MULTILINE) is not None


def has_duplicate_title_h1(text: str, title: str) -> bool:
    if not title:
        return False
    pattern = rf"^#\s+{re.escape(title.strip())}\s*$"
    return re.search(pattern, text, flags=re.MULTILINE) is not None


def strip_code_fences(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def h2_body(text: str, section: str) -> str:
    match = re.search(
        rf"^##\s+{heading_pattern(section)}\s*(.*?)(?=^##\s+|\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    return match.group(1) if match else ""


def details_body(text: str) -> str:
    terminal_headings = (
        *SECTION_HEADINGS["source_map"],
        "Examples / 示例",
        "Examples",
        "Edge Cases / 边界情况",
        "Edge Cases",
        "Related Docs / 相关文档",
        "Related Docs",
        "Verification / 验证",
        "Verification",
    )
    terminal_pattern = "(?:" + "|".join(re.escape(heading) for heading in terminal_headings) + ")"
    match = re.search(
        rf"^##\s+{heading_pattern('details')}\s*(.*?)(?=^##\s+{terminal_pattern}\s*$|\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    return match.group(1) if match else ""


def normalize_line(text: str) -> str:
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    # bilingual-compat: The punctuation class includes Chinese punctuation for legacy source comparison.
    text = re.sub(r"[#>*_`=\-•\s，。！？；：,.!?;:()\[\]（）【】\"'“”‘’]+", "", text)
    return text.strip().lower()


def content_items(text: str) -> list[str]:
    items: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(("- ", "* ")):
            item = normalize_line(stripped[2:])
        elif re.match(r"^\d+[.)]\s+", stripped):
            item = normalize_line(re.sub(r"^\d+[.)]\s+", "", stripped))
        else:
            item = ""
        if len(item) >= 12:
            items.append(item)
    if items:
        return items
    for paragraph in re.split(r"\n\s*\n", text):
        item = normalize_line(paragraph)
        if len(item) >= 24:
            items.append(item)
    return items


def bullet_lines(text: str) -> list[str]:
    lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(("- ", "* ")) or re.match(r"^\d+[.)]\s+", stripped):
            lines.append(stripped)
    return lines


def is_similar_item(candidate: str, existing: str) -> bool:
    if not candidate or not existing:
        return False
    if candidate in existing or existing in candidate:
        return True
    return difflib.SequenceMatcher(None, candidate, existing).ratio() >= 0.88


def summary_sections(details: str) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []
    matches = list(re.finditer(r"^(#{3,6})\s+(.+?)\s*$", details, flags=re.MULTILINE))
    for index, match in enumerate(matches):
        heading = match.group(2).strip().rstrip("：:")
        if heading not in SUMMARY_SECTION_HEADINGS:
            continue
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(details)
        sections.append((heading, details[start:end]))
    return sections


def has_empty_summary_section(text: str) -> bool:
    return any(not normalize_line(section) for _, section in summary_sections(details_body(text)))


def has_cover_metadata_conclusion(text: str) -> bool:
    conclusion_lines = bullet_lines(h2_body(text, "summary"))
    if not conclusion_lines:
        return False
    metadata_count = 0
    for line in conclusion_lines:
        value = line.lstrip("-* 0123456789.)").strip()
        if any(value.startswith(f"{prefix}:") or value.startswith(f"{prefix}：") for prefix in COVER_METADATA_PREFIXES):
            metadata_count += 1
    has_real_summary = any(content_items(section) for _, section in summary_sections(details_body(text)))
    return has_real_summary and metadata_count >= 2


def has_duplicate_conclusion_summary(text: str) -> bool:
    conclusion_items = content_items(h2_body(text, "summary"))
    if not conclusion_items:
        return False
    details = details_body(text)
    for _, section in summary_sections(details):
        section_items = content_items(section)
        if not section_items:
            continue
        duplicate_count = sum(
            1 for item in section_items if any(is_similar_item(item, conclusion) for conclusion in conclusion_items)
        )
        if duplicate_count >= 2 or duplicate_count == len(section_items):
            return True
    return False


def has_details_peer_heading(text: str) -> bool:
    details_without_code = strip_code_fences(details_body(text))
    return re.search(r"^##\s+.+", details_without_code, flags=re.MULTILINE) is not None


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8", errors="replace")
    fields, frontmatter_error = parse_frontmatter(text)
    if frontmatter_error:
        errors.append(frontmatter_error)
    else:
        for field in REQUIRED_FRONTMATTER_FIELDS:
            if field not in fields:
                errors.append(f"Missing frontmatter field: {field}. / 缺少 frontmatter 字段：{field}。")
        if has_duplicate_title_h1(text, fields.get("title", "")):
            errors.append(
                "Do not repeat the frontmatter title as a body H1; start with ## Summary / 摘要. / 不要在正文 H1 重复 frontmatter 标题；正文应从 ## Summary / 摘要 开始。"
            )
        if has_empty_related(frontmatter_text(text)):
            errors.append(
                "Omit empty related frontmatter instead of writing related: [] or an empty related field. / 省略空的 related frontmatter，不要写 related: [] 或空 related 字段。"
            )

    for section in REQUIRED_SECTIONS:
        if not has_section(text, section):
            errors.append(
                f"Missing section: ## {SECTION_DISPLAY[section]} / 缺少章节：## {SECTION_DISPLAY[section]}"
            )

    if has_section(text, "source_map"):
        source_map_match = re.search(
            rf"^##\s+{heading_pattern('source_map')}\s*(.*?)(?:\n##\s+|\Z)",
            text,
            flags=re.MULTILINE | re.DOTALL,
        )
        if source_map_match:
            body = source_map_match.group(1)
            source_map_ok = SOURCE_MAP_LINK_PATTERN.search(body)
            if is_code_repo_doc(fields, text):
                source_map_ok = source_map_ok or CODE_REPO_SOURCE_MAP_PATTERN.search(body)
            if "|" in body or not source_map_ok:
                errors.append(
                    "Source Map should be a bullet list of article-level archived Obsidian wikilinks, "
                    "e.g. '- [[Archived/path/source.md]]'. / 来源映射应使用文章级归档 Obsidian wikilink 的项目列表。"
                )

    for heading in MERGED_BOILERPLATE_HEADINGS:
        count = len(re.findall(rf"^###\s+{re.escape(heading)}\s*$", text, flags=re.MULTILINE))
        if count > 1:
            errors.append(
                f"Duplicate boilerplate section in merged output: ### {heading} appears {count} times; keep at most one. / 合并输出中样板章节重复：### {heading} 出现 {count} 次；最多保留一次。"
            )

    if has_duplicate_conclusion_summary(text):
        errors.append(
            "Do not duplicate conclusion content in Details summary sections; remove repeated legacy summary content after it is promoted to ## Summary / 摘要. / 不要在详情的摘要小节重复结论；内容提升到 ## Summary / 摘要 后应删除重复项。"
        )

    if has_details_peer_heading(text):
        errors.append(
            "Source headings inside ## Details / 详情 should be H3 or deeper. "
            "/ ## Details / 详情 内的来源标题应使用 H3 或更深层级。"
        )

    if has_empty_summary_section(text):
        errors.append("Omit empty summary sections inside Details. / 省略 Details 内的空摘要小节。")

    if has_cover_metadata_conclusion(text):
        errors.append(
            "Do not use cover metadata as ## Summary / 摘要 when a source summary exists. / 原文存在摘要时，不要用封面 metadata 充当 ## Summary / 摘要。"
        )

    body_without_code = strip_code_fences(text)
    if UNSIZED_OBSIDIAN_IMAGE_PATTERN.search(body_without_code) or UNSIZED_MARKDOWN_IMAGE_PATTERN.search(body_without_code):
        errors.append(
            "Images should include an Obsidian width hint, e.g. ![[image.png|560]] or ![alt|560](url). / 图片应包含 Obsidian 宽度提示。"
        )

    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate agent-readable Markdown structure. / 验证 Agent 可读 Markdown 结构。"
    )
    parser.add_argument("files", nargs="+", help="Markdown files to validate. / 要验证的 Markdown 文件。")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    had_errors = False
    for item in args.files:
        path = Path(item)
        errors = validate(path)
        if errors:
            had_errors = True
            print(f"{path}: FAIL / 失败")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"{path}: OK / 通过")
    return 1 if had_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
