#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""钢结构吨位估算：截面标注 × 米重公式 × 图面长度。

输入是 cad-file-reader `cad_steel_geometry` 的产物 `*.steel.json`
（schema cad-steel-geometry/v1）。识图层只给证据（截面标注、构件标注、
钢构件图层线段），重量在此按以下口径估算：

  米重   = 截面几何公式近似（ρ=7.85，面积 mm² × 0.00785 kg/m）
           不含圆角/公差，H 型约偏低 1~2%，冷弯 C/Z 型偏低 2~5%
           号数型槽钢/工字钢无几何公式，走 GB/T 706 理论重量查表
           （[5~[40、I10~I63，含 a/b/c 分档）
  长度   两档——
           ① 显式长度：文本里 L=12345 / 长度 12345（置信高，直接用）
           ② 图面线段：钢构件图层 geometry 段长合计（图面口径，不含
              节点板/加劲肋/下料余量，系统偏低，只作下限证据）
  不足   2 段式 H 型（H400x200）缺腹板/翼缘厚度，只计数不进吨位；
         GB/T 706 表外号数（如 [99）同样只计数。
         钢板无宽度时只计数。

输出为估算带（±15%），final_quantity=false，不替代深化设计、翻样或结算。

用法
  # 正式入口：只从 lis-skill-bus 按 contract_id 取契约
  python3 steel_tonnage.py --from-contract <contract_id> --project 项目 --out-prefix 钢结构吨位
  # 手工/文件降级：必须显式 --allow-manual，结果 final_quantity=false
  python3 steel_tonnage.py --steel 钢结构识图/xxx.steel.json --allow-manual --out-prefix 钢结构吨位

来源准入由 contract_guard.guard_contract 把关；缺 reader/bus 时先跑 --check-deps，
不得自行实现 DWG/DXF 解析或用其它解析器兜底。
"""
from __future__ import annotations

try:
    import os as _boot_os, sys as _boot_sys
    _boot_sys.path.insert(0, _boot_os.path.dirname(_boot_os.path.abspath(__file__)))
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass

import argparse
import csv
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from collections import defaultdict
from datetime import datetime
from io import StringIO
from pathlib import Path
from typing import Any

from contract_guard import GuardError, guard_contract, stamp_result
import contract_support as cs
import entry_gate as eg

SCHEMA = "cad-steel-tonnage/v0.2"
INPUT_SCHEMA = "cad-steel-geometry/v1"
CONTRACT_SCHEMA = "cad-contract/v1"
SKILL_NAME = "gangjiegou-suanliang"
SKILL_VERSION_FALLBACK = "0.4.0"
RHO = 0.00785  # mm² → kg/m
KNOWN_GRADES = (
    "Q235", "Q345", "Q355", "Q390", "Q420", "Q460",
    "S235", "S355", "A36", "16Mn",
)
GRADE_ORDER = {grade: i for i, grade in enumerate(KNOWN_GRADES)}
GRADE_RE = re.compile(
    r"^(?:Q235|Q345|Q355|Q390|Q420|Q460|S235|S355|A36|16Mn)", re.I)

# ---------------------------------------------------------------- 连接/涂装

CONNECTION_ORDER = (
    "high_strength_bolt", "bolt", "anchor_bolt", "stud",
    "plate_connection", "stiffener", "other",
)
CONNECTION_LABELS = {
    "high_strength_bolt": "高强螺栓",
    "bolt": "普通螺栓",
    "anchor_bolt": "锚栓",
    "stud": "栓钉",
    "plate_connection": "节点板",
    "stiffener": "加劲肋",
    "other": "其他连接",
}
CONNECTION_QUANTITY_PATTERNS = (
    re.compile(r"(?<!\d)(\d{1,5})\s*(?:套|个|颗|只|孔|处|排)(?!\d)"),
    re.compile(r"(?:数量|COUNT)\s*[=＝:]\s*(\d{1,5})", re.I),
    re.compile(r"(?:^|(?<![A-Z0-9]))N\s*[=＝]\s*(\d{1,5})", re.I),
    re.compile(r"(?<!\d)(\d{1,5})\s*[-×xX*]\s*M(?=\d)"),
)
ANCHOR_BOLT_RE = re.compile(r"(?:锚栓|地脚螺栓|化学锚栓|ANCHOR\s*BOLT)", re.I)
FINISH_ORDER = (
    "primer", "topcoat", "hot_dip_galvanized", "fireproof_coating",
)
FINISH_LABELS = {
    "primer": "底漆",
    "topcoat": "面漆",
    "hot_dip_galvanized": "热浸镀锌",
    "fireproof_coating": "防火涂料",
}
FINISH_AREA_RE = re.compile(
    r"(?:面积|涂装面积|展开面积|表面积)\s*[=＝:]?\s*"
    r"(\d+(?:\.\d+)?)\s*(m\^?2|m²|㎡|mm\^?2|mm²)", re.I)
PLATE_THICKNESS_RE = re.compile(
    r"(?:PL|板厚|厚度|T)\s*[=＝]?\s*(\d+(?:\.\d+)?)"
    r"(?:\s*(?:mm|毫米))?(?:\s*厚)?", re.I)
PLATE_AREA_M2_RE = re.compile(
    r"(\d+(?:\.\d+)?)\s*(?:m\^?2|m²|㎡)", re.I)
PLATE_AREA_MM2_RE = re.compile(
    r"(\d+(?:\.\d+)?)\s*(?:mm\^?2|mm²)", re.I)
PLATE_LENGTH_RE = re.compile(
    r"(?:L\s*[=＝:]|长度)\s*(\d+(?:\.\d+)?)", re.I)
PAIR_DIM_RE = re.compile(r"(\d+(?:\.\d+)?)\s*[xX×]\s*(\d+(?:\.\d+)?)")
TRIPLE_DIM_RE = re.compile(
    r"(\d+(?:\.\d+)?)\s*[xX×]\s*(\d+(?:\.\d+)?)\s*[xX×]\s*(\d+(?:\.\d+)?)")


# ---------------------------------------------------------------- 米重引擎

def _num(values: list[str]) -> list[float]:
    out = []
    for v in values:
        try:
            out.append(float(v))
        except (TypeError, ValueError):
            pass
    return out


def unit_weight_h(text: str, nums: list[float]) -> tuple[float, str]:
    """H 型钢：HN400x200x8x13 → h,b,t1,t2；H400x200 缺厚度 → 不进吨位。"""
    if len(nums) >= 4:
        h, b, t1, t2 = nums[0], nums[1], nums[2], nums[3]
        area = 2 * b * t2 + max(h - 2 * t2, 0) * t1  # 两翼缘 + 腹板
        return area * RHO, "公式（不含圆角，约偏低1~2%）"
    return 0.0, "2 段式 H 型缺腹板/翼缘厚度，仅计数"


def unit_weight_tube(text: str, nums: list[float]) -> tuple[float, str]:
    """圆管 Φ180x6 / D180x6；只有 Φd 一个数字时按实心圆钢。"""
    if len(nums) >= 2 and nums[0] > nums[1]:
        d, t = nums[0], nums[1]
        return (d - t) * 3.14159265 * t * RHO, "公式"
    if len(nums) == 1:
        d = nums[0]
        return 3.14159265 / 4 * d * d * RHO, "无壁厚按实心圆钢公式（若为管需给壁厚）"
    return 0.0, "圆管格式无法解析，仅计数"


def unit_weight_rect(text: str, nums: list[float]) -> tuple[float, str]:
    """方/矩管 □100x100x4 / 200x100x6。"""
    if len(nums) >= 3:
        a, b, t = nums[0], nums[1], nums[2]
        return (2 * (a + b) - 4 * t) * t * RHO, "公式（直角近似）"
    return 0.0, "方矩管缺壁厚，仅计数"


def unit_weight_angle(text: str, nums: list[float]) -> tuple[float, str]:
    """角钢 L100x8（等边）/ L100x63x8（不等边）。"""
    if len(nums) >= 3:
        a, b, t = nums[0], nums[1], nums[2]
        return (a + b - t) * t * RHO, "公式（不含内圆弧）"
    if len(nums) == 2:
        a, t = nums[0], nums[1]
        return (2 * a - t) * t * RHO, "等边公式（不含内圆弧）"
    return 0.0, "角钢格式无法解析，仅计数"


def unit_weight_purlin(text: str, nums: list[float]) -> tuple[float, str]:
    """C/Z 檩条 C200x70x20x2.5 → 展开宽 × 厚。"""
    if len(nums) >= 4:
        h, b = nums[0], nums[1]
        t = nums[3] if nums[3] < nums[2] else nums[2]
        return (h + 2 * b) * t * RHO, "展开宽公式（不含卷边，偏低2~5%）"
    if len(nums) == 3:
        h, b, t = nums[0], nums[1], nums[2]
        return (h + 2 * b) * t * RHO, "展开宽公式（无卷边尺寸）"
    return 0.0, "檩条截面无法解析，仅计数"


def unit_weight_plate(text: str, nums: list[float]) -> tuple[float, str]:
    """钢板 PL8x200（厚x宽，按每米长 kg）；只有厚度时仅计数。"""
    if len(nums) >= 2:
        t, w = nums[0], nums[1]
        return t * w * RHO, "厚×宽（每米长 kg；宽度为标称宽）"
    return 0.0, "钢板缺宽度，仅计数"


_WEIGHTERS = {
    "h_section": unit_weight_h,
    "tube": unit_weight_tube,
    "rect_tube": unit_weight_rect,
    "angle": unit_weight_angle,
    "purlin_section": unit_weight_purlin,
    "plate": unit_weight_plate,
}

_CHANNEL_NO_WEIGHT = {"槽钢", "[", "C"}  # 号数型槽钢无公式


# GB/T 706 热轧型钢理论重量（kg/m）查表值，只补「号数型、无几何公式」的截面。
# 号数 → a/b/c 分档；无字母时为该号唯一值。来源：GB/T 706 理论重量表（手册值，
# 与厂家实测可能有 <1% 差异，仍落在 ±15% 估算带内）。
GB706_CHANNEL = {          # 热轧槽钢 [5 ~ [40
    5: 5.438, 6.3: 6.634, 8: 8.045, 10: 10.007, 12: 12.059, 12.6: 12.318,
    14: {"a": 14.535, "b": 16.733},
    16: {"a": 17.240, "b": 19.752},
    18: {"a": 20.174, "b": 23.000},
    20: {"a": 22.637, "b": 25.777},
    22: {"a": 24.999, "b": 28.453},
    25: {"a": 27.410, "b": 31.335, "c": 35.260},
    28: {"a": 31.427, "b": 35.823, "c": 40.219},
    30: {"a": 34.463, "b": 39.173, "c": 43.883},
    32: {"a": 38.083, "b": 43.107, "c": 48.131},
    36: {"a": 47.814, "b": 53.466, "c": 59.118},
    40: {"a": 58.928, "b": 65.208, "c": 71.488},
}
GB706_I_BEAM = {           # 热轧工字钢 I10 ~ I63
    10: 11.261, 12: 13.987, 12.6: 14.223, 14: 16.890, 16: 20.513, 18: 24.143,
    20: {"a": 27.929, "b": 31.069},
    22: {"a": 33.070, "b": 36.524},
    25: {"a": 38.105, "b": 42.030},
    28: {"a": 43.492, "b": 47.888},
    30: {"a": 48.084, "b": 52.794, "c": 57.504},
    32: {"a": 52.717, "b": 57.741, "c": 62.765},
    36: {"a": 60.037, "b": 65.689, "c": 71.341},
    40: {"a": 67.598, "b": 73.878, "c": 80.158},
    45: {"a": 80.420, "b": 87.485, "c": 94.550},
    50: {"a": 93.654, "b": 101.504, "c": 109.354},
    56: {"a": 106.316, "b": 115.108, "c": 123.900},
    63: {"a": 121.407, "b": 131.298, "c": 141.189},
}

_TABLE_SIZE_RE = re.compile(
    r"^(?:槽钢|工字钢|工|\[|C|I)?\s*(\d{1,3}(?:\.\d)?)\s*([abcABC]?)$")


def gb706_lookup(table: dict, norm: str) -> tuple[float, str]:
    """号数型截面查表：[16a / 槽钢16 / 工20b → GB/T 706 理论重量 kg/m。"""
    hit = _TABLE_SIZE_RE.match(norm)
    if not hit:
        return 0.0, "号数格式无法解析，仅计数"
    try:
        size = float(hit.group(1))
    except ValueError:
        return 0.0, "号数格式无法解析，仅计数"
    val = table.get(size)
    if isinstance(val, dict):
        letter = hit.group(2).lower() or "a"
        if letter not in val:
            return 0.0, f"GB/T 706 无 {size}{letter} 分档，仅计数"
        return val[letter], f"GB/T 706 查表（{size}{letter}）"
    if isinstance(val, (int, float)):
        if hit.group(2):
            return 0.0, f"GB/T 706 中 {size} 号无 {hit.group(2)} 分档，仅计数"
        return float(val), f"GB/T 706 查表（{size} 号）"
    return 0.0, "GB/T 706 无此规格，仅计数"


def _channel_formula(nums: list[float]) -> tuple[float, str]:
    """槽钢给足尺寸（[200x75x9 → h,b,t）时走近似几何公式。"""
    if len(nums) >= 3:
        h, b, t = nums[0], nums[1], nums[2]
        if h > b and h > t:
            return (2 * b * t + max(h - 2 * t, 0) * t) * RHO, "槽钢近似几何公式（不含圆弧）"
    return 0.0, ""


def parse_section(row: dict) -> dict:
    """section 候选 → 解析结果：米重（0=不进吨位）+ 备注。"""
    text = str(row.get("text") or "").strip()
    stype = str(row.get("section_type") or "")
    norm = text.replace("×", "x").replace("X", "x").replace(" ", "")
    nums = _num(re.findall(r"\d+(?:\.\d+)?", norm))
    # 槽钢：给足尺寸走几何公式；只给号数（[16a / 槽钢16）走 GB/T 706 查表
    if stype == "channel" or (stype != "purlin_section" and re.match(r"^(\[|槽钢)\d", norm)):
        kg_m, note = _channel_formula(nums)
        if not kg_m:
            kg_m, note = gb706_lookup(GB706_CHANNEL, norm)
        return {"text": text, "section_type": stype or "channel",
                "kg_m": round(kg_m, 2), "note": note or "仅计数"}
    # 工字钢号数型（工20a / 工字钢20b / I20a）
    if not _WEIGHTERS.get(stype) and re.match(
            r"^(?:工字钢|工|I)\s*\d{1,3}(?:\.\d)?[abcABC]?$", norm):
        kg_m, note = gb706_lookup(GB706_I_BEAM, norm)
        return {"text": text, "section_type": "i_section",
                "kg_m": round(kg_m, 2), "note": note}
    fn = _WEIGHTERS.get(stype)
    if fn is None:
        if re.match(r"^[A-Za-z]?\d+$", norm):  # 裸数字，无截面类型
            return {"text": text, "section_type": stype, "kg_m": 0.0,
                    "note": "截面类型不明，仅计数"}
        return {"text": text, "section_type": stype, "kg_m": 0.0,
                "note": "截面类型未映射，仅计数"}
    kg_m, note = fn(norm, nums)
    return {"text": text, "section_type": stype, "kg_m": round(kg_m, 2),
            "note": note if kg_m else note}


# ---------------------------------------------------------------- 长度证据

LEN_RE = re.compile(r"(?:L\s*[=＝:]|长度)\s*(\d{3,6})", re.I)


def explicit_lengths(members: list[dict]) -> dict[str, float]:
    """构件标注文本里的显式长度（L=6000 / 长度6000，mm→m）。

    同一编号出现多条显式长度证据时按候选条目合计，避免重复编号被静默丢弃；
    是否为同一构件的重复标注仍由调用方按 duplicate_member_codes 复核。
    """
    out: dict[str, float] = defaultdict(float)
    for m in members:
        for ev in m.get("evidence") or []:
            text = str(ev.get("text") or "")
            hit = LEN_RE.search(text)
            if hit:
                mm = float(hit.group(1))
                if 200 <= mm <= 60000:
                    code = str(m.get("code") or m.get("name") or "?")
                    out[code] += mm / 1000.0
    return out


def duplicate_member_codes(members: list[dict]) -> list[dict]:
    """返回有编号/名称重复的构件候选，供人工确认是否为重复标注。"""
    counts: dict[str, int] = defaultdict(int)
    for m in members:
        code = str(m.get("code") or m.get("name") or "").strip()
        if code:
            counts[code] += 1
    return [{"code": code, "count": count}
            for code, count in sorted(counts.items()) if count > 1]


def normalize_grade(raw) -> str:
    """识别层牌号 → 输出分档；只接受契约中列出的钢号前缀。"""
    hit = GRADE_RE.match(str(raw or "").strip())
    if not hit:
        return ""
    return hit.group(0).upper()


def _compact_text(value) -> str:
    return (str(value or "").replace("×", "x").replace("X", "x")
            .replace(" ", "").replace("　", "").lower())


def _evidence_text(row: dict) -> str:
    parts = []
    for ev in row.get("evidence") or []:
        if isinstance(ev, dict):
            parts.append(str(ev.get("text") or ""))
        else:
            parts.append(str(ev))
    return " ".join(parts)


def _candidate_text(row: dict) -> str:
    raw = str(row.get("raw") or "")
    text = str(row.get("text") or "")
    return " ".join(x for x in (raw, text, _evidence_text(row)) if x)


def connection_category(row: dict) -> str:
    """把识图连接类别归到本技能的六类计数口径。"""
    category = str(row.get("category") or "").strip()
    text = _candidate_text(row)
    if category == "high_strength_bolt":
        return "high_strength_bolt"
    if category == "stud":
        return "stud"
    if category == "plate_connection":
        return "plate_connection"
    if category == "stiffener":
        return "stiffener"
    if category == "bolt":
        return "anchor_bolt" if ANCHOR_BOLT_RE.search(text) else "bolt"
    # 兼容旧产物或自定义契约：仍只按原文证据分类，不做图上推断。
    if ANCHOR_BOLT_RE.search(text):
        return "anchor_bolt"
    if re.search(r"高强螺栓|高强度螺栓|10\.9S|8\.8S|HSFG", text, re.I):
        return "high_strength_bolt"
    if "栓钉" in text or "剪力钉" in text:
        return "stud"
    if re.search(r"节点板|连接板|拼接板|端板|法兰", text):
        return "plate_connection"
    if re.search(r"加劲肋|加劲板|腹板加劲", text):
        return "stiffener"
    if "螺栓" in text:
        return "bolt"
    return "other"


def connection_quantity(row: dict) -> int | None:
    """只提取图面显式数量；无证据时返回 None，不由坐标或标注次数推数量。"""
    text = _candidate_text(row)
    for regex in CONNECTION_QUANTITY_PATTERNS:
        hit = regex.search(text)
        if hit:
            try:
                value = int(float(hit.group(1)))
            except (TypeError, ValueError):
                continue
            if value > 0:
                return value
    return None


def connection_ledger(connections: list[dict]) -> tuple[list[dict], list[dict], list[dict]]:
    """连接候选 → 分类清单与复核清单；count 只表达证据口径，不做硬凑。"""
    grouped: dict[str, list[dict]] = defaultdict(list)
    rows: list[dict] = []
    for idx, raw_row in enumerate(connections):
        if not isinstance(raw_row, dict):
            continue
        category = connection_category(raw_row)
        evidence_quantity = connection_quantity(raw_row)
        row = {
            "category": category,
            "label": CONNECTION_LABELS[category],
            "raw": str(raw_row.get("raw") or raw_row.get("text") or ""),
            "file": raw_row.get("file"),
            "sheet": raw_row.get("sheet"),
            "x": raw_row.get("x"),
            "y": raw_row.get("y"),
            "label_count": 1,
            "evidence_quantity": evidence_quantity,
            "count": evidence_quantity if evidence_quantity is not None else 1,
            "count_basis": "显式数量证据" if evidence_quantity is not None else "标注次数",
            "quantity_status": ("evidence" if evidence_quantity is not None
                                else "needs_review"),
            "status": str(raw_row.get("status") or "candidate"),
            "review_reason": str(raw_row.get("review_reason") or ""),
            "evidence_text": _candidate_text(raw_row),
        }
        grouped[category].append(row)
        rows.append(row)

    summary: list[dict] = []
    review: list[dict] = []
    for category in CONNECTION_ORDER:
        items = grouped.get(category)
        if not items:
            continue
        quantities = [x["evidence_quantity"] for x in items]
        if all(q is not None for q in quantities):
            count = sum(int(q) for q in quantities)
            count_basis = "显式数量证据合计"
            quantity_status = "evidence"
            reason = ""
        elif any(q is not None for q in quantities):
            count = None
            count_basis = "混合证据（显式数量 + 仅标注），总量待复核"
            quantity_status = "needs_review"
            reason = "部分连接只有标注次数，未做数量外推"
        else:
            count = len(items)
            count_basis = "标注次数"
            quantity_status = "needs_review"
            reason = "无显式数量证据，仅记录标注次数"
        summary.append({
            "category": category,
            "label": CONNECTION_LABELS[category],
            "label_count": len(items),
            "evidence_quantity": (sum(int(q) for q in quantities)
                                  if all(q is not None for q in quantities) else None),
            "count": count,
            "count_basis": count_basis,
            "quantity_status": quantity_status,
        })
        for item in items:
            reasons = [reason] if reason else []
            if item["review_reason"]:
                reasons.append(item["review_reason"])
            if reasons:
                review.append({
                    "type": "connection_count",
                    "code": item["raw"] or CONNECTION_LABELS[category],
                    "reasons": reasons,
                    "evidence": [item["evidence_text"]] if item["evidence_text"] else [],
                })
    return summary, review, rows


def _first_match(text: str, regexes: list[re.Pattern[str]]) -> float | None:
    hits = []
    for regex in regexes:
        hit = regex.search(text)
        if hit:
            try:
                hits.append((hit.start(), float(hit.group(1))))
            except (TypeError, ValueError):
                continue
    return min(hits)[1] if hits else None


def plate_tonnage_rows(connections: list[dict]) -> tuple[list[dict], list[float]]:
    """仅当节点板有厚×宽×长或板厚×面积证据时进入吨位。"""
    rows: list[dict] = []
    total = [0.0, 0.0]
    for idx, row in enumerate(connections):
        if not isinstance(row, dict) or connection_category(row) != "plate_connection":
            continue
        text = _candidate_text(row)
        thickness = None
        structured = row.get("plate") if isinstance(row.get("plate"), dict) else {}
        if structured:
            thickness = _f(structured.get("thickness_mm") or structured.get("thickness"))
            thickness = thickness or None
        else:
            thickness = _first_match(text, [PLATE_THICKNESS_RE])

        width = length = None
        area_m2 = area_mm2 = None
        if structured:
            width = _f(structured.get("width_mm") or structured.get("width")) or None
            length = _f(structured.get("length_mm") or structured.get("length")) or None
            area_m2 = _f(structured.get("area_m2") or structured.get("area")) or None
            area_mm2 = _f(structured.get("area_mm2")) or None
        else:
            triple = TRIPLE_DIM_RE.search(text)
            if triple:
                a, b, c = (float(triple.group(i)) for i in (1, 2, 3))
                if thickness is None:
                    # 节点板常见两种写法：PL20x400x600（先厚）或 300x400x20（末位厚）。
                    if re.search(r"PL|板厚|厚度", text, re.I):
                        width, length = b, c
                    else:
                        width, length, thickness = a, b, c
                else:
                    width, length = b, c
            elif thickness is not None:
                pair = PAIR_DIM_RE.search(text)
                if pair:
                    width, length = float(pair.group(1)), float(pair.group(2))
                length_hit = PLATE_LENGTH_RE.search(text)
                if length_hit and not pair:
                    length = float(length_hit.group(1))
            area_m2 = _first_match(text, [PLATE_AREA_M2_RE])
            area_mm2 = _first_match(text, [PLATE_AREA_MM2_RE])

        has_area = area_m2 is not None or area_mm2 is not None
        has_rect = None not in (thickness, width, length)
        if not has_rect and not has_area:
            continue
        evidence: dict[str, Any] = {
            "thickness_mm": thickness, "width_mm": width, "length_mm": length,
            "area_m2": area_m2, "area_mm2": area_mm2,
        }
        if has_rect:
            volume_mm3 = thickness * width * length
        else:
            volume_mm3 = ((area_m2 or 0.0) * 1_000_000 + (area_mm2 or 0.0)) * (thickness or 0.0)
        if volume_mm3 <= 0:
            continue
        kg = volume_mm3 * 7.85e-6
        band = [round(kg * 0.85 / 1000.0, 6), round(kg * 1.15 / 1000.0, 6)]
        rows.append({
            "category": "plate_connection",
            "raw": str(row.get("raw") or row.get("text") or ""),
            "evidence": evidence,
            "basis": "厚×宽×长" if has_rect else "板厚×面积",
            "kg": round(kg, 3),
            "tonnage_t": band,
            "file": row.get("file"),
            "sheet": row.get("sheet"),
        })
        total[0] += band[0]
        total[1] += band[1]
    return rows, [round(total[0], 6), round(total[1], 6)]


def finish_area_m2(row: dict) -> float | None:
    """只接受显式涂装/展开面积证据；结构化字段优先。"""
    if isinstance(row.get("area_m2"), (int, float)) and float(row["area_m2"]) > 0:
        return float(row["area_m2"])
    hit = FINISH_AREA_RE.search(_candidate_text(row))
    if not hit:
        return None
    value, unit = float(hit.group(1)), hit.group(2).lower()
    if unit.startswith("mm"):
        return value / 1_000_000.0
    return value


def finish_ledger(finishes: list[dict]) -> tuple[list[dict], list[dict], list[dict]]:
    """涂装候选 → 分类面积带；无面积/范围证据时如实 unavailable。"""
    grouped: dict[str, list[dict]] = defaultdict(list)
    rows: list[dict] = []
    for idx, raw_row in enumerate(finishes):
        if not isinstance(raw_row, dict):
            continue
        category = str(raw_row.get("category") or "").strip()
        if category not in FINISH_LABELS:
            text = _candidate_text(raw_row)
            for key, label in FINISH_LABELS.items():
                if key in text or label in text:
                    category = key
                    break
        if category not in FINISH_LABELS:
            continue
        area = finish_area_m2(raw_row)
        row = {
            "category": category,
            "label": FINISH_LABELS[category],
            "raw": str(raw_row.get("raw") or raw_row.get("text") or ""),
            "file": raw_row.get("file"),
            "sheet": raw_row.get("sheet"),
            "x": raw_row.get("x"),
            "y": raw_row.get("y"),
            "area_m2": area,
            "area_m2_band": ([round(area * 0.85, 2), round(area * 1.15, 2)]
                              if area is not None else None),
            "area_status": "estimated" if area is not None else "unavailable",
            "basis": "显式面积证据 ±15%" if area is not None
                     else "缺显式面积或可计算范围，unavailable",
            "fire_rating": None,
            "evidence_text": _candidate_text(raw_row),
            "status": str(raw_row.get("status") or "candidate"),
            "review_reason": str(raw_row.get("review_reason") or ""),
        }
        grouped[category].append(row)
        rows.append(row)

    summary: list[dict] = []
    review: list[dict] = []
    for category in FINISH_ORDER:
        items = grouped.get(category)
        if not items:
            summary.append({
                "category": category, "label": FINISH_LABELS[category],
                "candidate_count": 0, "area_status": "unavailable",
                "area_m2_band": None, "basis": "无涂装候选，unavailable",
                "fire_rating": None,
            })
            continue
        areas = [x["area_m2"] for x in items if x["area_m2"] is not None]
        missing = len(items) - len(areas)
        if len(areas) == len(items):
            status = "estimated"
            basis = "显式面积证据合计 ±15%"
            band = [round(sum(a * 0.85 for a in areas), 2),
                    round(sum(a * 1.15 for a in areas), 2)]
        elif areas:
            status = "unavailable"
            basis = "部分候选缺面积证据，不混合硬算"
            band = None
        else:
            status = "unavailable"
            basis = f"{FINISH_LABELS[category]}面积或范围证据缺失，unavailable"
            band = None
        fire_rating = None
        if category == "fireproof_coating":
            # 防火等级不由“耐火极限”候选默认推断，保持空值供人工确认。
            fire_rating = None
        summary.append({
            "category": category, "label": FINISH_LABELS[category],
            "candidate_count": len(items), "area_status": status,
            "area_m2_band": band, "basis": basis,
            "fire_rating": fire_rating,
        })
        if status != "estimated":
            review.append({
                "type": "finish_area", "code": FINISH_LABELS[category],
                "reasons": [basis],
                "evidence": [x["evidence_text"] for x in items if x["evidence_text"]][:10],
            })
    return summary, review, rows


def _same_context(a: dict, b: dict) -> bool:
    af, bf = a.get("file"), b.get("file")
    asheet, bsheet = a.get("sheet"), b.get("sheet")
    if af and bf and af != bf:
        return False
    if asheet and bsheet and asheet != bsheet:
        return False
    try:
        ax, ay = float(a.get("x")), float(a.get("y"))
        bx, by = float(b.get("x")), float(b.get("y"))
    except (TypeError, ValueError):
        return bool(af and bf and af == bf and asheet == bsheet)
    return ((ax - bx) ** 2 + (ay - by) ** 2) ** 0.5 <= 1500.0


def member_merge(members: list[dict], parsed_sections: list[dict],
                 sections: list[dict], materials: list[dict]) -> tuple[list[dict], list[dict]]:
    """按编号归并构件；只保留识图层给出的类别、系统、截面和牌号证据。

    相邻阈值 1500 图面单位用于截面表/材料表和编号标注的空间关联；
    有坐标冲突或证据不明时不做牌号默认，而进入 unknown_grade/复核。
    """
    section_items = []
    for row, parsed in zip(sections, parsed_sections):
        text = str(parsed.get("text") or "").strip()
        if text:
            section_items.append({"row": row, "parsed": parsed,
                                  "text": text, "norm": _compact_text(text)})

    material_items = []
    for row in materials:
        grade = normalize_grade(row.get("grade") or row.get("raw") or row.get("text"))
        if grade:
            material_items.append({"row": row, "grade": grade,
                                   "text": _compact_text(_evidence_text(row))})

    grouped: dict[str, dict] = {}
    unnumbered = 0
    for idx, m in enumerate(members):
        code = str(m.get("code") or "").strip()
        name = str(m.get("name") or "").strip()
        if not code and name:
            code = name
        if not code:
            unnumbered += 1
            code = f"<unnumbered-{unnumbered}>"
        rec = grouped.setdefault(code, {
            "code": code, "members": [], "grades": set(), "grade_evidence": set(),
            "section_texts": set(), "sections": {}, "length_evidence": [],
            "explicit_length_m": 0.0, "categories": set(), "systems": set(),
            "source_status": set(), "source_review_reasons": set(),
            "unnumbered": False,
            "x": None, "y": None, "z": None, "rotation": None,
        })
        rec["members"].append(m)
        for coord in ("x", "y", "z", "rotation"):
            if rec[coord] is None and m.get(coord) is not None:
                rec[coord] = m.get(coord)
        if code.startswith("<unnumbered-"):
            rec["unnumbered"] = True
        if m.get("category"):
            rec["categories"].add(str(m["category"]))
        if m.get("system"):
            rec["systems"].add(str(m["system"]))
        if m.get("status"):
            rec["source_status"].add(str(m["status"]))
        if m.get("review_reason"):
            rec["source_review_reasons"].add(str(m["review_reason"]))

        member_ev = _evidence_text(m)
        member_norm = _compact_text(member_ev)
        for item in section_items:
            sec_row = item["row"]
            matched = bool(item["norm"]) and item["norm"] in member_norm
            if not matched and _same_context(m, sec_row):
                matched = True
            if matched:
                rec["section_texts"].add(item["text"])
                key = (item["parsed"].get("section_type"), item["text"])
                rec["sections"][key] = item["parsed"]

        direct_grade = normalize_grade(m.get("grade") or m.get("material"))
        if direct_grade:
            rec["grades"].add(direct_grade)
            rec["grade_evidence"].add(f"member[{idx}]")
        for j, item in enumerate(material_items):
            mat_row = item["row"]
            matched = bool(code and not code.startswith("<unnumbered-")
                           and _compact_text(code) in item["text"])
            if not matched and _compact_text(member_ev) == item["text"]:
                matched = True
            if not matched and _same_context(m, mat_row):
                matched = True
            if matched:
                rec["grades"].add(item["grade"])
                rec["grade_evidence"].add(f"material[{j}]")

        for ev in m.get("evidence") or []:
            text = str(ev.get("text") if isinstance(ev, dict) else ev or "")
            hit = LEN_RE.search(text)
            if hit:
                mm = float(hit.group(1))
                if 200 <= mm <= 60000:
                    rec["explicit_length_m"] += mm / 1000.0
                    rec["length_evidence"].append(text)

    rows: list[dict] = []
    review: list[dict] = []
    for code, rec in grouped.items():
        sections_out = [
            {"section_type": key[0], "text": key[1], "kg_m": val.get("kg_m", 0.0),
             "note": val.get("note", "")}
            for key, val in sorted(rec["sections"].items(), key=lambda kv: (kv[0][1], kv[0][0]))
        ]
        usable = [s for s in sections_out if s["kg_m"] > 0]
        length_m = round(rec["explicit_length_m"], 3)
        tonnage: list[float] = []
        tonnage_basis = ""
        if length_m > 0 and usable:
            lo_kg = min(s["kg_m"] for s in usable)
            hi_kg = sum(s["kg_m"] for s in usable)
            tonnage = [round(lo_kg * length_m * 0.85 / 1000.0, 4),
                       round(hi_kg * length_m * 1.15 / 1000.0, 4)]
            tonnage_basis = ("explicit_length + 单截面" if len(usable) == 1
                             else "explicit_length + 多截面证据带（下限最轻截面、上限截面合计）")

        grades = sorted(rec["grades"], key=lambda g: (GRADE_ORDER.get(g, 999), g))
        if len(grades) > 1:
            grade = "mixed_grade"
        elif grades:
            grade = grades[0]
        else:
            grade = "unknown_grade"

        conflicts: list[str] = []
        reasons: list[str] = []
        categories = sorted(rec["categories"])
        systems = sorted(rec["systems"])
        if len(categories) > 1:
            conflicts.append("同编号构件类别冲突")
        if len(systems) > 1:
            conflicts.append("同编号跨系统冲突")
        if rec["unnumbered"]:
            reasons.append("构件编号缺失，无法归并")
        reasons.extend(sorted(rec["source_review_reasons"]))
        if not sections_out:
            reasons.append("无截面映射")
        elif len(usable) > 1:
            reasons.append("多截面映射，需人工确认长度归属")
        if len(grades) > 1:
            reasons.append("多牌号证据冲突，不得默认归档")

        row = {
            "code": code,
            "instance_count": len(rec["members"]),
            "categories": categories,
            "systems": systems,
            "grade": grade,
            "grade_evidence": sorted(rec["grade_evidence"]),
            "section_texts": sorted(rec["section_texts"]),
            "sections": sections_out,
            "explicit_length_m": length_m,
            "length_evidence": rec["length_evidence"],
            "x": rec["x"], "y": rec["y"], "z": rec["z"],
            "rotation": rec["rotation"],
            "zone": next((str(x.get("zone")) for x in rec["members"] if x.get("zone")), ""),
            "floor": next((str(x.get("floor")) for x in rec["members"] if x.get("floor")), ""),
            "coord_unit": "mm",
            "location_status": ("provided" if rec["x"] is not None and rec["y"] is not None
                                else "missing"),
            "tonnage_t": tonnage,
            "tonnage_basis": tonnage_basis,
            "conflicts": conflicts,
            "review_reasons": reasons,
        }
        rows.append(row)

        if conflicts or reasons:
            review.append({
                "type": "member_merge", "code": code,
                "reasons": conflicts + reasons,
                "evidence": [
                    _evidence_text(m) for m in rec["members"] if _evidence_text(m)
                ][:10],
            })

    rows.sort(key=lambda r: (r["grade"] not in KNOWN_GRADES, GRADE_ORDER.get(r["grade"], 999), r["code"]))
    review.sort(key=lambda r: (r["code"]))
    return rows, review


def grade_tonnage_rows(merged: list[dict], total_t: list[float],
                       total_basis: str = "allocated_estimate",
                       plate_total: list[float] | None = None) -> list[dict]:
    """把构件级牌号证据汇成分档吨位；无直接证据时余量归 unknown_grade。"""
    buckets: dict[str, dict] = {}
    direct_by_grade: dict[str, list[list[float]]] = defaultdict(list)
    for row in merged:
        if row.get("tonnage_t") and row.get("grade") in KNOWN_GRADES:
            direct_by_grade[row["grade"]].append(row["tonnage_t"])
        elif row.get("tonnage_t") and row.get("grade") == "unknown_grade":
            direct_by_grade["unknown_grade"].append(row["tonnage_t"])

    for grade in (*KNOWN_GRADES, "unknown_grade"):
        bands = direct_by_grade.get(grade)
        lo = hi = 0.0
        basis = "无吨位证据"
        if bands:
            lo = sum(b[0] for b in bands)
            hi = sum(b[1] for b in bands)
            basis = "构件显式长度 + 截面映射"
        elif grade == "unknown_grade" and total_t:
            lo, hi = total_t
            basis = "总吨位余量，无构件级牌号证据"
        buckets[grade] = {"grade": grade, "tonnage_t": [round(lo, 4), round(hi, 4)],
                          "allocation": basis}

    # 余量只算一次：逐根口径直接对未分牌号构件求和；分摊口径才用总吨位相减。
    known_lo = sum(buckets[g]["tonnage_t"][0] for g in KNOWN_GRADES)
    known_hi = sum(buckets[g]["tonnage_t"][1] for g in KNOWN_GRADES)
    if total_basis == "member_level":
        unknown_rows = [r["tonnage_t"] for r in merged
                        if r.get("tonnage_t") and r.get("grade") not in KNOWN_GRADES]
        plate = plate_total or [0.0, 0.0]
        lo = sum(float(b[0]) for b in unknown_rows) + float(plate[0])
        hi = sum(float(b[1]) for b in unknown_rows) + float(plate[1])
        buckets["unknown_grade"]["tonnage_t"] = [round(lo, 2), round(hi, 2)]
        if unknown_rows and (plate[0] or plate[1]):
            basis_text = "逐根未分牌号构件求和 + 节点板无牌号证据"
        elif unknown_rows:
            basis_text = "逐根未分牌号构件求和"
        elif plate[0] or plate[1]:
            basis_text = "节点板无牌号证据"
        else:
            basis_text = "全部构件已有牌号证据"
        buckets["unknown_grade"]["allocation"] = basis_text
    elif total_t:
        lo = max(0.0, float(total_t[0]) - known_hi)
        hi = max(0.0, float(total_t[1]) - known_lo)
        buckets["unknown_grade"]["tonnage_t"] = [round(lo, 2), round(hi, 2)]
        buckets["unknown_grade"]["allocation"] = (
            "总吨位扣除已分牌号余量" if (known_lo or known_hi)
            else "总吨位全部未分牌号")

    out = [buckets[g] for g in KNOWN_GRADES if buckets[g]["tonnage_t"] != [0, 0]]
    unknown = buckets["unknown_grade"]
    if unknown["tonnage_t"] != [0, 0]:
        out.append(unknown)
    return out


def drawn_length(steel: dict) -> dict[str, float]:
    """钢构件图层 geometry 段长合计（图面口径，按图层分组，mm→m）。"""
    per_layer: dict[str, float] = defaultdict(float)
    for item in steel.get("steel_geometry") or []:
        if not isinstance(item, dict):
            continue
        layer = str(item.get("layer") or "?")
        geom = item.get("geometry")
        vals: list[float] = []
        if isinstance(geom, dict):
            vals = [_f(geom.get(k)) for k in ("length", "length_mm")]
        elif isinstance(geom, (list, tuple)) and len(geom) >= 4:
            x0, y0, x1, y1 = (_f(geom[0]), _f(geom[1]), _f(geom[2]), _f(geom[3]))
            vals = [((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5]
        for v in vals:
            if v > 0:
                per_layer[layer] += v / 1000.0
    return dict(per_layer)


def _f(v) -> float:
    try:
        x = float(v)
    except (TypeError, ValueError):
        return 0.0
    return x


def _validate_contract(data) -> dict:
    """校验 cad-steel-geometry/v1 输入契约。"""
    if not isinstance(data, dict):
        raise SystemExit("❌ 非契约输入：*.steel.json 顶层必须是 JSON object")
    if data.get("schema") != INPUT_SCHEMA:
        got = data.get("schema") or "<missing>"
        raise SystemExit(
            f"❌ 非契约输入：schema 必须是 {INPUT_SCHEMA}，当前为 {got}")
    required: dict[str, list] = {}
    for key in ("sections", "members", "steel_geometry"):
        value = data.get(key)
        if value is None:
            raise SystemExit(f"❌ 非契约输入：缺少 {key}[] 字段")
        if not isinstance(value, list):
            raise SystemExit(f"❌ 非契约输入：{key}[] 必须是数组")
        for i, item in enumerate(value):
            if not isinstance(item, dict):
                raise SystemExit(f"❌ 非契约输入：{key}[{i}] 必须是 object")
        required[key] = value
    materials = data.get("materials")
    if materials is not None and not isinstance(materials, list):
        raise SystemExit("❌ 非契约输入：materials[] 必须是数组")
    for i, item in enumerate(materials or []):
        if not isinstance(item, dict):
            raise SystemExit(f"❌ 非契约输入：materials[{i}] 必须是 object")
    for key in ("connections", "finishes"):
        value = data.get(key)
        if value is not None and not isinstance(value, list):
            raise SystemExit(f"❌ 非契约输入：{key}[] 必须是数组")
        for i, item in enumerate(value or []):
            if not isinstance(item, dict):
                raise SystemExit(f"❌ 非契约输入：{key}[{i}] 必须是 object")
    if not any(required.values()):
        raise SystemExit(
            "❌ 空输入：sections/members/steel_geometry 全部为空"
            "（确认输入是 cad_steel_geometry 的 *.steel.json）")
    return data


# ---------------------------------------------------------------- 前置/体检

def _first_existing_skill(*names: str) -> str | None:
    """在常见技能安装根目录找技能目录（兼容带 __skillhub 等后缀）。"""
    roots = [
        Path.home() / ".codex" / "skills",
        Path.home() / ".workbuddy" / "skills",
        Path.cwd() / "skills",
    ]
    for root in roots:
        for name in names:
            direct = root / name
            if direct.is_dir():
                return str(direct)
            if root.is_dir():
                for hit in sorted(root.glob(name + "*")):
                    if hit.is_dir():
                        return str(hit)
    return None



# ---------------------------------------------------------------- 来源闸门

def _skill_version() -> str:
    """从 manifest.json 读版本；读不到时用常量，避免结果里出现空版本。"""
    manifest = Path(__file__).resolve().parent.parent / "manifest.json"
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
        version = str(data.get("version") or "").strip()
        if version:
            return version
    except (OSError, json.JSONDecodeError):
        pass
    return SKILL_VERSION_FALLBACK


def _now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _doc_unit(doc) -> str:
    """兼容 guard 认的几种坐标单位位置，只用于判断是否需要补 mm。"""
    if not isinstance(doc, dict):
        return ""
    candidates = [
        doc.get("coordinate_unit"),
        (doc.get("units") or {}).get("coordinate") if isinstance(doc.get("units"), dict) else None,
        (doc.get("coordinate") or {}).get("unit") if isinstance(doc.get("coordinate"), dict) else None,
        ((doc.get("contract") or {}).get("coordinate_unit")
         if isinstance(doc.get("contract"), dict) else None),
        (doc.get("source") or {}).get("unit") if isinstance(doc.get("source"), dict) else None,
    ]
    for raw in candidates:
        if isinstance(raw, str) and raw.strip():
            return raw.strip()
    return ""


def _pick_reader_version(*docs) -> str:
    """从契约/载荷里找 cad-file-reader 的版本标识（如 cad-file-reader/v0）。"""
    paths = (
        ("reader_version",),
        ("spec",),
        ("producer", "reader_version"),
        ("producer", "schema"),
        ("_provenance", "reader_version"),
        ("_provenance", "schema"),
    )
    for doc in docs:
        if not isinstance(doc, dict):
            continue
        for path in paths:
            cur = doc
            for key in path:
                cur = cur.get(key) if isinstance(cur, dict) else None
            if isinstance(cur, str) and cur.strip().lower().startswith("cad-file-reader"):
                return cur.strip()
    return ""


def _bus_client_path() -> Path | None:
    """定位 lis-skill-bus 的 CLI；支持 SKILLBUS_HOME 和常见技能根。"""
    bus = os.environ.get("SKILLBUS_HOME") or _first_existing_skill("lis-skill-bus")
    if not bus:
        return None
    for cand in (Path(bus) / "skillbus_client.py",
                 Path(bus) / "scripts" / "skillbus_client.py"):
        if cand.is_file():
            return cand
    return None


def _bus_pull(project: str, contract_id: str) -> tuple[dict | None, str]:
    """按 contract_id 从 bus 取 entry；返回 (entry, error)。"""
    client = _bus_client_path()
    if client is None:
        return None, (
            "找不到 lis-skill-bus/skillbus_client.py。安装："
            "bash ${CODEX_HOME:-$HOME/.codex}/skills/lis-skill-bus/install_skillbus.sh --apply"
        )
    cmd = [sys.executable, str(client), "pull", "--project", project,
           "--entry-id", contract_id]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return None, "bus pull 执行失败：%s" % exc
    if proc.returncode != 0:
        return None, "bus pull 失败 rc=%d：%s" % (
            proc.returncode, (proc.stderr or "").strip()[-300:])
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return None, "bus pull 输出不是 JSON：%s" % (proc.stdout or "")[:200]
    entry = data.get("entry")
    if not data.get("hit") or not isinstance(entry, dict):
        return None, str(data.get("reason") or "bus 中未找到契约 %s" % contract_id)
    return entry, ""


def _normalize_bus_entry(entry: dict, requested_id: str) -> tuple[dict, dict, list[str]]:
    """把 bus entry 归一成 (guard 用的 cad-contract/v1 文档, 实际算量载荷, 警告)。"""
    warnings: list[str] = []
    schema = str(entry.get("schema") or "").strip()
    payload = entry.get("contract") if schema == CONTRACT_SCHEMA else entry
    if not isinstance(payload, dict):
        payload = entry

    provenance = str(entry.get("provenance") or "").strip()
    if not provenance:
        meta = entry.get("_provenance") if isinstance(entry.get("_provenance"), dict) else {}
        producer = entry.get("producer") if isinstance(entry.get("producer"), dict) else {}
        provenance = str(
            meta.get("source_skill") or meta.get("source") or meta.get("mode")
            or producer.get("skill") or "").strip()
    contract_id = str(
        entry.get("contract_id") or entry.get("_id") or requested_id or "").strip()

    if schema == CONTRACT_SCHEMA:
        guard_doc = dict(entry)
        if not guard_doc.get("contract_id"):
            guard_doc["contract_id"] = contract_id
        if not guard_doc.get("provenance") and provenance:
            guard_doc["provenance"] = provenance
        if not _doc_unit(guard_doc) and not _doc_unit(payload):
            guard_doc["coordinate_unit"] = "mm"
            warnings.append("bus 契约未声明坐标单位，按本技能既有 mm 口径处理；算量前请核对。")
        if not isinstance(guard_doc.get("source"), dict) and isinstance(payload.get("source"), dict):
            guard_doc["source"] = payload.get("source")
        return guard_doc, payload, warnings

    if schema == INPUT_SCHEMA:
        # bus 里直接放了未包 envelope 的载荷：合成最小 cad-contract/v1 外壳再验。
        guard_doc = {
            "schema": CONTRACT_SCHEMA,
            "provenance": provenance or "manual",
            "contract_id": contract_id,
            "coordinate_unit": _doc_unit(payload) or "mm",
            "contract": payload,
        }
        if isinstance(payload.get("source"), dict):
            guard_doc["source"] = payload.get("source")
        if not _doc_unit(payload):
            warnings.append("bus 契约未声明坐标单位，按本技能既有 mm 口径处理；算量前请核对。")
        return guard_doc, payload, warnings

    guard_doc = dict(entry)
    if not guard_doc.get("contract_id"):
        guard_doc["contract_id"] = contract_id
    return guard_doc, payload, warnings


def _guard_from_dict(doc: dict, *, allow_manual: bool,
                     label: str = "<契约>") -> dict:
    """把 dict 落临时文件后交给共享 guard；bus 文档无法保留原始字节，跳过内嵌哈希绊线。"""
    with tempfile.TemporaryDirectory(prefix="steel_contract_") as tmp:
        path = Path(tmp) / "contract.json"
        path.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
        try:
            return guard_contract(path, allow_manual=allow_manual, require_hash=False)
        except GuardError as exc:
            # 临时文件已删除，错误提示里的路径换回真实来源，避免给用户死路径。
            raise GuardError(
                exc.code,
                exc.message.replace(str(path), label),
                exc.hint.replace(str(path), label),
            ) from None


def _synthetic_guard_doc(payload: dict) -> dict:
    """给裸 cad-steel-geometry/v1 载荷套最小 cad-contract/v1 外壳；不改载荷本身。"""
    provenance = str(payload.get("provenance") or "").strip()
    contract_id = str(
        payload.get("contract_id") or payload.get("contractId") or "").strip()
    doc = {
        "schema": CONTRACT_SCHEMA,
        "provenance": provenance,
        "contract_id": contract_id,
        "coordinate_unit": _doc_unit(payload),
        "contract": payload,
    }
    if isinstance(payload.get("source"), dict):
        doc["source"] = payload.get("source")
    return doc


def _guard_file_manual(path: str) -> tuple[dict, dict]:
    """文件路径一律按 manual 降级；返回 (guard, 算量载荷)。

    * 裸 cad-steel-geometry/v1：套 cad-contract/v1 外壳后验来源/单位；
    * 已是 cad-contract/v0|v1：原样验版本，v0 会 exit 4。
    """
    data, load_err = _load_json(path)
    if load_err:
        raise GuardError(2, load_err, hint="先确认路径：ls -l %s" % path)
    if not isinstance(data, dict):
        raise GuardError(2, "契约顶层必须是 JSON 对象", hint="检查文件开头")
    schema = str(data.get("schema") or "").strip()
    if schema == INPUT_SCHEMA:
        guard = _guard_from_dict(_synthetic_guard_doc(data), allow_manual=True, label=path)
        payload = data
    else:
        guard = guard_contract(path, allow_manual=True)
        payload = data.get("contract") if (
            schema == CONTRACT_SCHEMA and isinstance(data.get("contract"), dict)) else data
    if guard.get("mode") == "formal":
        guard = dict(guard)
        guard["mode"] = "manual"
        guard["provenance"] = "manual"
        guard["formal_ledger_eligible"] = False
        guard["warnings"] = list(guard.get("warnings") or []) + [
            "来源是文件路径而不是 bus，已按 manual 降级；正式量请用 --from-contract。"
        ]
    return guard, payload


def _validated_payload(data) -> dict:
    """结构不合法 -> exit 2；空证据 -> exit 5（数据不足）。"""
    try:
        return _validate_contract(data)
    except SystemExit as exc:
        message = str(exc)
        code = 5 if "空输入" in message else 2
        print(message, file=sys.stderr)
        raise SystemExit(code) from None


def _run_manifest(guard: dict) -> dict:
    """统一 run_manifest（contract-only 入口）；只记版本/参数/时间/契约哈希，不记图纸内容。"""
    return cs.run_manifest(SKILL_NAME, _skill_version(), guard, argv=sys.argv[1:])


def _print_guard_error(exc: GuardError) -> None:
    print("[GuardError %d] %s" % (exc.code, exc.message), file=sys.stderr)
    if exc.hint:
        print("修复: %s" % exc.hint, file=sys.stderr)


def prerequisites_status() -> dict:
    """探测正式识图链路的前置依赖；统一走 contract_support，只读，不改环境。"""
    status = cs.check_deps()
    status["scope"] = ("仅正式识图链路（cad-file-reader -> lis-skill-bus -> 本技能）需要；"
                       "文件契约必须显式加 --allow-manual，结果按 manual 降级、不是正式量。")
    return status


def _install_command(st: dict) -> str:
    parts = []
    if not st["lis_skill_bus"]["found"]:
        parts.append("bash ${CODEX_HOME:-$HOME/.codex}/skills/lis-skill-bus/install_skillbus.sh --apply")
    if not st["cad_file_reader"]["found"]:
        parts.append("bash ${CODEX_HOME:-$HOME/.codex}/skills/cad-file-reader/scripts/setup.sh")
    return " && ".join(parts)


def format_prerequisites(st: dict) -> str:
    cad = "✅" if st["cad_file_reader"]["found"] else "❌"
    bus = "✅" if st["lis_skill_bus"]["found"] else "❌"
    lines = [
        "正式识图链路前置探测",
        f"- cad-file-reader：{cad} {st['cad_file_reader']['path'] or '未找到'}",
        f"- lis-skill-bus：{bus} {st['lis_skill_bus']['path'] or '未找到'}",
        f"- 正式链路可用：{'是' if st['ready_for_formal_pipeline'] else '否'}",
    ]
    if st.get("install_hint"):
        lines.append(f"- 处理：{st['install_hint']}")
        lines.append(f"- 安装命令（复制执行）：{_install_command(st)}")
        lines.append("- 包本身不存在时，先从 SkillHub 安装对应技能，再执行上面的命令。")
    return "\n".join(lines)


def _load_json(path: str) -> tuple[dict | None, str | None]:
    try:
        with Path(path).open(encoding="utf-8") as f:
            return json.load(f), None
    except FileNotFoundError:
        return None, f"输入文件不存在：{path}"
    except json.JSONDecodeError as exc:
        return None, f"非契约 JSON：{path} 解析失败（第 {exc.lineno} 行，第 {exc.colno} 列）"


def contract_health(data) -> dict:
    """契约体检：只诊断字段、截面匹配和仅计数项，不出吨位、不写文件。"""
    report: dict = {
        "schema": "cad-steel-contract-health/v1",
        "status": "ok",
        "errors": [],
        "warnings": [],
        "counts": {},
        "length": {},
        "sections": [],
        "members": {"total": 0, "matched": 0, "unmatched": [], "no_length": [],
                    "no_section": []},
        "dependencies": prerequisites_status(),
    }
    if not isinstance(data, dict):
        report["status"] = "error"
        report["errors"].append("顶层必须是 JSON object")
        return report
    if data.get("schema") != INPUT_SCHEMA:
        report["status"] = "error"
        report["errors"].append(
            f"schema 必须是 {INPUT_SCHEMA}，当前为 {data.get('schema') or '<missing>'}")
        return report

    for key in ("sections", "members", "steel_geometry"):
        value = data.get(key)
        if value is None:
            report["errors"].append(f"缺少 {key}[] 字段")
        elif not isinstance(value, list):
            report["errors"].append(f"{key}[] 必须是数组")
        else:
            for i, item in enumerate(value):
                if not isinstance(item, dict):
                    report["errors"].append(f"{key}[{i}] 必须是 object")
    for key in ("materials", "connections", "finishes"):
        value = data.get(key)
        if value is not None and not isinstance(value, list):
            report["errors"].append(f"{key}[] 必须是数组")
        elif isinstance(value, list):
            for i, item in enumerate(value):
                if not isinstance(item, dict):
                    report["errors"].append(f"{key}[{i}] 必须是 object")
    if report["errors"]:
        report["status"] = "error"
        return report

    sections = data.get("sections") or []
    members = data.get("members") or []
    geometry = data.get("steel_geometry") or []
    connections = data.get("connections") or []
    finishes = data.get("finishes") or []
    materials = data.get("materials") or []
    if not (sections or members or geometry):
        report["status"] = "error"
        report["errors"].append("sections/members/steel_geometry 全部为空，无法计算")
        return report

    parsed = [parse_section(r) for r in sections]
    for p in parsed:
        report["sections"].append({
            "text": p["text"], "section_type": p["section_type"],
            "kg_m": p["kg_m"],
            "status": "tonnage" if p["kg_m"] > 0 else "count_only",
            "note": p["note"],
        })
    only = [x for x in report["sections"] if x["status"] == "count_only"]
    if only:
        report["warnings"].append(
            f"{len(only)} 条截面只能计数、不进吨位："
            + "、".join(f"{x['text']}（{x['note']}）" for x in only[:10])
            + ("…" if len(only) > 10 else ""))

    merged, merge_review = member_merge(members, parsed, sections, materials)
    report["members"]["total"] = len(members)
    for r in merged:
        if r["sections"]:
            report["members"]["matched"] += r["instance_count"]
        else:
            report["members"]["no_section"].append(r["code"])
            report["members"]["unmatched"].append({
                "code": r["code"], "instances": r["instance_count"],
                "reason": "未匹配到任何截面标注",
            })
        if not r["explicit_length_m"]:
            report["members"]["no_length"].append(r["code"])
    if report["members"]["no_section"]:
        report["warnings"].append(
            f"{len(report['members']['no_section'])} 个构件编号未匹配到截面："
            + "、".join(report["members"]["no_section"][:10])
            + ("…" if len(report["members"]["no_section"]) > 10 else ""))
    if report["members"]["no_length"]:
        report["warnings"].append(
            f"{len(report['members']['no_length'])} 个构件编号无显式长度："
            + "、".join(report["members"]["no_length"][:10])
            + ("…" if len(report["members"]["no_length"]) > 10 else ""))

    expl = explicit_lengths(members)
    layer_len = {}
    for item in geometry:
        layer = str(item.get("layer") or "<no-layer>")
        geom = item.get("geometry")
        vals = []
        if isinstance(geom, dict):
            vals = [_f(geom.get(k)) for k in ("length", "length_mm")]
        elif isinstance(geom, (list, tuple)) and len(geom) >= 4:
            vals = [((_f(geom[2]) - _f(geom[0])) ** 2
                     + (_f(geom[3]) - _f(geom[1])) ** 2) ** 0.5]
        for v in vals:
            if v > 0:
                layer_len[layer] = layer_len.get(layer, 0.0) + v / 1000.0
    report["length"] = {
        "explicit_count": len(expl),
        "explicit_total_m": round(sum(expl.values()), 3),
        "drawn_total_m": round(sum(layer_len.values()), 3),
        "basis": ("explicit" if expl else ("drawn" if layer_len else "none")),
        "explicit_items": dict(sorted(expl.items(), key=lambda kv: -kv[1])[:20]),
    }
    if report["length"]["basis"] == "none":
        report["warnings"].append("无任何长度证据：只能出截面谱，不出吨位")

    report["counts"] = {
        "sections": len(sections), "sections_tonnage": len(parsed) - len(only),
        "sections_count_only": len(only), "members": len(members),
        "member_codes": len(merged), "steel_geometry": len(geometry),
        "materials": len(materials), "connections": len(connections),
        "finishes": len(finishes), "merge_review": len(merge_review),
    }
    if not connections:
        report["warnings"].append("connections[] 为空：不做连接计数（输入无证据，不是未实现）")
    if not finishes:
        report["warnings"].append("finishes[] 为空：不做涂装面积（输入无证据，不是未实现）")
    if not geometry:
        report["warnings"].append("steel_geometry[] 为空：图面线段长度口径不可用")

    report["status"] = "warn" if report["warnings"] else "ok"
    return report


def format_health(report: dict) -> str:
    label = {"ok": "✅ 契约可计算", "warn": "⚠️ 契约可计算，但有需复核项",
             "error": "❌ 契约不可计算"}[report["status"]]
    lines = [f"契约体检：{label}"]
    if report["errors"]:
        lines.append("错误：")
        lines.extend(f"- {x}" for x in report["errors"])
    counts = report.get("counts") or {}
    if counts:
        lines.append(
            "规模：截面 {sections}（可计米重 {sections_tonnage}、仅计数 {sections_count_only}）；"
            "构件 {members} 条 / 归并 {member_codes} 个编号；"
            "steel_geometry {steel_geometry} 段；materials {materials}；"
            "connections {connections}；finishes {finishes}".format(**counts))
        length = report.get("length") or {}
        if length:
            lines.append(
                f"长度：{length['basis']}（显式 {length['explicit_count']} 条 / "
                f"{length['explicit_total_m']} m；图面线段 {length['drawn_total_m']} m）")
    if report.get("warnings"):
        lines.append("需复核：")
        lines.extend(f"- {x}" for x in report["warnings"])
    deps = report.get("dependencies") or {}
    if deps:
        lines.append(
            "前置：cad-file-reader {c} / lis-skill-bus {b}（只影响正式识图链路）".format(
                c="✅" if deps.get("cad_file_reader", {}).get("found") else "❌",
                b="✅" if deps.get("lis_skill_bus", {}).get("found") else "❌"))
    return "\n".join(lines)


def validate_path(path: str) -> dict:
    data, err = _load_json(path)
    if err:
        return {
            "schema": "cad-steel-contract-health/v1", "status": "error",
            "errors": [err], "warnings": [], "counts": {}, "length": {},
            "sections": [], "members": {"total": 0, "matched": 0, "unmatched": [],
                                        "no_length": [], "no_section": []},
            "dependencies": prerequisites_status(),
        }
    return contract_health(data)


def member_level_total(merged: list[dict]) -> tuple[list[float], str]:
    """逐根台账求和的可用性判定；不完整时返回空带和原因。"""
    if not merged:
        return [], "无构件归并台账"
    missing_length = [r["code"] for r in merged if not r.get("explicit_length_m")]
    if missing_length:
        return [], f"{len(missing_length)} 个构件编号缺显式长度，逐根口径不完整"
    missing_tonnage = [r["code"] for r in merged if not r.get("tonnage_t")]
    if missing_tonnage:
        return [], f"{len(missing_tonnage)} 个构件编号缺截面映射或米重，逐根口径不完整"
    multi = [r["code"] for r in merged
             if len([s for s in r.get("sections", []) if s.get("kg_m", 0) > 0]) != 1]
    if multi:
        return [], f"{len(multi)} 个构件编号有多截面冲突，长度归属不确定"
    lo = sum(float(r["tonnage_t"][0]) for r in merged)
    hi = sum(float(r["tonnage_t"][1]) for r in merged)
    return [round(lo, 2), round(hi, 2)], "逐根构件台账求和（推荐口径）"


def length_scenario_rows(spec_rows: list[dict], lengths: list[float]) -> list[dict]:
    """按统一构件长度给吨位敏感性场景；场景值不是结果。"""
    rows = []
    for length in lengths or []:
        try:
            length_m = float(length)
        except (TypeError, ValueError):
            continue
        if length_m <= 0:
            continue
        lo = sum(r["kg_m"] * r["count"] * length_m * 0.85 / 1000.0
                 for r in spec_rows if r["kg_m"] > 0)
        hi = sum(r["kg_m"] * r["count"] * length_m * 1.15 / 1000.0
                 for r in spec_rows if r["kg_m"] > 0)
        rows.append({
            "length_m": round(length_m, 3),
            "total_t_band": [round(lo, 2), round(hi, 2)],
            "basis": "每个截面标注按同一构件长度 L 估算；场景值，不替代缺长度证据的结论",
        })
    return rows


def allowance_advice(total_band: list[float]) -> dict:
    """吊装/运输用建议附加系数；不并入 total_t。"""
    items = [
        {"item": "连接件/节点板/加劲肋", "rate": 0.03,
         "note": "本技能只在显式尺寸证据下计节点板；未计量部分可加 3%"},
        {"item": "涂装/防火层", "rate": 0.05,
         "note": "吊装/运输需要总重时叠加 5%"},
        {"item": "下料余量/焊材/包装", "rate": 0.08,
         "note": "综合附加 8%，不与前两项简单叠加"},
    ]
    ref = []
    if total_band:
        ref = [round(total_band[0] * 1.03, 2), round(total_band[1] * 1.08, 2)]
    return {
        "included_in_total": False,
        "items": items,
        "hoisting_reference_t": ref,
        "note": "建议系数，不是规范值；正式重量仍以深化翻样为准。",
    }


# ---------------------------------------------------------------- 汇总

def _handoff_members(merged: list[dict]) -> list[dict]:
    """把构件归并结果映射成 site-handoff/v1 成员。

    只输出已有证据：坐标(mm→m)缺失写 null，吨位缺失写 null/unknown；
    吨位带取上限（+15%）作为吊装保守重量，basis 明确标注估算口径。
    """
    members = []
    for row in merged:
        x, y, z = row.get("x"), row.get("y"), row.get("z")
        x_m = round(float(x) / 1000.0, 4) if x is not None else None
        y_m = round(float(y) / 1000.0, 4) if y is not None else None
        z_m = round(float(z) / 1000.0, 4) if z is not None else None
        band = row.get("tonnage_t") or []
        weight_t = round(float(band[1]), 4) if len(band) >= 2 else None
        weight_basis = "estimate_band_upper" if weight_t is not None else "unknown"
        sections = row.get("sections") or []
        section = str(sections[0].get("text") or "") if sections else ""
        grade = row.get("grade") or ""
        if grade in ("unknown_grade", "mixed_grade"):
            grade = ""
        length_m = row.get("explicit_length_m") or None
        members.append(cs.handoff_member(
            row.get("code") or "",
            weight_t=weight_t, length_m=length_m, section=section, grade=grade,
            x_m=x_m, y_m=y_m, z_m=z_m,
            zone=str(row.get("zone") or ""), floor=str(row.get("floor") or ""),
            weight_basis=weight_basis,
            coord_status=("provided" if x_m is not None and y_m is not None else "missing"),
            kind="、".join(row.get("categories") or []),
            instance_count=row.get("instance_count"),
        ))
    return members


def build(steel_path: str, out_prefix: str,
          length_scenarios: list[float] | None = None,
          payload: dict | None = None,
          guard: dict | None = None,
          run_manifest: dict | None = None) -> Path:
    if payload is None:
        steel_path_obj = Path(steel_path)
        try:
            with steel_path_obj.open(encoding="utf-8") as f:
                steel = json.load(f)
        except FileNotFoundError as exc:
            raise SystemExit(f"❌ 输入文件不存在：{steel_path}") from exc
        except json.JSONDecodeError as exc:
            raise SystemExit(
                f"❌ 非契约 JSON：{steel_path} 解析失败"
                f"（第 {exc.lineno} 行，第 {exc.colno} 列）") from exc
    else:
        steel = payload
    steel = _validate_contract(steel)
    sections = steel.get("sections") or []
    members = steel.get("members") or []
    connections = steel.get("connections") or []
    finishes = steel.get("finishes") or []

    parsed = [parse_section(r) for r in sections]
    usable = [p for p in parsed if p["kg_m"] > 0]
    only_count = [p for p in parsed if p["kg_m"] <= 0]

    expl = explicit_lengths(members)
    duplicates = duplicate_member_codes(members)
    merged, merge_review = member_merge(
        members, parsed, sections, steel.get("materials") or [])
    connection_summary, connection_review, connection_rows = connection_ledger(connections)
    plate_rows, plate_total = plate_tonnage_rows(connections)
    finish_summary, finish_review, finish_rows = finish_ledger(finishes)
    layer_len = drawn_length(steel)
    drawn_total = sum(layer_len.values())

    # 长度策略：显式长度有则用其合计；否则用图面线段长度（并标注口径）
    expl_total = sum(expl.values())
    if expl_total > 0:
        length_basis = "explicit"
        length_used, length_note = expl_total, "构件表显式长度 L= 合计"
    elif drawn_total > 0:
        length_basis = "drawn"
        length_used, length_note = drawn_total, "钢构件图层线段长度合计（图面口径，系统偏低）"
    else:
        length_basis = "none"
        length_used, length_note = 0.0, "无长度证据，只出截面谱不出吨位"

    # 截面谱：按（类型,文本,米重）聚合标注次数
    spec: dict[tuple, dict] = {}
    for p in parsed:
        key = (p["section_type"], p["text"], p["kg_m"])
        rec = spec.setdefault(key, {"count": 0, "note": p["note"]})
        rec["count"] += 1
    spec_rows = [
        {"section_type": k[0], "text": k[1], "kg_m": k[2],
         "count": v["count"], "note": v["note"]}
        for k, v in sorted(spec.items(), key=lambda kv: (-kv[0][2], kv[0][1]))
    ]

    # 吨位 A（草稿分摊）：把总长度按「截面米重加权」分摊到有米重的截面。
    # 这是在缺「每根构件↔截面」映射时退而求其次的口径，字段名必须带 allocated。
    rows: list[dict] = []
    alloc_lo = alloc_hi = 0.0
    weight_sum = sum(r["kg_m"] * r["count"] for r in spec_rows if r["kg_m"] > 0)
    if length_used > 0 and weight_sum > 0:
        for r in spec_rows:
            if r["kg_m"] <= 0:
                continue
            share = (r["kg_m"] * r["count"]) / weight_sum
            length_m = length_used * share
            t_lo = r["kg_m"] * length_m * 0.85 / 1000.0   # -15%
            t_hi = r["kg_m"] * length_m * 1.15 / 1000.0   # +15%
            alloc_lo += t_lo
            alloc_hi += t_hi
            rows.append({
                "截面类型": r["section_type"], "截面": r["text"],
                "标注次数": r["count"], "米重kg/m": r["kg_m"],
                "分摊长度m": round(length_m, 1),
                "吨位带t": [round(t_lo, 2), round(t_hi, 2)],
            })
    if rows:
        alloc_lo, alloc_hi = round(alloc_lo, 2), round(alloc_hi, 2)
    else:
        alloc_lo = alloc_hi = 0.0
    if plate_rows:
        alloc_lo = round(alloc_lo + plate_total[0], 2)
        alloc_hi = round(alloc_hi + plate_total[1], 2)
    allocated_band = [alloc_lo, alloc_hi] if (rows or plate_rows) else []

    # 吨位 B（推荐）：逐根台账求和。只有全部构件都有显式长度且单截面映射
    # 才算完整；否则退回分摊口径，并在报告中写明原因。
    member_band, member_note = member_level_total(merged)
    if member_band and plate_rows:
        member_band = [round(member_band[0] + plate_total[0], 2),
                       round(member_band[1] + plate_total[1], 2)]
    if member_band:
        total_band, total_basis = member_band, "member_level"
    elif allocated_band:
        total_band, total_basis = allocated_band, "allocated_estimate"
    else:
        total_band, total_basis = [], "none"

    grade_rows = grade_tonnage_rows(merged, total_band, total_basis, plate_total)
    scenarios = length_scenario_rows(spec_rows, length_scenarios or [])
    pre = prerequisites_status()
    closure = steel.get("geometry_closure")
    if isinstance(closure, dict):
        closure_check = {"status": "provided", "source": "cad-file-reader"}
        closure_check.update(closure)
    else:
        closure_check = {
            "status": "not_provided",
            "note": "圆/线段个数闭合校核须由 cad-file-reader 识图层提供；本技能不做识图。",
        }

    out = {
        "schema": SCHEMA,
        "final_quantity": False,
        "length_basis": length_basis,
        "length_note": length_note,
        "length_used_m": round(length_used, 1),
        "drawn_length_by_layer": {k: round(v, 1) for k, v in
                                  sorted(layer_len.items(), key=lambda kv: -kv[1])},
        "explicit_lengths_m": expl,
        "duplicate_members": duplicates,
        "grade_tonnage": grade_rows,
        "grade_counts": {
            grade: sum(1 for m in merged if m["grade"] == grade)
            for grade in sorted({m["grade"] for m in merged})
        },
        "member_merge": merged,
        "member_review_items": merge_review,
        "connection_review_items": connection_review,
        "finish_review_items": finish_review,
        "review_items": merge_review + connection_review + finish_review,
        "connection_summary": connection_summary,
        "connection_ledger": connection_rows,
        "connection_plate_tonnage": plate_rows,
        "connection_plate_total_t": plate_total if plate_rows else [],
        "finish_summary": finish_summary,
        "finish_ledger": finish_rows,
        "rows": rows,
        "spec_rows": spec_rows,
        "only_count": [p["text"] for p in only_count],
        "total_t": total_band,
        "total_basis": total_basis,
        "total_t_member_level": member_band or [],
        "total_t_allocated_estimate": allocated_band,
        "member_level_note": member_note,
        "length_scenarios": scenarios,
        "allowance_advice": allowance_advice(total_band),
        "geometry_closure_check": closure_check,
        "prerequisites": pre,
        "input_evidence": {
            "sections": len(sections),
            "members": len(members),
            "steel_geometry": len(steel.get("steel_geometry") or []),
            "materials": len(steel.get("materials") or []),
            "connections": len(connections),
            "finishes": len(finishes),
        },
        "summary": {
            "截面标注数": len(parsed),
            "可计米重截面数": len(usable),
            "仅计数截面数": len(only_count),
            "构件标注数": len(members),
            "构件归并数": len(merged),
            "归并复核数": len(merge_review),
            "牌号分档数": len(grade_rows),
            "总吨位带t": total_band,
            "总吨位口径": total_basis,
        },
    }
    if guard:
        stamp_result(out, guard)
        out["reader_version"] = guard.get("reader_version") or ""
    else:
        out["provenance"] = "manual"
        out["contract_id"] = ""
        out["source_sha256"] = ""
        out["contract_sha256"] = ""
        out["formal_ledger_eligible"] = False
        out["reader_version"] = ""
    out["run_manifest"] = run_manifest or cs.run_manifest(
        SKILL_NAME, _skill_version(), guard, argv=[])
    cs.write_handoff(Path(out_prefix).resolve().parent,
                     str(steel.get("project") or ""), "steel",
                     guard or {}, _handoff_members(merged))
    _render(out, Path(steel_path).stem, out_prefix)
    return Path(str(out_prefix) + ".csv")


def _render(out: dict, title: str, out_prefix: str) -> None:
    out_base = Path(out_prefix)
    out_base.parent.mkdir(parents=True, exist_ok=True)
    Path(str(out_base) + ".json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    md = StringIO()
    s = out["summary"]
    md.write(f"# {title}（钢结构吨位估算）\n\n")
    md.write("> **口径声明**：估算带（±15%），final_quantity=false；米重为截面几何公式近似"
             "（不含圆角，H 型偏低 1~2%、冷弯 C/Z 偏低 2~5%）；不替代深化设计、翻样、下料与结算。\n")
    md.write(f"> 长度口径：**{out['length_note']}**\n")
    pre = out.get("prerequisites") or {}
    provenance = out.get("provenance") or "unknown"
    if provenance == "reader":
        md.write("> 输入来源：lis-skill-bus 正式契约（provenance=reader，contract_id={}）\n".format(
            out.get("contract_id") or "-"))
    else:
        md.write("> 输入来源：文件契约手工降级（provenance={}），不是正式量；"
                 "正式量请用 --from-contract。\n".format(provenance))
    if not pre.get("ready_for_formal_pipeline"):
        problems = pre.get("problems") or []
        md.write("> 前置体检未通过：{}；识图仍由 cad-file-reader 完成，本技能不自带解图器。\n".format(
            "；".join(problems) if problems else "存在缺项"))
        if pre.get("install_hint") and pre.get("missing"):
            md.write(f"> {pre['install_hint']}\n")
    ev = out.get("input_evidence") or {}
    if ev and not ev.get("steel_geometry"):
        md.write("> 输入无证据：`steel_geometry[]` 为空，图面线段长度口径不可用。\n")
    md.write("\n")
    md.write(f"- 截面标注 {s['截面标注数']} 条（可计米重 {s['可计米重截面数']}、"
             f"仅计数 {s['仅计数截面数']}）；构件标注 {s['构件标注数']} 条\n")
    if out["duplicate_members"]:
        shown = "、".join(
            f"{r['code']}×{r['count']}" for r in out["duplicate_members"][:20])
        md.write(f"- ⚠️ 重复构件编号/名称：{shown}（需人工确认重复标注与实例数）\n")
    if out["total_t"]:
        basis_label = {
            "member_level": "逐根构件台账求和（推荐口径）",
            "allocated_estimate": "米重×标注次数分摊（草稿口径，非逐根）",
            "none": "无",
        }.get(out["total_basis"], out["total_basis"])
        total_label = ("总吨位带（推荐）" if out["total_basis"] == "member_level"
                       else "总吨位带（分摊草稿，不是答案）")
        md.write(f"- **{total_label}：{out['total_t'][0]}~{out['total_t'][1]} t**，"
                 f"口径：{basis_label}\n")
        if (out["total_basis"] == "member_level"
                and out.get("total_t_allocated_estimate")):
            a = out["total_t_allocated_estimate"]
            md.write(f"- 分摊口径参考：{a[0]}~{a[1]} t"
                     "（字段 `total_t_allocated_estimate`，仅供草稿对照，不作推荐值）\n")
        if out["total_basis"] == "allocated_estimate":
            md.write(f"- ⚠️ 未能建立完整逐根台账：{out.get('member_level_note') or '缺显式长度或截面映射'}；"
                     "总吨位为分摊草稿，构件级净量需人工复核\n")
        md.write("\n")
        if out["rows"]:
            md.write("## 分截面分摊（草稿明细，非逐根台账）\n\n"
                     "| 截面类型 | 截面 | 标注次数 | 米重kg/m | 分摊长度m | 吨位t带 |\n"
                     "|---|---|---|---|---|---|\n")
            for r in out["rows"]:
                md.write(f"| {r['截面类型']} | {r['截面']} | {r['标注次数']} | {r['米重kg/m']} "
                         f"| {r['分摊长度m']} | {r['吨位带t'][0]}~{r['吨位带t'][1]} |\n")
            md.write("\n")
    else:
        md.write("- ⚠️ 无长度证据或无可计米重截面：只出截面谱，不出吨位\n\n")
    if out.get("length_scenarios"):
        md.write("## 长度敏感性场景（不是结果）\n\n"
                 "每个截面标注按同一构件长度 L 估算，用于缺长度证据时对比选值。\n\n"
                 "| 构件长度m | 吨位t带 | 依据 |\n|---:|---|---|\n")
        for r in out["length_scenarios"]:
            md.write(f"| {r['length_m']} | {r['total_t_band'][0]}~{r['total_t_band'][1]} "
                     f"| {r['basis']} |\n")
        md.write("\n")
    allow = out.get("allowance_advice") or {}
    if allow.get("hoisting_reference_t"):
        md.write("## 吊装/运输建议附加（不并入总吨位）\n\n"
                 "| 项目 | 建议系数 | 说明 |\n|---|---:|---|\n")
        for r in allow["items"]:
            md.write(f"| {r['item']} | {int(r['rate'] * 100)}% | {r['note']} |\n")
        ref = allow["hoisting_reference_t"]
        md.write(f"\n- 参照总重（{allow['note']}）：**{ref[0]}~{ref[1]} t**\n\n")
    md.write("\n## 连接清单\n\n| 连接类别 | 标注次数 | 数量口径 | 计数依据 | 状态 |\n|---|---:|---|---|---|\n")
    for r in out["connection_summary"]:
        md.write(
            f"| {r['label']} | {r['label_count']} | {r['count'] if r['count'] is not None else '待复核'} "
            f"| {r['count_basis']} | {r['quantity_status']} |\n")
    if not (out.get("input_evidence") or {}).get("connections"):
        md.write("\n> 输入无证据：`connections[]` 为空，未做连接计数（不是技能未实现）。\n")
    if out["connection_ledger"]:
        md.write("\n### 连接台账\n\n| 类别 | 原文 | 单条计数 | 计数依据 | 状态 |\n|---|---|---:|---|---|\n")
        for r in out["connection_ledger"]:
            md.write(
                f"| {r['label']} | {r['raw']} | {r['count']} | {r['count_basis']} | {r['quantity_status']} |\n")
    if out["connection_plate_tonnage"]:
        md.write("\n## 节点板吨位（连接清单内）\n\n| 原文 | 依据 | kg | 吨位t带 |\n|---|---|---:|---|\n")
        for r in out["connection_plate_tonnage"]:
            md.write(f"| {r['raw']} | {r['basis']} | {r['kg']} | {r['tonnage_t'][0]}~{r['tonnage_t'][1]} |\n")

    md.write("\n## 涂装清单\n\n| 涂装类别 | 候选数 | 面积m²带 | 状态 | 依据 | 防火等级 |\n|---|---:|---|---|---|---|\n")
    for r in out["finish_summary"]:
        band = (f"{r['area_m2_band'][0]}~{r['area_m2_band'][1]}"
                if r["area_m2_band"] else "unavailable")
        md.write(
            f"| {r['label']} | {r['candidate_count']} | {band} | {r['area_status']} "
            f"| {r['basis']} | {r['fire_rating'] if r['fire_rating'] is not None else 'unavailable'} |\n")
    if not (out.get("input_evidence") or {}).get("finishes"):
        md.write("\n> 输入无证据：`finishes[]` 为空，未做涂装面积（不是技能未实现，防火等级不推断）。\n\n")
    if out["finish_ledger"]:
        md.write("\n### 涂装台账\n\n| 类别 | 原文 | 面积m²带 | 状态 | 依据 |\n|---|---|---|---|---|\n")
        for r in out["finish_ledger"]:
            band = (f"{r['area_m2_band'][0]}~{r['area_m2_band'][1]}"
                    if r["area_m2_band"] else "unavailable")
            md.write(f"| {r['label']} | {r['raw']} | {band} | {r['area_status']} | {r['basis']} |\n")

    if out["drawn_length_by_layer"]:
        md.write("## 图面线段长度（钢构件图层）\n\n| 图层 | 长度m |\n|---|---|\n")
        for k, v in out["drawn_length_by_layer"].items():
            md.write(f"| {k} | {v} |\n")
        md.write("\n")
    if out["grade_tonnage"]:
        md.write("## 牌号吨位带\n\n| 牌号 | 吨位t带 | 归并依据 |\n|---|---|---|\n")
        for r in out["grade_tonnage"]:
            md.write(f"| {r['grade']} | {r['tonnage_t'][0]}~{r['tonnage_t'][1]} | {r['allocation']} |\n")
        md.write("\n")
    md.write("## 截面谱（全部标注）\n\n| 截面类型 | 截面原文 | 次数 | 米重kg/m | 备注 |\n|---|---|---|---|---|\n")
    for r in out["spec_rows"]:
        md.write(f"| {r['section_type']} | {r['text']} | {r['count']} | "
                 f"{r['kg_m'] or '-'} | {r['note']} |\n")
    if out["only_count"]:
        md.write(f"\n（以下 {len(out['only_count'])} 条标注未进吨位：{'、'.join(out['only_count'][:20])}"
                 f"{'…' if len(out['only_count']) > 20 else ''}）\n")
    if out["member_merge"]:
        md.write("\n## 构件归并台账\n\n| 编号 | 实例 | 牌号 | 类别 | 系统 | 截面 | 显式长度m | 吨位t带 | 坐标x,y(mm) | 复核 |\n|---|---:|---|---|---|---|---:|---|---|---|\n")
        for r in out["member_merge"]:
            review_text = "；".join(r["conflicts"] + r["review_reasons"])
            coord = (f"{r['x']},{r['y']}" if r.get("location_status") == "provided" else "-")
            md.write(
                f"| {r['code']} | {r['instance_count']} | {r['grade']} | "
                f"{'+'.join(r['categories']) or '-'} | {'+'.join(r['systems']) or '-'} | "
                f"{'+'.join(r['section_texts']) or '-'} | {r['explicit_length_m']} | "
                f"{r['tonnage_t'][0] if r['tonnage_t'] else '-'}~"
                f"{r['tonnage_t'][1] if r['tonnage_t'] else '-'} | {coord} | {review_text or '-'} |\n")
    if out["review_items"]:
        md.write("\n## 复核清单\n\n")
        for r in out["review_items"][:50]:
            reasons = "；".join(r["reasons"])
            evidence = " | ".join(x for x in r["evidence"] if x)
            md.write(f"- {r['type']}｜{r['code']}：{reasons}{'；证据：' + evidence if evidence else ''}\n")
        if len(out["review_items"]) > 50:
            md.write(f"- …另有 {len(out['review_items']) - 50} 条复核项\n")
    Path(str(out_base) + ".md").write_text(md.getvalue(), encoding="utf-8")

    with Path(str(out_base) + ".csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["口径", "数值", "说明"])
        if out["total_t"]:
            basis_label = {"member_level": "逐根构件台账求和（推荐）",
                           "allocated_estimate": "米重×标注次数分摊（草稿）",
                           "none": "无"}.get(out["total_basis"], out["total_basis"])
            total_label = ("总吨位带t（推荐）" if out["total_basis"] == "member_level"
                           else "总吨位带t（分摊草稿）")
            w.writerow([total_label, f"{out['total_t'][0]}~{out['total_t'][1]}",
                        f"口径：{basis_label}；长度口径：{out['length_note']}"])
            if (out["total_basis"] == "member_level"
                    and out.get("total_t_allocated_estimate")):
                a = out["total_t_allocated_estimate"]
                w.writerow(["总吨位带t（分摊草稿）", f"{a[0]}~{a[1]}",
                            "字段 total_t_allocated_estimate，仅供对照，不作推荐值"])
            if out["rows"]:
                for r in out["rows"]:
                    w.writerow([f"吨位-{r['截面']}", f"{r['吨位带t'][0]}~{r['吨位带t'][1]}",
                                f"{r['米重kg/m']} kg/m × {r['分摊长度m']} m × {r['标注次数']} 次标注分摊"])
            if out["connection_plate_total_t"]:
                w.writerow(["连接节点板吨位t",
                            f"{out['connection_plate_total_t'][0]}~{out['connection_plate_total_t'][1]}",
                            "仅含厚×宽×长或板厚×面积证据的节点板"])
        elif out["connection_plate_total_t"]:
            w.writerow(["总吨位带t（仅节点板）",
                        f"{out['connection_plate_total_t'][0]}~{out['connection_plate_total_t'][1]}",
                        "无杆件长度证据；总吨位仅含连接节点板"])
        else:
            w.writerow(["总吨位", "", "无长度证据或无可计米重截面，只出截面谱"])
        for r in out.get("length_scenarios") or []:
            w.writerow([f"长度场景-{r['length_m']}m",
                        f"{r['total_t_band'][0]}~{r['total_t_band'][1]}", r["basis"]])
        allow = out.get("allowance_advice") or {}
        if allow.get("hoisting_reference_t"):
            ref = allow["hoisting_reference_t"]
            w.writerow(["吊装/运输参照总重t（不含在总吨位）", f"{ref[0]}~{ref[1]}",
                        allow["note"]])
        for r in out["connection_summary"]:
            w.writerow([f"连接-{r['label']}",
                        r["count"] if r["count"] is not None else "待复核",
                        f"标注次数={r['label_count']}；计数依据={r['count_basis']}；状态={r['quantity_status']}"])
        for r in out["connection_ledger"]:
            w.writerow([f"连接台账-{r['label']}-{r['raw']}", r["count"],
                        f"计数依据={r['count_basis']}；状态={r['quantity_status']}"])
        for r in out["finish_summary"]:
            w.writerow([f"涂装-{r['label']}",
                        (f"{r['area_m2_band'][0]}~{r['area_m2_band'][1]}m²"
                         if r["area_m2_band"] else "unavailable"),
                        f"候选数={r['candidate_count']}；依据={r['basis']}；防火等级={r['fire_rating'] or 'unavailable'}"])
        for r in out["finish_ledger"]:
            w.writerow([f"涂装台账-{r['label']}-{r['raw']}",
                        (f"{r['area_m2_band'][0]}~{r['area_m2_band'][1]}m²"
                         if r["area_m2_band"] else "unavailable"), r["basis"]])
        for r in out["review_items"]:
            w.writerow([f"复核-{r['type']}-{r['code']}", len(r["reasons"]),
                        "；".join(r["reasons"])])
        for r in out["spec_rows"]:
            w.writerow([f"截面谱-{r['text']}", r["count"], f"{r['section_type']}；{r['note']}"])
        for r in out["grade_tonnage"]:
            w.writerow([f"牌号吨位-{r['grade']}",
                        f"{r['tonnage_t'][0]}~{r['tonnage_t'][1]}", r["allocation"]])
        for r in out["member_merge"]:
            review_text = "；".join(r["conflicts"] + r["review_reasons"])
            w.writerow([
                f"构件归并-{r['code']}", r["instance_count"],
                f"牌号={r['grade']}；类别={'+'.join(r['categories']) or '-'}；"
                f"系统={'+'.join(r['systems']) or '-'}；截面={'+'.join(r['section_texts']) or '-'}；"
                f"长度={r['explicit_length_m']}m；吨位={r['tonnage_t'][0] if r['tonnage_t'] else '-'}~"
                f"{r['tonnage_t'][1] if r['tonnage_t'] else '-'}；复核={review_text or '-'}",
            ])


def main() -> None:
    raw = sys.argv[1:]
    ap = argparse.ArgumentParser(
        description="Steel tonnage estimate from cad_steel_geometry output")
    ap.add_argument("contract", nargs="?",
                    help="契约 JSON 路径（文件路径算量/mode=manual；--validate 时可作为位置参数）")
    ap.add_argument("--steel",
                    help="cad_steel_geometry 产物 *.steel.json（文件路径算量，必须配 --allow-manual）")
    ap.add_argument("--from-contract", metavar="CONTRACT_ID",
                    help="按 contract_id 从 lis-skill-bus 取正式契约（bus-only 入口）")
    ap.add_argument("--project", default="",
                    help="--from-contract 使用的 bus 项目标识")
    ap.add_argument("--allow-manual", action="store_true",
                    help="显式允许手工/文件契约；结果 provenance=manual、final_quantity=false")
    ap.add_argument("--out-prefix", help="输出前缀（计算模式必填）")
    ap.add_argument("--validate", action="store_true",
                    help="只体检输入契约：缺字段、未匹配截面、仅计数项；不出吨位")
    ap.add_argument("--report", help="--validate 时把体检报告另存为 JSON")
    ap.add_argument("--check-deps", action="store_true",
                    help="检查正式识图链路前置（cad-file-reader / lis-skill-bus）；缺 reader=20、缺 bus=21")
    ap.add_argument("--length-scenario", action="append", type=float, default=[],
                    metavar="M", help="长度敏感性场景（米，可重复，如 --length-scenario 4.5）")
    a = ap.parse_args(raw)

    if a.check_deps:
        status = cs.check_deps()
        print(cs.format_deps(status))
        raise SystemExit(eg.dependency_exit_code())

    # 入口闸门：缺 cad-file-reader / lis-skill-bus 先停；直接给图纸一律拒收。
    try:
        eg.require_reader()
        eg.require_bus()
        eg.reject_drawing_input(a.contract, a.steel)
    except eg.GateError as exc:
        raise SystemExit(eg.print_gate_error(exc)) from None

    steel_path = a.steel or a.contract
    if a.validate:
        if not steel_path:
            ap.error("--validate 需要契约路径：--steel 路径 或 直接放位置参数")
        report = validate_path(steel_path)
        print(format_health(report))
        if a.report:
            rp = Path(a.report)
            rp.parent.mkdir(parents=True, exist_ok=True)
            rp.write_text(json.dumps(report, ensure_ascii=False, indent=2),
                          encoding="utf-8")
            print(f"体检报告：{rp}")
        raise SystemExit(0 if report["status"] != "error" else 2)

    if a.from_contract and a.contract:
        print("WARN: 位置参数 contract 与 --from-contract 同时出现，"
              "已忽略位置参数，以 --from-contract=%s 为准。" % a.from_contract,
              file=sys.stderr)

    if not a.out_prefix:
        ap.error("计算模式需要 --out-prefix；只体检请用 --validate")

    if a.from_contract:
        # 正式入口：只认 bus 里的契约；取不到就停，不退回本地文件/自写解析。
        entry, err = _bus_pull(a.project, a.from_contract)
        if entry is None:
            print("❌ 未取到契约 %s：%s" % (a.from_contract, err), file=sys.stderr)
            print("拉取命令（复制执行）：python3 ${CODEX_HOME:-$HOME/.codex}/skills/lis-skill-bus/"
                  "skillbus_client.py pull --project %s --entry-id %s"
                  % (a.project or "<项目>", a.from_contract), file=sys.stderr)
            print("安装 bus（复制执行）：bash ${CODEX_HOME:-$HOME/.codex}/skills/lis-skill-bus/"
                  "install_skillbus.sh --apply", file=sys.stderr)
            raise SystemExit(1)
        guard_doc, payload, bus_warnings = _normalize_bus_entry(
            entry, a.from_contract)
        try:
            guard = _guard_from_dict(guard_doc, allow_manual=False,
                                     label="bus:%s" % a.from_contract)
        except GuardError as exc:
            _print_guard_error(exc)
            raise SystemExit(exc.code) from None
        if guard.get("mode") != "formal":
            print("❌ 契约来源不是 reader/bus，不能进正式算量。", file=sys.stderr)
            raise SystemExit(3)
        guard["warnings"] = list(guard.get("warnings") or []) + bus_warnings
        guard["reader_version"] = _pick_reader_version(guard_doc, payload)
        payload = _validated_payload(payload)
        safe_id = re.sub(r"[^0-9A-Za-z._-]+", "-", a.from_contract)[:64] or "contract"
        build("bus-" + safe_id, a.out_prefix,
              length_scenarios=a.length_scenario, payload=payload,
              guard=guard, run_manifest=_run_manifest(guard))
        return

    if not steel_path:
        ap.error("计算模式需要 --from-contract 或 --steel/位置参数 + --out-prefix；"
                 "只体检请用 --validate")

    # 文件/手工入口：必须显式 --allow-manual；缺了就 exit 3。
    if not a.allow_manual:
        print("❌ 来源未授权：--steel/位置参数是文件契约，必须同时给 --allow-manual。",
              file=sys.stderr)
        print("正式量请用 --from-contract <contract_id> --project <项目>；"
              "手工降级请加 --allow-manual（结果 final_quantity=false）。",
              file=sys.stderr)
        raise SystemExit(3)

    try:
        guard, payload = _guard_file_manual(steel_path)
    except GuardError as exc:
        _print_guard_error(exc)
        raise SystemExit(exc.code) from None
    guard["reader_version"] = _pick_reader_version(guard.get("contract") or {})
    payload = _validated_payload(payload)
    build(steel_path, a.out_prefix, length_scenarios=a.length_scenario,
          payload=payload, guard=guard, run_manifest=_run_manifest(guard))


if __name__ == "__main__":
    main()
