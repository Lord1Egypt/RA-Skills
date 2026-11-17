from __future__ import annotations

from typing import Any


SCHEMA_VERSION = "1.0.0"
REQUIRED_FIELDS = {
    "schema_version",
    "slide_id",
    "slide_role",
    "audience_question",
    "message",
    "evidence_refs",
    "priority",
    "primary_expression",
    "page_archetype",
    "semantic_component",
    "visual_anchor",
    "layout",
    "density",
    "editability",
    "delivery",
    "style_system",
    "forbidden_patterns",
    "qa_focus",
}


def validate_page_design_intent(document: dict[str, Any]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    if document.get("schema_version") != SCHEMA_VERSION:
        issues.append({"code": "INTENT_SCHEMA_VERSION_REQUIRED"})
    for field in sorted(REQUIRED_FIELDS - set(document)):
        issues.append({"code": f"INTENT_{field.upper()}_REQUIRED"})

    fallbacks = ((document.get("delivery") or {}).get("allowed_fallbacks") or [])
    if (
        (document.get("editability") or {}).get("message_bearing") == "native_required"
        and "generic_card" in fallbacks
    ):
        issues.append({"code": "INTENT_NATIVE_GENERIC_CARD_FORBIDDEN"})
    return issues
