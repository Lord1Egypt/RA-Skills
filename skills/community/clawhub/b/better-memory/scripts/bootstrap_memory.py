#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import date, datetime, timedelta
from pathlib import Path
import re
from textwrap import dedent

from memory_os_common import (
    DEFAULT_SETTINGS,
    MANAGED_AGENT_BLOCK_END,
    MANAGED_AGENT_BLOCK_START,
    MANAGED_MEMORY_BLOCK_END,
    MANAGED_MEMORY_BLOCK_START,
    save_settings,
    save_state,
    sidecar_dir,
    upsert_marked_block,
)

WEEKDAYS = {"MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"}


def _is_valid_time(value: str) -> bool:
    match = re.fullmatch(r"(\d{2}):(\d{2})", value.strip())
    if not match:
        return False
    hour = int(match.group(1))
    minute = int(match.group(2))
    return 0 <= hour <= 23 and 0 <= minute <= 59


def _validate_settings(settings: dict) -> None:
    if not _is_valid_time(settings["daily_review_time"]):
        raise SystemExit("Invalid --daily-review-time. Expected HH:MM in 24h format.")
    if settings["weekly_rollup_day"] not in WEEKDAYS:
        raise SystemExit(f"Invalid --weekly-rollup-day. Use one of: {', '.join(sorted(WEEKDAYS))}")
    if not _is_valid_time(settings["weekly_rollup_time"]):
        raise SystemExit("Invalid --weekly-rollup-time. Expected HH:MM in 24h format.")
    if not 1 <= int(settings["monthly_review_day"]) <= 31:
        raise SystemExit("Invalid --monthly-review-day. Expected 1-31.")
    if not _is_valid_time(settings["monthly_review_time"]):
        raise SystemExit("Invalid --monthly-review-time. Expected HH:MM in 24h format.")
    if int(settings["l1_entry_threshold"]) <= 0:
        raise SystemExit("Invalid --l1-entry-threshold. Must be > 0.")


def render_agent_block(settings: dict) -> str:
    return dedent(
        f"""
        {MANAGED_AGENT_BLOCK_START}
        ## Better Memory V2

        This block is additive. Keep all workspace rules outside this block unchanged.

        Native memory source of truth:
        - `memory/YYYY-MM-DD.md` for raw daily memory (L1)
        - `MEMORY.md` for high-level weekly rollup memory (L3)

        Sidecar layer:
        - `.openclaw-memory-os/l2/*.md` for daily structured summaries (L2)
        - `.openclaw-memory-os/reviews/*.md` for monthly review artifacts
        - Sidecar files stay outside `memory/` to keep native `memory_search` clean.

        Typed memory taxonomy:
        - `experience`: `think`, `say`, `do`
        - `value`: `good`, `bad`
        - `standard`: `right`, `wrong`

        Capture command:
        `python3 skills/better-memory/scripts/capture_memory.py --workspace . --kind <experience|value|standard> --axis <axis> --topic "<topic>" --statement "<statement>"`

        Scheduled pipeline commands:
        - Daily L1->L2:
          `python3 skills/better-memory/scripts/run_daily_review.py --workspace .`
        - Weekly L2->L3:
          `python3 skills/better-memory/scripts/run_weekly_rollup.py --workspace .`
        - Monthly review report:
          `python3 skills/better-memory/scripts/run_monthly_review.py --workspace .`
        - Apply confirmed monthly cleanup actions:
          `python3 skills/better-memory/scripts/apply_monthly_cleanup.py --workspace . --rerollup`

        Settings:
        - `daily_review_time={settings["daily_review_time"]}`
        - `weekly_rollup_day={settings["weekly_rollup_day"]}`
        - `weekly_rollup_time={settings["weekly_rollup_time"]}`
        - `monthly_review_day={settings["monthly_review_day"]}`
        - `monthly_review_time={settings["monthly_review_time"]}`
        - `l1_entry_threshold={settings["l1_entry_threshold"]}`
        - `stale_days={settings["stale_days"]}`
        - `max_l3_per_kind={settings["max_l3_per_kind"]}`
        - `min_evidence_for_l3={settings["min_evidence_for_l3"]}`
        - `migration_days={settings["migration_days"]}`
        - `daily_entries_soft_limit={settings["daily_entries_soft_limit"]}`

        Install migration policy:
        - Preserve existing `AGENTS.md`, `MEMORY.md`, and daily notes.
        - Generate migration review and editable migration plan.
        - Do not auto-import legacy lines unless explicitly enabled in plan.
        {MANAGED_AGENT_BLOCK_END}
        """
    ).strip()


