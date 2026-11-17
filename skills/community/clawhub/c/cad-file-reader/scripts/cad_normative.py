#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CAD 规范/图集辅助定位：只做资料入口、版本风险与输入缺口提示，不做合规判定。"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

SKILL_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = SKILL_DIR / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from cad_interpret import (  # noqa: E402
    _all_texts,
    _display_scope,
    collect_profiles,
    extract_refs,
    norm_ref,
)

PROFILE_LABELS = {
    "concrete": "混凝土等级",
    "seismic": "抗震等级",
    "cover": "保护层",
    "connections": "钢筋连接",
    "lap_percent": "接头百分率",
}

DISCIPLINE_REQUIREMENTS = [
    (("结构", "混凝土", "抗震", "平法", "钢筋"), ["concrete", "seismic", "cover"]),
    (("砌体", "二次结构"), ["masonry_material", "block_type", "anchorage"]),
    (("装饰", "装修", "地面", "防水", "保温", "节能", "室内环境", "防火"),
     ["finish_schedule", "fire_rating", "waterproof_grade"]),
    (("给排水", "消防", "电气", "安装"), ["systems", "sizes", "device_counts"]),
    (("工程量", "造价", "清单", "面积"), ["quantity_scope", "member_scope", "deduction_rules"]),
    (("制图",), ["drawing_scale", "layer_standard"]),
]


def _norm_id(value: Any) -> str:
    value = norm_ref(str(value or ""))
    value = value.replace("_", "/")
    return value


def _aliases(value: Any) -> set[str]:
    """生成编号别名：含斜杠、不含斜杠、去掉年版后缀。"""
    v = _norm_id(value)
    if not v:
        return set()
    base = re.sub(r"\(\d{4}\s*年版?\)$", "", v)
    out = {v, v.replace("/", ""), base, base.replace("/", "")}
    return {x for x in out if x}


def _status(item: dict[str, Any] | None) -> str:
    if not item:
        return "unknown"
    raw = str(item.get("status") or item.get("note") or "")
    if "废止" in raw:
        return "obsolete"
    if re.search(r"旧图|旧版|16G101", raw) or str(item.get("id", "")).startswith("16G101"):
        return "legacy"
    if "待确认" in raw or "待人工" in raw or not raw:
        return "unconfirmed"
    if "现行" in raw:
        return "current"
    return "unconfirmed"


def _rule_status(item: dict[str, Any] | None, covered: set[str]) -> str:
    if not item:
        return "not-indexed"
    ids = _aliases(item.get("id"))
    return "rule-covered" if ids & covered else "metadata-only"


def _requirements(discipline: str) -> list[str]:
    d = str(discipline or "")
    for keys, values in DISCIPLINE_REQUIREMENTS:
        if any(k in d for k in keys):
            return values
    return []


def _profile_summary(data: dict[str, Any]) -> tuple[dict[str, list[str]], list[dict[str, Any]], list[dict[str, Any]]]:
    records = data.get("text_records") or data.get("keyword_rows") or []
    scopes = collect_profiles(records)
    values: dict[str, list[str]] = defaultdict(list)
    evidences: list[dict[str, Any]] = []
    for key, profile in sorted(scopes.items(), key=lambda x: str(x[0])):
        for kind, label in PROFILE_LABELS.items():
            seen: set[str] = set()
            for item in profile.get(kind, []):
                value = str(item.get("value") or "")
                if value and value not in seen:
                    seen.add(value)
                    values[label].append(value)
                    evidences.append({
                        "parameter": label,
                        "value": value,
                        "scope": _display_scope(data, key),
                        "evidence": str(item.get("text") or "")[:180],
                    })
    ordered = {label: sorted(set(v)) for label, v in values.items()}
    conflicts = []
    for label, vals in ordered.items():
        if len(vals) > 1:
            conflicts.append({
                "parameter": label,
                "values": vals,
                "risk": "不同图框/构件/说明可能口径不同，需绑定部位后复核",
            })
    return ordered, conflicts, evidences


