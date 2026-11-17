#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从图纸说明表反解「钢筋符号 → 牌号」，让「各型号钢筋量」能报出 HRB400 而不是 unknown。

问题与数据事实
--------------
结构图的配筋标注通常只写符号不写字面牌号：`%%13225`（= 三级钢 Φ25）。而 `project_aggregate`
的 `parse_rebar` 只认字面 `HRB400`，于是所有钢筋的 `grade` 恒为 `unknown`，
只能报「Φ25 共 2720 处」，报不出「HRB400 Φ25」——对不上料表。

但牌号就在图里，在「结构设计总说明」的钢筋材料表：

    钢筋：采用 HPB300钢筋（\\ue530）fy=270N/mm²；HRB400钢筋（\\ue532）fy=360N/mm²。

符号没有丢失，而是以 CAD 字体的私有区字符（U+E530 一带）保留在 text_records 里。
所以这件事不是「猜」，是**把图纸自己写的对照表读出来**。

两套编码与桥接
--------------
- 说明表里用私有区字符：`\\ue532`
- 标注里用 AutoCAD 转义：`%%132`

两者尾号相同（`0xE532 & 0xF == 2`，`%%13` 后也是 `2`）。实测 721 条标注文本里
`\\ue53225` 与 `%%13225` 出现在同一句（同一构件的不同钢筋），可作等价佐证。

但尾号对应终究是**编码规律**而非本图说明表的直接陈述，因此分两层：

    direct   0.92   本批图纸说明表直接给出「符号 → 牌号」，可进 confirmed_evidence
    bridged  0.85   按尾号从 direct 外推，只进 inferred_candidate，且必须写明依据

红线
----
- **没有本批说明表就一律 unknown**，绝不套国标默认值（不同项目图例可能自定义）。
- 映射只在传入的这批图纸内生效，不跨项目串用。
- 同一符号出现两个牌号 → 标 ambiguous 并排除，不挑一个凑数。
- 输出不含任何工程量字段，`final_quantity` 恒 false。

用法
----
    python3 rebar_grade.py --inputs <*_detail.json / *structural.json ...> --out legend.json
    python3 rebar_grade.py --inputs ... --out legend.json --md-out legend.md
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

SCHEMA = "cad-rebar-legend/v1"
CLEARANCE = "本表为图纸牌号映射提取结果，非工程量，不可直接用于结算"

# 说明表直接证据：符号与牌号在图纸自己的文字里成对出现
CONF_DIRECT = 0.92
# 尾号桥接：属于编码规律外推，不给到确认档
CONF_BRIDGED = 0.85

# 私有区钢筋符号段（tssdeng.shx / hztxt.shx 等把 %%13x 映射到这里）
PRIVATE_BASE = 0xE530
PRIVATE_SPAN = 16

SYM_PAT = r"(?:[\ue000-\uf8ff]|%%13[0-3])"

# 模式 A：牌号在前，符号在紧跟的括号里 —— `HRB400钢筋（\ue532）` / `HPB300(%%130)`
PAIR_A = re.compile(
    r"(HPB|HRB|RRB|CRB)\s*(\d{3})\s*([Ee])?\s*(?:级)?\s*(?:钢筋|钢)?\s*[（(]\s*(" + SYM_PAT + r")\s*[）)]"
)
# 模式 B：符号在前，破折号/连字符后跟牌号 —— `\ue531—HPB300-270N/mm2` / `\ue532-HRB400(fy=360)`
PAIR_B = re.compile(
    r"(" + SYM_PAT + r")\s*[—–\-－]\s*(HPB|HRB|RRB|CRB)\s*(\d{3})\s*([Ee])?"
)

ANY_SYM = re.compile(SYM_PAT)


# ---------------------------------------------------------------- 符号与尾号

def drawing_key(name: str) -> str:
    """把产物文件名归一到图纸名，用于校验「映射是否来自同一批图纸」。

    `X_detail.json`、`X_detail.structural.json`、`X_scan.json` 都应归到 `X`。
    """
    stem = Path(str(name or "")).stem
    # 先剥点分形式（s1b 产物是 X_detail.structural.json），再剥下划线形式
    for suffix in (".structural", ".detail", ".scan"):
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]
    for suffix in ("_detail", "_structural", "_scan"):
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]
    if stem in ("detail", "structural", "scan"):
        parent = Path(str(name or "")).parent.name
        for suffix in ("_detail", "_structural", "_scan"):
            if parent.endswith(suffix):
                parent = parent[: -len(suffix)]
        stem = parent or stem
    return stem


