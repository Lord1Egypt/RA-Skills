#!/usr/bin/env python3
"""由扫描 JSON 生成安装物资计划：回路匹配分规格、损耗折算订货量。"""
from __future__ import annotations

try:
    import os as _boot_os, sys as _boot_sys
    _boot_sys.path.insert(0, _boot_os.path.dirname(_boot_os.path.abspath(__file__)))
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass


import argparse
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict

import i18n
from pathlib import Path

import contract_support as cs
import entry_gate as eg
from contract_guard import GuardError

# openpyxl 只在写 xlsx 时需要：延迟到出表函数内导入，避免"没装 openpyxl 连 --help 都跑不了"

CIRCUIT_LABEL = re.compile(r"(?::|^)\s*(W[A-Z]{1,3}\d*[A-Za-z]?)\s*$")
CIRCUIT_BARE = re.compile(r"^(W[A-Z]{1,3}\d*[A-Za-z]?)$")
CIRCUIT_SPEC = re.compile(
    r"\b(W[A-Z]{1,3}\d*[A-Za-z]?):(WD[A-Z]*-?[A-Z]+-([0-9xX×.+]+))[-–]?([A-Z0-9/]+)?"
)
BOX_CIRCUIT = re.compile(
    r"(?::|^)\s*([A-Za-z0-9_\-]+)[:：]\s*(W[A-Z]{1,3}\d*[A-Za-z]?)\s*$"
)
BOX_CODE = re.compile(
    r"(?i)(?<![A-Z0-9])([A-Z0-9]{1,4}[-]?[A-Z0-9]{0,5}?"
    r"(?:AL|AP|AW|AE|ATG|APGY|ZAPGY|APPW|FJAP|ATSDT|ALE)[A-Z0-9\-]*\d)(?![A-Z0-9])"
)
CIRCUIT_TOKEN = re.compile(r"^W[A-Z]{1,3}\d*[A-Za-z]?\s*[:：]?$")
DN_LABEL = re.compile(r"\b(DN|dn|De|de)\s*-?\s*(\d{2,3})\b")
RISER_ID = re.compile(
    r"(?<![A-Za-z0-9])(HYL|SPL|JL|PL|TL|FL|WL|YL|HL|RL)-"
    r"[A-Za-z0-9]+['′]?(?![A-Za-z0-9])",
    re.I,
)
RISER_SYSTEMS = {
    "HYL": "虹吸雨水", "SPL": "水炮", "JL": "给水", "PL": "排水",
    "TL": "通气", "FL": "废水", "WL": "污水", "YL": "雨水",
    "HL": "中水", "RL": "热水",
}
TRUNK_CABLE = re.compile(
    r"\b(WD[A-Z]{0,4}[-–][A-Z]{2,4}[-–][0-9xX×.+]+(?:\+[0-9xX×.+]+)*(?:[-–][A-Z0-9/.]+)*)"
)
CONDUIT_RE = re.compile(r"\b(PVC|PC|SC|MT|KBG|JDG|TC|CPVC)[- ]?(\d{2,3})\b", re.I)
# 电线规格的数x芯写法：`3*10` `3x10` `3×10` `2*2.5+1*2.5` 都出现过，
# 早期只认 x/×，实测样例这批图一律写 `*`（`WDZ-BYJ-3*10`），整个规格解析不下来。
SIZE_TAIL_RE = re.compile(r"([0-9xX×*.+]+)$")
SIZE_SPLIT_RE = re.compile(r"[xX×*]")
# 芯数×截面：`3*10` `3x10` `3×2.5` `4*25+1*16`（取第一组，多芯组合另算）
SIZE_CORE_RE = re.compile(r"(\d{1,2})\s*[xX×*]\s*(\d+(?:\.\d+)?)")
# 规格家族开头：有这些才算「电线/电缆规格串」，避免把尺寸标注当成规格
SPEC_FAMILY_RE = re.compile(
    r"^(?:WDZ[A-Z]*|WDZA|WDZB|WDZC|ZR|NH|BTLY|NG-A|BV|BVR|BYJ|RVV|RVVP|YJV|YJY|KVV|BLV)",
    re.I)
DOOR_CODE = re.compile(r"^[MXZ]?C?\d{4}$")
TAG_CODE = re.compile(r"^[A-Z]{1,2}[-]?\d+$")
TABLE_TAGS = {"WHAT", "SN", "SNN", "SPEC", "UNIT", "UN", "数量", "TYPE"}
UNICODE_ESCAPE_RE = re.compile(r"(?:\\U\+|U\+)([0-9A-Fa-f]{4})")
ELECTRIC_ROUTE_RE = re.compile(r"(WIRE|LGT|BUSB|强电|弱电|电缆|照明线路|景观照明|路灯|SITE[_-]?(?:WIRE|LIGHT)|DIM-动力|管线-动照|管线-供电)", re.I)
PIPE_ROUTE_RE = re.compile(r"(PIPE|管网|综合管网|室外管网|雨水|污水|废水|给水|中水|消防|喷淋|燃气|热力|暖通|采暖|供热|SITE[_-]?PIPE|DIM_|EQUIP_|管线-|HEATER|HEATING)", re.I)
TRAY_ROUTE_RE = re.compile(r"(CABLETRAY|电缆沟|电缆排管|强电排管|弱电排管|SITE[_-]?TRAY)", re.I)
# 「不是管线」的图层：标注、图框、墙体、轴网、文字、楼梯。
# 实测样例 J-5 电气图 `DIM-照明` 11329.9m、`DIM_SYMB` 1638.3m 全落在标注图层上，
# 而 PIPE_ROUTE_RE 里的 `DIM_` / `ELEV` 又让 `DIM_SYMB`、`DIM-消防` 命中「水专业」，
# 于是 1.6km 尺寸线被算成水管道。判据必须排在路由判据之前。
NON_ROUTE_RE = re.compile(
    r"^(?:DIM|DIMENSION)|标注|尺寸|图框|标题|会签|PUB[_-]?TITLE|^WALL$|墙体|^STAIR|楼梯"
    r"|^AXIS|轴网|^DOTE$|^TEXT|文字|^HATCH|填充|图例|^EQUIP[_-]|设备图",
    re.I)


def is_non_route_layer(layer: str) -> bool:
    """标注/图框/设备符号/建筑底图类图层，任何路由判据都不该命中它们。

    `EQUIP-*` 是设备符号层：里面是块参照炸开的符号线，按线长算管道会把
    一个消防栓算成几米管（实测 J-5 电气图 `EQUIP-消防` 602.5m 全被当成水管）。
    设备量走 ATTRIB 计数，不走线长。
    """
    return bool(NON_ROUTE_RE.search(layer or ""))


def is_electric_route_layer(layer: str) -> bool:
    return not is_non_route_layer(layer) and bool(ELECTRIC_ROUTE_RE.search(layer))


def is_pipe_route_layer(layer: str) -> bool:
    # 电气优先：`WIRE-消防` 是消防联动/报警线路，不是消防水管。
    # 早期两条判据互不排斥，同一批 841.7m 既进「电线电缆」又进「水专业」，
    # 全楼管线量凭空多出一份。
    if is_non_route_layer(layer) or is_electric_route_layer(layer):
        return False
    return bool(PIPE_ROUTE_RE.search(layer))


def is_tray_route_layer(layer: str) -> bool:
    return not is_non_route_layer(layer) and bool(TRAY_ROUTE_RE.search(layer))


def layer_role(layer: str) -> tuple[str, str]:
    """图层 -> (归属, 说明)。用于「图层分档」与「总量守恒」两张表对齐口径。"""
    if is_non_route_layer(layer):
        return "非管线路由", "标注/图框/设备符号类，不计入任何量"
    if is_tray_route_layer(layer):
        return "桥架", "按图层出量，不走回路规格匹配"
    if is_electric_route_layer(layer):
        return "电气回路", "按就近回路/规格标注匹配"
    if is_pipe_route_layer(layer):
        return "水专业", "按就近 DN 标注匹配"
    return "未归类", "图层名无路由关键字，未计入任何量"


def load(path: str) -> dict:
    return json.load(open(path, encoding="utf-8"))


def decode_cad_text(text: str) -> str:
    """解码 CAD 文本中残留的 \\U+ 转义，避免核对清单二次出现转义噪声。"""
    return UNICODE_ESCAPE_RE.sub(lambda m: chr(int(m.group(1), 16)), text)


def spec_tables(sys_scans: list[dict]) -> tuple[dict[str, Counter], dict[str, str]]:
    """回路编号 -> {规格: n}，回路编号 -> 类型(照明/插座/...)。"""
    specs: dict[str, Counter] = defaultdict(Counter)
    kind = {"L": "照明", "X": "插座", "P": "动力", "E": "应急照明", "K": "控制"}
    ctype = {}
    for sys_scan in sys_scans:
        for t in sys_scan.get("texts", []):
            for m in CIRCUIT_SPEC.finditer(t["text"]):
                token, cable, _size, conduit = m.groups()
                specs[token][cable + ("-" + conduit if conduit else "")] += 1
                ctype[token[1]] = kind.get(token[1], token[1])
    return specs, ctype


def boxed_system_specs(sys_scans: list[dict], radius_mm: float = 250_000) -> dict[tuple[str, str], Counter]:
    """系统图中同号回路按就近配电箱编号分箱，避免跨箱规格互相污染。"""
    boxed: dict[tuple[str, str], Counter] = defaultdict(Counter)
    for sys_scan in sys_scans:
        boxes = []
        for t in sys_scan.get("texts", []):
            text = decode_cad_text(t["text"])
            if len(text) <= 60:
                for m in BOX_CODE.finditer(text):
                    boxes.append((m.group(1).upper(), t["x"], t["y"]))
        cable_texts = []
        for t in sys_scan.get("texts", []):
            if CIRCUIT_TOKEN.fullmatch(decode_cad_text(t["text"]).strip()):
                continue
            m = TRUNK_CABLE.search(decode_cad_text(t["text"]))
            if m:
                cable_texts.append((m.group(0), t["x"], t["y"]))
        for t in sys_scan.get("texts", []):
            text = decode_cad_text(t["text"])
            hits = []
            for m in CIRCUIT_SPEC.finditer(text):
                token, cable, _size, conduit = m.groups()
                spec = cable + ("-" + conduit if conduit else "")
                token = token.upper()
                hits.append((token, spec, t["x"], t["y"]))
            if not hits:
                token_m = CIRCUIT_TOKEN.fullmatch(text.strip())
                if not token_m:
                    continue
                token = token_m.group(0).rstrip(":： ").upper()
                best_spec, spec_d = None, None
                for spec, cx, cy in cable_texts:
                    d = math.hypot(t["x"] - cx, t["y"] - cy)
                    if spec_d is None or d < spec_d:
                        best_spec, spec_d = spec, d
                if not best_spec or spec_d > 10_000:
                    continue
                hits.append((token, best_spec, t["x"], t["y"]))
            for token, spec, x, y in hits:
                best, best_d = None, None
                for box, bx, by in boxes:
                    d = math.hypot(x - bx, y - by)
                    if best_d is None or d < best_d:
                        best, best_d = box, d
                if best and best_d <= radius_mm:
                    boxed[(best, token)][spec] += 1
    return boxed


def plan_labels(scan: dict) -> list[tuple[str, float, float]]:
    out = []
    for t in scan.get("texts", []):
        m = CIRCUIT_LABEL.search(t["text"]) or CIRCUIT_BARE.match(t["text"])
        if m:
            out.append((m.group(1), t["x"], t["y"]))
    return out


