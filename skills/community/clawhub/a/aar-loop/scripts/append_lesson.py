#!/usr/bin/env python3
"""
AAR Lesson Logger - Creates individual lesson files and updates LESSONS.md index.

Usage:
  python3 append_lesson.py --task "Task" --expected "Exp" --actual "Act" --why "Why" --lesson "Lesson" --tags "t1,t2"
  python3 append_lesson.py --list
  python3 append_lesson.py --search "keyword"
"""
import argparse, os, re, sys
from datetime import datetime
from pathlib import Path

WORKSPACE_ROOT = Path(os.environ.get("OPENCLAW_WORKSPACE", "/root/.openclaw/workspace"))
LESSONS_DIR = WORKSPACE_ROOT / "lessons"
LESSONS_INDEX = WORKSPACE_ROOT / "LESSONS.md"
TEMPLATES_DIR = Path(__file__).parent.parent / "templates"

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text)
    return text.strip('-')[:50]

def create_lesson_file(task, expected, actual, why, lesson, tags, fix_target=None, fix_edit=None):
    LESSONS_DIR.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    slug = slugify(task)
    filename = f"{date_str}_{slug}.md"
    filepath = LESSONS_DIR / filename
    template_path = TEMPLATES_DIR / "lesson-template.md"
    if template_path.exists():
        content = template_path.read_text()
    else:
        content = "---\ndate: {date}\ntags: [{tags}]\ntask: \"{task}\"\nfix_applied: {fix_applied}\n---\n\n## What Was Supposed To Happen?\n{expected}\n\n## What Actually Happened?\n{actual}\n\n## Why Was There A Difference?\n{why}\n\n## What Can We Learn?\n{lesson}\n\n## Fix Plan (if applicable)\n{fix_plan}\n"
    tags_str = ", ".join([t.strip() for t in tags.split(",")]) if tags else ""
    fix_applied = "true" if fix_target and fix_edit else "false"
    fix_plan = ""
    if fix_target and fix_edit:
        fix_plan = f"**Target:** `{fix_target}`\n**Edit:** `{fix_edit}`"
    content = content.format(date=date_str, tags=tags_str, task=task, expected=expected, actual=actual, why=why, lesson=lesson, fix_applied=fix_applied, fix_plan=fix_plan)
    filepath.write_text(content)
    print(f"Created lesson file: {filepath}")
    return filepath, filename

def update_index(task, lesson, filename, tags):
    date_str = datetime.now().strftime("%Y-%m-%d")
    if not LESSONS_INDEX.exists():
        LESSONS_INDEX.write_text("# Lessons Index\n\n")
    content = LESSONS_INDEX.read_text()
    tags_list = [t.strip() for t in tags.split(",")] if tags else []
    tags_str = ", ".join(tags_list)
    new_entry = f"## {date_str} - {task}\n- Task: {task}\n- Lesson: {lesson}\n- Detail: [lessons/{filename}](lessons/{filename})\n- Tags: {tags_str}\n"
    entry_header = f"## {date_str} - {task}"
    if entry_header in content:
        print(f"Entry already exists in index, skipping")
        return
    lines = content.split('\n')
    insert_pos = 0
    for i, line in enumerate(lines):
        if line.startswith('# '):
            insert_pos = i + 1
            break
    lines.insert(insert_pos, "")
    lines.insert(insert_pos + 1, new_entry.strip())
    LESSONS_INDEX.write_text('\n'.join(lines))
    print(f"Updated index: {LESSONS_INDEX}")

def list_lessons():
    if not LESSONS_INDEX.exists():
        print("No lessons found.")
        return
    print(LESSONS_INDEX.read_text())

def search_lessons(keyword):
    if not LESSONS_INDEX.exists():
        print("No lessons found.")
        return
    content = LESSONS_INDEX.read_text()
    keyword_lower = keyword.lower()
    entries = content.split('\n## ')
    matches = [e for e in entries if keyword_lower in e.lower() and not e.startswith('# Lessons Index')]
    if matches:
        print(f"Found {len(matches)} matching lesson(s):\n")
        for match in matches:
            print(f"## {match}")
    else:
        print(f"No lessons found matching '{keyword}'")

def main():
    parser = argparse.ArgumentParser(description="AAR Lesson Logger")
    parser.add_argument("--task", help="Task name")
    parser.add_argument("--expected", help="Expected outcome")
    parser.add_argument("--actual", help="Actual outcome")
    parser.add_argument("--why", help="Root cause")
    parser.add_argument("--lesson", help="Lesson learned")
    parser.add_argument("--tags", help="Comma-separated tags")
    parser.add_argument("--fix-target", help="File to fix")
    parser.add_argument("--fix-edit", help="Exact edit to make")
    parser.add_argument("--list", action="store_true", help="List all lessons")
    parser.add_argument("--search", help="Search lessons by keyword")
    args = parser.parse_args()
    if args.list:
        list_lessons()
        return
    if args.search:
        search_lessons(args.search)
        return
    if not all([args.task, args.expected, args.actual, args.why, args.lesson]):
        parser.error("--task, --expected, --actual, --why, and --lesson are required")
    filepath, filename = create_lesson_file(task=args.task, expected=args.expected, actual=args.actual, why=args.why, lesson=args.lesson, tags=args.tags, fix_target=args.fix_target, fix_edit=args.fix_edit)
    update_index(task=args.task, lesson=args.lesson, filename=filename, tags=args.tags)
    print(f"\nLesson logged successfully! File: {filepath}, Index: {LESSONS_INDEX}")

if __name__ == "__main__":
    main()