def symbol_label(sym: str) -> str:
    """把符号转成稳定标识：私有区字符用 U+XXXX，转义保持原样。"""
    if len(sym) == 1 and 0xE000 <= ord(sym) <= 0xF8FF:
        return f"U+{ord(sym):04X}"
    return sym


def symbol_kind(sym: str) -> str:
    if len(sym) == 1 and 0xE000 <= ord(sym) <= 0xF8FF:
        return "private"
    return "escape"


def symbol_tail(sym: str) -> str | None:
    """取符号的尾号，用于把 %%13x 与私有区 \\ue53x 对上。取不到返回 None。

    只认可信区段：私有区限 U+E530~U+E53F（CAD 字体约定的钢筋符号段），
    转义只认 %%130~%%133。超出这两段的字符不参与桥接——宁可 unknown 也不乱配。
    """
    if len(sym) == 1 and 0xE000 <= ord(sym) <= 0xF8FF:
        code = ord(sym)
        if PRIVATE_BASE <= code < PRIVATE_BASE + PRIVATE_SPAN:
            return str(code & 0xF)
        return None
    m = re.fullmatch(r"%%13([0-3])", sym, re.I)
    if m:
        return m.group(1)
    return None


# ---------------------------------------------------------------- 说明表解析

def _grade_name(prefix: str, digits: str, seismic: str | None) -> str:
    return f"{prefix.upper()}{digits}{(seismic or '').upper()}"


def extract_pairs(text: str) -> list[tuple[str, str]]:
    """从一条文本里抽出 (符号, 牌号) 对。只认严格模式，不做就近猜测。"""
    out: list[tuple[str, str]] = []
    for m in PAIR_A.finditer(text or ""):
        out.append((m.group(4), _grade_name(m.group(1), m.group(2), m.group(3))))
    for m in PAIR_B.finditer(text or ""):
        out.append((m.group(1), _grade_name(m.group(2), m.group(3), m.group(4))))
    return out


def _iter_texts(payload: dict[str, Any]) -> Iterable[dict[str, Any]]:
    """产物里的文本记录：detail 有 text_records；structural 的候选里带 evidence。"""
    for rec in (payload.get("text_records") or []):
        if isinstance(rec, dict) and rec.get("text"):
            yield rec
    for key in ("members", "rebars", "nodes"):
        for item in (payload.get(key) or []):
            if not isinstance(item, dict):
                continue
            for ev in (item.get("evidence") or []):
                if isinstance(ev, dict) and ev.get("text"):
                    yield ev


def collect(sources: list[tuple[str, dict[str, Any]]]) -> dict[str, Any]:
    """扫一批产物，收集「符号→牌号」证据并聚合成映射表。

    sources: [(展示名, payload), ...]；只在传进来的这批里找，不跨项目。
    """
    observed: dict[str, list[dict[str, Any]]] = {}
    drawings: set[str] = set()
    text_seen = 0
    for name, payload in sources:
        key = drawing_key(payload.get("source_file") or name)
        drawings.add(key)
        for rec in _iter_texts(payload):
            text_seen += 1
            text = rec.get("text") or ""
            for sym, grade in extract_pairs(text):
                label = symbol_label(sym)
                observed.setdefault(label, []).append({
                    "symbol": sym,
                    "symbol_kind": symbol_kind(sym),
                    "tail": symbol_tail(sym),
                    "grade": grade,
                    "source": name,
                    "file": rec.get("file_name") or rec.get("file") or payload.get("source_file") or "",
                    "text": text[:200],
                })
    return {"observed": observed, "texts_scanned": text_seen, "drawings": drawings}


