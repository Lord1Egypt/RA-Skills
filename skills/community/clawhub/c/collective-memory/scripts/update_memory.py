#!/usr/bin/env python3
"""
collective-memory: broadcast a single memory note to multiple agent workspaces.

Pure file-ops, zero network, zero LLM. The calling agent decides what to write
and which key to look up; this script does the file work atomically.

Match strategy (idempotent two-step):
  Step 1: heading-line exact match (English/Chinese word-segment OR)
          → replace that section
  Step 2: no match → append

Usage (single target — backward compatible):
  python3 update_memory.py \\
    --workspace /path/to/workspace \\
    --file MEMORY.md \\
    --key   "API key path" \\
    --content "## API key path\\nstored in .secrets/api-keys.env"

Usage (multi-target broadcast):
  python3 update_memory.py \\
    --target /path/to/ws1:MEMORY.md \\
    --target /path/to/ws2:AGENTS.md \\
    --key   "API key path" \\
    --content "## API key path\\n..."

Usage (auto-discover agents under a parent directory):
  python3 update_memory.py \\
    --discover-under ~/.claude/projects \\
    --file MEMORY.md \\
    --key   "API key path" \\
    --content "## API key path\\n..."

  Multiple --discover-under flags are allowed.

Common flags:
  --dry-run     Show planned changes, do not modify any file.
  --json        Emit machine-readable JSON results to stdout.

Exit codes:
  0 = all targets succeeded (or dry-run completed)
  1 = bad arguments or at least one target failed
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import List, Optional, Tuple


# ── Tokenization ────────────────────────────────────────────────────────────

def tokenize(text: str) -> List[str]:
    """
    Mixed-language tokenizer.

    English/digit runs: kept as a single lowercased token if length >= 1
      (changed from >= 2 in v1.0.0 of the internal version — single-char
       English keys like "a" / "v" / "y" now match correctly).
    CJK runs: any 2+ contiguous CJK char span becomes one token; single CJK
      chars are dropped because they are too ambiguous.
    """
    tokens: List[str] = []
    for seg in re.findall(r"[A-Za-z0-9]+", text):
        if len(seg) >= 1:
            tokens.append(seg.lower())
    for seg in re.findall(r"[\u4e00-\u9fff]{2,}", text):
        tokens.append(seg)
    return tokens


# ── Heading utilities ───────────────────────────────────────────────────────

def extract_headings(lines: List[str]) -> List[Tuple[int, str]]:
    """Return [(line_index, heading_text), ...] for #..#### headings."""
    out: List[Tuple[int, str]] = []
    for i, line in enumerate(lines):
        m = re.match(r"^#{1,4}\s+(.+)", line.rstrip())
        if m:
            out.append((i, m.group(1).strip()))
    return out


def get_section_range(lines: List[str], heading_line: int) -> Tuple[int, int]:
    """
    Return (start, end) where end is exclusive; section ends at the next
    same-or-higher level heading, or EOF.
    """
    level_match = re.match(r"^(#+)", lines[heading_line])
    if not level_match:
        return (heading_line, heading_line + 1)
    level = len(level_match.group(1))
    end = heading_line + 1
    while end < len(lines):
        m = re.match(r"^(#+)\s", lines[end])
        if m and len(m.group(1)) <= level:
            break
        end += 1
    return (heading_line, end)


def match_by_heading(lines: List[str], key: str) -> Optional[int]:
    """Find first heading line whose text contains any token from `key`."""
    tokens = tokenize(key)
    if not tokens:
        tokens = [key.lower()]
    for line_no, title in extract_headings(lines):
        title_lower = title.lower()
        if any(tok in title_lower for tok in tokens):
            return line_no
    return None


# ── Core upsert ─────────────────────────────────────────────────────────────

def upsert_memory(workspace: str, filename: str, key: str, content: str,
                  dry_run: bool = False) -> Tuple[str, str]:
    """
    Upsert content into <workspace>/<filename>.
    Returns (action, filepath_str) where action ∈ {"updated", "appended", "would_update", "would_append"}.
    """
    filepath = Path(workspace) / filename

    if not filepath.exists():
        if not dry_run:
            filepath.parent.mkdir(parents=True, exist_ok=True)
            filepath.write_text(f"# {filename.replace('.md', '')}\n\n", encoding="utf-8")
        # When dry-run on a non-existing file, treat as "would_append"
        return ("would_append" if dry_run else "appended", str(filepath))

    raw = filepath.read_text(encoding="utf-8")
    lines = raw.splitlines(keepends=True)
    heading_line = match_by_heading(lines, key)

    if heading_line is not None:
        if dry_run:
            return ("would_update", str(filepath))
        start, end = get_section_range(lines, heading_line)
        lines[start:end] = [content.rstrip("\n") + "\n"]
        filepath.write_text("".join(lines), encoding="utf-8")
        return ("updated", str(filepath))

    if dry_run:
        return ("would_append", str(filepath))
    suffix = "\n" if raw and not raw.endswith("\n") else ""
    filepath.write_text(raw + suffix + "\n" + content.rstrip("\n") + "\n",
                        encoding="utf-8")
    return ("appended", str(filepath))


