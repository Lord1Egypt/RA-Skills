#!/usr/bin/env python3
"""Migrate a legacy workspace memory system to the layered working-memory architecture.

Detects:
    /workspace/AGENTS.md or AGENT.md — agent configuration
    /workspace/MEMORY.md             — long-term memory (flat or unstructured)
    /workspace/memory/               — daily session logs (YYYY-MM-DD.md)

Creates (only missing files):
    memory/resumption.md
    memory/threads.md
    memory/state.json      — bootstrapped from existing daily logs
    memory/index.md        — rebuilt from existing daily logs
    memory/archive.md
    memory/events.json

Patches (surgically, not appended):
    AGENTS.md / AGENT.md   — injects into existing sections at anchor points

Preserves:
    MEMORY.md              — restructured with Active/Fading/Maintenance tiers if flat
    memory/YYYY-MM-DD.md   — untouched, canonical location confirmed

Usage:
    python migrate.py /workspace
    python migrate.py /workspace --dry-run
    python migrate.py /workspace --skip-agent-patch
"""

import argparse
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# Detection
# ---------------------------------------------------------------------------

def find_agent_md(root: Path) -> Optional[Path]:
    """Return the path to the agent config file, preferring AGENTS.md over AGENT.md."""
    for name in ("AGENTS.md", "AGENT.md"):
        p = root / name
        if p.exists():
            return p
    return None


def detect_legacy(root: Path) -> dict:
    """Scan *root* and return a report of what exists."""
    memory_dir = root / "memory"
    date_glob = "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].md"

    daily_logs = sorted(memory_dir.glob(date_glob)) if memory_dir.exists() else []
    legacy_daily = sorted((memory_dir / "daily").glob(date_glob)) if (memory_dir / "daily").exists() else []

    agent_path = find_agent_md(root)

    return {
        "root": root,
        "agent_md_path": agent_path,
        "agent_md_name": agent_path.name if agent_path else None,
        "has_agent_md": agent_path is not None,
        "has_memory_md": (root / "MEMORY.md").exists(),
        "has_memory_dir": memory_dir.exists(),
        "daily_log_count": len(daily_logs),
        "legacy_daily_count": len(legacy_daily),
        "daily_logs": daily_logs,
        "legacy_daily_logs": legacy_daily,
        "has_resumption": (memory_dir / "resumption.md").exists(),
        "has_threads": (memory_dir / "threads.md").exists(),
        "has_state": (memory_dir / "state.json").exists(),
        "has_index": (memory_dir / "index.md").exists(),
        "has_archive": (memory_dir / "archive.md").exists(),
        "has_events": (memory_dir / "events.json").exists(),
        "is_legacy": (
            agent_path is not None
            and (root / "MEMORY.md").exists()
            and not (memory_dir / "state.json").exists()
        ),
    }


def print_detection(report: dict):
    root = report["root"]
    agent_name = report["agent_md_name"] or "(none)"
    print(f"\n{'='*60}")
    print(f"  Legacy detection: {root}")
    print(f"{'='*60}")
    print(f"  Agent config       {agent_name if report['has_agent_md'] else 'missing'}")
    print(f"  MEMORY.md          {'FOUND' if report['has_memory_md'] else 'missing'}")
    print(f"  memory/ dir        {'FOUND' if report['has_memory_dir'] else 'missing'}")
    print(f"  Flat daily logs    {report['daily_log_count']}")
    print(f"  Legacy daily/ logs {report['legacy_daily_count']}")
    print(f"  resumption.md      {'exists' if report['has_resumption'] else 'NEEDS CREATION'}")
    print(f"  threads.md         {'exists' if report['has_threads'] else 'NEEDS CREATION'}")
    print(f"  state.json         {'exists' if report['has_state'] else 'NEEDS CREATION'}")
    print(f"  index.md           {'exists' if report['has_index'] else 'NEEDS CREATION'}")
    print(f"  archive.md         {'exists' if report['has_archive'] else 'NEEDS CREATION'}")
    print(f"  events.json        {'exists' if report['has_events'] else 'NEEDS CREATION'}")
    print(f"  ---")
    print(f"  Legacy system?     {'YES — migration needed' if report['is_legacy'] else 'no (already migrated or fresh)'}")
    print()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def create_if_missing(path: Path, content: str, dry_run: bool = False) -> bool:
    if path.exists():
        print(f"  SKIP (exists): {path.name}")
        return False
    if dry_run:
        print(f"  WOULD CREATE: {path.name}")
        return True
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  CREATE: {path.name}")
    return True