def build_legend(collected: dict[str, Any]) -> dict[str, Any]:
    """把观察到的配对整理成映射表：一致则采纳，冲突则标 ambiguous 并排除。"""
    mapping: list[dict[str, Any]] = []
    ambiguous: list[dict[str, Any]] = []
    for label, hits in sorted(collected["observed"].items()):
        grades = sorted({h["grade"] for h in hits})
        first = hits[0]
        if len(grades) > 1:
            ambiguous.append({
                "symbol": first["symbol"], "symbol_label": label,
                "grades": grades, "occurrences": len(hits),
                "reason": "同一符号在本批图纸里对应多个牌号，不猜",
                "sources": sorted({h["source"] for h in hits}),
            })
            continue
        mapping.append({
            "symbol": first["symbol"], "symbol_label": label,
            "symbol_kind": first["symbol_kind"], "tail": first["tail"],
            "grade": grades[0], "basis": "direct", "confidence": CONF_DIRECT,
            "occurrences": len(hits),
            "evidence": {
                "source": first["source"], "file": first["file"], "text": first["text"],
            },
            "sources": sorted({h["source"] for h in hits}),
        })

    by_tail: dict[str, str] = {}
    tail_conflict: list[dict[str, Any]] = []
    for item in mapping:
        tail, grade = item.get("tail"), item["grade"]
        if tail is None:
            continue
        if tail in by_tail and by_tail[tail] != grade:
            tail_conflict.append({"tail": tail, "grades": sorted({by_tail[tail], grade})})
            by_tail.pop(tail, None)  # 冲突尾号不参与桥接
            continue
        by_tail[tail] = grade

    return {"mapping": mapping, "ambiguous": ambiguous, "by_tail": by_tail,
            "tail_conflict": tail_conflict}


def add_bridges(legend: dict[str, Any]) -> dict[str, Any]:
    """按尾号为缺失的符号补 bridged 条目。已 direct 的符号不覆盖。"""
    have = {m["symbol"] for m in legend["mapping"]}
    have_label = {m["symbol_label"] for m in legend["mapping"]}
    bridges: list[dict[str, Any]] = []
    for tail, grade in sorted(legend["by_tail"].items()):
        for sym, kind in ((f"%%13{tail}", "escape"), (chr(PRIVATE_BASE + int(tail)), "private")):
            label = symbol_label(sym)
            if label in have_label:
                continue  # 已有直接证据，不降级覆盖
            bridges.append({
                "symbol": sym, "symbol_label": label, "symbol_kind": kind, "tail": tail,
                "grade": grade, "basis": "bridged", "confidence": CONF_BRIDGED,
                "evidence": {
                    "reason": "按 CAD 字体尾号对应外推（%%13x 与 U+E53x 同尾号），非本图说明表直接陈述",
                    "from_direct_tail": tail,
                },
            })
            have.add(sym)
    legend["mapping"].extend(bridges)
    legend["bridges"] = bridges
    return legend


def build(sources: list[tuple[str, dict[str, Any]]]) -> dict[str, Any]:
    collected = collect(sources)
    legend = build_legend(collected)
    legend = add_bridges(legend)
    legend.update({
        "schema": SCHEMA,
        "clearance": CLEARANCE,
        "source_count": len(sources),
        "texts_scanned": collected["texts_scanned"],
        "source_drawings": sorted(collected["drawings"]),
        "contract": {"final_quantity": False},
        "boundary": [
            "映射只来自本批图纸的说明表；本批没有说明表就全部 unknown，不套国标默认值。",
            "bridged 是按编码尾号外推的，不是本图说明表写的，只到 inferred_candidate。",
            "同符号多牌号一律记 ambiguous 并排除，不挑一个凑数。",
        ],
    })
    return legend


# ---------------------------------------------------------------- 应用到标注

def resolve_grade(spec: str, legend: dict[str, Any]) -> tuple[str, str, float]:
    """给一条配筋标注解析牌号。返回 (牌号, 依据, 置信度)；解不出返回 ("unknown","none",0.0)。"""
    text = (spec or "").upper()
    index = {m["symbol"]: m for m in legend.get("mapping") or []}
    found: list[tuple[str, str, float]] = []
    for m in ANY_SYM.finditer(text):
        sym = m.group(0)
        hit = index.get(sym)
        if not hit:
            # 大小写差异（%%13x 可能被 upper 过）
            hit = next((v for k, v in index.items() if k.upper() == sym), None)
        if hit:
            found.append((hit["grade"], hit["basis"], hit["confidence"]))
    if not found:
        return ("unknown", "none", 0.0)
    grades = {f[0] for f in found}
    if len(grades) == 1:
        # 同一标注多个符号牌号一致：取最高依据
        best = max(found, key=lambda f: f[2])
        return best
    # 一条标注里出现不同牌号的符号（如主筋+箍筋混写），不猜，交回 unknown
    return ("unknown", "mixed", 0.0)


