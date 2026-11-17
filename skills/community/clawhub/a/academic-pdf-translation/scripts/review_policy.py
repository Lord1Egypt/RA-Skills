from __future__ import annotations

from typing import Any


REVIEW_CHOICES = {
    "fast": ("none", 0, 0),
    "balanced": ("independent", 1, 1),
    "precise": ("precise", 1, 1),
    "off": ("none", 0, 0),
    "on": ("independent", 1, 1),
}

REVIEW_MODE_LIMITS = {
    "none": (0, 0),
    "independent": (1, 1),
    "precise": (1, 1),
}

PRECISE_KEY_CHECKS = (
    "statistics",
    "core-definitions",
    "instruments",
    "figures",
)


def review_choice_config(choice: str) -> tuple[str, int, int]:
    if choice not in REVIEW_CHOICES:
        raise ValueError("review 必须是 'fast'、'balanced' 或 'precise'")
    return REVIEW_CHOICES[choice]


def post_repair_confirmation_template(source_hash: str | None = None) -> dict:
    return {
        "schema_version": "1.0",
        "mode": None,
        "producer_id": None,
        "reviewer_id": None,
        "decision": "PENDING",
        "source_sha256": source_hash,
        "base_review_candidate_sha256": None,
        "candidate_sha256": None,
        "changed_pages": [],
        "same_type_pages": [],
        "checked_pages": [],
        "key_content_checks": [],
        "issues": [],
        "qa_sha256": None,
        "completeness_audit_sha256": None,
        "comparison_manifest_sha256": None,
        "reviewed_at": None,
    }


def _page_list(
    value: Any,
    *,
    field: str,
    page_count: int,
    errors: list[str],
) -> list[int]:
    if not isinstance(value, list):
        errors.append(f"{field} 必须是页码数组")
        return []
    pages: list[int] = []
    for page in value:
        if (
            isinstance(page, bool)
            or not isinstance(page, int)
            or not 1 <= page <= page_count
        ):
            errors.append(f"{field} 含无效页码: {page!r}")
            continue
        pages.append(page)
    if len(pages) != len(set(pages)):
        errors.append(f"{field} 含重复页码")
    return sorted(set(pages))


def required_post_repair_pages(
    changed_pages: list[int],
    same_type_pages: list[int],
    page_count: int,
) -> list[int]:
    pages = set(changed_pages) | set(same_type_pages)
    for page in changed_pages:
        if page > 1:
            pages.add(page - 1)
        if page < page_count:
            pages.add(page + 1)
    return sorted(pages)


def validate_post_repair_confirmation(
    confirmation: Any,
    *,
    mode: str,
    producer_id: str,
    reviewer_id: str,
    source_hash: str,
    base_candidate_hash: str,
    candidate_hash: str,
    page_count: int,
    qa_hash: str,
    completeness_hash: str,
    comparison_manifest_hash: str,
) -> list[str]:
    errors: list[str] = []
    if not isinstance(confirmation, dict):
        return ["返修确认记录必须是对象"]
    if mode not in {"independent", "precise"}:
        errors.append("快速档不应创建返修后人工确认")
    if confirmation.get("mode") != mode:
        errors.append("返修确认记录的质量档位不一致")
    if confirmation.get("producer_id") != producer_id:
        errors.append("返修确认记录的制作人 ID 不一致")
    if confirmation.get("reviewer_id") != reviewer_id:
        errors.append("返修确认记录的复审人 ID 不一致")
    if not producer_id.strip():
        errors.append("缺少制作人 ID")
    if not reviewer_id.strip():
        errors.append("缺少复审人 ID")
    if producer_id.strip() == reviewer_id.strip():
        errors.append("制作人与独立复审人不能相同")
    if confirmation.get("decision") != "PASS":
        errors.append("返修后定向确认尚未通过")
    if confirmation.get("source_sha256") != source_hash:
        errors.append("返修确认对应的原文哈希不一致")
    if (
        confirmation.get("base_review_candidate_sha256")
        != base_candidate_hash
    ):
        errors.append("返修确认没有绑定独立复审失败的候选")
    if confirmation.get("candidate_sha256") != candidate_hash:
        errors.append("返修确认对应的当前候选哈希不一致")

    changed_pages = _page_list(
        confirmation.get("changed_pages"),
        field="changed_pages",
        page_count=page_count,
        errors=errors,
    )
    same_type_pages = _page_list(
        confirmation.get("same_type_pages"),
        field="same_type_pages",
        page_count=page_count,
        errors=errors,
    )
    checked_pages = _page_list(
        confirmation.get("checked_pages"),
        field="checked_pages",
        page_count=page_count,
        errors=errors,
    )
    if not changed_pages:
        errors.append("返修确认必须记录至少一个改动页")
    required_pages = required_post_repair_pages(
        changed_pages,
        same_type_pages,
        page_count,
    )
    missing_pages = sorted(set(required_pages) - set(checked_pages))
    if missing_pages:
        errors.append(
            "返修确认未覆盖改动页、相邻页或同类受影响页: "
            + ", ".join(map(str, missing_pages))
        )

    issues = confirmation.get("issues")
    if not isinstance(issues, list):
        errors.append("返修确认 issues 必须是数组")
    elif issues:
        errors.append("PASS 的返修确认不能保留未解决问题")

    checks = confirmation.get("key_content_checks")
    if not isinstance(checks, list):
        errors.append("key_content_checks 必须是数组")
        checks = []
    categories: dict[str, dict] = {}
    for index, check in enumerate(checks):
        if not isinstance(check, dict):
            errors.append(f"key_content_checks[{index}] 必须是对象")
            continue
        category = str(check.get("category") or "")
        if not category:
            errors.append(f"key_content_checks[{index}] 缺少 category")
            continue
        if category in categories:
            errors.append(f"关键内容检查重复: {category}")
        categories[category] = check
        if check.get("status") not in {"PASS", "NOT_APPLICABLE"}:
            errors.append(f"关键内容检查状态无效: {category}")
        if not str(check.get("evidence") or "").strip():
            errors.append(f"关键内容检查缺少依据: {category}")
    if mode == "precise":
        missing_checks = [
            category
            for category in PRECISE_KEY_CHECKS
            if category not in categories
        ]
        if missing_checks:
            errors.append(
                "精细档缺少关键内容检查: " + ", ".join(missing_checks)
            )

    expected_hashes = {
        "qa_sha256": qa_hash,
        "completeness_audit_sha256": completeness_hash,
        "comparison_manifest_sha256": comparison_manifest_hash,
    }
    for field, expected in expected_hashes.items():
        if not expected or confirmation.get(field) != expected:
            errors.append(f"返修确认的 {field} 已过期或缺失")
    if not str(confirmation.get("reviewed_at") or "").strip():
        errors.append("返修确认缺少 reviewed_at")
    return errors
