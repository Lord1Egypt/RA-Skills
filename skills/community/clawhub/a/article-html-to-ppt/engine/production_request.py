"""Production request validation and content-aware page budgeting.

Page count is a user constraint, not a generator constant.  A narrative
planner supplies a content assessment; this module reconciles it with an
``auto``, ``target``, ``range`` or ``exact`` page contract without silently
cramming content or inventing filler.
"""
from __future__ import annotations

import json
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "v4" / "production-request.schema.json"


def _finding(code: str, path: str, message: str) -> dict:
    return {"code": code, "path": path, "message": message}


def validate_production_request(request: dict) -> list[dict]:
    """Return schema and semantic findings for a production request."""
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    errors = sorted(
        jsonschema.Draft202012Validator(schema).iter_errors(request),
        key=lambda item: list(item.path),
    )
    findings = [
        _finding("SCHEMA", "/" + "/".join(map(str, error.path)), error.message)
        for error in errors
    ]
    if findings:
        return findings

    contract = request["page_contract"]
    if contract["mode"] == "range" and contract["min_pages"] > contract["max_pages"]:
        findings.append(_finding(
            "PAGE_RANGE_INVALID", "/page_contract",
            "min_pages must be less than or equal to max_pages",
        ))
    return findings


def _declared_output_pages(page_contract: dict):
    mode = page_contract["mode"]
    if mode == "exact":
        return page_contract["exact_pages"]
    if mode == "target":
        return page_contract["target_pages"]
    if mode == "range":
        return {"min": page_contract["min_pages"], "max": page_contract["max_pages"]}
    return None


def prepare_template_context(request: dict, template_path: str | Path | None) -> dict:
    """Bind an uploaded template to a production request.

    The deterministic analyzer supplies raw evidence only.  It never turns
    the template slide count into an output page limit and never claims that
    geometry alone is a reviewed design language.
    """
    template_contract = request.get("template")
    if template_contract is None:
        return {"status": "not_requested"}
    if template_path is None:
        if template_contract.get("required"):
            return {"status": "rejected", "code": "TEMPLATE_REQUIRED_MISSING"}
        return {"status": "not_provided"}

    from .template_evidence import analyze_template  # local import avoids routing coupling

    evidence = analyze_template(template_path)
    declared_sha = template_contract["source_sha256"]
    actual_sha = evidence["source"]["sha256"]
    if declared_sha != actual_sha:
        return {
            "status": "rejected", "code": "TEMPLATE_SOURCE_HASH_MISMATCH",
            "declared_sha256": declared_sha, "actual_sha256": actual_sha,
        }

    preferred = template_contract.get("preferred_slide_indices", [])
    available = {slide["slide_index"] for slide in evidence["slides"]}
    unknown = sorted(set(preferred) - available)
    if unknown:
        return {
            "status": "rejected", "code": "TEMPLATE_SLIDE_UNKNOWN",
            "unknown_slide_indices": unknown,
        }

    use_mode = template_contract["use_mode"]
    policies = {
        "strict": {
            "reuse_master_and_brand_assets": True,
            "allow_new_compositions": False,
        },
        "style_transfer": {
            "reuse_master_and_brand_assets": False,
            "allow_new_compositions": True,
        },
        "inspiration": {
            "reuse_master_and_brand_assets": False,
            "allow_new_compositions": True,
        },
    }
    generation_policy = {
        "template_slide_count_limits_output": False,
        **policies[use_mode],
    }
    return {
        "status": "ready_for_visual_interpretation",
        "use_mode": use_mode,
        "required": bool(template_contract["required"]),
        "source": evidence["source"],
        "preferred_slide_indices": list(preferred),
        "requested_output_pages": _declared_output_pages(request["page_contract"]),
        "generation_policy": generation_policy,
        "review": evidence["review"],
        "evidence": evidence,
    }


def _assessment_bounds(assessment: dict) -> tuple[int, int, int]:
    minimum = int(assessment["minimum_viable_pages"])
    recommended = int(assessment["recommended_pages"])
    maximum = int(assessment["maximum_useful_pages"])
    if minimum < 1 or not minimum <= recommended <= maximum:
        raise ValueError("content assessment must satisfy 1 <= minimum <= recommended <= maximum")
    return minimum, recommended, maximum