# ── Target resolution ───────────────────────────────────────────────────────

def parse_target(spec: str) -> Tuple[str, str]:
    """
    Parse '<workspace>:<file>' spec. Supports paths containing ':' on Windows
    drive letters by splitting on the LAST ':' only.
    """
    if ":" not in spec:
        raise ValueError(f"--target must be '<workspace>:<file>', got: {spec!r}")
    workspace, filename = spec.rsplit(":", 1)
    if not workspace or not filename:
        raise ValueError(f"--target both sides required, got: {spec!r}")
    return (str(Path(workspace).expanduser()), filename)


def discover_under(parent: str, default_file: str) -> List[Tuple[str, str]]:
    """
    Auto-discover candidate workspaces directly under `parent`.

    A candidate is any first-level subdirectory of `parent` that is a directory.
    The default file name (default_file) is paired with each.

    Returns [(workspace, filename), ...]; empty list if parent doesn't exist.
    """
    p = Path(parent).expanduser()
    if not p.is_dir():
        return []
    out: List[Tuple[str, str]] = []
    for child in sorted(p.iterdir()):
        if child.is_dir() and not child.name.startswith("."):
            out.append((str(child), default_file))
    return out


# ── Entry point ─────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Broadcast a memory note to one or more agent workspaces "
                    "(pure file-ops, zero network, zero LLM).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    # Single-target mode (backward compatible)
    parser.add_argument("--workspace", help="Single workspace path (legacy mode)")
    parser.add_argument("--file",
                        help="Default file name (e.g. MEMORY.md). Used for "
                             "--workspace and --discover-under modes.")
    # Multi-target mode
    parser.add_argument("--target", action="append", default=[],
                        help="Repeatable. '<workspace>:<file>' spec. "
                             "Pass once per agent target.")
    # Auto-discover mode
    parser.add_argument("--discover-under", action="append", default=[],
                        help="Repeatable. Auto-discover workspaces directly "
                             "under this parent dir. Combined with --file.")
    # Required for all modes
    parser.add_argument("--key", required=True,
                        help="Lookup key used to find an existing heading "
                             "(tokenized OR-match against heading text).")
    parser.add_argument("--content", required=True,
                        help="Full Markdown block to upsert. Must include "
                             "its own heading line.")
    # Behavior flags
    parser.add_argument("--dry-run", action="store_true",
                        help="Show planned changes; do not modify files.")
    parser.add_argument("--json", action="store_true",
                        help="Emit machine-readable JSON result.")
    args = parser.parse_args()

    # Resolve targets
    targets: List[Tuple[str, str]] = []
    if args.workspace:
        if not args.file:
            parser.error("--workspace requires --file")
        targets.append((str(Path(args.workspace).expanduser()), args.file))
    for spec in args.target:
        try:
            targets.append(parse_target(spec))
        except ValueError as e:
            parser.error(str(e))
    if args.discover_under:
        if not args.file:
            parser.error("--discover-under requires --file (default file name)")
        for parent in args.discover_under:
            targets.extend(discover_under(parent, args.file))

    if not targets:
        parser.error("No targets resolved. Provide --workspace, --target, "
                     "or --discover-under.")

    # Deduplicate while preserving order
    seen = set()
    uniq_targets = []
    for t in targets:
        key = (str(Path(t[0]).resolve(strict=False)), t[1])
        if key in seen:
            continue
        seen.add(key)
        uniq_targets.append(t)

    # Execute
    results = []
    overall_ok = True
    for workspace, filename in uniq_targets:
        if not os.path.isdir(workspace):
            results.append({"workspace": workspace, "file": filename,
                            "status": "error", "reason": "workspace not found"})
            overall_ok = False
            continue
        try:
            action, filepath = upsert_memory(workspace, filename, args.key,
                                             args.content, dry_run=args.dry_run)
            results.append({"workspace": workspace, "file": filename,
                            "status": action, "path": filepath})
        except Exception as e:
            results.append({"workspace": workspace, "file": filename,
                            "status": "error", "reason": str(e)})
            overall_ok = False

    # Report
    if args.json:
        print(json.dumps({"dry_run": args.dry_run, "results": results},
                         ensure_ascii=False, indent=2))
    else:
        prefix = "[DRY-RUN] " if args.dry_run else ""
        print(f"{prefix}Broadcast to {len(uniq_targets)} target(s):")
        for r in results:
            mark = "✅" if r["status"] not in ("error",) else "❌"
            extra = f" — {r.get('reason', '')}" if r["status"] == "error" else ""
            print(f"  {mark} [{r['status']}] {r['workspace']} → {r['file']}{extra}")

    return 0 if overall_ok else 1


if __name__ == "__main__":
    sys.exit(main())