def apply_to_payload(payload: dict[str, Any], legend: dict[str, Any]) -> dict[str, int]:
    """就地回填 payload 里 rebars 的 grade。返回统计。"""
    stat = {"total": 0, "resolved": 0, "unknown": 0, "mixed": 0}
    for item in (payload.get("rebars") or []):
        if not isinstance(item, dict):
            continue
        stat["total"] += 1
        spec = item.get("rebar_spec") or item.get("raw") or ""
        grade, basis, conf = resolve_grade(spec, legend)
        if grade == "unknown":
            item["rebar_grade"] = "unknown"
            item["rebar_grade_basis"] = basis
            stat["mixed" if basis == "mixed" else "unknown"] += 1
            continue
        item["rebar_grade"] = grade
        item["rebar_grade_basis"] = basis
        item["rebar_grade_confidence"] = conf
        item["rebar_grade_evidence"] = next(
            ({"source": m.get("evidence", {}).get("source"),
              "text": m.get("evidence", {}).get("text")}
             for m in legend.get("mapping") or []
             if m["grade"] == grade and m["basis"] == basis), None)
        stat["resolved"] += 1
    return stat


# ---------------------------------------------------------------- 展示

def write_markdown(legend: dict[str, Any], path: Path) -> None:
    lines = ["# 钢筋符号 → 牌号映射（从图纸说明表反解）", "", f"> {CLEARANCE}", ""]
    lines.append(f"- 扫描产物：{legend['source_count']} 份 / 文本记录 {legend['texts_scanned']} 条")
    direct = [m for m in legend["mapping"] if m["basis"] == "direct"]
    bridged = [m for m in legend["mapping"] if m["basis"] == "bridged"]
    lines.append(f"- 直接证据 {len(direct)} 条 / 尾号外推 {len(bridged)} 条 / 冲突 {len(legend['ambiguous'])} 条")
    lines.append("")
    if direct:
        lines += ["## 直接证据（本批说明表原文）", "",
                  "| 符号 | 牌号 | 次数 | 依据原文 |", "|---|---|---|---|"]
        for m in direct:
            text = (m["evidence"].get("text") or "").replace("|", "\\|")[:70]
            lines.append(f"| `{m['symbol_label']}` | **{m['grade']}** | {m['occurrences']} | {text} |")
        lines.append("")
    if bridged:
        lines += ["## 尾号外推（非本图直接陈述，仅到 inferred_candidate）", "",
                  "| 符号 | 牌号 | 依据 |", "|---|---|---|"]
        for m in bridged:
            lines.append(f"| `{m['symbol_label']}` | {m['grade']} | 与尾号 {m['tail']} 的直接证据同尾号 |")
        lines.append("")
    if legend["ambiguous"]:
        lines += ["## 未采用（同符号多牌号）", ""]
        for a in legend["ambiguous"]:
            lines.append(f"- `{a['symbol_label']}`：{' / '.join(a['grades'])}（{a['reason']}）")
        lines.append("")
    if not direct:
        lines += ["> 本批图纸没有可识别的说明表，牌号全部保持 unknown。这是如实结果，不是缺陷。", ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def load_payload(path: Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser(description="从图纸说明表反解钢筋符号→牌号")
    ap.add_argument("--inputs", nargs="+", required=True, help="*_detail.json 或 *_structural.json")
    ap.add_argument("--out", required=True, help="映射表 JSON 输出")
    ap.add_argument("--md-out", help="映射表 Markdown 输出")
    args = ap.parse_args()

    sources: list[tuple[str, dict[str, Any]]] = []
    for raw in args.inputs:
        p = Path(raw)
        try:
            sources.append((p.name, load_payload(p)))
        except Exception as exc:
            print(f"跳过 {p.name}：{exc}", file=sys.stderr)
    legend = build(sources)
    Path(args.out).write_text(json.dumps(legend, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.md_out:
        write_markdown(legend, Path(args.md_out))
    direct = sum(1 for m in legend["mapping"] if m["basis"] == "direct")
    print(f"完成：{args.out}（直接证据 {direct} 条 / 外推 {len(legend['bridges'])} 条 / 冲突 {len(legend['ambiguous'])} 条）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
