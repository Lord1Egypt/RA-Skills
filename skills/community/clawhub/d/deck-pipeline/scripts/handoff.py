#!/usr/bin/env python3
"""Write HANDOFF.md at session end.

Usage:
    python3 handoff.py <deck-stem> [--out HANDOFF.md]

Reads optional input via stdin as JSON:
{
  "target_file": "...",
  "backup": "...",
  "profile": "default v0.1.0",
  "completed": ["...", "..."],
  "unresolved": ["..."],
  "cautions": ["..."],
  "principles": ["..."],
  "constraints": ["..."]
}

Without stdin input, generates a template with placeholders.
"""
import sys
import json
import os
import datetime


TEMPLATE = """# {stem} — Handoff

**Date:** {date}
**Target file:** `{target_file}`
**Backup:** `{backup}`
**Tooling:** python-pptx, openpyxl{renderer_note}
**Profile in use:** {profile}

---

## Completed
{completed}

---

## Unresolved
{unresolved}

---

## Cautions
{cautions}

---

## Principles confirmed this session
{principles}

---

## Constraints
{constraints}
"""


def bulletize(items, default="- (none)"):
    if not items:
        return default
    return "\n".join(f"- {x}" for x in items)


def main():
    if len(sys.argv) < 2:
        print("Usage: handoff.py <deck-stem> [--out PATH]")
        sys.exit(1)
    stem = sys.argv[1]
    out = "HANDOFF.md"
    if "--out" in sys.argv:
        out = sys.argv[sys.argv.index("--out") + 1]

    data = {}
    if not sys.stdin.isatty():
        try:
            data = json.load(sys.stdin)
        except Exception:
            pass

    content = TEMPLATE.format(
        stem=stem,
        date=data.get("date", datetime.datetime.now().strftime("%Y-%m-%d")),
        target_file=data.get("target_file", "<path>"),
        backup=data.get("backup", "<path>"),
        renderer_note=(", " + data["renderer"]) if data.get("renderer") else "",
        profile=data.get("profile", "default v0.1.0"),
        completed=bulletize(data.get("completed")),
        unresolved=bulletize(data.get("unresolved")),
        cautions=bulletize(data.get("cautions"),
                           "- Do not open the deck in PowerPoint between sessions — autosave may overwrite changes."),
        principles=bulletize(data.get("principles")),
        constraints=bulletize(data.get("constraints")),
    )

    with open(out, "w") as f:
        f.write(content)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
