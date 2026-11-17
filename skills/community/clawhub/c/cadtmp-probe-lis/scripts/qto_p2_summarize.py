#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""qto-project/v1 P2 汇总层：读 <项目目录>/算量/<专业>/*.json，生成 <项目目录>/汇总/ 汇总表。

原则：
- 只汇总不计算量：不执行专业算量算法，不把占位/候选当最终工程量。
- 状态口径：ok（有量算候选）/ pending（等专业算量）/ gap（缺识别，写缺口占位）/
  not_installed（未安装且无算量）/ missing（已装或登记 active 但缺算量输出）。
- 输出与人类可读 CSV 同路径：<key>__汇总__<date>.json + <key>__汇总__<date>.csv。
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

SKILL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_DIR / "scripts"))

from qto_project import (  # noqa: E402
    PLACEHOLDER_NOT_INSTALLED,
    QTO_SPEC,
    QTO_VERSION,
    RECOG_DIR,
    QTY_DIR,
    SUMMARY_DIR,
    SKILL_SLUGS,
    read_project_yaml,
    safe_name,
)

SUMMARY_SPEC = "qto-project/summary/v1"
SUMMARY_VERSION = "0.1.0"
STATUS_OK = "ok"
STATUS_PENDING = "pending"
STATUS_GAP = "gap"
STATUS_NOT_INSTALLED = "not_installed"
STATUS_MISSING = "missing"


def summarize_project(project_dir: Path, when: str | None = None) -> dict[str, Any]:
    project_dir = Path(project_dir)
    proj = read_project_yaml(project_dir)
    pk = proj.get("project_key") or {}
    specialties: dict[str, str] = proj.get("specialties") or {}
    qty_dir = project_dir / QTY_DIR

    per_specialty: list[dict[str, Any]] = []
    candidate_total = 0
    review_required_total = 0
    file_count = 0
    status_counts: dict[str, int] = {s: 0 for s in (STATUS_OK, STATUS_PENDING, STATUS_GAP,
                                                    STATUS_NOT_INSTALLED, STATUS_MISSING)}

    for slug in SKILL_SLUGS:
        if slug == "cad-file-reader":
            continue
        sp_dir = qty_dir / slug
        files = sorted(sp_dir.glob("*.json")) if sp_dir.is_dir() else []
        if not files:
            st = PLACEHOLDER_NOT_INSTALLED if specialties.get(slug) == PLACEHOLDER_NOT_INSTALLED else STATUS_MISSING
            per_specialty.append({"specialty": slug, "status": st, "files": 0,
                                  "files_detail": [], "candidate_count": 0,
                                  "review_required": bool(pk.get("review_required") or st == STATUS_MISSING),
                                  "note": "未在算量/ 发现输出"})
            status_counts[st] += 1
            continue

        file_rows: list[dict[str, Any]] = []
        has_ok = False
        has_pending = False
        has_gap = False
        has_not_installed = False
        for fp in files:
            file_count += 1
            try:
                data = json.loads(fp.read_text(encoding="utf-8"))
            except Exception as exc:
                file_rows.append({"file": fp.name, "status": "unreadable", "note": str(exc)})
                per_specialty.append({"specialty": slug, "status": "unreadable", "files": 1})
                status_counts.setdefault("unreadable", 0)
                status_counts["unreadable"] += 1
                continue
            placeholder = data.get("placeholder")
            ph_kind = placeholder.get("kind") if isinstance(placeholder, dict) else None
            contract = data.get("contract")
            candidates = (contract or {}).get("candidates") or []
            cand_n = len(candidates)
            candidate_total += cand_n
            rr = bool((data.get("project_key") or {}).get("review_required"))
            if rr:
                review_required_total += 1
            if ph_kind == "recognition_missing":
                st = STATUS_GAP
                has_gap = True
                note = placeholder.get("note", "缺识别")
            elif ph_kind == "quantity_pending":
                st = STATUS_PENDING
                has_pending = True
                note = placeholder.get("note", "等待专业算量")
            elif ph_kind == PLACEHOLDER_NOT_INSTALLED:
                st = STATUS_NOT_INSTALLED
                has_not_installed = True
                note = placeholder.get("note", "未安装")
            else:
                st = STATUS_OK
                has_ok = True
                note = contract.get("boundary") or "已有量算登记候选"
            file_rows.append({
                "file": fp.name,
                "status": st,
                "placeholder_kind": ph_kind,
                "candidate_count": cand_n,
                "review_required": rr,
                "source": str(data.get("contract", {}).get("source", ""))[:120],
                "note": str(note)[:200],
            })
        if has_ok:
            st = STATUS_OK
        elif has_gap:
            st = STATUS_GAP
        elif has_pending:
            st = STATUS_PENDING
        elif has_not_installed:
            st = STATUS_NOT_INSTALLED
        else:
            st = STATUS_MISSING
        status_counts[st] += 1
        per_specialty.append({
            "specialty": slug,
            "status": st,
            "files": len(files),
            "files_detail": file_rows,
            "candidate_count": sum(r["candidate_count"] for r in file_rows if "candidate_count" in r),
            "review_required": any(r.get("review_required") for r in file_rows),
            "note": "；".join(sorted({r["note"] for r in file_rows if "note" in r}))[:300],
        })

    if when is None:
        when = date.today().strftime("%Y%m%d")
    key = safe_name(pk.get("project") or pk.get("building") or "project")
    summary = {
        "schema": SUMMARY_SPEC,
        "version": SUMMARY_VERSION,
        "qto_spec": QTO_SPEC,
        "qto_version": QTO_VERSION,
        "generated_at": when,
        "project_key": pk,
        "specialties": per_specialty,
        "totals": {
            "specialty_count": len(per_specialty),
            "file_count": file_count,
            "status_counts": status_counts,
            "candidate_total": candidate_total,
            "review_required_total": review_required_total,
        },
        "boundary": "P2 汇总层：只汇总各专业登记状态/候选数与缺口，不做跨专业仲裁（P3），不生成最终工程量。",
    }
    return summary


