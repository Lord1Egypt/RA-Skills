#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""跨图聚合层：把多张图纸的识图候选，按「楼层 × 分区 × 构件 × 规格 / 钢筋型号」归并成表。

设计动机
--------
上游 cad_structural_geometry.py 只产出**逐条候选流水账**（实测 13 张样例 J 车库图：
members 4196、rebars 7178），用户拿不到「各型号钢筋量」「每层有多少种规格的梁柱」。
真图回归也印证瓶颈不在单条精度而在「没成表、不能跨图归并」：24 张抽样里
duplicate_candidate 21303 条、missing_layer 18613 条。本模块的正解不是丢数据，
而是**归并计数**——同一 (楼层, 分区, 类别, 规格) 只出一行，用 count 说明原候选重复了多少次。

边界（红线）
------------
- 只做**提取与归并**：出「型号出现频次 / 规格出现频次 / 涉及图纸数」。
- 绝不出吨位、体积、面积、长度、造价——那是 tujian-suanliang 等算量技能的下游职责。
- 确认态 confirmed_evidence 不允许由本模块自行升级：聚合行置信度固定 < 0.90，
  因此只可能落在 inferred_candidate 或 review_required。
- 所有候选 final_quantity=false。
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

try:  # 牌号映射是可选的：没有说明表时聚合层行为与从前完全一致
    from rebar_grade import resolve_grade as _resolve_grade
except Exception:  # pragma: no cover - 单独拷走本脚本时降级
    _resolve_grade = None

ROOT = Path(__file__).resolve().parents[1]
RULES_PATH = ROOT / "packs" / "structural-geometry" / "rules.json"

from cad_common import compact, load_rules  # noqa: E402
from cad_contract import contractize_payload  # noqa: E402

SCHEMA = "cad-project-aggregate/v1"
CLEARANCE = "本表为提取结果，非工程量，不可直接用于结算"
# 聚合行置信度：刻意低于 confirmed_evidence 的 0.90 门槛，防止本模块自行升级确认态。
AGGREGATE_CONFIDENCE = 0.72

UNKNOWN_FLOOR = "unknown"
UNKNOWN_ZONE = "unknown"
UNKNOWN_SPEC = "未标注规格"

# packs/structural-geometry/rules.json 的 member_rules 用英文类别，出表时转中文便于用户直接看
CATEGORY_ZH = {
    "beam": "梁", "column": "柱", "slab": "板", "wall": "墙",
    "foundation": "基础", "stair": "楼梯", "node_strengthening": "节点加强",
    "opening_strengthening": "洞口加强", "rebar_set": "配筋集",
}

# ---------------------------------------------------------------- 楼层归一化

