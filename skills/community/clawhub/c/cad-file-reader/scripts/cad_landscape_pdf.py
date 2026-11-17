#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PDF → 园林识图候选流水线（final_quantity=false）。

输入：
  1. PDF 文件（也可给多个文件或目录）：先调 cad_pdf_ocr.py 走本机矢量/OCR 分流，得到文字候选；
  2. 已存在的 cad_pdf_ocr 输出 JSON：直接跳过重新解析，复用其 pdf_meta/contract。

批量：多文件/目录时按“<文件茎>_detail.json”分别输出并汇总 `_batch_summary.json`；单文件沿用原 `pdf_detail.json` 命名。

说明：
  - PDF 提供“文字候选 + 坐标（矢量页）”；无图层、无块引用语义，铺装/绿地闭合域与
    块名/几何指纹为空；矢量 PDF 另输出 pdf_geometry_candidates 作 review 证据。
  - 苗木图例/系统/图纸类型按文字识别；全部 final_quantity=false，不输出苗木数量、
    铺装面积、土方量、造价或结算量。
  - --pages 可只处理部分页，兼顾大 PDF 的资源占用。
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent

def _parse_page_list(pages_arg: str | None):
    """把 --pages 1,3-5 转成一列 1-based 页码；None/空返回 None。"""
    if not pages_arg:
        return None
    wanted: list[int] = []
    for part in str(pages_arg).split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, _, b = part.partition("-")
            try:
                lo, hi = int(a), int(b)
            except ValueError:
                continue
            wanted.extend(range(lo, hi + 1))
        else:
            try:
                wanted.append(int(part))
            except ValueError:
                continue
    return sorted({int(x) for x in wanted if int(x) > 0}) or None


def _iter_inputs(raws: list[str]) -> list[Path]:
    out: list[Path] = []
    for raw in raws:
        p = Path(raw).resolve()
        if p.is_dir():
            out.extend(sorted(x for x in p.rglob("*") if x.suffix.lower() == ".pdf"))
        elif p.exists():
            out.append(p)
    # 去重保序
    seen: set[str] = set()
    dedup: list[Path] = []
    for p in out:
        key = str(p)
        if key not in seen:
            seen.add(key)
            dedup.append(p)
    return dedup


def _json_paths(out_dir: Path):
    return sorted(out_dir.glob("*.json"))


def run_pdf_ocr(pdf: Path, out_dir: Path, cache_dir: Path | None, pages: list[int] | None = None):
    out_dir.mkdir(parents=True, exist_ok=True)
    py = sys.executable
    cmd = [py, str(SCRIPT_DIR / "cad_pdf_ocr.py"), str(pdf),
           "--out-dir", str(out_dir), "--workers", "3"]
    if pages:
        cmd += ["--pages", ",".join(str(p) for p in pages)]
    if cache_dir:
        cmd += ["--cache-dir", str(cache_dir)]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        err = (proc.stderr or "").strip().splitlines()
        raise RuntimeError(" || ".join(err[-3:]) or f"cad_pdf_ocr 退出码 {proc.returncode}")
    jsons = [p for p in _json_paths(out_dir) if p.suffix == ".json"]
    if not jsons:
        raise RuntimeError("cad_pdf_ocr 未产生输出 JSON")
    # 优先取与 pdf 同名的输出；找不到则取最新生成文件
    stem_json = out_dir / f"{pdf.stem}.pdf识图.json"
    return stem_json if stem_json.exists() else max(jsons, key=lambda p: p.stat().st_mtime)


def _mid(bbox) -> tuple[float | None, float | None]:
    try:
        if not isinstance(bbox, (list, tuple)) or len(bbox) < 4:
            return None, None
        x0, y0, x1, y1 = (float(b) for b in bbox[:4])
        return (x0 + x1) / 2.0, (y0 + y1) / 2.0
    except (TypeError, ValueError):
        return None, None


def build_detail(payload: dict, src: Path, pdf_segments: list | None = None) -> dict:
    meta = payload.get("pdf_meta") or {}
    files = [{"name": src.name, "path": str(src)}]
    records: list[dict] = []
    sid = 0
    vec_items = meta.get("vector_text_items") or []
    for item in vec_items:
        text = str(item.get("text") or "").strip()
        if not text:
            continue
        try:
            x = float(item.get("x") or 0) + (float(item.get("width") or 0) / 2.0)
            y = float(item.get("y") or 0) + (float(item.get("height") or 0) / 2.0)
        except (TypeError, ValueError):
            x, y = None, None
        records.append({"kind": "TEXT", "text": text[:240], "x": x, "y": y,
                        "layer": None, "sheet": int(item.get("page") or 1),
                        "file": 0, "page": int(item.get("page") or 1), "_idx": sid})
        sid += 1
    if not records:
        # 扫描/混合页：用 OCR 文本行当候选（bbox 中心为坐标近似）
        contract = payload.get("contract") or {}
        for cand in (contract.get("candidates") or []) + (contract.get("review_candidates") or []):
            text = str(cand.get("text") or "").strip()
            if not text:
                continue
            x, y = _mid(cand.get("bbox"))
            records.append({"kind": "TEXT", "text": text[:240], "x": x, "y": y,
                            "layer": None, "sheet": int(cand.get("page_index") or 1),
                            "file": 0, "page": int(cand.get("page_index") or 1), "_idx": sid})
            sid += 1
    if pdf_segments is None:
        pdf_segments = payload.get("pdf_geometry_segments") or []
    return {
        "source_format": meta.get("source_format") or payload.get("source_format") or "pdf_unknown",
        "pdf_geometry_segments": pdf_segments,
        "files": files,
        "text_records": records,
        "layers": [],
        "meta": {
            "pdf": {
                "source_format": meta.get("source_format") or payload.get("source_format"),
                "pdf_type": meta.get("pdf_type"),
                "page_count": meta.get("page_count"),
                "vector_text_count": meta.get("vector_text_count"),
                "title_block": meta.get("title_block"),
            }
        },
        "geometry_segments": [],
        "geometry_layers": [],
        "notes": ["PDF 输入：无图层/块引用/矢量几何，铺装与绿地闭合域为空；苗木图例/系统按文字识别。"],
    }


