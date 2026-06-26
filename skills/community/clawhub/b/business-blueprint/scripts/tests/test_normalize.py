from business_blueprint.normalize import normalize_system_name
from business_blueprint.clarify import build_clarify_requests
from business_blueprint.normalize import merge_or_create_system


def test_normalize_system_name_maps_known_aliases() -> None:
    assert normalize_system_name("Salesforce CRM") == "CRM"
    assert normalize_system_name("企微") == "企业微信"


def test_merge_or_create_system_uses_alias_match() -> None:
    systems = [
        {
            "id": "sys-crm",
            "kind": "system",
            "name": "Salesforce",
            "aliases": [],
            "resolution": {"status": "canonical", "canonicalName": "CRM"},
        }
    ]

    merged = merge_or_create_system(
        systems,
        raw_name="CRM",
        description="customer platform",
    )

    assert merged["id"] == "sys-crm"
    assert len(systems) == 1
    assert "CRM" in merged["aliases"]


def test_build_clarify_requests_flags_ambiguous_systems() -> None:
    blueprint = {
        "context": {},
        "library": {
            "systems": [
                {
                    "id": "sys-1",
                    "name": "ERP",
                    "resolution": {"status": "ambiguous", "canonicalName": "ERP"},
                }
            ]
        },
    }

    requests = build_clarify_requests(blueprint)

    assert requests[0]["code"] == "AMBIGUOUS_SYSTEM"
    assert requests[0]["affectedIds"] == ["sys-1"]
