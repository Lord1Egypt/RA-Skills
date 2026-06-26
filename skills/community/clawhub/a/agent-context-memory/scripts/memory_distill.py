#!/usr/bin/env python3
"""
memory_distill.py — 从 daily 记忆文件自动提炼经验教训到 MEMORY.md

扫描 memory/YYYY-MM-DD.md，提取"技术收获"、"问题+修复"等内容，
去重后追加到 MEMORY.md。

用法:
    python3 memory_distill.py                  # 处理最近 7 天
    python3 memory_distill.py --days 30        # 处理最近 30 天
    python3 memory_distill.py --all            # 处理所有未处理的文件
    python3 memory_distill.py --dry-run        # 只预览，不写入
"""

import argparse
import json
import re
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[3]
MEMORY_DIR = WORKSPACE / "memory"
MEMORY_FILE = WORKSPACE / "MEMORY.md"
STATE_FILE = MEMORY_DIR / "distill-state.json"

SECTION_KEYWORDS = ["技术收获", "收获", "教训", "经验总结", "踩坑", "技术要点"]

HEADING_RE = re.compile(r"^(#{2,4})\s+(.+)")


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {"processed": [], "last_run": None}


def save_state(state: dict):
    state["last_run"] = datetime.now().isoformat()
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def find_daily_files(days: int | None = None) -> list[Path]:
    files = sorted(MEMORY_DIR.glob("????-??-??.md"))
    if days is not None:
        cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        files = [f for f in files if f.stem >= cutoff]
    return files


def load_existing_memory() -> str:
    if MEMORY_FILE.exists():
        return MEMORY_FILE.read_text(encoding="utf-8")
    return ""


def parse_headings(lines: list[str]) -> list[dict]:
    """解析文件为按标题分段的结构。"""
    sections = []
    for i, line in enumerate(lines):
        m = HEADING_RE.match(line.strip())
        if m:
            sections.append({
                "level": len(m.group(1)),
                "title": m.group(2).strip(),
                "line_idx": i,
                "content_lines": [],
            })

    for idx, sec in enumerate(sections):
        start = sec["line_idx"] + 1
        end = sections[idx + 1]["line_idx"] if idx + 1 < len(sections) else len(lines)
        sec["content_lines"] = lines[start:end]
        sec["content"] = "\n".join(lines[start:end]).strip()

    return sections


def is_takeaway_section(title: str) -> bool:
    clean = title.strip().lstrip("0123456789.、 ")
    return any(kw in clean for kw in SECTION_KEYWORDS)


def has_problem_fix(content: str) -> bool:
    """检查内容是否同时包含问题描述和修复方案。"""
    has_problem = bool(re.search(r"\*\*(?:问题|原因|坑)\*\*\s*[:：]", content))
    has_fix = bool(re.search(r"\*\*(?:修复|解决|方案|操作)\*\*\s*[:：]", content))
    return has_problem and has_fix


def extract_problem_fix_summary(section: dict) -> str:
    """从 problem+fix 段落中提取精简摘要。"""
    lines = section["content_lines"]
    result = []
    for line in lines:
        stripped = line.strip()
        if re.match(r"[-*]\s*\*\*(?:问题|原因|修复|解决|教训)\*\*\s*[:：]", stripped):
            result.append(stripped)
    return "\n".join(result)


def extract_lessons_from_file(filepath: Path) -> list[dict]:
    content = filepath.read_text(encoding="utf-8")
    lines = content.split("\n")
    date = filepath.stem
    sections = parse_headings(lines)
    lessons = []
    seen_titles = set()

    for sec in sections:
        if is_takeaway_section(sec["title"]) and sec["content"].strip():
            key = sec["title"].strip()
            if key in seen_titles:
                continue
            seen_titles.add(key)

            clean_lines = []
            for line in sec["content_lines"]:
                stripped = line.strip()
                if stripped.startswith("- [ ]") or stripped.startswith("- [x]"):
                    continue
                if stripped:
                    clean_lines.append(stripped)
            clean_content = "\n".join(clean_lines)
            if clean_content:
                lessons.append({
                    "date": date,
                    "title": "技术收获",
                    "content": clean_content,
                    "source": "section",
                })

    for sec in sections:
        if sec["level"] == 3 and has_problem_fix(sec["content"]):
            summary = extract_problem_fix_summary(sec)
            if summary:
                title = sec["title"].lstrip("0123456789.、 ")
                lessons.append({
                    "date": date,
                    "title": title,
                    "content": summary,
                    "source": "problem_fix",
                })

    return lessons