CN_DIGITS = {"零": 0, "一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5,
             "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}


def cn_to_int(text: str) -> int | None:
    """中文数字 → int，支持 一~十、十一~十九、二十~九十九。"""
    text = compact(text)
    if not text:
        return None
    if text.isdigit():
        return int(text)
    if text == "十":
        return 10
    if "十" in text:
        head, _, tail = text.partition("十")
        tens = CN_DIGITS.get(head, 1) if head else 1
        ones = CN_DIGITS.get(tail, 0) if tail else 0
        return tens * 10 + ones
    value = 0
    for ch in text:
        if ch not in CN_DIGITS:
            return None
        value = value * 10 + CN_DIGITS[ch]
    return value


def _floor(label: str, order: int) -> dict[str, Any]:
    return {"label": label, "order": order}


def _match_floor(text: str, rules: list[tuple[str, Any]]) -> dict[str, Any] | None:
    for pattern, handler in rules:
        m = re.search(pattern, text)
        if not m:
            continue
        result = handler(m)
        if result:
            return result
    return None


def _neg(m) -> dict[str, Any]:
    value = cn_to_int(m.group(1))
    if value is None:
        return None
    return _floor(f"-{value}F", -value)


def _pos(m) -> dict[str, Any]:
    value = cn_to_int(m.group(1))
    if value is None or value <= 0:
        return None
    return _floor(f"{value}F", value)


def _fixed(label: str, order: int):
    def _h(_m):
        return _floor(label, order)
    return _h


# 图名/图号专用（可识别 B1 / -1F 这类缩写，代价是可能与构件编号撞车，故只用于图名）
NAME_FLOOR_RULES: list[tuple[str, Any]] = [
    (r"(机房层|设备层|电梯机房)", _fixed("机房层", 900)),
    (r"(屋面层|屋面|屋顶|顶层)", _fixed("屋面", 999)),
    (r"(?:地下室|地下)\s*([0-9一二三四五六七八九十]{1,3})\s*层", _neg),
    (r"(?:地下室|地下)(?![0-9一二三四五六七八九十])", _fixed("-1F", -1)),
    (r"[-−负]\s*([0-9一二三四五六七八九十]{1,3})\s*[层F](?![A-Za-z0-9])", _neg),
    (r"(?<![A-Za-z0-9])B\s*([0-9]{1,2})(?![A-Za-z0-9])", _neg),
    (r"(?<![A-Za-z0-9])([0-9]{1,3})\s*F(?![A-Za-z0-9])", _pos),
    (r"([0-9]{1,3})\s*层", _pos),
    (r"([一二三四五六七八九十]{1,3})\s*层", _pos),
    (r"首层", _fixed("1F", 1)),
    (r"(顶板|屋面板)", _fixed("屋面", 999)),
    (r"(基础|承台|筏板|底板)", _fixed("基础", -999)),
]

# 图内文本专用（只用显式中文写法与独立成词的 XF，避免把 B1 板编号当楼层）
TEXT_FLOOR_RULES: list[tuple[str, Any]] = [
    (r"(机房层|设备层|电梯机房)", _fixed("机房层", 900)),
    (r"(屋面层|屋面|屋顶|顶层)", _fixed("屋面", 999)),
    (r"(?:地下室|地下)\s*([0-9一二三四五六七八九十]{1,3})\s*层", _neg),
    (r"[-−负]\s*([0-9一二三四五六七八九十]{1,3})\s*[层F](?![A-Za-z0-9])", _neg),
    (r"(?<![A-Za-z0-9])-?\s*([0-9]{1,2})\s*F(?![A-Za-z0-9])", _pos),
    (r"([0-9]{1,3})\s*层", _pos),
    (r"([一二三四五六七八九十]{1,3})\s*层", _pos),
    (r"首层", _fixed("1F", 1)),
]

ZONE_RE = re.compile(r"([0-9]{1,2}[A-Za-z]?)\s*J?区")


def infer_zone(name: str) -> str:
    """从图名推断分区/标段（如 1J区、2J区、5J区）；无则 unknown。"""
    m = ZONE_RE.search(compact(name))
    return m.group(0) if m else UNKNOWN_ZONE


def infer_floor(name: str, texts: list[str] | None = None, top_n: int = 30) -> dict[str, Any]:
    """推断楼层：图名优先；图名判不出时用图内文本投票（取出现最多的楼层写法）。

    返回 {"label","order","source","raw","votes"}，判不出时 label=unknown。
    """
    name_floor = _match_floor(compact(name), NAME_FLOOR_RULES)
    if name_floor:
        return {**name_floor, "source": "drawing_name", "raw": compact(name)[:80], "votes": 1}

    votes: Counter[tuple[str, int]] = Counter()
    raws: dict[tuple[str, int], str] = {}
    for raw in (texts or [])[:top_n]:
        hit = _match_floor(compact(raw), TEXT_FLOOR_RULES)
        if not hit:
            continue
        key = (hit["label"], hit["order"])
        votes[key] += 1
        raws.setdefault(key, compact(raw)[:80])
    if votes:
        (label, order), count = votes.most_common(1)[0]
        return {"label": label, "order": order, "source": "drawing_text", "raw": raws[(label, order)], "votes": count}
    return {"label": UNKNOWN_FLOOR, "order": 10 ** 6, "source": "none", "raw": "", "votes": 0}


# ---------------------------------------------------------------- 钢筋解析

# 私有区字符（tssdeng.shx 等 CAD 字体把钢筋符号映射到 U+E532 一带）与标准 Φφ 一并认。
_REBAR_SYMBOL = r"(?:%%13[0-2]|[Φφ-])"
_COUNT_DIA_RE = re.compile(r"(?<![0-9])(\d{1,2})\s*" + _REBAR_SYMBOL + r"\s*(\d{1,2})")
_PCT_DIA_RE = re.compile(r"%%13[0-2]\s*(\d{1,2})")
_SYM_DIA_RE = re.compile(_REBAR_SYMBOL + r"\s*(\d{1,2})")
_AT_DIA_RE = re.compile(r"(?<![0-9.])(\d{1,2})\s*@\s*\d{2,4}")
_SPACING_RE = re.compile(r"@\s*(\d{2,4})(?:\s*/\s*(\d{2,4}))?")
_LEGS_RE = re.compile(r"\((\d{1,2})\)")
_GRADE_RE = re.compile(r"(HPB300|HRB300|HRB335|HRB400|HRB500|CRB550|RRB400)")
_GRADE_LETTER_RE = re.compile(r"(?<![A-Za-z0-9])([ABC])(\d{1,2})(?![0-9])")

MIN_DIA, MAX_DIA = 4, 50


def display_spec(spec: str) -> str:
    """把 CAD 私有区钢筋符号 / %%13x 转义替换成可读的 Φ（只影响展示，不改原始证据）。"""
    text = compact(spec)
    text = re.sub(r"%%13[0-2]", "Φ", text)
    text = re.sub(r"[\ue000-\uf8ff]", "Φ", text)
    text = re.sub(r"Φ{2,}", "Φ", text)
    return text


def parse_rebar(spec: str) -> dict[str, Any]:
    """把一条配筋标注解析成结构化字段；直径不在 4~50 时判为 unknown。"""
    raw = compact(spec).upper()
    out: dict[str, Any] = {"raw": raw, "count": None, "diameter": None,
                           "spacing": None, "encryption": None, "legs": None,
                           "grade": None, "kind": "unknown"}

    m = _COUNT_DIA_RE.search(raw)
    if m:
        out["count"] = int(m.group(1))
        out["diameter"] = int(m.group(2))
    if out["diameter"] is None:
        m = _PCT_DIA_RE.search(raw)
        if m:
            out["diameter"] = int(m.group(1))
    if out["diameter"] is None:
        m = _SYM_DIA_RE.search(raw)
        if m:
            out["diameter"] = int(m.group(1))
    if out["diameter"] is None:
        m = _AT_DIA_RE.search(raw)
        if m:
            out["diameter"] = int(m.group(1))
    if out["diameter"] is not None and not (MIN_DIA <= out["diameter"] <= MAX_DIA):
        out["diameter"] = None

    m = _SPACING_RE.search(raw)
    if m:
        out["spacing"] = int(m.group(1))
        if m.group(2):
            out["encryption"] = int(m.group(2))
    m = _LEGS_RE.search(raw)
    if m:
        out["legs"] = int(m.group(1))

    m = _GRADE_RE.search(raw)
    if m:
        out["grade"] = m.group(1)
    else:
        m = _GRADE_LETTER_RE.search(raw)
        if m:
            out["grade"] = m.group(1)

    if out["spacing"] is not None:
        out["kind"] = "spacing"
    elif out["count"] is not None:
        out["kind"] = "count"
    elif out["diameter"] is not None:
        out["kind"] = "diameter_only"
    return out


# ---------------------------------------------------------------- 构件规格

SECTION_RE = re.compile(r"(?<![0-9.])(\d{2,4})\s*[xX×]\s*(\d{2,4})(?![0-9])")


def member_spec(row: dict[str, Any]) -> tuple[str, str | None]:
    """返回 (主规格, 主截面)。优先构件编号（KL1/KZ3），没有则取截面 B×H。"""
    code = compact(row.get("code") or "")
    text = compact((row.get("evidence") or [{}])[0].get("text", ""))
    m = SECTION_RE.search(text)
    section = f"{m.group(1)}×{m.group(2)}" if m else None
    if code:
        return code, section
    if section:
        return section, section
    return UNKNOWN_SPEC, None


# ---------------------------------------------------------------- 输入装载


def load_source(path: Path, rules: dict[str, Any] | None = None) -> dict[str, Any]:
    """装载一个输入：结构识图产物直接用；cad_scan 详情则现算一次结构识图。"""
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data.get("members"), list) and isinstance(data.get("rebars"), list):
        return data
    if isinstance(data.get("text_records"), list) or isinstance(data.get("texts"), list):
        from cad_structural_geometry import analyze_file  # 延迟导入：只在需要时依赖
        if rules is None:
            rules = load_rules(RULES_PATH)
        return analyze_file(path, rules)
    raise ValueError(f"无法识别的输入（既无 members/rebars，也无 text_records）：{path}")