def box_circuits(scans: list[dict], specs: dict[str, Counter], radius_mm: float,
                 boxed_specs: dict[tuple[str, str], Counter] | None = None) -> list[dict]:
    """按“配电箱:回路”标注出回路规格表；裸回路不硬归属配电箱。"""
    rows: dict[tuple[str, str, str], dict] = defaultdict(
        lambda: {"length_mm": 0.0, "objects": 0, "sources": Counter(), "samples": []}
    )
    for scan in scans:
        labels = []
        for t in scan.get("texts", []):
            m = BOX_CIRCUIT.search(decode_cad_text(t["text"]))
            if m:
                labels.append((m.group(1), m.group(2), t["x"], t["y"]))
        for seg in scan.get("segments", []):
            layer, length, x, y = seg[0], seg[1], seg[2], seg[3]
            if not is_electric_route_layer(layer):
                continue
            best, best_d = None, None
            for box, token, lx, ly in labels:
                d = seg_distance(seg, lx, ly)
                if best_d is None or d < best_d:
                    best, best_d = (box, token), d
            if not best or best[1] not in specs or best_d > radius_mm:
                continue
            box, token = best
            counter = (boxed_specs or {}).get((box, token)) or specs[token]
            spec = counter.most_common(1)[0][0]
            rec = rows[(box, token, spec)]
            rec["length_mm"] += length
            rec["objects"] += 1
            rec["sources"][scan.get("file", "")] += length
            if len(rec["samples"]) < 3:
                rec["samples"].append(f"({x:,.0f},{y:,.0f})")
    return [
        {"box": box, "circuit": token, "spec": spec,
         "ambiguous": len((boxed_specs or {}).get((box, token)) or specs[token]) > 1, **rec}
        for (box, token, spec), rec in sorted(rows.items())
    ]


def cluster_unmatched(rows: list[dict], grid_mm: float = 50_000,
                      max_rows: int = 50) -> list[dict]:
    """未匹配管段按 50m 网格汇总，便于按坐标回图核对。

    入参是匹配函数**实际没定下规格**的线段，不再在这里重算一遍——
    重算会和传播/端点距离口径不一致，出现「表里说未匹配、坐标簇里没有」。
    """
    clusters: dict[tuple[str, int, int], dict] = defaultdict(
        lambda: {"length_mm": 0.0, "objects": 0, "layers": Counter(), "samples": []}
    )
    for row in rows:
        x, y = row["x"], row["y"]
        gx, gy = math.floor(x / grid_mm), math.floor(y / grid_mm)
        rec = clusters[(row["file"], gx, gy)]
        rec["length_mm"] += row["length_mm"]
        rec["objects"] += 1
        rec["layers"][row["layer"]] += row["length_mm"]
        if len(rec["samples"]) < 1:
            rec["samples"].append(f"({x:,.0f},{y:,.0f})")
    ordered = sorted(clusters.items(), key=lambda item: -item[1]["length_mm"])[:max_rows]
    return [{"file": file, "gx": gx, "gy": gy, **rec}
            for (file, gx, gy), rec in ordered]


def dn_labels(scan: dict) -> list[tuple[str, float, float]]:
    out = []
    for t in scan.get("texts", []):
        for m in DN_LABEL.finditer(t["text"]):
            out.append((m.group(1).upper() + m.group(2), t["x"], t["y"],
                        water_label_system(t.get("layer", ""), t.get("text", ""))))
    return out


def water_system(layer: str) -> str:
    """按图层归并水系统，避免跨系统 DN 标注互相污染。"""
    for key, system in (
        ("虹吸雨水", "虹吸雨水"), ("压力废", "压力废水"), ("压力污", "压力污水"),
        ("喷淋", "喷淋"), ("消防", "消防"), ("水炮", "水炮"), ("给水", "给水"),
        ("中水", "中水"), ("市政给", "给水"), ("凝结", "凝结水"),
        ("HEATER", "暖通"), ("HEATING", "暖通"), ("暖通", "暖通"), ("暖供", "暖通"), ("暖回", "暖通"),
        ("自动喷淋", "喷淋"), ("动照", "电力"), ("供电", "电力"),
        ("雨水", "雨水"), ("废水", "废水"), ("污水", "污水"), ("通气", "通气"),
    ):
        if key in layer:
            return system
    return "其他水" if is_pipe_route_layer(layer) else ""


def water_label_system(layer: str, text: str = "") -> str | None:
    """DN 标注所属水系统；None 表示通用标注，可匹配任何水系统。"""
    system = water_system(layer)
    if system and system != "其他水":
        return system
    if any(k in layer for k in ("图框", "图例", "说明")):
        return None
    m = RISER_ID.match(decode_cad_text(text).strip())
    if m:
        return RISER_SYSTEMS.get(m.group(1).upper())
    return None


def water_zone(layer: str, system: str) -> str:
    """从图层尾缀识别高/中/低区；过滤常见室外管综图层前缀。"""
    tail = layer
    for prefix in ("PIPE-", "管线-", "DIM_", "TEXT_", "EQUIP_", "WIRE-", "DIM-"):
        if tail.upper().startswith(prefix.upper()):
            tail = tail[len(prefix):]
            break
    for token in (system, "给水", "中水", "雨水", "污水", "废水", "消防", "喷淋", "暖通", "采暖", "供热", "动照", "供电", "电力"):
        if token and tail.startswith(token):
            tail = tail[len(token):]
            break
    if system == "给水" and tail.startswith("市政给"):
        tail = "市政"
    tail = tail.strip("-_ ")
    if "高" in tail:
        return "高区"
    if "中" in tail and "中水" not in layer:
        return "中区"
    if "低" in tail:
        return "低区"
    return tail or "全图"


def water_segment_specs(scans: list[dict], radius_mm: float,
                        fallback_radius_mm: float = 0.0) -> list[dict]:
    """PIPE-* 管段的系统/分区/管径记录，保留端点供局部连通校核。"""
    records: list[dict] = []
    for scan in scans:
        labels = dn_labels(scan)
        for seg in scan.get("pipe_segments") or scan.get("segments", []):
            layer, length = seg[0], seg[1]
            if len(seg) >= 8:
                x1, y1, z1, x2, y2, z2 = seg[2:8]
                x, y = (x1 + x2) / 2, (y1 + y2) / 2
            else:
                x1 = y1 = z1 = x2 = y2 = z2 = None
                x, y = seg[2], seg[3]
            if not is_pipe_route_layer(layer):
                continue
            pipe_system = water_system(layer)
            best, best_d = None, None
            for dn, lx, ly, label_system in labels:
                if label_system and pipe_system != "其他水" and label_system != pipe_system:
                    continue
                d = math.hypot(x - lx, y - ly)
                if best_d is None or d < best_d:
                    best, best_d = dn, d
            if best is None or best_d > radius_mm:
                records.append({
                    "file": scan.get("file", ""), "layer": layer,
                    "length_mm": length, "system": pipe_system,
                    "zone": water_zone(layer, pipe_system), "dn": None,
                    "direct": False, "inferred": False,
                    "x": x, "y": y, "x1": x1, "y1": y1, "z1": z1,
                    "x2": x2, "y2": y2, "z2": z2,
                })
            else:
                records.append({
                    "file": scan.get("file", ""), "layer": layer,
                    "length_mm": length, "system": pipe_system,
                    "zone": water_zone(layer, pipe_system), "dn": best,
                    "direct": True, "inferred": False,
                    "x": x, "y": y, "x1": x1, "y1": y1, "z1": z1,
                    "x2": x2, "y2": y2, "z2": z2,
                })

        if fallback_radius_mm > 0:
            labeled = defaultdict(list)
            for rec in records:
                if rec["direct"]:
                    labeled[rec["layer"]].append((rec["x"], rec["y"], rec["dn"]))
            for rec in records:
                if rec["dn"] or not labeled[rec["layer"]]:
                    continue
                lx, ly, nearest = min(
                    labeled[rec["layer"]],
                    key=lambda item: math.hypot(rec["x"] - item[0], rec["y"] - item[1])
                )
                if math.hypot(rec["x"] - lx, rec["y"] - ly) <= fallback_radius_mm:
                    rec["dn"] = nearest
                    rec["inferred"] = True
    return records


def water_diameter_from_records(records: list[dict]):
    """按管段记录汇总 DN；保持原有总量口径。"""
    by = defaultdict(float)
    inferred = defaultdict(float)
    unmatched = defaultdict(float)
    for rec in records:
        if rec["dn"]:
            if rec["inferred"]:
                inferred[(rec["layer"], rec["dn"])] += rec["length_mm"]
            else:
                by[(rec["layer"], rec["dn"])] += rec["length_mm"]
        else:
            unmatched[rec["layer"]] += rec["length_mm"]
    return by, inferred, unmatched


def water_diameter(scans: list[dict], radius_mm: float, fallback_radius_mm: float = 0.0):
    """PIPE-* 管段就近 DN 标注；同图内无标注管段按邻近已标注管段兜底。"""
    return water_diameter_from_records(
        water_segment_specs(scans, radius_mm, fallback_radius_mm)
    )


