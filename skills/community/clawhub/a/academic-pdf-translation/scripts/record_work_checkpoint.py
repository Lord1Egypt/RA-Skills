from __future__ import annotations

import argparse
from pathlib import Path

from _common import (
    SCHEMA_VERSION,
    SkillError,
    internal_job_path,
    load_json,
    utc_now,
    write_json,
)


PHASES = {
    "translation",
    "layout",
    "repair",
    "review",
    "integration",
}


def record_work_checkpoint(
    job_dir: Path,
    completed_through: int,
    phase: str,
    note: str,
    blocking_issue: str | None = None,
    checkpoint_interval_pages: int = 5,
) -> dict:
    job_dir = job_dir.resolve()
    job = load_json(job_dir / "job.json")
    page_count = int(job["source"]["page_count"])
    if phase not in PHASES:
        raise SkillError(f"未知工作阶段: {phase}")
    if not 0 <= completed_through <= page_count:
        raise SkillError(
            f"completed-through 必须在 0 到 {page_count} 之间"
        )
    if checkpoint_interval_pages < 1:
        raise SkillError("checkpoint-interval-pages 必须大于 0")
    if not note.strip():
        raise SkillError("检查点 note 不能为空")

    checkpoint_path = job_dir / "work_checkpoint.json"
    previous = (
        load_json(checkpoint_path)
        if checkpoint_path.is_file()
        else {}
    )
    previous_count = int(previous.get("completed_page_count") or 0)
    if (
        previous.get("phase") == phase
        and completed_through < previous_count
    ):
        raise SkillError(
            f"检查点不能从第 {previous_count} 页倒退到"
            f"第 {completed_through} 页"
        )

    if phase == "translation" and completed_through:
        translation_path = internal_job_path(
            job_dir,
            job["files"]["translation"],
        )
        translation = load_json(translation_path)
        translated_pages = {
            unit.get("page")
            for unit in translation.get("units", [])
            if isinstance(unit.get("page"), int)
            and str(unit.get("source") or "").strip()
            and (
                str(unit.get("translation") or "").strip()
                or str(unit.get("keep_source_reason") or "").strip()
            )
        }
        missing_pages = [
            page
            for page in range(1, completed_through + 1)
            if page not in translated_pages
        ]
        if missing_pages:
            preview = ", ".join(map(str, missing_pages[:12]))
            suffix = "..." if len(missing_pages) > 12 else ""
            raise SkillError(
                "不能记录尚未落盘的翻译页: "
                f"{preview}{suffix}"
            )

    completed_pages = list(range(1, completed_through + 1))
    checkpoint = {
        "schema_version": SCHEMA_VERSION,
        "job": job_dir.name,
        "source_page_count": page_count,
        "completed_pages": completed_pages,
        "completed_page_count": completed_through,
        "last_completed_page": completed_through or None,
        "next_page": (
            completed_through + 1
            if completed_through < page_count
            else None
        ),
        "checkpoint_interval_pages": checkpoint_interval_pages,
        "phase": phase,
        "status": (
            "blocked"
            if blocking_issue
            else "complete"
            if completed_through == page_count
            else "in_progress"
        ),
        "blocking_issue": blocking_issue,
        "note": note.strip(),
        "updated_at": utc_now(),
    }
    write_json(checkpoint_path, checkpoint)
    return checkpoint


def main() -> int:
    parser = argparse.ArgumentParser(
        description="记录可恢复的逐页工作检查点"
    )
    parser.add_argument("job_dir", type=Path)
    parser.add_argument("--completed-through", type=int, required=True)
    parser.add_argument("--phase", choices=sorted(PHASES), required=True)
    parser.add_argument("--note", required=True)
    parser.add_argument("--blocking-issue")
    parser.add_argument("--checkpoint-interval-pages", type=int, default=5)
    args = parser.parse_args()
    try:
        checkpoint = record_work_checkpoint(
            args.job_dir,
            args.completed_through,
            args.phase,
            args.note,
            args.blocking_issue,
            args.checkpoint_interval_pages,
        )
        next_page = checkpoint["next_page"]
        if next_page is None:
            print("检查点已记录：该阶段全部页面完成")
        else:
            print(f"检查点已记录：下一页为 {next_page}")
        return 0
    except SkillError as exc:
        print(f"错误: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
