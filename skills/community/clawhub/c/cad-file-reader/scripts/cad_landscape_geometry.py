#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 cad_scan 详情 JSON 提炼园林/景观识图中间数据和证据。

边界：只识别园林图纸类型、种植系统、苗木图例（乔/灌/地被/其他）、硬景铺装
闭合域候选、水景/家具等构件候选；全部 final_quantity=false，不输出苗木数量、
铺装面积、土方量、材料量、造价或结算量。
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
import sys
from collections import Counter, deque
from pathlib import Path
from typing import Any

from cad_common import compact, load_rules, match_rule
from cad_contract import contractize_payload

ROOT = Path(__file__).resolve().parents[1]
RULES_PATH = ROOT / "packs" / "landscape-geometry" / "rules.json"
INSTITUTE_DIR = ROOT / "packs" / "landscape-geometry" / "institutes"
SCHEMA = "cad-landscape-geometry/v1"


def merge_override(base, override):
    """轻量合并：dict 深合并（值 dict 合并，list 追加去重），其他覆盖。"""
    base = dict(base or {})
    for key, val in (override or {}).items():
        if not isinstance(val, dict):
            base[key] = val
            continue
        cur = base.get(key)
        if isinstance(cur, dict):
            merged = dict(cur)
            for k, v in val.items():
                if isinstance(v, dict) and isinstance(merged.get(k), dict):
                    merged[k] = dict(merged[k])
                    merged[k].update(v)
                elif isinstance(v, list) and isinstance(merged.get(k), list):
                    seen = merged[k] + [x for x in v if x not in merged[k]]
                    merged[k] = seen
                else:
                    merged[k] = v
            base[key] = merged
        elif isinstance(cur, list):
            base[key] = cur + [x for x in val if x not in cur]
        else:
            base[key] = val
    return base


def load_rules_with_institute(rules, institute=None):
    if not institute:
        return rules
    rp = INSTITUTE_DIR / f"{institute}.json"
    if not rp.exists():
        raise FileNotFoundError(f"设计院图例覆盖不存在：{rp}")
    override = json.loads(rp.read_text(encoding="utf-8"))
    return merge_override(rules, override)