def extract_log_date(log_path: Path) -> Optional[str]:
    m = re.match(r"(\d{4}-\d{2}-\d{2})\.md$", log_path.name)
    return m.group(1) if m else None


# ---------------------------------------------------------------------------
# Bootstrap state.json from existing daily logs
# ---------------------------------------------------------------------------

def bootstrap_state(report: dict) -> dict:
    logs = report["daily_logs"] or report["legacy_daily_logs"]
    total = len(logs)
    last_log = logs[-1] if logs else None
    last_date = extract_log_date(last_log) if last_log else None

    if last_date:
        last_ts = f"{last_date}T23:59:00Z"
        last_log_ref = f"memory/{last_log.name}"
    else:
        last_ts = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        last_log_ref = None

    memory_path = report["root"] / "MEMORY.md"
    has_fading = False
    if memory_path.exists():
        text = memory_path.read_text(encoding="utf-8")
        if "## Fading" in text:
            fading_section = text.split("## Fading")[1].split("##")[0].strip()
            has_fading = bool(fading_section and fading_section != "(Nothing here yet)")

    return {
        "_schema_version": "0.2.0",
        "_description": "Machine-readable ephemeral state. Bootstrapped from legacy migration.",
        "last_session": {
            "timestamp": last_ts,
            "duration_minutes": 0,
            "daily_log": last_log_ref,
        },
        "session_counter": {
            "total": total,
            "this_week": min(total, 5),
            "since_last_memory_review": total,
        },
        "active_threads": [],
        "pending_questions": [],
        "flags": {
            "memory_review_due": total >= 5,
            "threads_need_update": False,
            "archive_candidates_exist": has_fading,
        },
        "context_hints": {
            "current_mood_hypothesis": None,
            "conversation_style": None,
            "last_topic_position": f"Migrated from legacy system. {total} session logs found.",
        },
    }


# ---------------------------------------------------------------------------
# Restructure MEMORY.md
# ---------------------------------------------------------------------------

def restructure_memory_md(root: Path, dry_run: bool = False) -> bool:
    path = root / "MEMORY.md"
    if not path.exists():
        return False

    text = path.read_text(encoding="utf-8")

    if "## Active" in text and "## Fading" in text:
        print(f"  SKIP (already structured): MEMORY.md")
        return False

    if dry_run:
        print(f"  WOULD RESTRUCTURE: MEMORY.md (wrap existing content under ## Active)")
        return True

    backup = root / "MEMORY.md.bak"
    shutil.copy2(path, backup)
    print(f"  BACKUP: MEMORY.md -> MEMORY.md.bak")

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    restructured = f"""# Long-Term Memory

> Last reviewed: {today}
> Next review due: after 5 sessions or 7 days, whichever comes first
> Migrated from legacy MEMORY.md -- review and curate entries below.

---

## Active

{text.strip()}

---

## Fading

(Nothing here yet -- entries not referenced in 7+ sessions will move here)

---

## Maintenance Log

| Date       | Action                                              |
|------------|-----------------------------------------------------|
| {today} | Migrated from legacy flat MEMORY.md                  |
"""
    path.write_text(restructured, encoding="utf-8")
    print(f"  RESTRUCTURE: MEMORY.md (existing content wrapped under ## Active)")
    return True


# ---------------------------------------------------------------------------
# Surgical AGENTS.md / AGENT.md patching
# ---------------------------------------------------------------------------

