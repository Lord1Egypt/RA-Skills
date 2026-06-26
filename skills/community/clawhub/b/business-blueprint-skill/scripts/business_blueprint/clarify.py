"""Build clarifyRequests for blueprints.

Two output styles coexist:

1. Legacy architecture style (used by the existing pipeline):
   {"code": "...", "question": "...", "affectedIds": [...]}

2. v2 domain-knowledge style (required by knowledge_validate):
   {"id": "clr-001", "targetEntityId": "pain-001", "question": "...",
    "rationale": "...", "options": [...optional]}

The dispatcher reads ``meta.blueprintType`` and emits whichever style fits.
"""
from __future__ import annotations

from typing import Any

from knowledge_self_check import SELF_CHECK_QUESTIONS


def build_clarify_requests(blueprint: dict[str, Any]) -> list[dict[str, Any]]:
    bp_type = (blueprint.get("meta") or {}).get("blueprintType", "architecture")
    if bp_type == "domain-knowledge":
        return build_knowledge_clarify_requests(blueprint)
    return build_architecture_clarify_requests(blueprint)


def build_architecture_clarify_requests(blueprint: dict[str, Any]) -> list[dict[str, Any]]:
    """Original architecture-style clarify generation (preserved for back-compat)."""
    requests: list[dict[str, Any]] = []
    library = blueprint.get("library", {})

    for system in library.get("systems", []):
        if system.get("resolution", {}).get("status") == "ambiguous":
            requests.append(
                {
                    "code": "AMBIGUOUS_SYSTEM",
                    "question": f"Please clarify whether '{system.get('name', '')}' refers to an existing canonical system or a distinct system.",
                    "affectedIds": [system["id"]],
                }
            )

    if not library.get("actors"):
        requests.append(
            {
                "code": "MISSING_PRIMARY_ACTOR",
                "question": "Which primary business actors should appear in the solution?",
                "affectedIds": [],
            }
        )

    if not library.get("capabilities"):
        requests.append(
            {
                "code": "MISSING_CAPABILITY",
                "question": "Which business capabilities must be represented in the blueprint?",
                "affectedIds": [],
            }
        )

    if library.get("capabilities") and not library.get("flowSteps"):
        requests.append(
            {
                "code": "MISSING_MAIN_FLOW",
                "question": "What is the main business flow that should be represented?",
                "affectedIds": [],
            }
        )

    if not library.get("systems"):
        requests.append(
            {
                "code": "MISSING_SYSTEM",
                "question": "Which existing or target systems should appear in the architecture?",
                "affectedIds": [],
            }
        )

    return requests


