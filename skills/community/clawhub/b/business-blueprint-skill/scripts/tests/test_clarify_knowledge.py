"""Tests for the v2 knowledge-style clarifyRequests builder in clarify.py."""
from business_blueprint.clarify import (
    build_architecture_clarify_requests,
    build_clarify_requests,
    build_knowledge_clarify_requests,
)


def _knowledge_blueprint(painpoints=None, strategies=None, pitfalls=None, relations=None):
    return {
        "meta": {
            "blueprintType": "domain-knowledge",
            "detectedIntent": "test",
        },
        "library": {
            "capabilities": [],
            "actors": [],
            "flowSteps": [],
            "systems": [],
            "knowledge": {
                "painPoints": painpoints or [],
                "strategies": strategies or [],
                "rules": [],
                "metrics": [],
                "practices": [],
                "pitfalls": pitfalls or [],
            },
        },
        "relations": relations or [],
    }


def test_dispatcher_picks_knowledge_when_dk_blueprint():
    bp = _knowledge_blueprint(
        painpoints=[
            {"id": "pain-001", "name": "ROI 不稳", "entityType": "painPoint", "level": 1}
        ]
    )
    requests = build_clarify_requests(bp)
    # v2 knowledge-style requests have a targetEntityId field
    assert any("targetEntityId" in req for req in requests)


def test_dispatcher_uses_architecture_for_arch_blueprint():
    bp = {
        "meta": {"blueprintType": "architecture"},
        "library": {
            "capabilities": [],
            "actors": [],
            "flowSteps": [],
            "systems": [],
        },
    }
    requests = build_clarify_requests(bp)
    # Architecture-style uses 'code' / 'affectedIds'
    assert all("targetEntityId" not in req for req in requests)
    assert any("code" in req for req in requests)


def test_top_level_painpoint_triggers_root_cause_clarification():
    bp = _knowledge_blueprint(
        painpoints=[
            {"id": "pain-001", "name": "ROI 不稳", "entityType": "painPoint", "level": 1}
        ]
    )
    requests = build_knowledge_clarify_requests(bp)
    # Should include hierarchy/root-cause clarification for level=1 pain
    matching = [
        r for r in requests
        if r.get("targetEntityId") == "pain-001"
        and ("根因" in r.get("question", "") or "症状" in r.get("question", ""))
    ]
    assert matching


def test_strategy_without_solves_triggers_clarification():
    bp = _knowledge_blueprint(
        painpoints=[
            {"id": "pain-001", "name": "X", "entityType": "painPoint"}
        ],
        strategies=[
            {"id": "str-001", "name": "Y", "entityType": "strategy"}
        ],
    )
    requests = build_knowledge_clarify_requests(bp)
    matching = [
        r for r in requests
        if r.get("targetEntityId") == "str-001"
        and "痛点" in r.get("question", "")
    ]
    assert matching


def test_strategy_with_solves_skips_pain_question():
    bp = _knowledge_blueprint(
        painpoints=[
            {"id": "pain-001", "name": "X", "entityType": "painPoint"}
        ],
        strategies=[
            {"id": "str-001", "name": "Y", "entityType": "strategy"}
        ],
        relations=[
            {"id": "rel-001", "type": "solves", "from": "str-001", "to": "pain-001"}
        ],
    )
    requests = build_knowledge_clarify_requests(bp)
    # No "对应哪个痛点" question for str-001 since solves exists
    pain_questions = [
        r for r in requests
        if r.get("targetEntityId") == "str-001"
        and "对应哪个具体痛点" in r.get("question", "")
    ]
    assert not pain_questions


def test_pads_to_minimum_three_when_few_triggers():
    bp = _knowledge_blueprint(
        painpoints=[
            {"id": "pain-001", "name": "正常长度的痛点名称", "entityType": "painPoint"}
        ],
    )
    requests = build_knowledge_clarify_requests(bp)
    assert len(requests) >= 3, f"Expected >=3, got {len(requests)}: {requests}"


def test_each_request_has_unique_id():
    bp = _knowledge_blueprint(
        painpoints=[
            {"id": "pain-001", "name": "X", "entityType": "painPoint", "level": 1},
            {"id": "pain-002", "name": "Y", "entityType": "painPoint", "level": 1},
        ],
        strategies=[
            {"id": "str-001", "name": "Z", "entityType": "strategy"}
        ],
    )
    requests = build_knowledge_clarify_requests(bp)
    ids = [r["id"] for r in requests]
    assert len(ids) == len(set(ids)), f"duplicate ids: {ids}"


def test_short_name_triggers_granularity_clarification():
    bp = _knowledge_blueprint(
        painpoints=[
            {"id": "pain-001", "name": "X", "entityType": "painPoint"}
        ]
    )
    requests = build_knowledge_clarify_requests(bp)
    matching = [r for r in requests if "过短" in r.get("question", "")]
    assert matching


def test_architecture_clarify_back_compat():
    bp = {
        "library": {
            "capabilities": [],
            "actors": [],
            "flowSteps": [],
            "systems": [],
        }
    }
    requests = build_architecture_clarify_requests(bp)
    codes = {r["code"] for r in requests}
    assert "MISSING_PRIMARY_ACTOR" in codes
    assert "MISSING_CAPABILITY" in codes
