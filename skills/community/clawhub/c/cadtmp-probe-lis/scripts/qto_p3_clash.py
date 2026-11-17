#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""qto-project/v1 P3 跨专业交叉核对：只读识别/算量登记，输出“同部位多专业是否齐/缺口/需人工核对”清单。

原则：
- 不计算量：不做跨专业量值仲裁，不生成最终工程量。
- 按 project_key 的 (building, floor, zone) 或文件名前缀聚合“部位”。
- 同部位 ≥2 专业有算量登记 → 形成 cross_check 行，提示需人工交叉核对。
- 专业登记 active/recognized 但算量层缺输出 → missing 信号。
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
import re
from datetime import date
from pathlib import Path
from typing import Any

SKILL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_DIR / "scripts"))

from qto_project import (  # noqa: E402
    PLACEHOLDER_NOT_INSTALLED,
    QTO_SPEC,
    QTO_VERSION,
    QTY_DIR,
    SUMMARY_DIR,
    SKILL_SLUGS,
    read_project_yaml,
    safe_name,
)

CLASH_SPEC = "qto-project/clash/v1"
CLASH_VERSION = "0.1.0"
FILENAME_KEY_RE = re.compile(r"^(?P<key>.+)__(?P<slug>[a-zA-Z0-9][a-zA-Z0-9-]*)__(?P<date>\d{8})\.json$")


def _pluck_room(data: dict[str, Any], filename: str) -> str:
    pk = data.get("project_key")
    if isinstance(pk, dict):
        bits = [str(pk.get(k) or "").strip() for k in ("building", "floor", "zone")]
        if any(bits):
            key = "/".join(b for b in bits if b) or "未绑定部位"
            return key
    m = FILENAME_KEY_RE.match(filename)
    if m:
        return m.group("key") or "未绑定部位"
    return "未绑定部位"