def write_summary(project_dir: Path, summary: dict[str, Any]) -> tuple[Path, Path]:
    when = summary["generated_at"]
    pk = summary["project_key"]
    key = safe_name(pk.get("project") or pk.get("building") or "project")
    summary_dir = Path(project_dir) / SUMMARY_DIR
    summary_dir.mkdir(parents=True, exist_ok=True)
    base = summary_dir / f"{key}__汇总__{when}"
    json_path = base.with_suffix(".json")
    csv_path = base.with_suffix(".csv")

    json_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    rows = []
    for sp in summary["specialties"]:
        if sp.get("files_detail"):
            for fd in sp["files_detail"]:
                rows.append({
                    "专业": sp["specialty"],
                    "状态": fd["status"],
                    "文件": fd["file"],
                    "候选数": fd.get("candidate_count", ""),
                    "需核对": fd.get("review_required", ""),
                    "识别源": fd.get("source", ""),
                    "备注": fd.get("note", ""),
                })
        else:
            rows.append({"专业": sp["specialty"], "状态": sp["status"], "文件": "",
                         "候选数": "", "需核对": sp.get("review_required", ""),
                         "识别源": "", "备注": sp.get("note", "")})
    with csv_path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["专业", "状态", "文件", "候选数", "需核对", "识别源", "备注"])
        writer.writeheader()
        writer.writerows(rows)
    return json_path, csv_path


def main() -> int:
    import pyboot
    pyboot.ensure_utf8_io()
    ap = argparse.ArgumentParser(description="qto-project/v1 P2 汇总层（只汇总，不计算量）")
    ap.add_argument("--project-dir", required=True, help="项目目录（含 .qto/project.yaml 与 算量/）")
    ap.add_argument("--date", default=None, help="YYYYMMDD，默认今天")
    args = ap.parse_args()
    project_dir = Path(args.project_dir)
    summary = summarize_project(project_dir, when=args.date)
    json_path, csv_path = write_summary(project_dir, summary)
    print(json.dumps({
        "ok": True,
        "date": summary["generated_at"],
        "json": str(json_path),
        "csv": str(csv_path),
        "totals": summary["totals"],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
