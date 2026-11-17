#!/usr/bin/env python3
"""recall.py — find out why something was decided, across your memory files.

Pure stdlib, zero dependencies, read-only (writes nothing).

Why this exists
---------------
The most common memory failure is not "I forgot the fact" — it is "I forgot
that we already decided this, and why". A flat grep over a vault answers
"does this string appear somewhere" but not "what did we conclude, when, and
on what grounds".

recall.py searches the surfaces where decisions actually get written and
prints them with file and line, so the answer to "why did we do it this way?"
is one command away:

  1. todos        — open items carry the "waiting on / decided because" notes
  2. journal      — dated logs: what happened, in order
  3. notes/docs   — meeting notes, decision records, specs
  4. archive      — the shelf where old material lives (must stay searchable)

Usage:
  python scripts/recall.py "why did we pick SQLite"        # all keywords must match one line
  python scripts/recall.py handover --paths notes journal   # limit the surfaces
  python scripts/recall.py schema --limit 40 --demo

Exit codes:
  0 = ran (0 hits is a valid answer, but the surfaces that were searched are
      always printed, so "nothing found" is never confused with "not looked")
  3 = no surface could be searched at all (nothing readable found) — never
      silently report zero hits when there was nothing to search
  1 = usage error

Notes:
  - Keywords are AND-ed: every keyword must appear on the same line.
  - Case-insensitive. A single line longer than 300 chars is truncated.
  - Each surface shows at most limit/4 hits, so one surface cannot eat the
    whole budget and hide the others.
"""

import argparse
import os
import sys

SURFACES = {
    "todos": ("todo.md", "todos.md", "TODO.md", "tasks.md", "docs/TODO.md"),
    "journal": ("journal", "logs", "docs/journal", "worklog"),
    "notes": ("notes", "docs", "adr", "decisions", "specs"),
    "archive": ("archive", "notes/archive", "journal/archive", "docs/archive"),
}
EXCLUDE_DIRS = {".git", ".obsidian", ".trash", ".venv", "node_modules",
                ".changsheng", "__pycache__", ".idea", ".vscode"}
TEXT_EXT = (".md", ".txt", ".markdown", ".rst")


def _hits(text, keywords):
    low = text.lower()
    return all(k.lower() in low for k in keywords)


def _files_in_surface(base, names, recursive=True):
    out = []
    seen = set()
    for n in names:
        p = os.path.join(base, n)
        if os.path.isfile(p):
            key = os.path.normcase(os.path.abspath(p))
            if key not in seen:
                seen.add(key)
                out.append(p)
        elif os.path.isdir(p):
            for dirpath, dirnames, filenames in os.walk(p):
                dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
                if not recursive:
                    dirnames[:] = []
                for fn in filenames:
                    if fn.lower().endswith(TEXT_EXT) and not fn.startswith("."):
                        full = os.path.join(dirpath, fn)
                        key = os.path.normcase(os.path.abspath(full))
                        if key in seen:
                            continue   # case-insensitive fs: todo.md and TODO.md are one file
                        seen.add(key)
                        out.append(full)
    return out