PATCH_MARKER = "<!-- wm-migrated -->"


def _insert_after(text: str, anchor: str, injection: str) -> Optional[str]:
    """Insert *injection* on the line after the first line containing *anchor*."""
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if anchor in line:
            lines.insert(i + 1, injection)
            return "\n".join(lines)
    return None


def _insert_before(text: str, anchor: str, injection: str) -> Optional[str]:
    """Insert *injection* on the line before the first line containing *anchor*."""
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if anchor in line:
            lines.insert(i, injection)
            return "\n".join(lines)
    return None


def patch_agent_md(report: dict, dry_run: bool = False) -> bool:
    """Surgically patch AGENTS.md (or AGENT.md) by injecting into existing sections.

    Five insertion points, matched by anchor text in the original document:

    1. Session Startup   -- add steps for state.json, resumption.md, threads.md
    2. Memory file list  -- add new memory files alongside daily notes + MEMORY.md
    3. Security model    -- extend MEMORY.md rules to cover new personal files
    4. Session End       -- new subsection: what to persist before closing
    5. Heartbeat maint   -- extend curation checklist with threads/events/flags

    Idempotent: if the patch marker is already present, the function is skipped.
    """
    path = report["agent_md_path"]
    if not path:
        print(f"  SKIP (not found): AGENTS.md / AGENT.md")
        return False

    name = path.name
    text = path.read_text(encoding="utf-8")

    if PATCH_MARKER in text:
        print(f"  SKIP (already patched): {name}")
        return False

    if dry_run:
        print(f"  WOULD PATCH: {name} (5 surgical injections into existing sections)")
        return True

    backup = path.with_suffix(".md.bak")
    shutil.copy2(path, backup)
    print(f"  BACKUP: {name} -> {backup.name}")

    injected = 0

    # -- Patch 1: Session Startup ------------------------------------------
    # Anchor: "Don't ask permission. Just do it."
    # Insert new steps before that closing line.
    p1 = _insert_before(text, "Don't ask permission. Just do it.", (
        "5. Read `memory/state.json` — how long you've been away, active threads, flags\n"
        "6. Read `memory/resumption.md` — past-you left a note. Read it.\n"
        "7. **If in MAIN SESSION**: Skim `memory/threads.md` for ongoing topics\n\n"
    ))
    if p1:
        text = p1
        injected += 1

    # -- Patch 2: Memory file list -----------------------------------------
    # Anchor: the line with "**Long-term:** `MEMORY.md`"
    # Insert new files after it.
    p2 = _insert_after(text, "**Long-term:** `MEMORY.md`", (
        "- **Resumption:** `memory/resumption.md` — a handoff note from past-you to present-you\n"
        "- **Threads:** `memory/threads.md` — ongoing topics with enough state to resume cold\n"
        "- **State:** `memory/state.json` — timestamps, counters, flags (machine-readable, safe in any context)\n"
        "- **Events:** `memory/events.json` — structured dated events (purchases, issues, meetings)\n"
        "- **Archive:** `memory/archive.md` — memories demoted from MEMORY.md, still searchable"
    ))
    if p2:
        text = p2
        injected += 1

    # -- Patch 3: Security model -------------------------------------------
    # Anchor: the "Write It Down" header
    # Insert security rules for new files before it.
    p3 = _insert_before(text, "Write It Down", (
        "### 🔒 New Memory Files — Same Security Rules\n"
        "\n"
        "Same deal as MEMORY.md — **personal context stays in main sessions**:\n"
        "\n"
        "- `memory/resumption.md` → **MAIN SESSION ONLY** (personal context about your human)\n"
        "- `memory/threads.md` → **MAIN SESSION ONLY** (personal project details)\n"
        "- `memory/events.json` → **MAIN SESSION ONLY** (personal dated events)\n"
        "- `memory/archive.md` → **MAIN SESSION ONLY** (demoted but still personal)\n"
        "- `memory/state.json` → safe anywhere (just timestamps and counters, nothing personal)\n"
        "- `memory/YYYY-MM-DD.md` → safe anywhere (operational logs, not personal secrets)\n"
        "\n"
    ))
    if p3:
        text = p3
        injected += 1

    # -- Patch 4: Session End ----------------------------------------------
    # Anchor: "## Red Lines"
    # Insert new subsection before it.
    p4 = _insert_before(text, "## Red Lines", (
        "### ✍️ Session End — Close the Loop\n"
        "\n"
        "Before a session wraps up:\n"
        "\n"
        "1. Append to today's `memory/YYYY-MM-DD.md` — what happened, decisions, open questions\n"
        "2. Update `memory/threads.md` — advance thread positions, close resolved questions\n"
        "3. Write `memory/resumption.md` — a note *from you to future-you* (not a summary, a *handoff*)\n"
        "4. Update `memory/state.json` — timestamp, session count, flags\n"
        "5. Log any dated events the human mentioned to `memory/events.json`\n"
        "\n"
        'The resumption note is the big one. Think: "If I woke up tomorrow with zero memory,\n'
        'what would I need to pick up where I left off?" What were we doing, what\'s likely next,\n'
        "what tone to match. Predictions > recaps.\n"
        "\n"
    ))
    if p4:
        text = p4
        injected += 1

    # -- Patch 5: Heartbeat maintenance ------------------------------------
    # Anchor: "Remove outdated info from MEMORY.md"
    # Insert new steps after it.
    p5 = _insert_after(text, "Remove outdated info from MEMORY.md", (
        "5. Check `memory/state.json` — if `memory_review_due` flag is true, do a full curation pass on MEMORY.md\n"
        "6. Prune `memory/threads.md` — close stale threads, archive dead ones\n"
        "7. Review `memory/events.json` — clean up events with missing dates or duplicates"
    ))
    if p5:
        text = p5
        injected += 1

    # -- Stamp the marker --------------------------------------------------
    text = text.rstrip() + "\n\n" + PATCH_MARKER + "\n"

    path.write_text(text, encoding="utf-8")
    print(f"  PATCH: {name} ({injected}/5 injections applied)")
    return True


