#!/usr/bin/env python3
"""
create_agent_bundle.py — Generate an agent identity skill bundle.

Usage:
  python3 create_agent_bundle.py \
    --name "Aria" \
    --emoji "✨" \
    --nature "AI companion with a sharp wit and genuine care" \
    --vibe "Warm but direct. Smart without being showy." \
    --serving "solo founders who need a reliable thinking partner" \
    --slug "aria" \
    --version "1.0.0" \
    --output-dir ./dist

Generates a .skill file at ./dist/aria.skill containing:
  - assets/workspace-template/SOUL.md
  - assets/workspace-template/IDENTITY.md
  - assets/workspace-template/AGENTS.md
  - SKILL.md (install instructions for the agent identity)
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
SKILL_DIR = SCRIPT_DIR.parent
TEMPLATE_DIR = SKILL_DIR / "assets" / "workspace-template"


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9-]", "-", name.lower()).strip("-")


def fill_template(text: str, replacements: dict) -> str:
    for key, value in replacements.items():
        text = text.replace(f"{{{{{key}}}}}", value)
    return text


def build_skill_md(name: str, slug: str, emoji: str, nature: str, vibe: str, serving: str, version: str) -> str:
    return f"""---
name: {slug}
description: Agent identity package for {name} {emoji} — installs SOUL.md, IDENTITY.md, and AGENTS.md into an OpenClaw workspace to give an AI agent its personality, name, and operational rules. Use when setting up a new agent or replacing an agent's identity files.
---

# {name} {emoji} — Agent Identity

This skill installs the workspace identity files for **{name}**, an AI agent with the following profile:

- **Nature:** {nature}
- **Vibe:** {vibe}
- **Serving:** {serving}

## Installation

Copy the three files from `assets/workspace-template/` into the agent's workspace directory (the folder pointed to by `workspace` in `openclaw.json`):

```bash
cp assets/workspace-template/SOUL.md     /path/to/workspace/SOUL.md
cp assets/workspace-template/IDENTITY.md /path/to/workspace/IDENTITY.md
cp assets/workspace-template/AGENTS.md  /path/to/workspace/AGENTS.md
```

Then restart the OpenClaw gateway so the agent picks up the new identity.

## Files

| File | Purpose |
|------|---------|
| `SOUL.md` | Who {name} is — personality, tone, values |
| `IDENTITY.md` | Name, emoji, avatar path |
| `AGENTS.md` | Operational rules — memory, safety, group chat behavior |

## Version

`{version}` — generated {date.today().isoformat()}
"""


def main():
    parser = argparse.ArgumentParser(description="Create an agent identity skill bundle")
    parser.add_argument("--name", required=True, help="Agent name (e.g. 'Aria')")
    parser.add_argument("--emoji", default="🤖", help="Agent emoji (e.g. '✨')")
    parser.add_argument("--nature", required=True, help="One-line description of the agent's nature/role")
    parser.add_argument("--vibe", required=True, help="Personality vibe description")
    parser.add_argument("--serving", default="the user", help="Who the agent serves")
    parser.add_argument("--slug", help="Skill slug (auto-derived from name if omitted)")
    parser.add_argument("--version", default="1.0.0", help="Skill version")
    parser.add_argument("--output-dir", default=".", help="Directory to write the .skill file")
    args = parser.parse_args()

    slug = args.slug or slugify(args.name)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    replacements = {
        "AGENT_NAME": args.name,
        "AGENT_EMOJI": args.emoji,
        "AGENT_NATURE": args.nature,
        "AGENT_VIBE": args.vibe,
        "AGENT_SLUG": slug,
        "AGENT_AVATAR": f"*(not yet set)*",
        "DATE": date.today().isoformat(),
    }

    # Build skill in a temp directory
    with tempfile.TemporaryDirectory() as tmpdir:
        skill_dir = Path(tmpdir) / slug
        workspace_dir = skill_dir / "assets" / "workspace-template"
        workspace_dir.mkdir(parents=True)

        # Fill and write the 3 identity templates
        for tpl_name in ("SOUL.md", "IDENTITY.md", "AGENTS.md"):
            tpl_path = TEMPLATE_DIR / tpl_name
            if not tpl_path.exists():
                print(f"ERROR: Template not found: {tpl_path}", file=sys.stderr)
                sys.exit(1)
            content = tpl_path.read_text()
            filled = fill_template(content, replacements)
            (workspace_dir / tpl_name).write_text(filled)

        # Write SKILL.md
        skill_md = build_skill_md(
            name=args.name,
            slug=slug,
            emoji=args.emoji,
            nature=args.nature,
            vibe=args.vibe,
            serving=args.serving,
            version=args.version,
        )
        (skill_dir / "SKILL.md").write_text(skill_md)

        # Run package_skill.py
        packager = SCRIPT_DIR / "package_skill.py"
        result = subprocess.run(
            [sys.executable, str(packager), str(skill_dir), str(output_dir)],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print("Packaging failed:", file=sys.stderr)
            print(result.stdout, file=sys.stderr)
            print(result.stderr, file=sys.stderr)
            sys.exit(1)

        skill_file = output_dir / f"{slug}.skill"
        print(f"✅ Created: {skill_file}")
        print(f"   Name:    {args.name} {args.emoji}")
        print(f"   Slug:    {slug}")
        print(f"   Version: {args.version}")
        print()
        print("To upload to ClawHub:")
        print(f'  clawhub publish {skill_file} --slug {slug} --name "{args.name}" --version {args.version}')


if __name__ == "__main__":
    main()
