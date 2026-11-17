#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P1 算量联动适配器：从 <项目目录>/识别/<专业> 读底座识图，写 <项目目录>/算量/<专业>/。

原则：
- 优先读底座 cad-file-reader 识别结果；缺识别结果给缺口清单，不自行解析大 DWG。
- 输出文件名含 project_key_safe + 专业 slug + 日期版本。
- 不执行任何专业算量算法；若已有该专业的量算结果 JSON，可经 --quantity 附着为
  quantity 层参考（仍标 review_required/final_quantity=false，不上报结算量）。
- 单专业安装即可独立使用；多专业并存时只写自己的专业目录。
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

SKILL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_DIR / "scripts"))

from qto_project import (  # noqa: E402
    QTO_SPEC,
    QTO_VERSION,
    LEGACY_SPEC,
    RECOG_DIR,
    QTY_DIR,
    SKILL_SLUGS,
    DRAFT_TYPES,
    default_project_key,
    read_project_yaml,
    safe_name,
)

P1_GAP_KIND = "recognition_missing"
P1_PENDING_KIND = "quantity_pending"


def _pick_recognition(project_dir: Path, specialty: str) -> tuple[Path | None, list[str]]:
    d = project_dir / RECOG_DIR / specialty
    gap: list[str] = []
    if not d.is_dir():
        gap.append(f"缺少识别目录 识别/{specialty}/")
        return None, gap
    files = sorted(d.glob("*.json"))
    if not files:
        gap.append(f"识别/{specialty}/ 下没有 JSON 识别结果")
        return None, gap
    return files[0], gap


def build_p1_payload(source_recognition: str | None, quantity_source: str | None,
                     specialist_slug: str, project_key: dict[str, Any],
                     draft_type: str, placeholder: dict[str, Any] | None,
                     quantity_meta: str = "") -> dict[str, Any]:
    contract = {
        "schema": LEGACY_SPEC,
        "source": source_recognition or "",
        "origin_schema": "qto-p1-link/v1",
        "summary": {"total": 0, "confirmed_evidence": 0, "inferred_candidate": 0,
                    "review_required": 0, "candidate_count": 0, "duplicate_candidate": 0},
        "review_reasons": [],
        "candidates": [],
        "review_candidates": [],
        "boundary": "P1 算量联动适配层：只登记输入/输出与缺口，不执行算量算法、不输出最终工程量。",
    }
    if quantity_source and Path(quantity_source).is_file():
        src = Path(quantity_source).read_text(encoding="utf-8")
        try:
            q = json.loads(src)
            contract = {
                "schema": LEGACY_SPEC,
                "source": source_recognition or "",
                "origin_schema": "qto-p1-link/v1",
                "summary": {"total": 1, "confirmed_evidence": 0, "inferred_candidate": 1,
                            "review_required": 0, "candidate_count": 1, "duplicate_candidate": 0},
                "review_reasons": [],
                "candidates": [{
                    "id": f"p1-qty-{safe_name(specialist_slug)}-1",
                    "kind": "measurement",
                    "value": None,
                    "unit": None,
                    "layer": None,
                    "block_name": None,
                    "text": quantity_meta or "P1 算量输出登记",
                    "bbox": None,
                    "evidence": [{"source": str(q.get("source_file", ""))[:80]}],
                    "method": "qto-p1-link/adapter",
                    "confidence": 0.5,
                    "confidence_tier": "inferred_candidate",
                    "review_reasons": [],
                    "review_notes": "P1 联动层登记；专业量仍需在算量 skill 内完成扣减/做法/损耗后人工核对",
                    "source_schema": LEGACY_SPEC,
                    "source_id": Path(quantity_source).name,
                    "final_quantity": False,
                }],
                "review_candidates": [],
                "boundary": "P1 量算层：只登记来源，不替代该专业既有算法。",
            }
        except Exception as exc:
            placeholder = {"kind": P1_PENDING_KIND, "note": f"--quantity 内容不是合法 JSON：{exc}"}
    payload = {
        "qto_spec": QTO_SPEC,
        "qto_version": QTO_VERSION,
        "project_key": project_key,
        "specialty": specialist_slug,
        "draft_type": draft_type if draft_type in DRAFT_TYPES else "draft_type_pending",
        "producer": {"skill": "cad-file-reader", "role": "link-p1-adapter"},
        "qto_p1": {"layer": "quantity", "steps": [
            "读 识别/<专业>/ 底座识图候选",
            "有既有量算结果用 --quantity 附着",
            "缺识别结果写缺口清单（不解析大 DWG）",
            "输出写 算量/<专业>/<key>__<专业>__<日期>.json",
        ]},
        "placeholder": None,
        "contract": contract,
    }
    if placeholder is not None:
        payload["placeholder"] = placeholder
    if quantity_source:
        payload["quantity_source"] = str(quantity_source)
    return payload


