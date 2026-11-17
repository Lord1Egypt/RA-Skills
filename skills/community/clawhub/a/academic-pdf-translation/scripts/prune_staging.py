from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from _common import SkillError, internal_job_path, load_json


MANAGED_PREFIXES = (
    "candidate-",
    "preflight-",
    "render-readiness-",
    "repair-plan-",
)


def plan_staging_prune(
    job_dir: Path,
    *,
    keep_per_kind: int = 2,
) -> dict[str, Any]:
    if keep_per_kind < 1:
        raise SkillError("keep_per_kind 必须至少为 1")
    job_dir = job_dir.resolve()
    job = load_json(job_dir / "job.json")
    staging = job_dir / "staging"
    if not staging.is_dir():
        return {"staging": str(staging), "keep": [], "remove": []}

    protected: set[Path] = set()
    files = job.get("files", {})
    for key in ("preflight_ledger", "render_readiness"):
        relative = files.get(key)
        if isinstance(relative, str) and relative:
            protected.add(internal_job_path(job_dir, relative))

    keep = set(protected)
    remove: set[Path] = set()
    for prefix in MANAGED_PREFIXES:
        candidates = sorted(
            (
                path
                for path in staging.iterdir()
                if path.is_file() and path.name.startswith(prefix)
            ),
            key=lambda path: (path.stat().st_mtime_ns, path.name),
            reverse=True,
        )
        keep.update(candidates[:keep_per_kind])
        remove.update(candidates[keep_per_kind:])
    remove.difference_update(keep)
    return {
        "staging": str(staging),
        "keep": [str(path) for path in sorted(keep)],
        "remove": [str(path) for path in sorted(remove)],
    }


def prune_staging(
    job_dir: Path,
    *,
    keep_per_kind: int = 2,
    apply: bool = False,
) -> dict[str, Any]:
    plan = plan_staging_prune(
        job_dir,
        keep_per_kind=keep_per_kind,
    )
    if apply:
        for value in plan["remove"]:
            Path(value).unlink()
    plan["applied"] = apply
    plan["removed_count"] = len(plan["remove"]) if apply else 0
    return plan


def main() -> int:
    parser = argparse.ArgumentParser(
        description="清理不再需要的候选、预检和返修 staging 产物"
    )
    parser.add_argument("job_dir", type=Path)
    parser.add_argument("--keep-per-kind", type=int, default=2)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="实际删除；默认只输出清理计划",
    )
    args = parser.parse_args()
    try:
        report = prune_staging(
            args.job_dir,
            keep_per_kind=args.keep_per_kind,
            apply=args.apply,
        )
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0
    except SkillError as exc:
        print(f"错误: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
