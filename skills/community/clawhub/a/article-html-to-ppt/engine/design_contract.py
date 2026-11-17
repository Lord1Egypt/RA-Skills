"""Validation of source-bound, review-gated page Design Contracts.

This module deliberately does not render or route pages. It verifies that a
reviewer may only select existing IR content and source-matched template
Evidence; it cannot introduce narrative text, metrics or template identity.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "v4" / "design-contract.schema.json"


def _finding(code: str, path: str, message: str) -> dict:
    return {"code": code, "path": path, "message": message}


def _schema_findings(contract: dict) -> list[dict]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    errors = sorted(jsonschema.Draft202012Validator(schema).iter_errors(contract), key=lambda item: list(item.path))
    return [_finding("SCHEMA", "/" + "/".join(map(str, error.path)), error.message) for error in errors]


def _slide_index(ir: dict) -> dict[str, dict]:
    return {slide.get("id"): slide for slide in ir.get("slides", []) if slide.get("id")}


def _ref_exists(ref: dict, slide: dict) -> bool:
    kind = ref["kind"]
    if kind == "slide_message":
        return bool(slide.get("message"))
    if kind == "slide_title":
        return bool(slide.get("title"))
    if kind == "chart":
        return isinstance(slide.get("chart"), dict)
    if kind == "diagram_ir":
        return isinstance(slide.get("diagram_ir"), dict)
    if kind == "block":
        return any(block.get("id") == ref.get("block_id") for block in slide.get("blocks", []))
    return False


def validate_design_contract(contract: dict, ir: dict, template_evidence: dict) -> list[dict]:
    """Return validation findings; an empty list means the draft is structurally safe.

    Valid means *reference-safe*, not visually approved. A caller must still
    enforce review status before a future renderer is allowed to consume it.
    """
    findings = _schema_findings(contract)
    if findings:
        return findings

    ir_sha = "sha256:" + hashlib.sha256(
        json.dumps(ir, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    if contract["source_ir_sha256"] != ir_sha:
        findings.append(_finding(
            "CONTRACT_IR_HASH_MISMATCH", "/source_ir_sha256",
            "design contract source IR hash does not match supplied IR",
        ))

    evidence_sha = template_evidence.get("source", {}).get("sha256")
    if contract["template_evidence"]["source_sha256"] != evidence_sha:
        findings.append(_finding(
            "CONTRACT_TEMPLATE_HASH_MISMATCH", "/template_evidence/source_sha256",
            "design contract template hash does not match supplied Template Evidence",
        ))

    available_template_slides = {slide.get("slide_index") for slide in template_evidence.get("slides", [])}
    for index in contract["template_evidence"]["slide_indices"]:
        if index not in available_template_slides:
            findings.append(_finding(
                "CONTRACT_TEMPLATE_SLIDE_UNKNOWN", "/template_evidence/slide_indices",
                f"template slide {index} does not exist in supplied Template Evidence",
            ))

    slides = _slide_index(ir)
    for page_index, page in enumerate(contract["pages"]):
        path = f"/pages/{page_index}"
        slide = slides.get(page["slide_id"])
        if slide is None:
            findings.append(_finding("CONTRACT_SLIDE_UNKNOWN", f"{path}/slide_id",
                                     f"slide '{page['slide_id']}' does not exist in source IR"))
            continue
        if page["template_slide_index"] not in available_template_slides:
            findings.append(_finding("CONTRACT_TEMPLATE_SLIDE_UNKNOWN", f"{path}/template_slide_index",
                                     f"template slide {page['template_slide_index']} does not exist"))
        if page["composition"] == "action_roadmap":
            has_steps = any(
                block.get("role") == "list" and block.get("semantics") in {"steps", "stages"}
                for block in slide.get("blocks", [])
            )
            if not has_steps:
                findings.append(_finding(
                    "CONTRACT_COMPOSITION_CONTENT_MISMATCH", f"{path}/composition",
                    "action_roadmap requires an IR list block explicitly marked steps or stages",
                ))
        refs = [("message_ref", page["message_ref"]), ("primary_ref", page["primary_ref"])]
        refs.extend((f"evidence_refs/{index}", ref) for index, ref in enumerate(page["evidence_refs"]))
        if page.get("visual_ref"):
            refs.append(("visual_ref", page["visual_ref"]))
        for ref_path, ref in refs:
            if not _ref_exists(ref, slide):
                code = "CONTRACT_BLOCK_REF_UNKNOWN" if ref["kind"] == "block" else "CONTRACT_CONTENT_REF_UNKNOWN"
                findings.append(_finding(code, f"{path}/{ref_path}",
                                         f"{ref['kind']} reference is unavailable on IR slide '{slide['id']}'"))

    review = contract["review"]
    if contract["status"] == "draft" and review["state"] != "unreviewed":
        findings.append(_finding("CONTRACT_REVIEW_STATE_INVALID", "/review/state",
                                 "a draft Design Contract must remain unreviewed"))
    if contract["status"] == "approved":
        approved = review["state"] == "approved" and bool(review["evidence"])
        if not approved:
            findings.append(_finding("CONTRACT_APPROVAL_EVIDENCE_MISSING", "/review",
                                     "approved Design Contract requires approved review state and evidence"))
    if contract["status"] == "rejected" and review["state"] != "rejected":
        findings.append(_finding("CONTRACT_REVIEW_STATE_INVALID", "/review/state",
                                 "a rejected Design Contract must have rejected review state"))
    return findings
