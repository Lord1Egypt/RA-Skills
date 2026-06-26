#!/usr/bin/env python3
"""
Batch driver for chat-history-importer skill.

Usage:
  python3 scripts/batch.py --dir ~/chat_exports [--since YYYY-MM-DD] [--dry-run] [--format openai|anthropic|auto]

Processes all JSON export files in the given directory.
Supports OpenAI (conversations.json) and Anthropic (conversations.json) export formats.
Writes daily episodic summaries to memory/episodic/YYYY-MM-DD.md (deduplicates on re-runs).
"""

import argparse
import json
import subprocess
import os
import sys
from pathlib import Path
from datetime import datetime

SCRIPTS_DIR = Path(__file__).parent

def detect_format(file_path: Path) -> str:
    """Auto-detect export format by inspecting JSON structure."""
    try:
        with open(file_path) as f:
            data = json.load(f)
        if isinstance(data, list) and data:
            first = data[0]
            if "chat_messages" in first:
                return "anthropic"
            if "mapping" in first or "conversation_id" in first:
                return "openai"
            # Anthropic also uses uuid + sender fields
            if "uuid" in first and "sender" not in str(first.get("chat_messages", [{}])[0] if first.get("chat_messages") else {}):
                return "anthropic"
    except Exception:
        pass
    return "openai"  # default

def parse_export(file_path: Path, fmt: str = "auto"):
    """Run appropriate parser and yield normalized chat objects."""
    if fmt == "auto":
        fmt = detect_format(file_path)

    parser_script = SCRIPTS_DIR / f"parse_{fmt}.py"
    if not parser_script.exists():
        print(f"  Warning: no parser for format '{fmt}', skipping {file_path.name}", file=sys.stderr)
        return

    proc = subprocess.run(
        ["python3", str(parser_script), str(file_path)],
        capture_output=True, text=True
    )
    if proc.returncode != 0:
        print(f"  Error parsing {file_path.name}: {proc.stderr.strip()}", file=sys.stderr)
        return
    for line in proc.stdout.strip().splitlines():
        if line:
            yield json.loads(line)

def load_identity_names(workspace: Path) -> tuple[str, str]:
    """
    Read agent name from IDENTITY.md and user name from USER.md.
    Returns (agent_name, user_name) — falls back to 'Assistant' / 'User' if not found.
    """
    agent_name = "Assistant"
    user_name = "User"

    identity_file = workspace / "IDENTITY.md"
    if identity_file.exists():
        for line in identity_file.read_text().splitlines():
            if line.strip().startswith("- **Name:**"):
                name = line.split("**Name:**", 1)[-1].strip()
                if name:
                    agent_name = name
                break

    user_file = workspace / "USER.md"
    if user_file.exists():
        for line in user_file.read_text().splitlines():
            if line.strip().startswith("- **Name:**"):
                name = line.split("**Name:**", 1)[-1].strip()
                if name:
                    user_name = name
                break

    return agent_name, user_name


def humanize_role(role: str, agent_name: str, user_name: str) -> str:
    """Map raw role strings to human-readable speaker names."""
    if role in ("assistant",):
        return agent_name
    if role in ("user", "human"):
        return user_name
    return role.capitalize()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", required=True, help="Directory containing export JSON files")
    parser.add_argument("--since", help="Only process chats created on or after this date (YYYY-MM-DD)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing anything")
    parser.add_argument("--verbose", action="store_true", help="Show message count and snippet per chat")
    parser.add_argument("--format", choices=["openai", "anthropic", "auto"], default="auto",
                        help="Export format (default: auto-detect)")
    parser.add_argument("--agent-name", help="Override agent name (default: read from IDENTITY.md)")
    parser.add_argument("--user-name", help="Override user name (default: read from USER.md)")
    args = parser.parse_args()

    # Use environment variable to point to the right agent workspace
    workspace = Path(os.environ.get("OPENCLAW_WORKSPACE", Path.home() / ".openclaw/workspace"))
    episodic_dir = workspace / "memory/episodic"

    # Resolve speaker names (from IDENTITY.md / USER.md, or CLI overrides)
    agent_name, user_name = load_identity_names(workspace)
    if args.agent_name:
        agent_name = args.agent_name
    if args.user_name:
        user_name = args.user_name
    print(f"Speaker mapping: 'assistant' → '{agent_name}' | 'user' → '{user_name}'")

    base_dir = Path(args.dir).expanduser()
    if not base_dir.is_dir():
        print(f"Error: directory not found: {base_dir}", file=sys.stderr)
        sys.exit(1)

    since_date = None
    if args.since:
        since_date = datetime.strptime(args.since, "%Y-%m-%d").date()

    # Only process known conversation files — skip metadata files
    SKIP_FILES = {"user.json", "user_settings.json", "export_manifest.json", "shared_conversations.json", "message_feedback.json"}
    json_files = [f for f in base_dir.glob("*.json") if f.name not in SKIP_FILES]
    if not json_files:
        print(f"No conversation JSON files found in {base_dir}")
        return

    total_chats = 0
    for file in json_files:
        fmt = args.format if args.format != "auto" else detect_format(file)
        print(f"Processing {file.name} (format: {fmt})...")
        for chat in parse_export(file, fmt):
            chat_date = datetime.strptime(chat["date"], "%Y-%m-%d").date()
            if since_date and chat_date < since_date:
                continue
            total_chats += 1
            msg_count = len(chat['messages'])
            print(f"  • {chat['title']} ({chat['date']}) — {msg_count} messages")
            if args.verbose:
                # Show first substantive user message as a preview
                for msg in chat['messages']:
                    if msg['role'] == 'user' and len(msg['content'].strip()) > 20:
                        preview = msg['content'].strip()[:120].replace("\n", " ")
                        print(f"    └─ {preview}...")
                        break
            if not args.dry_run:
                # Write episodic summary
                episodic_dir.mkdir(parents=True, exist_ok=True)
                mem_file = episodic_dir / f"{chat['date']}.md"

                # Check if episodic entry already exists
                already_in_episodic = mem_file.exists() and f"Chat ID: {chat['id']}" in mem_file.read_text()

                if not already_in_episodic:
                    entry = f"\n## Chat: {chat['title']}\n- Chat ID: {chat['id']}\n- Messages: {len(chat['messages'])}\n"
                    summary = []
                    for msg in chat['messages']:
                        speaker = humanize_role(msg['role'], agent_name, user_name)
                        content = msg['content'][:200].replace("\n", " ")
                        summary.append(f"- {speaker}: {content}...")
                    entry += "\n".join(summary) + "\n"
                    with open(mem_file, 'a') as f:
                        f.write(entry)
                    print(f"    Wrote episodic entry")
                else:
                    print(f"    (episodic already exists, skipping write)")


            else:
                print("  (dry run, no writes)")

    print(f"\nProcessed {total_chats} chats.")

if __name__ == "__main__":
    import sys
    main()