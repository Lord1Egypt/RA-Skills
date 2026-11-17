from __future__ import annotations

import argparse
from pathlib import Path

from _common import (
    SCHEMA_VERSION,
    SkillError,
    internal_job_path,
    load_json,
    sha256_file,
    utc_now,
    write_json,
)
from review_policy import REVIEW_MODE_LIMITS


def _pending_review(source_hash: str) -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "reviewer_role": "independent",
        "reviewer_id": None,
        "decision": "PENDING",
        "source_sha256": source_hash,
        "candidate_sha256": None,
        "coverage": [],
        "reviewed_pages": [],
        "issues": [],
        "residual_risks": [],
        "reviewed_at": None,
    }


def record_review_round(job_dir: Path) -> dict:
    job_dir = job_dir.resolve()
    job = load_json(job_dir / "job.json")
    mode = job.get("review", {}).get("mode", "legacy-double")
    limits = REVIEW_MODE_LIMITS.get(mode)
    if limits is None or limits[0] == 0:
        raise SkillError("当前质量档位不需要独立复审")

    files = job.get("files", {})
    review_path = internal_job_path(
        job_dir,
        files.get("independent_review", "reviews/independent.json"),
    )
    rounds_relative = files.get("review_rounds", "reviews/rounds.json")
    rounds_path = internal_job_path(job_dir, rounds_relative)
    review = load_json(review_path)

    decision = review.get("decision")
    if decision not in {"PASS", "FAIL"}:
        raise SkillError("当前独立复审尚未完成")
    if not isinstance(review.get("reviewer_id"), str) or not review[
        "reviewer_id"
    ].strip():
        raise SkillError("当前独立复审缺少 reviewer_id")
    producer_id = job.get("review", {}).get("producer_id")
    if not isinstance(producer_id, str) or not producer_id.strip():
        raise SkillError("当前候选缺少 producer_id")
    if producer_id.strip() == review["reviewer_id"].strip():
        raise SkillError("制作人与独立复审人不能相同")
    if not isinstance(review.get("coverage"), list) or not review["coverage"]:
        raise SkillError("当前独立复审缺少 coverage")
    if not isinstance(review.get("reviewed_at"), str) or not review[
        "reviewed_at"
    ].strip():
        raise SkillError("当前独立复审缺少 reviewed_at")

    source_path = internal_job_path(job_dir, job["source"]["job_path"])
    candidate_path = internal_job_path(job_dir, files["candidate"])
    source_hash = sha256_file(source_path)
    candidate_hash = sha256_file(candidate_path)
    if review.get("source_sha256") != source_hash:
        raise SkillError("当前独立复审对应的原文哈希不一致")
    if review.get("candidate_sha256") != candidate_hash:
        raise SkillError("当前独立复审对应的候选哈希不一致")

    page_count = int(job["source"]["page_count"])
    reviewed_pages = review.get("reviewed_pages")
    if reviewed_pages != list(range(1, page_count + 1)):
        raise SkillError("当前独立复审必须按顺序覆盖全部页面")
    if decision == "PASS":
        if review.get("issues"):
            raise SkillError("PASS 复审不能保留问题")
        if review.get("residual_risks"):
            raise SkillError("PASS 复审不能保留残余风险")
    elif not review.get("issues"):
        raise SkillError("FAIL 复审必须记录具体问题")

    if rounds_path.is_file():
        ledger = load_json(rounds_path)
    else:
        ledger = {"schema_version": SCHEMA_VERSION, "rounds": []}
    rounds = ledger.setdefault("rounds", [])
    if not isinstance(rounds, list):
        raise SkillError("reviews/rounds.json 的 rounds 必须是数组")
    limit = limits[0]
    if len(rounds) >= limit:
        raise SkillError(f"当前质量档位最多允许 {limit} 轮独立复审")
    if any(
        item.get("candidate_sha256") == candidate_hash
        and item.get("reviewer_id") == review.get("reviewer_id")
        and item.get("reviewed_at") == review.get("reviewed_at")
        for item in rounds
        if isinstance(item, dict)
    ):
        raise SkillError("当前独立复审已经记录，拒绝重复追加")

    snapshot = dict(review)
    snapshot["round_number"] = len(rounds) + 1
    snapshot["recorded_at"] = utc_now()
    rounds.append(snapshot)
    write_json(rounds_path, ledger)

    if len(rounds) < limit and decision == "PASS":
        write_json(review_path, _pending_review(source_hash))
    return snapshot


def main() -> int:
    parser = argparse.ArgumentParser(
        description="把一次完整独立复审写入轻量轮次记录"
    )
    parser.add_argument("job_dir", type=Path)
    args = parser.parse_args()
    try:
        snapshot = record_review_round(args.job_dir)
        print(
            f"已记录第 {snapshot['round_number']} 轮独立复审: "
            f"{snapshot['decision']}"
        )
        return 0
    except SkillError as exc:
        print(f"错误: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
