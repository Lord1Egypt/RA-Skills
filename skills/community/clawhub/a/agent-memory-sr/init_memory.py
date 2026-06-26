#!/usr/bin/env python3
"""
Agent Memory — Workspace Initialization
========================================
Sets up a persistent memory structure for your AI agent.

Usage:
    python3 init_memory.py
    python3 init_memory.py --workspace /path/to/workspace
    python3 init_memory.py --workspace . --agent "Agent Smith" --user "Rose" --timezone "America/Denver"
    python3 init_memory.py --non-interactive --workspace .

Author: Shadow Rose
License: MIT
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
TEMPLATES_DIR = SCRIPT_DIR / "templates"

TEMPLATE_FILES = [
    ("AGENTS.md.template",      "AGENTS.md"),
    ("MEMORY.md.template",      "MEMORY.md"),
    ("USER.md.template",        "USER.md"),
    ("MASTER_MAP.md.template",  "MASTER_MAP.md"),
    ("HEARTBEAT.md.template",   "HEARTBEAT.md"),
    ("HANDOFF.md.template",     "HANDOFF.md"),
]

# Owner namespace templates (go into memory/owner/)
OWNER_TEMPLATE_FILES = [
    "identity.md",
    "preferences.md",
    "decisions.md",
    "learnings.md",
    "people.md",
    "projects.md",
]


def render_template(template_path: Path, substitutions: dict) -> str:
    """Read template and apply substitutions."""
    content = template_path.read_text(encoding="utf-8")
    for key, value in substitutions.items():
        content = content.replace("{{" + key + "}}", value)
    return content


def prompt(question: str, default: str) -> str:
    """Prompt with a default value."""
    answer = input(f"{question} [{default}]: ").strip()
    return answer if answer else default


def init_workspace(workspace: str, agent_name: str, user_name: str, timezone: str,
                   overwrite: bool = False) -> None:
    ws = Path(workspace).resolve()

    if not ws.exists():
        print(f"Creating workspace directory: {ws}")
        ws.mkdir(parents=True)

    # Create memory/ directory structure
    memory_dir = ws / "memory"
    memory_dir.mkdir(exist_ok=True)

    # Owner namespace (shared across all channels)
    owner_dir = memory_dir / "owner"
    owner_dir.mkdir(exist_ok=True)

    # Channel isolation directories
    for channel in ("discord", "telegram", "signal"):
        (memory_dir / "channels" / channel).mkdir(parents=True, exist_ok=True)

    # Ephemeral working scratch
    (memory_dir / "working").mkdir(exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    substitutions = {
        "AGENT_NAME": agent_name,
        "USER_NAME":  user_name,
        "TIMEZONE":   timezone,
        "DATE":       today,
    }

    created = []
    skipped = []

    for template_name, output_name in TEMPLATE_FILES:
        template_path = TEMPLATES_DIR / template_name
        if not template_path.exists():
            print(f"  WARNING: Template not found: {template_name}")
            continue

        output_path = ws / output_name

        if output_path.exists() and not overwrite:
            skipped.append(output_name)
            continue

        content = render_template(template_path, substitutions)
        output_path.write_text(content, encoding="utf-8")
        created.append(output_name)

    # Create owner namespace files
    owner_templates_dir = TEMPLATES_DIR / "owner"
    for fname in OWNER_TEMPLATE_FILES:
        src = owner_templates_dir / fname
        dest = owner_dir / fname
        if not src.exists():
            continue
        if dest.exists() and not overwrite:
            skipped.append(f"memory/owner/{fname}")
            continue
        content = render_template(src, substitutions)
        dest.write_text(content, encoding="utf-8")
        created.append(f"memory/owner/{fname}")

    # Create today's memory file if it doesn't exist
    daily_log = memory_dir / f"{today}.md"
    if not daily_log.exists():
        daily_log.write_text(
            f"# {today}\n\n*Session log — append notes here as the day progresses.*\n",
            encoding="utf-8"
        )
        created.append(f"memory/{today}.md")

    # Summary
    print(f"\nOK. Agent Memory initialized at: {ws}")
    print(f"\nCreated ({len(created)}):")
    for f in created:
        print(f"  + {f}")

    if skipped:
        print(f"\nSkipped (already exist -- use --overwrite to replace):")
        for f in skipped:
            print(f"  ~ {f}")

    print(f"""
Next steps:
  1. Edit USER.md               — fill in your profile (most important)
  2. Edit memory/owner/         — fill in identity.md + preferences.md at minimum
  3. Edit AGENTS.md             — add behavioral rules and conventions
  4. Edit MASTER_MAP.md         — add your active projects and systems
  5. Add this to your agent's system prompt:

     Session start order:
     1. Check HANDOFF.md first — if it has real content, read + follow it, then archive to memory/{today}-handoff.md and clear
     2. Read AGENTS.md
     3. Read USER.md
     4. Read memory/owner/identity.md + memory/owner/preferences.md
     5. Read MASTER_MAP.md
     6. Read MEMORY.md (main/direct sessions only — not group chats)
     7. Read memory/{today}.md if it exists

  Owner namespace files (memory/owner/):
    identity.md    — who you and the agent are (load every session)
    preferences.md — communication style and preferences (load most sessions)
    decisions.md   — important choices + rationale (load when relevant)
    learnings.md   — lessons learned and patterns (load after mistakes)
    people.md      — trusted users and relationships (load when people mentioned)
    projects.md    — active and completed work (load during project work)

  Channel isolation (memory/channels/):
    discord/ telegram/ signal/ — isolated per-channel memory
    Owner DM sessions share memory/owner/ context
    Guild/group chats stay isolated — never bleed into owner sessions
""")


def main():
    parser = argparse.ArgumentParser(
        description="Initialize Agent Memory workspace structure",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 init_memory.py
  python3 init_memory.py --workspace /path/to/my/workspace
  python3 init_memory.py --workspace . --agent "Assistant" --user "Alice" --timezone "America/New_York"
  python3 init_memory.py --non-interactive --workspace .
        """
    )
    parser.add_argument("--workspace", default=None, help="Path to workspace directory (default: current dir)")
    parser.add_argument("--agent", default=None, help="Agent name")
    parser.add_argument("--user", default=None, help="User/human name")
    parser.add_argument("--timezone", default=None, help="Timezone (e.g. America/New_York)")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing files")
    parser.add_argument("--non-interactive", action="store_true", help="Use defaults without prompting")
    args = parser.parse_args()

    print("=" * 50)
    print("  Agent Memory — Workspace Setup")
    print("=" * 50)

    if args.non_interactive:
        workspace  = args.workspace  or "."
        agent_name = args.agent      or "Agent"
        user_name  = args.user       or "User"
        timezone   = args.timezone   or "UTC"
    else:
        workspace  = args.workspace  or prompt("Workspace path", ".")
        agent_name = args.agent      or prompt("Agent name", "Agent")
        user_name  = args.user       or prompt("Your name", "User")
        timezone   = args.timezone   or prompt("Your timezone", "UTC")
        print()

    init_workspace(workspace, agent_name, user_name, timezone, overwrite=args.overwrite)


if __name__ == "__main__":
    main()
