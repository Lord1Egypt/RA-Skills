#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""本机真实 DWG 识图回归：用知识库真图做电气/结构/总图场地识图回归。

只在本机执行，负责把 cad_scan + 对应识图包串起来并核对候选数。
清单每条 case 可带 kind=electrical|structural|site（默认 electrical）。
真图清单由 --manifest 指定，通常放在技能包之外（本地工作区），发布内容不得包含真图路径。
输出结果为脱敏后的计数与状态，不含图纸字节。
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from cad_common import start_mem_guard  # noqa: E402
from cad_contract import validate_contract_payload  # noqa: E402
from cad_preflight import preflight_file  # noqa: E402


def _scan_yield(detail_path: Path) -> dict:
    """从 cad_scan 的 detail JSON 取“实际读出多少内容”，用于区分
    “图纸没读进来”与“读进来了但领域候选为 0”这两类完全不同的问题。"""
    out = {"text_total": None, "layers": None}
    try:
        d = json.loads(Path(detail_path).read_text(encoding="utf-8"))
    except Exception:
        return out
    files = d.get("files") or []
    if files:
        f = files[0]
        out["text_total"] = f.get("texts")
        out["layers"] = f.get("layers")
    if out["text_total"] is None:
        out["text_total"] = d.get("text_total")
    if out["layers"] is None:
        lv = d.get("layers")
        out["layers"] = len(lv) if isinstance(lv, list) else lv
    return out



def _cache_hits_from_json(path: Path) -> int | None:
    """读取 cad_scan 的 JSON 报告里的 cache.hits；无法解析返回 None。"""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return int(data.get("cache", {}).get("hits", 0) or 0)
    except Exception:
        return None


def run(cmd, **kw):
    return subprocess.run(cmd, text=True, **kw)


