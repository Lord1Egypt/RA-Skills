#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from datetime import date, datetime
from pathlib import Path

from capture_memory import AXIS_BY_KIND, ensure_daily_file, next_entry_id, sanitize
from memory_os_common import sidecar_dir

PLAN_FILENAME = "migration-plan.json"
CANDIDATE_RE = re.compile(r"^- (?P<source>[^:]+ :: )(?P<statement>.+)$")
KIND_ALIAS = {"preference": "value"}


def latest_migration_review(workspace: Path) -> Path | None:
    review_dir = sidecar_dir(workspace) / "reviews"
    reviews = sorted(review_dir.glob("migration-*.md"))
    return reviews[-1] if reviews else None


def plan_path(workspace: Path) -> Path:
    return sidecar_dir(workspace) / PLAN_FILENAME


def extract_candidates(review_path: Path) -> list[dict]:
    candidates: list[dict] = []
    for raw in review_path.read_text(encoding="utf-8").splitlines():
        match = CANDIDATE_RE.match(raw.strip())
        if not match:
            continue
        source = match.group("source")[:-4]
        statement = match.group("statement").strip()
        statement = statement.lstrip("- ").strip()
        candidates.append(
            {
                "source": source,
                "statement": statement,
                "enabled": False,
                "kind": "",
                "axis": "",
                "topic": "",
                "status": "candidate",
                "confidence": "medium",
                "imported_at": None,
                "entry_id": None,
            }
        )
    return candidates


def prepare_plan(workspace: Path, review_path: Path, force: bool) -> Path:
    target = plan_path(workspace)
    if target.exists() and not force:
        raise SystemExit(f"Plan already exists: {target}. Use --force to overwrite.")

    plan = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "review_path": str(review_path),
        "items": extract_candidates(review_path),
    }
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(plan, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    return target


def validate_item(item: dict, index: int) -> None:
    if not item.get("enabled"):
        return
    kind = KIND_ALIAS.get(item.get("kind", ""), item.get("kind", ""))
    axis = item.get("axis", "")
    if kind not in AXIS_BY_KIND:
        raise SystemExit(f"Plan item {index} has invalid kind: {kind!r}")
    if axis not in AXIS_BY_KIND[kind]:
        raise SystemExit(f"Plan item {index} has invalid axis {axis!r} for kind {kind!r}")
    if not item.get("topic", "").strip():
        raise SystemExit(f"Plan item {index} is enabled but missing topic")
    if not item.get("statement", "").strip():
        raise SystemExit(f"Plan item {index} is enabled but missing statement")


def append_promotions(workspace: Path, plan: dict, dry_run: bool) -> tuple[int, Path]:
    today = date.today().isoformat()
    daily_path = workspace / "memory" / f"{today}.md"
    ensure_daily_file(daily_path, today)
    promoted = 0

    for index, item in enumerate(plan.get("items", []), start=1):
        validate_item(item, index)
        if not item.get("enabled") or item.get("imported_at"):
            continue

        kind = KIND_ALIAS.get(item["kind"], item["kind"])
        entry_id = next_entry_id(daily_path, today)
        topic = sanitize(item["topic"].strip().lower())
        statement = sanitize(item["statement"].strip())
        line = (
            f"- [{today}|{entry_id}|{kind}|{item['axis']}|"
            f"{item.get('status', 'candidate')}|{item.get('confidence', 'medium')}|{topic}] {statement}"
        )
        if not dry_run:
            with daily_path.open("a", encoding="utf-8") as handle:
                if daily_path.read_text(encoding="utf-8").rstrip().endswith("## L1 Entries"):
                    handle.write("\n")
                handle.write(line + "\n")
            item["kind"] = kind
            item["imported_at"] = datetime.now().isoformat(timespec="seconds")
            item["entry_id"] = entry_id
        promoted += 1
    return promoted, daily_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare or apply a legacy-memory promotion plan.")
    parser.add_argument("--workspace", default=".", help="Workspace path (default: current directory)")
    parser.add_argument("--prepare", action="store_true", help="Generate a migration plan JSON from the latest migration review")
    parser.add_argument("--apply", action="store_true", help="Apply enabled items from the migration plan into today's L1 file")
    parser.add_argument("--review", help="Optional path to a migration review file")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing plan when used with --prepare")
    parser.add_argument("--dry-run", action="store_true", help="Validate and count promotions without writing")
    args = parser.parse_args()

    if args.prepare == args.apply:
        raise SystemExit("Use exactly one of --prepare or --apply.")

    workspace = Path(args.workspace).expanduser().resolve()
    if args.prepare:
        review_path = Path(args.review).expanduser().resolve() if args.review else latest_migration_review(workspace)
        if review_path is None or not review_path.exists():
            raise SystemExit("No migration review found.")
        target = prepare_plan(workspace, review_path, args.force)
        print(f"Prepared migration plan: {target}")
        return 0

    target = plan_path(workspace)
    if not target.exists():
        raise SystemExit(f"Migration plan not found: {target}. Run with --prepare first.")
    plan = json.loads(target.read_text(encoding="utf-8"))
    promoted, daily_path = append_promotions(workspace, plan, args.dry_run)
    if not args.dry_run:
        target.write_text(json.dumps(plan, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    print(f"Promotions {'validated' if args.dry_run else 'written'}: {promoted}")
    print(f"Daily file: {daily_path}")
    print(f"Plan: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