def _overflow_conflict(minimum: int, maximum: int, requested: int) -> dict:
    return {
        "status": "conflict",
        "code": "PAGE_CONTRACT_CONTENT_OVERFLOW",
        "planned_pages": None,
        "requested_pages": requested,
        "hard_min": minimum,
        "hard_max": maximum,
        "alternatives": ["increase_pages", "appendix", "split_deck", "reduce_scope"],
    }


def _underflow_conflict(minimum: int, maximum: int, requested: int) -> dict:
    return {
        "status": "conflict",
        "code": "PAGE_CONTRACT_CONTENT_UNDERFLOW",
        "planned_pages": None,
        "requested_pages": requested,
        "hard_min": minimum,
        "hard_max": maximum,
        "alternatives": ["fewer_pages", "request_more_source_material"],
    }


def resolve_page_budget(page_contract: dict, content_assessment: dict) -> dict:
    """Reconcile a user page contract with a narrative content assessment.

    ``minimum_viable_pages`` is the smallest readable deck that retains all
    mandatory claims. ``maximum_useful_pages`` is the largest deck supported
    by the supplied material without filler. The function never fabricates
    content and never silently drops mandatory material.
    """
    minimum, recommended, maximum = _assessment_bounds(content_assessment)
    mode = page_contract["mode"]

    if mode == "auto":
        return {
            "status": "accepted", "planned_pages": recommended,
            "hard_min": minimum, "hard_max": maximum,
            "reason": "content_recommendation",
        }

    if mode == "exact":
        requested = int(page_contract["exact_pages"])
        if requested < minimum:
            return _overflow_conflict(minimum, maximum, requested)
        if requested > maximum:
            return _underflow_conflict(minimum, maximum, requested)
        return {
            "status": "accepted", "planned_pages": requested,
            "requested_pages": requested, "hard_min": requested,
            "hard_max": requested, "reason": "user_exact",
        }

    if mode == "range":
        requested_min = int(page_contract["min_pages"])
        requested_max = int(page_contract["max_pages"])
        if requested_max < minimum:
            return _overflow_conflict(minimum, maximum, requested_max)
        if requested_min > maximum:
            return _underflow_conflict(minimum, maximum, requested_min)
        hard_min = max(minimum, requested_min)
        hard_max = min(maximum, requested_max)
        planned = min(max(recommended, hard_min), hard_max)
        return {
            "status": "accepted", "planned_pages": planned,
            "hard_min": hard_min, "hard_max": hard_max,
            "reason": "content_recommendation_within_user_range",
        }

    if mode == "target":
        requested = int(page_contract["target_pages"])
        tolerance = int(page_contract.get("tolerance_pages", 0))
        preferred_min = max(1, requested - tolerance)
        preferred_max = requested + tolerance
        if preferred_max < minimum:
            return {
                "status": "accepted_with_adjustment",
                "code": "PAGE_TARGET_BELOW_CONTENT_MINIMUM",
                "planned_pages": minimum, "requested_pages": requested,
                "hard_min": minimum, "hard_max": maximum,
                "reason": "preserve_mandatory_content",
            }
        if preferred_min > maximum:
            return {
                "status": "accepted_with_adjustment",
                "code": "PAGE_TARGET_ABOVE_USEFUL_MAXIMUM",
                "planned_pages": maximum, "requested_pages": requested,
                "hard_min": minimum, "hard_max": maximum,
                "reason": "avoid_invented_filler",
            }
        preferred_min = max(preferred_min, minimum)
        preferred_max = min(preferred_max, maximum)
        planned = min(max(recommended, preferred_min), preferred_max)
        return {
            "status": "accepted", "planned_pages": planned,
            "requested_pages": requested, "hard_min": minimum,
            "hard_max": maximum, "reason": "user_target_with_tolerance",
        }

    raise ValueError(f"unsupported page contract mode: {mode}")
