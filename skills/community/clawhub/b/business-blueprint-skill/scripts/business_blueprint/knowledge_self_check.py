"""Self-check question library for knowledge entities.

The AI is expected to populate ``_selfCheck`` on each knowledge entity:

    {
      "id": "pain-001",
      "name": "ROI 不稳",
      "entityType": "painPoint",
      "_selfCheck": {
        "passed": ["可观测", "受影响方明确"],
        "questions": ["是症状还是根因？— 待用户确认"]
      }
    }

This module provides:
- ``SELF_CHECK_QUESTIONS``: canonical question list per entityType
- ``derive_questions``: heuristic check given an entity (used to seed
  ``_selfCheck.questions`` when AI has not populated it)
- ``has_unresolved_questions``: True if entity has non-empty questions
"""
from __future__ import annotations

from typing import Any


SELF_CHECK_QUESTIONS: dict[str, list[str]] = {
    "painPoint": [
        "是症状还是根因？",
        "严重度判断依据是什么（数据/感受/对标）？",
        "受影响的角色或部门是谁？",
    ],
    "strategy": [
        "对应哪个具体痛点（必须有 solves 关系）？",
        "执行前提是什么（资源/能力/时机）？",
        "怎么衡量它有效（必须有 measures 关系指向 metric）？",
    ],
    "rule": [
        "规则来源是什么（平台/法规/内部）？",
        "违反后果具体是什么？",
        "约束哪些策略（必须有 enforces 关系）？",
    ],
    "metric": [
        "计算方式或基准值是什么？",
        "衡量哪个策略（必须有 measures 关系）？",
        "阈值的业务依据是什么？",
    ],
    "practice": [
        "频率或周期是多少？",
        "支撑哪个策略（必须有 requires 反向关系）？",
        "成功的衡量信号是什么？",
    ],
    "pitfall": [
        "导致什么具体痛点（必须有 causes 关系）？",
        "避免方式是什么？",
        "是否有真实案例或数据支撑？",
    ],
}


def has_unresolved_questions(entity: dict[str, Any]) -> bool:
    """True if the entity has a non-empty ``_selfCheck.questions`` list."""
    self_check = entity.get("_selfCheck")
    if not isinstance(self_check, dict):
        return False
    questions = self_check.get("questions", [])
    return isinstance(questions, list) and len(questions) > 0


def derive_questions(
    entity: dict[str, Any],
    relations: list[dict[str, Any]] | None = None,
) -> list[str]:
    """Heuristic self-check.

    Given an entity (and optionally the surrounding relations list), return the
    subset of canonical questions that look unresolved based on what's actually
    in the entity. Used to seed ``_selfCheck.questions`` when AI has not
    populated it explicitly.

    Heuristics:
    - strategy without an outgoing ``solves`` relation → keep the "对应哪个痛点" question
    - strategy without an outgoing ``measures`` relation → keep the metric question
    - rule without an outgoing ``enforces`` relation → keep the strategy question
    - metric without an outgoing ``measures`` relation → keep the strategy question
    - pitfall without an outgoing ``causes`` relation → keep the painPoint question
    - painPoint always keeps "症状还是根因" (we cannot infer this)
    - description-less entities keep "依据/计算方式" question
    """
    entity_type = entity.get("entityType")
    if entity_type not in SELF_CHECK_QUESTIONS:
        return []

    relations = relations or []
    entity_id = entity.get("id")

    outgoing_types: set[str] = set()
    for rel in relations:
        if isinstance(rel, dict) and rel.get("from") == entity_id:
            rel_type = rel.get("type")
            if isinstance(rel_type, str):
                outgoing_types.add(rel_type)

    pool = SELF_CHECK_QUESTIONS[entity_type]
    keep: list[str] = []

    if entity_type == "painPoint":
        keep.append(pool[0])  # 症状还是根因 — never inferable
        if not entity.get("severity"):
            keep.append(pool[1])  # 严重度依据
        if not entity.get("description"):
            keep.append(pool[2])  # 受影响方
    elif entity_type == "strategy":
        if "solves" not in outgoing_types:
            keep.append(pool[0])
        if not entity.get("description"):
            keep.append(pool[1])
        if "measures" not in {r.get("type") for r in relations
                              if isinstance(r, dict) and r.get("to") == entity_id}:
            keep.append(pool[2])
    elif entity_type == "rule":
        if not entity.get("platform") and not entity.get("description"):
            keep.append(pool[0])
        if not entity.get("penalty"):
            keep.append(pool[1])
        if "enforces" not in outgoing_types:
            keep.append(pool[2])
    elif entity_type == "metric":
        if not entity.get("value") and not entity.get("calculationMethod"):
            keep.append(pool[0])
        if "measures" not in outgoing_types:
            keep.append(pool[1])
        if not entity.get("benchmarkContext"):
            keep.append(pool[2])
    elif entity_type == "practice":
        if not entity.get("frequency"):
            keep.append(pool[0])
        # Practice supports strategy via reverse `requires` (strategy -> practice)
        incoming_requires = any(
            isinstance(r, dict) and r.get("type") == "requires" and r.get("to") == entity_id
            for r in relations
        )
        if not incoming_requires:
            keep.append(pool[1])
        if not entity.get("successMetric"):
            keep.append(pool[2])
    elif entity_type == "pitfall":
        if "causes" not in outgoing_types:
            keep.append(pool[0])
        if not entity.get("avoidanceStrategy"):
            keep.append(pool[1])
        if not entity.get("realCase"):
            keep.append(pool[2])

    return keep


def populate_self_check(
    blueprint: dict[str, Any],
    overwrite: bool = False,
) -> dict[str, Any]:
    """Walk the knowledge block and populate ``_selfCheck`` for entities that
    don't already have one. Returns the blueprint (mutated in place).

    If ``overwrite`` is True, existing _selfCheck is replaced.
    """
    library = blueprint.get("library", {}) or {}
    knowledge = library.get("knowledge", {}) or {}
    relations = blueprint.get("relations", []) or []

    if not isinstance(knowledge, dict):
        return blueprint

    for entities in knowledge.values():
        if not isinstance(entities, list):
            continue
        for entity in entities:
            if not isinstance(entity, dict):
                continue
            if entity.get("_selfCheck") and not overwrite:
                continue
            questions = derive_questions(entity, relations)
            entity["_selfCheck"] = {
                "passed": [],
                "questions": questions,
            }
    return blueprint
