#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cad_interpret.py — 图纸说明、规范目录与构件规则解读。

依赖 cad_scan.py 的 JSON 输出；建议先用低内存路径写出 detail JSON：

    cad_scan.sh 图纸.dwg --with-mtext --with-geom --detail-json 图纸.detail.json \
        --format json -o 图纸.scan
    cad_interpret.py --scan 图纸.scan.json --detail 图纸.detail.json --format md

该脚本只做图纸说明、标注和构件规则的识图解释；自动推断的净跨、支座或配筋
都会在输出中标明依据和复核范围，不输出体积、面积、材料量或工程量。
"""
from __future__ import annotations

import argparse
import ast
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Optional

SKILL_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = SKILL_DIR / "scripts"
VENDOR_DIR = SKILL_DIR / "vendor"
if VENDOR_DIR.exists():
    sys.path.insert(0, str(VENDOR_DIR))
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import cad_scan  # noqa: E402

DEFAULT_RULES = SKILL_DIR / "rules"


# ---------------------------------------------------------------- 文本/规范
DOC_RE = re.compile(
    r"""
    (?P<code>
      (?:
        (?:GB(?:\s*/\s*T)?|JGJ(?:\s*/\s*T)?|JG(?:\s*/\s*T)?|CJJ|JTG|CECS|DB\d{2,3}(?:/\s*T)?|T/)
        \s*[-/]?\s*\d+(?:\.\d+)?
        (?:\s*[-—]\s*\d{4})?
        (?:\s*\(\s*\d{4}\s*年版?\s*\))?
      |
        \d{2}\s*[GJS]\s*\d{2,4}(?:\s*[-—]\s*\d+(?:-\d+)?)?
      |
        \d{2}\s*J\s*\d{2,4}(?:\s*[-—]\s*\d+(?:-\d+)?)?
      |
        L\d{2}\s*[GJ]\s*\d+(?:-\d+)?
      )
    )
    """,
    re.X | re.I,
)

C_RE = re.compile(r"(?<![A-Za-z0-9])(C\d{2})(?!\d)")
COVER_RE = re.compile(r"(保护层(?:厚度)?[^。;；]{0,30}?)(\d{2,3})\s*mm", re.I)
SEISMIC_RE = re.compile(
    r"抗震(?:设防)?等级\s*[为是：:=]\s*(特一|一|二|三|四)级")
CONNECT_RE = re.compile(
    r"(?:钢筋|纵筋|受力钢筋)?(?:连接|接头)(?:方式|要求)?[^。;；]{0,12}?"
    r"(绑扎搭接|机械连接|焊接|套筒|直螺纹|挤压|搭接)")
LAP_PCT_RE = re.compile(
    r"(?:接头|搭接|连接区段)(?:面积)?(?:百分率|率)\s*[^0-9]{0,10}?(\d{1,3})%")
ADD_RE = re.compile(
    r"(?:附加|吊筋|加箍|次梁加筋)[^。;；]{0,50}")
COMPONENTS = ("梁", "柱", "板", "墙", "基础", "楼梯")
BEAM_HEAD_RE = re.compile(r"(WKL|XL|LL|JZL|JGL|TXL|KL|DL|TL|WL|ZHL|QL|L)\d{1,3}[a-f]?", re.I)


def norm_ref(value: str) -> str:
    value = (value or "").replace("\u2014", "-").replace("\u2013", "-").replace("\uff0d", "-")
    value = value.replace(" ", "").replace("\u3000", "").upper()
    value = value.replace("（", "(").replace("）", ")")
    return value


def _known_map(rules_dir: Path) -> list[dict[str, Any]]:
    known = []
    path = rules_dir / "standards.json"
    if not path.exists():
        return known
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return known
    for item in data.get("known", []):
        if isinstance(item, dict) and item.get("id"):
            item["_id_norm"] = norm_ref(item["id"])
            known.append(item)
    return known


def extract_refs(texts: Iterable[str]) -> list[dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for text in texts:
        if not text:
            continue
        for m in DOC_RE.finditer(text):
            raw = m.group("code")
            if not raw:
                continue
            code = norm_ref(raw)
            if len(code) < 4 or code.count("GB") + code.count("JGJ") > 2:
                continue
            if code.startswith(("YDB", "YKTB", "DB-", "TB-", "DB1")):
                continue
            key = code
            out.setdefault(key, {"code": code, "kind": "atlas" if re.search(r"(?i)\d[GSJ]\d|^L\d{2}[GJ]", code) else "standard",
                                 "raw": raw.strip(), "sources": set()})
            snippet = text[max(0, m.start() - 30):m.end() + 30].replace("\n", " ").strip()
            out[key]["sources"].add(snippet[:100])
    rows = []
    for item in out.values():
        item["sources"] = sorted(item["sources"])[:3]
        rows.append(item)
    return sorted(rows, key=lambda x: x["code"])


def _components_in_window(text: str, pos: int, radius: int = 45) -> list[str]:
    window = text[max(0, pos - radius):pos + radius]
    found = [c for c in COMPONENTS if c in window]
    return found or ["全部"]


def parse_profile_text(text: str) -> dict[str, list[dict[str, Any]]]:
    """从一段图纸说明中抽取可绑定构件的结构参数，不负责最终计算结论。"""
    out = {"concrete": [], "seismic": [], "cover": [], "connections": [], "lap_percent": []}
    for clause in re.split(r"[；;。\n]+", text):
        for m in C_RE.finditer(clause):
            out["concrete"].append({
                "value": m.group(1),
                "component": _components_in_window(clause, m.start()),
                "text": clause[max(0, m.start() - 35):m.end() + 35].replace("\n", " ").strip(),
            })
    for m in COVER_RE.finditer(text):
        out["cover"].append({
            "value": m.group(2),
            "component": _components_in_window(text, m.start()),
            "text": m.group(1).replace("\n", " ").strip(),
        })
    for m in SEISMIC_RE.finditer(text):
        out["seismic"].append({
            "value": m.group(1) + "级",
            "component": ["全部"],
            "text": m.group(0).replace("\n", " ").strip(),
        })
    for m in CONNECT_RE.finditer(text):
        out["connections"].append({
            "value": m.group(1),
            "component": ["全部"],
            "text": m.group(0).replace("\n", " ").strip(),
        })
    for m in LAP_PCT_RE.finditer(text):
        out["lap_percent"].append({
            "value": m.group(1) + "%",
            "component": ["全部"],
            "text": m.group(0).replace("\n", " ").strip(),
        })
    return out


def _scope_key(rec: dict[str, Any]) -> tuple:
    f = rec.get("file")
    s = rec.get("sheet")
    rot = rec.get("rotation")
    try:
        ab = int(float(rot) % 180.0 // 5.0) if rot is not None else None
    except (TypeError, ValueError):
        ab = None
    return (str(f) if f is not None else "", str(s) if s is not None else "", ab)


def collect_profiles(records: list[dict[str, Any]]) -> dict[tuple, dict[str, list[dict[str, Any]]]]:
    by_scope: dict[tuple, dict[str, list[dict[str, Any]]]] = defaultdict(
        lambda: {"concrete": [], "seismic": [], "cover": [], "connections": [], "lap_percent": []})
    for rec in records:
        text = str(rec.get("text") or "")
        if not text:
            continue
        parsed = parse_profile_text(text)
        key = _scope_key(rec)
        for kind in parsed:
            by_scope[key][kind].extend(parsed[kind])
    return by_scope


def _unique_profile(profile: dict[str, list[dict[str, Any]]], component: str) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for kind in ("concrete", "seismic", "cover", "connections", "lap_percent"):
        values = []
        for item in profile.get(kind, []):
            comps = item.get("component") or ["全部"]
            if component in comps or "全部" in comps:
                values.append(str(item["value"]))
        counts = Counter(values)
        out[kind] = [v for v, _ in counts.most_common(3)]
    return out


# ---------------------------------------------------------------- 规则
def load_rules(rules_dir: Path) -> tuple[list[dict[str, Any]], list[str]]:
    """加载 rules/ 下所有 JSON 的 beam_rules，忽略以 _ 开头的文件。"""
    rules: list[dict[str, Any]] = []
    errors: list[str] = []
    if not rules_dir.is_dir():
        return rules, [f"规则目录不存在：{rules_dir}"]
    for path in sorted(rules_dir.rglob("*.json")):
        if path.name.startswith("_"):
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            items = data.get("beam_rules", []) if isinstance(data, dict) else []
            for item in items:
                if isinstance(item, dict) and item.get("id"):
                    item["_source_file"] = str(path.relative_to(rules_dir))
                    rules.append(item)
        except Exception as exc:
            errors.append(f"{path.name}: {exc}")
    return rules, errors


_SAFE_FUNCS = {
    "max": max,
    "min": min,
    "abs": abs,
    "round": round,
    "sqrt": math.sqrt,
}


def _eval_rule_node(node: ast.AST, ns: dict[str, Any]) -> Any:
    """纯 AST 解释器：只解释白名单内节点，与 Python 语义保持一致，不执行任意代码。"""
    if isinstance(node, ast.Expression):
        return _eval_rule_node(node.body, ns)
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name):
        if node.id in _SAFE_FUNCS:
            return _SAFE_FUNCS[node.id]
        if node.id in ns:
            return ns[node.id]
        raise ValueError(f"公式使用了未知变量：{node.id}")
    if isinstance(node, ast.BinOp):
        left = _eval_rule_node(node.left, ns)
        right = _eval_rule_node(node.right, ns)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            return left / right
        if isinstance(node.op, ast.FloorDiv):
            return left // right
        if isinstance(node.op, ast.Pow):
            return left ** right
        if isinstance(node.op, ast.Mod):
            return left % right
        raise ValueError("不支持的二元运算符")
    if isinstance(node, ast.UnaryOp):
        operand = _eval_rule_node(node.operand, ns)
        if isinstance(node.op, ast.USub):
            return -operand
        if isinstance(node.op, ast.UAdd):
            return +operand
        raise ValueError("不支持的一元运算符")
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name) or node.func.id not in _SAFE_FUNCS:
            raise ValueError("公式不允许调用该函数")
        if node.keywords:
            raise ValueError("公式不允许关键字参数")
        args = [_eval_rule_node(a, ns) for a in node.args]
        return _SAFE_FUNCS[node.func.id](*args)
    if isinstance(node, ast.Compare):
        left = _eval_rule_node(node.left, ns)
        for op, comparator in zip(node.ops, node.comparators):
            right = _eval_rule_node(comparator, ns)
            if isinstance(op, ast.Eq):
                ok = left == right
            elif isinstance(op, ast.NotEq):
                ok = left != right
            elif isinstance(op, ast.Lt):
                ok = left < right
            elif isinstance(op, ast.LtE):
                ok = left <= right
            elif isinstance(op, ast.Gt):
                ok = left > right
            elif isinstance(op, ast.GtE):
                ok = left >= right
            else:
                raise ValueError("不支持的比较运算符")
            if not ok:
                return False
            left = right
        return True
    if isinstance(node, ast.BoolOp):
        if isinstance(node.op, ast.And):
            last = True
            for value in node.values:
                last = _eval_rule_node(value, ns)
                if not last:
                    return last
            return last
        if isinstance(node.op, ast.Or):
            last = False
            for value in node.values:
                last = _eval_rule_node(value, ns)
                if last:
                    return last
            return last
        raise ValueError("不支持的逻辑运算符")
    if isinstance(node, ast.IfExp):
        if _eval_rule_node(node.test, ns):
            return _eval_rule_node(node.body, ns)
        return _eval_rule_node(node.orelse, ns)
    raise ValueError(f"不支持的节点：{type(node).__name__}")


def safe_eval_expression(expr: str, namespace: dict[str, Any]) -> Any:
    """只允许算术/比较表达式的安全求值，不执行任意代码（纯 AST 解释器）。"""
    tree = ast.parse(expr, mode="eval")
    allowed = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Constant, ast.Name,
               ast.Call, ast.Load, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
               ast.Pow, ast.Mod, ast.USub, ast.UAdd, ast.Compare, ast.Eq, ast.NotEq,
               ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.BoolOp, ast.And, ast.Or, ast.IfExp)
    for node in ast.walk(tree):
        if not isinstance(node, allowed):
            raise ValueError(f"公式含不允许的语法：{type(node).__name__}")
        if isinstance(node, ast.Name) and node.id not in namespace and node.id not in _SAFE_FUNCS:
            raise ValueError(f"公式使用了未知变量：{node.id}")
    ns = dict(namespace)
    ns.update(_SAFE_FUNCS)
    return _eval_rule_node(tree, ns)


def apply_rule(rule: dict[str, Any], member: dict[str, Any], profile: dict[str, list[str]],
               overrides: dict[str, str]) -> dict[str, Any]:
    kind = rule.get("kind")
    if not rule.get("enabled", True):
        return {"rule_id": rule.get("id"), "status": "disabled"}
    if kind == "constant":
        return {
            "rule_id": rule.get("id"),
            "name": rule.get("name"),
            "value": rule.get("value_mm"),
            "unit": "mm",
            "status": "applied",
            "source": rule.get("source", ""),
            "source_page": rule.get("source_page", ""),
            "uncertainty": rule.get("uncertainty", ""),
        }
    if kind != "expression":
        return {"rule_id": rule.get("id"), "status": f"unsupported-kind:{kind}"}
    required = rule.get("required_inputs") or []
    inputs: dict[str, Any] = {}
    for key in required:
        if key == "section_h_mm":
            h = overrides.get("section_h_mm") or member.get("h")
            try:
                inputs[key] = int(h)
            except (TypeError, ValueError):
                return {"rule_id": rule.get("id"), "status": "missing-input", "missing": key}
        elif key == "seismic_level":
            value = overrides.get("seismic_level") or (profile.get("seismic") or [""])[0]
            if not value:
                return {"rule_id": rule.get("id"), "status": "missing-input", "missing": key}
            inputs[key] = value
        elif key == "concrete":
            value = overrides.get("concrete") or (profile.get("concrete") or [""])[0]
            if not value:
                return {"rule_id": rule.get("id"), "status": "missing-input", "missing": key}
            inputs[key] = value
        else:
            return {"rule_id": rule.get("id"), "status": "missing-param-def", "missing": key}
    params = rule.get("params") or {}
    for key, config in params.items():
        if key in inputs and isinstance(config, dict):
            selected = config.get(str(inputs[key]))
            if isinstance(selected, dict):
                inputs.update(selected)
    try:
        value = safe_eval_expression(rule.get("formula", ""), inputs)
    except Exception as exc:
        return {"rule_id": rule.get("id"), "status": f"formula-error:{exc}"}
    return {
        "rule_id": rule.get("id"),
        "name": rule.get("name"),
        "value": round(float(value), 1),
        "unit": "mm",
        "status": "applied",
        "formula": rule.get("formula", ""),
        "source": rule.get("source", ""),
        "source_page": rule.get("source_page", ""),
        "uncertainty": rule.get("uncertainty", ""),
    }


# ---------------------------------------------------------------- 构件解析
def _split_longitudinal(member: dict[str, Any], raw: str) -> dict[str, Any]:
    text = str(member.get("l_txt") or raw or "")
    parts = [p.strip() for p in re.split(r"[;；]", text) if p.strip()]
    first = parts[0] if parts else ""
    second = parts[1] if len(parts) > 1 else ""
    side: list[str] = []
    for m in re.finditer(r"(?<!\d)([NG])\s*(\d{1,2})\s*([ⅠⅡⅢⅣΦ\u03a6]?)\s*(\d{1,2})", text):
        side.append(f"{m.group(1)}{m.group(2)}{m.group(3)}{m.group(4)}")
    second = re.sub(r"(?<!\d)[NG]\s*\d{1,2}\s*[ⅠⅡⅢⅣΦ\u03a6]?\s*\d{1,2}", "", second).strip()
    additions = [m.group(0).strip() for m in ADD_RE.finditer(str(raw or ""))]
    return {
        "upper_or_tension_candidate": first[:180],
        "lower_candidate": second[:180],
        "side_rebar_candidate": "、".join(side) if side else "",
        "additional_rebar_text": "、".join(additions[:5]) if additions else "",
        "raw": raw[:220],
    }


def _interval_merge(items: list[list[float]]) -> list[list[float]]:
    items = sorted(items)
    out: list[list[float]] = []
    for a, b in items:
        if not out or a - out[-1][1] > 200:
            out.append([a, b])
        else:
            out[-1][1] = max(out[-1][1], b)
    return out


def infer_support_spans(segments: list[list[float]], x: float, y: float,
                        support_hits: list[dict[str, Any]]) -> dict[str, Any]:
    """按柱/墙标注中心沿梁轴线分跨，只作为支座核对候选，不冒充净跨。"""
    try:
        import numpy as np
    except Exception:
        return {"net_spans_mm": [], "support_points": [], "status": "no-numpy"}
    if not segments or not support_hits:
        return {"net_spans_mm": [], "support_points": [], "status": "no-support-data"}
    try:
        S = np.asarray(segments, float)
        if S.ndim != 2 or S.shape[1] < 4:
            return {"net_spans_mm": [], "support_points": [], "status": "bad-geometry"}
        mx = (S[:, 0] + S[:, 2]) / 2.0
        my = (S[:, 1] + S[:, 3]) / 2.0
        ang = np.degrees(np.arctan2(S[:, 3] - S[:, 1], S[:, 2] - S[:, 0])) % 180.0
        ln = np.hypot(S[:, 2] - S[:, 0], S[:, 3] - S[:, 1])
        near = np.nonzero((np.hypot(mx - x, my - y) <= 4000) & (ln > 500))[0]
        if near.size == 0:
            return {"net_spans_mm": [], "support_points": [], "status": "no-near-geometry"}
        base = near[int(np.argmax(ln[near]))]
        a0 = ang[base]
        same = near[np.abs(((ang[near] - a0 + 90.0) % 180.0) - 90.0) <= 3.0]
        ux = math.cos(math.radians(a0))
        uy = math.sin(math.radians(a0))
        intervals = []
        for i in same:
            p1 = (S[i, 0] - x) * ux + (S[i, 1] - y) * uy
            p2 = (S[i, 2] - x) * ux + (S[i, 3] - y) * uy
            intervals.append([min(p1, p2), max(p1, p2)])
        merged = _interval_merge(intervals)
        if not merged:
            return {"net_spans_mm": [], "support_points": [], "status": "no-collinear-segments"}
        best = max(merged, key=lambda z: z[1] - z[0])
        lo, hi = best
        points = []
        for h in support_hits:
            try:
                hx, hy = float(h["x"]), float(h["y"])
            except (TypeError, ValueError, KeyError):
                continue
            px = (hx - x) * ux + (hy - y) * uy
            py = abs(-(hx - x) * uy + (hy - y) * ux)
            if py <= 1800 and lo - 5000 <= px <= hi + 5000:
                points.append(round(px, 1))
        points = sorted(set(int(round(p)) for p in points))
        if len(points) < 2:
            return {"net_spans_mm": [], "support_points": points, "status": "insufficient-supports"}
        spans = [points[i + 1] - points[i] for i in range(len(points) - 1)]
        spans = [s for s in spans if s >= 500]
        if not spans:
            return {"net_spans_mm": [], "support_points": points, "status": "spans-too-short"}
        return {
            "net_spans_mm": spans,
            "support_points": points,
            "status": "column-label-center-spans [推测]",
        }
    except Exception:
        return {"net_spans_mm": [], "support_points": [], "status": "inference-error"}


def _span_input(overrides: dict[str, str], code: str) -> list[int]:
    value = overrides.get(code)
    if not value:
        return []
    out = []
    for item in str(value).split("+"):
        try:
            out.append(int(float(item)))
        except ValueError:
            continue
    return out


def _profile_for_scope(profiles: dict[tuple, dict[str, list[dict[str, Any]]]],
                       scope: tuple, component: str) -> dict[str, list[str]]:
    local = profiles.get(scope)
    if local:
        return _unique_profile(local, component)
    merged: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for p in profiles.values():
        for kind, items in p.items():
            merged[kind].extend(items)
    return _unique_profile(dict(merged), component)


def beam_rows(data: dict[str, Any], profiles: dict[tuple, dict[str, list[dict[str, Any]]]],
              rules: list[dict[str, Any]], overrides: dict[str, str]) -> list[dict[str, Any]]:
    members = (data.get("members") or {}).get("梁") or {}
    hits = data.get("hits") or []
    geom = data.get("geometry_segments") or []
    rows: list[dict[str, Any]] = []
    beam_hits = [h for h in hits if h.get("cat") == "梁"]
    support_hits = [h for h in hits if h.get("cat") in ("柱", "墙")]
    for code, d in members.items():
        raw = " ".join(d.get("raws") or [])
        related = [h for h in beam_hits if h.get("code") == code]
        file_sheet = ""
        scope: tuple = ("", "")
        if related:
            first = related[0]
            file_idx = first.get("file")
            file_sheet = "、".join(sorted({f"{h.get('file','')}/{h.get('sheet','')}" for h in related}))
            scope = (str(file_idx) if file_idx is not None else "",
                     str(first.get("sheet")) if first.get("sheet") is not None else "")
        profile = _profile_for_scope(profiles, scope, "梁")
        section_h = d.get("h") or ""
        span_mm = overrides.get("net_spans_mm")
        net_spans: list[int] = []
        span_status = "未提供净跨"
        if span_mm:
            try:
                net_spans = [int(float(v)) for v in str(span_mm).split("+") if v.strip()]
                span_status = "用户覆盖净跨"
            except ValueError:
                pass
        if not net_spans:
            net_spans = _span_input(overrides, code)
            if net_spans:
                span_status = "用户按构件覆盖净跨"
        if not net_spans and related and geom:
            for seg_file in geom:
                hit = next((h for h in related if isinstance(h.get("x"), (int, float))), None)
                if hit:
                    inference = infer_support_spans(seg_file, hit.get("x") or 0.0,
                                                    hit.get("y") or 0.0, support_hits)
                    if inference.get("net_spans_mm"):
                        net_spans = inference["net_spans_mm"]
                        span_status = inference.get("status", "自动分跨")
                        break
        span_count = ""
        cant = ""
        sm = cad_scan.SPAN.search(code)
        if sm:
            span_count = sm.group(1)
            cant = {"A": "一端悬挑", "B": "两端悬挑"}.get(sm.group(2) or "", "")
        if not span_count and d.get("span"):
            span_count = str(d["span"])
        if not cant and d.get("cant"):
            cant = d.get("cant")
        split = _split_longitudinal(d, raw)
        calc_results = []
        for rule in rules:
            if _applies(rule, code):
                calc_results.append(apply_rule(rule, d, profile, overrides))
        encrypted = next((r for r in calc_results if r.get("rule_id") == "beam-stirrup-encrypted-length"), None)
        offset = next((r for r in calc_results if r.get("rule_id") == "first-stirrup-offset"), None)
        rows.append({
            "code": code,
            "span_count": span_count,
            "cant": cant,
            "section": f"{d.get('b') or ''}x{d.get('h') or ''}",
            "section_h_mm": section_h,
            "stirrup": cad_scan.stirrup_of(d) if d.get("gd") else "",
            "concrete": "、".join(profile.get("concrete") or []),
            "seismic": "、".join(profile.get("seismic") or []),
            "cover": "、".join(profile.get("cover") or []),
            "connection": "、".join(profile.get("connections") or []),
            "lap_percent": "、".join(profile.get("lap_percent") or []),
            "net_spans_mm": net_spans,
            "span_status": span_status,
            "upper_or_tension_candidate": split["upper_or_tension_candidate"],
            "lower_candidate": split["lower_candidate"],
            "side_rebar_candidate": split["side_rebar_candidate"],
            "additional_rebar_text": split["additional_rebar_text"],
            "file_sheet": file_sheet,
            "occurrences": len(related) or 1,
            "encrypted": encrypted,
            "first_stirrup_offset_mm": offset.get("value") if offset and offset.get("status") == "applied" else "",
            "raw": raw[:220],
        })
    rows.sort(key=lambda r: (r["occurrences"] and -r["occurrences"], r["code"]))
    return rows


def beam_instances(data: dict[str, Any]) -> list[dict[str, Any]]:
    """把图面命中的梁拆成“构件实例”，同一梁编号在不同图框/坐标不再合并。"""
    files = data.get("files") or []
    labels = detect_sheet_labels(data)
    rows = []
    for h in data.get("hits") or []:
        if h.get("cat") != "梁":
            continue
        code = str(h.get("code") or "")
        raw = cad_scan.normalize(str(h.get("raw") or h.get("text") or ""))
        raw = cad_scan.clean_mtext(raw) if raw else ""
        sheet = h.get("sheet")
        file_idx = h.get("file")
        file_name = str(files[file_idx].get("name") or "") if isinstance(file_idx, int) and 0 <= file_idx < len(files) else ""
        sec = cad_scan.SEC_BH.search(raw)
        stir = cad_scan.STIRRUP.search(raw)
        spans = []
        for m in cad_scan.LONGIT_SEQ.finditer(raw):
            spans.append(re.sub(r"\s+", "", m.group(1)))
            if len(spans) >= 2:
                break
        span_count = ""
        cant = ""
        sm = cad_scan.SPAN.search(code)
        if sm:
            span_count = sm.group(1)
            cant = {"A": "一端悬挑", "B": "两端悬挑"}.get(sm.group(2) or "", "")
        x, y = h.get("x"), h.get("y")
        sheet_label = labels.get(str(sheet), "") if sheet is not None else ""
        rows.append({
            "code": code,
            "base_code": re.sub(r"\(\s*\d+\s*[AB]?\s*\)", "", code),
            "sheet": sheet,
            "sheet_label": sheet_label,
            "is_beam_plan": "梁平法施工图" in sheet_label,
            "file": file_name,
            "x": round(x, 1) if isinstance(x, (int, float)) else None,
            "y": round(y, 1) if isinstance(y, (int, float)) else None,
            "raw": raw[:260],
            "section": f"{sec.group(1)}x{sec.group(2)}" if sec else "",
            "section_h_mm": int(sec.group(2)) if sec else "",
            "stirrup": cad_scan.stirrup_of({
                "gl": stir.group(1) or "", "gd": stir.group(2), "gp": stir.group(3),
                "ga": stir.group(4) or "", "ge": stir.group(5) or "",
            }) if stir else "",
            "longitudinal_candidates": spans,
            "span_count": span_count,
            "cant": cant,
        })
    rows.sort(key=lambda r: (r["base_code"], r["sheet"] or 0, r["x"] or 0.0, r["y"] or 0.0))
    return rows


def detect_sheet_labels(data: dict[str, Any]) -> dict[str, str]:
    """从每张图的标题文字中识别梁/板/墙柱图纸名，供实例定位到楼层。"""
    patterns = [
        re.compile(r"([^。\n]{0,32}梁平法施工图)"),
        re.compile(r"([^。\n]{0,32}板结构施工图)"),
        re.compile(r"([^。\n]{0,32}墙柱平法施工图)"),
        re.compile(r"([^。\n]{0,32}(?:基础平面布置图|预制底板平面布置图|结构设计总说明))"),
        re.compile(r"([^。\n]{0,32}(?:大样图|配筋图|楼梯.*平面图))"),
    ]
    by_sheet: dict[str, list[str]] = defaultdict(list)
    for rec in data.get("text_records") or data.get("keyword_rows") or []:
        sheet = rec.get("sheet")
        if sheet is None:
            continue
        text = str(rec.get("text") or "").replace("\n", " ")
        for pat in patterns:
            m = pat.search(text)
            if m:
                label = m.group(1).strip()
                if 1 < len(label) <= 34:
                    by_sheet[str(sheet)].append(label)
                break
    labels = {}
    for sheet, candidates in by_sheet.items():
        if not candidates:
            continue
        counts: dict[str, int] = Counter()
        for c in candidates:
            counts[c] += 1
        best = min(counts, key=lambda c: (len(c), -counts[c]))
        labels[sheet] = best
    return labels


def _applies(rule: dict[str, Any], code: str) -> bool:
    applies = rule.get("applies_to") or []
    if not applies:
        return True
    head = ""
    m = BEAM_HEAD_RE.search(str(code))
    if m:
        head = m.group(1).upper()
    return any(str(x).upper() == head for x in applies)


# ---------------------------------------------------------------- 输出
def refs_rows(refs: list[dict[str, Any]], known: list[dict[str, Any]],
              covered: set[str]) -> list[list[str]]:
    rows = []
    for r in refs:
        norm = norm_ref(r["code"])
        known_item = next(
            (k for k in known if norm == k.get("_id_norm")
             or norm.startswith(k.get("_id_norm", "").split("(")[0])
             or k.get("_id_norm", "").startswith(norm)),
            None)
        base = norm.split("(")[0]
        known_norm = known_item.get("_id_norm", "") if known_item else ""
        is_covered = norm in covered or base in covered or known_norm in covered
        rows.append([
            r["code"],
            "图集" if r["kind"] == "atlas" else "规范",
            (known_item.get("name") or "") if known_item else "",
            "已覆盖" if is_covered else "待补充规则",
            "；".join(r.get("sources") or []),
        ])
    return rows


def render_md(data: dict[str, Any], refs: list[dict[str, Any]], beam: list[dict[str, Any]],
              known: list[dict[str, Any]], covered: set[str], rule_errors: list[str]) -> str:
    o = ["# CAD 图纸说明与规则解读", ""]
    if refs:
        o.append("## 图纸引用的规范/图集目录")
        o.append("")
        o.append("| 编号 | 类型 | 名称 | 规则状态 | 出处 |")
        o.append("|---|---|---|---|---|")
        for row in refs_rows(refs, known, covered):
            o.append("| " + " | ".join(str(x).replace("|", "/") if x else "-" for x in row) + " |")
        o.append("")
    else:
        o.append("## 规范/图集目录")
        o.append("")
        o.append("未从当前图纸说明中识别到规范/图集编号，可能需要 `--with-mtext` 后重跑 cad_scan。")
        o.append("")
    o.append("## 图纸说明关键参数")
    o.append("")
    rows = []
    scopes = profiles_by_scope(data)
    for key, p in sorted(scopes.items(), key=lambda x: str(x[0])):
        uni = _unique_profile(p, "梁")
        for kind, label in (("concrete", "混凝土等级"), ("seismic", "抗震等级"),
                            ("cover", "保护层"), ("connections", "钢筋连接"),
                            ("lap_percent", "接头百分率")):
            values = uni.get(kind) or []
            if values:
                rows.append([label, "、".join(values), _display_scope(data, key)])
    if rows:
        o.append("| 参数 | 识别值 | 文件/图框 |")
        o.append("|---|---|---|")
        for row in rows:
            o.append("| " + " | ".join(str(x).replace("|", "/") for x in row) + " |")
        o.append("")
    else:
        o.append("未识别到可绑定参数。")
        o.append("")
    o.append("## 梁规则计算")
    o.append("")
    o.append("净跨、支座和加密区长度按图纸/图集复核后才可用于工程算量。")
    o.append("")
    o.append("| 编号 | 混凝土 | 抗震等级 | 截面 | 箍筋 | 加密区长度mm | 首根箍筋距支座mm | 净跨mm | 净跨状态 | 附加筋原文 |")
    o.append("|---|---|---|---|---|---|---|---|---|---|")
    for row in beam:
        encrypted = row.get("encrypted") or {}
        encrypted_value = encrypted.get("value") if encrypted.get("status") == "applied" else ""
        offset_value = row.get("first_stirrup_offset_mm") or "-"
        span_txt = "+".join(str(x) for x in row.get("net_spans_mm") or [])
        o.append("| " + " | ".join([
            str(row["code"]), str(row["concrete"]) or "-", str(row["seismic"]) or "-",
            str(row["section"]) or "-",
            str(row["stirrup"]) or "-", str(encrypted_value) or "-", str(offset_value),
            span_txt or "-", str(row["span_status"]), str(row["additional_rebar_text"]) or "-",
        ]) + " |")
    o.append("")
    o.append("## 梁配筋分组与说明")
    o.append("")
    o.append("| 编号 | 上部/通长候选 | 下部候选 | 腰筋/抗扭候选 | 原文 |")
    o.append("|---|---|---|---|---|")
    for row in beam:
        o.append("| " + " | ".join([
            str(row["code"]), str(row["upper_or_tension_candidate"]) or "-",
            str(row["lower_candidate"]) or "-", str(row["side_rebar_candidate"]) or "-",
            str(row["raw"]) or "-",
        ]) + " |")
    o.append("")
    if rule_errors:
        o.append("## 规则加载提示")
        o.append("")
        o.append("、".join(rule_errors))
        o.append("")
    o.append("> 本报告中的“候选/自动/推测”内容用于核对，不替代图纸会审、翻样或结算。")
    o.append("> 规则来源页码为空时，必须先由用户补充图纸指定图集页码后再作为依据。")
    return "\n".join(o)


def profiles_by_scope(data: dict[str, Any]) -> dict[tuple, dict[str, list[dict[str, Any]]]]:
    records = data.get("text_records") or data.get("keyword_rows") or []
    return collect_profiles(records)


def _display_scope(data: dict[str, Any], key: tuple) -> str:
    file_id, sheet = key[0], key[1]
    try:
        fidx = int(file_id)
        files = data.get("files") or []
        if 0 <= fidx < len(files):
            file_id = str(files[fidx].get("name") or file_id)
    except (TypeError, ValueError):
        pass
    return f"{file_id}/图{sheet}" if sheet else file_id


def main() -> int:
    import pyboot
    pyboot.ensure_utf8_io()
    ap = argparse.ArgumentParser(description="CAD 图纸说明与规则解读")
    ap.add_argument("--scan", default=None, help="cad_scan 输出的 JSON")
    ap.add_argument("--detail", default=None, help="cad_scan --detail-json 输出")
    ap.add_argument("--rules", default=str(DEFAULT_RULES), help="规则目录，默认 rules/")
    ap.add_argument("--member", default=None, help="只输出指定梁编号")
    ap.add_argument("--format", default="md", choices=["md", "json", "csv"])
    ap.add_argument("-o", "--out", default=None)
    ap.add_argument("--seismic", default=None, help="覆盖抗震等级，如 三级")
    ap.add_argument("--concrete", default=None, help="覆盖混凝土等级，如 C35")
    ap.add_argument("--net-spans-mm", default=None,
                    help="覆盖净跨，如 5000+4200（作用于全部梁）")
    ap.add_argument("--member-net-spans", default=None,
                    help="按梁覆盖净跨，如 KL1=5000+4200,KL2=4200+4200")
    ap.add_argument("--instances-json", default=None,
                    help="额外写出按图框/坐标拆开的梁实例 JSON")
    ap.add_argument("--sheet-labels-json", default=None,
                    help="额外写出图框号到图纸名称的映射 JSON")
    args = ap.parse_args()
    if not args.scan:
        ap.error("需要 --scan cad_scan JSON")
    scan_path = Path(args.scan)
    detail_path = Path(args.detail) if args.detail else None
    try:
        data = json.loads(scan_path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"读取 --scan 失败：{exc}", file=sys.stderr)
        return 2
    if detail_path and detail_path.exists():
        try:
            detail = json.loads(detail_path.read_text(encoding="utf-8"))
            data.update(detail)
        except Exception as exc:
            print(f"读取 --detail 失败：{exc}", file=sys.stderr)
            return 2
    elif not data.get("text_records"):
        sidecar = scan_path.with_name(scan_path.stem + ".detail.json")
        if sidecar.exists():
            try:
                detail = json.loads(sidecar.read_text(encoding="utf-8"))
                data.update(detail)
            except Exception:
                pass
    overrides = {
        "net_spans_mm": args.net_spans_mm,
        "seismic_level": args.seismic,
        "concrete": args.concrete,
    }
    if args.member_net_spans:
        for pair in str(args.member_net_spans).split(","):
            if "=" in pair:
                k, v = pair.split("=", 1)
                overrides[k.strip()] = v.strip()
    rules_dir = Path(args.rules)
    rules, rule_errors = load_rules(rules_dir)
    known = _known_map(rules_dir)
    refs = extract_refs(_all_texts(data))
    covered = set()
    for item in (json.loads((rules_dir / "standards.json").read_text(encoding="utf-8"))
                 if (rules_dir / "standards.json").exists() else {}).get("covered_ids", []):
        covered.add(norm_ref(item))
    profiles = collect_profiles(data.get("text_records") or data.get("keyword_rows") or [])
    beam = beam_rows(data, profiles, rules, overrides)
    if args.member:
        beam = [r for r in beam if str(args.member).upper() in str(r["code"]).upper()]
    instances = beam_instances(data)
    if args.instances_json:
        ins_path = Path(args.instances_json)
        ins_path.write_text(json.dumps(instances, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"已写出梁实例 {ins_path}", file=sys.stderr)
    sheet_labels = detect_sheet_labels(data)
    if args.sheet_labels_json:
        labels_path = Path(args.sheet_labels_json)
        labels_path.write_text(json.dumps(sheet_labels, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"已写出图框图纸名 {labels_path}", file=sys.stderr)
    text = render_md(data, refs, beam, known, covered, rule_errors)
    if args.format == "json":
        payload = {
            "refs": refs_rows(refs, known, covered),
            "beam": beam,
            "rule_errors": rule_errors,
            "beam_instance_count": len(instances),
            "beam_instances": instances,
        }
        text = json.dumps(payload, ensure_ascii=False, indent=1)
    elif args.format == "csv":
        import csv
        import io
        buf = io.StringIO()
        w = csv.writer(buf)
        w.writerow(["编号", "截面", "抗震等级", "箍筋", "加密区长度mm", "净跨mm", "净跨状态", "附加筋原文"])
        for row in beam:
            encrypted = row.get("encrypted") or {}
            w.writerow([row["code"], row["section"], row["seismic"], row["stirrup"],
                        encrypted.get("value") if encrypted.get("status") == "applied" else "",
                        "+".join(str(x) for x in row.get("net_spans_mm") or []),
                        row["span_status"], row["additional_rebar_text"]])
        text = buf.getvalue()
    if args.out:
        out_path = Path(args.out)
        out_path.write_text(text, encoding="utf-8")
        print(f"已写出 {out_path}", file=sys.stderr)
    else:
        sys.stdout.write(text + "\n")
    return 0


def _all_texts(data: dict[str, Any]) -> list[str]:
    out: list[str] = []
    for rec in data.get("text_records") or []:
        out.append(str(rec.get("text") or ""))
    for rec in data.get("keyword_rows") or []:
        out.append(str(rec.get("text") or ""))
    for members in (data.get("members") or {}).values():
        for d in members.values():
            out.extend(str(x) for x in d.get("raws") or [])
    return out


if __name__ == "__main__":
    sys.exit(main())
