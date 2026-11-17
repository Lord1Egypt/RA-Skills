#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cad-file-reader v0 统一候选契约：置信度分层、复核原因与稳定 ID。

本模块只整理已有识图候选，不新增工程量、扣减、材料量或最终数量。
所有候选固定 final_quantity=false。
"""
from __future__ import annotations

import hashlib
import json
import os
import math
from pathlib import Path
from typing import Any

CONTRACT_SCHEMA = "cad-file-reader/v0"


def _concise_default() -> bool:
    """默认精简契约（可由 CAD_CONCISE=0 关闭）。"""
    return os.environ.get("CAD_CONCISE", "1") == "1"
CONFIDENCE_TIERS = ("confirmed_evidence", "inferred_candidate", "review_required")
REVIEW_REASONS = (
    "missing_scale",
    "missing_unit",
    "missing_layer",
    "missing_block_definition",
    "ambiguous_text_binding",
    "geometry_conflict",
    "duplicate_candidate",
    "outside_viewport",
    "incomplete_geometry",
    "low_confidence_inference",
)
REASON_NOTES = {
    "missing_scale": "缺比例或比例依据不足",
    "missing_unit": "缺单位或单位依据不足",
    "missing_layer": "缺图层或图层归属不足",
    "missing_block_definition": "缺块定义或块名依据",
    "ambiguous_text_binding": "文字与几何/构件的绑定不明确",
    "geometry_conflict": "几何关系冲突",
    "duplicate_candidate": "存在重复候选",
    "outside_viewport": "证据坐标在图框外",
    "incomplete_geometry": "几何不完整或缺少闭合/端点证据",
    "low_confidence_inference": "低置信度推断，需人工复核",
}
CANDIDATE_KINDS = ("text", "block", "line", "polyline", "route", "room", "device", "measurement")

SECTION_KINDS = {
    # 描述几何/装饰
    "views": "text",
    "text_records": "text",
    "rooms": "room",
    "room_schedules": "room",
    "openings": "block",
    "opening_summary": "block",
    "practices": "text",
    "room_boundaries": "polyline",
    "wall_segments": "line",
    "ceiling_zones": "polyline",
    "stair_ramp_steps": "measurement",
    "exterior_wall_zones": "polyline",
    "node_detail_index": "text",
    # 安装
    "drawing_types": "text",
    "systems": "route",
    "route_segments": "route",
    "equipment": "device",
    "labels": "text",
    "risers": "route",
    "vertical_routes": "route",
    # 钢结构
    "members": "line",
    "sections": "text",
    "connections": "line",
    "materials": "text",
    "finishes": "text",
    "nodes": "line",
    "grids": "line",
    "steel_geometry": "line",
    # 市政
    "components": "device",
    "pipe_network": "line",
    "references": "text",
    "municipal_geometry": "line",
    # 测量候选
    "measurements": "measurement",
    # 语义与对比
    "semantic_layers": "text",
    "semantic_blocks": "block",
    "block_instances": "block",
    "mep_relations": "route",
    "legend_matches": "text",
    "drawing_changes": "text",
    # 电气
    "circuits": "route",
    "specs": "text",
    "lightning": "device",
    "fire_protection": "device",
    "weak_current": "device",
    "intelligent_building": "device",
    # 结构识图
    "rebars": "text",
    "structural_geometry": "line",
    # 总图/场地识图
    "site_geometry": "line",
    # 园林/景观识图
    "plant_legends": "text",
    "plant_block_legends": "block",
    "plant_block_fingerprints": "block",
    "plant_schedule_links": "text",
    "paving_closed_areas": "polyline",
    "green_area_candidates": "polyline",
    "pdf_geometry_candidates": "polyline",
    "hardscape": "text",
    # 深化识图引擎（给排水暖通/精装修/幕墙/人防/预制装配）
    "hvac_plumbing_geometry": "line",
    "interior_finish_geometry": "line",
    "curtain_wall_geometry": "line",
    "civil_defense_geometry": "line",
    "precast_geometry": "line",
}


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value))


def _bbox(row: dict[str, Any], evidence: list[dict[str, Any]]) -> list[float] | None:
    raw = row.get("bbox")
    if isinstance(raw, (list, tuple)) and len(raw) >= 4 and all(_is_number(v) for v in raw[:4]):
        x1, y1, x2, y2 = (float(v) for v in raw[:4])
        return [min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)]
    for key in ("geometry", "segment", "line", "geometry_segment"):
        raw = row.get(key)
        if isinstance(raw, (list, tuple)) and len(raw) >= 4 and all(_is_number(v) for v in raw[:4]):
            x1, y1, x2, y2 = (float(v) for v in raw[:4])
            return [min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)]
    raw = row.get("polygon")
    if isinstance(raw, (list, tuple)) and raw:
        xs: list[float] = []
        ys: list[float] = []
        for point in raw:
            if isinstance(point, (list, tuple)) and len(point) >= 2 and _is_number(point[0]) and _is_number(point[1]):
                xs.append(float(point[0]))
                ys.append(float(point[1]))
        if xs and ys:
            return [min(xs), min(ys), max(xs), max(ys)]
    for item in evidence:
        coord = item.get("coord")
        if isinstance(coord, (list, tuple)) and len(coord) >= 2 and _is_number(coord[0]) and _is_number(coord[1]):
            x, y = float(coord[0]), float(coord[1])
            return [x, y, x, y]
    if _is_number(row.get("x")) and _is_number(row.get("y")):
        x, y = float(row["x"]), float(row["y"])
        return [x, y, x, y]
    return None


def _confidence(row: dict[str, Any]) -> float:
    raw = row.get("confidence")
    if isinstance(raw, str):
        aliases = {"high": 0.95, "medium": 0.72, "low": 0.42}
        raw = aliases.get(raw.strip().lower(), 0.70)
    if not _is_number(raw):
        raw = 0.95 if row.get("status") == "candidate" else 0.42
    return max(0.0, min(1.0, float(raw)))


def _text(row: dict[str, Any]) -> str | None:
    for key in ("text", "raw", "title", "name", "room", "code", "label", "system"):
        value = row.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()[:240]
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return str(value)
    return None


def _layer(row: dict[str, Any], evidence: list[dict[str, Any]]) -> str | None:
    value = row.get("layer")
    if isinstance(value, str) and value.strip():
        return value.strip()
    for item in evidence:
        value = item.get("layer")
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _block_name(row: dict[str, Any]) -> str | None:
    for key in ("block_name", "block", "insert_name"):
        value = row.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _evidence(row: dict[str, Any]) -> list[dict[str, Any]]:
    raw = row.get("evidence")
    if raw is None:
        return []
    if isinstance(raw, dict):
        return [raw]
    if isinstance(raw, list):
        out: list[dict[str, Any]] = []
        for item in raw:
            if isinstance(item, dict):
                out.append(item)
            elif item is not None:
                out.append({"value": str(item)})
        return out
    return [{"value": str(raw)}]


def _value(row: dict[str, Any]) -> float | str | None:
    for key in ("value", "len_mm", "length_drawing_units", "area_drawing_units"):
        value = row.get(key)
        if _is_number(value):
            return float(value)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _unit(row: dict[str, Any]) -> str | None:
    value = row.get("unit") or row.get("drawing_unit")
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def _source_id(row: dict[str, Any]) -> str | None:
    for key in ("source_id", "id", "component_id", "boundary_id", "parent_zone_id"):
        value = row.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return str(value)
    return None


def _review_text(row: dict[str, Any]) -> str:
    values: list[str] = []
    for key in ("review_reason", "reason", "review_note", "review_notes", "note"):
        value = row.get(key)
        if isinstance(value, str) and value.strip():
            values.append(value.strip())
        elif isinstance(value, list):
            values.extend(str(v).strip() for v in value if str(v).strip())
    return "；".join(dict.fromkeys(values))


def _standard_reasons(
    row: dict[str, Any], kind: str, confidence: float, text: str, layer: str | None,
    block_name: str | None, bbox: list[float] | None, evidence: list[dict[str, Any]], duplicate: bool,
) -> list[str]:
    out: set[str] = set()
    low = text.lower()
    if "缺比例" in text or "比例需确认" in text or "比例依据不足" in text or "未提取到比例" in text:
        out.add("missing_scale")
    if (
        "缺单位" in text or "单位需确认" in text or "单位依据不足" in text or "未提取到单位" in text
        or (("比例" in text and "单位" in text) and any(token in text for token in ("缺", "需确认", "依据不足", "未提取")))
    ):
        out.add("missing_unit")
    if not layer or "缺图层" in text or "图层未分类" in text or "图层未映射" in text:
        out.add("missing_layer")
    if (kind == "block" and not block_name) or "缺块定义" in text or "块定义缺失" in text:
        out.add("missing_block_definition")
    if any(token in text for token in ("绑定", "文字关联", "关联不明确", "匹配不唯一")):
        out.add("ambiguous_text_binding")
    if "冲突" in text or "矛盾" in text:
        out.add("geometry_conflict")
    if duplicate or "重复" in text:
        out.add("duplicate_candidate")
    if "图框外" in text or "outside" in low:
        out.add("outside_viewport")
    if (
        any(token in text for token in ("未找到", "缺宽高", "缺显式", "不完整", "缺几何", "缺少 geometry", "缺闭合"))
        or (bbox is None and kind in {"line", "polyline", "route", "measurement"})
    ):
        out.add("incomplete_geometry")
    if confidence < 0.50:
        out.add("low_confidence_inference")
    return [reason for reason in REVIEW_REASONS if reason in out]


def _candidate(
    section: str, kind: str, row: dict[str, Any], source: Any, origin_schema: str,
    seen: dict[str, int], concise: bool = False,
) -> dict[str, Any]:
    evidence = _evidence(row)
    text = _text(row)
    layer = _layer(row, evidence)
    block_name = _block_name(row)
    bbox = _bbox(row, evidence)
    value = _value(row)
    unit = _unit(row)
    source_id = _source_id(row)
    key_payload = {
        "source": source,
        "origin_schema": origin_schema,
        "section": section,
        "kind": kind,
        "text": text,
        "layer": layer,
        "block_name": block_name,
        "value": value,
        "unit": unit,
        "bbox": bbox,
        "evidence": evidence,
    }
    key = hashlib.sha256(json.dumps(key_payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()[:16]
    occurrence = seen.get(key, 0)
    seen[key] = occurrence + 1
    candidate_id = key if occurrence == 0 else f"{key}-{occurrence + 1:02d}"
    duplicate = occurrence > 0
    confidence = _confidence(row)
    review_text = _review_text(row)
    declared_reasons = row.get("review_reasons")
    reasons = _standard_reasons(row, kind, confidence, review_text or "", layer, block_name, bbox, evidence, duplicate)
    if isinstance(declared_reasons, list):
        reasons.extend(str(x) for x in declared_reasons if str(x) in REVIEW_REASONS)
    reasons = [reason for reason in REVIEW_REASONS if reason in set(reasons)]
    if row.get("status") == "review" and not reasons:
        reasons = ["low_confidence_inference"]
    tier = "review_required" if reasons else ("confirmed_evidence" if confidence >= 0.90 else "inferred_candidate")
    notes = review_text or "；".join(REASON_NOTES[reason] for reason in reasons)
    full = {
        "id": candidate_id,
        "kind": kind,
        "value": value,
        "unit": unit,
        "layer": layer,
        "block_name": block_name,
        "text": text,
        "bbox": bbox,
        "evidence": evidence,
        "method": row.get("method") or row.get("basis") or section,
        "confidence": round(confidence, 4),
        "confidence_score": round(confidence, 4),
        "confidence_tier": tier,
        "review_reasons": reasons,
        "review_notes": notes,
        "source_schema": CONTRACT_SCHEMA,
        "source_id": source_id,
        "final_quantity": False,
        "origin_schema": origin_schema,
        "section": section,
        "source_file": source,
        "status": row.get("status") or ("review" if reasons else "candidate"),
        "rotation": row.get("rotation"),
        "discipline_refs": row.get("discipline_refs"),
        "confidence_scores": row.get("confidence_scores"),
    }
    if not concise:
        return full
    return {
        "id": candidate_id,
        "kind": kind,
        "value": value,
        "unit": unit,
        "layer": layer,
        "block_name": block_name,
        "text": text,
        "bbox": None,
        "evidence": [],
        "method": row.get("method") or row.get("basis") or section,
        "confidence": round(confidence, 4),
        "confidence_score": round(confidence, 4),
        "confidence_tier": tier,
        "review_reasons": reasons,
        "review_notes": notes,
        "source_schema": CONTRACT_SCHEMA,
        "source_id": source_id,
        "final_quantity": False,
        "origin_schema": origin_schema,
        "section": section,
        "source_file": source,
        "status": row.get("status") or ("review" if reasons else "candidate"),
        "rotation": None,
        "discipline_refs": row.get("discipline_refs") if isinstance(row.get("discipline_refs"), list) else [],
        "confidence_scores": row.get("confidence_scores") if isinstance(row.get("confidence_scores"), dict) else {},
    }


def contractize_payload(payload: dict[str, Any], source: Any = None, concise: bool | None = None) -> dict[str, Any]:
    """为已有识图 payload 追加 `contract` 字段；不改写既有业务数组。"""
    if concise is None:
        concise = _concise_default()
    if not isinstance(payload, dict):
        raise TypeError("contractize_payload 需要 JSON 对象")
    if source is None:
        source = payload.get("source_file")
        if source is None and isinstance(payload.get("source_files"), list):
            source = [Path(str(v)).name for v in payload["source_files"]]
        if source is None:
            source = ""
    if isinstance(source, Path):
        source = str(source)
    origin_schema = str(payload.get("schema") or "cad-scan-detail")
    seen: dict[str, int] = {}
    candidates: list[dict[str, Any]] = []
    for section, kind in SECTION_KINDS.items():
        rows = payload.get(section)
        if not isinstance(rows, list):
            continue
        for row in rows:
            if not isinstance(row, dict):
                continue
            candidates.append(_candidate(section, kind, row, source, origin_schema, seen, concise))
    main = [row for row in candidates if row["confidence_tier"] != "review_required"]
    review = [row for row in candidates if row["confidence_tier"] == "review_required"]
    summary = {
        "total": len(candidates),
        "confirmed_evidence": sum(1 for row in main if row["confidence_tier"] == "confirmed_evidence"),
        "inferred_candidate": sum(1 for row in main if row["confidence_tier"] == "inferred_candidate"),
        "review_required": len(review),
        "candidate_count": len(main),
        "duplicate_candidate": sum(1 for row in candidates if "duplicate_candidate" in row["review_reasons"]),
    }
    payload["contract"] = {
        "schema": CONTRACT_SCHEMA,
        "source": source,
        "origin_schema": origin_schema,
        "summary": summary,
        "review_reasons": REVIEW_REASONS,
        "candidates": main,
        "review_candidates": review,
        "boundary": "识图候选与测量候选，final_quantity=false；不输出最终工程量、材料量、造价或结算量。",
    }
    return payload


def validate_contract_payload(data: dict[str, Any]) -> list[str]:
    """内置轻量校验；返回错误列表，空列表表示通过。"""
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["根节点必须是 JSON 对象"]
    contract = data.get("contract")
    if not isinstance(contract, dict):
        return ["缺少 contract 对象"]
    if contract.get("schema") != CONTRACT_SCHEMA:
        errors.append("contract.schema 必须是 cad-file-reader/v0")
    arrays = (("candidates", contract.get("candidates")), ("review_candidates", contract.get("review_candidates")))
    seen_ids: set[str] = set()
    for array_name, rows in arrays:
        if not isinstance(rows, list):
            errors.append(f"contract.{array_name} 必须是数组")
            continue
        expected_tier = "review_required" if array_name == "review_candidates" else None
        for index, row in enumerate(rows):
            prefix = f"contract.{array_name}[{index}]"
            if not isinstance(row, dict):
                errors.append(f"{prefix} 必须是对象")
                continue
            for field in ("id", "kind", "value", "unit", "layer", "block_name", "text", "bbox", "evidence", "method", "confidence", "confidence_tier", "review_reasons", "review_notes", "source_schema", "source_id", "final_quantity"):
                if field not in row:
                    errors.append(f"{prefix}.{field} 缺失")
            if not isinstance(row.get("id"), str) or not row.get("id"):
                errors.append(f"{prefix}.id 必须是非空字符串")
            elif row["id"] in seen_ids:
                errors.append(f"{prefix}.id 重复：{row['id']}")
            else:
                seen_ids.add(row["id"])
            if row.get("kind") not in CANDIDATE_KINDS:
                errors.append(f"{prefix}.kind 非法")
            if row.get("confidence_tier") not in CONFIDENCE_TIERS:
                errors.append(f"{prefix}.confidence_tier 非法")
            elif expected_tier and row.get("confidence_tier") != expected_tier:
                errors.append(f"{prefix}.confidence_tier 放错数组")
            reasons = row.get("review_reasons")
            if not isinstance(reasons, list) or any(reason not in REVIEW_REASONS for reason in reasons):
                errors.append(f"{prefix}.review_reasons 含未定义原因")
            if row.get("confidence_tier") == "review_required" and not reasons:
                errors.append(f"{prefix}.review_reasons 不能为空")
            confidence = row.get("confidence")
            if not _is_number(confidence) or not 0.0 <= float(confidence) <= 1.0:
                errors.append(f"{prefix}.confidence 必须在 0..1")
            bbox = row.get("bbox")
            if bbox is not None and (
                not isinstance(bbox, list) or len(bbox) != 4 or not all(_is_number(v) for v in bbox)
                or bbox[0] > bbox[2] or bbox[1] > bbox[3]
            ):
                errors.append(f"{prefix}.bbox 必须是四元有序数值数组或 null")
            if not isinstance(row.get("evidence"), list):
                errors.append(f"{prefix}.evidence 必须是数组")
            if row.get("rotation") is not None and not _is_number(row["rotation"]):
                errors.append(f"{prefix}.rotation 必须是数字或 null")
            if row.get("discipline_refs") is not None and not isinstance(row["discipline_refs"], list):
                errors.append(f"{prefix}.discipline_refs 必须是数组")
            if row.get("confidence_scores") is not None and not isinstance(row["confidence_scores"], dict):
                errors.append(f"{prefix}.confidence_scores 必须是对象")
            if row.get("confidence_score") is not None and (not _is_number(row["confidence_score"]) or not 0.0 <= float(row["confidence_score"]) <= 1.0):
                errors.append(f"{prefix}.confidence_score 必须是 0..1 数字或 null")
            if row.get("source_schema") != CONTRACT_SCHEMA:
                errors.append(f"{prefix}.source_schema 必须是 cad-file-reader/v0")
            if row.get("final_quantity") is not False:
                errors.append(f"{prefix}.final_quantity 必须为 false")
        # 缺关键字段（比例/单位/图层/块定义）的候选必须进 review_candidates，不能留在主线候选静默
        missing_prefix = ("missing_scale", "missing_unit", "missing_layer", "missing_block_definition")
        for index, row in enumerate(contract.get("candidates") or []):
            reasons = row.get("review_reasons") or []
            hit = [r for r in reasons if r in missing_prefix]
            if hit:
                errors.append(
                    f"contract.candidates[{index}] 缺关键字段却留在主线候选（{', '.join(hit)}）；必须进 review_candidates"
                )
    summary = contract.get("summary")
    if not isinstance(summary, dict):
        errors.append("contract.summary 必须是对象")
    else:
        candidates = contract.get("candidates") or []
        review = contract.get("review_candidates") or []
        expected = {
            "total": len(candidates) + len(review),
            "candidate_count": len(candidates),
            "review_required": len(review),
            "confirmed_evidence": sum(1 for row in candidates if row.get("confidence_tier") == "confirmed_evidence"),
            "inferred_candidate": sum(1 for row in candidates if row.get("confidence_tier") == "inferred_candidate"),
        }
        for key, value in expected.items():
            if summary.get(key) != value:
                errors.append(f"contract.summary.{key} 与候选数组不一致")
    return errors


def validate_contract_file(path: str | Path) -> list[str]:
    with Path(path).open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    return validate_contract_payload(data)