def sheet_name(payload: dict[str, Any], path: Path) -> str:
    """图纸显示名：优先 payload.source_file，并剥掉 cad_scan 产物后缀（_detail/_structural 等）。"""
    base = compact(payload.get("source_file") or path.name) or path.name
    stem = Path(base).stem
    for suffix in ("_detail", "_structural", "_scan"):
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]
    if stem in ("detail", "structural", "scan"):  # 形如 <名>_structural/detail.json
        stem = path.parent.name
        for suffix in ("_detail", "_structural", "_scan"):
            if stem.endswith(suffix):
                stem = stem[: -len(suffix)]
    return stem or Path(base).stem


# ---------------------------------------------------------------- 聚合主流程


def aggregate(sources: list[tuple[Path, dict[str, Any]]],
              legend: dict[str, Any] | None = None) -> dict[str, Any]:
    """把多个图纸产物归并成楼层表 / 构件归并表 / 钢筋型号表 / 楼层×直径交叉表。

    legend 是 rebar_grade 产出的「符号→牌号」映射（可选）。不给时牌号仍按字面解析，
    与从前行为一致——**没有说明表就不给牌号**，绝不套国标默认值。
    """
    # 批次校验：映射必须来自本批图纸之一。跨项目套用会得出「全部 HRB400」这类假结果，
    # 比 unknown 更危险——unknown 至少知道自己不知道。所以宁可弃用映射，也不让错牌号流出去。
    legend_mismatch: dict[str, Any] | None = None
    if legend:
        src_drawings = set(legend.get("source_drawings") or [])
        here = {sheet_name(payload, path) for path, payload in sources}
        if src_drawings and not (src_drawings & here):
            legend_mismatch = {
                "legend_from": sorted(src_drawings)[:8],
                "current": sorted(here)[:8],
            }
            legend = None
    inputs: list[dict[str, Any]] = []
    member_rows: dict[tuple, dict[str, Any]] = {}
    rebar_rows: dict[tuple, dict[str, Any]] = {}
    rebar_floor_rows: dict[tuple, dict[str, Any]] = {}
    review: list[dict[str, Any]] = []
    floor_index: dict[str, dict[str, Any]] = {}

    for path, payload in sources:
        name = sheet_name(payload, path)
        texts = [compact((r.get("evidence") or [{}])[0].get("text", "")) for r in (payload.get("members") or [])]
        reb_texts = [compact((r.get("evidence") or [{}])[0].get("text", "")) for r in (payload.get("rebars") or [])]
        floor = infer_floor(name, texts + reb_texts)
        zone = infer_zone(name)
        inputs.append({"drawing": name, "path": str(path), "floor": floor["label"],
                       "floor_order": floor["order"], "floor_source": floor["source"],
                       "floor_raw": floor["raw"], "zone": zone})

        node = floor_index.setdefault(floor["label"], {"label": floor["label"], "order": floor["order"],
                                                       "drawings": [], "zones": []})
        if name not in node["drawings"]:
            node["drawings"].append(name)
        if zone not in node["zones"]:
            node["zones"].append(zone)
        if floor["label"] == UNKNOWN_FLOOR:
            review.append({"type": "floor_unknown", "reason": f"未能判定楼层：{name}", "evidence": [{"file": name}]})

        # --- 构件归并 ---
        for row in (payload.get("members") or []):
            category = compact(row.get("category") or "其它") or "其它"
            spec, section = member_spec(row)
            key = (floor["label"], zone, category, spec)
            item = member_rows.setdefault(key, {
                "floor": floor["label"], "floor_order": floor["order"], "zone": zone,
                "category": category, "spec": spec, "name": spec, "count": 0,
                "drawings": [], "section_counts": Counter(), "layers": Counter(),
                "evidence": [], "confidence": AGGREGATE_CONFIDENCE, "status": "candidate"})
            item["count"] += 1
            if section:
                item["section_counts"][section] += 1
            layer = compact(row.get("layer") or "")
            if layer:
                item["layers"][layer] += 1
            dname = compact(row.get("file") or name)
            if dname not in item["drawings"]:
                item["drawings"].append(dname)
            if len(item["evidence"]) < 3:
                item["evidence"].extend(row.get("evidence") or [])

        # --- 钢筋归并 ---
        for row in (payload.get("rebars") or []):
            parsed = parse_rebar(compact(row.get("rebar_spec") or ""))
            dia = parsed["diameter"]
            if dia is None:
                review.append({"type": "rebar_diameter_unknown",
                               "reason": f"配筋标注未解析出直径：{parsed['raw'][:60]}",
                               "evidence": [{"file": compact(row.get("file") or name), "text": parsed["raw"][:60]}]})
                continue
            grade = parsed["grade"] or "unknown"
            grade_basis = "literal" if parsed["grade"] else "none"
            if grade == "unknown" and legend and _resolve_grade is not None:
                grade, grade_basis, _conf = _resolve_grade(parsed["raw"], legend)
            key = (dia, grade)
            item = rebar_rows.setdefault(key, {
                "diameter": dia, "grade": grade, "name": f"Φ{dia}", "count": 0, "drawings": [],
                "samples": Counter(), "kinds": Counter(), "floors": Counter(), "layers": Counter(),
                "bases": Counter(), "confidence": AGGREGATE_CONFIDENCE, "status": "candidate"})
            item["count"] += 1
            item["bases"][grade_basis] += 1
            item["samples"][display_spec(parsed["raw"])[:60]] += 1
            item["kinds"][parsed["kind"]] += 1
            item["floors"][floor["label"]] += 1
            rlayer = compact(row.get("layer") or "")
            if rlayer:
                item["layers"][rlayer] += 1
            dname = compact(row.get("file") or name)
            if dname not in item["drawings"]:
                item["drawings"].append(dname)

            fkey = (floor["label"], dia, grade)
            fitem = rebar_floor_rows.setdefault(fkey, {
                "floor": floor["label"], "floor_order": floor["order"], "diameter": dia,
                "grade": grade, "count": 0, "drawings": [], "grades": Counter(),
                "confidence": AGGREGATE_CONFIDENCE, "status": "candidate"})
            fitem["count"] += 1
            fitem["grades"][grade] += 1
            if dname not in fitem["drawings"]:
                fitem["drawings"].append(dname)

    def _finalize(item: dict[str, Any]) -> dict[str, Any]:
        out = {k: v for k, v in item.items()
               if k not in ("section_counts", "layers", "samples", "kinds", "floors", "grades", "bases")}
        if "section_counts" in item:
            counts = item["section_counts"]
            out["sections"] = [{"section": s, "count": c} for s, c in counts.most_common(5)]
            out["section"] = counts.most_common(1)[0][0] if counts else None
        if "category" in out:
            out["category_code"] = out["category"]
            out["category"] = CATEGORY_ZH.get(out["category"], out["category"])
        layers = item.get("layers")
        if isinstance(layers, Counter):
            out["layer"] = layers.most_common(1)[0][0] if layers else None
            out["layer_count"] = len(layers)
        if "samples" in item:
            out["samples"] = [s for s, _ in item["samples"].most_common(5)]
            out["kinds"] = dict(item["kinds"])
            out["floor_counts"] = dict(item["floors"])
        if "bases" in item:
            bases = item["bases"]
            out["grade_basis"] = bases.most_common(1)[0][0] if bases else "none"
            out["grade_bases"] = dict(bases)
        if "grades" in item:
            out["grades"] = dict(item["grades"])
        out["drawing_count"] = len(out.get("drawings") or [])
        if isinstance(layers, Counter) and not layers:
            out["status"] = "review"
            out["review_reasons"] = ["missing_layer"]
        return out

    member_table = sorted((_finalize(v) for v in member_rows.values()),
                          key=lambda r: (-r["count"], r["floor_order"], r["category"], r["spec"]))
    rebar_table = sorted((_finalize(v) for v in rebar_rows.values()),
                         key=lambda r: (-r["count"], -(r["diameter"] or 0)))
    rebar_by_floor = sorted((_finalize(v) for v in rebar_floor_rows.values()),
                            key=lambda r: (r["floor_order"], -(r["diameter"] or 0)))
    floors = sorted(floor_index.values(), key=lambda r: r["order"])

    if legend_mismatch:
        review.append({
            "type": "legend_source_mismatch",
            "reason": "牌号映射不是来自本批图纸，已弃用（否则会给出看似完整实则错误的牌号）",
            "evidence": [{"legend_from": legend_mismatch["legend_from"],
                          "current": legend_mismatch["current"]}],
        })

    total_members = sum(r["count"] for r in member_table)
    total_rebars = sum(r["count"] for r in rebar_table)
    # 牌号覆盖：直接说清有多少条真拿到了牌号、多少条还是未标注，别让人以为全解出来了
    grade_stat = Counter()
    for r in rebar_table:
        for basis, n in (r.get("grade_bases") or {}).items():
            grade_stat[basis] += n
    payload = {
        "schema": SCHEMA,
        "clearance": CLEARANCE,
        "boundary": "只输出提取与归并结果（型号/规格出现频次与涉及图纸数）；不出吨位、体积、面积、长度、造价或结算量。",
        "source_count": len(sources),
        "inputs": inputs,
        "floors": floors,
        "members": member_table,
        "rebars": rebar_table,
        "rebar_by_floor": rebar_by_floor,
        "review": review,
        "summary": {
            "drawings": len(sources),
            "floors": len(floors),
            "member_groups": len(member_table),
            "member_candidates": total_members,
            "rebar_groups": len(rebar_table),
            "rebar_candidates": total_rebars,
            "rebar_by_floor_groups": len(rebar_by_floor),
            "review_items": len(review),
            "rebar_grade": {
                "total": total_rebars,
                "direct": grade_stat.get("direct", 0),
                "bridged": grade_stat.get("bridged", 0),
                "literal": grade_stat.get("literal", 0),
                "unknown": grade_stat.get("none", 0) + grade_stat.get("mixed", 0),
            },
        },
    }
    return payload


