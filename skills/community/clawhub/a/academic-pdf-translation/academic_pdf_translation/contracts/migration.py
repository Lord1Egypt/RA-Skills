"""旧作业迁移。

规矩只有三条：

1. 只加字段，不删旧字段。旧检查还在用它们。
2. 迁移前把旧 ``job.json`` 原样存一份快照，随时可以回头看。
3. 每次迁移都记 ``migration_version``，没迁过的作业不会被当成迁过的。
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from academic_pdf_translation.contracts.enums import (
    QUALITY_MODE_TO_REVIEW_MODE,
    QualityMode,
)

#: 当前迁移版本。加新迁移步骤时 +1。
MIGRATION_VERSION = 2

SNAPSHOT_DIR_NAME = "migrations"


def _snapshot(job_dir: Path, job_path: Path, version: int) -> Path:
    target = job_dir / SNAPSHOT_DIR_NAME / f"job.before-v{version}.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        shutil.copy2(job_path, target)
    return target


def needs_migration(job: dict[str, Any]) -> bool:
    return int(job.get("migration_version") or 0) < MIGRATION_VERSION


def derive_quality_mode(job: dict[str, Any]) -> QualityMode:
    """从作业数据推出质量档位。

    ``quality_mode`` 优先；没有就看旧的 ``review.mode``：
    none → fast，independent → balanced，precise → precise。
    """

    explicit = job.get("quality_mode")
    if explicit:
        return QualityMode.parse(explicit)
    legacy = job.get("review", {}).get("mode")
    if legacy:
        return QualityMode.parse(legacy)
    raise ValueError("作业缺少 quality_mode 和 review.mode，无法判定质量档位")


def migrate_job(
    job: dict[str, Any],
    *,
    job_dir: Path | None = None,
) -> tuple[dict[str, Any], list[str]]:
    """把作业数据迁到当前版本，返回 (作业, 迁移记录)。

    不写盘。写盘由 :func:`migrate_job_file` 负责。
    """

    changes: list[str] = []
    if not needs_migration(job):
        return job, changes

    if "quality_mode" not in job:
        mode = derive_quality_mode(job)
        job["quality_mode"] = mode.value
        changes.append(
            f"从 review.mode={job.get('review', {}).get('mode')!r} "
            f"推出 quality_mode={mode.value!r}"
        )
    else:
        mode = QualityMode.parse(job["quality_mode"])

    # review.mode 从此由 quality_mode 派生。旧字段保留，值对齐。
    review = job.setdefault("review", {})
    expected = QUALITY_MODE_TO_REVIEW_MODE[mode]
    if review.get("mode") != expected:
        changes.append(
            f"review.mode 由 quality_mode 派生: "
            f"{review.get('mode')!r} → {expected!r}"
        )
        review["mode"] = expected
    review["derived_from_quality_mode"] = True

    job["migration_version"] = MIGRATION_VERSION
    changes.append(f"migration_version → {MIGRATION_VERSION}")
    return job, changes


def migrate_job_file(job_dir: Path) -> dict[str, Any]:
    """迁移磁盘上的 job.json，迁移前先存快照。"""

    job_dir = Path(job_dir).resolve()
    job_path = job_dir / "job.json"
    job = json.loads(job_path.read_text(encoding="utf-8"))
    if not needs_migration(job):
        return {
            "status": "unchanged",
            "migration_version": int(job.get("migration_version") or 0),
            "quality_mode": job.get("quality_mode"),
            "changes": [],
            "snapshot": None,
        }
    snapshot = _snapshot(job_dir, job_path, MIGRATION_VERSION)
    job, changes = migrate_job(job, job_dir=job_dir)
    job_path.write_text(
        json.dumps(job, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return {
        "status": "migrated",
        "migration_version": MIGRATION_VERSION,
        "quality_mode": job["quality_mode"],
        "changes": changes,
        "snapshot": str(snapshot),
    }
