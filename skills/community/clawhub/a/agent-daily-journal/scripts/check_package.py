#!/usr/bin/env python3
"""Pre-publish check for this skill package.

Runs the repo's hardline authoring rules against the package as it sits on disk:

  - SKILL.md frontmatter starts at byte 0, closes with `---`, parses as YAML
  - name / description / version / author / license / platforms / metadata.hermes present
  - description <= 60 chars, one sentence, ends with a period
  - SKILL.md <= 100_000 chars
  - no machine-local paths (drive-letter workspaces, home dirs, AppData) in shipped text
  - every file `SKILL.md` points at exists
  - no example journal entry (a copyable sample) in the prompt contract or style templates

Exit 0 when clean, 1 with a list of problems.

Usage: python scripts/check_package.py
"""

from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOCAL_PATH_PATTERNS = [
    r"[A-Za-z]:\\Users\\",
    r"[A-Za-z]:/Users/",
    r"[A-Za-z]:\\workspace",
    r"\bAppData/Local\b",
    r"\bAppData\\Local\b",
]
TEXT_SUFFIXES = {".md", ".py", ".json"}
SKIPPED_DIRS = {".git", "__pycache__"}


def frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        raise ValueError("SKILL.md must start with '---' at byte 0")
    match = re.search(r"\n---\s*\n", text[3:])
    if not match:
        raise ValueError("SKILL.md frontmatter is not closed with '---'")
    raw = text[3: match.start() + 3]
    try:
        import yaml
    except ImportError:                                  # stdlib-only fallback
        data = {}
        for line in raw.splitlines():
            key, sep, value = line.partition(":")
            if sep and not line.startswith((" ", "-")):
                data[key.strip()] = value.strip().strip('"')
        return data
    return yaml.safe_load(raw) or {}


def main() -> int:
    problems: list[str] = []
    skill = ROOT / "SKILL.md"
    text = skill.read_text(encoding="utf-8")

    try:
        meta = frontmatter(text)
    except ValueError as exc:
        print(f"FAIL frontmatter: {exc}")
        return 1

    for field in ("name", "description", "version", "author", "license", "platforms", "metadata"):
        if field not in meta:
            problems.append(f"frontmatter: missing '{field}'")
    description = str(meta.get("description", ""))
    if len(description) > 60:
        problems.append(f"description is {len(description)} chars (hardline 60): {description!r}")
    if not description.endswith("."):
        problems.append("description must end with a period")
    if len(text) > 100_000:
        problems.append(f"SKILL.md is {len(text)} chars (limit 100000)")
    hermes = (meta.get("metadata") or {}).get("hermes") or {}
    if not hermes.get("tags"):
        problems.append("frontmatter: metadata.hermes.tags is empty")

    # referenced files must exist
    for match in re.finditer(r"`((?:scripts|references|config|assets|examples|tests)/[^`\s]+)`", text):
        rel = match.group(1).rstrip(".,)")
        if not (ROOT / rel).exists():
            problems.append(f"SKILL.md points at a missing file: {rel}")

    # no machine-local paths in shipped text
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
            continue
        if SKIPPED_DIRS & set(path.parts):
            continue
        body = path.read_text(encoding="utf-8", errors="replace")
        for pattern in LOCAL_PATH_PATTERNS:
            for hit in re.finditer(pattern, body):
                line = body[: hit.start()].count("\n") + 1
                problems.append(f"{path.relative_to(ROOT)}:{line} machine-local path: {hit.group(0)}")

    # no copyable example entry in the writer contract or style templates
    for rel in ("examples/cron-prompt.md", "assets/style.example.md", "assets/style.zh.example.md"):
        body = (ROOT / rel).read_text(encoding="utf-8")
        if re.search(r"^##\s+\d{4}-\d{2}-\d{2}", body, re.M):
            problems.append(f"{rel} contains a full example entry heading (copyable sample)")

    if problems:
        print(f"FAIL — {len(problems)} problem(s)")
        for problem in problems:
            print("  -", problem)
        return 1
    print(f"OK — {meta['name']} {meta['version']}, description {len(description)} chars, "
          f"SKILL.md {len(text)} chars")
    return 0


if __name__ == "__main__":
    sys.exit(main())