def main() -> int:
    import pyboot
    pyboot.ensure_utf8_io()
    ap = argparse.ArgumentParser(description="PDF → 园林识图候选流水线（可多个文件/目录）")
    ap.add_argument("inputs", nargs="+", help="PDF 文件、cad_pdf_ocr 输出 JSON，或含 PDF 的目录")
    ap.add_argument("--out-dir", default="园林识图pdf", help="输出目录")
    ap.add_argument("--pdf-out-dir", default=None, help="cad_pdf_ocr 中间输出目录（默认 out-dir/_pdf）")
    ap.add_argument("--cache-dir", default=None, help="OCR 两级缓存目录")
    ap.add_argument("--pages", default=None, metavar="1,3-5", help="只处理指定 1-based 页码（逗号/连字符）；默认全部页")
    args = ap.parse_args()
    pages = _parse_page_list(args.pages)
    srcs = _iter_inputs(args.inputs)
    if not srcs:
        print(json.dumps({"error": f"没有找到可处理的 PDF/JSON: {args.inputs}"}, ensure_ascii=False, indent=2))
        return 1

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf_out = Path(args.pdf_out_dir) if args.pdf_out_dir else out_dir / "_pdf"
    multi = len(srcs) > 1
    batch: list[dict[str, Any]] = []
    had_error = False
    for src in srcs:
        try:
            if src.suffix.lower() == ".pdf":
                pdf_json = run_pdf_ocr(src, pdf_out, Path(args.cache_dir) if args.cache_dir else None, pages)
                payload = json.loads(pdf_json.read_text(encoding="utf-8"))
                pdf_segments = None
                try:
                    sys.path.insert(0, str(SCRIPT_DIR))
                    from cad_pdf_geometry import extract_geometry_segments
                    pdf_segments = extract_geometry_segments(src, pages=pages)
                except Exception as exc:  # noqa: BLE001
                    payload.setdefault("pdf_meta", {})["geometry_extract_error"] = str(exc)
                detail = build_detail(payload, src, pdf_segments)
            else:
                payload = json.loads(src.read_text(encoding="utf-8"))
                detail = build_detail(payload, src)
            stem = src.stem if multi else "pdf_detail"
            intermediate = out_dir / (f"{src.stem}_detail.json" if multi else "pdf_detail.json")
            _write_detail(intermediate, detail, out_dir, stem=stem)
            batch.append({"file": src.name, "source": str(src), "stem": src.stem, "summary": None})
        except Exception as exc:  # noqa: BLE001
            had_error = True
            print(json.dumps({"error": f"{src.name} 识别失败: {exc}"}, ensure_ascii=False))
    if multi:
        bs = out_dir / "_batch_summary.json"
        bs.write_text(json.dumps({"count": len(srcs), "ok": len(batch), "files": [b["file"] for b in batch]}, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps({"batch_summary": str(bs), "count": len(srcs), "ok": len(batch)}, ensure_ascii=False))
    return 1 if had_error else 0


def _write_detail(detail_path: Path, detail: dict, out_dir: Path, stem: str | None = None):
    sys.path.insert(0, str(SCRIPT_DIR))
    from cad_common import load_rules
    import cad_landscape_geometry as lg

    rules = load_rules(lg.RULES_PATH)
    from cad_contract import contractize_payload
    detail_path.write_text(json.dumps(detail, ensure_ascii=False, indent=2), encoding="utf-8")
    payload = contractize_payload(lg.analyze_file(detail_path, rules), source=detail_path.name)
    stem = stem or detail_path.stem
    lg.write_markdown(payload, out_dir / f"{stem}.landscape.md")
    lg.write_csv(payload, out_dir / f"{stem}.landscape.csv")
    json_out = out_dir / f"{stem}.landscape.json"
    json_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"source": str(detail_path), "summary": payload["summary"],
                      "outputs": [str(x) for x in (json_out,
                                                   out_dir / f"{stem}.landscape.md",
                                                   out_dir / f"{stem}.landscape.csv")]}, ensure_ascii=False))


if __name__ == "__main__":
    raise SystemExit(main())