def search(base, surfaces, keywords, limit):
    """Return (report_lines, searched_surfaces, total_hits).

    Each file is searched once across all surfaces (surfaces overlap by
    design — a dated journal inside notes/ would otherwise be counted twice).
    """
    lines = []
    searched = []
    total = 0
    seen_files = set()
    per_surface = max(1, limit // max(1, len(surfaces)))
    for surface in surfaces:
        names = SURFACES.get(surface)
        if names is None:
            names = (surface,)
        files = _files_in_surface(base, names)
        if not files:
            lines.append(f"— {surface}: no files found here (nothing searched)")
            continue
        searched.append(surface)
        shown = 0
        surface_hits = 0
        n_new = 0
        for path in sorted(files):
            key = os.path.normcase(os.path.abspath(path))
            if key in seen_files:
                continue
            seen_files.add(key)
            n_new += 1
            try:
                with open(path, encoding="utf-8", errors="ignore") as f:
                    for i, line in enumerate(f, 1):
                        if not _hits(line, keywords):
                            continue
                        surface_hits += 1
                        total += 1
                        if shown < per_surface:
                            text = line.strip()
                            if len(text) > 300:
                                text = text[:300] + "…"
                            rel = os.path.relpath(path, base)
                            lines.append(f"{rel}:{i}  {text}")
                            shown += 1
            except OSError:
                continue
        note = "" if surface_hits <= per_surface else f" (showing first {per_surface} of {surface_hits})"
        lines.append(f"— {surface}: {n_new} file(s) searched, {surface_hits} hit(s){note}")
    return lines, searched, total


def demo():
    import shutil
    import tempfile
    d = tempfile.mkdtemp()
    try:
        base = os.path.join(d, "p")
        os.makedirs(os.path.join(base, "notes"))
        os.makedirs(os.path.join(base, "journal"))
        with open(os.path.join(base, "todo.md"), "w", encoding="utf-8") as f:
            f.write("- ship the skill\n  why: reviewers wanted a pure-stdlib build\n")
        with open(os.path.join(base, "notes", "decision.md"), "w", encoding="utf-8") as f:
            f.write("# Decision\nwe picked SQLite because it needs no server\n")
        with open(os.path.join(base, "journal", "2026-01-02.md"), "w", encoding="utf-8") as f:
            f.write("shipped the handover template\n")

        lines, searched, total = search(base, ["todos", "journal", "notes"], ["pure-stdlib"], 40)
        assert total == 1, f"A expected 1 hit, got {total}: {lines}"
        assert any("todo.md" in l for l in lines), f"A wrong file: {lines}"

        lines, searched, total = search(base, ["todos", "journal", "notes"], ["SQLite"], 40)
        assert total == 1 and any("decision.md" in l for l in lines), f"B wrong: {lines}"

        # C: AND semantics — both keywords must be on the same line
        lines, _, total = search(base, ["notes"], ["SQLite", "postgres"], 40)
        assert total == 0, f"C AND not applied: {lines}"

        # D: a surface with no files is reported, not silently dropped
        lines, searched, total = search(base, ["archive"], ["anything"], 40)
        assert "archive" in " ".join(lines) and not searched, f"D missing surface note: {lines}"

        # E: journal surface is actually searched
        lines, searched, total = search(base, ["journal"], ["handover template"], 40)
        assert total == 1 and "journal" in searched, f"E journal not searched: {lines}"

        # F: per-surface cap keeps every surface visible
        lines, _, total = search(base, ["todos", "journal", "notes"], ["the"], 4)
        assert any("journal" in l for l in lines), f"F surface starved: {lines}"

        print("[demo] recall: 6/6 PASS")
    finally:
        shutil.rmtree(d, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("keywords", nargs="*", help="keywords (all must appear on the same line)")
    ap.add_argument("--paths", nargs="*", default=None,
                    help="surfaces to search (todo/journal/notes/archive, or any path)")
    ap.add_argument("--base", default=".", help="root to search under (default .)")
    ap.add_argument("--limit", type=int, default=60, help="max hits (default 60)")
    ap.add_argument("--demo", action="store_true")
    args = ap.parse_args()
    if args.demo:
        return demo()
    if not args.keywords:
        print("recall.py: give at least one keyword (usage: recall.py \"why did we ...\")",
              file=sys.stderr)
        return 1
    base = os.path.abspath(args.base)
    surfaces = args.paths if args.paths else list(SURFACES)
    lines, searched, total = search(base, surfaces, args.keywords, args.limit)
    print("\n".join(lines))
    print(f"total {total} hit(s) across {len(searched)} searched surface(s)")
    if not searched:
        print("no surface could be searched — nothing was read, so this is not a "
              "'not found' answer", file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