def _missing_requirements(items: list[dict[str, Any]], profile: dict[str, list[str]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for item in items:
        for key in _requirements(str(item.get("discipline") or "")):
            row = (str(item.get("id") or ""), key)
            if row in seen:
                continue
            seen.add(row)
            label = PROFILE_LABELS.get(key, key)
            if label not in profile or not profile[label]:
                out.append({
                    "standard_id": item.get("id") or "",
                    "input": key,
                    "label": label,
                    "source": item.get("name") or "",
                })
    return out


def build_payload(data: dict[str, Any], standards_path: Path) -> dict[str, Any]:
    standards_config: dict[str, Any] = {}
    if standards_path.exists():
        standards_config = json.loads(standards_path.read_text(encoding="utf-8"))
    known_raw = standards_config.get("known", [])
    known: list[dict[str, Any]] = []
    by_alias: dict[str, dict[str, Any]] = {}
    for item in known_raw:
        row = dict(item)
        row.setdefault("entry", "kb-metadata")
        row["entry_note"] = "知识库仅保存元数据/授权入口，不保存全文"
        known.append(row)
        aliases = _aliases(row.get("id"))
        for alias in row.get("aliases", []):
            aliases |= _aliases(alias)
        for alias in aliases:
            by_alias.setdefault(alias, row)

    refs = extract_refs(_all_texts(data))
    covered: set[str] = set()
    for value in standards_config.get("covered_ids", []):
        covered |= _aliases(value)
    profile, conflicts, evidences = _profile_summary(data)
    rows: list[dict[str, Any]] = []
    matched_items: list[dict[str, Any]] = []
    for ref in refs:
        ref_ids = _aliases(ref.get("code"))
        item = next((by_alias[x] for x in ref_ids if x in by_alias), None)
        status = _status(item)
        rule_status = _rule_status(item, covered)
        if item:
            matched_items.append(item)
        rows.append({
            "ref": ref.get("code"),
            "matched": bool(item),
            "standard_id": item.get("id") if item else ref.get("code"),
            "name": item.get("name") if item else "",
            "kind": item.get("kind") if item else ("atlas" if re.search(r"(?i)\d[GSJ]\d|^L\d{2}[GJ]", str(ref.get("code", ""))) else "standard"),
            "discipline": item.get("discipline") if item else "",
            "status": status,
            "rule_status": rule_status,
            "entry": item.get("entry") if item else "",
            "kb_path": item.get("kb_path") if item else "",
            "source_url": item.get("source_url") if item else "",
            "evidence": (ref.get("sources") or [])[:2],
            "action": (
                "人工核对编号/名称/现行版本，并补充索引" if not item else
                "按授权入口核对原文；只引用元数据，不复制全文"
            ),
        })

    missing = _missing_requirements(matched_items, profile)
    counts = {k: sum(1 for r in rows if r["status"] == k)
              for k in ("current", "legacy", "unconfirmed", "obsolete", "unknown")}
    counts["indexed_refs"] = sum(1 for r in rows if r["matched"])
    counts["unindexed_refs"] = sum(1 for r in rows if not r["matched"])
    payload = {
        "schema": "cad-normative-assist/v1",
        "boundary": "仅定位规范/图集元数据、版本风险和缺少的设计输入；不输出条文符合性结论。",
        "summary": {
            "ref_count": len(rows),
            **counts,
            "conflict_count": len(conflicts),
            "missing_input_count": len(missing),
        },
        "refs": rows,
        "profile": profile,
        "profile_evidence": evidences[:120],
        "conflicts": conflicts,
        "missing_inputs": missing,
        "knowledge_base": standards_config.get("knowledge_base", {}),
    }
    return payload


def render_md(payload: dict[str, Any]) -> str:
    o = ["# CAD 规范/图集辅助核查", "", payload["boundary"], ""]
    s = payload["summary"]
    o += ["## 汇总", "",
          f"- 引用编号：{s['ref_count']}；已索引：{s['indexed_refs']}；未索引：{s['unindexed_refs']}",
          f"- 版本状态：现行 {s['current']} / 旧版 {s['legacy']} / 待确认 {s['unconfirmed']} / 废止 {s['obsolete']} / 未识别 {s['unknown']}",
          f"- 口径冲突：{s['conflict_count']}；缺输入：{s['missing_input_count']}", ""]
    o += ["## 引用清单", "",
          "| 编号 | 状态 | 类型 | 专业 | 名称 | 资料入口 | 动作 |", "|---|---|---|---|---|---|---|"]
    for r in payload["refs"]:
        entry = r.get("kb_path") or r.get("source_url") or "-"
        o.append(f"| {r['ref']} | {r['status']} | {r['kind']} | {r['discipline'] or '-'} | "
                 f"{r['name'] or '-'} | {entry} | {r['action']} |")
    o += ["", "## 图纸参数候选", ""]
    if payload["profile"]:
        o += ["| 参数 | 候选值 |", "|---|---|"]
        for k, v in payload["profile"].items():
            o.append(f"| {k} | {'、'.join(v)} |")
    else:
        o.append("未识别到结构说明参数；可用 `cad_scan --with-mtext` 重跑。")
    if payload["conflicts"]:
        o += ["", "## 需分部位绑定", ""]
        for r in payload["conflicts"]:
            o.append(f"- {r['parameter']}：{'、'.join(r['values'])}；{r['risk']}")
    if payload["missing_inputs"]:
        o += ["", "## 缺少的设计输入", ""]
        for r in payload["missing_inputs"]:
            o.append(f"- {r['standard_id']} / {r['label']}（{r['source']}）")
    o += ["", "> 本报告不判定合规；条文适用性以图纸指定版本和正式授权全文为准。"]
    return "\n".join(o)


def render_csv(payload: dict[str, Any]) -> str:
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["编号", "匹配", "状态", "类型", "专业", "名称", "资料入口", "动作"])
    for r in payload["refs"]:
        w.writerow([r["ref"], r["matched"], r["status"], r["kind"], r["discipline"],
                    r["name"], r.get("kb_path") or r.get("source_url") or "", r["action"]])
    return buf.getvalue()


def main() -> int:
    import pyboot
    pyboot.ensure_utf8_io()
    ap = argparse.ArgumentParser(description="CAD 规范/图集元数据与输入缺口核查")
    ap.add_argument("--scan", required=True, help="cad_scan 输出的 JSON")
    ap.add_argument("--detail", help="cad_scan --detail-json 输出")
    ap.add_argument("--rules", default=str(SKILL_DIR / "rules"))
    ap.add_argument("--format", default="md", choices=["md", "json", "csv", "all"])
    ap.add_argument("-o", "--out", help="输出前缀；不传则输出到 stdout")
    args = ap.parse_args()
    scan_path = Path(args.scan)
    data = json.loads(scan_path.read_text(encoding="utf-8"))
    detail_path = Path(args.detail) if args.detail else scan_path.with_name(scan_path.stem + ".detail.json")
    if args.detail or (detail_path.exists() and not data.get("text_records")):
        if detail_path.exists():
            data.update(json.loads(detail_path.read_text(encoding="utf-8")))
    payload = build_payload(data, Path(args.rules) / "standards.json")
    if args.out:
        prefix = Path(args.out)
        if args.format in ("md", "all"):
            prefix.with_suffix(".md").write_text(render_md(payload), encoding="utf-8")
        if args.format in ("json", "all"):
            prefix.with_suffix(".json").write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
        if args.format in ("csv", "all"):
            prefix.with_suffix(".csv").write_text(render_csv(payload), encoding="utf-8")
        print(f"已写出规范辅助核查：{prefix}", file=sys.stderr)
        return 0
    if args.format == "json":
        sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=1) + "\n")
    elif args.format == "csv":
        sys.stdout.write(render_csv(payload) + "\n")
    else:
        sys.stdout.write(render_md(payload) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
