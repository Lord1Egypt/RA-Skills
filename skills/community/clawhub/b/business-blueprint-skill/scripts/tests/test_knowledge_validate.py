"""Tests for the v2 knowledge extension validator (knowledge_validate.py)."""
from business_blueprint.validate import validate_blueprint


def _make_minimal_dk_blueprint() -> dict:
    """Minimal valid domain-knowledge blueprint."""
    return {
        "version": "1.0",
        "meta": {
            "blueprintType": "domain-knowledge",
            "detectedIntent": "用户想要跨境电商领域 know-how",
        },
        "context": {
            "clarifyRequests": [
                {
                    "id": f"clr-00{i}",
                    "targetEntityId": "pain-001",
                    "question": f"q{i}",
                }
                for i in range(1, 4)
            ],
            "clarifications": [],
        },
        "library": {
            "capabilities": [],
            "actors": [],
            "flowSteps": [],
            "systems": [],
            "knowledge": {
                "painPoints": [
                    {
                        "id": "pain-001",
                        "name": "ROI 不稳",
                        "entityType": "painPoint",
                    }
                ],
                "strategies": [],
                "rules": [],
                "metrics": [],
                "practices": [],
                "pitfalls": [],
            },
        },
        "relations": [],
        "views": [],
        "editor": {},
        "artifacts": {},
    }


def _errors(result: dict) -> list[dict]:
    return [i for i in result["issues"] if i["severity"] == "error"]


def _warnings(result: dict) -> list[dict]:
    return [i for i in result["issues"] if i["severity"] == "warning"]


def _codes(issues: list[dict]) -> set[str]:
    return {i["errorCode"] for i in issues}


def test_minimal_dk_blueprint_passes():
    bp = _make_minimal_dk_blueprint()
    result = validate_blueprint(bp)
    errs = _errors(result)
    assert not errs, f"unexpected errors: {errs}"


def test_invalid_blueprint_type():
    bp = _make_minimal_dk_blueprint()
    bp["meta"]["blueprintType"] = "totally-bogus"
    result = validate_blueprint(bp)
    assert "INVALID_BLUEPRINT_TYPE" in _codes(_errors(result))


def test_dk_missing_intent():
    bp = _make_minimal_dk_blueprint()
    bp["meta"]["detectedIntent"] = ""
    result = validate_blueprint(bp)
    assert "MISSING_DETECTED_INTENT" in _codes(_errors(result))


def test_architecture_blueprint_unchanged_passes():
    """Backward compat: bare architecture blueprint with no v2 fields."""
    bp = {
        "version": "1.0",
        "meta": {"title": "Existing", "industry": "retail"},
        "context": {},
        "library": {
            "capabilities": [
                {"id": "cap-001", "name": "Order", "level": 1},
            ],
            "actors": [],
            "flowSteps": [],
            "systems": [],
        },
        "relations": [],
        "views": [],
        "editor": {},
        "artifacts": {},
    }
    result = validate_blueprint(bp)
    # No v2-specific errors
    codes = _codes(_errors(result))
    assert "INVALID_BLUEPRINT_TYPE" not in codes
    assert "MISSING_DETECTED_INTENT" not in codes
    assert "DOMAIN_KNOWLEDGE_EMPTY" not in codes


def test_architecture_with_knowledge_errors():
    bp = _make_minimal_dk_blueprint()
    bp["meta"]["blueprintType"] = "architecture"
    bp["meta"]["detectedIntent"] = ""
    result = validate_blueprint(bp)
    assert "ARCHITECTURE_WITH_KNOWLEDGE" in _codes(_errors(result))


def test_dk_empty_knowledge_block():
    bp = _make_minimal_dk_blueprint()
    bp["library"]["knowledge"] = {
        "painPoints": [],
        "strategies": [],
        "rules": [],
        "metrics": [],
        "practices": [],
        "pitfalls": [],
    }
    bp["context"]["clarifyRequests"] = []  # also empty - knowledge is empty
    result = validate_blueprint(bp)
    assert "DOMAIN_KNOWLEDGE_EMPTY" in _codes(_errors(result))


