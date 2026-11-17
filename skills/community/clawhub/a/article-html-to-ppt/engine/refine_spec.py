"""P12-refine: apply a compile-time refine spec onto the IR.

The refine spec lets the user choose refinement AT GENERATION TIME (not
as a post-hoc step): pass ``compile --refine refine.json`` and the engine
applies the page-level composition intent to the matching slides before
layout, exactly as if the model had written ``slide.refine`` in the IR.

Spec format (JSON):
  {
    "<slide_id>": {
      "type": "split" | "wheel" | "contrast" | "spotlight",
      "left":  [0],          // block indices into slide.blocks (0-based)
      "right": [1, 2],
      "hub":   [0],
      "spokes": [1, 2, 3],
      "spotlight": [0],
      "supporting": [1, 2],
      "visual_left":  {"chart": {...}} | {"diagram_ir": {...}},   // split only
      "visual_right": {...}                                       // split only
    },
    ...
  }

Indices are resolved to the slide's blocks in order; a spec targeting an
unknown slide or out-of-range index is recorded as a rejection and the
slide keeps its rule archetype (honest degrade, never a failure).
"""

from __future__ import annotations

import json
from pathlib import Path

_INDEX_FIELDS = ("left", "right", "hub", "spokes", "spotlight", "supporting")
_VISUAL_FIELDS = ("visual_left", "visual_right")


def _block_refs(slide: dict, indices: list) -> list[str]:
    """Map 0-based block indices to block ids (assigning ids if absent)."""
    blocks = slide.get("blocks", [])
    for idx, block in enumerate(blocks):
        if not block.get("id"):
            block["id"] = f"b{idx + 1}"
    refs = []
    for i in indices:
        if isinstance(i, int) and 0 <= i < len(blocks):
            refs.append(blocks[i]["id"])
    return refs


def _to_slot(slide: dict, indices: list) -> dict:
    return {"blocks": _block_refs(slide, indices)}


def apply_refine_spec(ir: dict, spec: dict) -> dict:
    """Apply the refine spec to the IR in place; returns a report dict.

    report = {
      "applied": [{slide_id, type}],
      "rejected": [{slide_id, code, reason}],
    }
    """
    report: dict[str, list] = {"applied": [], "rejected": []}
    slides = {s["id"]: s for s in ir.get("slides", [])}

    for slide_id, intent in (spec or {}).items():
        slide = slides.get(slide_id)
        if slide is None:
            report["rejected"].append({
                "slide_id": slide_id,
                "code": "REFINE_SPEC_UNKNOWN_SLIDE",
                "reason": f"slide '{slide_id}' not in IR"})
            continue
        if not isinstance(intent, dict) or not intent.get("type"):
            report["rejected"].append({
                "slide_id": slide_id,
                "code": "REFINE_SPEC_MISSING_TYPE",
                "reason": "refine intent needs a 'type'"})
            continue

        rtype = intent["type"]
        if rtype not in ("split", "wheel", "contrast", "spotlight"):
            report["rejected"].append({
                "slide_id": slide_id, "code": "REFINE_SPEC_UNKNOWN_TYPE",
                "reason": f"unknown refine type '{rtype}'"})
            continue

        refine: dict = {"type": rtype}
        for field in _INDEX_FIELDS:
            indices = intent.get(field)
            if indices:
                refine[field] = _to_slot(slide, indices) if field != "spokes" \
                    else _block_refs(slide, indices)
        for field in _VISUAL_FIELDS:
            visual = intent.get(field)
            if visual:
                side = field.replace("visual_", "")
                refine.setdefault(side, {})
                refine[side]["visual"] = visual

        # explicit refine wins over chart inference (handled by chart_inference)
        slide["refine"] = refine
        report["applied"].append({"slide_id": slide_id, "type": rtype})

    return report


def load_refine_spec(path: str | Path | None) -> dict | None:
    if not path:
        return None
    return json.loads(Path(path).read_text(encoding="utf-8"))
