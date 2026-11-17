"""Autonomy tiers (D7): behavioral probe, L1 advisor choices, L2
constrained composition proposals, local archetype hardening, and the
content-free contribution export (D10).

Freedom is granted by demonstrated behavior, never by model self-report:
the probe is a micro IR round-trip against a built-in source. Every
granted freedom stays inside engine-verifiable bounds — L1 picks from the
rule engine's own candidate menu; L2 proposes row/column compositions in
a grid language the engine lays out and QA-gates; a rejected proposal
falls back to the rule archetype.

Local hardening: a proposal that passed QA (plus user approval, asserted
by the caller) is stored content-free (role signature + row structure)
and becomes a rule candidate for future decks — any model, any tier.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
from pathlib import Path

PROBE_SOURCE = """# 蓝湖数据季度简报

蓝湖数据本季度营收 1.2 亿元，同比增长 24%。

## 增长构成

- 订阅收入 +31%
- 服务收入 +9%

毛利率保持在 61%，环比持平。
"""

TIERS = ("L0", "L1", "L2")


def home_dir() -> Path:
    return Path(os.environ.get("PPT_SMITH_HOME", str(Path.home() / ".ppt-smith")))


# ---- behavioral probe -------------------------------------------------------

def grade_probe(ir: dict, schema_errors: list, provenance_errors: list) -> dict:
    """Grade a probe IR round-trip into a tier grant."""
    if schema_errors or provenance_errors:
        tier, reason = "L0", "probe IR failed validation"
        result = "fail"
    else:
        metrics = relations = messages = 0
        for slide in ir.get("slides", []):
            messages += 1 if slide.get("message") else 0
            relations += len(slide.get("relations", []) or [])
            metrics += sum(1 for b in slide.get("blocks", [])
                           if b.get("role") == "metric")
        if metrics >= 1 and relations >= 1 and messages >= 1:
            tier, reason, result = "L2", "valid, anchored, enriched", "pass"
        else:
            tier, reason, result = "L1", "valid and anchored, minimal enrichment", "pass"
    return {
        "tier": tier,
        "probe": {"result": result,
                  "ir_roundtrip_valid": not (schema_errors or provenance_errors),
                  "repair_rounds_used": 0},
        "reason": reason,
        "schema_error_count": len(schema_errors),
        "provenance_error_count": len(provenance_errors),
    }


# ---- L2 composition proposals ----------------------------------------------

MAX_ROWS = 6
MAX_COLS = 4


def validate_proposals(proposals: list[dict], ir: dict) -> list[dict]:
    """Machine-readable validation of L2 composition proposals."""
    errors: list[dict] = []
    slides = {s["id"]: s for s in ir.get("slides", [])}
    for p_idx, proposal in enumerate(proposals):
        path = f"/proposals/{p_idx}"
        slide = slides.get(proposal.get("slide_id", ""))
        if slide is None:
            errors.append({"code": "PROPOSAL_UNKNOWN_SLIDE", "path": path,
                           "message": f"slide '{proposal.get('slide_id')}' not in IR"})
            continue
        rows = proposal.get("rows") or []
        if not rows or len(rows) > MAX_ROWS:
            errors.append({"code": "PROPOSAL_ROWS_OUT_OF_RANGE", "path": path,
                           "message": f"1..{MAX_ROWS} rows required"})
            continue
        block_ids = {b.get("id") for b in slide.get("blocks", []) if b.get("id")}
        seen: set[str] = set()
        for r_idx, row in enumerate(rows):
            ids = row.get("block_ids") or []
            if not ids or len(ids) > MAX_COLS:
                errors.append({"code": "PROPOSAL_COLS_OUT_OF_RANGE",
                               "path": f"{path}/rows/{r_idx}",
                               "message": f"1..{MAX_COLS} blocks per row"})
            for bid in ids:
                if bid not in block_ids:
                    errors.append({"code": "PROPOSAL_UNKNOWN_BLOCK",
                                   "path": f"{path}/rows/{r_idx}",
                                   "message": f"block id '{bid}' not in slide "
                                              "(blocks need explicit ids)"})
                elif bid in seen:
                    errors.append({"code": "PROPOSAL_DUPLICATE_BLOCK",
                                   "path": f"{path}/rows/{r_idx}",
                                   "message": f"block id '{bid}' used twice"})
                seen.add(bid)
    return errors


def proposal_sha(proposal: dict) -> str:
    return hashlib.sha256(
        json.dumps(proposal, sort_keys=True).encode("utf-8")).hexdigest()


# ---- local archetype store --------------------------------------------------

def _roles_signature(slide: dict) -> str:
    counts: dict[str, int] = {}
    for block in slide.get("blocks", []):
        counts[block.get("role", "?")] = counts.get(block.get("role", "?"), 0) + 1
    return "|".join(f"{k}:{v}" for k, v in sorted(counts.items()))


def structure_of(proposal: dict, slide: dict) -> dict:
    """Content-free hardened structure: role signature + row widths only."""
    id_to_role = {b.get("id"): b.get("role") for b in slide.get("blocks", [])}
    return {
        "rows": [{"roles": [id_to_role.get(bid, "?") for bid in row["block_ids"]]}
                 for row in proposal["rows"]],
        "roles_signature": _roles_signature(slide),
    }


def harden(proposal: dict, slide: dict, store: Path | None = None) -> dict:
    structure = structure_of(proposal, slide)
    pattern_id = "local-" + proposal_sha(structure)[:10]
    record = {"pattern_id": pattern_id, "version": 1, **structure}
    store_dir = (store or home_dir() / "local-archetypes")
    store_dir.mkdir(parents=True, exist_ok=True)
    (store_dir / f"{pattern_id}.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return record


def load_local_archetypes(store: Path | None = None) -> list[dict]:
    store_dir = store or home_dir() / "local-archetypes"
    records = []
    if store_dir.is_dir():
        for path in sorted(store_dir.glob("local-*.json")):
            try:
                record = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            if isinstance(record, dict) and record.get("pattern_id") and record.get("rows"):
                records.append(record)
    return records


def match_local_archetype(slide: dict, records: list[dict]) -> dict | None:
    signature = _roles_signature(slide)
    for record in records:
        if record.get("roles_signature") == signature:
            return record
    return None


def rows_from_pattern(slide: dict, record: dict) -> list[dict] | None:
    """Re-instantiate a hardened pattern on a new slide: assign this
    slide's blocks (in order, by role) into the stored row structure."""
    pool: dict[str, list[int]] = {}
    for idx, block in enumerate(slide.get("blocks", [])):
        pool.setdefault(block.get("role", "?"), []).append(idx)
    rows: list[dict] = []
    for row in record["rows"]:
        indices = []
        for role in row["roles"]:
            if not pool.get(role):
                return None  # signature matched but order exhausted; bail out
            indices.append(pool[role].pop(0))
        rows.append({"block_indices": indices})
    if any(pool.values()):
        leftovers = [i for indices in pool.values() for i in indices]
        rows.extend({"block_indices": [i]} for i in sorted(leftovers))
    return rows


