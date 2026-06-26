#!/usr/bin/env python3
"""Scaffold a compatibility-preserving working memory workspace.

Use when initializing a project that needs layered memory files without breaking
OpenClaw conventions.

Usage:
    python scaffold.py /path/to/project-root [--agent-name "My Agent"] [--user-name "User"]

Creates canonical files:
    MEMORY.md
    memory/resumption.md
    memory/threads.md
    memory/state.json
    memory/index.md
    memory/archive.md
    memory/events.json

Creates compatibility helpers:
    memory/daily/           # mirror-only directory for tools that still expect it

Keep daily logs canonical at `memory/YYYY-MM-DD.md`.
Never overwrite existing files.
"""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def create_if_missing(path: Path, content: str) -> bool:
    if path.exists():
        print(f"  SKIP (exists): {path}")
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  CREATE: {path}")
    return True


def scaffold(root: str, agent_name: str = "Agent", user_name: str = "User"):
    root = Path(root).resolve()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    now_iso = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    print(f"\nScaffolding working memory system in: {root}\n")

    create_if_missing(root / "MEMORY.md", f"""# Long-Term Memory

> Last reviewed: {today}
> Next review due: after 5 sessions or 7 days, whichever comes first

---

## Active

### About {user_name}
- [1 session] [low] (Add observations about the user's preferences, working style, and patterns here)

### About This Project
- [1 session] [low] (Add key facts about the project, its goals, and architectural decisions here)

### Working Style
- [1 session] [low] (Add notes about how the user prefers to interact — e.g., co-design vs. receive proposals)

---

## Fading

(Nothing here yet)

---

## Maintenance Log

| Date       | Action                     |
|------------|----------------------------|
| {today} | Initial memory file created |
""")

    create_if_missing(root / "memory" / "resumption.md", f"""# Resumption Note

> Written: {today}, initial setup
> For: my next session self

---

This is a fresh compatibility-preserving working memory system. Daily logs stay flat under memory/YYYY-MM-DD.md.
""")

    create_if_missing(root / "memory" / "threads.md", """# Active Threads

> Threads carry state so resuming doesn't require re-reading all related daily logs.
> Each thread is self-contained enough to jump back into cold.

---

<!-- Template for new threads:

## Thread: [Title]
- **ID**: thread-[slug]
- **Status**: active
- **Started**: YYYY-MM-DD
- **Last touched**: YYYY-MM-DD
- **Sessions involved**: 1

### Current Position
[Where the conversation currently stands — enough context to resume cold]

### Key Decisions Made
1. **[Decision]** — [reasoning]. [ref: memory/YYYY-MM-DD.md#decisions]

### Open Questions
- [ ] [Question]

### Next Likely Steps
1. [Step]

### Related
- [Links to other threads, MEMORY.md sections, etc.]
-->

(No active threads yet. Create your first thread when an ongoing topic emerges.)

---

# Closed Threads

(No closed threads yet.)
""")

    state = {
        "_schema_version": "0.2.0",
        "_description": "Machine-readable ephemeral state.",
        "last_session": {"timestamp": now_iso, "duration_minutes": 0, "daily_log": None},
        "session_counter": {"total": 0, "this_week": 0, "since_last_memory_review": 0},
        "active_threads": [],
        "pending_questions": [],
        "flags": {"memory_review_due": False, "threads_need_update": False, "archive_candidates_exist": False},
        "context_hints": {"current_mood_hypothesis": None, "conversation_style": None, "last_topic_position": "Fresh system — no prior sessions."},
    }
    create_if_missing(root / "memory" / "state.json", json.dumps(state, indent=2, ensure_ascii=False) + "\n")

    create_if_missing(root / "memory" / "index.md", f"""# Daily Log Index

> Auto-generated. Rebuilt weekly or when daily log count changes by 5+.
> Last rebuilt: {today}
> Total logs: 0

| Date | Threads Touched | Key Topics | Decisions | Mood/Tone |
|------|-----------------|------------|-----------|-----------|
""")

    create_if_missing(root / "memory" / "archive.md", """# Archived Memories

> Entries demoted from MEMORY.md after 20+ sessions without recall.

---

(No archived entries yet.)
""")

    create_if_missing(root / "memory" / "events.json", json.dumps({
        "events": []
    }, indent=2, ensure_ascii=False) + "\n")

    (root / "memory" / "daily").mkdir(parents=True, exist_ok=True)

    print(f"""
Done! Your working memory system is ready at: {root}

Daily logs remain flat under memory/YYYY-MM-DD.md for compatibility.
""")


def is_legacy_workspace(root: Path) -> bool:
    """Return True if this looks like a legacy workspace with AGENT.md + MEMORY.md but no state.json."""
    return (
        (root / "AGENT.md").exists()
        and (root / "MEMORY.md").exists()
        and not (root / "memory" / "state.json").exists()
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scaffold a working memory system")
    parser.add_argument("root", help="Target project root directory")
    parser.add_argument("--agent-name", default="Agent")
    parser.add_argument("--user-name", default="User")
    parser.add_argument("--force-scaffold", action="store_true",
                        help="Run scaffold even if a legacy system is detected")
    args = parser.parse_args()

    root = Path(args.root).resolve()

    if not args.force_scaffold and is_legacy_workspace(root):
        print(f"\n  Legacy memory system detected at: {root}")
        print(f"  Found: AGENT.md + MEMORY.md without state.json")
        print()
        print(f"  Use migrate.py instead to preserve existing data:")
        print(f"    python migrate.py {root}")
        print(f"    python migrate.py {root} --dry-run    # preview changes first")
        print()
        print(f"  Or run with --force-scaffold to ignore legacy detection.")
    else:
        scaffold(args.root, args.agent_name, args.user_name)

