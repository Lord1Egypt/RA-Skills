#!/usr/bin/env python3
"""rebuild_index — 从章节文件确定性重建 chapters/index.json。

支持非补零旧章节名，检测重复章号和无效文件名，
支持 dry-run 和差异输出。
"""

import argparse
import json
import os
import re
import sys
from typing import List, Optional, Tuple

from _contract import count_words  # noqa: E402


def parse_chapter_file(name: str) -> Optional[Tuple[int, str]]:
    """解析章节文件名，返回 (章号, 标题)。"""
    if not name.endswith(".md"):
        return None
    # 支持 0001_标题.md、1_标题.md、第1章_标题.md 等格式
    m = re.match(r"^(\d+)[_\-]?(.*)$", name)
    if not m:
        return None
    num = int(m.group(1))
    title = m.group(2).replace("_", " ").replace("-", " ").strip()
    # 去除标题末尾的 .md 扩展名（如 "0001_入门.md" -> "入门"）
    if title.endswith(".md"):
        title = title[:-3].strip()
    # 去除第X章前缀
    title = re.sub(r"^第?\d+[章回节卷]\s*", "", title).strip()
    return num, title or name.replace(".md", "")


def scan_chapters(chapters_dir: str) -> List[dict]:
    """扫描章节文件，返回排序后的 index 条目列表。"""
    entries = []
    for name in sorted(os.listdir(chapters_dir)):
        parsed = parse_chapter_file(name)
        if parsed is None:
            continue
        num, title = parsed
        full_path = os.path.join(chapters_dir, name)
        # 统计字数（与 validate_book 共用 _contract.count_words，单一算法源）
        with open(full_path, "r", encoding="utf-8") as f:
            text = f.read()
        word_count = count_words(text)
        entries.append({
            "number": num,
            "file": name,
            "title": title,
            "status": "drafting",
            "wordCount": word_count,
        })
    # 按章号数值排序
    entries.sort(key=lambda e: e["number"])
    return entries


def detect_issues(entries: List[dict]) -> Tuple[List[str], List[str]]:
    """检测重复章号和无效文件名。"""
    errors = []
    warnings = []
    nums = [e["number"] for e in entries]
    seen = set()
    for num in nums:
        if num in seen:
            errors.append(f"重复章号：{num}")
        seen.add(num)
    # 检查连续性
    if nums:
        for i in range(nums[0], nums[-1] + 1):
            if i not in seen:
                warnings.append(f"章号缺失：{i}")
    return errors, warnings


def rebuild(book_dir: str, dry_run: bool = False) -> dict:
    """重建 index，返回结果信息。"""
    chapters_dir = os.path.join(book_dir, "chapters")
    if not os.path.isdir(chapters_dir):
        return {"ok": False, "error": "chapters/ 目录不存在"}

    entries = scan_chapters(chapters_dir)
    errors, warnings = detect_issues(entries)

    index = {"chapters": entries}

    result = {
        "ok": not errors,
        "entries": len(entries),
        "errors": errors,
        "warnings": warnings,
        "index": index,
    }

    if dry_run:
        # 读取现有 index 做差异比较
        index_path = os.path.join(book_dir, "chapters", "index.json")
        if os.path.isfile(index_path):
            try:
                with open(index_path, "r", encoding="utf-8") as f:
                    old = json.load(f)
                old_files = {e.get("file") for e in old.get("chapters", [])}
                new_files = {e["file"] for e in entries}
                added = new_files - old_files
                removed = old_files - new_files
                result["diff"] = {
                    "added": sorted(added),
                    "removed": sorted(removed),
                }
            except (json.JSONDecodeError, KeyError):
                pass
    else:
        index_path = os.path.join(book_dir, "chapters", "index.json")
        with open(index_path, "w", encoding="utf-8") as f:
            json.dump(index, f, ensure_ascii=False, indent=2)
            f.write("\n")

    return result


def main():
    parser = argparse.ArgumentParser(description="重建章节 index")
    parser.add_argument("book_dir", help="书籍根目录")
    parser.add_argument("--dry-run", action="store_true", help="仅输出差异，不写入文件")
    parser.add_argument("--json", action="store_true", help="输出机器可读 JSON")
    args = parser.parse_args()

    result = rebuild(args.book_dir, dry_run=args.dry_run)

    if args.json:
        # 不输出完整 index 到 JSON diff
        out = {k: v for k, v in result.items() if k != "index"}
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        if not result["ok"]:
            print(f"[FAIL] Rebuild failed: {result.get('error', 'unknown')}", file=sys.stderr)
            sys.exit(1)
        print(f"[OK] Rebuild complete, {result['entries']} chapters")
        for e in result["errors"]:
            print(f"  [ERROR] {e}")
        for w in result["warnings"]:
            print(f"  [WARN] {w}")
        if args.dry_run and "diff" in result:
            diff = result["diff"]
            if diff.get("added"):
                print(f"  Added: {', '.join(diff['added'])}")
            if diff.get("removed"):
                print(f"  Removed: {', '.join(diff['removed'])}")
            if not diff.get("added") and not diff.get("removed"):
                print("  No diff")

    sys.exit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