def render_memory_block() -> str:
    return dedent(
        f"""
        {MANAGED_MEMORY_BLOCK_START}
        ## L3 Experience
        - (empty)

        ## L3 Values
        - (empty)

        ## L3 Standards
        - (empty)

        ## Contradictions To Resolve
        - (none)

        ## Stale Candidates
        - (none)

        ## Last Distillation
        - (not run yet)
        {MANAGED_MEMORY_BLOCK_END}
        """
    ).strip()


def ensure_daily_file(path: Path, iso_date: str) -> bool:
    template = dedent(
        f"""
        # {iso_date} Memory Log (L1)

        ## Format
        Use one line per memory item:
        - [YYYY-MM-DD|M-YYYYMMDD-###|kind|axis|status|confidence|topic] statement

        ## L1 Entries
        """
    ).strip() + "\n"

    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(template, encoding="utf-8")
        return True

    original = path.read_text(encoding="utf-8")
    if "## L1 Entries" in original:
        return False

    path.write_text(original.rstrip() + "\n\n## L1 Entries\n", encoding="utf-8")
    return True


def ensure_memory_md(memory_path: Path) -> bool:
    if memory_path.exists():
        original = memory_path.read_text(encoding="utf-8")
    else:
        original = "# MEMORY.md\n\n"

    original = original.replace("## L3 Preferences", "## L3 Values")
    updated = upsert_marked_block(
        original,
        MANAGED_MEMORY_BLOCK_START,
        MANAGED_MEMORY_BLOCK_END,
        render_memory_block(),
    )
    if updated == original:
        return False
    memory_path.write_text(updated, encoding="utf-8")
    return True


def ensure_agents_md(agents_path: Path, settings: dict) -> bool:
    original = agents_path.read_text(encoding="utf-8") if agents_path.exists() else "# AGENTS.md\n\n"
    updated = upsert_marked_block(
        original,
        MANAGED_AGENT_BLOCK_START,
        MANAGED_AGENT_BLOCK_END,
        render_agent_block(settings),
    )
    if updated == original:
        return False
    agents_path.write_text(updated, encoding="utf-8")
    return True


