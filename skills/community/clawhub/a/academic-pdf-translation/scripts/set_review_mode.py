from __future__ import annotations

import sys
from pathlib import Path

# 按 README 的写法 `python3 scripts/X.py` 运行时，sys.path 里只有 scripts/，
# 没有仓库根，academic_pdf_translation 包就 import 不到。先把根加进去。
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import argparse  # noqa: E402
from pathlib import Path  # noqa: E402

from academic_pdf_translation.contracts.enums import QualityMode  # noqa: E402
from academic_pdf_translation.contracts.migration import MIGRATION_VERSION  # noqa: E402

from _common import SkillError, load_json, utc_now, write_json  # noqa: E402
from review_policy import (  # noqa: E402
    post_repair_confirmation_template,
    review_choice_config,
)


def set_review_mode(
    job_dir: Path,
    review: str,
    *,
    reopen_finalized: bool = False,
    producer_id: str | None = None,
) -> str:
    try:
        mode, max_review_rounds, max_repair_rounds = review_choice_config(
            review
        )
    except ValueError as exc:
        raise SkillError(str(exc)) from exc
    if producer_id is not None and not producer_id.strip():
        raise SkillError("producer_id 不能是空字符串")

    job_dir = job_dir.resolve()
    job_path = job_dir / "job.json"
    job = load_json(job_path)
    was_finalized = job.get("status") == "finalized"
    if was_finalized and not reopen_finalized:
        raise SkillError(
            "已正式收尾的作业需要显式使用 --reopen-finalized 才能改检查方式"
        )

    previous_mode = job.get("review", {}).get("mode")
    previous_producer = job.get("review", {}).get("producer_id")
    effective_producer = (
        producer_id.strip()
        if isinstance(producer_id, str) and producer_id.strip()
        else previous_producer
    )
    if mode in {"independent", "precise"} and not (
        isinstance(effective_producer, str)
        and effective_producer.strip()
    ):
        raise SkillError("平衡档或精细档必须提供 --producer-id")
    files = job.setdefault("files", {})
    provenance_path = job_dir / files.get(
        "candidate_provenance",
        "candidate_provenance.json",
    )
    provenance = (
        load_json(provenance_path)
        if provenance_path.is_file()
        else None
    )
    if (
        isinstance(effective_producer, str)
        and effective_producer.strip()
        and isinstance(provenance, dict)
        and provenance.get("producer_id")
        not in {None, "", effective_producer}
    ):
        raise SkillError("当前候选已经绑定其他制作人 ID")
    if was_finalized:
        job["status"] = "accepted"
        job["review_reopened"] = {
            "at": utc_now(),
            "previous_status": "finalized",
            "previous_mode": previous_mode,
            "reason": "用户在正式收尾后要求增加完整独立审查",
        }
    # 用户改的是质量档位；review.mode 由它派生，两个字段必须一起更新，
    # 否则一致性检查会（正确地）把作业判为不一致。
    quality_mode = QualityMode.parse(review)
    job["quality_mode"] = quality_mode.value
    job["migration_version"] = MIGRATION_VERSION
    job["review"] = {
        "mode": mode,
        "derived_from_quality_mode": True,
        "choice_recorded": True,
        "producer_id": effective_producer,
        "max_review_rounds": max_review_rounds,
        "max_repair_rounds": max_repair_rounds,
    }
    rounds_relative = files.setdefault("review_rounds", "reviews/rounds.json")
    write_json(job_path, job)

    rounds_path = job_dir / rounds_relative
    if not rounds_path.is_file():
        write_json(
            rounds_path,
            {
                "schema_version": job.get("schema_version", "1.0"),
                "rounds": [],
            },
        )

    finalization_path = job_dir / job.get("files", {}).get(
        "finalization",
        "finalization.json",
    )
    finalization = load_json(finalization_path)
    finalization["review_mode"] = mode
    if was_finalized:
        finalization["review_reopened_at"] = job["review_reopened"]["at"]
        finalization["previous_review_mode"] = previous_mode
    write_json(finalization_path, finalization)

    if mode in {"independent", "precise"}:
        review_path = job_dir / job.get("files", {}).get(
            "independent_review",
            "reviews/independent.json",
        )
        independent = load_json(review_path)
        independent.setdefault("reviewed_pages", [])
        write_json(review_path, independent)
    confirmation_path = job_dir / files.get(
        "post_repair_confirmation",
        "reviews/post-repair.json",
    )
    if not confirmation_path.is_file():
        source_hash = str(job.get("source", {}).get("sha256") or "")
        write_json(
            confirmation_path,
            post_repair_confirmation_template(source_hash or None),
        )
    bound_producer = job["review"].get("producer_id")
    if (
        isinstance(bound_producer, str)
        and bound_producer.strip()
        and isinstance(provenance, dict)
    ):
        recorded = provenance.get("producer_id")
        if provenance.get("candidate_sha256") and not recorded:
            provenance["producer_id"] = bound_producer
            write_json(provenance_path, provenance)
    return mode


def main() -> int:
    parser = argparse.ArgumentParser(
        description="为已有学术 PDF 译制作业记录用户选择的检查方式"
    )
    parser.add_argument("job_dir", type=Path)
    parser.add_argument(
        "--review",
        choices=("fast", "balanced", "precise", "on", "off"),
        required=True,
    )
    parser.add_argument(
        "--reopen-finalized",
        action="store_true",
        help="将已快速收尾的作业退回 accepted，再增加独立检查",
    )
    parser.add_argument("--producer-id")
    args = parser.parse_args()
    try:
        mode = set_review_mode(
            args.job_dir,
            args.review,
            reopen_finalized=args.reopen_finalized,
            producer_id=args.producer_id,
        )
        print(
            "质量档位已更新: "
            + {
                "none": "快速",
                "independent": "平衡（推荐）",
                "precise": "精细",
            }[mode]
        )
        return 0
    except SkillError as exc:
        print(f"错误: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
