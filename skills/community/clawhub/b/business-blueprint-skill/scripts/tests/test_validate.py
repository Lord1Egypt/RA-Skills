from business_blueprint.validate import validate_blueprint


def test_validate_reports_duplicate_ids() -> None:
    blueprint = {
        "version": "1.0",
        "meta": {"revisionId": "r1"},
        "context": {},
        "library": {
            "capabilities": [
                {"id": "cap-order", "name": "Order"},
                {"id": "cap-order", "name": "Order Duplicate"},
            ],
            "flowSteps": [],
            "systems": [],
        },
        "relations": [],
        "views": [],
        "editor": {},
        "artifacts": {},
    }

    result = validate_blueprint(blueprint)

    assert any(issue["errorCode"] == "DUPLICATE_ID" for issue in result["issues"])


def test_validate_reports_unmapped_first_party_system() -> None:
    blueprint = {
        "version": "1.0",
        "meta": {"revisionId": "r1"},
        "context": {},
        "library": {
            "capabilities": [{"id": "cap-order", "name": "Order"}],
            "flowSteps": [],
            "systems": [
                {
                    "id": "sys-crm",
                    "name": "CRM",
                    "category": "business-app",
                    "supportOnly": False,
                }
            ],
        },
        "relations": [],
        "views": [
            {
                "id": "view-arch",
                "type": "application-architecture",
                "includedNodeIds": ["sys-crm"],
                "includedRelationIds": [],
                "layout": {},
                "annotations": [],
            }
        ],
        "editor": {},
        "artifacts": {},
    }

    result = validate_blueprint(blueprint)

    assert any(issue["errorCode"] == "UNMAPPED_SYSTEM" for issue in result["issues"])


def test_validate_reports_orphan_capability() -> None:
    blueprint = {
        "version": "1.0",
        "meta": {"revisionId": "r1"},
        "context": {},
        "library": {
            "capabilities": [{"id": "cap-membership", "name": "会员运营"}],
            "actors": [],
            "flowSteps": [],
            "systems": [],
        },
        "relations": [],
        "views": [],
        "editor": {},
        "artifacts": {},
    }

    result = validate_blueprint(blueprint)

    assert any(issue["errorCode"] == "ORPHAN_CAPABILITY" for issue in result["issues"])
    assert result["summary"]["orphan_capability_count"] == 1
    assert result["summary"]["orphan_capability_ids"] == ["cap-membership"]


def test_validate_reports_flow_step_missing_actor() -> None:
    blueprint = {
        "version": "1.0",
        "meta": {"revisionId": "r1"},
        "context": {},
        "library": {
            "capabilities": [{"id": "cap-order", "name": "订单管理"}],
            "actors": [],
            "flowSteps": [
                {
                    "id": "flow-order-create",
                    "name": "订单创建",
                    "capabilityIds": ["cap-order"],
                    "systemIds": [],
                }
            ],
            "systems": [],
        },
        "relations": [],
        "views": [],
        "editor": {},
        "artifacts": {},
    }

    result = validate_blueprint(blueprint)

    assert any(issue["errorCode"] == "FLOW_STEP_MISSING_ACTOR" for issue in result["issues"])
    assert result["summary"]["flow_step_missing_actor_count"] == 1
    assert result["summary"]["flow_step_missing_actor_ids"] == ["flow-order-create"]


def test_validate_reports_capability_missing_from_map_and_no_shared_linkage() -> None:
    blueprint = {
        "version": "1.0",
        "meta": {"revisionId": "r1"},
        "context": {},
        "library": {
            "capabilities": [
                {"id": "cap-flow", "name": "Flow Capability"},
                {"id": "cap-system", "name": "System Capability"},
            ],
            "actors": [{"id": "actor-service", "name": "客服"}],
            "flowSteps": [
                {
                    "id": "flow-1",
                    "name": "流程步骤",
                    "actorId": "actor-service",
                    "capabilityIds": ["cap-flow"],
                    "systemIds": [],
                }
            ],
            "systems": [
                {
                    "id": "sys-1",
                    "name": "系统A",
                    "category": "business-app",
                    "capabilityIds": ["cap-system"],
                }
            ],
        },
        "relations": [],
        "views": [
            {
                "id": "view-capability",
                "type": "business-capability-map",
                "includedNodeIds": [],
                "includedRelationIds": [],
                "layout": {},
                "annotations": [],
            }
        ],
        "editor": {},
        "artifacts": {},
    }

    result = validate_blueprint(blueprint)

    assert any(issue["errorCode"] == "CAPABILITY_MISSING_FROM_MAP" for issue in result["issues"])
    assert any(issue["errorCode"] == "NO_SHARED_CAPABILITY_LINKAGE" for issue in result["issues"])


def test_validate_ignores_malformed_capability_entries() -> None:
    blueprint = {
        "version": "1.0",
        "meta": {"revisionId": "r1"},
        "context": {},
        "library": {
            "capabilities": ["bad-entry", {"name": "missing-id"}, {"id": "cap-good", "name": "Good"}],
            "actors": [],
            "flowSteps": [],
            "systems": [],
        },
        "relations": [],
        "views": [],
        "editor": {},
        "artifacts": {},
    }

    result = validate_blueprint(blueprint)

    assert result["summary"]["warningCount"] >= 1