def migrate_preference_to_value(workspace: Path) -> list[str]:
    changed_files: list[str] = []

    for path in sorted((workspace / "memory").glob("20??-??-??.md")):
        original = path.read_text(encoding="utf-8")
        updated = re.sub(r"\|preference\|", "|value|", original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed_files.append(str(path))

    memory_md = workspace / "MEMORY.md"
    if memory_md.exists():
        original = memory_md.read_text(encoding="utf-8")
        updated = original.replace("L3 Preferences", "L3 Values")
        if updated != original:
            memory_md.write_text(updated, encoding="utf-8")
            changed_files.append(str(memory_md))

    l2_dir = sidecar_dir(workspace) / "l2"
    pref_path = l2_dir / "preference.md"
    value_path = l2_dir / "value.md"
    if pref_path.exists():
        if value_path.exists():
            merged = value_path.read_text(encoding="utf-8").rstrip() + "\n\n" + pref_path.read_text(encoding="utf-8")
            value_path.write_text(merged.rstrip() + "\n", encoding="utf-8")
            pref_path.unlink()
            changed_files.extend([str(value_path), str(pref_path)])
        else:
            pref_path.rename(value_path)
            changed_files.extend([str(pref_path), str(value_path)])

    return changed_files


def collect_legacy_lines(workspace: Path, migration_days: int) -> list[str]:
    lines: list[str] = []
    memory_path = workspace / "MEMORY.md"
    if memory_path.exists():
        in_managed_block = False
        for raw in memory_path.read_text(encoding="utf-8").splitlines():
            stripped = raw.strip()
            if stripped == MANAGED_MEMORY_BLOCK_START:
                in_managed_block = True
                continue
            if stripped == MANAGED_MEMORY_BLOCK_END:
                in_managed_block = False
                continue
            if in_managed_block:
                continue
            if not stripped or stripped.startswith("<!-- OPENCLAW_MEMORY_OS_"):
                continue
            if stripped.startswith("#"):
                continue
            if len(stripped) >= 12:
                lines.append(f"MEMORY.md :: {stripped}")

    memory_dir = workspace / "memory"
    if not memory_dir.exists():
        return lines

    cutoff = date.today() - timedelta(days=migration_days)
    for path in sorted(memory_dir.glob("20??-??-??.md")):
        try:
            log_date = date.fromisoformat(path.stem)
        except ValueError:
            continue
        if log_date < cutoff:
            continue
        for raw in path.read_text(encoding="utf-8").splitlines():
            stripped = raw.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if stripped.startswith("- [") or stripped.startswith("Use one line per memory item"):
                continue
            if len(stripped) >= 12:
                lines.append(f"{path.name} :: {stripped}")
    return lines


def write_migration_review(workspace: Path, migration_days: int) -> Path:
    review_dir = sidecar_dir(workspace) / "reviews"
    review_dir.mkdir(parents=True, exist_ok=True)
    path = review_dir / f"migration-{date.today().isoformat()}.md"
    legacy_lines = collect_legacy_lines(workspace, migration_days)

    body = [
        f"# Legacy Memory Migration Review {date.today().isoformat()}",
        "",
        "This file is outside native memory on purpose.",
        "Promote selected items into typed L1 entries instead of copying everything blindly.",
        "",
        f"- scanned_window_days: {migration_days}",
        f"- legacy_candidates: {len(legacy_lines)}",
        "",
        "## Candidates",
    ]
    if legacy_lines:
        for line in legacy_lines:
            body.append(f"- {line}")
    else:
        body.append("- (none)")
    body.append("")

    path.write_text("\n".join(body), encoding="utf-8")
    return path


def bootstrap(workspace: Path, settings: dict) -> list[str]:
    _validate_settings(settings)
    changed: list[str] = []
    sidecar = sidecar_dir(workspace)
    sidecar.mkdir(parents=True, exist_ok=True)
    (sidecar / "l2").mkdir(parents=True, exist_ok=True)
    (sidecar / "reviews").mkdir(parents=True, exist_ok=True)

    review_path = write_migration_review(workspace, settings["migration_days"])
    changed.append(str(review_path))

    config = save_settings(workspace, settings)
    changed.append(str(config))
    state = save_state(workspace, {})
    changed.append(str(state))

    memory_path = workspace / "MEMORY.md"
    if ensure_memory_md(memory_path):
        changed.append(str(memory_path))

    today = date.today().isoformat()
    today_path = workspace / "memory" / f"{today}.md"
    if ensure_daily_file(today_path, today):
        changed.append(str(today_path))

    agents_path = workspace / "AGENTS.md"
    if ensure_agents_md(agents_path, settings):
        changed.append(str(agents_path))

    migration_changes = migrate_preference_to_value(workspace)
    changed.extend(migration_changes)

    marker_path = sidecar / "installed.txt"
    marker_path.write_text(
        f"installed_at={datetime.now().isoformat(timespec='seconds')}\n",
        encoding="utf-8",
    )
    changed.append(str(marker_path))
    return sorted(set(changed))


def main() -> int:
    parser = argparse.ArgumentParser(description="Install or update Better Memory additively.")
    parser.add_argument("--workspace", default=".", help="Workspace path (default: current directory)")
    parser.add_argument("--stale-days", type=int, default=DEFAULT_SETTINGS["stale_days"])
    parser.add_argument("--max-l3-per-kind", type=int, default=DEFAULT_SETTINGS["max_l3_per_kind"])
    parser.add_argument("--min-evidence-for-l3", type=int, default=DEFAULT_SETTINGS["min_evidence_for_l3"])
    parser.add_argument("--migration-days", type=int, default=DEFAULT_SETTINGS["migration_days"])
    parser.add_argument("--daily-entries-soft-limit", type=int, default=DEFAULT_SETTINGS["daily_entries_soft_limit"])
    parser.add_argument("--daily-review-time", default=DEFAULT_SETTINGS["daily_review_time"])
    parser.add_argument("--weekly-rollup-day", default=DEFAULT_SETTINGS["weekly_rollup_day"])
    parser.add_argument("--weekly-rollup-time", default=DEFAULT_SETTINGS["weekly_rollup_time"])
    parser.add_argument("--monthly-review-day", type=int, default=DEFAULT_SETTINGS["monthly_review_day"])
    parser.add_argument("--monthly-review-time", default=DEFAULT_SETTINGS["monthly_review_time"])
    parser.add_argument("--l1-entry-threshold", type=int, default=DEFAULT_SETTINGS["l1_entry_threshold"])
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    settings = {
        "stale_days": args.stale_days,
        "max_l3_per_kind": args.max_l3_per_kind,
        "min_evidence_for_l3": args.min_evidence_for_l3,
        "migration_days": args.migration_days,
        "daily_entries_soft_limit": args.daily_entries_soft_limit,
        "daily_review_time": args.daily_review_time.strip(),
        "weekly_rollup_day": args.weekly_rollup_day.strip().upper(),
        "weekly_rollup_time": args.weekly_rollup_time.strip(),
        "monthly_review_day": args.monthly_review_day,
        "monthly_review_time": args.monthly_review_time.strip(),
        "l1_entry_threshold": args.l1_entry_threshold,
    }

    changed = bootstrap(workspace, settings)
    print(f"Workspace: {workspace}")
    print("Installed/updated additively.")
    for path in changed:
        print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
