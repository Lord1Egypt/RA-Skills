#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
BACKUPS = ROOT / "backups"
PIPELINE_BACKUPS = BACKUPS / "pipeline"
TRASH_CMD = "/usr/bin/trash"


def now_iso() -> str:
    return datetime.now(UTC).isoformat()


def mb(n: int) -> float:
    return round(n / (1024 * 1024), 2)


def dir_size(path: Path) -> int:
    total = 0
    for p in path.rglob("*"):
        if p.is_file():
            try:
                total += p.stat().st_size
            except OSError:
                pass
    return total


def list_snapshots() -> list[Path]:
    return sorted([p for p in BACKUPS.rglob("*") if p.is_dir() and (p / "fitbit_metrics.sqlite3").exists()])


def plan_keep(snapshot_paths: list[Path], keep_recent_days: int) -> tuple[set[Path], list[dict[str, Any]]]:
    keep: set[Path] = set()
    info: list[dict[str, Any]] = []
    by_day: dict[str, list[Path]] = defaultdict(list)

    for snap in snapshot_paths:
        kind = snap.parent.name
        stamp = snap.name
        day = stamp[:8]
        size = dir_size(snap)
        info.append({"path": snap, "kind": kind, "stamp": stamp, "day": day, "size": size})
        by_day[day].append(snap)
        if kind != "pipeline":
            keep.add(snap)

    pipeline_days = sorted({i["day"] for i in info if i["kind"] == "pipeline"})
    recent_days = set(pipeline_days[-keep_recent_days:]) if keep_recent_days > 0 else set()

    for i in info:
        if i["kind"] == "pipeline" and i["day"] in recent_days:
            keep.add(i["path"])

    for day, snaps in by_day.items():
        pipeline_snaps = sorted([s for s in snaps if s.parent.name == "pipeline"], key=lambda p: p.name)
        if pipeline_snaps:
            keep.add(pipeline_snaps[-1])

    plan = []
    for i in sorted(info, key=lambda x: str(x["path"])):
        plan.append(
            {
                "snapshot": str(i["path"].relative_to(ROOT)),
                "kind": i["kind"],
                "day": i["day"],
                "size_mb": mb(i["size"]),
                "action": "keep" if i["path"] in keep else "trash",
            }
        )

    return keep, plan


def apply_trash(paths: list[Path]) -> None:
    if not paths:
        return
    subprocess.run([TRASH_CMD, *[str(p) for p in paths]], check=True)


def prune_pipeline_snapshots(keep_recent_days: int = 1, apply: bool = False) -> dict[str, Any]:
    snapshots = sorted([p for p in PIPELINE_BACKUPS.iterdir() if p.is_dir() and (p / "fitbit_metrics.sqlite3").exists()]) if PIPELINE_BACKUPS.exists() else []
    by_day: dict[str, list[Path]] = defaultdict(list)
    for snap in snapshots:
        by_day[snap.name[:8]].append(snap)

    pipeline_days = sorted(by_day.keys())
    recent_days = set(pipeline_days[-keep_recent_days:]) if keep_recent_days > 0 else set()

    keep: set[Path] = set()
    for day, snaps in by_day.items():
        ordered = sorted(snaps, key=lambda p: p.name)
        keep.add(ordered[-1])
        if day in recent_days:
            keep.update(ordered)

    trash_paths = [p for p in snapshots if p not in keep]
    reclaim_bytes = sum(dir_size(p) for p in trash_paths)

    if apply:
        apply_trash(trash_paths)

    return {
        "ok": True,
        "operation": "fitbit-pipeline-backup-prune",
        "applied": apply,
        "keep_recent_days": keep_recent_days,
        "total_snapshots": len(snapshots),
        "keep_count": len(keep),
        "trash_count": len(trash_paths),
        "reclaim_mb": mb(reclaim_bytes),
        "kept_snapshots": [str(p.relative_to(ROOT)) for p in sorted(keep)],
        "trashed_snapshots": [str(p.relative_to(ROOT)) for p in sorted(trash_paths)],
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--keep-recent-days", type=int, default=1, help="Keep all pipeline snapshots from the most recent N distinct pipeline days")
    ap.add_argument("--apply", action="store_true", help="Move prune candidates to Trash")
    args = ap.parse_args()

    snapshots = list_snapshots()
    keep, plan = plan_keep(snapshots, args.keep_recent_days)
    trash_paths = [p for p in snapshots if p not in keep]
    reclaim_bytes = sum(dir_size(p) for p in trash_paths)

    if args.apply:
        apply_trash(trash_paths)

    pipeline = prune_pipeline_snapshots(keep_recent_days=args.keep_recent_days, apply=False)

    out = {
        "generated_at": now_iso(),
        "operation": "fitbit-backup-prune",
        "applied": args.apply,
        "keep_recent_days": args.keep_recent_days,
        "total_snapshots": len(snapshots),
        "keep_count": len(keep),
        "trash_count": len(trash_paths),
        "reclaim_mb": mb(reclaim_bytes),
        "pipeline_policy_preview": pipeline,
        "plan": plan,
    }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