# ---------------------------------------------------------------------------
# Bootstrap resumption.md from recent daily logs
# ---------------------------------------------------------------------------

def bootstrap_resumption(report: dict) -> str:
    logs = report["daily_logs"] or report["legacy_daily_logs"]
    if not logs:
        return (
            "Just migrated from a legacy memory layout. No prior sessions to resume from.\n"
            "Treat this as a fresh start -- daily logs are available if you need to dig back."
        )

    last_log = logs[-1]
    last_date = extract_log_date(last_log)
    text = last_log.read_text(encoding="utf-8")

    summary_match = re.search(r"## Session Summary\n+(.*?)(?=\n##|\Z)", text, re.DOTALL)
    summary = summary_match.group(1).strip()[:300] if summary_match else ""

    if summary:
        return (
            f"Just migrated from the old memory layout. "
            f"Last session ({last_date}) was about: {summary}\n\n"
            f"Pick up from there. MEMORY.md has been restructured with Active/Fading "
            f"tiers -- worth a curation pass in the next few sessions."
        )
    else:
        return (
            f"Migrated from legacy system. Last session log: {last_date}. "
            f"Read it if you need context. MEMORY.md has been restructured -- "
            f"curate it soon."
        )


# ---------------------------------------------------------------------------
# Main migration
# ---------------------------------------------------------------------------

