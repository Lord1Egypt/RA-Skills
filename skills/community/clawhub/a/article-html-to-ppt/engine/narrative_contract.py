"""Validation for non-prescriptive Bespoke narrative quality contracts."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "v4" / "narrative-contract.schema.json"


PRESCRIPTIVE_FIELDS = {
    "composition",
    "coordinates",
    "geometry",
    "layout",
    "page_archetype",
    "template_slide_index",
}


def _find_prescriptive_fields(value, path: str = "") -> list[dict]:
    findings: list[dict] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}/{key}"
            if key in PRESCRIPTIVE_FIELDS:
                findings.append({
                    "code": "NARRATIVE_PRESCRIPTIVE_FIELD",
                    "path": child_path,
                    "message": (
                        f"{key} belongs to the high-capability visual author, "
                        "not the narrative quality contract"
                    ),
                })
            findings.extend(_find_prescriptive_fields(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            findings.extend(_find_prescriptive_fields(child, f"{path}/{index}"))
    return findings


def _chapter_sequence_finding(contract: dict, ir: dict) -> list[dict]:
    chapters = contract.get("chapters")
    slides = ir.get("slides")
    if not isinstance(chapters, list) or not isinstance(slides, list):
        return []
    chapter_slide_ids = [
        slide_id
        for chapter in chapters
        if isinstance(chapter, dict) and isinstance(chapter.get("slide_ids"), list)
        for slide_id in chapter["slide_ids"]
    ]
    ir_slide_ids = [
        slide.get("id") for slide in slides if isinstance(slide, dict)
    ]
    if chapter_slide_ids == ir_slide_ids:
        return []
    return [{
        "code": "NARRATIVE_CHAPTER_SEQUENCE_MISMATCH",
        "path": "/chapters",
        "message": "chapters must partition every IR slide exactly once and preserve story order",
    }]


def _evidence_ref_findings(contract: dict, ir: dict) -> list[dict]:
    pages = contract.get("pages")
    slides = ir.get("slides")
    if not isinstance(pages, list) or not isinstance(slides, list):
        return []
    known_blocks = {
        str(slide.get("id")): {
            str(block.get("id"))
            for block in slide.get("blocks", [])
            if isinstance(block, dict) and block.get("id")
        }
        for slide in slides
        if isinstance(slide, dict) and slide.get("id")
    }
    findings: list[dict] = []
    for page_index, page in enumerate(pages):
        if not isinstance(page, dict):
            continue
        slide_id = page.get("slide_id")
        refs = page.get("evidence_refs")
        if not isinstance(slide_id, str) or not isinstance(refs, list):
            continue
        for ref_index, ref in enumerate(refs):
            parts = ref.split(":") if isinstance(ref, str) else []
            if (
                len(parts) != 3
                or parts[0] != "block"
                or parts[1] != slide_id
                or parts[2] not in known_blocks.get(slide_id, set())
            ):
                findings.append({
                    "code": "NARRATIVE_EVIDENCE_REF_UNKNOWN",
                    "path": f"/pages/{page_index}/evidence_refs/{ref_index}",
                    "message": "evidence reference must resolve to a block on the same IR slide",
                })
    return findings


def _page_sequence_finding(contract: dict, ir: dict) -> list[dict]:
    pages = contract.get("pages")
    slides = ir.get("slides")
    if not isinstance(pages, list) or not isinstance(slides, list):
        return []
    page_slide_ids = [
        page.get("slide_id") for page in pages if isinstance(page, dict)
    ]
    ir_slide_ids = [
        slide.get("id") for slide in slides if isinstance(slide, dict)
    ]
    if page_slide_ids == ir_slide_ids:
        return []
    return [{
        "code": "NARRATIVE_PAGE_SEQUENCE_MISMATCH",
        "path": "/pages",
        "message": "narrative pages must cover every IR slide exactly once and preserve story order",
    }]


def _assertion_ref_findings(contract: dict) -> list[dict]:
    pages = contract.get("pages")
    if not isinstance(pages, list):
        return []
    findings: list[dict] = []
    for index, page in enumerate(pages):
        if not isinstance(page, dict) or not isinstance(page.get("slide_id"), str):
            continue
        expected = f"slide:{page['slide_id']}:message"
        if page.get("assertion_ref") != expected:
            findings.append({
                "code": "NARRATIVE_ASSERTION_REF_MISMATCH",
                "path": f"/pages/{index}/assertion_ref",
                "message": "assertion_ref must point to the message of the same IR slide",
            })
    return findings


def _transition_findings(contract: dict) -> list[dict]:
    pages = contract.get("pages")
    if not isinstance(pages, list):
        return []
    findings: list[dict] = []
    for index, page in enumerate(pages[:-1]):
        if not isinstance(page, dict):
            continue
        transition = page.get("transition_to_next")
        if not isinstance(transition, str) or not transition.strip():
            findings.append({
                "code": "NARRATIVE_TRANSITION_REQUIRED",
                "path": f"/pages/{index}/transition_to_next",
                "message": "every nonfinal page must state how it advances to the next page",
            })
    return findings


def validate_narrative_contract(contract: dict, ir: dict) -> list[dict]:
    """Return findings without selecting layouts or rewriting narrative choices."""
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    schema_errors = sorted(
        jsonschema.Draft202012Validator(schema).iter_errors(contract),
        key=lambda item: list(item.path),
    )
    findings: list[dict] = []
    for error in schema_errors:
        path = list(error.path)
        if error.validator == "required" and isinstance(error.instance, dict):
            missing = next(
                (key for key in error.validator_value if key not in error.instance),
                None,
            )
            if missing is not None:
                path.append(missing)
        findings.append({
            "code": "NARRATIVE_SCHEMA",
            "path": "/" + "/".join(map(str, path)),
            "message": error.message,
        })
    findings.extend(_find_prescriptive_fields(contract))
    findings.extend(_chapter_sequence_finding(contract, ir))
    findings.extend(_page_sequence_finding(contract, ir))
    findings.extend(_assertion_ref_findings(contract))
    findings.extend(_transition_findings(contract))
    findings.extend(_evidence_ref_findings(contract, ir))
    raw = json.dumps(ir, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    expected_sha = "sha256:" + hashlib.sha256(raw.encode("utf-8")).hexdigest()
    if contract.get("source_ir_sha256") != expected_sha:
        findings.append({
            "code": "NARRATIVE_SOURCE_IR_MISMATCH",
            "path": "/source_ir_sha256",
            "message": "narrative contract must bind the exact source IR",
        })
    return findings