# ---- contribution export ----------------------------------------------------

# Export vocabulary is deliberately independent of caller-supplied labels.
_EXPORT_ROLES = frozenset(("fact", "quote", "metric", "list", "table", "image",
                           "insight", "risk", "recommendation", "context"))
_EXPORT_DIAGRAMS = frozenset((
    "causal_chain", "phase_roadmap", "layered_architecture", "heat_matrix",
    "drill_down_stair", "interaction_storyboard", "product_ui_overview",
    "process_flow", "process_lane", "swimlane", "timeline", "issue_tree",
    "decision_tree", "flywheel", "hub_spoke", "zoned_ecosystem",
    "capability_landscape", "dependency_graph", "data_flow", "state_transition"))
_EXPORT_REFINES = frozenset(("split", "wheel", "contrast", "spotlight"))
_EXPORT_CHOICES = frozenset((
    "kpi_wall", "full_table", "quote_focus", "list_stack", "image_story",
    "evidence_stack", "step_cards", "proposed_grid",
    *("chart_" + x for x in ("column", "bar", "line", "pie", "doughnut", "combo", "scatter")),
    *("diagram_" + x for x in _EXPORT_DIAGRAMS),
    *("refine_" + x for x in _EXPORT_REFINES)))
_EXPORT_STAGES = frozenset(("narrative", "archetype", "component", "layout_variant",
                            "style_mapping", "text_fitting", "repair", "fallback"))
