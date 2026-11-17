"""Provenance verifier: deterministic source_ref checks against SourceDocs.

Plan decision D4: the LLM's work is defined as *selection from the source*,
and selection is machine-verifiable. Every error is machine-readable and
slide-addressable so a repair loop (D5) can feed it straight back to the
model; fabricated numbers and dangling anchors are rejected, not rendered.

Error codes:
  SOURCE_ID_UNKNOWN        source_ref names a source not in the IR/doc set
  LOC_MALFORMED            anchor fails the frozen grammar
  LOC_NOT_FOUND            anchor points at no parsed element
  SPAN_OUT_OF_RANGE        #start-end exceeds the element text
  QUOTE_MISMATCH           verbatim quote not found in the referenced element
  METRIC_VALUE_NOT_IN_SOURCE  metric value/delta digits absent from element
  TABLE_REF_NOT_TABLE      table block anchored to a non-table element
  IMAGE_REF_NOT_IMAGE      image block anchored to a non-image element
"""

from __future__ import annotations

import re
from .source_doc import SourceDoc, extract_numbers, normalize_text, parse_anchor

_NUM_RE = re.compile(r"[-+]?\d[\d,]*(?:\.\d+)?%?")


def _issue(code: str, path: str, message: str, **extra) -> dict:
    return {"code": code, "path": path, "message": message, **extra}


def _check_ref(ref: dict, path: str, docs: dict[str, SourceDoc]) -> list[dict]:
    errors: list[dict] = []
    source_id, loc = ref.get("source_id"), ref.get("loc", "")
    doc = docs.get(source_id or "")
    if doc is None:
        return [_issue("SOURCE_ID_UNKNOWN", path,
                       f"source_id '{source_id}' has no parsed source document")]
    parsed = parse_anchor(loc)
    if parsed is None:
        return [_issue("LOC_MALFORMED", path, f"anchor '{loc}' violates the anchor grammar")]
    etype, index, span = parsed
    element = doc.get(f"{etype}_{index}")
    if element is None:
        return [_issue("LOC_NOT_FOUND", path,
                       f"anchor '{etype}_{index}' does not exist in source '{source_id}'")]

    haystack = element.full_text()
    if span is not None:
        start, end = span
        if start >= end or end > len(haystack):
            errors.append(_issue("SPAN_OUT_OF_RANGE", path,
                                 f"span #{start}-{end} exceeds element length {len(haystack)}"))
        else:
            haystack = haystack[start:end]

    quote = ref.get("quote")
    if quote and normalize_text(quote) not in haystack:
        errors.append(_issue("QUOTE_MISMATCH", path,
                             f"quote not found verbatim in '{element.anchor}'",
                             quote=quote))
    return errors


def _metric_numbers_check(block: dict, ref: dict, path: str,
                          docs: dict[str, SourceDoc]) -> list[dict]:
    doc = docs.get(ref.get("source_id") or "")
    parsed = parse_anchor(ref.get("loc", ""))
    if doc is None or parsed is None:
        return []  # structural errors already reported by _check_ref
    element = doc.get(f"{parsed[0]}_{parsed[1]}")
    if element is None:
        return []
    # Normalize the % sign away on both sides: it is a unit, not part of the
    # numeric value. "88%" in a metric must match "88 percent" in the source —
    # rejecting on the glyph alone would be a false fabrication signal.
    available = {a.rstrip("%") for a in element.numbers()}
    errors: list[dict] = []
    for key in ("value", "delta", "baseline"):
        raw = block.get(key)
        if not raw:
            continue
        claimed = {m.group(0).replace(",", "").rstrip("%")
                   for m in _NUM_RE.finditer(normalize_text(raw))}
        missing = {c for c in claimed
                   if c not in available and c.lstrip("+-") not in available}
        if missing:
            errors.append(_issue(
                "METRIC_VALUE_NOT_IN_SOURCE", f"{path}/{key}",
                f"numbers {sorted(missing)} not present in '{element.anchor}'",
                missing=sorted(missing)))
    return errors


def _typed_anchor_check(block: dict, ref: dict, path: str,
                        docs: dict[str, SourceDoc]) -> list[dict]:
    doc = docs.get(ref.get("source_id") or "")
    parsed = parse_anchor(ref.get("loc", ""))
    if doc is None or parsed is None:
        return []
    element = doc.get(f"{parsed[0]}_{parsed[1]}")
    if element is None:
        return []
    role = block.get("role")
    if role == "table" and element.etype != "table":
        return [_issue("TABLE_REF_NOT_TABLE", path,
                       f"table block anchored to '{element.anchor}' ({element.etype})")]
    if role == "image" and element.etype != "img":
        return [_issue("IMAGE_REF_NOT_IMAGE", path,
                       f"image block anchored to '{element.anchor}' ({element.etype})")]
    return []


def verify_ir(ir: dict, docs: dict[str, SourceDoc]) -> list[dict]:
    """Verify every source_ref in a v4 IR. Returns machine-readable errors."""
    errors: list[dict] = []
    declared = {s.get("source_id") for s in ir.get("sources", [])}
    for source_id in declared:
        if source_id not in docs:
            errors.append(_issue("SOURCE_ID_UNKNOWN", "/sources",
                                 f"declared source '{source_id}' has no parsed document"))

    for s_idx, slide in enumerate(ir.get("slides", [])):
        for b_idx, block in enumerate(slide.get("blocks", [])):
            path = f"/slides/{s_idx}/blocks/{b_idx}"
            ref = block.get("source_ref")
            if isinstance(ref, dict):
                errors.extend(_check_ref(ref, f"{path}/source_ref", docs))
                errors.extend(_typed_anchor_check(block, ref, path, docs))
                if block.get("role") == "metric":
                    errors.extend(_metric_numbers_check(block, ref, path, docs))
            for r_idx, multi_ref in enumerate(block.get("source_refs", []) or []):
                errors.extend(_check_ref(multi_ref, f"{path}/source_refs/{r_idx}", docs))
            for i_idx, item in enumerate(block.get("items", []) or []):
                item_ref = item.get("source_ref")
                if isinstance(item_ref, dict):
                    errors.extend(_check_ref(
                        item_ref, f"{path}/items/{i_idx}/source_ref", docs))
                for r_idx, multi_ref in enumerate(item.get("source_refs", []) or []):
                    errors.extend(_check_ref(
                        multi_ref,
                        f"{path}/items/{i_idx}/source_refs/{r_idx}",
                        docs,
                    ))
        notes = slide.get("speaker_notes")
        if isinstance(notes, dict):
            for r_idx, note_ref in enumerate(notes.get("source_refs", []) or []):
                if isinstance(note_ref, dict):
                    errors.extend(_check_ref(
                        note_ref,
                        f"/slides/{s_idx}/speaker_notes/source_refs/{r_idx}",
                        docs,
                    ))
    return errors