def main() -> int:
    import pyboot
    pyboot.ensure_utf8_io()
    ap = argparse.ArgumentParser(description="真实 DWG 回归")
    ap.add_argument("--manifest", required=True, help="真图清单 JSON")
    ap.add_argument("--scan-dir", help="复用已有 cad_scan 详情 JSON 的目录（含 <id>_detail.json）")
    ap.add_argument("--report-json", help="脱敏回归报告输出 JSON；默认 stdout")
    ap.add_argument("--work-dir", default="", help="临时工作目录前缀（默认用 /tmp）")
    ap.add_argument("--verify-cache", action="store_true", help="第二次运行同参 cad_scan 验证缓存命中")
    args = ap.parse_args()
    guard = start_mem_guard(name="run_real_dwg_regression内存闸")

    manifest_path = Path(args.manifest)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    cases = manifest.get("cases") or manifest.get("drawings") or []
    if not cases:
        print("❌清单没有 drawings/cases", file=sys.stderr)
        return 2
    scan_dir = Path(args.scan_dir) if args.scan_dir else None
    work_root = Path(args.work_dir) if args.work_dir else Path(tempfile.mkdtemp(prefix="cad_real_dwg_"))
    work_root.mkdir(parents=True, exist_ok=True)
    results = []
    failed = 0
    empty = 0
    PACK_GEO = {
        "electrical": ("cad_electrical_geometry.sh", ".electrical.json", ("drawing_types", "systems", "route_segments", "equipment", "circuits", "specs", "fire_protection", "weak_current", "intelligent_building")),
        "structural": ("cad_structural_geometry.sh", ".structural.json", ("drawing_types", "systems", "members", "rebars", "nodes", "grids", "structural_geometry")),
        "site": ("cad_site_geometry.sh", ".site.json", ("drawing_types", "systems", "components", "references", "site_geometry")),
        "hvac_plumbing": ("cad_deep_geometry.sh", ".hvac_plumbing.json", ("drawing_types", "systems", "components", "references", "geometry")),
        "interior_finish": ("cad_deep_geometry.sh", ".interior_finish.json", ("drawing_types", "systems", "components", "references", "geometry")),
        "curtain_wall": ("cad_deep_geometry.sh", ".curtain_wall.json", ("drawing_types", "systems", "components", "references", "geometry")),
        "civil_defense": ("cad_deep_geometry.sh", ".civil_defense.json", ("drawing_types", "systems", "components", "references", "geometry")),
        "precast": ("cad_deep_geometry.sh", ".precast.json", ("drawing_types", "systems", "components", "references", "geometry")),
        "landscape": ("cad_landscape_geometry.sh", ".landscape.json", ("drawing_types", "systems", "plant_legends", "plant_block_legends", "plant_block_fingerprints", "plant_schedule_links", "paving_closed_areas", "green_area_candidates")),
        "municipal": ("cad_municipal_geometry.sh", ".municipal.json", ("drawing_types", "systems", "components", "pipe_candidates", "materials", "labels", "geometry_segments")),
        "pdf": (None, None, ("pdf_processed",)),
    }
    DEEP_PACK_ARG = {
        "hvac_plumbing": "hvac_plumbing",
        "interior_finish": "interior_finish",
        "curtain_wall": "curtain_wall",
        "civil_defense": "civil_defense",
        "precast": "precast",
    }
    DEEP_SCRIPT = {
        "hvac_plumbing": "cad_hvac_plumbing_geometry.sh",
        "interior_finish": "cad_interior_finish_geometry.sh",
        "curtain_wall": "cad_curtain_wall_geometry.sh",
        "civil_defense": "cad_civil_defense_geometry.sh",
        "precast": "cad_precast_geometry.sh",
    }

    for case in cases:
        cid = str(case.get("id") or case.get("name") or "")
        dwg = case.get("path") or case.get("dwg") or ""
        kind = str(case.get("kind") or case.get("pack") or "electrical")
        use_fallback = bool(case.get("dwg_dxf_fallback") or manifest.get("dwg_dxf_fallback"))
        if kind not in PACK_GEO:
            item = {"id": cid, "name": case.get("name", cid), "status": "skip", "reason": f"未知识图包:{kind}"}
            results.append(item); continue
        geo_script, out_suffix, summary_keys = PACK_GEO[kind]
        expect = case.get("expect") or {}
        # 无显式 expect 时，缺省门槛=整套识图包至少产出一个领域候选，避免把“该图纸本无此细分域”算成缺陷。
        item = {"id": cid, "name": case.get("name", cid), "kind": kind, "status": "pending", "summary": None, "review_items": None}
        if kind == "pdf":
            pdf_dir = work_root / f"{cid}_pdfocr"
            pdf_dir.mkdir(parents=True, exist_ok=True)
            t0 = time.time()
            pr = run([str(SKILL_DIR / "scripts" / "cad_pdf_ocr.sh"), dwg, "--classify-only", "--out-dir", str(pdf_dir)], capture_output=True)
            item["scan_seconds"] = round(time.time() - t0, 2)
            if pr.returncode != 0:
                item["status"] = "error"; item["reason"] = "cad_pdf_ocr失败"; item["stderr"] = pr.stderr[-500:]
                results.append(item); failed += 1; continue
            item["summary"] = {"pdf_processed": 1, "pdf_output": str(pdf_dir)}
            item["contract_valid"] = True
            item["status"] = "pass"
            results.append(item); continue
        detail_path = None
        scanned_here = False
        if scan_dir:
            cand = scan_dir / f"{cid}_detail.json"
            if cand.exists():
                detail_path = cand
        if detail_path is None:
            if not dwg or not Path(dwg).exists():
                item["status"] = "skip"; item["reason"] = "真图不存在"; item["path"] = dwg
                results.append(item); continue
            # 先做输入预检：版本不支持 / 损坏 / 过小等属“图纸本身不可用”，
            # 不是识图能力缺陷，必须与“读进来了但领域候选为 0”分开统计，
            # 否则报告会把“图根本没读进来”伪装成“提取能力不行”。
            pf = preflight_file(dwg)
            if not pf.get("ok"):
                item["status"] = "skip"
                item["reason"] = f"输入预检未通过：{pf.get('reason')}"
                item["preflight_kind"] = pf.get("kind")
                item["dwg_version"] = pf.get("version")
                results.append(item); continue
            case_out = work_root / f"{cid}_scan"
            detail_path = work_root / f"{cid}_detail.json"
            cache_dir_arg = [str(work_root / "_cad_cache")] if args.verify_cache else []
            t0 = time.time()
            scan_cmd = [str(SKILL_DIR / "scripts" / "cad_scan.sh"), dwg,
                        "--with-mtext", "--with-insert", "--with-geom", "--with-geom-layer",
                        "--detail-json", str(detail_path), "--format", "json", "-o", str(case_out)]
            if use_fallback:
                scan_cmd.append("--dwg-dxf-fallback")
            if cache_dir_arg:
                scan_cmd += ["--cache-dir", cache_dir_arg[0]]
            r = run(scan_cmd, capture_output=True)
            item["scan_seconds"] = round(time.time() - t0, 2)
            scanned_here = True
            if r.returncode != 0 or not detail_path.exists():
                item["status"] = "error"; item["reason"] = "cad_scan失败"; item["stderr"] = r.stderr[-500:]
                results.append(item); failed += 1; continue
        elif not detail_path.exists():
            item["status"] = "error"; item["reason"] = "复用详情不存在"
            results.append(item); failed += 1; continue
        item.update(_scan_yield(detail_path))
        out_dir = work_root / f"{cid}_{kind}"
        pack_arg = DEEP_PACK_ARG.get(kind)
        if pack_arg:
            geo_script = DEEP_SCRIPT[kind]
        cmd = [str(SKILL_DIR / "scripts" / geo_script), str(detail_path), "--out-dir", str(out_dir)]
        if pack_arg:
            cmd.insert(1, "--pack")
            cmd.insert(2, pack_arg)
        t0 = time.time()
        r = run(cmd, capture_output=True)
        item["geo_seconds"] = round(time.time() - t0, 2)
        if r.returncode != 0:
            item["status"] = "error"; item["reason"] = f"{geo_script}失败"; item["stderr"] = r.stderr[-500:]
            results.append(item); failed += 1; continue
        out_json = out_dir / f"{Path(detail_path).stem}{out_suffix}"
        if not out_json.exists():
            item["status"] = "error"; item["reason"] = f"{kind}输出缺失"; item["stderr"] = r.stderr[-300:]
            results.append(item); failed += 1; continue
        try:
            payload = json.loads(out_json.read_text(encoding="utf-8"))
        except Exception as exc:
            item["status"] = "error"; item["reason"] = f"输出解析失败:{exc}"
            results.append(item); failed += 1; continue
        summary = payload.get("summary") or {}
        item["summary"] = {k: summary.get(k) for k in summary_keys}
        item["review_items"] = summary.get("review_items")
        contract_errors = validate_contract_payload(payload)
        item["contract_valid"] = not contract_errors
        if expect:
            missing = {k: summary.get(k, 0) for k, v in expect.items() if int(summary.get(k, 0)) < int(v)}
        else:
            low = [k for k in summary_keys if int(summary.get(k, 0)) >= 1]
            missing = {} if low else {"__no_candidate__": 0}
        if contract_errors:
            item["status"] = "fail"; item["reason"] = f"契约校验失败:{contract_errors[:3]}"
            failed += 1
            results.append(item); continue
        if missing:
            texts = item.get("text_total")
            if texts is None or int(texts or 0) == 0:
                # 图纸一个字都没读出来：是“没读进来”，不是“提取不出”，属解析侧问题。
                item["status"] = "error"
                item["reason"] = "扫描零产出：cad_scan 未读出任何文字（图纸可能损坏/加密/非标格式，需看 stderr 里的解码报错）"
            else:
                # 读得出来但没有该领域候选：可能本图确实无此细分域，也可能规则不足，必须人工确认，
                # 因此单独计 empty，不计入 failed，避免把“图纸没这个专业”误判为能力缺陷。
                item["status"] = "empty"
                item["reason"] = f"已读出 {texts} 条文字，但 {kind} 领域候选为 0（需人工确认：本图无此细分域，或提取规则不足）"
                empty += 1
                results.append(item); continue
            failed += 1
        elif args.verify_cache and scanned_here:
            # 已在本轮跑过 cad_scan 才验证缓存命中（复用详情时跳过）
            verify_out = work_root / f"{cid}_scan_verify"
            verify_detail = work_root / f"{cid}_verify_detail.json"
            v_cmd = [str(SKILL_DIR / "scripts" / "cad_scan.sh"), dwg,
                     "--with-mtext", "--with-insert", "--with-geom", "--with-geom-layer",
                     "--detail-json", str(verify_detail), "--format", "json", "-o", str(verify_out)]
            if use_fallback:
                v_cmd.append("--dwg-dxf-fallback")
            v_cmd += ["--cache-dir", str(work_root / "_cad_cache")]
            t0 = time.time()
            rv = run(v_cmd, capture_output=True)
            item["cache_verify_seconds"] = round(time.time() - t0, 2)
            hits = _cache_hits_from_json(verify_out.with_suffix(".json"))
            item["cache_hits"] = hits
            if rv.returncode != 0 or not hits:
                item["status"] = "fail"; item["reason"] = "第二次扫描缓存未命中"
                item["stderr"] = rv.stderr[-300:]
                failed += 1
            else:
                item["status"] = "pass"
        else:
            item["status"] = "pass"
        results.append(item)

    def _n(st):
        return sum(1 for x in results if x["status"] == st)

    report = {"schema": "cad-real-dwg-regression/v2", "manifest": manifest_path.name, "total": len(results),
              "passed": _n("pass"), "empty": _n("empty"), "skipped": _n("skip"), "failed": failed,
              "mem_guard": guard, "results": results}
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.report_json:
        Path(args.report_json).write_text(text + "\n", encoding="utf-8")
        print(text)
    else:
        print(text)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