def connectivity_check(records: list[dict], cfg: dict, max_rows: int = 50):
    """同系统/管径端点吸附，输出断点坐标簇；不改总长。"""
    tolerance = max(float(cfg.get("water_connect_radius_mm", 500)), 1.0)
    grid = max(float(cfg.get("connectivity_grid_mm", 50_000)), 1.0)
    cross_z = max(float(cfg.get("cross_layer_z_mm", 3_000)), 1.0)
    groups: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    missing = sum(1 for r in records if r.get("x1") is None)
    total_open = total_isolated = total_cross = 0
    clusters: dict[tuple[str, str, str, str, int, int], dict] = defaultdict(
        lambda: {"breaks": 0, "length_mm": 0.0, "components": 0,
                 "isolated": 0, "cross": 0, "layers": Counter(), "samples": [],
                 "_roots": set(), "_isolated": 0}
    )

    for rec in records:
        if rec.get("x1") is None:
            continue
        groups[(rec["file"], rec["system"], rec.get("dn") or "未标注")].append(rec)

    for (file, system, dn), recs in sorted(groups.items()):
        buckets: dict[tuple[int, int], list[int]] = {}
        coords: dict[int, tuple[float, float, float]] = {}
        parent: dict[int, int] = {}
        degree: dict[int, int] = defaultdict(int)
        seg_roots: list[int] = []

        def find(node: int) -> int:
            while parent[node] != node:
                parent[node] = parent[parent[node]]
                node = parent[node]
            return node

        def node_id(x: float, y: float, _z: float) -> int:
            kx, ky = int(math.floor(x / tolerance)), int(math.floor(y / tolerance))
            candidates = []
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    key = (kx + dx, ky + dy)
                    for node in buckets.get(key, []):
                        nx, ny, _nz = coords[node]
                        candidates.append((math.hypot(x - nx, y - ny), node))
            if candidates:
                dist, node = min(candidates)
                if dist <= tolerance:
                    return node
            node = len(coords)
            buckets.setdefault((kx, ky), []).append(node)
            coords[node] = (x, y, _z)
            parent[node] = node
            return node

        def union(a: int, b: int) -> None:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[rb] = ra

        for rec in recs:
            a = node_id(rec["x1"], rec["y1"], rec["z1"] or 0)
            b = node_id(rec["x2"], rec["y2"], rec["z2"] or 0)
            union(a, b)
            seg_roots.append(find(a))
            degree[a] += 1
            degree[b] += 1

        comps: dict[int, dict] = defaultdict(
            lambda: {"length_mm": 0.0, "objects": 0, "layers": Counter(),
                     "zones": Counter(), "open": [], "cross": 0}
        )
        for rec, root in zip(recs, seg_roots):
            comp = comps[find(root)]
            comp["length_mm"] += rec["length_mm"]
            comp["objects"] += 1
            comp["layers"][rec["layer"]] += rec["length_mm"]
            comp["zones"][rec["zone"]] += rec["length_mm"]
            if abs((rec.get("z2") or 0) - (rec.get("z1") or 0)) > cross_z:
                comp["cross"] += 1
        for node, count in degree.items():
            if count == 1:
                root = find(node)
                comps[root]["open"].append(coords[node])
        for root, comp in comps.items():
            comp["isolated"] = 1 if comp["objects"] == 1 else 0
            comp["cross_zone"] = 1 if len(comp["zones"]) > 1 else 0
            total_open += len(comp["open"])
            total_isolated += comp["isolated"]
            total_cross += comp["cross"] + comp["cross_zone"]
            for x, y, _z in comp["open"]:
                gx, gy = math.floor(x / grid), math.floor(y / grid)
                key = (file, system, dn, f"{gx},{gy}", gx, gy)
                cluster = clusters[key]
                cluster["_roots"].add(root)
                cluster["_isolated"] += comp["isolated"]
                cluster["breaks"] += 1
                cluster["length_mm"] += comp["length_mm"] / max(len(comp["open"]), 1)
                cluster["cross"] += comp["cross"] + comp["cross_zone"]
                for layer, mm in comp["layers"].items():
                    cluster["layers"][layer] += mm / max(len(comp["open"]), 1)
                if len(cluster["samples"]) < 2:
                    cluster["samples"].append(f"({x:,.0f},{y:,.0f})")

    priority = ("给水", "喷淋", "消防", "虹吸雨水")
    ordered = sorted(
        clusters.items(),
        key=lambda kv: (kv[0][1] not in priority, -kv[1]["breaks"],
                        -kv[1]["length_mm"], kv[0])
    )
    rows = []
    for rec in clusters.values():
        rec["components"] = len(rec.pop("_roots"))
        rec["isolated"] = rec.pop("_isolated")
    for (file, system, dn, _grid_key, gx, gy), rec in ordered[:max_rows]:
        x0, x1 = gx * grid / 1000, (gx + 1) * grid / 1000
        y0, y1 = gy * grid / 1000, (gy + 1) * grid / 1000
        layers = "；".join(f"{layer} {mm / 1000:.1f}m"
                           for layer, mm in rec["layers"].most_common(3))
        rows.append(["断点坐标簇", system, dn, layers, file,
                     f"{x0:,.0f}-{x1:,.0f},{y0:,.0f}-{y1:,.0f}",
                     rec["breaks"], round(rec["length_mm"] / 1000, 1),
                     rec["isolated"], rec["cross"], " ".join(rec["samples"]),
                     "需回图确认"])
    summary = [
        ["端点吸附管段", len(records) - missing, "PIPE 图层且扫描保留端点"],
        ["缺端点管段", missing, "旧扫描无 pipe_segments，需重扫"],
        ["开路端点", total_open, "同系统/同管径端点吸附后仍单侧悬空"],
        ["孤立段对象", total_isolated, "1 个对象自成连通块"],
        ["疑似跨层/跨分区", total_cross, "按 z 高差或图层分区差异提示"],
    ]
    return summary, rows


def water_zone_riser_rows(zone_groups: dict, riser_rows: list[dict]) -> list[list]:
    """只输出分区/立管的明显重复或漏识别提示。"""
    rows: list[list] = []
    zones_by_system = defaultdict(set)
    for (system, zone), rec in zone_groups.items():
        zones_by_system[system].add(zone)
        if len(rec["layers"]) > 1:
            rows.append(["分区核对", system, f"{zone} 多图层", rec["objects"],
                         source_text(rec["sources"]), "；".join(rec["layers"]),
                         "", "需核对是否同一分区"])
    for system, zones in sorted(zones_by_system.items()):
        if len(zones) > 1 and "全图" in zones:
            rows.append(["分区核对", system, "全图+分区混用", len(zones), "", "", "",
                         "需核对分区图层命名"])

    riser_by_id = defaultdict(set)
    for rec in riser_rows:
        riser_by_id[rec["id"].upper()].add(rec["system"])
    for rec in riser_rows:
        if len(rec["sources"]) > 1:
            rows.append(["立管核对", rec["system"], rec["id"], rec["count"],
                         source_text(rec["sources"]), rec["sample"],
                         "", "跨图重复标注，需核对"])
        if len(riser_by_id[rec["id"].upper()]) > 1:
            rows.append(["立管核对", rec["system"], rec["id"], rec["count"],
                         source_text(rec["sources"]), rec["sample"], "", "同号跨系统，需核对"])
    pipe_systems = set(zones_by_system)
    riser_systems = {rec["system"] for rec in riser_rows}
    for system in sorted(pipe_systems - riser_systems):
        rows.append(["立管核对", system, "无立管编号", "", "", "", "", "疑似漏识别"])
    for system in sorted(riser_systems - pipe_systems):
        rows.append(["立管核对", system, "无平面管线", "", "", "", "", "需核对系统归属"])
    return rows
    return by, inferred, unmatched


def riser_identification(scans: list[dict]) -> list[dict]:
    """从水专业标注层识别立管编号；同一编号跨图只计一根。"""
    rows: dict[tuple[str, str], dict] = {}
    for scan in scans:
        for t in scan.get("texts", []):
            text = decode_cad_text(t.get("text", "")).strip()
            if any(k in text for k in ("管道类别", "立管编号", "图例")):
                continue
            system = water_system(t.get("layer", ""))
            if not system or system == "其他水":
                continue
            head = RISER_ID.match(text)
            if not head:
                continue
            tail = text[head.end():]
            ids = [head.group(0)]
            if tail and re.fullmatch(r"(?:/[A-Za-z0-9]+['′]?)+", tail):
                ids.extend(f"{head.group(1)}-{part}"
                           for part in tail.split("/") if part)
            for rid in ids:
                key = (system, rid.upper())
                rec = rows.setdefault(key, {"system": system, "id": rid,
                                            "count": 0, "sources": Counter(),
                                            "sample": ""})
                rec["count"] += 1
                rec["sources"][scan.get("file", "")] += 1
                if not rec["sample"]:
                    rec["sample"] = f'{t.get("layer", "")} ({t.get("x", 0):,.0f},{t.get("y", 0):,.0f})'
    return sorted(rows.values(), key=lambda r: (r["system"], r["id"]))


def trunk_cables(system_scans: list[dict]) -> Counter:
    hits: Counter = Counter()
    for scan in system_scans:
        for t in scan.get("texts", []):
            if re.search(r"\bW[A-Z]{1,3}\d*[A-Za-z]?:", t["text"]):
                continue
            for m in TRUNK_CABLE.finditer(t["text"]):
                hits[m.group(1)] += 1
    return hits


def trunk_labels(scan: dict) -> list[tuple[str, float, float]]:
    labels = []
    for t in scan.get("texts", []):
        if re.search(r"\bW[A-Z]{1,3}\d*[A-Za-z]?:", t["text"]):
            continue
        for m in TRUNK_CABLE.finditer(t["text"]):
            labels.append((m.group(1), t["x"], t["y"]))
    return labels


def is_trunk_route_layer(layer: str) -> bool:
    up = layer.upper()
    if any(k in up for k in ("TEL", "WEAK", "RADIO", "SECU", "通讯")):
        return False
    return "BUSB" in up or "母线" in layer or "CABLETRAY" in up


def trunk_routes(trunk_scans: list[dict], radius_mm: float = 30000):
    """干线平面/母线层路由估算；无规格标注时按图层出未分配量。"""
    matched: Counter = Counter()
    unmatched: dict[str, float] = defaultdict(float)
    routes: dict[str, list[float]] = defaultdict(lambda: [0.0, 0])
    confidence: dict[str, defaultdict] = defaultdict(lambda: defaultdict(float))
    for scan in trunk_scans:
        labels = trunk_labels(scan)
        for seg in scan.get("segments", []):
            layer, length, x, y = seg[0], seg[1], seg[2], seg[3]
            if not is_trunk_route_layer(layer):
                continue
            routes[layer][0] += length
            routes[layer][1] += 1
            best, best_d = None, None
            for spec, lx, ly in labels:
                d = seg_distance(seg, lx, ly)
                if best_d is None or d < best_d:
                    best, best_d = spec, d
            if best and best_d <= radius_mm:
                matched[best] += length
                confidence[layer]["高" if best_d <= radius_mm / 3 else "中"] += length
            else:
                unmatched[layer] += length
                confidence[layer]["低"] += length
    return matched, unmatched, routes, confidence


def parse_spec(spec: str) -> dict:
    """规格串 -> {conduit, tray, cores, core_size, is_cable, family}。

    芯数×截面必须**在整串里找**，不能取 `split("-")[2]`：
    `BV-2*2.5-SC15` 的第三段是 `SC15`，照旧写法定会解析成「15 芯」。
    """
    conduit_m = CONDUIT_RE.search(spec)
    conduit = f"{conduit_m.group(1).upper()}{conduit_m.group(2)}" if conduit_m else ""
    tray = not conduit and "MR" in spec.upper()
    cores, core_size = 1, ""
    size_m = SIZE_CORE_RE.search(spec)
    if size_m:
        cores = int(size_m.group(1))
        core_size = size_m.group(2)
    else:
        # 单芯写法：BV-2.5 / BV-2.5-SC15，取第一个独立的数值段
        single = re.search(r"[-–](\d+(?:\.\d+)?)(?=[-–]|$)", spec)
        if single:
            core_size = single.group(1)
    is_cable = bool(re.search(r"YJV|YJY", spec, re.I))
    head = re.split(r"[-–]", spec)
    # 型号家族取「首段-次段」且次段是纯字母时才算（WDZ-BYJ / WDZ-YJV），
    # 否则只取首段（BV / RVV）——否则会把 `2*2.5` 当成家族名
    family = (f"{head[0]}-{head[1]}" if len(head) > 1 and head[1].isalpha() else head[0]).upper()
    return {"spec": spec, "conduit": conduit, "tray": tray, "cores": cores,
            "core_size": core_size, "is_cable": is_cable, "family": family}


def match_circuits(scans: list[dict], specs: dict[str, Counter], radius_mm: float,
                   high_radius_mm: float | None = None):
    """段 -> 最近回路标注。返回 (按规格合计, 按图层匹配/未匹配, 歧义回路, 未定规格线段)。"""
    high_radius = radius_mm / 3 if high_radius_mm is None else high_radius_mm
    by_spec = defaultdict(lambda: {"length_mm": 0.0, "circuits": set(),
                                   "sources": Counter(), "samples": [],
                                   "confidence": defaultdict(float)})
    by_layer = defaultdict(lambda: {"total": 0.0, "matched": 0.0})
    ambiguous = Counter()
    unmatched: list[dict] = []
    for scan in scans:
        labels = plan_labels(scan)
        for seg in scan.get("segments", []):
            layer, length, x, y = seg[0], seg[1], seg[2], seg[3]
            by_layer[layer]["total"] += length
            up = layer.upper()
            if not is_electric_route_layer(layer):
                continue  # 桥架/PIPE 等不走回路规格，按图层单独出量
            best, best_d = None, None
            for token, lx, ly in labels:
                d = seg_distance(seg, lx, ly)
                if best_d is None or d < best_d:
                    best, best_d = token, d
            if best is None or best_d > radius_mm or best not in specs:
                unmatched.append({"file": scan.get("file", ""), "layer": layer,
                                  "length_mm": length, "x": x, "y": y})
                continue
            counter = specs[best]
            if len(counter) > 1:
                ambiguous[best] += 1
            spec, _n = counter.most_common(1)[0]
            by_spec[spec]["length_mm"] += length
            by_spec[spec]["confidence"]["中" if len(counter) > 1 else
                                       ("高" if best_d <= high_radius else "中")] += length
            by_spec[spec]["circuits"].add(best)
            by_spec[spec]["sources"][scan.get("file", "")] += length
            if len(by_spec[spec]["samples"]) < 3:
                by_spec[spec]["samples"].append(f"({x:,.0f},{y:,.0f})")
            by_layer[layer]["matched"] += length
            by_layer[layer].setdefault("specs", Counter())[spec] += length
    return by_spec, by_layer, ambiguous, unmatched


