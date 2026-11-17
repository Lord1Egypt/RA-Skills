"""Validate source-backed slide content contracts for the Template route."""

from __future__ import annotations

from .evidence_ledger import evidence_by_id, validate_evidence_ledger


EVIDENCE_OPTIONAL_ARCHETYPES = {"cover", "section", "closing"}


def _issue(code: str, *, slide_id: str | None = None, evidence_id: str | None = None) -> dict:
    issue = {"code": code}
    if slide_id is not None:
        issue["slide_id"] = slide_id
    if evidence_id is not None:
        issue["evidence_id"] = evidence_id
    return issue


def _string_ids(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str) and item]


def validate_content_contracts(content_bindings: dict, ledger: dict) -> list[dict]:
    """Return stable issues for slide contracts and deck-wide required evidence."""
    ledger_issues = validate_evidence_ledger(ledger)
    if ledger_issues:
        return ledger_issues
    known = evidence_by_id(ledger)
    slides = content_bindings.get("slides") if isinstance(content_bindings, dict) else None
    if not isinstance(slides, list) or not slides:
        return [_issue("CONTENT_CONTRACT_SLIDES_INVALID")]

    issues: list[dict] = []
    selected_across_deck: set[str] = set()
    explained_omissions: set[str] = set()
    for index, slide in enumerate(slides):
        if not isinstance(slide, dict):
            issues.append(_issue("SLIDE_CONTENT_CONTRACT_INVALID", slide_id=str(index + 1)))
            continue
        slide_id = slide.get("id")
        if not isinstance(slide_id, str) or not slide_id:
            slide_id = str(index + 1)
            issues.append(_issue("SLIDE_ID_MISSING", slide_id=slide_id))
        archetype = slide.get("archetype", "body")
        assertion = slide.get("assertion")
        evidence_ids = _string_ids(slide.get("evidence_ids"))
        required_ids = _string_ids(slide.get("required_evidence_ids"))

        if archetype not in EVIDENCE_OPTIONAL_ARCHETYPES:
            if not isinstance(assertion, str) or not assertion.strip():
                issues.append(_issue("SLIDE_ASSERTION_MISSING", slide_id=slide_id))
            if not evidence_ids:
                issues.append(_issue("SLIDE_EVIDENCE_MISSING", slide_id=slide_id))

        for evidence_id in evidence_ids:
            if evidence_id not in known:
                issues.append(_issue(
                    "EVIDENCE_ID_UNKNOWN", slide_id=slide_id, evidence_id=evidence_id,
                ))
            else:
                selected_across_deck.add(evidence_id)

        omissions = slide.get("omissions", [])
        if not isinstance(omissions, list):
            omissions = []
        explained_here: set[str] = set()
        for omission in omissions:
            if not isinstance(omission, dict):
                continue
            evidence_id = omission.get("evidence_id")
            reason = omission.get("reason")
            if not isinstance(evidence_id, str) or evidence_id not in known:
                issues.append(_issue(
                    "EVIDENCE_ID_UNKNOWN", slide_id=slide_id,
                    evidence_id=evidence_id if isinstance(evidence_id, str) else None,
                ))
                continue
            if not isinstance(reason, str) or not reason.strip():
                code = (
                    "EXHIBIT_OMISSION_UNEXPLAINED"
                    if known[evidence_id].get("kind") == "exhibit"
                    else "EVIDENCE_OMISSION_UNEXPLAINED"
                )
                issues.append(_issue(code, slide_id=slide_id, evidence_id=evidence_id))
                continue
            explained_here.add(evidence_id)
            explained_omissions.add(evidence_id)

        handled_here = set(evidence_ids) | explained_here
        for evidence_id in required_ids:
            if evidence_id not in known:
                issues.append(_issue(
                    "EVIDENCE_ID_UNKNOWN", slide_id=slide_id, evidence_id=evidence_id,
                ))
            if evidence_id not in handled_here:
                issues.append(_issue(
                    "REQUIRED_EVIDENCE_MISSING", slide_id=slide_id,
                    evidence_id=evidence_id,
                ))

    handled_across_deck = selected_across_deck | explained_omissions
    for evidence_id, unit in known.items():
        if unit.get("must_keep") and evidence_id not in handled_across_deck:
            issues.append(_issue("REQUIRED_EVIDENCE_MISSING", evidence_id=evidence_id))
    return issues