def migrate(root: str, dry_run: bool = False, skip_agent_patch: bool = False):
    root = Path(root).resolve()
    report = detect_legacy(root)
    print_detection(report)

    if not report["has_memory_dir"] and not report["has_memory_md"]:
        print("No legacy memory system detected. Use scaffold.py for a fresh setup instead.")
        return report

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    changes = 0

    print("--- Migration steps ---\n")

    # 1. Restructure MEMORY.md
    if report["has_memory_md"]:
        if restructure_memory_md(root, dry_run):
            changes += 1

    # 2. Create missing layered files
    memory_dir = root / "memory"

    if create_if_missing(memory_dir / "resumption.md", f"""# Resumption Note

> Written: {today}, legacy migration
> For: my next session self

---

{bootstrap_resumption(report)}
""", dry_run):
        changes += 1

    if create_if_missing(memory_dir / "threads.md", """# Active Threads

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
[Where the conversation currently stands -- enough context to resume cold]

### Key Decisions Made
1. **[Decision]** -- [reasoning]. [ref: memory/YYYY-MM-DD.md#decisions]

### Open Questions
- [ ] [Question]

### Next Likely Steps
1. [Step]

### Related
- [Links to other threads, MEMORY.md sections, etc.]
-->

(No active threads yet. Review recent daily logs and create threads for ongoing topics.)

---

# Closed Threads

(No closed threads yet.)
""", dry_run):
        changes += 1

    state = bootstrap_state(report)
    if create_if_missing(
        memory_dir / "state.json",
        json.dumps(state, indent=2, ensure_ascii=False) + "\n",
        dry_run,
    ):
        changes += 1

    if create_if_missing(memory_dir / "index.md", f"""# Daily Log Index

> Auto-generated. Rebuilt weekly or when daily log count changes by 5+.
> Last rebuilt: {today}
> Total logs: {report['daily_log_count']}

| Date | Threads Touched | Key Topics | Decisions | Mood/Tone |
|------|-----------------|------------|-----------|-----------|
""", dry_run):
        changes += 1

    if create_if_missing(memory_dir / "archive.md", """# Archived Memories

> Entries demoted from MEMORY.md after 20+ sessions without recall.

---

(No archived entries yet.)
""", dry_run):
        changes += 1

    if create_if_missing(memory_dir / "events.json",
        json.dumps({"events": []}, indent=2, ensure_ascii=False) + "\n",
        dry_run,
    ):
        changes += 1

    # 3. Compatibility mirror directory
    if not dry_run:
        (memory_dir / "daily").mkdir(parents=True, exist_ok=True)

    # 4. Patch agent config
    if not skip_agent_patch and report["has_agent_md"]:
        if patch_agent_md(report, dry_run):
            changes += 1

    # 5. Rebuild index if we have logs
    if not dry_run and report["daily_log_count"] > 0:
        try:
            from rebuild_index import rebuild_index
            print()
            rebuild_index(str(root))
        except ImportError:
            print("  NOTE: rebuild_index.py not on path -- run it manually to index existing logs.")

    # Summary
    agent_name = report["agent_md_name"] or "AGENT.md"
    print(f"\n{'='*60}")
    if dry_run:
        print(f"  DRY RUN complete. {changes} file(s) would be created/modified.")
    else:
        print(f"  Migration complete. {changes} file(s) created/modified.")
    print()
    print("  Backups created:")
    for bak in sorted(root.glob("*.bak")):
        print(f"    {bak.name}")
    print()
    print("  Next steps:")
    print(f"    1. Review MEMORY.md -- curate entries under ## Active")
    print(f"    2. Review {agent_name} -- verify the injected sections")
    print(f"    3. Create threads for ongoing topics from recent daily logs")
    print(f"    4. Run a session to verify the loader works:")
    print(f"       python loader.py {root} \"test message\"")
    print(f"{'='*60}\n")

    return report


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Migrate a legacy workspace to the layered working-memory system"
    )
    parser.add_argument("root", help="Workspace root directory (e.g., /workspace)")
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show what would change without writing anything"
    )
    parser.add_argument(
        "--skip-agent-patch", action="store_true",
        help="Do not modify AGENTS.md / AGENT.md"
    )
    args = parser.parse_args()
    migrate(args.root, dry_run=args.dry_run, skip_agent_patch=args.skip_agent_patch)