def clean_spec(text: str) -> str:
    """规格串规范化：去空格、全角括号转半角、× 统一成 *。"""
    s = re.sub(r"\s+", "", decode_cad_text(text))
    s = s.replace("（", "(").replace("）", ")").replace("×", "*").replace("–", "-")
    return s.strip(":：,，。;；").upper()


def looks_like_spec(s: str) -> bool:
    """判断一段文字是不是「只有规格、没有回路号」的回路标注。

    实测样例这批电气图平面上一律写 `WDZ-BYJ-3*10-(CT)PVC32-FWC`，
    回路号（W1/WL2…）只出现在配电系统图上。早期实现要求「回路号:规格」，
    于是一整栋楼的电气管线全部匹配失败、电线电缆表 0 行。
    """
    if not (6 <= len(s) <= 60):
        return False
    if not SPEC_FAMILY_RE.match(s):
        return False
    if s.count("-") < 2:
        return False
    return bool(SIZE_CORE_RE.search(s))


def plan_spec_labels(scan: dict) -> list[tuple[str, float, float]]:
    """平面图上的「裸规格」标注点。"""
    out = []
    for t in scan.get("texts", []):
        spec = clean_spec(t.get("text") or "")
        if looks_like_spec(spec):
            out.append((spec, t.get("x", 0.0), t.get("y", 0.0)))
    return out


def seg_distance(seg: list, lx: float, ly: float) -> float:
    """标注点到线段的距离（mm）。

    扫描端 0.4.29 起给每个线段带上两端坐标，这里算真正的「点到线段」距离：
    一条 60m 直线只有中点时，标在两端也超过 30m 半径，会被判成匹配不上。
    老扫描 JSON 没有端点（长度 4），退回中点到标注点的距离。
    """
    if len(seg) >= 8:
        x1, y1, x2, y2 = seg[4], seg[5], seg[6], seg[7]
        dx, dy = x2 - x1, y2 - y1
        den = dx * dx + dy * dy
        if den <= 1e-9:
            return math.hypot(lx - x1, ly - y1)
        t = max(0.0, min(1.0, ((lx - x1) * dx + (ly - y1) * dy) / den))
        return math.hypot(lx - (x1 + t * dx), ly - (y1 + t * dy))
    return math.hypot(lx - seg[2], ly - seg[3])


def match_plan_specs(scans: list[dict], radius_mm: float,
                     propagate_radius_mm: float = 2500.0,
                     propagate_rounds: int = 3) -> tuple[dict, dict, int, float]:
    """没有回路号时按「规格标注」就近匹配线段，仍按规格分档出量。

    回路号缺失只影响「分回路」这一层，不影响按规格算管长/线长——
    概算要的正是按规格分档的量。回路列留空（记为 `-`）并在口径页说明。

    距离法只够照到标注附近：实测 J-5 照明线 3289m 里，30m 内只有 1396m。
    剩下的一大半并不在别的回路上，而是同一条回路的远端——同一回路的线是连着的，
    所以再跑一轮「相邻传播」：已定规格的线段把规格传给 2.5m 内未定的同层线段。
    传播来的量在「置信度分级」里记低，和直接命中的量分开，方便人工只抽查低置信度那部分。
    """
    by_spec: dict[str, dict] = defaultdict(
        lambda: {"length_mm": 0.0, "circuits": set(), "sources": Counter(),
                 "samples": [], "confidence": defaultdict(float)})
    by_layer: dict[str, dict] = defaultdict(lambda: {"total": 0.0, "matched": 0.0})
    label_count = 0
    propagated_mm = 0.0
    unmatched: list[dict] = []
    for scan in scans:
        labels = plan_spec_labels(scan)
        label_count += len(labels)
        items: list[dict] = []
        for seg in scan.get("segments", []):
            layer, length, x, y = seg[0], seg[1], seg[2], seg[3]
            by_layer[layer]["total"] += length
            if not is_electric_route_layer(layer):
                continue
            items.append({"layer": layer, "length": length, "x": x, "y": y,
                          "seg": seg, "spec": None, "how": ""})
        if not items:
            continue
        if labels:
            for it in items:
                best, best_d = None, None
                for spec, lx, ly in labels:
                    d = seg_distance(it["seg"], lx, ly)
                    if best_d is None or d < best_d:
                        best, best_d = spec, d
                if best is not None and best_d <= radius_mm:
                    it["spec"], it["how"] = best, "标注"
        if propagate_radius_mm > 0:
            propagate_route_specs(items, propagate_radius_mm, propagate_rounds)
        for it in items:
            spec = it["spec"]
            length = it["length"]
            if not spec:
                unmatched.append({"file": scan.get("file", ""), "layer": it["layer"],
                                  "length_mm": length, "x": it["x"], "y": it["y"]})
                continue
            rec = by_spec[spec]
            rec["length_mm"] += length
            rec["circuits"].add("-")
            if it["how"] == "传播":
                rec["confidence"]["低"] += length
                propagated_mm += length
            else:
                rec["confidence"]["中"] += length
            rec["sources"][scan.get("file", "")] += length
            if len(rec["samples"]) < 3:
                rec["samples"].append(f"({it['x']:,.0f},{it['y']:,.0f})")
            by_layer[it["layer"]]["matched"] += length
            by_layer[it["layer"]].setdefault("specs", Counter())[spec] += length
    return by_spec, by_layer, label_count, propagated_mm, unmatched


def _item_distance(a: dict, b: dict) -> float:
    """线段 a 到线段 b 的距离（mm）：两端点对端点集取最小；无端点时退回中点距。"""
    sa, sb = a.get("seg") or [], b.get("seg") or []
    if len(sa) >= 8 and len(sb) >= 8:
        return min(
            seg_distance(sa, sb[4], sb[5]), seg_distance(sa, sb[6], sb[7]),
            seg_distance(sb, sa[4], sa[5]), seg_distance(sb, sa[6], sa[7]),
        )
    return math.hypot(a["x"] - b["x"], a["y"] - b["y"])