def build_knowledge_clarify_requests(blueprint: dict[str, Any]) -> list[dict[str, Any]]:
    """Generate v2 domain-knowledge clarifyRequests.

    Trigger priority (see design v2 §IV.1):
    1. Hierarchy ambiguity — top-level (level=1) painPoint or strategy
    2. Missing relations — strategy without ``solves``; pitfall without ``causes``
    3. Missing metrics — strategy without an incoming ``measures``
    4. Granularity suspicious — entity name is too short or too long
    5. Backfill — pad to 3 with generic questions on extant entities

    Each request has a unique id and points to a real entity.
    """
    requests: list[dict[str, Any]] = []
    library = blueprint.get("library", {}) or {}
    knowledge = library.get("knowledge", {}) or {}
    if not isinstance(knowledge, dict):
        return requests
    relations = blueprint.get("relations", []) or []

    pain_points = knowledge.get("painPoints", []) or []
    strategies = knowledge.get("strategies", []) or []
    pitfalls = knowledge.get("pitfalls", []) or []

    seq = [0]

    def _next_id() -> str:
        seq[0] += 1
        return f"clr-{seq[0]:03d}"

    # 1. Hierarchy ambiguity for level=1 painPoints
    for pain in pain_points:
        if not isinstance(pain, dict):
            continue
        if pain.get("level") == 1:
            requests.append({
                "id": _next_id(),
                "targetEntityId": pain.get("id"),
                "question": (
                    f"我把 '{pain.get('name', '')}' 识别为顶层痛点（level=1），"
                    "但这是症状还是根因？如果是症状，根因可能是什么？"
                ),
                "options": ["症状 - 根因待补充", "根因 - 已是最深层"],
                "rationale": "顶层痛点应是根因；如果是症状，建议追溯到根因后重新分层。",
            })

    # 2. strategy without outgoing solves
    strategies_with_solves = {
        rel.get("from") for rel in relations
        if isinstance(rel, dict) and rel.get("type") == "solves"
    }
    for strategy in strategies:
        if not isinstance(strategy, dict):
            continue
        sid = strategy.get("id")
        if sid and sid not in strategies_with_solves:
            requests.append({
                "id": _next_id(),
                "targetEntityId": sid,
                "question": (
                    f"策略 '{strategy.get('name', '')}' 对应哪个具体痛点？"
                    "请选择或补充。"
                ),
                "rationale": "策略必须明确解决某个痛点（建立 solves 关系），否则容易变成空泛口号。",
            })

    # 3. strategy without incoming measures
    strategies_with_measures = {
        rel.get("to") for rel in relations
        if isinstance(rel, dict) and rel.get("type") == "measures"
    }
    for strategy in strategies:
        if not isinstance(strategy, dict):
            continue
        sid = strategy.get("id")
        if sid and sid not in strategies_with_measures:
            requests.append({
                "id": _next_id(),
                "targetEntityId": sid,
                "question": (
                    f"策略 '{strategy.get('name', '')}' 怎么衡量是否有效？"
                    "需要对应一个 metric（建立 measures 关系）。"
                ),
                "rationale": "无指标的策略无法判定是否成功，建议明确衡量标准。",
            })

    # 4. pitfall without causes
    pitfalls_with_causes = {
        rel.get("from") for rel in relations
        if isinstance(rel, dict) and rel.get("type") == "causes"
    }
    for pitfall in pitfalls:
        if not isinstance(pitfall, dict):
            continue
        pid = pitfall.get("id")
        if pid and pid not in pitfalls_with_causes:
            requests.append({
                "id": _next_id(),
                "targetEntityId": pid,
                "question": (
                    f"误区 '{pitfall.get('name', '')}' 会导致什么具体痛点？"
                    "建议建立 causes 关系。"
                ),
                "rationale": "脱钩痛点的误区会变成抽象警告，难以驱动行动。",
            })

    # 5. Granularity suspicious
    for entity_type, entities in knowledge.items():
        if not isinstance(entities, list):
            continue
        for entity in entities:
            if not isinstance(entity, dict):
                continue
            name = entity.get("name", "")
            if not isinstance(name, str):
                continue
            if 0 < len(name) < 4:
                requests.append({
                    "id": _next_id(),
                    "targetEntityId": entity.get("id"),
                    "question": (
                        f"实体 '{name}' 名称过短（{len(name)} 字），是否需要更具体的命名？"
                    ),
                    "rationale": "过短名称容易歧义，建议至少 4 字承载业务含义。",
                })
            elif len(name) > 30:
                requests.append({
                    "id": _next_id(),
                    "targetEntityId": entity.get("id"),
                    "question": (
                        f"实体 '{name}' 名称过长（{len(name)} 字），"
                        "是否需要拆分或精简？"
                    ),
                    "rationale": "过长名称通常含多重概念，建议拆分。",
                })

    # 5. Pad to >=3 if we somehow under-shot. Fallback: cycle through
    # self-check question pools across all entities until the threshold is met.
    if len(requests) < 3:
        candidates: list[tuple[dict[str, Any], str]] = []
        for entities in knowledge.values():
            if not isinstance(entities, list):
                continue
            for entity in entities:
                if not isinstance(entity, dict):
                    continue
                ent_type = entity.get("entityType")
                if ent_type not in SELF_CHECK_QUESTIONS:
                    continue
                for question in SELF_CHECK_QUESTIONS[ent_type]:
                    candidates.append((entity, question))

        already_keyed = {
            (req.get("targetEntityId"), req.get("question"))
            for req in requests
        }
        for entity, question in candidates:
            if len(requests) >= 3:
                break
            wrapped = f"针对 '{entity.get('name', '')}'：{question}"
            key = (entity.get("id"), wrapped)
            if key in already_keyed:
                continue
            requests.append({
                "id": _next_id(),
                "targetEntityId": entity.get("id"),
                "question": wrapped,
                "rationale": "padding 至最低 3 条澄清以满足 v2 强制要求。",
            })
            already_keyed.add(key)

    return requests