def clash_project(project_dir: Path, when: str | None = None) -> dict[str, Any]:
    project_dir = Path(project_dir)
    proj = read_project_yaml(project_dir)
    pk = proj.get("project_key") or {}
    specialties_reg: dict[str, str] = proj.get("specialties") or {}
    qty_dir = project_dir / QTY_DIR

    rows: list[dict[str, Any]] = []
    room_map: dict[str, list[str]] = {}
    file_count = 0
    candidate_total = 0
    review_required_total = 0
    status_counts: dict[str, int] = {}

    for slug in SKILL_SLUGS:
        if slug == "cad-file-reader":
            continue
        sp_dir = qty_dir / slug
        files = sorted(sp_dir.glob("*.json")) if sp_dir.is_dir() else []
        if not files:
            st = PLACEHOLDER_NOT_INSTALLED if specialties_reg.get(slug) == PLACEHOLDER_NOT_INSTALLED else "missing"
            status_counts[st] = status_counts.get(st, 0) + 1
            rows.append({"specialty": slug, "status": st, "files": 0, "room": "",
                         "candidate_count": 0, "review_required": bool(pk.get("review_required") or st == "missing"),
                         "note": "算量/ 未发现输出"})
            continue
        for fp in files:
            file_count += 1
            try:
                data = json.loads(fp.read_text(encoding="utf-8"))
            except Exception as exc:
                rows.append({"specialty": slug, "status": "unreadable", "files": 1, "room": "",
                             "candidate_count": 0, "review_required": True, "note": str(exc)})
                status_counts["unreadable"] = status_counts.get("unreadable", 0) + 1
                continue
            placeholder = data.get("placeholder")
            ph_kind = placeholder.get("kind") if isinstance(placeholder, dict) else None
            if ph_kind == "recognition_missing":
                st = "gap"
            elif ph_kind == "quantity_pending":
                st = "pending"
            elif ph_kind == PLACEHOLDER_NOT_INSTALLED:
                st = PLACEHOLDER_NOT_INSTALLED
            else:
                st = "ok"
            status_counts[st] = status_counts.get(st, 0) + 1
            room = _pluck_room(data, fp.name)
            room_map.setdefault(room, []).append(slug)
            contract = data.get("contract") or {}
            cand_n = len(contract.get("candidates") or [])
            candidate_total += cand_n
            rr = bool((data.get("project_key") or {}).get("review_required"))
            if rr:
                review_required_total += 1
            rows.append({
                "specialty": slug, "status": st, "files": 1, "room": room,
                "file": fp.name, "candidate_count": cand_n, "review_required": rr,
                "note": (placeholder.get("note") if isinstance(placeholder, dict) else (contract.get("boundary") or ""))[:200],
            })

    cross_checks: list[dict[str, Any]] = []
    for room, specs in sorted(room_map.items()):
        uniq = sorted(set(specs))
        if len(uniq) >= 2:
            cross_checks.append({
                "room": room,
                "specialties": uniq,
                "specialty_count": len(uniq),
                "note": "同部位多专业均有算量登记，需按图纸交叉核对（不仲裁量值，建议各专业先各自复核）",
            })
        elif room and not room.startswith("未绑定"):
            cross_checks.append({
                "room": room,
                "specialties": uniq,
                "specialty_count": 1,
                "note": "单专业有算量登记；若其它专业应有该部位输出而未出现，视为覆盖缺口",
            })

    if when is None:
        when = date.today().strftime("%Y%m%d")
    key = safe_name(pk.get("project") or pk.get("building") or "project")
    return {
        "schema": CLASH_SPEC,
        "version": CLASH_VERSION,
        "qto_spec": QTO_SPEC,
        "qto_version": QTO_VERSION,
        "generated_at": when,
        "project_key": pk,
        "specialties": rows,
        "cross_checks": cross_checks,
        "totals": {
            "file_count": file_count,
            "status_counts": status_counts,
            "candidate_total": candidate_total,
            "review_required_total": review_required_total,
            "multi_specialty_rooms": sum(1 for c in cross_checks if c["specialty_count"] >= 2),
        },
        "boundary": "P3 交叉核对层：只按部位/状态提示多专业同部位、缺口与需人工核对，不生成最终工程量。",
    }


def write_clash(project_dir: Path, clash: dict[str, Any]) -> tuple[Path, Path]:
    when = clash["generated_at"]
    pk = clash["project_key"]
    key = safe_name(pk.get("project") or pk.get("building") or "project")
    out_dir = Path(project_dir) / SUMMARY_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    base = out_dir / f"{key}__交叉核对__{when}"
    json_path = base.with_suffix(".json")
    csv_path = base.with_suffix(".csv")
    json_path.write_text(json.dumps(clash, ensure_ascii=False, indent=2), encoding="utf-8")
    with csv_path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["专业", "状态", "文件", "部位", "候选数", "需核对", "备注"])
        writer.writeheader()
        for sp in clash["specialties"]:
            writer.writerow({
                "专业": sp.get("specialty", ""), "状态": sp.get("status", ""),
                "文件": sp.get("file", ""), "部位": sp.get("room", ""),
                "候选数": sp.get("candidate_count", ""), "需核对": sp.get("review_required", ""),
                "备注": sp.get("note", ""),
            })
    return json_path, csv_path


def main() -> int:
    import pyboot
    pyboot.ensure_utf8_io()
    ap = argparse.ArgumentParser(description="qto-project/v1 P3 跨专业交叉核对（只读汇总，不计算量）")
    ap.add_argument("--project-dir", required=True)
    ap.add_argument("--date", default=None, help="YYYYMMDD，默认今天")
    args = ap.parse_args()
    clash = clash_project(Path(args.project_dir), when=args.date)
    j, c = write_clash(Path(args.project_dir), clash)
    print(json.dumps({"ok": True, "json": str(j), "csv": str(c),
                      "totals": clash["totals"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