def output_path(project_dir: Path, specialty: str, project_key: dict[str, Any],
                when: str | None = None) -> Path:
    if when is None:
        when = date.today().strftime("%Y%m%d")
    key = safe_name(project_key.get("building") or project_key.get("project") or "project")
    return project_dir / QTY_DIR / specialty / f"{key}__{specialty}__{when}.json"


def run(project_dir: Path, specialty: str, draft_type: str = "draft_type_pending",
        quantity: str | None = None, when: str | None = None,
        note: str = "") -> dict[str, Any]:
    project_dir = Path(project_dir)
    proj = read_project_yaml(project_dir)
    pk = proj.get("project_key") or {}
    base_project = pk.get("project") or ""
    building = pk.get("building") or ""
    source = pk.get("source") or "file"
    pkey = default_project_key(base_project, specialty, building=building,
                               source=source, review_required=True)
    recog, gaps = _pick_recognition(project_dir, specialty)
    recog_path = str(recog.relative_to(project_dir)) if recog else ""
    placeholder = None
    status = "ok"
    if not recog:
        placeholder = {"kind": P1_GAP_KIND, "note": "缺识别结果：" + "；".join(gaps)}
        status = "gap"
    elif not quantity:
        placeholder = {"kind": P1_PENDING_KIND,
                       "note": note or "已读到识别结果，但未提供 --quantity 既有算量输出；P1 仅登记，等待专业算量执行。"}
        status = "pending"
    payload = build_p1_payload(recog_path, quantity, specialty, pkey, draft_type, placeholder,
                               quantity_meta=note)
    out = output_path(project_dir, specialty, pkey, when=when)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return {
        # 缺口/待专业量算均为正常状态：写入占位/登记文件，不阻断体系（CLI rc=0）。
        "ok": True,
        "status": status,
        "out": str(out),
        "specialty": specialty,
        "recognition_input": recog_path,
        "recognition_gaps": gaps,
        "quantity_source": quantity,
        "review_required": pkey["review_required"],
    }


def main() -> int:
    import pyboot
    pyboot.ensure_utf8_io()
    ap = argparse.ArgumentParser(description="P1 算量联动适配器（底座 cad-file-reader）")
    ap.add_argument("--project-dir", required=True)
    ap.add_argument("--specialty", required=True, choices=SKILL_SLUGS,
                    help="量算专业正式 slug（不含底座 cad-file-reader）")
    ap.add_argument("--draft-type", default="draft_type_pending")
    ap.add_argument("--quantity", help="可选：该专业已有的量算结果 JSON 路径")
    ap.add_argument("--date", default=None, help="YYYYMMDD，默认今天")
    ap.add_argument("--note", default="", help="附加说明（缺口清单/复核理由）")
    args = ap.parse_args()
    if args.specialty == "cad-file-reader":
        print("❌ 底座 cad-file-reader 不写算量层；请选择四个量算专业 slug", file=sys.stderr)
        return 2
    result = run(Path(args.project_dir), args.specialty, draft_type=args.draft_type,
                 quantity=args.quantity, when=args.date, note=args.note)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