def test_knowledge_missing_core_fields():
    bp = _make_minimal_dk_blueprint()
    bp["library"]["knowledge"]["painPoints"] = [
        # Missing name and entityType
        {"id": "pain-001"}
    ]
    result = validate_blueprint(bp)
    codes = _codes(_errors(result))
    assert "KNOWLEDGE_MISSING_NAME" in codes
    assert "KNOWLEDGE_MISSING_ENTITYTYPE" in codes


def test_knowledge_duplicate_id():
    bp = _make_minimal_dk_blueprint()
    bp["library"]["knowledge"]["painPoints"].append(
        {"id": "pain-001", "name": "Other", "entityType": "painPoint"}
    )
    result = validate_blueprint(bp)
    assert "KNOWLEDGE_DUPLICATE_ID" in _codes(_errors(result))


def test_user_defined_fields_allowed():
    bp = _make_minimal_dk_blueprint()
    bp["library"]["knowledge"]["painPoints"][0]["customField"] = "anything"
    bp["library"]["knowledge"]["painPoints"][0]["nestedJunk"] = {
        "any": {"thing": "ok"}
    }
    result = validate_blueprint(bp)
    assert not _errors(result)


def test_relation_missing_from_id():
    bp = _make_minimal_dk_blueprint()
    bp["relations"] = [
        {"id": "rel-001", "type": "solves", "from": "ghost", "to": "pain-001"}
    ]
    result = validate_blueprint(bp)
    assert "RELATION_MISSING_FROM" in _codes(_errors(result))


def test_relation_missing_to_id():
    bp = _make_minimal_dk_blueprint()
    bp["relations"] = [
        {"id": "rel-001", "type": "solves", "from": "pain-001", "to": "ghost"}
    ]
    result = validate_blueprint(bp)
    assert "RELATION_MISSING_TO" in _codes(_errors(result))


def test_unknown_relation_type_is_warning():
    bp = _make_minimal_dk_blueprint()
    bp["relations"] = [
        {
            "id": "rel-001",
            "type": "totally_made_up",
            "from": "pain-001",
            "to": "pain-001",
        }
    ]
    result = validate_blueprint(bp)
    assert "RELATION_UNKNOWN_TYPE" in _codes(_warnings(result))


def test_clarify_requests_insufficient_count():
    bp = _make_minimal_dk_blueprint()
    bp["context"]["clarifyRequests"] = bp["context"]["clarifyRequests"][:1]
    result = validate_blueprint(bp)
    assert "CLARIFY_REQUESTS_INSUFFICIENT" in _codes(_errors(result))


def test_clarify_request_invalid_target_entity():
    bp = _make_minimal_dk_blueprint()
    bp["context"]["clarifyRequests"][0]["targetEntityId"] = "ghost-id"
    result = validate_blueprint(bp)
    assert "CLARIFY_REQUEST_INVALID_TARGET" in _codes(_errors(result))


def test_clarify_request_missing_target():
    bp = _make_minimal_dk_blueprint()
    bp["context"]["clarifyRequests"][0].pop("targetEntityId")
    result = validate_blueprint(bp)
    assert "CLARIFY_REQUEST_MISSING_TARGET" in _codes(_errors(result))


def test_architecture_no_clarify_required():
    """Architecture blueprints don't trigger clarifyRequests >= 3 rule."""
    bp = {
        "version": "1.0",
        "meta": {"title": "Test", "industry": "retail"},
        "context": {"clarifyRequests": []},
        "library": {
            "capabilities": [{"id": "cap-001", "name": "X", "level": 1}],
            "actors": [],
            "flowSteps": [],
            "systems": [],
        },
        "relations": [],
        "views": [],
        "editor": {},
        "artifacts": {},
    }
    result = validate_blueprint(bp)
    assert "CLARIFY_REQUESTS_INSUFFICIENT" not in _codes(_errors(result))