def _anchor_cells(it: dict, cell: float) -> list[tuple[int, int]]:
    """线段占用的网格：中点 + 两端，长线不会被当成只有一个点。"""
    cells = [(int(it["x"] // cell), int(it["y"] // cell))]
    seg = it.get("seg") or []
    if len(seg) >= 8:
        for px, py in ((seg[4], seg[5]), (seg[6], seg[7])):
            c = (int(px // cell), int(py // cell))
            if c not in cells:
                cells.append(c)
    return cells


def propagate_route_specs(items: list[dict], radius_mm: float, rounds: int = 3) -> int:
    """把已定规格传给相邻未定线段；返回传播成功的线段数。

    不做连通图追踪——同层平行走的线多半同回路同规格，追连通反而容易漏。
    层不同绝不传播（强电/弱电不能串）。
    """
    cell = max(radius_mm, 1.0)
    total = 0
    for _ in range(max(int(rounds), 0)):
        grid: dict[tuple[int, int], list[dict]] = defaultdict(list)
        for it in items:
            if it["spec"]:
                for c in _anchor_cells(it, cell):
                    grid[c].append(it)
        changed = 0
        for it in items:
            if it["spec"]:
                continue
            best, best_d = None, None
            seen = set()
            for c in _anchor_cells(it, cell):
                gx, gy = c
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        for nb in grid.get((gx + dx, gy + dy), ()):
                            if id(nb) in seen or nb["layer"] != it["layer"]:
                                continue
                            seen.add(id(nb))
                            d = _item_distance(it, nb)
                            if d <= radius_mm and (best_d is None or d < best_d):
                                best, best_d = nb["spec"], d
            if best:
                it["spec"], it["how"] = best, "传播"
                changed += 1
        total += changed
        if not changed:
            break
    return total


def device_rows(scans: list[dict]) -> list[tuple[str, int, dict]]:
    rows: dict[str, dict] = {}
    for scan in scans:
        for raw, n in scan["attrib_groups"].get("A", {}).items():
            text = decode_cad_text(raw).strip()
            if DOOR_CODE.match(text) or TAG_CODE.match(text):
                continue
            if len(text) <= 2 and not re.search(r"[\u4e00-\u9fff]", text):
                continue
            rec = rows.setdefault(text, {"qty": 0, "sources": Counter()})
            rec["qty"] += n
            rec["sources"][scan.get("file", "")] += n
    return [(text, rec["qty"], dict(rec["sources"]))
            for text, rec in sorted(rows.items(), key=lambda kv: -kv[1]["qty"])]


def support_family(layer: str) -> str:
    up = layer.upper()
    if "喷淋" in up or "SPRINKLER" in up:
        return "sprinkler"
    if "消防" in up or "水炮" in up or "FIRE" in up:
        return "fire"
    if any(k in up for k in ("给水", "中水", "SUPPLY")):
        return "supply"
    if any(k in up for k in ("排水", "废水", "污水", "雨水", "压力废", "压力污", "通气", "DRAIN")):
        return "drainage"
    return "default"


def support_estimates(by_dn: dict, dn_unmatched: dict, tray_mm: float, cfg: dict,
                      inferred: dict | None = None) -> list[list]:
    """按管径分档估算水专业支架数；桥架按水平吊架间距估算。"""
    spacing_cfg = cfg.get("water_support_spacing_m", {})
    totals: dict[tuple[str, str], float] = defaultdict(float)
    inferred = inferred or {}
    for key, mm in by_dn.items():
        totals[key] += mm
    for key, mm in dn_unmatched.items():
        layer = key[0] if isinstance(key, tuple) else key
        totals[(layer, "默认")] += mm
    rows: list[list] = []
    for (layer, dn), mm in sorted(totals.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        family = support_family(layer)
        spacing_map = spacing_cfg.get(family, spacing_cfg.get("default", {}))
        spacing = spacing_map.get(dn, spacing_map.get("default", 3.0))
        count = math.ceil(mm / 1000 / max(spacing, 0.1))
        note = "含邻近管段兜底推测" if inferred.get((layer, dn), 0) > 0 else ""
        rows.append([layer, dn, round(mm / 1000, 1), spacing, count, note])
    if tray_mm > 0:
        spacing = cfg.get("tray_support_spacing_m", 1.5)
        rows.append(["桥架", "全部", round(tray_mm / 1000, 1), spacing,
                     math.ceil(tray_mm / 1000 / spacing), "水平吊架估算"])
    return rows


def conservation_row(name: str, source_mm: float, classified_mm: float,
                     allow_partial: bool = False) -> list:
    """源总长 vs 分档合计。

    `allow_partial`：该类图元允许「有一部分没出量」（比如某段电线就近找不到规格），
    此时差值为正记「未出量」而不是「异常」——早期版本把 matched + (total-matched)
    当成合计，恒等于源总长，那张表永远全「通过」，等于没核对。
    """
    diff = source_mm - classified_mm
    if abs(diff) <= 500:
        status = "通过"
    elif allow_partial and diff > 0:
        status = "未出量"
    else:
        status = "异常"
    return [name, round(source_mm / 1000, 1), round(classified_mm / 1000, 1),
            round(diff / 1000, 1), status]


def tray_route_totals(scans: list[dict], max_segment_mm: float = 50_000) -> tuple[float, float]:
    """桥架单段量汇总；超过阈值的长线按异常剔除并单独计数。"""
    total_mm = 0.0
    excluded_mm = 0.0
    for scan in scans:
        for layer, length_mm, *_xy in scan.get("segments", []):
            if not is_tray_route_layer(layer):
                continue
            if length_mm > max_segment_mm:
                excluded_mm += length_mm
            else:
                total_mm += length_mm
    return total_mm, excluded_mm


def tray_route_by_layer(scans: list[dict], max_segment_mm: float = 50_000) -> dict[str, float]:
    """桥架按图层计入量（已剔除异常长线），用于和图层总长对账。"""
    out: dict[str, float] = defaultdict(float)
    for scan in scans:
        for layer, length_mm, *_xy in scan.get("segments", []):
            if not is_tray_route_layer(layer):
                continue
            if length_mm <= max_segment_mm:
                out[layer] += length_mm
    return out


def wire_expanded_length(route_m: float, cores: int, reserve_m: float) -> float:
    """电线展开：单段路由和两端预留都按芯数展开。"""
    return (route_m + reserve_m) * max(int(cores), 1)


def table_rows(scan: dict) -> list[list[str]]:
    rows = defaultdict(list)
    for rec in scan.get("devices", []):
        if rec["tag"] in TABLE_TAGS:
            rows[round(rec["y"] / 1000)].append(rec)
    dedupe: Counter = Counter()
    for _k, recs in sorted(rows.items()):
        tags = {r["tag"] for r in recs}
        if not ({"WHAT", "SN", "SNN"} & tags):
            continue
        recs.sort(key=lambda r: r["x"])
        key = tuple(sorted((r["tag"], r["text"]) for r in recs))
        dedupe[key] += 1
    out = []
    for key, n in dedupe.items():
        label = " | ".join(f"{tag}:{text}" for tag, text in key) + (f" ×{n}" if n > 1 else "")
        out.append([label])
    return out


def table_records(scan: dict) -> list[dict]:
    rows = defaultdict(list)
    for rec in scan.get("devices", []):
        if rec["tag"] in TABLE_TAGS:
            rows[round(rec["y"] / 1000)].append(rec)
    out = []
    for _key, recs in sorted(rows.items()):
        if not ({"WHAT", "SN", "SNN"} & {r["tag"] for r in recs}):
            continue
        recs.sort(key=lambda r: r["x"])
        names = [decode_cad_text(r["text"]).strip()
                 for r in recs if r["tag"] in ("WHAT", "SN", "SNN")]
        specs = sorted({decode_cad_text(r["text"]).strip()
                        for r in recs if r["tag"] == "SPEC"})
        units = [decode_cad_text(r["text"]).strip()
                 for r in recs if r["tag"] in ("UNIT", "UN")]
        numbers = []
        for r in recs:
            if r["tag"] == "数量":
                try:
                    numbers.append(float(r["text"]))
                except (TypeError, ValueError):
                    pass
        qty = max(numbers) if numbers else max(len(names), 1)
        name = next((v for v in names if v), "")
        if name:
            out.append({"name": name, "spec": " / ".join(specs),
                        "unit": next((v for v in units if v), ""), "qty": int(qty)})
    return out


def material_rows(scans: list[dict]) -> list[dict]:
    merged: dict[tuple[str, str, str], dict] = {}
    for scan in scans:
        for rec in table_records(scan):
            key = (rec["name"], rec["spec"], rec["unit"])
            row = merged.setdefault(key, {"qty": 0, "sources": Counter(), "rows": 0})
            row["qty"] += rec["qty"]
            row["rows"] += 1
            row["sources"][scan.get("file", "")] += rec["qty"]
    return [{"name": k[0], "spec": k[1], "unit": k[2], **v}
            for k, v in sorted(merged.items(), key=lambda kv: -kv[1]["qty"])]


def measurement_candidates(data: dict | None) -> list[dict]:
    """读取 cad-file-reader 测量候选，只作识图证据，不参与本技能算量。"""
    if not isinstance(data, dict):
        return []
    rows = data.get("measurements")
    return [row for row in rows if isinstance(row, dict)] if isinstance(rows, list) else []


def mep_relations(data: dict | None) -> list[dict]:
    """读取 cad-file-reader MEP 几何候选（设备-管段/立管-管段/端点冲突）；只作复核证据。"""
    if not isinstance(data, dict):
        return []
    rows = data.get("mep_relations")
    return [r for r in rows if isinstance(r, dict)] if isinstance(rows, list) else []


def cad_validate_json(path: str) -> dict:
    """可选：用 cad-file-reader cad_validate.sh 校验交接 JSON；缺底座/失败不阻断。"""
    import os, subprocess
    base = os.environ.get("CAD_SKILL_DIR")
    if not base:
        for d in (Path(__file__).resolve().parent.parent.parent / "cad-file-reader",
                  *sorted(Path.home().glob(".workbuddy/skills/*/cad-file-reader")),
                  Path.home() / ".claude/skills/cad-file-reader",
                  Path.home() / ".codex/skills/cad-file-reader"):
            if Path(d).is_dir():
                base = d
                break
    if not base:
        return {}
    validator = Path(base) / "scripts" / "cad_validate.sh"
    if not validator.exists():
        return {}
    try:
        r = subprocess.run(["bash", str(validator), path], capture_output=True, text=True, timeout=180)
    except Exception as exc:
        return {"ok": False, "errors": [f"{type(exc).__name__}: {exc}"]}
    errors = []
    for ln in r.stdout.splitlines():
        if not ln.strip():
            continue
        try:
            rec = json.loads(ln)
            errors.extend(rec.get("errors") or [])
        except Exception:
            pass
    return {"ok": r.returncode == 0 and not errors, "errors": errors[:20]}


def source_text(sources: dict) -> str:
    return "；".join(f"{k}:{v:,.0f}"
                     for k, v in sorted(sources.items(), key=lambda kv: -kv[1]) if k)


def water_blocks(scans: list[dict]) -> list[tuple[str, str, int]]:
    merged: dict[str, int] = defaultdict(int)
    src = {}
    for scan in scans:
        for name, n in scan["inserts"].items():
            if name.startswith("$"):
                merged[name] += n
                src[name] = scan["file"]
    rows = []
    for name, n in sorted(merged.items(), key=lambda kv: -kv[1])[:20]:
        kind = ("阀门类" if name.startswith("$VALVE$")
                else "电动阀类(需核对)" if name.startswith("$EVALVE$")
                else "天正设备符号(需图例核对)" if name.startswith("$TwtSys$")
                else "附件类(需核对)")
        rows.append((src[name], name, n, kind))
    return rows


def build(scans: list[dict], sys_scans: list[dict], cfg: dict, out_prefix: str,
          trunk_scans: list[dict] | None = None, cad_measurement: dict | None = None,
          mep_geometry: dict | None = None, stats: dict | None = None) -> Path:
    specs, _ctype = spec_tables(sys_scans)
    boxed_specs = boxed_system_specs(
        sys_scans, cfg.get("system_box_spec_radius_mm", 250_000)
    )
    by_spec, by_layer, ambiguous, unmatched_rows = match_circuits(
        scans, specs, cfg.get("match_radius_mm", 30000),
        cfg.get("electrical_high_radius_mm", 10000)
    )
    # 无线号图纸兜底：平面图只标「规格」不标「回路号」时（样例这批全是），
    # 走规格就近匹配。有回路号时不动，避免和系统图口径重复计数。
    plan_spec_labels_n = 0
    propagated_mm = 0.0
    if not by_spec:
        by_spec, by_layer, plan_spec_labels_n, propagated_mm, unmatched_rows = match_plan_specs(
            scans, cfg.get("match_radius_mm", 30000),
            float(cfg.get("propagate_radius_mm", 2500)),
            int(cfg.get("propagate_rounds", 3)))

    conduits, cables, wires = [], [], []
    for spec, rec in sorted(by_spec.items(), key=lambda kv: -kv[1]["length_mm"]):
        info = parse_spec(spec)
        length_m = rec["length_mm"] / 1000
        n_circuit = len(rec["circuits"])
        if info["conduit"]:
            order = length_m * (1 + cfg["conduit_loss_pct"] / 100)
            conduits.append((info["conduit"], spec, round(length_m, 1), n_circuit, round(order, 1)))
        elif info["tray"]:
            order = length_m * (1 + cfg["tray_loss_pct"] / 100)
            conduits.append(("MR桥架", spec, round(length_m, 1), n_circuit, round(order, 1)))
        reserve = cfg["reserve_per_end_m"] * 2 * n_circuit
        if info["is_cable"]:
            order = (length_m + reserve) * (1 + cfg["cable_loss_pct"] / 100)
            cables.append((spec, "电缆", round(length_m, 1), info["cores"], round(reserve, 1),
                           round(length_m + reserve, 1), round(order, 1)))
        elif not info["is_cable"] and info["core_size"]:
            expanded_len = wire_expanded_length(length_m, info["cores"], reserve)
            order = expanded_len * (1 + cfg["wire_loss_pct"] / 100)
            wires.append((f"{info['family']}-{info['core_size']}", spec, round(length_m, 1),
                          info["cores"], round(reserve, 1), round(expanded_len, 1), round(order, 1)))

    devices = device_rows(scans)
    dev_loss = cfg["device_loss_pct"] / 100
    tray_max_segment_mm = max(float(cfg.get("tray_max_segment_mm", 50_000)), 1.0)
    tray_mm, tray_excluded_mm = tray_route_totals(scans, tray_max_segment_mm)
    # 水专业/桥架的分档量提前算出来，「图层分档」和「总量守恒」两张表才能跟源总长对账
    water_records = water_segment_specs(
        scans,
        cfg.get("water_match_radius_mm", 15000),
        cfg.get("water_fallback_radius_mm", 30000),
    )
    by_dn, dn_inferred, dn_unmatched = water_diameter_from_records(water_records)
    water_done_by_layer: dict[str, float] = defaultdict(float)
    for rec in water_records:
        if rec["dn"]:
            water_done_by_layer[rec["layer"]] += rec["length_mm"]
    tray_by_layer = tray_route_by_layer(scans, tray_max_segment_mm)

    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font
    except ImportError as exc:  # pragma: no cover - 环境缺失时的友好提示
        raise SystemExit(
            "❌ 生成 xlsx 需要 openpyxl。\n"
            "   已随底座 vendor 提供时可自动导入；若仍报错，请执行：\n"
            "     bash scripts/setup.sh            # 推荐，自动补齐依赖\n"
            "     python3 -m pip install openpyxl  # 或手动安装\n"
        ) from exc

    wb = Workbook()
    bold = Font(bold=True)
    notes = [
        "口径：计划口径 ±5~10%，不替代翻样/下料/结算",
        "管长=单线中心线水平投影；未含立管/竖向（立管见配置估算）",
        "回路匹配=线段就近标注（默认半径30m），多规格回路取多数规格并在歧义列提示",
        "电线展开=(路由长＋两端预留)×芯数；预留=每端" + str(cfg["reserve_per_end_m"]) + "m×回路数；损耗按 loss_rules.json",
        "桥架剔除单段>" + str(round(tray_max_segment_mm / 1000, 1)) + "m异常线；剔除量单独列出",
    ]
    if plan_spec_labels_n:
        notes.append(
            "本批图纸平面只标规格、未标回路号（共识别 " + str(plan_spec_labels_n) +
            " 处规格标注）：回路列记 `-`，按规格出量；分回路需另配配电系统图")
    if propagated_mm > 0:
        notes.append(
            "其中 " + str(round(propagated_mm / 1000, 1)) +
            "m 由相邻线段传播定规格（置信度=低），抽样核对时优先看这部分")
    notes.append("标注层(DIM-*)、设备符号层(EQUIP-*)、图框/墙体/轴网不计入任何量，见「图层分档」")
    ws = wb.active
    ws.title = "口径"
    for n in notes:
        ws.append([n])

    ws = wb.create_sheet("输入质量核对")
    ws.append(["文件", "识图域", "图面单位", "单位状态", "坐标单位", "块参照数", "块内几何提示"])
    for scan in scans:
        unit = scan.get("drawing_unit") or {}
        ws.append([
            scan.get("file", ""), scan.get("domain", ""),
            unit.get("effective") or "unknown", unit.get("status") or "review",
            unit.get("insunits", ""), scan.get("block_reference_count", 0),
            scan.get("block_geometry_review", ""),
        ])
    ws["A1"].font = bold

    measure_rows = measurement_candidates(cad_measurement)
    ws = wb.create_sheet("CAD测量候选核对")
    ws.append(["说明", "cad-file-reader 测量候选只作识图证据，final_quantity=false；不参与本技能管长/材料/损耗计算"])
    ws.append(["编号", "类型", "候选值", "单位", "依据", "状态", "复核原因", "源 schema", "源编号"])
    for row in measure_rows:
        ws.append([
            row.get("id", ""), row.get("kind", ""), row.get("value", ""), row.get("unit", ""),
            row.get("basis", ""), row.get("status", ""), row.get("review_reason", ""),
            row.get("source_schema", ""), row.get("source_id", ""),
        ])
    ws["A1"].font = bold

    mep_rows = mep_relations(mep_geometry)
    ws = wb.create_sheet("MEP关联候选核对")
    ws.append(["说明", "cad-file-reader MEP 几何候选只作复核证据（设备-管段/立管-管段/端点冲突），final_quantity=false；不参与算量"])
    ws.append(["编号", "关联类型", "系统", "路由类", "状态", "复核原因", "源 schema", "源编号"])
    for row in mep_rows:
        ws.append([
            row.get("id", ""), row.get("relation_type", ""), row.get("system", ""),
            row.get("route_class", ""), row.get("status", ""), row.get("review_reason", ""),
            row.get("source_schema", ""), row.get("source_id", ""),
        ])
    ws["A1"].font = bold

    ws = wb.create_sheet("规范约束")
    ws.append(["层级", "对象", "规范要求", "当前算法", "覆盖状态", "修正建议"])
    std_path = Path(__file__).parent.parent / "references/standard_rules.json"
    std_rules = json.load(open(std_path, encoding="utf-8")) if std_path.exists() else {"checks": []}
    for row in std_rules.get("checks", []):
        ws.append([
            row.get("layer", ""),
            row.get("object", ""),
            row.get("rule", ""),
            row.get("current", ""),
            row.get("coverage", ""),
            row.get("action", "")
        ])
    ws["A1"].font = bold

    mapping_path = Path(__file__).parent.parent / "references/dual_caliber_rules.json"
    mapping_rules = json.load(open(mapping_path, encoding="utf-8")) if mapping_path.exists() else {"rows": []}
    ws = wb.create_sheet("双口径映射")
    ws.append(["图纸对象", "概算清单项", "概算单位", "项目特征要点", "概算计算规则",
               "物资材料行", "物资单位", "物资计算规则", "输出定位", "依据", "覆盖状态"])
    for row in mapping_rules.get("rows", []):
        ws.append([row.get(k, "") for k in (
            "drawing_object", "boq_item", "boq_unit", "boq_feature", "boq_rule",
            "material_item", "material_unit", "material_rule", "output_location", "basis", "status"
        )])
    ws["A1"].font = bold

    ws = wb.create_sheet("导管与桥架")
    ws.append(["导管/桥架", "回路规格", "匹配长度m", "回路数", "订货量m"])
    for row in conduits:
        ws.append(list(row))
    ws["A1"].font = bold

    ws = wb.create_sheet("电线电缆")
    ws.append(["规格/名称", "类别/来源规格", "路由长m", "芯数", "预留m", "展开长度m", "订货量m"])
    for row in cables + wires:
        ws.append(list(row))
    ws["A1"].font = bold

    if tray_mm > 0:
        ws = wb["导管与桥架"]
        ws.append(["桥架(计入≤" + str(round(tray_max_segment_mm / 1000, 1)) + "m单段)", "CABLETRAY 类图层",
                   round(tray_mm / 1000, 1), "",
                   round(tray_mm / 1000 * (1 + cfg["tray_loss_pct"] / 100), 1)])
        if tray_excluded_mm > 0:
            ws.append(["桥架异常剔除", ">" + str(round(tray_max_segment_mm / 1000, 1)) + "m单段",
                       round(tray_excluded_mm / 1000, 1), "", ""])

    trunk_scans = trunk_scans or []
    trunks = trunk_cables(sys_scans)
    trunk_matched, trunk_unmatched, trunk_route_layers, trunk_conf = trunk_routes(
        trunk_scans, cfg.get("match_radius_mm", 30000)
    )
    if trunks or trunk_scans:
        ws = wb.create_sheet("干线电缆")
        ws.append(["规格", "系统图次数", "就近干线段长度m", "订货量m", "说明"])
        cable_loss = cfg["cable_loss_pct"] / 100
        for spec in sorted(set(trunks) | set(trunk_matched),
                           key=lambda s: (-trunk_matched.get(s, 0), -trunks.get(s, 0), s))[:40]:
            route_m = trunk_matched.get(spec, 0) / 1000
            order = route_m * (1 + cable_loss) if route_m else ""
            note = ("就近干线段估算" if route_m else
                    "[推测] 系统图次数≈表行数；无就近规格标注，需结合干线平面")
            ws.append([spec, trunks.get(spec, 0), round(route_m, 1) if route_m else "",
                       round(order, 1) if route_m else "", note])
        if trunk_route_layers:
            ws.append([])
            ws.append(["干线平面图层", "总长m", "对象数", "未分配m", "说明"])
            for layer, rec in sorted(trunk_route_layers.items(), key=lambda kv: -kv[1][0]):
                ws.append([layer, round(rec[0] / 1000, 1), rec[1],
                           round(trunk_unmatched.get(layer, 0) / 1000, 1),
                           "无就近规格标注时需人工分配"])
        ws["A1"].font = bold

    ws = wb.create_sheet("设备")
    ws.append(["设备名称(图面属性)", "数量", "订货量(含损耗)"])
    for text, n, _sources in devices:
        ws.append([text, n, round(n * (1 + dev_loss), 1)])
    ws["A1"].font = bold

    ws = wb.create_sheet("图层分档")
    ws.append(["图层", "总长m", "归属", "已出量m", "未出量m", "说明"])
    tray_by_layer = tray_route_by_layer(scans)
    for layer, rec in sorted(by_layer.items(), key=lambda kv: -kv[1]["total"]):
        if rec["total"] <= 1000:
            continue
        role, note = layer_role(layer)
        total_m = rec["total"] / 1000
        if role == "电气回路":
            done = rec["matched"] / 1000
        elif role == "桥架":
            done = tray_by_layer.get(layer, 0.0) / 1000
        elif role == "水专业":
            done = water_done_by_layer.get(layer, 0.0) / 1000
        else:
            done = 0.0
        unmatched_m = max(total_m - done, 0.0)
        if role == "电气回路" and rec["matched"] > 0 and unmatched_m > total_m * 0.30:
            layer_specs = rec.get("specs") or {}
            if layer_specs:
                top_spec, top_mm = layer_specs.most_common(1)[0]
                pct = top_mm / rec["matched"] * 100
                note += (f"；未出量段无就近标注，主规格候选 {top_spec}"
                         f"（占已匹配 {pct:.0f}%），需人工确认后按此分档")
        ws.append([layer, round(total_m, 1), role, round(done, 1),
                   round(unmatched_m, 1), note])
    ws.append([])
    ws.append(["歧义回路(多规格取多数)", "命中次数"])
    for token, n in ambiguous.most_common(20):
        ws.append([token, n])
    ws["A1"].font = bold

    ws = wb.create_sheet("配电箱回路")
    ws.append(["配电箱", "回路", "规格", "管长m", "对象数", "样本坐标", "来源文件", "状态"])
    for row in box_circuits(scans, specs, cfg.get("match_radius_mm", 30000), boxed_specs):
        ws.append([row["box"], row["circuit"], row["spec"],
                   round(row["length_mm"] / 1000, 1), row["objects"],
                   " ".join(row["samples"]), source_text(row["sources"]),
                   "歧义，需抽查" if row["ambiguous"] else "需抽查"])
    ws["A1"].font = bold

    ws = wb.create_sheet("未匹配坐标簇")
    ws.append(["来源文件", "x区间m", "y区间m", "未匹配m", "对象数", "图层", "样本坐标"])
    for rec in cluster_unmatched(unmatched_rows):
        x0, x1 = rec["gx"] * 50_000 / 1000, (rec["gx"] + 1) * 50_000 / 1000
        y0, y1 = rec["gy"] * 50_000 / 1000, (rec["gy"] + 1) * 50_000 / 1000
        layers = "；".join(f"{layer} {mm / 1000:.1f}m"
                           for layer, mm in rec["layers"].most_common(3))
        ws.append([rec["file"], f"{x0:,.0f}-{x1:,.0f}", f"{y0:,.0f}-{y1:,.0f}",
                   round(rec["length_mm"] / 1000, 1), rec["objects"],
                   layers, " ".join(rec["samples"])])
    ws["A1"].font = bold

    ws = wb.create_sheet("分层")
    zones = sorted({z for s in scans for z in s.get("wire_by_zone", {})})
    ws.append(["文件", "分区", "管线/设备摘要"])
    for scan in scans:
        for z, layers in scan.get("wire_by_zone", {}).items():
            top = "；".join(f"{k} {v:,.0f}m" for k, v in list(layers.items())[:4])
            ws.append([scan["file"], z, top])
        for z, devs in scan.get("devices_by_zone", {}).items():
            ws.append([scan["file"], z, f"设备总数 {sum(devs.values())}"])
    ws["A1"].font = bold

    ws = wb.create_sheet("水专业")
    ws.append(["图层", "长度m", "对象数"])
    merged: dict[str, list] = defaultdict(lambda: [0.0, 0])
    water_source_totals: dict[str, float] = defaultdict(float)
    water_layer_sources: dict[str, Counter] = defaultdict(Counter)
    for scan in scans:
        for layer, rec in scan["wire_layers"].items():
            if is_pipe_route_layer(layer):
                merged[layer][0] += rec["length_mm"]
                merged[layer][1] += rec["entities"]
                water_source_totals[layer] += rec["length_mm"]
                water_layer_sources[layer][scan["file"]] += rec["length_mm"]
    for layer, (mm, n) in sorted(merged.items(), key=lambda kv: -kv[1][0]):
        ws.append([layer, round(mm / 1000, 1), n])
    riser_rows = riser_identification(scans)
    n_floors = cfg.get("riser_floor_count") or max(
        (len(s.get("floor_labels", {})) for s in scans), default=1
    )
    riser_m_each = cfg["floor_height_mm"] / 1000 * max(n_floors - 1, 1)
    loss = cfg.get("water_pipe_loss_pct", 3.0) / 100
    water_totals = defaultdict(float)
    for key, mm in by_dn.items():
        water_totals[key] += mm
    for key, mm in dn_inferred.items():
        water_totals[key] += mm
    ws.append([])
    ws.append(["图层", "管径", "匹配长度m", "订货量m", "说明"])
    for (layer, dn), mm in sorted(water_totals.items(), key=lambda kv: -kv[1]):
        m_len = mm / 1000
        inferred_m = dn_inferred.get((layer, dn), 0) / 1000
        note = f"含邻近管段兜底推测 {round(inferred_m, 1)}m" if inferred_m > 0 else ""
        ws.append([layer, dn, round(m_len, 1), round(m_len * (1 + loss), 1), note])
    for layer, mm in sorted(dn_unmatched.items(), key=lambda kv: -kv[1]):
        if mm > 1000:
            ws.append([layer, "未标注", round(mm / 1000, 1), "", "就近无 DN 标注，需人工"])
    ws.append([])
    ws.append(["出处", "块名", "数量", "类别"])
    for row in water_blocks(scans):
        ws.append(list(row))
    ws["A1"].font = bold

    zone_groups: dict[tuple[str, str], dict] = defaultdict(
        lambda: {"length_mm": 0.0, "objects": 0, "layers": {}, "sources": Counter()}
    )
    for scan in scans:
        for layer, rec in scan["wire_layers"].items():
            if not is_pipe_route_layer(layer):
                continue
            system = water_system(layer)
            key = (system, water_zone(layer, system))
            group = zone_groups[key]
            group["length_mm"] += rec["length_mm"]
            group["objects"] += rec["entities"]
            group["layers"][layer] = rec["length_mm"]
            group["sources"][scan["file"]] += rec["length_mm"]

    ws = wb.create_sheet("水系统分区")
    ws.append(["系统", "分区", "水平长度m", "对象数", "直接DN匹配m",
               "邻近兜底m", "未标注m", "来源文件"])
    for (system, zone), rec in sorted(
        zone_groups.items(), key=lambda kv: (-kv[1]["length_mm"], kv[0])
    ):
        layers = rec["layers"]
        matched = sum(mm for (layer, _dn), mm in by_dn.items() if layer in layers)
        inferred = sum(mm for (layer, _dn), mm in dn_inferred.items() if layer in layers)
        unmatched = sum(mm for layer, mm in dn_unmatched.items() if layer in layers)
        ws.append([system, zone, round(rec["length_mm"] / 1000, 1), rec["objects"],
                   round(matched / 1000, 1), round(inferred / 1000, 1),
                   round(unmatched / 1000, 1), source_text(rec["sources"])])
    ws["A1"].font = bold

    connect_summary, connect_rows = connectivity_check(
        water_records, cfg, cfg.get("connectivity_max_rows", 50)
    )
    ws = wb.create_sheet("连通性核对")
    ws.append(["指标", "数值", "说明"])
    for row in connect_summary:
        ws.append(row)
    ws.append([])
    ws.append(["类别", "系统", "管径", "图层/分区", "来源文件", "坐标区间m",
               "断点数", "关联段长m", "孤立段对象数", "疑似跨层/分区",
               "样本坐标", "状态"])
    for row in connect_rows:
        ws.append(row)
    ws.append([])
    ws.append(["类别", "系统", "对象", "数量", "来源文件", "图层/样本", "样本坐标", "状态"])
    for row in water_zone_riser_rows(zone_groups, riser_rows):
        ws.append(row)
    ws["A1"].font = bold

    ws = wb.create_sheet("立管识别")
    ws.append(["系统", "立管编号", "图面出现次数", "来源文件", "样本",
               "单根折算m", "状态"])
    for rec in riser_rows:
        ws.append([rec["system"], rec["id"], rec["count"], source_text(rec["sources"]),
                   rec["sample"], round(riser_m_each, 1),
                   "[推测] 立管折算未含水平管、变径和附件，需按系统图核对"])
    if riser_rows:
        ws.append(["合计", f"{len(riser_rows)} 根", "",
                   "", "", round(riser_m_each * len(riser_rows), 1),
                   "同号跨图只计 1 根"])
    ws["A1"].font = bold

    ws = wb.create_sheet("支架估算")
    ws.append(["系统/图层", "管径", "净长m", "间距m", "估算数量", "说明"])
    for row in support_estimates(water_totals, dn_unmatched, tray_mm, cfg, dn_inferred):
        ws.append(row)
    ws["A1"].font = bold

    ws = wb.create_sheet("置信度分级")
    ws.append(["类别", "对象", "高m", "中m", "低m", "合计m", "高占比%", "中占比%", "低占比%"])

    def conf_row(kind: str, name: str, conf: dict) -> list:
        vals = [conf.get(k, 0.0) / 1000 for k in ("高", "中", "低")]
        total = sum(vals)
        pct = [round(v / total * 100, 1) if total else 0.0 for v in vals]
        return [kind, name, round(vals[0], 1), round(vals[1], 1), round(vals[2], 1),
                round(total, 1), *pct]

    for spec, rec in by_spec.items():
        ws.append(conf_row("电气回路", spec, rec["confidence"]))
    for layer in water_source_totals:
        conf = defaultdict(float)
        for (pipe_layer, _dn), mm in by_dn.items():
            if pipe_layer == layer:
                conf["高"] += mm
        for (pipe_layer, _dn), mm in dn_inferred.items():
            if pipe_layer == layer:
                conf["中"] += mm
        conf["低"] = max(water_source_totals[layer] - conf["高"] - conf["中"], 0.0)
        ws.append(conf_row("水专业", layer, conf))
    for layer, conf in trunk_conf.items():
        ws.append(conf_row("干线", layer, conf))
    ws["A1"].font = bold

    ws = wb.create_sheet("总量守恒")
    ws.append(["对象", "源总长m", "分档合计m", "差值m", "状态", "说明"])
    for layer, rec in by_layer.items():
        if rec["total"] <= 1000:
            continue
        role, _note = layer_role(layer)
        if role == "电气回路":
            if rec["matched"] <= 0:
                hint = "整层无规格标注（避雷/接地/应急类回路图上通常不标，照明类需人工确认）"
            else:
                hint = "未出量=就近无规格标注，见「图层分档」主规格候选"
            ws.append(conservation_row(f"电气-{layer}", rec["total"], rec["matched"],
                                       allow_partial=True) + [hint])
        elif role == "桥架":
            ws.append(conservation_row(f"桥架-{layer}", rec["total"],
                                       tray_by_layer.get(layer, 0.0), allow_partial=True)
                      + ["未出量=超过单段阈值的异常长线，已在「导管与桥架」单列"])
    for layer, source_mm in water_source_totals.items():
        classified = sum(mm for (pipe_layer, _dn), mm in by_dn.items() if pipe_layer == layer)
        classified += sum(mm for (pipe_layer, _dn), mm in dn_inferred.items() if pipe_layer == layer)
        classified += max(dn_unmatched.get(layer, 0.0), 0.0)
        ws.append(conservation_row(f"水专业-{layer}", source_mm, classified) + ["含未标注管段"])
    for layer, rec in trunk_route_layers.items():
        classified = sum(trunk_conf.get(layer, {}).values())
        ws.append(conservation_row(f"干线-{layer}", rec[0], classified) + ["干线规格就近匹配"])
    ws["A1"].font = bold

    ws = wb.create_sheet("材料表提取")
    ws.append(["来源", "行(属性:文本)"])
    for scan in scans:
        for row in table_rows(scan):
            ws.append([scan["file"], " | ".join(row)])
    ws["A1"].font = bold

    ws = wb.create_sheet("材料归并")
    ws.append(["名称", "规格", "单位", "数量", "来源文件", "原始行数", "状态"])
    for rec in material_rows(scans):
        status = "跨图重复，需核对图例" if len(rec["sources"]) > 1 else ""
        ws.append([rec["name"], rec["spec"], rec["unit"], rec["qty"],
                   source_text(rec["sources"]), rec["rows"], status])
    ws["A1"].font = bold

    ws = wb.create_sheet("立管估算")
    ws.append(["名称", "根数", "折算m", "说明"])
    for r in cfg.get("risers", []):
        meters = r.get("count", 0) * cfg["floor_height_mm"] / 1000 * max(n_floors - 1, 1)
        ws.append([r["name"], r.get("count", 0), round(meters, 1),
                   "[推测] 根数需人工从系统图数出后填入配置"])
    ws["A1"].font = bold

    ws = wb.create_sheet("核对清单")
    ws.append(["类别", "名称/规格", "数量/长度", "订货量", "来源文件", "图层/算法", "样本坐标", "状态"])
    for spec, rec in sorted(by_spec.items(), key=lambda kv: -kv[1]["length_mm"]):
        info = parse_spec(spec)
        length_m = rec["length_mm"] / 1000
        if info["conduit"]:
            kind, qty, order = "导管/桥架", length_m, length_m * (1 + cfg["conduit_loss_pct"] / 100)
            rule = "回路就近匹配"
        elif info["tray"]:
            kind, qty, order = "导管/桥架", length_m, length_m * (1 + cfg["tray_loss_pct"] / 100)
            rule = "回路就近匹配/桥架"
        elif info["is_cable"]:
            kind, qty, order = "电缆", length_m, length_m * (1 + cfg["cable_loss_pct"] / 100)
            rule = "回路就近匹配"
        else:
            kind, qty, order = "电线", length_m * info["cores"], length_m * info["cores"] * (1 + cfg["wire_loss_pct"] / 100)
            rule = "回路就近匹配×芯数"
        ws.append([kind, spec, round(qty, 1), round(order, 1),
                   source_text(rec["sources"]), rule, " ".join(rec["samples"]), "需抽查"])
    for spec, route_m in sorted(trunk_matched.items(), key=lambda kv: -kv[1]):
        ws.append(["干线电缆", spec, round(route_m / 1000, 1), round(route_m / 1000 * (1 + cfg["cable_loss_pct"] / 100), 1),
                   "；".join(s.get("file", "") for s in trunk_scans), "干线规格就近匹配", "", "需抽查"])
    for (layer, dn), mm in sorted(water_totals.items(), key=lambda kv: -kv[1]):
        status = "含兜底推测，需抽查" if dn_inferred.get((layer, dn), 0) > 0 else "需抽查"
        ws.append(["水专业", f"{layer} {dn}", round(mm / 1000, 1), round(mm / 1000 * (1 + loss), 1),
                   source_text(water_layer_sources.get(layer, {})), layer, "", status])
    for text, n, sources in devices:
        status = "跨图重复，需核对" if len(sources) > 1 else ""
        ws.append(["设备", text, n, round(n * (1 + dev_loss), 1), source_text(sources), "ATTRIB", "", status])
    for rec in material_rows(scans):
        status = "跨图重复，需核对图例" if len(rec["sources"]) > 1 else ""
        ws.append(["材料表", " ".join(x for x in (rec["name"], rec["spec"]) if x),
                   rec["qty"], "", source_text(rec["sources"]), "图纸材料表", "", status])
    ws["A1"].font = bold

    out = Path(out_prefix + ".xlsx")
    wb.save(out)
    if stats is not None:
        stats["members"] = _plan_members(by_spec, trunk_matched, water_totals, devices)
    return out



# ---------------------------------------------------------------- 来源闸门
FORMAL_PLAN_PROVENANCE = {"reader", "bus"}


def _doc_provenance(doc: dict) -> str:
    """取 scan JSON 的来源；兼容裸 scan、scan+contract、以及 reader 契约块。"""
    if not isinstance(doc, dict):
        return "manual"
    prov = str(doc.get("provenance") or "").strip().lower()
    if prov:
        return prov
    contract = doc.get("contract") if isinstance(doc.get("contract"), dict) else {}
    prov = str(contract.get("provenance") or "").strip().lower()
    if prov:
        return prov
    # reader 产出的 cad-contract/v1 一定有 contract_id；有它才算 reader 产物。
    # reader 详情 JSON 的版本写在 contract.contract_version，bus 包装件才写在顶层 schema。
    version = str(contract.get("contract_version") or contract.get("schema") or "").strip()
    if version == "cad-contract/v1" and str(contract.get("contract_id") or "").strip():
        return "reader"
    if str(doc.get("schema") or "") == "cad-contract/v1" and str(doc.get("contract_id") or "").strip():
        return "reader"
    return "manual"


def _doc_contract_id(doc: dict) -> str:
    if not isinstance(doc, dict):
        return ""
    return str(doc.get("contract_id") or (doc.get("contract") or {}).get("contract_id") or "").strip()


def guard_plan_sources(docs: list[tuple[str, dict]], *, allow_manual: bool) -> dict:
    """按输入 scan 的 provenance 判定来源；只有 reader/bus 才免手工开关。

    安装物资计划本身是概算口径，final_quantity 恒为 false；本闸门只解决
    “输入是不是识图链路产物”，不把物资计划冒充正式台账量。
    """
    if not docs:
        raise GuardError(5, "没有可用的扫描 JSON。", hint="先用 cad-file-reader 出契约，再 mep_scan --contract 生成 scan JSON。")
    provs, ids, src_shas, reader_versions, warnings = [], [], [], [], []
    for label, doc in docs:
        prov = _doc_provenance(doc)
        provs.append(prov)
        cid = _doc_contract_id(doc)
        if cid:
            ids.append(cid)
        sha = str(doc.get("source_sha256") or (doc.get("contract") or {}).get("source_sha256") or "").strip()
        if sha:
            src_shas.append(sha)
        rv = str(doc.get("reader_version") or (doc.get("contract") or {}).get("reader_version") or "").strip()
        if rv:
            reader_versions.append(rv)
        if prov not in FORMAL_PLAN_PROVENANCE:
            warnings.append("%s 的 provenance=%s，按手工来源处理。" % (label, prov or "缺失"))
    formal = all(p in FORMAL_PLAN_PROVENANCE for p in provs)
    if not formal and not allow_manual:
        raise GuardError(
            3,
            "扫描输入 provenance=%s，不是 reader/bus，拒入正式链路。" % "、".join(sorted(set(provs))),
            hint="确认是手工/旧扫描结果后加 --allow-manual；结果强制 final_quantity=false。",
        )
    return {
        "mode": "formal" if formal else "manual",
        "provenance": "reader" if formal else "manual",
        "contract_id": ",".join(dict.fromkeys(ids)),
        "source_sha256": ",".join(dict.fromkeys(src_shas)),
        "contract_sha256": "",
        "reader_version": reader_versions[0] if reader_versions else "",
        # 物资计划不是正式台账量：两种来源都锁 false。
        "formal_ledger_eligible": False,
        "warnings": warnings,
    }


def _plan_members(by_spec: dict, trunk_matched: dict, water_totals: dict,
                  devices: list) -> list:
    """把计划里的管/缆/线/水/设备折成交接成员；无重量、无坐标如实留空。"""
    members = []
    n = 0

    def add(kind, name, qty, unit, note=""):
        nonlocal n
        n += 1
        members.append(cs.handoff_member(
            "MEP-%04d" % n,
            weight_t=None, length_m=(round(float(qty), 2) if unit == "m" else None),
            section=str(name or ""), grade="", zone="",
            weight_basis="unknown", coord_status="missing",
            kind=kind, quantity=round(float(qty), 2), unit=unit, note=note))

    for spec, rec in sorted(by_spec.items(), key=lambda kv: -kv[1]["length_mm"]):
        info = parse_spec(spec)
        length_m = rec["length_mm"] / 1000.0
        if info.get("conduit"):
            add("导管", spec, length_m, "m", "回路就近匹配")
        elif info.get("tray"):
            add("桥架", spec, length_m, "m", "回路就近匹配")
        elif info.get("is_cable"):
            add("电缆", spec, length_m, "m", "回路就近匹配")
        else:
            add("电线", spec, length_m * info.get("cores", 1), "m", "回路就近匹配×芯数")
    for spec, route_mm in sorted(trunk_matched.items(), key=lambda kv: -kv[1]):
        add("干线电缆", spec, float(route_mm) / 1000.0, "m", "干线规格就近匹配")
    for (layer, dn), mm in sorted(water_totals.items(), key=lambda kv: -kv[1]):
        add("水专业管道", "%s %s" % (layer, dn), float(mm) / 1000.0, "m", "管径就近匹配")
    for text, count, _sources in devices:
        add("设备", text, float(count), "个", "ATTRIB 计数")
    return members


def write_plan_sidecars(out_prefix: str, guard: dict, stats: dict, argv: list) -> dict:
    """写 provenance / run_manifest / site_handoff；返回随输出打印的摘要。"""
    out = Path(out_prefix + ".xlsx")
    out_dir = out.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    prov = cs.provenance_fields(guard)
    prov["mode"] = guard.get("mode") or "manual"
    prov["boundary"] = ("安装物资计划=概算口径；只做回路/管径匹配与损耗折算，"
                        "final_quantity=false，不替代结算清单。")
    prov["inputs"] = stats.get("inputs") or []
    cs.write_json(Path(out_prefix + ".provenance.json"), prov)
    manifest = cs.run_manifest("anzhuang-suanliang", _skill_version(), guard, argv=argv)
    cs.write_json(Path(out_prefix + ".run.json"), manifest)
    members = stats.get("members") or []
    cs.write_handoff(out_dir, str(stats.get("project") or ""), "mep", guard, members)
    return {"provenance": prov, "run_manifest": manifest, "members": len(members)}


def _skill_version() -> str:
    try:
        return str(json.loads((Path(__file__).resolve().parents[1] / "manifest.json")
                              .read_text(encoding="utf-8")).get("version") or "")
    except Exception:
        return ""


def main() -> None:
    raw = sys.argv[1:]
    lang = i18n.argv_lang(raw)
    # --check-deps 必须在 required 参数之前拦下，否则永远提示缺 --scan。
    if "--check-deps" in raw:
        status = cs.check_deps()
        print(cs.format_deps(status))
        raise SystemExit(eg.dependency_exit_code())
    desc = (__doc__ if lang == "zh" else
            "Generate installation material plan from scan JSON: circuit-to-spec matching, loss-to-order rounding.")
    ap = argparse.ArgumentParser(description=desc)
    i18n.add_lang_arg(ap, default=lang)
    ap.add_argument("--scan", nargs="+", required=True, help="mep_scan output JSON(s)" if lang == "en" else "mep_scan 输出的 JSON")
    ap.add_argument("--system", nargs="+", help="system-diagram scan JSON(s)" if lang == "en" else "系统图扫描 JSON（可多张）")
    ap.add_argument("--trunk-scan", nargs="+", help="trunk / busbar scan JSON(s)" if lang == "en" else "干线平面/母线层扫描 JSON（可多张）")
    ap.add_argument("--cad-measurement", default=None, help="cad-file-reader measurement candidates JSON (review evidence only)" if lang == "en" else "cad-file-reader 测量候选 JSON；只作复核证据")
    ap.add_argument("--mep-geometry", default=None, help="cad-file-reader MEP geometry candidates JSON (review evidence only)" if lang == "en" else "cad-file-reader MEP 几何候选 JSON；只作复核证据")
    ap.add_argument("--config", default=str(Path(__file__).parent.parent / "references/loss_rules.json"),
                    help="loss-rule JSON config" if lang == "en" else "损耗规则 JSON 配置")
    ap.add_argument("--out-prefix", required=True,
                    help="output file prefix" if lang == "en" else "输出文件前缀")
    ap.add_argument("--allow-manual", action="store_true",
                    help="allow scan JSON without reader provenance; result is forced final_quantity=false" if lang == "en"
                    else "允许消费无 reader 溯源的 scan JSON（手工/旧结果）；结果强制 final_quantity=false")
    ap.add_argument("--check-deps", action="store_true",
                    help="only check cad-file-reader / lis-skill-bus / Python" if lang == "en"
                    else "只检查 cad-file-reader / lis-skill-bus / Python 前置")
    ap.add_argument("--project", default="",
                    help="project id written into site_handoff.json" if lang == "en" else "写入 site_handoff.json 的项目标识")
    args = ap.parse_args(raw)
    # 入口闸门：缺 cad-file-reader / lis-skill-bus 先停；任何图纸输入一律拒收。
    try:
        eg.require_reader()
        eg.require_bus()
        eg.reject_drawing_input(args.scan, args.system, args.trunk_scan,
                                args.cad_measurement, args.mep_geometry)
    except eg.GateError as exc:
        raise SystemExit(eg.print_gate_error(exc)) from None
    scans = [load(p) for p in args.scan]
    sys_scans = [load(p) for p in args.system] if args.system else []
    trunk_scans = [load(p) for p in args.trunk_scan] if args.trunk_scan else []
    cfg = json.load(open(args.config, encoding="utf-8"))
    cad_measurement = load(args.cad_measurement) if args.cad_measurement else None
    mep_geometry = load(args.mep_geometry) if args.mep_geometry else None
    validation = {}
    if args.cad_measurement:
        validation = cad_validate_json(args.cad_measurement)
    docs = ([("--scan", d) for d in scans] + [("--system", d) for d in sys_scans]
            + [("--trunk-scan", d) for d in trunk_scans])
    try:
        guard = guard_plan_sources(docs, allow_manual=bool(args.allow_manual))
    except GuardError as exc:
        sys.stderr.write("[GuardError %d] %s\n" % (exc.code, exc.message))
        if exc.hint:
            sys.stderr.write("修复: %s\n" % exc.hint)
        raise SystemExit(exc.code) from None
    stats: dict = {"project": args.project,
                   "inputs": [{"label": label, "file": str(d.get("file") or ""),
                               "provenance": _doc_provenance(d)} for label, d in docs]}
    out = build(scans, sys_scans, cfg, args.out_prefix, trunk_scans, cad_measurement, mep_geometry, stats=stats)
    side = write_plan_sidecars(args.out_prefix, guard, stats, raw)
    if validation.get("ok") is False:
        print("cad-measurement validation failed:", json.dumps(validation["errors"], ensure_ascii=False))
    if guard.get("mode") != "formal":
        sys.stderr.write("[mep_plan] 手工来源（provenance=manual）：final_quantity=false，不得报正式量。\n")
    print(i18n.T(lang, "written") + ":", out)
    print(json.dumps({"provenance": side["provenance"].get("provenance"),
                      "contract_id": side["provenance"].get("contract_id") or "",
                      "final_quantity": False,
                      "formal_ledger_eligible": False,
                      "handoff_members": side["members"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
