#!/usr/bin/env python3
"""Validate wisdom-card structure, routing, evidence coverage, and integration."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MENTORS = ROOT / "references" / "wisdom" / "mentors"
INDEX = MENTORS / "README.md"
EVIDENCE = ROOT / "references" / "wisdom" / "phase5-9-evidence-register.md"
ROUTING_CASES = MENTORS / "routing-acceptance-cases.json"
CORE_HEADING = "## 问题本质"
CURRENT_HEADINGS = ("## 触发条件", "## 行为指导", "## 不适用场景")
LEGACY_HEADINGS = ("## 关键洞察", "## 对 Carpe Diem 用户的启发", "## 反向提醒")
PHASE_5_9_CARDS = (
    "validate/pricing-test.md", "validate/competitive-analysis.md",
    "validate/experiment-design.md", "validate/gonogo-decision.md",
    "validate/user-interview.md", "cross/premature-optimization.md",
    "cross/feature-creep.md", "cross/analysis-paralysis.md",
    "cross/unicorn-mindset.md", "plan/rfc-design.md", "track/code-review.md",
    "track/retrospective.md", "track/tech-debt.md", "cross/async-communication.md",
    "cross/growth-flywheel.md", "cross/user-retention.md",
    "cross/product-strategy.md", "cross/continuous-discovery.md",
    "plan/api-design.md", "track/observability.md", "plan/data-modeling.md",
    "plan/security-design.md",
)
PHASE_5_9_EVIDENCE = {
    relative: f"WD-P{phase}-{number:02d}"
    for phase, cards in {
        5: PHASE_5_9_CARDS[0:5],
        6: PHASE_5_9_CARDS[5:9],
        7: PHASE_5_9_CARDS[9:14],
        8: PHASE_5_9_CARDS[14:18],
        9: PHASE_5_9_CARDS[18:22],
    }.items()
    for number, relative in enumerate(cards, start=1)
}
REQUIRED_ROUTING_CASES = {
    "validate-frame-before-experiment",
    "validate-choose-experiment",
    "validate-decide-after-experiment",
    "scope-before-commit",
    "scope-already-growing",
    "rfc-before-decision",
    "adr-after-decision",
    "retention-existing-users-leave",
    "growth-no-repeatable-loop",
}
VALID_STAGES = {"discover", "validate", "plan", "track", "cross"}


def normalized_hash(text: str) -> str:
    normalized = "\n".join(line.rstrip() for line in text.strip().splitlines())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def validate() -> list[str]:
    errors: list[str] = []
    cards = sorted(
        path for path in MENTORS.glob("*/*.md") if path.name != "README.md"
    )
    if not cards:
        return ["no wisdom cards found"]

    hashes: dict[str, Path] = {}
    for card in cards:
        text = card.read_text(encoding="utf-8")
        relative = card.relative_to(ROOT)
        if CORE_HEADING not in text:
            errors.append(f"{relative}: missing {CORE_HEADING}")
        current = all(heading in text for heading in CURRENT_HEADINGS)
        legacy = all(heading in text for heading in LEGACY_HEADINGS)
        if not current and not legacy:
            errors.append(
                f"{relative}: must use either current or legacy complete card structure"
            )
        digest = normalized_hash(text)
        if digest in hashes:
            errors.append(f"duplicate content: {relative} == {hashes[digest].relative_to(ROOT)}")
        else:
            hashes[digest] = card

    index_text = INDEX.read_text(encoding="utf-8")
    for link in re.findall(r"\]\(([^)]+\.md)\)", index_text):
        target = (INDEX.parent / link).resolve()
        if not target.is_file():
            errors.append(f"index link missing: {link}")

    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    manifest_files = set(manifest["files"])
    for card in cards:
        relative = card.relative_to(ROOT).as_posix()
        if relative not in manifest_files:
            errors.append(f"manifest missing card: {relative}")
    for required in (
        "references/wisdom/phase5-9-evidence-register.md",
        "references/wisdom/mentors/routing-acceptance-cases.json",
        "scripts/validate_wisdom_cards.py",
    ):
        if required not in manifest_files:
            errors.append(f"manifest missing resource: {required}")

    evidence_text = EVIDENCE.read_text(encoding="utf-8")
    evidence_rows = re.findall(
        r"^\| (WD-P\d+-\d+) \| `([^`]+)` \|.*?\| "
        r"(verified-primary|verified-multiple|needs-primary-source-check|rejected) \|",
        evidence_text,
        flags=re.MULTILINE,
    )
    evidence_statuses: dict[str, str] = {}
    for evidence_id, relative, status in evidence_rows:
        expected_id = PHASE_5_9_EVIDENCE.get(relative)
        if expected_id is None:
            errors.append(f"evidence register has unknown card: {relative}")
        elif evidence_id != expected_id:
            errors.append(
                f"evidence id mismatch for {relative}: {evidence_id} != {expected_id}"
            )
        if evidence_id in evidence_statuses:
            errors.append(f"duplicate evidence id: {evidence_id}")
        evidence_statuses[evidence_id] = status

    for relative, evidence_id in PHASE_5_9_EVIDENCE.items():
        if evidence_id not in evidence_statuses:
            errors.append(f"evidence register missing: {evidence_id} {relative}")
        card_text = (MENTORS / relative).read_text(encoding="utf-8")
        if f"证据编号：{evidence_id}" not in card_text:
            errors.append(f"{relative}: missing evidence id {evidence_id}")

    status_counts = {
        status: list(evidence_statuses.values()).count(status)
        for status in set(evidence_statuses.values())
    }
    if status_counts.get("verified-primary", 0) != 22:
        errors.append("evidence register must contain exactly 22 verified-primary cards")
    if status_counts.get("needs-primary-source-check", 0) != 0:
        errors.append("release evidence register must not contain pending source checks")

    routing = json.loads(ROUTING_CASES.read_text(encoding="utf-8"))
    if routing.get("schema_version") != 1:
        errors.append("routing acceptance cases must use schema_version 1")
    cases = routing.get("cases")
    if not isinstance(cases, list):
        errors.append("routing acceptance cases must contain a cases list")
        cases = []
    case_ids: set[str] = set()
    for case in cases:
        if not isinstance(case, dict):
            errors.append("routing acceptance case must be an object")
            continue
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id:
            errors.append("routing acceptance case missing id")
            continue
        if case_id in case_ids:
            errors.append(f"duplicate routing case id: {case_id}")
        case_ids.add(case_id)
        if case.get("stage") not in VALID_STAGES:
            errors.append(f"{case_id}: invalid stage {case.get('stage')!r}")

        primary = case.get("primary")
        supporting = case.get("supporting")
        selected = [item for item in (primary, supporting) if item is not None]
        if not isinstance(primary, str) or not primary:
            errors.append(f"{case_id}: primary card is required")
        if supporting is not None and not isinstance(supporting, str):
            errors.append(f"{case_id}: supporting card must be a string or null")
        if len(selected) > 2 or len(selected) != len(set(selected)):
            errors.append(f"{case_id}: selected cards must be unique and at most two")
        for relative in selected:
            if isinstance(relative, str) and not (MENTORS / relative).is_file():
                errors.append(f"{case_id}: selected card missing: {relative}")

        forbidden_cards = case.get("must_not_select")
        if not isinstance(forbidden_cards, list) or not all(
            isinstance(item, str) for item in forbidden_cards
        ):
            errors.append(f"{case_id}: must_not_select must be a string list")
            forbidden_cards = []
        overlap = set(selected) & set(forbidden_cards)
        if overlap:
            errors.append(f"{case_id}: selected and forbidden overlap: {sorted(overlap)}")
        for relative in forbidden_cards:
            if not (MENTORS / relative).is_file():
                errors.append(f"{case_id}: forbidden card missing: {relative}")

    missing_cases = REQUIRED_ROUTING_CASES - case_ids
    if missing_cases:
        errors.append(f"routing acceptance cases missing: {sorted(missing_cases)}")

    skill_zh = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    skill_en = (ROOT / "SKILL.en.md").read_text(encoding="utf-8")
    if "每轮最多加载 1 张主卡" not in skill_zh:
        errors.append("SKILL.md missing one-primary-card routing budget")
    if "at most one primary mentor card" not in skill_en:
        errors.append("SKILL.en.md missing one-primary-card routing budget")

    forbidden = {
        "references/wisdom/mentors/track/code-review.md": "< 200 行",
        "references/wisdom/mentors/track/observability.md": "三支柱：日志、指标、追踪",
        "references/wisdom/mentors/track/tech-debt.md": "每次 sprint 预留 20%",
    }
    for relative, phrase in forbidden.items():
        if phrase in (ROOT / relative).read_text(encoding="utf-8"):
            errors.append(f"{relative}: forbidden universal rule remains: {phrase}")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"wisdom validation failed: {len(errors)} error(s)")
        return 1
    count = len(list(MENTORS.glob("*/*.md")))
    print(f"wisdom validation passed: {count} cards")
    return 0


if __name__ == "__main__":
    sys.exit(main())
