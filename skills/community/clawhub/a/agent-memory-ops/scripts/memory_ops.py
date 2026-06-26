#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

SECRET_PATTERNS = [
    re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"\bBearer\s+[A-Za-z0-9._-]{16,}\b", re.I),
    re.compile(r"\b(api[_-]?key|password|passwd|secret|token)\b", re.I),
]

TODO_PATTERNS = [
    re.compile(p, re.I)
    for p in [
        r"\btodo\b",
        r"\bnext step\b",
        r"\bfollow[- ]?up\b",
        r"\bblocked\b",
        r"\bpending\b",
        r"\bin progress\b",
        r"待办",
        r"继续",
        r"跟进",
        r"阻塞",
        r"等待",
        r"发布",
        r"实现",
        r"修复",
    ]
]

DURABLE_PATTERNS = [
    re.compile(p, re.I)
    for p in [
        r"\bprefer\b",
        r"\bpreference\b",
        r"\balways\b",
        r"\bnever\b",
        r"\brule\b",
        r"\bconstraint\b",
        r"\bworkflow\b",
        r"\bdecision\b",
        r"\btimezone\b",
        r"偏好",
        r"不喜欢",
        r"约定",
        r"规则",
        r"长期",
        r"以后",
        r"习惯",
        r"风格",
    ]
]

LESSON_PATTERNS = [
    re.compile(p, re.I)
    for p in [
        r"\blesson\b",
        r"\blearned\b",
        r"\bmistake\b",
        r"\binsight\b",
        r"\bdiscovered\b",
        r"经验",
        r"教训",
        r"发现",
        r"以后记得",
    ]
]

BULLET_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+(.*\S)\s*$")
DATE_FILE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})\.md$")


@dataclass
class MemoryItem:
    file: str
    line_no: int
    text: str
    normalized: str


def is_secret(text: str) -> bool:
    return any(p.search(text) for p in SECRET_PATTERNS)


