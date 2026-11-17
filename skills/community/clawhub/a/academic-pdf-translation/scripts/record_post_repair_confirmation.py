from __future__ import annotations

import argparse
from pathlib import Path

from _common import (
    SkillError,
    internal_job_path,
    load_json,
    sha256_file,
    utc_now,
    write_json,
)
from review_policy import (
    PRECISE_KEY_CHECKS,
    required_post_repair_pages,
    validate_post_repair_confirmation,
)


def _parse_pages(value: str, page_count: int) -> list[int]:
    pages: set[int] = set()
    for part in str(value or "").split(","):
        token = part.strip()
        if not token:
            continue
        if "-" in token:
            left, right = token.split("-", 1)
            try:
                start = int(left)
                end = int(right)
            except ValueError as exc:
                raise SkillError(f"无效页码范围: {token}") from exc
            if start > end:
                raise SkillError(f"页码范围顺序错误: {token}")
            pages.update(range(start, end + 1))
        else:
            try:
                pages.add(int(token))
            except ValueError as exc:
                raise SkillError(f"无效页码: {token}") from exc
    invalid = sorted(page for page in pages if not 1 <= page <= page_count)
    if invalid:
        raise SkillError(
            f"页码超出 1..{page_count}: {', '.join(map(str, invalid))}"
        )
    return sorted(pages)


def _parse_key_checks(values: list[str]) -> list[dict]:
    checks: list[dict] = []
    for value in values:
        category, separator, remainder = value.partition("=")
        status, evidence_separator, evidence = remainder.partition(":")
        if (
            not separator
            or not evidence_separator
            or not category.strip()
            or status.strip() not in {"PASS", "NOT_APPLICABLE"}
            or not evidence.strip()
        ):
            raise SkillError(
                "--key-check 格式必须为 "
                "category=PASS:核对依据 或 "
                "category=NOT_APPLICABLE:不适用依据"
            )
        checks.append(
            {
                "category": category.strip(),
                "status": status.strip(),
                "evidence": evidence.strip(),
            }
        )
    return checks


def _latest_failed_review(job_dir: Path, job: dict) -> dict:
    files = job.get("files", {})
    rounds_path = internal_job_path(
        job_dir,
        files.get("review_rounds", "reviews/rounds.json"),
    )
    rounds = load_json(rounds_path).get("rounds", [])
    completed = [
        item
        for item in rounds
        if isinstance(item, dict)
        and item.get("decision") in {"PASS", "FAIL"}
    ]
    if not completed or completed[-1].get("decision") != "FAIL":
        raise SkillError("当前作业没有紧接在前的独立复审 FAIL 记录")
    return completed[-1]


