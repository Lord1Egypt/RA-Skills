#!/usr/bin/env python3
"""校验结构化南京留学移民机构审计矩阵。/ Validate a structured Nanjing overseas-agency audit matrix."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any


ALLOWED_GRADES = {"A", "B", "C", "D"}
ALLOWED_TIERS = {
    "综合老牌头部机构",
    "Established comprehensive leader",
    "垂直精品专项机构",
    "Vertical specialist boutique",
    "初创移民导向机构",
    "Startup immigration-focused agency",
    "主体或交付链条不合规代办",
    "Entity or delivery-chain noncompliant operator",
    "待分类",
    "Unclassified",
}
ALLOWED_LICENSE_STATUS = {
    "no-current-special-license-regime",
    "unverified",
    "yes-currently-verified",
}


def bi(chinese: str, english: str) -> str:
    """Return a Chinese-first bilingual message."""
    return f"{chinese} / {english}"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(bi("JSON顶层值必须是对象", "top-level JSON value must be an object"))
    return data


def is_http_url(value: Any) -> bool:
    return isinstance(value, str) and value.startswith(("https://", "http://"))


def validate_source(source: Any, label: str, errors: list[str]) -> None:
    if not isinstance(source, dict):
        errors.append(f"{label}: {bi('来源必须是对象', 'source must be an object')}")
        return
    if not is_http_url(source.get("url")):
        errors.append(f"{label}: {bi('source.url必须使用http(s)', 'source.url must be http(s)')}")
    if source.get("grade") not in ALLOWED_GRADES:
        errors.append(f"{label}: {bi('source.grade必须为A、B、C或D', 'source.grade must be A, B, C, or D')}")
    accessed = source.get("accessed")
    try:
        date.fromisoformat(accessed)
    except (TypeError, ValueError):
        errors.append(f"{label}: {bi('source.accessed必须为YYYY-MM-DD', 'source.accessed must be YYYY-MM-DD')}")


def validate_agency(agency: Any, index: int, errors: list[str], warnings: list[str]) -> None:
    label = f"agencies[{index}]"
    if not isinstance(agency, dict):
        errors.append(f"{label}: {bi('必须是对象', 'must be an object')}")
        return

    for field in ("name", "legal_entity", "tier", "current_double_license", "score", "evidence_coverage", "deductions"):
        if field not in agency:
            errors.append(f"{label}: {bi(f'缺少字段{field}', f'missing {field}')}")

    if agency.get("tier") not in ALLOWED_TIERS:
        errors.append(f"{label}: {bi('无效梯队', 'invalid tier')} {agency.get('tier')!r}")

    license_status = agency.get("current_double_license")
    if license_status not in ALLOWED_LICENSE_STATUS:
        errors.append(f"{label}: {bi('current_double_license值无效', 'invalid current_double_license value')}")

    try:
        score = float(agency.get("score"))
    except (TypeError, ValueError):
        errors.append(f"{label}: {bi('score必须为数字', 'score must be numeric')}")
        score = -1.0
    if not 0.0 <= score <= 10.0:
        errors.append(f"{label}: {bi('score必须在0到10之间', 'score must be between 0 and 10')}")

    coverage = agency.get("evidence_coverage")
    if not isinstance(coverage, int) or not 0 <= coverage <= 100 or coverage % 10:
        errors.append(f"{label}: {bi('evidence_coverage必须为0到100且以10递增', 'evidence_coverage must be 0..100 in steps of 10')}")
    elif coverage < 60 and not agency.get("score_label", "").startswith(("暂定", "Provisional", "provisional")):
        warnings.append(f"{label}: {bi('覆盖率低于60%；score_label应以“暂定”或“Provisional”开头', 'coverage below 60%; score_label should begin with 暂定 or Provisional')}")

    deductions = agency.get("deductions", [])
    if not isinstance(deductions, list):
        errors.append(f"{label}: {bi('deductions必须是列表', 'deductions must be a list')}")
        deductions = []

    total = 0.0
    for deduction_index, deduction in enumerate(deductions):
        dlabel = f"{label}.deductions[{deduction_index}]"
        if not isinstance(deduction, dict):
            errors.append(f"{dlabel}: {bi('必须是对象', 'must be an object')}")
            continue
        for field in ("points", "dimension", "fact", "reason", "sources"):
            if field not in deduction:
                errors.append(f"{dlabel}: {bi(f'缺少字段{field}', f'missing {field}')}")
        try:
            points = float(deduction.get("points"))
        except (TypeError, ValueError):
            errors.append(f"{dlabel}: {bi('points必须为数字', 'points must be numeric')}")
            continue
        if points <= 0 or points > 2:
            errors.append(f"{dlabel}: {bi('points必须大于0且不超过2', 'points must be >0 and <=2')}")
        if abs(points * 2 - round(points * 2)) > 1e-9:
            errors.append(f"{dlabel}: {bi('points必须以0.5递增', 'points must use 0.5 increments')}")
        total += points

        for field in ("dimension", "fact", "reason"):
            if not isinstance(deduction.get(field), str) or not deduction[field].strip():
                errors.append(f"{dlabel}: {bi(f'{field}必须为非空文本', f'{field} must be non-empty text')}")

        sources = deduction.get("sources", [])
        if not isinstance(sources, list) or not sources:
            errors.append(f"{dlabel}: {bi('至少需要一个来源', 'at least one source is required')}")
            sources = []
        grades: set[str] = set()
        for source_index, source in enumerate(sources):
            validate_source(source, f"{dlabel}.sources[{source_index}]", errors)
            if isinstance(source, dict) and source.get("grade") in ALLOWED_GRADES:
                grades.add(source["grade"])
        if grades and grades == {"D"}:
            errors.append(f"{dlabel}: {bi('D级证据不能单独支持扣分', 'Grade D cannot be the sole support for a deduction')}")

    expected = max(0.0, round(10.0 - total, 1))
    if score >= 0 and abs(score - expected) > 0.01:
        errors.append(f"{label}: {bi(f'得分{score:.1f}不等于10减去扣分（{expected:.1f}）', f'score {score:.1f} does not equal 10 - deductions ({expected:.1f})')}")

    if license_status == "yes-currently-verified":
        sources = agency.get("current_license_sources", [])
        official_sources = [source for source in sources if isinstance(source, dict) and source.get("grade") == "A"]
        if len(official_sources) < 2:
            errors.append(f"{label}: {bi('现行双证主张至少需要两个A级来源', 'a current dual-licence claim requires at least two Grade A sources')}")
        for source_index, source in enumerate(sources):
            validate_source(source, f"{label}.current_license_sources[{source_index}]", errors)


def validate(data: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    audit_date = data.get("audit_date")
    try:
        date.fromisoformat(audit_date)
    except (TypeError, ValueError):
        errors.append(bi("audit_date必须为YYYY-MM-DD", "audit_date must be YYYY-MM-DD"))

    agencies = data.get("agencies")
    if not isinstance(agencies, list) or not agencies:
        errors.append(bi("agencies必须是非空列表", "agencies must be a non-empty list"))
        return errors, warnings

    seen_entities: set[str] = set()
    for index, agency in enumerate(agencies):
        validate_agency(agency, index, errors, warnings)
        if isinstance(agency, dict):
            entity = agency.get("legal_entity")
            if isinstance(entity, str) and entity.strip():
                normalized = entity.strip().lower()
                if normalized in seen_entities:
                    warnings.append(f"agencies[{index}]: {bi('重复legal_entity', 'duplicate legal_entity')} {entity!r}")
                seen_entities.add(normalized)
    return errors, warnings


def self_test() -> int:
    sample = {
        "audit_date": "2026-08-14",
        "agencies": [
            {
                "name": "示例品牌",
                "legal_entity": "示例咨询有限公司",
                "tier": "待分类",
                "current_double_license": "no-current-special-license-regime",
                "score": 9.5,
                "score_label": "暂定9.5/10",
                "evidence_coverage": 50,
                "deductions": [
                    {
                        "points": 0.5,
                        "dimension": "合同退款",
                        "fact": "合同未写退款完成期限",
                        "reason": "消费者无法确定资金回收时间",
                        "sources": [
                            {
                                "url": "https://example.gov.cn/contract",
                                "grade": "B",
                                "accessed": "2026-08-14",
                            }
                        ],
                    }
                ],
            },
            {
                "name": "Example Brand",
                "legal_entity": "Example Consulting Ltd.",
                "tier": "Unclassified",
                "current_double_license": "no-current-special-license-regime",
                "score": 10.0,
                "score_label": "Provisional 10.0/10",
                "evidence_coverage": 40,
                "deductions": [],
            },
        ],
    }
    errors, warnings = validate(sample)
    if errors:
        print(bi("自测失败", "SELF-TEST FAILED"))
        for item in errors:
            print(f"错误 / ERROR: {item}")
        return 1

    invalid = json.loads(json.dumps(sample, ensure_ascii=False))
    invalid_agency = invalid["agencies"][0]
    invalid_agency["score"] = 10.0
    invalid_agency["deductions"][0]["sources"][0]["grade"] = "D"
    invalid_errors, _ = validate(invalid)
    if not any("does not equal 10 - deductions" in item for item in invalid_errors):
        print(bi("自测失败：未拒绝分数不一致", "SELF-TEST FAILED: score mismatch was not rejected"))
        return 1
    if not any("Grade D cannot be the sole support" in item for item in invalid_errors):
        print(bi("自测失败：未拒绝仅由D级证据支持的扣分", "SELF-TEST FAILED: Grade D-only deduction was not rejected"))
        return 1

    print(bi("自测通过", "SELF-TEST PASSED"))
    for item in warnings:
        print(f"警告 / WARNING: {item}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("json_path", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return self_test()
    if args.json_path is None:
        parser.error(bi("除非使用--self-test，否则必须提供json_path", "json_path is required unless --self-test is used"))

    try:
        data = load_json(args.json_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"错误 / ERROR: {exc}", file=sys.stderr)
        return 1

    errors, warnings = validate(data)
    for item in warnings:
        print(f"警告 / WARNING: {item}")
    for item in errors:
        print(f"错误 / ERROR: {item}", file=sys.stderr)
    if errors:
        print(bi(f"失败：{len(errors)}个错误，{len(warnings)}个警告", f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s)"))
        return 1
    print(bi(f"通过：{len(data['agencies'])}条机构记录，{len(warnings)}个警告", f"PASSED: {len(data['agencies'])} agency record(s), {len(warnings)} warning(s)"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