def normalize(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"`[^`]+`", "", text)
    text = re.sub(r"\b[0-9a-f]{7,40}\b", "", text)
    text = re.sub(r"\b\d{4}-\d{2}-\d{2}\b", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip(" -—–:：")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def collect_files(root: Path) -> Tuple[Path, List[Path]]:
    memory_md = root / "MEMORY.md"
    daily_dir = root / "memory"
    daily_files = sorted(daily_dir.glob("*.md")) if daily_dir.exists() else []
    return memory_md, daily_files


def extract_items(path: Path) -> List[MemoryItem]:
    items: List[MemoryItem] = []
    if not path.exists():
        return items
    for idx, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        m = BULLET_RE.match(line)
        if not m:
            continue
        text = m.group(1).strip()
        if len(text) < 10:
            continue
        items.append(MemoryItem(str(path), idx, text, normalize(text)))
    return items


def extract_todos(items: Iterable[MemoryItem]) -> List[MemoryItem]:
    return [item for item in items if any(p.search(item.text) for p in TODO_PATTERNS)]


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def cluster_duplicates(items: List[MemoryItem], threshold: float) -> List[List[MemoryItem]]:
    parent = list(range(len(items)))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for i in range(len(items)):
        if not items[i].normalized:
            continue
        for j in range(i + 1, len(items)):
            if not items[j].normalized:
                continue
            if items[i].file == items[j].file and items[i].line_no == items[j].line_no:
                continue
            score = similarity(items[i].normalized, items[j].normalized)
            if score >= threshold:
                union(i, j)

    groups: Dict[int, List[MemoryItem]] = {}
    for i, item in enumerate(items):
        groups.setdefault(find(i), []).append(item)

    clusters = [g for g in groups.values() if len(g) > 1]
    clusters.sort(key=lambda g: (-len(g), g[0].file, g[0].line_no))
    return clusters


def recent_daily_files(daily_files: List[Path], days: int | None, files: int | None) -> List[Path]:
    if files:
        return daily_files[-files:]
    if days:
        cutoff = dt.date.today() - dt.timedelta(days=max(days - 1, 0))
        keep: List[Path] = []
        for path in daily_files:
            m = DATE_FILE_RE.match(path.name)
            if not m:
                continue
            try:
                d = dt.date.fromisoformat(m.group(1))
            except ValueError:
                continue
            if d >= cutoff:
                keep.append(path)
        return keep
    return daily_files[-7:]


def classify_digest(items: Iterable[MemoryItem]) -> Dict[str, List[MemoryItem]]:
    out = {"durable": [], "active": [], "lessons": []}
    seen = set()
    for item in items:
        if is_secret(item.text):
            continue
        key = (item.normalized, item.file)
        if key in seen or len(item.text) < 12:
            continue
        seen.add(key)
        if any(p.search(item.text) for p in DURABLE_PATTERNS):
            out["durable"].append(item)
        elif any(p.search(item.text) for p in TODO_PATTERNS):
            out["active"].append(item)
        elif any(p.search(item.text) for p in LESSON_PATTERNS):
            out["lessons"].append(item)
    return out


def markdown_report(root: Path, memory_md: Path, daily_files: List[Path], items: List[MemoryItem], dupes: List[List[MemoryItem]], todos: List[MemoryItem]) -> str:
    today = dt.date.today()
    yesterday = today - dt.timedelta(days=1)
    expected = [f"{today.isoformat()}.md", f"{yesterday.isoformat()}.md"]
    missing = [name for name in expected if not (root / "memory" / name).exists()]

    lines = [
        "# Agent Memory Ops Report",
        "",
        f"- Root: `{root}`",
        f"- MEMORY.md exists: {'yes' if memory_md.exists() else 'no'}",
        f"- Daily memory files: {len(daily_files)}",
        f"- Bullet items scanned: {len(items)}",
        f"- Duplicate clusters: {len(dupes)}",
        f"- Follow-up / TODO candidates: {len(todos)}",
    ]
    if missing:
        lines.append(f"- Missing recent daily files: {', '.join(missing)}")

    if dupes:
        lines += ["", "## Duplicate / near-duplicate clusters"]
        for idx, cluster in enumerate(dupes[:10], start=1):
            lines.append(f"### Cluster {idx}")
            for item in cluster:
                lines.append(f"- `{Path(item.file).name}#{item.line_no}` — {item.text}")
    if todos:
        lines += ["", "## Follow-up candidates"]
        for item in todos[:15]:
            lines.append(f"- `{Path(item.file).name}#{item.line_no}` — {item.text}")

    return "\n".join(lines) + "\n"


def markdown_digest(groups: Dict[str, List[MemoryItem]], files: List[Path]) -> str:
    lines = [
        "# Agent Memory Digest Draft",
        "",
        "Scanned files:",
    ]
    lines += [f"- `{p.name}`" for p in files]

    sections = [
        ("Durable memory candidates", "durable"),
        ("Active thread candidates", "active"),
        ("Lessons / workflow candidates", "lessons"),
    ]
    for title, key in sections:
        lines += ["", f"## {title}"]
        if not groups[key]:
            lines.append("- None")
            continue
        for item in groups[key][:20]:
            lines.append(f"- {item.text}  ")
            lines.append(f"  Source: `{Path(item.file).name}#{item.line_no}`")
    return "\n".join(lines) + "\n"


def json_dump(obj) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def cmd_report(args) -> None:
    root = Path(args.root).resolve()
    memory_md, daily_files = collect_files(root)
    files = [memory_md] + daily_files
    items = [item for path in files for item in extract_items(path)]
    dupes = cluster_duplicates(items, args.threshold)
    todos = extract_todos(items)
    if args.format == "json":
        json_dump(
            {
                "root": str(root),
                "memory_exists": memory_md.exists(),
                "daily_files": len(daily_files),
                "items": len(items),
                "duplicate_clusters": [
                    [{"file": x.file, "line": x.line_no, "text": x.text} for x in c] for c in dupes
                ],
                "todos": [{"file": x.file, "line": x.line_no, "text": x.text} for x in todos],
            }
        )
        return
    print(markdown_report(root, memory_md, daily_files, items, dupes, todos))


def cmd_dedupe(args) -> None:
    root = Path(args.root).resolve()
    memory_md, daily_files = collect_files(root)
    items = [item for path in [memory_md] + daily_files for item in extract_items(path)]
    dupes = cluster_duplicates(items, args.threshold)
    if args.format == "json":
        json_dump([[{"file": x.file, "line": x.line_no, "text": x.text} for x in c] for c in dupes])
        return
    if not dupes:
        print("No duplicate clusters found.")
        return
    for idx, cluster in enumerate(dupes, start=1):
        print(f"## Cluster {idx}")
        for item in cluster:
            print(f"- {Path(item.file).name}#{item.line_no}: {item.text}")
        print()


def cmd_digest(args) -> None:
    root = Path(args.root).resolve()
    _, daily_files = collect_files(root)
    selected = recent_daily_files(daily_files, args.days, args.files)
    items = [item for path in selected for item in extract_items(path)]
    groups = classify_digest(items)
    if args.format == "json":
        json_dump(
            {
                key: [{"file": x.file, "line": x.line_no, "text": x.text} for x in values]
                for key, values in groups.items()
            }
        )
        return
    print(markdown_digest(groups, selected))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Audit and maintain OpenClaw-style memory files.")
    sub = p.add_subparsers(dest="cmd", required=True)

    report = sub.add_parser("report", help="Summarize memory health and follow-ups.")
    report.add_argument("--root", default=".")
    report.add_argument("--threshold", type=float, default=0.82)
    report.add_argument("--format", choices=["markdown", "json"], default="markdown")
    report.set_defaults(func=cmd_report)

    dedupe = sub.add_parser("dedupe", help="List duplicate / near-duplicate bullets.")
    dedupe.add_argument("--root", default=".")
    dedupe.add_argument("--threshold", type=float, default=0.82)
    dedupe.add_argument("--format", choices=["markdown", "json"], default="markdown")
    dedupe.set_defaults(func=cmd_dedupe)

    digest = sub.add_parser("digest", help="Draft durable memory candidates from recent daily files.")
    digest.add_argument("--root", default=".")
    digest.add_argument("--days", type=int)
    digest.add_argument("--files", type=int)
    digest.add_argument("--format", choices=["markdown", "json"], default="markdown")
    digest.set_defaults(func=cmd_digest)

    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