# ---------------------------------------------------------------- 输出


def _grade_coverage_line(stat: dict[str, int]) -> str:
    """牌号覆盖一行话。老实说清楚多少条还没解出来，别让人以为全给了。"""
    total = stat.get("total") or 0
    if not total:
        return "- 钢筋牌号：无"
    got = stat.get("direct", 0) + stat.get("literal", 0) + stat.get("bridged", 0)
    pct = got / total * 100
    parts = [f"{got}/{total} 条拿到牌号（{pct:.1f}%）"]
    if stat.get("literal"):
        parts.append(f"标注自带 {stat['literal']}")
    if stat.get("direct"):
        parts.append(f"说明表直接定义 {stat['direct']}")
    if stat.get("bridged"):
        parts.append(f"尾号外推 {stat['bridged']}")
    if stat.get("unknown"):
        parts.append(f"仍未知 {stat['unknown']}")
    return "- 钢筋牌号：" + "，".join(parts)


def write_markdown(payload: dict[str, Any], path: Path) -> None:
    s = payload["summary"]
    lines = ["# 跨图聚合 / 提取结果", "",
             f"- 图纸 {s['drawings']} 张，楼层 {s['floors']} 个",
             f"- 构件归并 {s['member_groups']} 组（原始候选 {s['member_candidates']} 条）",
             f"- 钢筋归并 {s['rebar_groups']} 组（原始候选 {s['rebar_candidates']} 条）",
             f"- 待复核 {s['review_items']} 项",
             _grade_coverage_line(s.get("rebar_grade") or {}), "",
             f"> {payload['clearance']}", "", "## 图纸与楼层", "",
             "| 图纸 | 楼层 | 分区 | 判定来源 |", "|---|---|---|---|"]
    for row in payload["inputs"]:
        lines.append(f"| {row['drawing']} | {row['floor']} | {row['zone']} | {row['floor_source']} |")

    lines += ["", "## 各型号钢筋（按直径×牌号）", "", "| 直径 | 牌号 | 出现次数 | 涉及图纸数 | 典型标注 |", "|---|---|---|---|---|"]
    for row in payload["rebars"][:120]:
        grade = row["grade"]
        bases = row.get("grade_bases") or {}
        bridged = bases.get("bridged", 0)
        # 牌号不是本图说明表直接写的就得说清楚，别让人当实证用。
        # 同一组里混有外推时也要写明条数——多数是 direct 不能掩盖少数是外推。
        if grade == "unknown":
            grade = "未标注"
        elif bridged and bridged >= row["count"]:
            grade += "（尾号外推）"
        elif bridged:
            grade += f"（含 {bridged} 处尾号外推）"
        lines.append(f"| Φ{row['diameter']} | {grade} | {row['count']} | {row['drawing_count']} | {('、'.join(row['samples'][:3]))} |")

    lines += ["", "## 每层钢筋直径分布", "", "| 楼层 | 直径 | 牌号 | 出现次数 | 涉及图纸数 |", "|---|---|---|---|---|"]
    for row in payload["rebar_by_floor"][:200]:
        grade = row.get("grade") or "unknown"
        if grade == "unknown":
            grade = "未标注"
        lines.append(f"| {row['floor']} | Φ{row['diameter']} | {grade} | {row['count']} | {row['drawing_count']} |")

    lines += ["", "## 各层构件规格", "", "| 楼层 | 分区 | 类别 | 规格 | 主截面 | 出现次数 | 涉及图纸数 |", "|---|---|---|---|---|---|---|"]
    for row in payload["members"][:200]:
        lines.append(f"| {row['floor']} | {row['zone']} | {row['category']} | {row['spec']} | {row.get('section') or '-'} | {row['count']} | {row['drawing_count']} |")

    lines += ["", "## 待复核", ""]
    if payload["review"]:
        lines += ["| 类型 | 原因 |", "|---|---|"]
        for row in payload["review"][:80]:
            lines.append(f"| {row['type']} | {row['reason']} |")
    else:
        lines.append("无")
    lines += ["", f"> {payload['boundary']}", ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_csv(payload: dict[str, Any], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.writer(fh)
        writer.writerow(["table", "floor", "zone", "category", "spec", "section",
                         "diameter", "grade", "count", "drawing_count", "drawings", "samples"])
        for row in payload["members"]:
            writer.writerow(["member", row["floor"], row["zone"], row["category"], row["spec"],
                             row.get("section") or "", "", "", row["count"], row["drawing_count"],
                             "、".join(row["drawings"][:5]), ""])
        for row in payload["rebars"]:
            writer.writerow(["rebar", "", "", "", "", "", row["diameter"], row["grade"],
                             row["count"], row["drawing_count"], "、".join(row["drawings"][:5]),
                             "、".join(row["samples"][:3])])
        for row in payload["rebar_by_floor"]:
            writer.writerow(["rebar_by_floor", row["floor"], "", "", "", "", row["diameter"],
                             "、".join(row["grades"]), row["count"], row["drawing_count"],
                             "、".join(row["drawings"][:5]), ""])


# ---------------------------------------------------------------- CLI


def main() -> None:
    import pyboot
    pyboot.ensure_utf8_io()
    parser = argparse.ArgumentParser(description="跨图聚合：把多张图纸的识图候选归并成楼层/规格/型号表。")
    parser.add_argument("--inputs", nargs="+", required=True, help="*_structural.json 或 *_detail.json")
    parser.add_argument("--out", default="项目聚合.json")
    parser.add_argument("--md-out", default="")
    parser.add_argument("--csv-out", default="")
    parser.add_argument("--rules", default=str(RULES_PATH))
    parser.add_argument("--legend", default="",
                        help="rebar_grade.py 产出的「符号→牌号」映射 JSON；不给则牌号只按字面解析")
    args = parser.parse_args()

    rules = load_rules(Path(args.rules))
    legend = None
    if args.legend:
        legend = json.loads(Path(args.legend).read_text(encoding="utf-8"))
    sources: list[tuple[Path, dict[str, Any]]] = []
    for value in args.inputs:
        src = Path(value)
        if not src.exists():
            raise FileNotFoundError(src)
        sources.append((src, load_source(src, rules)))

    payload = aggregate(sources, legend=legend)
    payload = contractize_payload(payload, source=[p.name for p, _ in sources])

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    outputs = [str(out)]
    if args.md_out:
        mp = Path(args.md_out)
        mp.parent.mkdir(parents=True, exist_ok=True)
        write_markdown(payload, mp)
        outputs.append(str(mp))
    if args.csv_out:
        cp = Path(args.csv_out)
        cp.parent.mkdir(parents=True, exist_ok=True)
        write_csv(payload, cp)
        outputs.append(str(cp))
    print(json.dumps({"source_count": len(sources), "summary": payload["summary"],
                      "contract": payload["contract"]["summary"], "outputs": outputs}, ensure_ascii=False))


if __name__ == "__main__":
    main()