def is_duplicate(lesson: dict, existing_memory: str) -> bool:
    content_lines = [l.strip().lstrip("-*").strip() for l in lesson["content"].split("\n") if l.strip()]
    match_count = sum(1 for line in content_lines if len(line) > 15 and line in existing_memory)
    if content_lines and match_count / len(content_lines) > 0.5:
        return True
    return False


def format_lessons(lessons: list[dict]) -> str:
    if not lessons:
        return ""

    by_date: dict[str, list[dict]] = {}
    for lesson in lessons:
        by_date.setdefault(lesson["date"], []).append(lesson)

    parts = []
    for date in sorted(by_date.keys()):
        items = by_date[date]
        for item in items:
            parts.append(f"### {item['title']}（{date}，自动提炼）")
            parts.append(item["content"])
            parts.append("")

    return "\n".join(parts)


def append_to_memory(formatted: str):
    content = load_existing_memory()

    separator_pos = content.rfind("\n---\n")
    if separator_pos != -1:
        before = content[:separator_pos].rstrip()
        after = content[separator_pos:]
        new_content = before + "\n\n" + formatted + after
    elif content.rstrip().endswith("---"):
        before = content.rstrip()[:-3].rstrip()
        new_content = before + "\n\n" + formatted + "\n---\n"
    else:
        new_content = content.rstrip() + "\n\n" + formatted

    MEMORY_FILE.write_text(new_content, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="从 daily 记忆文件提炼教训到 MEMORY.md")
    parser.add_argument("--days", type=int, default=7, help="处理最近 N 天（默认 7）")
    parser.add_argument("--all", action="store_true", help="处理所有未处理的文件")
    parser.add_argument("--dry-run", action="store_true", help="只预览，不写入")
    parser.add_argument("--force", action="store_true", help="忽略已处理状态，重新处理")
    args = parser.parse_args()

    state = load_state()
    processed_set = set(state.get("processed", []))

    daily_files = find_daily_files(days=None if args.all else args.days)
    if not args.force:
        daily_files = [f for f in daily_files if f.stem not in processed_set]

    if not daily_files:
        print("没有需要处理的新文件。")
        return

    print(f"找到 {len(daily_files)} 个待处理文件：")
    for f in daily_files:
        print(f"  - {f.stem}")

    existing_memory = load_existing_memory()
    all_lessons = []

    for filepath in daily_files:
        lessons = extract_lessons_from_file(filepath)
        new_lessons = [l for l in lessons if not is_duplicate(l, existing_memory)]
        if new_lessons:
            print(f"\n📄 {filepath.stem}：提取 {len(new_lessons)} 条")
            for l in new_lessons:
                print(f"    [{l['source']}] {l['title']}")
        else:
            print(f"\n📄 {filepath.stem}：无新内容")
        all_lessons.extend(new_lessons)

    if not all_lessons:
        print("\n没有新教训需要写入。")
        if not args.dry_run:
            for f in daily_files:
                processed_set.add(f.stem)
            state["processed"] = sorted(processed_set)
            save_state(state)
        return

    formatted = format_lessons(all_lessons)

    print(f"\n{'=' * 50}")
    print(f"共 {len(all_lessons)} 条新教训：")
    print(f"{'=' * 50}")
    print(formatted)

    if args.dry_run:
        print("[dry-run] 未写入 MEMORY.md")
    else:
        append_to_memory(formatted)
        for f in daily_files:
            processed_set.add(f.stem)
        state["processed"] = sorted(processed_set)
        save_state(state)
        print(f"\n✅ 已追加到 MEMORY.md，{len(daily_files)} 个文件标记为已处理")


if __name__ == "__main__":
    main()
