#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path

from refine_memory import parse_entries, run_daily_review, run_weekly_rollup, write_modified_files


def latest_plan_path(workspace: Path) -> Path | None:
    reviews_dir = workspace / ".openclaw-memory-os" / "reviews"
    if not reviews_dir.exists():
        return None
    plans = sorted(reviews_dir.glob("monthly-*-plan.json"))
    return plans[-1] if plans else None


def apply_actions(workspace: Path, plan: dict, dry_run: bool) -> tuple[int, int, int, list[dict], list[str]]:
    entries, file_lines = parse_entries(workspace)
    entry_by_id = {entry.entry_id: entry for entry in entries}
    enabled_actions = [action for action in plan.get("actions", []) if action.get("enabled")]
    enabled_action_ids = [str(action.get("id", "(no-id)")) for action in enabled_actions]
    changes: list[dict] = []

    touched = 0
    skipped = 0
    applied = 0
    for action in enabled_actions:
        action_id = str(action.get("id", "(no-id)"))
        action_type = action.get("type")
        target_ids = action.get("target_entry_ids", [])
        local_changes = 0

        for entry_id in target_ids:
            entry = entry_by_id.get(entry_id)
            if entry is None:
                skipped += 1
                continue

            desired_status = None
            if action_type == "mark_conflicted":
                if entry.status in {"active", "candidate"}:
                    desired_status = "conflicted"
            elif action_type == "mark_superseded":
                if entry.status in {"active", "candidate"}:
                    desired_status = "superseded"
            elif action_type == "mark_stale":
                if entry.status == "active":
                    desired_status = "stale"
            else:
                skipped += 1
                continue

            if desired_status is None or entry.status == desired_status:
                skipped += 1
                continue

            old_status = entry.status
            entry.status = desired_status
            file_lines[entry.path][entry.line_index] = entry.to_line()
            changes.append(
                {
                    "action_id": action_id,
                    "action_type": action_type,
                    "entry_id": entry.entry_id,
                    "kind": entry.kind,
                    "topic": entry.topic,
                    "old_status": old_status,
                    "new_status": desired_status,
                    "file": str(entry.path),
                    "statement": entry.statement,
                }
            )
            local_changes += 1
            touched += 1

        if local_changes > 0:
            applied += 1

    if touched > 0 and not dry_run:
        write_modified_files(file_lines)

    return touched, applied, skipped, changes, enabled_action_ids


def write_change_summary(
    workspace: Path,
    *,
    plan_path: Path,
    dry_run: bool,
    applied: int,
    touched: int,
    skipped: int,
    enabled_action_ids: list[str],
    changes: list[dict],
    rerollup_msg: str,
    summary_limit: int,
) -> Path:
    reviews_dir = workspace / ".openclaw-memory-os" / "reviews"
    reviews_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    summary_path = reviews_dir / f"apply-summary-{ts}.md"

    action_counts: dict[str, int] = {}
    for item in changes:
        action_id = item["action_id"]
        action_counts[action_id] = action_counts.get(action_id, 0) + 1

    lines = [
        f"# Monthly Cleanup Apply Summary {datetime.now().isoformat(timespec='seconds')}",
        "",
        f"- workspace: {workspace}",
        f"- plan: {plan_path}",
        f"- dry_run: {dry_run}",
        f"- enabled_actions: {len(enabled_action_ids)}",
        f"- actions_applied: {applied}",
        f"- entries_updated: {touched}",
        f"- skipped_targets: {skipped}",
        f"- rerollup: {rerollup_msg}",
        "",
        "## Enabled Actions",
    ]
    if enabled_action_ids:
        for action_id in enabled_action_ids:
            lines.append(f"- {action_id}")
    else:
        lines.append("- (none)")

    lines.extend(["", "## Action Impact"])
    if action_counts:
        for action_id in sorted(action_counts):
            lines.append(f"- {action_id}: {action_counts[action_id]} entries")
    else:
        lines.append("- (none)")

    lines.extend(["", f"## Entry Changes (showing up to {summary_limit})"])
    if changes:
        for item in changes[:summary_limit]:
            lines.append(
                f"- {item['entry_id']} | {item['kind']}/{item['topic']} | "
                f"{item['old_status']} -> {item['new_status']} | {item['action_id']}"
            )
        extra = len(changes) - min(len(changes), summary_limit)
        if extra > 0:
            lines.append(f"- ... {extra} more changes omitted")
    else:
        lines.append("- (none)")

    lines.append("")
    summary_path.write_text("\n".join(lines), encoding="utf-8")
    return summary_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply enabled actions from monthly cleanup plan.")
    parser.add_argument("--workspace", default=".", help="Workspace path (default: current directory)")
    parser.add_argument("--plan", help="Path to monthly plan JSON (default: latest monthly-*-plan.json)")
    parser.add_argument("--dry-run", action="store_true", help="Do not write files; only report pending changes")
    parser.add_argument("--rerollup", action="store_true", help="Run weekly rollup after successful apply")
    parser.add_argument("--summary-limit", type=int, default=20, help="Maximum number of entry changes in summary detail")
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    plan_path = Path(args.plan).expanduser().resolve() if args.plan else latest_plan_path(workspace)
    if plan_path is None or not plan_path.exists():
        raise SystemExit("Monthly cleanup plan not found. Run run_monthly_review.py first.")

    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    touched, applied, skipped, changes, enabled_action_ids = apply_actions(workspace, plan, dry_run=args.dry_run)

    if args.rerollup and not args.dry_run and touched > 0:
        run_daily_review(workspace, threshold_only=False, apply_stale=False)
        rollup = run_weekly_rollup(workspace)
        rerollup_msg = f"Daily review + weekly rollup updated: {rollup['memory_file']}"
    else:
        rerollup_msg = "Weekly rollup not run."

    summary_path = write_change_summary(
        workspace,
        plan_path=plan_path,
        dry_run=args.dry_run,
        applied=applied,
        touched=touched,
        skipped=skipped,
        enabled_action_ids=enabled_action_ids,
        changes=changes,
        rerollup_msg=rerollup_msg,
        summary_limit=max(1, args.summary_limit),
    )

    print(f"Workspace: {workspace}")
    print(f"Plan: {plan_path}")
    print(f"Dry run: {args.dry_run}")
    print(f"Enabled actions applied: {applied}")
    print(f"Entries updated: {touched}")
    print(f"Skipped targets: {skipped}")
    print(rerollup_msg)
    print(f"Summary file: {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