def record_post_repair_confirmation(
    job_dir: Path,
    *,
    reviewer_id: str,
    changed_pages: list[int],
    same_type_pages: list[int],
    checked_pages: list[int] | None,
    key_content_checks: list[dict],
    decision: str,
    issues: list[str],
) -> dict:
    job_dir = job_dir.resolve()
    job = load_json(job_dir / "job.json")
    mode = str(job.get("review", {}).get("mode") or "")
    if mode not in {"independent", "precise"}:
        raise SkillError("快速档不需要返修后人工确认")
    producer_id = str(
        job.get("review", {}).get("producer_id") or ""
    ).strip()
    reviewer_id = reviewer_id.strip()
    if not producer_id:
        raise SkillError("作业缺少 producer_id")
    if not reviewer_id:
        raise SkillError("reviewer_id 不能为空")
    if producer_id == reviewer_id:
        raise SkillError("制作人与独立复审人不能相同")
    if decision != "PASS":
        raise SkillError(
            "返修确认只记录可收尾的 PASS；仍有问题时继续修改，不写完成记录"
        )
    if issues:
        raise SkillError("PASS 不能保留未解决问题")

    files = job.get("files", {})
    source_path = internal_job_path(job_dir, job["source"]["job_path"])
    candidate_path = internal_job_path(job_dir, files["candidate"])
    provenance_path = internal_job_path(
        job_dir,
        files["candidate_provenance"],
    )
    qa_path = internal_job_path(job_dir, files["qa"])
    completeness_path = job_dir / "reviews" / "completeness-audit.json"
    comparison_path = job_dir / "comparisons" / "manifest.json"
    required_files = {
        "candidate": candidate_path,
        "candidate provenance": provenance_path,
        "QA": qa_path,
        "completeness audit": completeness_path,
        "comparison manifest": comparison_path,
    }
    missing = [
        label for label, path in required_files.items() if not path.is_file()
    ]
    if missing:
        raise SkillError("返修确认缺少证据文件: " + ", ".join(missing))

    source_hash = sha256_file(source_path)
    candidate_hash = sha256_file(candidate_path)
    provenance = load_json(provenance_path)
    failed_review = _latest_failed_review(job_dir, job)
    base_hash = str(failed_review.get("candidate_sha256") or "")
    if provenance.get("supersedes_candidate_sha256") != base_hash:
        raise SkillError("当前候选没有直接替代独立复审失败的候选")
    comparison = load_json(comparison_path)
    if comparison.get("source_sha256") != source_hash:
        raise SkillError("对照图包对应的原文已经过期")
    if comparison.get("candidate_sha256") != candidate_hash:
        raise SkillError("对照图包对应的候选已经过期")

    page_count = int(job["source"]["page_count"])
    required_pages = required_post_repair_pages(
        changed_pages,
        same_type_pages,
        page_count,
    )
    effective_checked = (
        sorted(set(checked_pages))
        if checked_pages is not None
        else required_pages
    )
    record = {
        "schema_version": "1.0",
        "mode": mode,
        "producer_id": producer_id,
        "reviewer_id": reviewer_id,
        "decision": decision,
        "source_sha256": source_hash,
        "base_review_candidate_sha256": base_hash,
        "candidate_sha256": candidate_hash,
        "changed_pages": sorted(set(changed_pages)),
        "same_type_pages": sorted(set(same_type_pages)),
        "checked_pages": effective_checked,
        "key_content_checks": key_content_checks,
        "issues": [{"message": issue} for issue in issues],
        "qa_sha256": sha256_file(qa_path),
        "completeness_audit_sha256": sha256_file(completeness_path),
        "comparison_manifest_sha256": sha256_file(comparison_path),
        "reviewed_at": utc_now(),
    }
    errors = validate_post_repair_confirmation(
        record,
        mode=mode,
        producer_id=producer_id,
        reviewer_id=reviewer_id,
        source_hash=source_hash,
        base_candidate_hash=base_hash,
        candidate_hash=candidate_hash,
        page_count=page_count,
        qa_hash=record["qa_sha256"],
        completeness_hash=record["completeness_audit_sha256"],
        comparison_manifest_hash=record["comparison_manifest_sha256"],
    )
    if errors:
        raise SkillError("返修确认无效: " + "；".join(errors))
    output_path = internal_job_path(
        job_dir,
        files.get(
            "post_repair_confirmation",
            "reviews/post-repair.json",
        ),
    )
    write_json(output_path, record)
    return record


def main() -> int:
    parser = argparse.ArgumentParser(
        description="记录集中返修后的改动页、相邻页和关键内容定向确认"
    )
    parser.add_argument("job_dir", type=Path)
    parser.add_argument("--reviewer-id", required=True)
    parser.add_argument("--changed-pages", required=True)
    parser.add_argument("--same-type-pages", default="")
    parser.add_argument("--checked-pages")
    parser.add_argument(
        "--key-check",
        action="append",
        default=[],
        help=(
            "精细档重复使用；例如 "
            "statistics=PASS:已核对全部统计值"
        ),
    )
    parser.add_argument(
        "--decision",
        choices=("PASS",),
        default="PASS",
    )
    parser.add_argument("--issue", action="append", default=[])
    args = parser.parse_args()
    try:
        job = load_json(args.job_dir.resolve() / "job.json")
        page_count = int(job["source"]["page_count"])
        changed_pages = _parse_pages(args.changed_pages, page_count)
        same_type_pages = _parse_pages(
            args.same_type_pages,
            page_count,
        )
        checked_pages = (
            _parse_pages(args.checked_pages, page_count)
            if args.checked_pages
            else None
        )
        key_checks = _parse_key_checks(args.key_check)
        if job.get("review", {}).get("mode") == "precise":
            provided = {
                str(item.get("category") or "")
                for item in key_checks
            }
            missing = [
                category
                for category in PRECISE_KEY_CHECKS
                if category not in provided
            ]
            if missing:
                raise SkillError(
                    "精细档缺少 --key-check: " + ", ".join(missing)
                )
        record = record_post_repair_confirmation(
            args.job_dir,
            reviewer_id=args.reviewer_id,
            changed_pages=changed_pages,
            same_type_pages=same_type_pages,
            checked_pages=checked_pages,
            key_content_checks=key_checks,
            decision=args.decision,
            issues=args.issue,
        )
        print(
            "返修后定向确认已记录: "
            f"{record['decision']}，覆盖 "
            f"{len(record['checked_pages'])} 个源页"
        )
        return 0
    except SkillError as exc:
        print(f"错误: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