def _num(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def data_file_name(data, value):
    if isinstance(value, dict):
        return compact(value.get("name") or value.get("path"))
    files = data.get("files") or []
    if isinstance(value, int) and 0 <= value < len(files):
        item = files[value]
        return compact(item.get("name") or item.get("path")) if isinstance(item, dict) else compact(item)
    return compact(value)


def evidence_of(record):
    ev = {"text": compact(record.get("text", "")), "layer": record.get("layer"), "kind": record.get("kind"), "space": record.get("space")}
    if record.get("x") is not None or record.get("y") is not None:
        ev["coord"] = [record.get("x"), record.get("y")]
    for key in ("file", "file_name", "sheet", "handle"):
        if record.get(key) is not None:
            ev[key] = record.get(key)
    return {k: v for k, v in ev.items() if v not in (None, "")}


def read_records(data):
    records = data.get("text_records") or data.get("texts") or []
    out = []
    for i, raw in enumerate(records):
        if not isinstance(raw, dict):
            continue
        text = compact(raw.get("text", ""))
        if not text:
            continue
        fname = raw.get("file_name")
        if fname is None:
            fname = data_file_name(data, raw.get("file"))
        out.append({"text": text, "layer": compact(raw.get("layer", "")), "kind": compact(raw.get("kind") or raw.get("type", "")), "space": raw.get("space"), "x": raw.get("x"), "y": raw.get("y"), "sheet": raw.get("sheet"), "file": raw.get("file"), "file_name": fname, "handle": raw.get("handle"), "_index": i})
    return out


def context_of(r):
    return (compact(r.get("file_name") or r.get("file")), r.get("sheet"), r.get("space"))


def iter_geometry(data):
    sfiles = data.get("geometry_segments") or []
    lfiles = data.get("geometry_layers") or []
    for fi, segs in enumerate(sfiles):
        layers = lfiles[fi] if fi < len(lfiles) else []
        for si, seg in enumerate(segs or []):
            if not isinstance(seg, (list, tuple)) or len(seg) < 4:
                continue
            layer = compact(layers[si]) if si < len(layers) else ""
            yield fi, si, layer, seg


def _base_key(seed):
    return seed[:2] if isinstance(seed, (list, tuple)) else None


def drawing_type_candidates(records, rules):
    out, seen = [], set()
    for rec in records:
        kind, _rule, pat = match_rule(rec["text"], rules.get("view_rules") or [], "type")
        if not kind:
            continue
        key = (context_of(rec), kind)
        if key in seen:
            continue
        seen.add(key)
        out.append({"type": kind, "raw": rec["text"], "pattern": pat, "confidence": float((rules.get("confidence") or {}).get("direct_label", 0.95)), "status": "candidate", "evidence": [evidence_of(rec)]})
    return out


def system_candidates(records, rules):
    out, seen = [], set()
    for rec in records:
        system, _rule, pat = match_rule(rec["text"], rules.get("system_rules") or [], "system")
        if not system:
            continue
        key = (context_of(rec), system, rec.get("layer"), rec["text"])
        if key in seen:
            continue
        seen.add(key)
        out.append({"system": system, "raw": rec["text"], "pattern": pat, "layer": rec.get("layer"), "file": rec.get("file_name"), "sheet": rec.get("sheet"), "confidence": float((rules.get("confidence") or {}).get("pattern_match", 0.78)), "status": "candidate", "evidence": [evidence_of(rec)]})
    return out


def plant_classify(text, rules):
    """按植物名/关键词分类到乔/灌/地被/其他。"""
    upper = compact(text).upper()
    normalized = re.sub(r"\s+", "", upper)
    for phrase in rules.get("plant_exclude_phrases") or []:
        ph = str(phrase).upper()
        if ph and ph in upper:
            return "", ""
    groups = [
        ("乔木", rules.get("plant_trees") or [], (rules.get("confidence") or {}).get("direct_label", 0.95)),
        ("灌木", rules.get("plant_shrubs") or [], (rules.get("confidence") or {}).get("direct_label", 0.95)),
        ("地被", rules.get("plant_groundcover") or [], (rules.get("confidence") or {}).get("pattern_match", 0.78)),
    ]
    best: tuple[float, str, str] = (0.0, "", "")
    for label, tokens, conf in groups:
        for token in tokens or []:
            tok = str(token).upper()
            tok_norm = re.sub(r"\s+", "", tok)
            if tok_norm and tok_norm in normalized and conf > best[0]:
                best = (conf, label, tok)
    if best[0] > 0:
        return best[1], best[2]
    for token in rules.get("plant_other") or []:
        token_norm = re.sub(r"\s+", "", str(token).upper())
        if token_norm and token_norm in normalized:
            return "其他", str(token)
    # 英文/通用图例词兜底（面向海外/ASCII 图例，中标在前面优先）
    aliases = rules.get("plant_english_aliases") or {}
    for token, category in aliases.items():
        tok = str(token).upper()
        if tok and re.search(r"(?<![A-Za-z])" + re.escape(tok) + r"(?![A-Za-z])", upper):
            return str(category), tok
    return "", ""




def plant_classify_by_block(block_name, rules):
    """按块名/图例代号 -> 乔/灌/地被/其他 分类（支持通用植物名与图例词）。"""
    upper = compact(block_name).upper()
    # 先按具体植物名/地被词
    label, token = plant_classify(block_name, rules)
    if label:
        return label, token
    # 再按通用块词（面向设计院图例代号，可配置）
    for tok, category in (rules.get("plant_block_aliases") or {}).items():
        t = str(tok).upper()
        if t and t in upper:
            return str(category), tok
    block_tokens = rules.get("plant_block_tokens") or []
    for tok in block_tokens:
        t = str(tok).upper()
        if t and t in upper:
            if any(k in upper for k in ("树", "乔", "乔木")):
                return "乔木", tok
            if any(k in upper for k in ("灌", "灌木")):
                return "灌木", tok
            if any(k in upper for k in ("草", "地被")):
                return "地被", tok
            return "其他", tok
    return "", ""


def block_plant_candidates(data, rules, records=None):
    """从块引用名识别植物图例块候选，附带插入坐标供苗木表交叉验证（final_quantity=false）。

    优先用 meta.block_refs 的计数，再用 records 里 INSERT 记录补齐坐标/图层。
    """
    meta = data.get("meta") or {}
    refs = meta.get("block_refs") or {}
    if not isinstance(refs, dict):
        refs = {}
    counts: dict[str, int] = {}
    point_map: dict[str, list[tuple[float, float]]] = {}
    layer_map: dict[str, set] = {}
    for name, count in refs.items():
        if isinstance(name, str) and name.strip():
            counts[name] = counts.get(name, 0) + int(count or 0)
    if records:
        for rec in records:
            if str(rec.get("kind", "")).upper() != "INSERT":
                continue
            name = str(rec.get("text", ""))
            if not name:
                continue
            counts[name] = counts.get(name, 0) + 1
            x, y = rec.get("x"), rec.get("y")
            if x is not None and y is not None:
                try:
                    pt = (float(x), float(y))
                    pts = point_map.setdefault(name, [])
                    if not any(abs(px - pt[0]) < 1e-6 and abs(py - pt[1]) < 1e-6 for px, py in pts[-80:]):
                        pts.append(pt)
                except (TypeError, ValueError):
                    pass
            if rec.get("layer"):
                layer_map.setdefault(name, set()).add(str(rec["layer"]))
    cap = int((rules.get("max_block_plants") or 500))
    out, seen = [], set()
    for name, count in counts.items():
        label, token = plant_classify_by_block(name, rules)
        if not label or name in seen:
            continue
        seen.add(name)
        reasons = []
        if not name.strip():
            reasons.append("missing_block_definition")
        pts = point_map.get(name, [])
        layers = sorted(layer_map.get(name, set()))
        supports: list[dict] = []
        sup = {"source": "block_name", "value": name, "matched_token": token, "instance_count": int(count or 0)}
        if pts:
            sup["coord"] = [round(pts[0][0], 3), round(pts[0][1], 3)]
            sup["sample_coords"] = [[round(px, 3), round(py, 3)] for px, py in pts[:60]]
        supports.append(sup)
        row = {
            "type": "plant_legend", "category": label, "system": "planting",
            "name": name, "plant": name, "matched_token": token,
            "layer": "; ".join(layers) if layers else None,
            "file": data_file_name(data, 0), "sheet": None,
            "x": pts[0][0] if pts else None, "y": pts[0][1] if pts else None,
            "instance_count": int(count or 0), "confidence": 0.9,
            "status": "candidate", "review_reasons": reasons, "review_reason": "; ".join(reasons),
            "evidence": [{"kind": "block_name", "value": name, "matched_token": token,
                          "instance_count": int(count or 0), "supports": supports}],
        }
        out.append(row)
        if len(out) >= cap:
            break
    return out

def _seg_in_radius(x1, y1, x2, y2, px, py, radius):
    """segment 与插入点距离是否在半径内：任一端点或中点命中即算。"""
    def close(x, y):
        return (x - px) ** 2 + (y - py) ** 2 <= radius * radius
    if close(x1, y1) or close(x2, y2):
        return True
    return close((x1 + x2) / 2.0, (y1 + y2) / 2.0)


def _component_shape(segs, tiny_tol):
    """把局部线段按端点邻接粗分组，返回组件级形状描述。"""
    class UF:
        def __init__(self):
            self.p = {}
        def key(self, x, y):
            return (int(round(x / tiny_tol)), int(round(y / tiny_tol)))
        def find(self, k):
            self.p.setdefault(k, k)
            while self.p.get(self.p[k], self.p[k]) != self.p[k]:
                self.p[k] = self.p[self.p[k]]
            return self.p[k]
        def union(self, a, b):
            ra, rb = self.find(a), self.find(b)
            if ra != rb:
                self.p[rb] = ra

    uf = UF()
    edges = []
    for x1, y1, x2, y2 in segs:
        k1, k2 = uf.key(x1, y1), uf.key(x2, y2)
        if k1 == k2:
            continue
        edges.append((k1, k2, (x1, y1, x2, y2)))
        uf.union(k1, k2)
    by_root = {}
    for k1, k2, raw in edges:
        root = uf.find(k1)
        by_root.setdefault(root, []).append(raw)
    comps = []
    for root, raw_segs in by_root.items():
        xs, ys = [], []
        length = 0.0
        for x1, y1, x2, y2 in raw_segs:
            xs += [x1, x2]
            ys += [y1, y2]
            length += ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        if len(raw_segs) < 2:
            continue
        minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
        w, h = max(0.0, maxx - minx), max(0.0, maxy - miny)
        side = max(w, h, 1.0)
        comps.append({
            "segment_count": len(raw_segs),
            "total_length": round(length, 3),
            "bbox": [round(minx, 3), round(miny, 3), round(maxx, 3), round(maxy, 3)],
            "width": round(w, 3),
            "height": round(h, 3),
            "aspect": round(side / max(min(w, h), 1.0), 3),
            "round_score": round(min(w, h) / side, 3),
        })
    comps.sort(key=lambda c: -c["total_length"])
    return comps


def _local_shape_features(segs, rules, scale=1.0):
    """对插入点附近的线段做形状指纹，返回特征字典；几何不足返回 None。

    scale 由 _detect_scale 给出（mm 等价比例因子），用于把阈值统一到图纸单位。
    """
    cfg = rules.get("plant_geom") or {}
    radius = float(cfg.get("radius") or 1200) * scale
    tiny_tol = float(cfg.get("tiny_tolerance") or max(10, radius / 20))
    min_len = float(cfg.get("min_total_length") or 400) * scale
    round_aspect = float(cfg.get("roundish_min_aspect") or 0.55)
    elong_aspect = float(cfg.get("elongated_min_aspect") or 2.5)
    tree_min = float(cfg.get("tree_min_bbox") or 150) * scale
    segs = [s for s in segs if _seg_in_radius(s[0], s[1], s[2], s[3], 0, 0, radius)]
    if len(segs) < 3:
        return None
    comps = _component_shape([(s[0], s[1], s[2], s[3]) for s in segs], tiny_tol)
    if not comps:
        return None
    total_len = sum(c["total_length"] for c in comps)
    dominant = comps[0]
    round_comps = [c for c in comps if c["round_score"] >= round_aspect]
    single_round = dominant["round_score"] >= round_aspect and dominant["width"] >= tree_min
    multi_round = len(round_comps) >= 2
    elongated = dominant["aspect"] >= elong_aspect and dominant["total_length"] >= min_len
    return {
        "segment_count": len(segs),
        "component_count": len(comps),
        "total_length": round(total_len, 3),
        "bbox": [min(c["bbox"][0] for c in comps), min(c["bbox"][1] for c in comps),
                 max(c["bbox"][2] for c in comps), max(c["bbox"][3] for c in comps)],
        "width": round(max(c["width"] for c in comps), 3),
        "height": round(max(c["height"] for c in comps), 3),
        "aspect": dominant["aspect"],
        "round_score": dominant["round_score"],
        "roundish_components": len(round_comps),
        "single_round": single_round,
        "multi_round": multi_round,
        "elongated": elongated,
        "components": comps[:8],
    }


def _fingerprint_classify(feat):
    lb = (0.0, "")
    if feat.get("elongated"):
        lb = (3, ("地被", "绿篱/地被条带"))
    if feat.get("multi_round") and 2 > lb[0]:
        lb = (2, ("灌木", "多圆团簇"))
    if feat.get("single_round") and 1 > lb[0]:
        lb = (1, ("乔木", "大圆+中心点"))
    return lb[1] if lb[0] else ("", "")


def _top_layer(segs):
    from collections import Counter
    counter = Counter(str(s[4]).strip() for s in segs if str(s[4]).strip())
    return counter.most_common(1)[0][0] if counter else None


def _detect_scale(data, records=None):
    """从文字/图层推断图纸长度单位，返回 mm 等价比例因子。

    mm 为单位时返回 1.0；米为单位返回 1000.0，把几何阈值统一换算到 mm。
    未识别时返回 1.0，结果仍为候选口径，不改变 final_quantity=false。
    """
    if records is None:
        records = read_records(data)
    samples: list[str] = []
    for rec in records[:3000]:
        t = compact(rec.get("text", ""))
        if not t:
            continue
        if "单位" in t or "unit" in t.lower() or "毫米" in t or "米" in t.lower():
            samples.append(t)
        if len(samples) >= 40:
            break
    for t in samples:
        low = t.lower()
        if "毫米" in t or ("mm" in low and "单位" in t):
            return 1.0
    for t in samples:
        low = t.lower()
        if ("单位" in t or "unit" in low or "米" in t) and ("米" in t or "m" in low):
            if "mm" not in low and "毫米" not in t:
                return 1000.0
    return 1.0


def _shifted_to_local(segs):
    """把绝对坐标线段转为以块内/插入点局部坐标表达的线段序列。"""
    if not segs:
        return []
    out = []
    for s in segs:
        if isinstance(s, dict):
            out.append((float(s.get("x1") or 0), float(s.get("y1") or 0),
                        float(s.get("x2") or 0), float(s.get("y2") or 0), compact(s.get("layer") or "")))
        elif len(s) >= 4:
            vals = [_num(v) for v in s[:4]]
            if any(v is None for v in vals):
                continue
            out.append((vals[0], vals[1], vals[2], vals[3], compact(s[4] if len(s) > 4 else "")))
    if not out:
        return []
    xs = [v[0] for v in out] + [v[2] for v in out]
    ys = [v[1] for v in out] + [v[3] for v in out]
    minx, miny = min(xs), min(ys)
    return [(x1 - minx, y1 - miny, x2 - minx, y2 - miny, layer) for x1, y1, x2, y2, layer in out]


def _layer_gate_segs(all_segs, rules):
    """大图性能保护：优先只保留植物图层段；无匹配图层时回退到全部段。"""
    tokens = [str(t).upper() for t in (rules.get("plant_layer_tokens") or [])]
    if not tokens:
        return all_segs
    gated = [s for s in all_segs if any(tok in str(s[4] or "").upper() for tok in tokens)]
    return gated if gated else all_segs


def block_geom_fingerprint_candidates(data, rules, records=None):
    """对块名无法映射的植物图例块做几何指纹分类（final_quantity=false）。

    优先使用 cad_scan --with-block-geom 提取的块定义内部几何；没有块定义
    几何时退回到多次插入点的近邻几何取样。大圆+中心点→乔木，多圆团簇→灌木，
    连续条带→地被/绿篱。输出候选，不产生任何数量。
    """
    if records is None:
        records = read_records(data)
    inset: dict[str, list[tuple[float, float]]] = {}
    name_layer_hits: dict[str, int] = {}
    plant_insert_tokens = [str(t).upper() for t in (rules.get("plant_insert_layer_tokens") or rules.get("plant_layer_tokens") or [])]
    for rec in records:
        if str(rec.get("kind", "")).upper() != "INSERT":
            continue
        name = compact(rec.get("text", ""))
        if not name or rec.get("x") is None or rec.get("y") is None:
            continue
        inset.setdefault(name, []).append((float(rec["x"]), float(rec["y"])))
        if plant_insert_tokens and any(tok in str(rec.get("layer", "") or "").upper() for tok in plant_insert_tokens):
            name_layer_hits[name] = name_layer_hits.get(name, 0) + 1
    if not inset:
        return []

    meta = data.get("meta") or {}
    block_geoms = meta.get("block_geometries") or {}
    block_defs = {k: v for k, v in block_geoms.items() if isinstance(v, dict) and v.get("segments")}

    cfg = rules.get("plant_geom") or {}
    scale = _detect_scale(data, records)
    radius = float(cfg.get("radius") or 1200) * scale
    min_inst = int(cfg.get("min_instances") or 3)
    req_ratio = float(cfg.get("required_vote_ratio") or 0.6)
    use_block_first = bool(cfg.get("prefer_block_geometry", True))
    cap = int(cfg.get("max_candidates") or 200)
    conf_geom = float((rules.get("confidence") or {}).get("geometry_pattern", 0.86))
    infer_conf = float(cfg.get("inferred_confidence") or 0.62)

    all_segs = []
    for _fi, _si, layer, seg in iter_geometry(data):
        coords = tuple(_num(v) for v in seg[:4])
        if any(c is None for c in coords):
            continue
        all_segs.append((coords[0], coords[1], coords[2], coords[3], layer))
    all_segs = _layer_gate_segs(all_segs, rules)

    exclude_tokens = [str(t).upper() for t in (rules.get("plant_block_exclude_tokens") or [])]
    min_layer_ratio = float(cfg.get("min_insert_plant_layer_ratio") or 0.0)
    block_def_names = set(block_defs.keys())

    out = []
    for name, pts in inset.items():
        upper_name = name.upper()
        if any(tok and tok in upper_name for tok in exclude_tokens) and name not in block_def_names:
            continue
        if plant_classify_by_block(name, rules)[0]:
            continue
        if len(pts) < min_inst and name not in block_defs:
            continue
        if name not in block_def_names and min_layer_ratio > 0.0 and plant_insert_tokens:
            ratio = name_layer_hits.get(name, 0) / max(len(pts), 1)
            if ratio < min_layer_ratio:
                continue
        if len(out) >= cap:
            continue
        supports = []
        # 1) 块定义内部几何：同一个块定义本身就是强样本，优先采用
        if use_block_first and name in block_defs:
            bgeo = block_defs[name]
            local = _shifted_to_local(bgeo.get("segments") or [])
            feat = _local_shape_features([(s[0], s[1], s[2], s[3]) for s in local], rules, scale=1.0)
            if feat:
                cat, token = _fingerprint_classify(feat)
                if cat:
                    supports.append({"coord": None, "bbox": feat["bbox"],
                                     "category": cat, "matched_token": token,
                                     "round_score": feat["round_score"],
                                     "roundish_components": feat["roundish_components"],
                                     "elongated": feat["elongated"],
                                     "segment_count": feat["segment_count"],
                                     "source": "block_definition"})
        # 2) 多插入点近邻几何取样
        for px, py in pts:
            if supports and all(s.get("source") == "block_definition" for s in supports):
                break  # 已有块定义几何，不需近邻取样
            local = [s for s in all_segs
                     if _seg_in_radius(s[0], s[1], s[2], s[3], px, py, radius)]
            shifted = [(s[0]-px, s[1]-py, s[2]-px, s[3]-py, s[4]) for s in local]
            feat = _local_shape_features(shifted, rules, scale=scale)
            if not feat:
                continue
            cat, token = _fingerprint_classify(feat)
            if not cat:
                continue
            supports.append({"coord": [round(px, 3), round(py, 3)], "bbox": feat["bbox"],
                             "category": cat, "matched_token": token,
                             "round_score": feat["round_score"],
                             "roundish_components": feat["roundish_components"],
                             "elongated": feat["elongated"],
                             "segment_count": feat["segment_count"],
                             "source": "nearby_segments"})
        if not supports:
            continue
        votes: dict[str, int] = {}
        for s in supports:
            votes[s["category"]] = votes.get(s["category"], 0) + 1
        category = max(sorted(votes), key=lambda c: (votes[c], {"乔木": 2, "灌木": 1, "地被": 0}.get(c, 0)))
        token = next((s["matched_token"] for s in supports if s["category"] == category), "geom_fingerprint")
        vote_ratio = votes[category] / max(len(supports), 1)
        has_block = any(s.get("source") == "block_definition" for s in supports)
        strong = (has_block and votes[category] >= 1) or (votes[category] >= 2 and vote_ratio >= req_ratio)
        confidence = round((conf_geom if strong else infer_conf) * min(1.0, vote_ratio + 0.2), 3)
        layer = _top_layer(all_segs)
        sample = supports[:8]
        row = {
            "type": "plant_legend", "category": category, "system": "planting",
            "name": name, "block_name": name, "plant": name,
            "matched_token": token, "layer": layer,
            "file": data_file_name(data, 0), "sheet": None,
            "instance_count": len(pts), "support_count": len(supports),
            "confidence": confidence, "method": "block_geom_fingerprint",
            "status": "candidate" if strong else "review",
            "review_reasons": [] if strong else ["low_confidence_inference"],
            "review_reason": "" if strong else "几何指纹支持度不足，需人工复核",
            "scale": scale,
            "evidence": [{"kind": "block_geom_fingerprint", "value": name,
                          "instance_count": len(pts), "support_count": len(supports),
                          "vote": votes, "category": category, "scale": scale,
                          "supports": sample}],
        }
        out.append(row)
    return out


def _rec_xy(rec):
    x, y = rec.get("x"), rec.get("y")
    try:
        if x is None or y is None:
            return None
        return float(x), float(y)
    except (TypeError, ValueError):
        return None


def link_plant_schedule(records, block_fp_rows, rules):
    """把植物块候选（块名或几何指纹）与苗木表/种植图例文字做近邻交叉验证。

    输入：完整文字记录 + 带坐标的植物块候选（plant_block_legends 或 plant_block_fingerprints）。
    输出：(增强后的 rows, 交叉验证匹配 matches)。
    仅关联坐标，不产生数量；不一致时把该候选降级 review。
    """
    cfg = rules.get("plant_schedule_link") or {}
    enable = bool(cfg.get("enable", True))
    radius = float(cfg.get("radius") or 1500)
    max_matches = int(cfg.get("max_matches") or 500)
    if not enable:
        return block_fp_rows, []

    schedule = []
    for rec in records:
        if str(rec.get("kind", "")).upper() == "INSERT":
            continue
        label, token = plant_classify(rec.get("text", ""), rules)
        if not label:
            continue
        pt = _rec_xy(rec)
        if pt is None:
            continue
        schedule.append((rec, label, token, pt))

    matches = []
    out = []
    for row in block_fp_rows:
        hits = []
        seen = set()
        coords = []
        for ev in (row.get("evidence") or []):
            for sup in (ev.get("supports") or []):
                c = sup.get("coord")
                if isinstance(c, (list, tuple)) and len(c) >= 2:
                    try:
                        coords.append((float(c[0]), float(c[1])))
                    except (TypeError, ValueError):
                        continue
        for cx, cy in coords:
            for rec, label, token, (rx, ry) in schedule:
                if (cx - rx) ** 2 + (cy - ry) ** 2 > radius * radius:
                    continue
                key = (rec.get("text"), round(rx, 3), round(ry, 3))
                if key in seen:
                    continue
                seen.add(key)
                hits.append({"text": rec.get("text"), "category": label, "matched_token": token,
                             "coord": [round(rx, 3), round(ry, 3)]})
        if not hits:
            out.append(row)
            continue
        best = next((h for h in hits if h["category"] == row.get("category")), hits[0])
        consistent = best["category"] == row.get("category")
        row = dict(row)
        row["linked_plant"] = best["text"]
        row["linked_plant_category"] = best["category"]
        row["link_count"] = len(hits)
        row["link_status"] = "consistent" if consistent else "conflict"
        if not consistent:
            row["status"] = "review"
            row["review_reason"] = "图例块几何与附近苗木表分类不一致，需人工复核"
            row["review_reasons"] = row.get("review_reasons") or []
            if "low_confidence_inference" not in row["review_reasons"]:
                row["review_reasons"].append("low_confidence_inference")
        out.append(row)
        matches.append({
            "type": "plant_schedule_link", "category": row.get("category"), "system": "planting",
            "raw": best["text"], "matched_token": best["matched_token"],
            "layer": row.get("layer"), "file": row.get("file"), "sheet": row.get("sheet"),
            "x": best["coord"][0], "y": best["coord"][1],
            "confidence": row.get("confidence"), "status": row.get("status"),
            "link_status": row.get("link_status"), "block_name": row.get("name"),
            "evidence": [{"kind": "plant_schedule_link", "block_name": row.get("name") or row.get("plant"),
                          "linked_plant": best["text"], "linked_category": best["category"],
                          "coord": best["coord"], "link_count": len(hits)}],
        })
        if len(matches) >= max_matches:
            break
    return out, matches


_LEGEND_STOP = {
    "图例", "表", "清单", "一览表", "编号", "苗木", "植物", "绿植", "种植", "绿化",
    "苗木图例", "植物图例", "地被图例", "灌木图例", "乔木图例", "种植图例", "草坪图例",
    "绿篱图例", "球类图例", "草皮图例", "色带图例", "乔", "灌", "地被", "乔木", "灌木",
    "落叶乔木", "常绿乔木", "球类", "绿篱", "竹类", "其他", "草花", "色带", "栽植",
    "配置", "单位", "比例", "规格", "密度",
}
_LEGEND_SPEC_RE = re.compile(
    r"(?:胸径|地径|冠幅|冠径|蓬径|高度|株高|土球|分枝点|盆数|密度)?"
    r"[ΦφфDØø]?\s*\d+(?:\.\d+)?\s*"
    r"(?:cm|mm|m|厘米|毫米|米|株/m2|盆/m2|棵/㎡|株/㎡|袋/m2|桶/m2|盆/㎡|kg/m2)?"
)
_LEGEND_RANGE_RE = re.compile(r"^\d+(?:[-—/×x·*.]\d+)?$")

def parse_plant_legend(raw: str) -> tuple[str, str]:
    """把苗木/植物图例文字拆成(植物名, 规格串)；拆不出时回退原文。

    例：'苗木图例 1-10 香樟 φ15cm' -> ('香樟', 'φ15cm')
        '地被图例 小叶黄杨 25盆/m2'  -> ('小叶黄杨', '25盆/m2')
    只做识图候选清洗，不算量、不生成数量。
    """
    text = compact(raw, 240)
    name: list[str] = []
    specs: list[str] = []
    for tok in re.split(r"\s+", text):
        t = tok.strip()
        if not t or t in _LEGEND_STOP:
            continue
        if _LEGEND_RANGE_RE.match(t):
            continue
        if _LEGEND_SPEC_RE.search(t):
            specs.append(t)
        else:
            name.append(t)
    if not name:
        return raw, ";".join(specs)
    return " ".join(name), ";".join(specs)


_PLANT_CTX_RE = re.compile(r"[苗木植物图例乔灌地被树花竹松柏枫梅槐楠桂梓榆桐杨柳杉樱海棠玉兰紫薇黄杨月季麦冬鸢尾]")
_AUDIT_HEAD_TAILS = ("图", "表", "说明", "平面", "立面", "详图", "设计", "比例", "单位", "图纸", "配置图", "平面图", "清单", "目录", "索引")
_PLANT_TOK_RE = re.compile(r"[苗木植物种植绿植乔灌地被树花竹松柏枫梅槐楠桂梓榆桐杨柳杉樱海棠玉兰紫薇黄杨月季麦冬鸢尾]")
_CJK_RE = re.compile(r"[\u4e00-\u9fff]")

def plant_coverage_audit(records, rules, limit: int = 30) -> dict:
    """词库覆盖审计：列出“带种植/图例上下文但没分到类”的候选词频（仅审计，不算量）。

    用于快速发现具体设计院植物名还没进词库的情况，方便补 rules.json 或按院覆盖。
    """
    miss: dict[str, int] = {}
    samples: dict[str, str] = {}
    for rec in records:
        text = compact(rec.get("text") or "", 240)
        if not text or plant_classify(text, rules)[0]:
            continue
        if not _PLANT_CTX_RE.search(text):
            continue
        toks = [x.strip() for x in re.split(r"[\s,;:：()（）\[\]·/–—-]+", text)]
        for tok in toks:
            if len(tok) < 1 or tok in _LEGEND_STOP or _LEGEND_RANGE_RE.match(tok) or _LEGEND_SPEC_RE.search(tok):
                continue
            if not (_CJK_RE.search(tok) or (tok.isalpha() and len(tok) >= 2)):
                continue
            if _CJK_RE.search(tok) and not _PLANT_TOK_RE.search(tok):
                continue
            if _CJK_RE.search(tok) and tok.endswith(_AUDIT_HEAD_TAILS):
                continue
            miss[tok] = miss.get(tok, 0) + 1
            if tok not in samples:
                samples[tok] = text[:80]
    top = [{"word": w, "count": c, "sample": samples[w]} for w, c in sorted(miss.items(), key=lambda kv: (-kv[1], kv[0]))[:limit]]
    return {"unclassified_legend_words": len(miss), "top": top, "note": "仅审计词库覆盖，不输出数量/算量。"}


def _noise_name_plant(plant_name: str, token: str, rules: dict) -> bool:
    """并列人名/非植物噪声判据（真图驱动，0.39.2）。

    真图教训：sample-road种植总图图签「signer-A signer-B」被单字 token「李」判成乔木。
    判据：植物名含空格（多段）且**没有任何一段**命中长度≥2 的植物词 → 不是植物。
    反例保护：「杉木柱 末口」第一段命中「杉木」（≥2 字）→ 真植物构件，必须保留。
    """
    parts = [p for p in re.split(r"\s+", str(plant_name or "")) if p]
    if len(parts) < 2:
        return False
    for p in parts:
        lab, tok = plant_classify(p, rules)
        if lab and len(re.sub(r"\s+", "", str(tok))) >= 2:
            return False
    return True


_NOTE_PUNCT_RE = re.compile(r"[。；，、,;:/]|[（(]|\\U\+")
# 硬景设施/小品不是植物（真图："成品花钵"9 条、"树池"3 条曾混进图例；用完整词避免误伤"丰花月季"）
_FURNITURE_RE = re.compile(r"花钵|花箱|树池|景墙|座椅|坐凳|廊架|车棚|亭|雕塑|水池|喷泉|台阶|坡道|排水沟|雨水口|层次")
_DRAWING_TAIL = ("图", "详图", "平面图", "说明", "表", "大样", "做法", "规格", "剖面", "立面",
                 "示意图", "形式", "配置图", "索引", "目录", "移植")
_MATERIAL_RE = re.compile(
    r"花岗岩|荔枝面|芝麻[白灰黑]|黄锈石|锈石|透水砖|水泥|混凝土|沥青|卵石|碎石|板材|面砖|"
    r"火烧面|光面|盲道|路缘石|植草砖|大理石|砖|砂|骨料")
# 真植物名长度上限（真图实测：sample-road 147 种图例里，>8 字的全是说明句/图名/铺装材料）
PLANT_NAME_MAX_LEN = 8


def _noise_note_nonplant(plant_name: str) -> str:
    """说明句/图名/铺装材料噪声判据（真图驱动，0.39.2）→ 返回原因串，空串=通过。

    真图教训：sample-road绿化设计说明的整段句子（"1.3、清除现场碎石…"）与铺装材料名
    （"芝麻白荔枝面花岗岩"19 次、"黄锈石荔枝面花岗岩（收边）"14 次、"杉树皮卷用棕榈绳
    捆束"13 次）都被词库子串命中成了"植物图例"。三条判据各自可追溯、不静默。
    """
    n = str(plant_name or "").strip()
    if not n:
        return "empty_name"
    if len(n) > PLANT_NAME_MAX_LEN:
        return "too_long_not_plant_name"
    if _NOTE_PUNCT_RE.search(n):
        return "punctuation_note"
    if n.endswith(_DRAWING_TAIL):
        return "drawing_title"
    if _MATERIAL_RE.search(n):
        return "hardscape_material"
    if _FURNITURE_RE.search(n):
        return "hardscape_furniture"
    return ""


def plant_legend_candidates(records, rules, stats: dict | None = None):
    out, seen = [], set()
    cap = int((rules.get("max_plant_legends") or 2000))
    for rec in records:
        label, token = plant_classify(rec["text"], rules)
        if not label:
            continue
        subject = rec["text"][:60]
        key = (context_of(rec), label, subject, rec.get("layer"), rec.get("x"), rec.get("y"))
        if key in seen:
            continue
        seen.add(key)
        rec_conf = float((rules.get("confidence") or {}).get("direct_label", 0.95))
        reasons = []
        if not rec.get("layer"):
            reasons.append("missing_layer")
        if rec.get("x") is None or rec.get("y") is None:
            reasons.append("ambiguous_text_binding")
        plant_name, spec = parse_plant_legend(rec["text"])
        if _noise_name_plant(plant_name, token, rules):
            if stats is not None:
                stats["name_noise_excluded"] = stats.get("name_noise_excluded", 0) + 1
            continue  # 图签并列人名等非植物噪声（不冒充图例，计数可追溯）
        noise = _noise_note_nonplant(plant_name)
        if noise:
            if stats is not None:
                stats["note_noise_excluded"] = stats.get("note_noise_excluded", 0) + 1
                stats[f"noise::{noise}"] = stats.get(f"noise::{noise}", 0) + 1
            continue  # 说明句/图名/铺装材料不是植物图例（不冒充图例，计数可追溯）
        row = {
            "type": "plant_legend", "category": label, "system": "planting",
            "plant": plant_name, "legend_raw": rec["text"], "spec": spec,
            "matched_token": token, "layer": rec.get("layer"),
            "file": rec.get("file_name"), "sheet": rec.get("sheet"), "x": rec.get("x"), "y": rec.get("y"),
            "confidence": round(rec_conf, 4),
            "status": "review" if reasons else "candidate",
            "review_reasons": reasons, "review_reason": "; ".join(reasons),
            "evidence": [evidence_of(rec)],
        }
        out.append(row)
        if len(out) >= cap:
            break
    return out


def _paving_components(edges):
    """按边归并连通分量，返回各分量闭合环与尺寸信息。"""
    class UF:
        def __init__(self):
            self.parent: dict[tuple[int, int], tuple[int, int]] = {}
        def find(self, x):
            parent = self.parent
            root = x
            while parent.get(root, root) != root:
                root = parent[root]
            while parent.get(x, x) != x:
                nxt = parent.get(x, x)
                parent[x] = root
                x = nxt
            return root
        def union(self, a, b):
            parent = self.parent
            parent.setdefault(a, a)
            parent.setdefault(b, b)
            ra, rb = self.find(a), self.find(b)
            if ra != rb:
                parent[rb] = ra

    uf = UF()
    for k1, k2, _raw in edges:
        uf.union(k1, k2)
    comp_edges: dict[tuple, list[tuple]] = {}
    for k1, k2, raw in edges:
        comp_edges.setdefault(uf.find(k1), []).append((k1, k2, raw))
    out = []
    for root, eds in comp_edges.items():
        node_set: set[tuple] = set()
        xs, ys = [], []
        length = 0.0
        for k1, k2, raw in eds:
            node_set.add(k1)
            node_set.add(k2)
            x1, y1, x2, y2 = raw
            xs += [x1, x2]
            ys += [y1, y2]
            length += ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        vcount, ecount = len(node_set), len(eds)
        cycle_count = max(0, ecount - vcount + 1) if vcount >= 3 else 0
        minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
        w, h = max(0.0, maxx - minx), max(0.0, maxy - miny)
        side = max(w, h, 1.0)
        out.append({
            "vertices_count": vcount,
            "edges_count": ecount,
            "cycle_candidates": cycle_count,
            "bbox": [round(minx, 3), round(miny, 3), round(maxx, 3), round(maxy, 3)],
            "width": round(w, 3),
            "height": round(h, 3),
            "aspect": round(side / max(min(w, h), 1.0), 3),
            "total_length": round(length, 3),
            "center": [round((minx + maxx) / 2.0, 3), round((miny + maxy) / 2.0, 3)],
        })
    out.sort(key=lambda c: (-c["cycle_candidates"], -c["width"] * c["height"]))
    return out


def _cluster_regions(rings, gap, layer="", label_tpl="{layer}|R{idx}|{rings}环"):
    """按环中心点近邻聚合成铺装区块候选（不含面积，仅范围）。"""
    regions: list[dict] = []
    for ring in rings:
        cx, cy = ring["center"]
        placed = None
        for region in regions:
            rx, ry = region["center"]
            if (cx - rx) ** 2 + (cy - ry) ** 2 <= gap * gap:
                placed = region
                break
        if placed is None:
            placed = {"center": [cx, cy], "members": [], "bbox": ring["bbox"][:]}
            regions.append(placed)
        placed["members"].append(ring)
        xs = [placed["bbox"][0], placed["bbox"][2], ring["bbox"][0], ring["bbox"][2]]
        ys = [placed["bbox"][1], placed["bbox"][3], ring["bbox"][1], ring["bbox"][3]]
        placed["bbox"] = [min(xs), min(ys), max(xs), max(ys)]
        placed["center"] = ring["center"][:]
    out = []
    for idx, region in enumerate(regions):
        xs, ys = region["bbox"][0], region["bbox"][1]
        xs2, ys2 = region["bbox"][2], region["bbox"][3]
        ring_count = sum(m["cycle_candidates"] for m in region["members"])
        try:
            review_label = label_tpl.format(layer=layer, idx=idx + 1, rings=ring_count)
        except Exception:
            review_label = f"{layer}|R{idx + 1}|{ring_count}环"
        out.append({
            "region_index": idx + 1,
            "review_label": review_label,
            "anchor_center": [round((xs + xs2) / 2.0, 3), round((ys + ys2) / 2.0, 3)],
            "ring_count": ring_count,
            "member_count": len(region["members"]),
            "bbox": [round(v, 3) for v in region["bbox"]],
            "width": round(xs2 - xs, 3),
            "height": round(ys2 - ys, 3),
            "approx_span": round(((xs2 - xs) ** 2 + (ys2 - ys) ** 2) ** 0.5, 3),
        })
    return out


def _closed_ring_candidates(data, rules, *, row_type, category, system, layer_tokens,
                               max_key, filter_key, incomplete_reason="图层几何未能形成闭合环"):
    """图层几何做轻量闭合环检测通用实现（铺装/绿地均可，final_quantity=false）。

    算法：端点在容差内吸附成节点，按线段建无向图；对每个连通分量统计
    独立环数 = max(0, E - V + 1)（仅作候选）。随后按 bbox 尺寸/长宽比过滤
    “细缝/装饰”小环，把相邻合规环聚合成区块候选。全程不计算面积。
    """
    tolerance = float(rules.get("geometry_close_tolerance") or 50)
    cap = int(rules.get(max_key) or 2000)
    filt = rules.get(filter_key) or {}
    min_bbox = float(filt.get("min_bbox") or 500)
    max_aspect = float(filt.get("max_aspect") or 20)
    region_gap = float(filt.get("region_gap") or 2000)
    min_region_rings = int(filt.get("min_rings_per_region") or 2)
    max_regions = int(filt.get("max_regions") or 200)
    max_filtered = int(filt.get("max_filtered_rings") or 400)
    upper_tokens = [str(t).upper() for t in layer_tokens]
    by_layer: dict[str, list[tuple[float, float, float, float]]] = {}
    for fi, _si, layer, seg in iter_geometry(data):
        if not layer:
            continue
        up = layer.upper()
        if not any(tok in up for tok in upper_tokens):
            continue
        coords = tuple(_num(v) for v in seg[:4])
        if any(c is None for c in coords):
            continue
        by_layer.setdefault(layer, []).append(coords)  # type: ignore[arg-type]

    def _key(v: float) -> int:
        return int(round(v / tolerance))

    out = []
    for layer, segs in by_layer.items():
        fname = data_file_name(data, 0)
        edges: list[tuple] = []
        for x1, y1, x2, y2 in segs:
            k1, k2 = (_key(x1), _key(y1)), (_key(x2), _key(y2))
            if k1 == k2:
                continue  # 零长/自闭环，跳过，避免误判
            edges.append((k1, k2, (x1, y1, x2, y2)))
        comps = _paving_components(edges)
        rings_main, rings_detail = [], []
        for comp in comps:
            if comp["cycle_candidates"] <= 0:
                continue
            largish = comp["bbox"][2] - comp["bbox"][0] >= min_bbox and comp["bbox"][3] - comp["bbox"][1] >= min_bbox
            not_slit = comp["aspect"] <= max_aspect
            if largish and not_slit:
                rings_main.append(comp)
            elif len(rings_detail) < max_filtered:
                rings_detail.append(comp)
        label_tpl = filt.get("review_label_tpl") or "{layer}|R{idx}|{rings}环"
        regions = _cluster_regions(rings_main, region_gap, layer=layer, label_tpl=label_tpl)
        regions = [r for r in regions if r["ring_count"] >= min_region_rings][:max_regions]
        xs, ys = [], []
        for x1, y1, x2, y2 in segs:
            xs += [x1, x2]
            ys += [y1, y2]
        bbox = [min(xs), min(ys), max(xs), max(ys)] if xs else None
        main_rings = sum(c["cycle_candidates"] for c in rings_main)
        closed = main_rings > 0
        row = {
            "type": row_type, "category": category, "system": system,
            "layer": layer, "file": fname,
            "segment_count": len(segs),
            "closed_ring_candidates": main_rings,
            "filtered_ring_candidates": sum(c["cycle_candidates"] for c in rings_detail),
            "bbox": [round(v, 3) for v in bbox] if bbox else None,
            "closed_ring_candidates_scaled": [{
                "cycle_candidates": c["cycle_candidates"],
                "bbox": c["bbox"], "width": c["width"], "height": c["height"],
                "aspect": c["aspect"], "vertices_count": c["vertices_count"],
                "edges_count": c["edges_count"],
            } for c in rings_main[:120]],
            "region_candidates": regions,
            "confidence": round(float((rules.get("confidence") or {}).get("geometry_pattern", 0.86)), 4),
            "status": "candidate" if closed else "review",
            "review_reasons": [] if closed else ["incomplete_geometry"],
            "review_reason": "" if closed else incomplete_reason,
            "evidence": [{"layer": layer, "kind": "geometry", "segment_count": len(segs), "bbox": bbox,
                          "components": comps[:40], "regions": regions}],
        }
        out.append(row)
        if len(out) >= cap:
            break
    return out


def paving_closed_candidates(data, rules):
    """硬景铺装图层几何做轻量闭合环检测（final_quantity=false）。

    复用通用闭合环实现，layer 词表用 `paving_layer_tokens`，过滤参数用 `paving_filter`。
    """
    return _closed_ring_candidates(
        data, rules,
        row_type="paving_closed_area", category="paving", system="paving",
        layer_tokens=rules.get("paving_layer_tokens") or [],
        max_key="max_paving_areas", filter_key="paving_filter",
        incomplete_reason="铺装图层几何未能形成闭合环",
    )


def green_area_candidates(data, rules):
    """绿地/地被图层几何做轻量闭合环候选（final_quantity=false）。

    复用通用闭合环实现，layer 词表用 `plant_layer_tokens`，过滤参数用 `green_area_filter`；
    只在“绿地/地被/灌木/草坪/绿化”类图层上找闭合边界，不输出面积、不算量。
    """
    return _closed_ring_candidates(
        data, rules,
        row_type="green_area", category="green_area", system="planting",
        layer_tokens=rules.get("plant_layer_tokens") or [],
        max_key="max_green_areas", filter_key="green_area_filter",
        incomplete_reason="绿地图层几何未能形成闭合环",
    )


def pdf_geometry_candidates(data, rules):
    """PDF 矢量几何仅作 review 证据候选（final_quantity=false）。

    PDF 无图层语义，捞到的线/矩形/曲线不进铺装/绿地闭合域，只输出页级段数、
    包围盒与复核提示，供人工判断该页是否有矢量底图。
    """
    seg_files = data.get("pdf_geometry_segments") or []
    if not isinstance(seg_files, list):
        return []
    cap = int((rules.get("max_pdf_geometry") or 2000))
    out = []
    fname = data_file_name(data, 0)
    for entry in seg_files:
        if not isinstance(entry, dict):
            continue
        page = int(entry.get("page") or 1)
        segs = entry.get("segments") or []
        valid = [sv for sv in segs if isinstance(sv, (list, tuple)) and len(sv) >= 4]
        if not valid:
            continue
        xs, ys = [], []
        for sv in valid[:20000]:
            xs += [float(sv[0]), float(sv[2])]
            ys += [float(sv[1]), float(sv[3])]
        bbox = [round(min(xs), 3), round(min(ys), 3), round(max(xs), 3), round(max(ys), 3)]
        row = {
            "type": "pdf_geometry", "category": "geometry", "system": "pdf",
            "layer": None, "file": fname, "sheet": page, "page": page,
            "segment_count": len(valid),
            "bbox": bbox,
            "confidence": 0.5,
            "status": "review",
            "review_reasons": ["pdf_no_layer_geometry"],
            "review_reason": "PDF 矢量几何无图层语义，仅作证据，不参与闭合域/算量",
            "evidence": [{"kind": "pdf_geometry", "page": page, "segment_count": len(valid),
                          "bbox": bbox, "sample": valid[:12]}],
        }
        out.append(row)
        if len(out) >= cap:
            break
    return out


def hardscape_candidates(records, rules):
    out, seen = [], set()
    tokens = rules.get("hardscape_text_tokens") or []
    for rec in records:
        hit = None
        for token in tokens:
            if str(token) in rec["text"]:
                hit = token
                break
        if not hit:
            continue
        key = (context_of(rec), hit, rec.get("layer"), rec.get("x"), rec.get("y"))
        if key in seen:
            continue
        seen.add(key)
        out.append({"type": "hardscape", "category": "hardscape", "system": "furniture", "raw": rec["text"][:60], "matched_token": hit, "layer": rec.get("layer"), "file": rec.get("file_name"), "sheet": rec.get("sheet"), "x": rec.get("x"), "y": rec.get("y"), "confidence": float((rules.get("confidence") or {}).get("pattern_match", 0.78)), "status": "candidate", "evidence": [evidence_of(rec)]})
    return out


# ---------- DXF 块内铺装/块引用回退（与 yuanlin_qty 0.4.37 等价上移） ----------
DEFAULT_PAVING_TOKENS = ("景观铺地", "铺装", "铺地", "园路", "波打", "收边", "PAVING", "HARDSCAPE", "PAVE")


def _ensure_vendor():
    vendor = ROOT / "vendor"
    if vendor.exists() and str(vendor) not in sys.path:
        sys.path.insert(0, str(vendor))


def _dxf_unit_info(doc):
    table = {1: (25.4, "inch"), 2: (304.8, "foot"), 4: (1.0, "mm"),
             5: (10.0, "cm"), 6: (1000.0, "m")}
    try:
        item = table.get(int(doc.header.get("$INSUNITS") or 0))
    except Exception:
        item = None
    if not item:
        return {"drawing_unit": None, "drawing_mm_per_unit": None, "source": "DXF $INSUNITS"}
    return {"drawing_unit": item[1], "drawing_mm_per_unit": item[0], "source": "DXF $INSUNITS"}


def _dxf_block_ref_records(path):
    """可选 DXF 回退：读取顶层 INSERT 坐标；只取模型空间，不展开嵌套。"""
    _ensure_vendor()
    try:
        import ezdxf  # type: ignore
    except Exception as exc:
        return {"records": [], "warnings": [f"ezdxf 不可用：{exc}"], "insert_count": 0}
    try:
        doc = ezdxf.readfile(str(path))
    except Exception as exc:
        return {"records": [], "warnings": [f"DXF 读取失败：{exc}"], "insert_count": 0}
    recs, warnings = [], []
    try:
        for entity in doc.modelspace().query("INSERT"):
            name = str(getattr(entity.dxf, "name", "") or "").strip()
            if not name:
                continue
            try:
                pt = entity.dxf.insert
                recs.append({"kind": "INSERT", "text": name,
                             "x": float(pt[0]), "y": float(pt[1]),
                             "layer": str(getattr(entity.dxf, "layer", "") or ""),
                             "source": "dxf_block_ref"})
            except Exception:
                continue
            if len(recs) >= 200000:
                warnings.append("DXF INSERT 超过安全上限，已截断")
                break
    except Exception as exc:
        warnings.append(f"DXF INSERT 读取失败：{exc}")
    return {"records": recs, "warnings": warnings, "insert_count": len(recs)}


def _poly_area(poly):
    s = 0.0
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        s += x1 * y2 - x2 * y1
    return s / 2.0


def _poly_key(poly, digits=6):
    """闭合环去重键：忽略起点和方向，只保留吸附后的点集。"""
    pts = [(round(float(x), digits), round(float(y), digits)) for x, y in poly]
    if len(pts) > 1 and pts[0] == pts[-1]:
        pts = pts[:-1]
    return tuple(sorted(pts))


def _faces(segs, tol):
    """轻量环面提取：把线段端点吸附成图，按逆时针邻接追踪边界，去重取多边形。"""
    key = lambda x, y: (round(x / max(tol, 1e-9)), round(y / max(tol, 1e-9)))
    nodes, edges = {}, []
    for s in segs:
        x1, y1, x2, y2 = s
        a, b = key(x1, y1), key(x2, y2)
        if a == b:
            continue
        nodes.setdefault(a, (x1, y1))
        nodes.setdefault(b, (x2, y2))
        edges.append((a, b))
    if not nodes:
        return []
    pts, idx = nodes, list(nodes)
    pidx = {p: i for i, p in enumerate(idx)}
    adj = [[] for _ in idx]
    edges = {(pidx[a], pidx[b]) for a, b in edges}
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    for i in range(len(idx)):
        adj[i].sort(key=lambda j: math.atan2(pts[idx[j]][1] - pts[idx[i]][1], pts[idx[j]][0] - pts[idx[i]][0]))
    pos = {}
    for i in range(len(idx)):
        for k, j in enumerate(adj[i]):
            pos[i, j] = k
    used, out = set(), []
    guard_max = len(idx) ** 2 + 8
    for a in range(len(idx)):
        for b in list(adj[a]):
            if (a, b) in used:
                continue
            path, cur, nx, guard = [], a, b, 0
            while (cur, nx) not in used and guard < guard_max:
                used.add((cur, nx))
                path.append(cur)
                guard += 1
                ns = adj[nx]
                k = pos.get((nx, cur))
                if k is None:
                    break
                nxt = ns[(k + 1) % len(ns)]
                cur, nx = nx, nxt
            if cur == a and nxt == b and len(path) >= 3 and len(set(path)) == len(path):
                poly = [pts[idx[i]] for i in path] + [pts[idx[a]]]
                ar = _poly_area(poly)
                if abs(ar) > 1e-6:
                    out.append((poly, ar))
    seen, res = set(), []
    for poly, ar in out:
        key2 = _poly_key(poly)
        if key2 in seen:
            continue
        seen.add(key2)
        res.append((poly, ar))
    return res


def _dxf_arc_points(start_point, end_point, bulge, max_deg=10.0):
    """把 LWPOLYLINE bulge 边展开成弦端点间的圆弧点列；保留旧实现的弧度口径。"""
    try:
        from ezdxf.math import bulge_to_arc
    except Exception:
        return []
    try:
        center, s_angle, e_angle, radius = bulge_to_arc(start_point, end_point, float(bulge))
        if radius <= 0 or not all(math.isfinite(float(v)) for v in (center[0], center[1], s_angle, e_angle, radius)):
            return []
        start_deg = math.degrees(s_angle)
        sweep = math.degrees(e_angle - s_angle)
        n = max(2, min(180, int(math.ceil(abs(sweep) / max(max_deg, 1.0)))))
        return [(center[0] + radius * math.cos(math.radians(start_deg + sweep * i / n)),
                 center[1] + radius * math.sin(math.radians(s_angle + sweep * i / n)))
                for i in range(1, n + 1)]
    except Exception:
        return []


def _dxf_arc_boundary_points(entity, max_deg=10.0):
    """ARC 边界点列（不含起点）；单独 ARC 以弦闭合后可形成 P3 候选环。"""
    try:
        cx, cy = float(entity.dxf.center.x), float(entity.dxf.center.y)
        r = float(entity.dxf.radius)
        s = float(entity.dxf.start_angle)
        e = float(entity.dxf.end_angle)
        if r <= 0 or not all(math.isfinite(v) for v in (cx, cy, r, s, e)):
            return []
        sweep = e - s
        while sweep <= 0:
            sweep += 360.0
        n = max(2, min(180, int(math.ceil(sweep / max(max_deg, 1.0)))))
        return [(cx + r * math.cos(math.radians(s + sweep * i / n)),
                 cy + r * math.sin(math.radians(s + sweep * i / n)))
                for i in range(1, n + 1)]
    except Exception:
        return []


def _dxf_hatch_boundary_points(path, max_deg=10.0):
    """HATCH 边界点列：支持 PolylinePath 与 Line/Arc EdgePath；只取边界。"""
    pts = []
    if hasattr(path, 'vertices'):
        for v in getattr(path, 'vertices', []) or []:
            try:
                x, y = float(v[0]), float(v[1])
                if math.isfinite(x) and math.isfinite(y):
                    pts.append((x, y))
            except Exception:
                pass
        if len(pts) >= 3 and pts[0] != pts[-1]:
            pts.append(pts[0])
        return pts
    if not hasattr(path, 'edges'):
        return []
    for edge in getattr(path, 'edges', []) or []:
        typ = str(getattr(edge, 'EDGE_TYPE', getattr(edge, 'type', '')) or '').lower()
        try:
            if typ == 'line':
                for v in (edge.start_point, edge.end_point):
                    x, y = float(v[0]), float(v[1])
                    if math.isfinite(x) and math.isfinite(y):
                        pts.append((x, y))
            elif typ == 'arc':
                a0 = float(edge.start_angle)
                a1 = float(edge.end_angle)
                cx, cy = float(edge.center.x), float(edge.center.y)
                r = float(edge.radius)
                sweep = a1 - a0
                while sweep <= 0:
                    sweep += 360.0
                n = max(2, min(180, int(math.ceil(sweep / max(max_deg, 1.0)))))
                pts.extend((cx + r * math.cos(math.radians(a0 + sweep * i / n)),
                            cy + r * math.sin(math.radians(a0 + sweep * i / n)))
                           for i in range(n + 1))
        except Exception:
            continue
    if len(pts) >= 3 and pts[0] != pts[-1]:
        pts.append(pts[0])
    return pts


def _dxf_block_paving_segments(path, rules):
    """展开 INSERT 变换，提取铺装块内闭合 LWPOLYLINE/POLYLINE/HATCH/ARC。

    与 yuanlin_qty 0.4.37 的 _dxf_block_paving_segments 同构；只处理命中
    铺装 token 的图层/块名，全部结果由调用方强制 P3。
    """
    _ensure_vendor()
    try:
        import ezdxf  # type: ignore
    except Exception as exc:
        return {"segments": [], "layers": [], "mm_per_unit": None, "units": {}, "warnings": [f"ezdxf 不可用：{exc}"]}

    tokens = [str(x).strip().lower() for x in (rules.get("paving_layer_tokens") or DEFAULT_PAVING_TOKENS) if str(x).strip()]
    skip_tokens = ("paving slab", "paving unit", "paver", "joint", "grout", "tile")
    segs, layers, warnings = [], [], []
    seen_entities = 0
    ring_count = 0
    try:
        doc = ezdxf.readfile(str(path))
    except Exception as exc:
        return {"segments": [], "layers": [], "mm_per_unit": None, "units": {}, "warnings": [f"DXF 读取失败：{exc}"]}
    units = _dxf_unit_info(doc)
    unit_mm_value = units.get("drawing_mm_per_unit")

    def add_ring(pts, layer_label):
        nonlocal ring_count
        clean = []
        for x, y in pts:
            if len(clean) >= 2 and abs(x - clean[-2][0]) < 1e-12 and abs(y - clean[-2][1]) < 1e-12:
                clean[-1] = (x, y)
                continue
            clean.append((x, y))
        while len(clean) > 1 and abs(clean[0][0] - clean[-1][0]) < 1e-12 and abs(clean[0][1] - clean[-1][1]) < 1e-12:
            clean.pop()
        if len(clean) < 3:
            return
        for i, (x1, y1) in enumerate(clean):
            x2, y2 = clean[(i + 1) % len(clean)]
            if abs(x1 - x2) < 1e-12 and abs(y1 - y2) < 1e-12:
                continue
            segs.append([x1, y1, x2, y2])
            layers.append(layer_label)
        ring_count += 1

    def walk(layout, matrix, path_names):
        nonlocal seen_entities, ring_count
        for entity in layout:
            seen_entities += 1
            if seen_entities > 200000 or ring_count > 5000:
                if len(warnings) < 3:
                    warnings.append("DXF 实体/闭合环超过安全上限，已截断")
                return
            typ = entity.dxftype()
            if typ in ("INSERT", "MINSERT"):
                name = str(getattr(entity.dxf, "name", "") or "")
                low_name = name.lower()
                if not name or name in path_names or any(s in low_name for s in skip_tokens):
                    continue
                try:
                    block = doc.blocks.get(name)
                except Exception:
                    continue
                try:
                    insert_matrix = entity.matrix44()
                    child_matrix = insert_matrix if matrix is None else matrix @ insert_matrix
                except Exception:
                    child_matrix = matrix
                walk(block, child_matrix, path_names + (name,))
                continue
            owner = " / ".join(path_names)
            entity_layer = str(entity.dxf.layer or "")
            effective_layer = entity_layer if entity_layer not in ("", "0") else (path_names[-1] if path_names else entity_layer)
            current_block = path_names[-1] if path_names else ""
            hay = f"{current_block} {entity_layer} {effective_layer}".lower()
            if not any(token in hay for token in tokens):
                continue
            if any(s in owner.lower() for s in skip_tokens):
                continue

            def transform_point(x, y):
                if matrix is not None:
                    p = matrix.transform((float(x), float(y), 0.0))
                    return float(p[0]), float(p[1])
                return float(x), float(y)

            def transformed(points):
                return [transform_point(x, y) for x, y in points]

            pts = []
            ring_ready = False
            try:
                if typ == "LWPOLYLINE":
                    raw = list(entity.get_points("xyb"))
                    for i, (x, y, bulge) in enumerate(raw):
                        pts.append((float(x), float(y)))
                        b = float(bulge or 0.0)
                        if abs(b) > 1e-9:
                            nx, ny = raw[(i + 1) % len(raw)][:2]
                            pts.extend(_dxf_arc_points((float(x), float(y)), (float(nx), float(ny)), b))
                    if getattr(entity, "closed", False):
                        ring_ready = True
                    elif len(pts) >= 3 and abs(pts[0][0] - pts[-1][0]) < 1e-9 and abs(pts[0][1] - pts[-1][1]) < 1e-9:
                        ring_ready = True
                elif typ == "POLYLINE" and getattr(entity, "is_closed", False):
                    vertices = list(entity.vertices)
                    for i, v in enumerate(vertices):
                        loc = v.dxf.location
                        pts.append((float(loc.x), float(loc.y)))
                        b = float(getattr(v.dxf, "bulge", 0.0) or 0.0)
                        if abs(b) > 1e-9:
                            nv = vertices[(i + 1) % len(vertices)].dxf.location
                            pts.extend(_dxf_arc_points((float(loc.x), float(loc.y)), (float(nv.x), float(nv.y)), b))
                    ring_ready = True
                elif typ == "HATCH":
                    for bp in entity.paths or []:
                        hp = _dxf_hatch_boundary_points(bp)
                        if len(hp) >= 3:
                            pts = transformed(hp)
                            add_ring(pts, f"（DXF回退）HATCH {owner} [{entity_layer or effective_layer}]" if owner else f"（DXF回退）HATCH [{entity_layer or effective_layer}]")
                    continue
                elif typ == "ARC":
                    ap = _dxf_arc_boundary_points(entity)
                    if ap:
                        start = (float(entity.dxf.center.x) + float(entity.dxf.radius) * math.cos(math.radians(float(entity.dxf.start_angle))),
                                 float(entity.dxf.center.y) + float(entity.dxf.radius) * math.sin(math.radians(float(entity.dxf.start_angle))))
                        pts = [transform_point(*start)] + transformed(ap) + [transform_point(*start)]
                        add_ring(pts, f"（DXF回退）ARC {owner} [{entity_layer or effective_layer}]" if owner else f"（DXF回退）ARC [{entity_layer or effective_layer}]")
                    continue
            except Exception as exc:
                if len(warnings) < 3:
                    warnings.append(f"DXF {typ} 边界展开失败：{exc}")
                continue
            if not ring_ready or len(pts) < 3:
                continue
            pts = transformed(pts)
            layer_label = f"（DXF回退）{owner} [{entity_layer or effective_layer}]" if owner else f"（DXF回退）{entity_layer or effective_layer or '未知铺装图层'}"
            add_ring(pts, layer_label)

    try:
        walk(doc.modelspace(), None, ())
    except Exception as exc:
        warnings.append(f"DXF 块几何展开失败：{exc}")
    return {"segments": segs, "layers": layers, "mm_per_unit": unit_mm_value,
            "units": units, "warnings": warnings}


def _source_from_paving_label(label):
    text = str(label or "")
    if text.startswith("（DXF回退）"):
        text = text[len("（DXF回退）"):]
    if text.startswith("HATCH "):
        text = text[len("HATCH "):]
    if text.startswith("ARC "):
        text = text[len("ARC "):]
    pos = text.rfind(" [")
    owner = text[:pos] if pos > 0 else ""
    layer = text[pos + 2:-1] if pos > 0 and text.endswith("]") else text
    return owner or "MODELSPACE", layer or None


def _block_paving_rows(path, rules):
    info = _dxf_block_paving_segments(path, rules)
    units = info.get("units") or {}
    mm_unit = units.get("drawing_mm_per_unit")
    try:
        tol = float(rules.get("geometry_close_tolerance") or 50) / max(float(mm_unit or 1.0), 1e-9)
    except Exception:
        tol = float(rules.get("geometry_close_tolerance") or 50)
    by_layer = {}
    for seg, layer in zip(info.get("segments") or [], info.get("layers") or []):
        if isinstance(seg, (list, tuple)) and len(seg) >= 4:
            by_layer.setdefault(str(layer or "未知铺装图层"), []).append(tuple(float(v) for v in seg[:4]))
    rows = []
    for layer_label, segs in by_layer.items():
        faces = _faces(segs, tol)
        seen, unique = set(), []
        for poly, ar in faces:
            xs = [p[0] for p in poly]
            ys = [p[1] for p in poly]
            key = (round(abs(ar), 6), tuple(round(v, 6) for v in (min(xs), min(ys), max(xs), max(ys))))
            if key in seen:
                continue
            seen.add(key)
            unique.append((poly, ar))
        for poly, ar in unique:
            if abs(ar) < 1e-6:
                continue
            source_block, layer = _source_from_paving_label(layer_label)
            xs = [p[0] for p in poly]
            ys = [p[1] for p in poly]
            rows.append({
                "type": "paving_ring", "category": "paving", "system": "paving",
                "layer": layer or layer_label, "layer_label": layer_label,
                "source_block": source_block,
                "points": [[round(float(x), 6), round(float(y), 6)] for x, y in poly],
                "point_count": len(poly), "vertex_count": max(0, len(poly) - 1),
                "closed": True,
                "area_drawing_units2": round(abs(ar), 6),
                "unit": "drawing_unit^2",
                "bbox": [round(min(xs), 6), round(min(ys), 6), round(max(xs), 6), round(max(ys), 6)],
                "confidence": 0.4, "status": "review",
                "review_note": "块内推定", "review_reason": "块内推定",
                "review_reasons": ["low_confidence_inference"],
                "final_quantity": False,
                "evidence": [{"layer": layer or layer_label, "kind": "dxf_block_ring",
                              "source_block": source_block, "point_count": len(poly),
                              "area_drawing_units2": round(abs(ar), 6)}],
            })
    rows.sort(key=lambda r: (-r["area_drawing_units2"], r.get("layer") or "", r.get("source_block") or ""))
    return rows, info


def _block_ref_rows(path):
    info = _dxf_block_ref_records(path)
    rows = []
    for rec in info.get("records") or []:
        name = str(rec.get("text") or "")
        rows.append({
            "type": "block_ref", "category": "block_ref", "system": "",
            "block_name": name, "name": name,
            "x": round(float(rec.get("x") or 0.0), 6),
            "y": round(float(rec.get("y") or 0.0), 6),
            "layer": rec.get("layer") or None,
            "source": "dxf_block_ref",
            "confidence": 0.4, "status": "review",
            "review_note": "块内推定", "review_reason": "块内推定",
            "review_reasons": ["low_confidence_inference"],
            "final_quantity": False,
            "evidence": [{"kind": "dxf_block_ref", "value": name,
                          "coord": [round(float(rec.get("x") or 0.0), 6), round(float(rec.get("y") or 0.0), 6)],
                          "layer": rec.get("layer") or None}],
        })
    return rows, info


def block_fallback_payload(path, rules, *, with_paving=False, with_refs=False):
    """只读一个 DXF，生成块内铺装环与顶层块引用回退候选。"""
    paving_rings, paving_info = ([], {}) if not with_paving else _block_paving_rows(path, rules)
    block_refs, refs_info = ([], {}) if not with_refs else _block_ref_rows(path)
    units = {}
    if with_paving:
        units = (paving_info.get("units") or {})
    if with_refs and not units:
        # block_refs 不涉及面积；仍记录 DXF 单位供下游解释坐标。
        _ensure_vendor()
        try:
            import ezdxf  # type: ignore
            units = _dxf_unit_info(ezdxf.readfile(str(path)))
        except Exception:
            units = {}
    review = []
    if paving_info.get("warnings"):
        review.extend({"type": "block_paving", "reason": str(x), "evidence": {"file": path.name}} for x in paving_info["warnings"])
    if refs_info.get("warnings"):
        review.extend({"type": "block_refs", "reason": str(x), "evidence": {"file": path.name}} for x in refs_info["warnings"])
    if with_paving:
        if paving_rings:
            review.append({"type": "block_paving", "reason": "块内推定", "evidence": {"file": path.name, "rings": len(paving_rings), "confidence": 0.4}})
        else:
            review.append({"type": "block_paving", "reason": "未从 DXF 块内提取到命中铺装 token 的闭合环；块名/图层/闭合关系需人工复核", "evidence": {"file": path.name}})
    if with_refs and not block_refs:
        review.append({"type": "block_refs", "reason": "DXF 模型空间未读到顶层 INSERT；植物块坐标回退不可用", "evidence": {"file": path.name}})
    summary = {
        "drawing_types": 0, "systems": 0, "plant_legends": 0,
        "plant_block_legends": 0, "plant_block_fingerprints": 0,
        "plant_schedule_links": 0, "paving_closed_areas": 0,
        "green_area_candidates": 0, "pdf_geometry_candidates": 0,
        "hardscape": 0, "plant_name_noise_excluded": 0,
        "plant_note_noise_excluded": 0, "unclassified_legend_words": 0,
        "paving_rings": len(paving_rings), "block_refs": len(block_refs),
        "review_items": len(review),
    }
    return {
        "schema": SCHEMA, "source_file": path.name, "summary": summary,
        "drawing_types": [], "systems": [], "plant_legends": [],
        "plant_block_legends": [], "plant_block_fingerprints": [],
        "plant_schedule_links": [], "paving_closed_areas": [],
        "paving_rings": paving_rings, "block_refs": block_refs,
        "green_area_candidates": [], "pdf_geometry_candidates": [],
        "hardscape": [], "audit": {}, "units": units, "review": review,
        "boundary": "只输出园林识图候选与证据；块内铺装环为 P3 候选，面积仅以图纸单位平方记录，不冒充 m²、不计入主线；不输出苗木数量、铺装面积、土方量、材料量、造价或结算量。",
    }


def analyze_file(path, rules, drawing_unit=None):
    data = json.loads(path.read_text(encoding="utf-8"))
    records = read_records(data)
    views = drawing_type_candidates(records, rules)
    systems = system_candidates(records, rules)
    plant_stats: dict = {}
    plants = plant_legend_candidates(records, rules, plant_stats)
    plant_blocks = block_plant_candidates(data, rules, records)
    plant_fp = block_geom_fingerprint_candidates(data, rules, records)
    plant_blocks, block_links = link_plant_schedule(records, plant_blocks, rules)
    plant_fp, fp_links = link_plant_schedule(records, plant_fp, rules)
    plant_links = block_links + fp_links
    paving = paving_closed_candidates(data, rules)
    green = green_area_candidates(data, rules)
    pdf_geom = pdf_geometry_candidates(data, rules)
    hardscape = hardscape_candidates(records, rules)
    audit = plant_coverage_audit(records, rules)
    summary = {"drawing_types": len(views), "systems": len(systems), "plant_legends": len(plants), "plant_block_legends": len(plant_blocks), "plant_block_fingerprints": len(plant_fp), "plant_schedule_links": len(plant_links), "paving_closed_areas": len(paving), "green_area_candidates": len(green), "pdf_geometry_candidates": len(pdf_geom), "hardscape": len(hardscape), "plant_name_noise_excluded": int(plant_stats.get("name_noise_excluded") or 0),
                  "plant_note_noise_excluded": int(plant_stats.get("note_noise_excluded") or 0), "unclassified_legend_words": audit.get("unclassified_legend_words", 0)}
    units = {}
    if drawing_unit:
        mm_per_unit = {"mm": 1.0, "cm": 10.0, "m": 1000.0, "ft": 304.8}.get(str(drawing_unit).lower())
        if mm_per_unit is None:
            raise ValueError(f"不支持的 --drawing-unit：{drawing_unit}（可选 mm/cm/m/ft）")
        units = {"drawing_unit": str(drawing_unit).lower(), "drawing_mm_per_unit": mm_per_unit,
                 "source": "user-confirmed"}
    return {"schema": SCHEMA, "source_file": path.name, "summary": summary, "drawing_types": views, "systems": systems, "plant_legends": plants, "plant_block_legends": plant_blocks, "plant_block_fingerprints": plant_fp, "plant_schedule_links": plant_links, "paving_closed_areas": paving, "green_area_candidates": green, "pdf_geometry_candidates": pdf_geom, "hardscape": hardscape, "audit": audit, "units": units, "boundary": "只输出园林识图候选与证据；不输出苗木数量、铺装面积、土方量、材料量、造价或结算量。"}


def write_markdown(payload, path):
    s = payload["summary"]
    lines = ["# 园林/景观识图 / 中间数据复核", "", f"- 源文件：`{payload['source_file']}`", f"- 候选：图纸类型 {s['drawing_types']}，系统 {s['systems']}，苗木图例 {s['plant_legends']}，块/图例植物 {s.get('plant_block_legends',0)}，几何指纹 {s.get('plant_block_fingerprints',0)}，苗木表回溯 {s.get('plant_schedule_links',0)}，铺装闭合域 {s['paving_closed_areas']}，绿地闭合域 {s.get('green_area_candidates',0)}，PDF几何 {s.get('pdf_geometry_candidates',0)}，硬景构件 {s['hardscape']}", "", "## 苗木图例候选", ""]
    if payload["plant_legends"]:
        lines += ["| 植物 | 分类 | 规格 | 图层 | 坐标 |", "|---|---|---|---|---|"]
        for row in payload["plant_legends"][:120]:
            coord = "" if row.get("x") is None else f"{round(float(row['x']),3)},{round(float(row['y']),3)}"
            lines.append(f"| {row['plant']} | {row['category']} | {row.get('spec','')} | {row.get('layer','')} | {coord} |")
    else:
        lines.append("无")
    lines += ["", "## 词库覆盖审计（未分类候选词）", ""]
    audit = payload.get("audit") or {}
    if audit.get("top"):
        lines += ["| 词 | 出现 | 样例 |", "|---|---|---|"]
        for item in audit["top"][:40]:
            lines.append(f"| {item['word']} | {item['count']} | {item.get('sample','')} |")
        lines.append(f"- 未分类图例词 {audit.get('unclassified_legend_words',0)} 个，供补词库/按院校准。")
    else:
        lines.append("无")
    lines += ["", "## 块名植物图例候选", ""]
    if payload.get("plant_block_legends"):
        lines += ["| 块名 | 分类 | 图层 | 实例 | 关联植物 | 关联分类 | 状态 |", "|---|---|---|---|---|---|---|"]
        for row in payload["plant_block_legends"][:80]:
            linked = row.get("linked_plant", "")
            linked_cat = row.get("linked_plant_category", "")
            lines.append(f"| {row.get('name') or row.get('plant','')} | {row['category']} | {row.get('layer','')} | {row.get('instance_count','')} | {linked} | {linked_cat} | {row.get('link_status','')} |")
    else:
        lines.append("无")
    lines += ["", "## 几何指纹植物块候选", ""]
    if payload.get("plant_block_fingerprints"):
        lines += ["| 块名 | 分类 | 方法 | 置信度 | 支持/实例 |", "|---|---|---|---|---|"]
        for row in payload["plant_block_fingerprints"][:80]:
            lines.append(f"| {row.get('name','')} | {row['category']} | {row.get('method','')} | {row.get('confidence','')} | {row.get('support_count','')}/{row.get('instance_count','')} |")
    else:
        lines.append("无")
    lines += ["", "## 苗木表↔图例块交叉验证", ""]
    if payload.get("plant_schedule_links"):
        lines += ["| 块名 | 图例分类 | 关联植物 | 关联分类 | 状态 | 坐标 |", "|---|---|---|---|---|---|"]
        for row in payload["plant_schedule_links"][:80]:
            coord = "" if row.get("x") is None else f"{round(float(row['x']),3)},{round(float(row['y']),3)}"
            lines.append(f"| {row.get('block_name','')} | {row['category']} | {row['raw']} | {row.get('linked_plant_category','')} | {row.get('link_status','')} | {coord} |")
    else:
        lines.append("无")
    lines += ["", "## 铺装闭合域候选", ""]
    if payload["paving_closed_areas"]:
        lines += ["| 图层 | 段数 | 主环 | 过滤细环 | 区块数 |", "|---|---|---|---|---|"]
        for row in payload["paving_closed_areas"][:80]:
            lines.append(f"| {row['layer']} | {row['segment_count']} | {row['closed_ring_candidates']} | {row.get('filtered_ring_candidates',0)} | {len(row.get('region_candidates') or [])} |")
    else:
        lines.append("无")
    lines += ["", "## 绿地/地被闭合域候选", ""]
    if payload.get("green_area_candidates"):
        lines += ["| 图层 | 段数 | 主环 | 过滤细环 | 区块数 |", "|---|---|---|---|---|"]
        for row in payload["green_area_candidates"][:80]:
            lines.append(f"| {row['layer']} | {row['segment_count']} | {row['closed_ring_candidates']} | {row.get('filtered_ring_candidates',0)} | {len(row.get('region_candidates') or [])} |")
    else:
        lines.append("无")
    lines += ["", "## PDF 矢量几何 review 候选", ""]
    if payload.get("pdf_geometry_candidates"):
        lines += ["| 页 | 段数 | 包围盒 | 状态 |", "|---|---|---|---|"]
        for row in payload["pdf_geometry_candidates"][:120]:
            lines.append(f"| {row.get('page','')} | {row['segment_count']} | {row.get('bbox','')} | {row['status']} |")
    else:
        lines.append("无")
    lines += ["", "## 硬景构件候选", ""]
    if payload["hardscape"]:
        lines += ["| 构件 | 图层 |", "|---|---|"]
        for row in payload["hardscape"][:120]:
            lines.append(f"| {row['raw']} | {row.get('layer','')} |")
    else:
        lines.append("无")
    if payload.get("paving_rings") is not None:
        lines += ["", "## DXF 块内铺装环回退候选（P3，仅图纸单位平方）", ""]
        if payload.get("paving_rings"):
            lines += ["| 来源块 | 图层 | 点数 | 原始面积(drawing_unit^2) | 状态 |", "|---|---|---|---|---|"]
            for row in payload["paving_rings"][:120]:
                lines.append(f"| {row.get('source_block','')} | {row.get('layer','')} | {row.get('point_count','')} | {row.get('area_drawing_units2','')} | {row.get('status','')} |")
            lines.append("- 面积只写图纸单位平方，不是 m²；不进入主线工程量。")
        else:
            lines.append("无")
    if payload.get("block_refs") is not None:
        lines += ["", "## DXF 顶层块引用回退候选", ""]
        if payload.get("block_refs"):
            lines += ["| 块名 | 图层 | 坐标 | 状态 |", "|---|---|---|---|"]
            for row in payload["block_refs"][:120]:
                coord = f"{row.get('x','')},{row.get('y','')}"
                lines.append(f"| {row.get('block_name','')} | {row.get('layer','')} | {coord} | {row.get('status','')} |")
        else:
            lines.append("无")
    lines += ["", f"> {payload['boundary']}", ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_csv(payload, path):
    with path.open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.writer(fh)
        writer.writerow(["row_type", "category", "system", "name", "layer", "file", "sheet", "coordinate", "status", "evidence"])
        for row in payload["drawing_types"]:
            ev = (row.get("evidence") or [{}])[0]
            writer.writerow(["drawing_type", "", "", row["type"], ev.get("layer", ""), ev.get("file_name", ""), ev.get("sheet", ""), ev.get("coord", ""), row["status"], row["raw"]])
        for row in payload["systems"]:
            writer.writerow(["system", "", row["system"], row["raw"], row.get("layer", ""), row.get("file", ""), row.get("sheet", ""), "", row["status"], row.get("pattern", "")])
        for row in payload["plant_legends"]:
            coord = "" if row.get("x") is None else f"{row.get('x')},{row.get('y')}"
            writer.writerow(["plant_legend", row["category"], "planting", row["plant"], row.get("layer", ""), row.get("file", ""), row.get("sheet", ""), coord, row["status"], f"spec={row.get('spec','')}|legend={row.get('legend_raw','')}|{row.get('matched_token','')}"])
        for row in payload.get("plant_block_legends") or []:
            coord = "" if row.get("x") is None else f"{row.get('x')},{row.get('y')}"
            ev = ""
            if row.get("link_status"):
                ev = f"link={row.get('link_status','')}|{row.get('linked_plant_category','')}|{row.get('linked_plant','')}"
            writer.writerow(["plant_block_legend", row["category"], "planting", row.get("name") or row.get("plant", ""), row.get("layer", ""), row.get("file", ""), row.get("sheet", ""), coord, row["status"], f"instance_count={row.get('instance_count','')}|{ev}"])
        for row in payload.get("plant_block_fingerprints") or []:
            writer.writerow(["plant_block_fingerprint", row["category"], "planting", row.get("name", ""), row.get("layer", ""), row.get("file", ""), "", "", row["status"], f"support={row.get('support_count','')},evidence={row.get('matched_token','')}"])
        for row in payload.get("plant_schedule_links") or []:
            coord = "" if row.get("x") is None else f"{row.get('x')},{row.get('y')}"
            writer.writerow(["plant_schedule_link", row.get("category",""), "planting", row.get("block_name",""), row.get("layer",""), row.get("file",""), row.get("sheet",""), coord, row.get("status",""), f"{row.get('link_status','')}|{row.get('linked_plant_category','')}|{row.get('raw','')}"])
        for row in payload["paving_closed_areas"]:
            writer.writerow(["paving_closed_area", "paving", "paving", row["layer"], row["layer"], row.get("file", ""), "", str(row.get("bbox", "")), row["status"], f"main={row.get('closed_ring_candidates',0)},filtered={row.get('filtered_ring_candidates',0)},regions={len(row.get('region_candidates') or [])} | {row.get('review_reason','')}"])
        for row in payload.get("green_area_candidates") or []:
            writer.writerow(["green_area", "green_area", "planting", row["layer"], row["layer"], row.get("file", ""), "", str(row.get("bbox", "")), row["status"], f"main={row.get('closed_ring_candidates',0)},filtered={row.get('filtered_ring_candidates',0)},regions={len(row.get('region_candidates') or [])} | {row.get('review_reason','')}"])
        for row in payload.get("pdf_geometry_candidates") or []:
            writer.writerow(["pdf_geometry", "geometry", "pdf", row.get("page",""), row.get("layer",""), row.get("file",""), row.get("page",""), str(row.get("bbox","")), row["status"], row.get("review_reason","")])
        for row in payload["hardscape"]:
            coord = "" if row.get("x") is None else f"{row.get('x')},{row.get('y')}"
            writer.writerow(["hardscape", "hardscape", row.get("system", ""), row["raw"], row.get("layer", ""), row.get("file", ""), row.get("sheet", ""), coord, row["status"], row.get("matched_token", "")])
        for row in payload.get("paving_rings") or []:
            writer.writerow(["paving_ring", "paving", "paving", row.get("source_block", ""), row.get("layer", ""), payload.get("source_file", ""), "", str(row.get("bbox", "")), row.get("status", ""), f"points={row.get('point_count','')}|area_drawing_units2={row.get('area_drawing_units2','')}|{row.get('review_note','')}"])
        for row in payload.get("block_refs") or []:
            coord = f"{row.get('x','')},{row.get('y','')}"
            writer.writerow(["block_ref", "block_ref", "", row.get("block_name", ""), row.get("layer", ""), payload.get("source_file", ""), "", coord, row.get("status", ""), row.get("review_note", "")])


def main():
    import pyboot
    pyboot.ensure_utf8_io()
    parser = argparse.ArgumentParser(description="从 cad_scan 详情 JSON 提取园林/景观识图中间数据；可选 DXF 块内铺装/块引用回退。")
    parser.add_argument("inputs", nargs="*", help="cad_scan 详情 JSON（可空；仅用 DXF 回退参数时不必给）")
    parser.add_argument("--out-dir", default="园林识图")
    parser.add_argument("--rules", default=str(RULES_PATH))
    parser.add_argument("--institute", default=None, help="设计院图例覆盖名（packs/landscape-geometry/institutes/<名>.json）")
    parser.add_argument("--block-paving", type=Path, default=None, action="append", help="从 DXF 递归展开块内铺装闭合环（P3，仅图纸单位平方；可重复）")
    parser.add_argument("--block-refs", type=Path, default=None, action="append", help="读取 DXF 模型空间顶层 INSERT 块引用（P3；可重复）")
    parser.add_argument("--drawing-unit", choices=["mm", "cm", "m", "ft"], default=None,
                        help="DWG 未声明单位时显式确认模型空间绘图单位（写进契约，不猜）")
    args = parser.parse_args()
    if not args.inputs and not args.block_paving and not args.block_refs:
        parser.error("至少提供一个 cad_scan 详情 JSON，或 --block-paving/--block-refs")
    rules = load_rules(Path(args.rules))
    if getattr(args, "institute", None):
        rules = load_rules_with_institute(rules, args.institute)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    def write_outputs(payload, src):
        payload = contractize_payload(payload, source=src.name)
        jp, mp, cp = out_dir / f"{src.stem}.landscape.json", out_dir / f"{src.stem}.landscape.md", out_dir / f"{src.stem}.landscape.csv"
        jp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        write_markdown(payload, mp)
        write_csv(payload, cp)
        print(json.dumps({"source": src.name, "summary": payload["summary"], "outputs": [str(jp), str(mp), str(cp)]}, ensure_ascii=False))

    for value in args.inputs:
        src = Path(value)
        if not src.exists():
            raise FileNotFoundError(src)
        write_outputs(analyze_file(src, rules, args.drawing_unit), src)

    paving = {Path(v).resolve(): Path(v) for v in (args.block_paving or [])}
    refs = {Path(v).resolve(): Path(v) for v in (args.block_refs or [])}
    seen = set()
    for key in list(paving) + [k for k in refs if k not in paving]:
        if key in seen:
            continue
        seen.add(key)
        src = paving.get(key) or refs[key]
        if not src.exists():
            raise FileNotFoundError(src)
        payload = block_fallback_payload(src, rules, with_paving=key in paving, with_refs=key in refs)
        write_outputs(payload, src)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