_EXPORT_ACTORS = frozenset(("rule", "fallback", "autonomy_l1", "autonomy_l2",
                            "llm_advisor", "llm_proposal", "user_override"))
_EXPORT_COUNTS = frozenset(("block_count", "metric_count", "table_count", "list_count",
                            "quote_count", "image_count", "fact_count", "insight_count",
                            "risk_count", "relation_count"))


def _export_enum(value: object, allowed: frozenset) -> str | None:
    return value if type(value) is str and value in allowed else None


def _export_confidence(value: object) -> float | None:
    if type(value) in (int, float) and 0 <= value <= 1 and math.isfinite(value):
        return round(value, 2)
    return None


def _export_evidence(evidence: object) -> dict:
    items = evidence.get("structural", []) if isinstance(evidence, dict) else []
    safe = []
    for item in items[:64] if isinstance(items, list) else []:
        if not isinstance(item, dict):
            continue
        feature, value = item.get("feature"), item.get("value")
        if type(feature) is not str:
            continue
        valid = (feature in _EXPORT_COUNTS and type(value) is int and 0 <= value <= 10000)
        valid |= feature in ("has_steps", "chart") and type(value) is bool
        valid |= feature == "diagram" and _export_enum(value, _EXPORT_DIAGRAMS) is not None
        valid |= feature == "refine" and _export_enum(value, _EXPORT_REFINES) is not None
        if valid:
            safe.append({"feature": feature, "value": value})
    return {"structural": safe}


def _export_pattern(record: dict) -> dict | None:
    rows = record.get("rows")
    if not isinstance(rows, list) or not 1 <= len(rows) <= MAX_ROWS:
        return None
    safe_rows, counts = [], {}
    for row in rows:
        roles = row.get("roles") if isinstance(row, dict) else None
        if not isinstance(roles, list) or not 1 <= len(roles) <= MAX_COLS:
            return None
        if any(_export_enum(role, _EXPORT_ROLES) is None for role in roles):
            return None
        safe_rows.append({"roles": list(roles)})
        for role in roles:
            counts[role] = counts.get(role, 0) + 1
    # Never copy local identifiers, signatures, versions or extension fields.
    structure = {"rows": safe_rows,
                 "roles_signature": "|".join(f"{k}:{v}" for k, v in sorted(counts.items()))}
    return {"pattern_id": "local-" + proposal_sha(structure)[:10],
            "version": 1, **structure}


def contribution_bundle(traces: list[dict], store: Path | None = None, *,
                        shared_export: bool = False) -> dict:
    """Build a local, allowlisted sharing bundle only after explicit consent.

    Callers must obtain user authorization before setting shared_export=True.
    This function never uploads. Structural statistics can still be sensitive;
    the allowlist prevents raw content leakage, not statistical inference.
    The three version-1 top-level keys remain stable; unknown data is omitted.
    """
    if shared_export is not True:
        raise PermissionError("Contribution sharing requires explicit authorization")
    patterns = []
    for record in load_local_archetypes(store):
        safe = _export_pattern(record)
        if safe is not None:
            patterns.append(safe)
    decisions = []
    for trace in traces:
        entries = trace.get("decisions", []) if isinstance(trace, dict) else []
        for decision in entries if isinstance(entries, list) else []:
            if not isinstance(decision, dict):
                continue
            candidates = decision.get("candidates", [])
            safe_candidates = []
            for candidate in candidates[:16] if isinstance(candidates, list) else []:
                if not isinstance(candidate, dict):
                    continue
                choice = _export_enum(candidate.get("choice"), _EXPORT_CHOICES)
                if choice is not None:
                    safe_candidates.append({"choice": choice,
                                            "confidence": _export_confidence(candidate.get("confidence"))})
            decisions.append({
                "stage": _export_enum(decision.get("stage"), _EXPORT_STAGES),
                "evidence": _export_evidence(decision.get("evidence")),
                "candidates": safe_candidates,
                "chosen": _export_enum(decision.get("chosen"), _EXPORT_CHOICES),
                "chosen_by": _export_enum(decision.get("chosen_by"), _EXPORT_ACTORS),
                "confidence": _export_confidence(decision.get("confidence")),
            })
    return {"bundle_version": 1, "local_archetypes": patterns, "decisions": decisions}
