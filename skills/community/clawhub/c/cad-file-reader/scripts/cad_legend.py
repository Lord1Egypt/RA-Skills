#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""轻量图例匹配候选（P0）：按规则词库匹配块名/图层/文字，输出 legend_matches 候选。

只输出识图候选与证据，不输出工程量和图例未覆盖结论。
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Any

from cad_common import compact, file_name, load_rules
from cad_contract import contractize_payload

SCHEMA = "cad-file-reader-legends/v1"
RULES_PATH = Path(__file__).resolve().parents[1] / "rules" / "legends.json"


def _tokens(text: Any) -> str:
    return compact(text).upper()


def match_legend(value: str, legends: list[dict[str, Any]]) -> tuple[str, str, float, str]:
    """返回 (discipline, semantic, confidence, matched_token)。短代号按边界匹配。"""
    upper = _tokens(value)
    best: tuple[str, str, float, str] = ("unknown", "", 0.0, "")
    for legend in legends:
        conf_base = float(legend.get("confidence_base") or 0.8)
        for token in legend.get("tokens") or []:
            tok = str(token).upper()
            if re.fullmatch(r"[A-Z]{1,6}", tok):
                hit = f" {upper} ".find(f" {tok} ") >= 0
            else:
                hit = tok in upper
            if hit and conf_base > best[2]:
                best = (legend.get("discipline") or "", legend.get("semantic") or "", conf_base, tok)
    return best


def match_symbol(value: str, symbols: list[dict[str, Any]]) -> tuple[str, str, float, str]:
    """块/符号名按别名指纹匹配。短代号按边界匹配，中文别名按子串匹配。"""
    upper = _tokens(value)
    best: tuple[str, str, float, str] = ("unknown", "", 0.0, "")
    for sym in symbols:
        conf_base = float(sym.get("confidence_base") or 0.82)
        for alias in sym.get("aliases") or []:
            al = str(alias).upper()
            if re.fullmatch(r"[A-Za-z0-9_]{3,}", al):
                hit = f" {upper} ".find(f" {al} ") >= 0
            else:
                hit = al in upper
            if hit and conf_base > best[2]:
                best = (sym.get("discipline") or "", sym.get("semantic") or "", conf_base, al)
    return best


def collect_candidates(data: dict[str, Any], legends: list[dict[str, Any]], max_matches: int, symbols: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    seen: set[str] = set()
    # 1) 块引用名（INSERT）
    blocks = data.get("meta") or {}
    block_refs = blocks.get("block_refs") or {}
    for name, count in (block_refs.items() if isinstance(block_refs, dict) else []):
        discipline, semantic, confidence, matched = match_symbol(name, symbols or [])
        method = "legend_symbol_fingerprint"
        basis = "legend_symbol_alias"
        if discipline == "unknown":
            discipline, semantic, confidence, matched = match_legend(name, legends)
            method = "legend_block_match"
            basis = "legend_block_name"
        if discipline == "unknown":
            continue
        key = f"block:{name}"
        if key in seen:
            continue
        seen.add(key)
        out.append({
            "id": key, "kind": "text", "text": name, "layer": None, "block_name": name,
            "discipline": discipline, "semantic": semantic, "matched_token": matched,
            "instance_count": int(count or 0), "confidence": round(confidence, 4),
            "status": "candidate",
            "review_reasons": [], "review_reason": "",
            "evidence": [{"kind": "block_name", "value": name, "matched_token": matched, "instance_count": int(count or 0)}],
            "method": method,
            "discipline_refs": [{"discipline": discipline, "semantic": semantic, "basis": basis}],
        })
        if len(out) >= max_matches:
            return out
    # 2) 图层名
    for layer in data.get("layers") or []:
        if not isinstance(layer, str):
            continue
        discipline, semantic, confidence, matched = match_legend(layer, legends)
        if discipline == "unknown":
            continue
        key = f"layer:{layer}"
        if key in seen:
            continue
        seen.add(key)
        out.append({
            "id": key, "kind": "text", "text": layer, "layer": layer, "block_name": None,
            "discipline": discipline, "semantic": semantic, "matched_token": matched,
            "instance_count": 0, "confidence": round(confidence, 4),
            "status": "candidate",
            "review_reasons": [], "review_reason": "",
            "evidence": [{"kind": "layer_name", "value": layer, "matched_token": matched}],
            "method": "legend_layer_match",
            "discipline_refs": [{"discipline": discipline, "semantic": semantic, "basis": "legend_layer_name"}],
        })
        if len(out) >= max_matches:
            return out
    # 3) 文字内容（图例表/注释）
    for rec in data.get("text_records") or []:
        if not isinstance(rec, dict):
            continue
        text = compact(rec.get("text", ""))
        if not text:
            continue
        discipline, semantic, confidence, matched = match_legend(text, legends)
        if discipline == "unknown":
            continue
        layer = compact(rec.get("layer"))
        block_key = f"block:{text}"
        if block_key in seen:
            continue  # 同名块引用已由符号指纹/块名路径覆盖，文字路径不再重复
        key = f"text:{text}:{layer}"
        if key in seen:
            continue
        seen.add(key)
        out.append({
            "id": key, "kind": "text", "text": text, "layer": layer or None, "block_name": None,
            "discipline": discipline, "semantic": semantic, "matched_token": matched,
            "instance_count": 0, "confidence": round(confidence, 4),
            "status": "candidate",
            "review_reasons": [], "review_reason": "",
            "evidence": [{"kind": "text_content", "value": text[:120], "matched_token": matched, "file": file_name(data, rec.get("file"))}],
            "method": "legend_text_match",
            "discipline_refs": [{"discipline": discipline, "semantic": semantic, "basis": "legend_text_content"}],
        })
        if len(out) >= max_matches:
            return out
    return out


def analyze_file(path: Path, max_matches: int) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    rules = load_rules(RULES_PATH) if RULES_PATH.exists() else {}
    legends = rules.get("legends") or []
    symbols = rules.get("symbols") or []
    matches = collect_candidates(data, legends, max_matches, symbols)
    summary = {
        "source_text_records": len(data.get("text_records") or []),
        "legend_matches": len(matches),
        "legend_matches_truncated": len(matches) == max_matches and len(matches) > 0,
    }
    payload: dict[str, Any] = {
        "schema": SCHEMA,
        "source_file": path.name,
        "summary": summary,
        "legend_matches": matches,
        "boundary": "只输出图例匹配候选；不输出工程量、材料量、造价或结算量。",
    }
    return contractize_payload(payload, source=path.name)


def write_markdown(payload: dict[str, Any], path: Path) -> None:
    lines = [
        "# 图例知识表候选", "",
        f"- 源文件：`{payload['source_file']}`",
        f"- 图例候选 {len(payload['legend_matches'])}；需复核 {payload['contract']['summary']['review_required']}",
        "", "> 本文件只输出图例匹配候选，不输出工程量。", "",
    ]
    for row in payload["legend_matches"]:
        lines.append(f"- [{row['discipline']}/{row['semantic']}] `{row['text']}` 命中 `{row['matched_token']}` 置信度 {row['confidence']}")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_csv(payload: dict[str, Any], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.writer(fh)
        writer.writerow(["id", "discipline", "semantic", "text", "layer", "block_name", "matched_token", "confidence", "method"])
        for row in payload["legend_matches"]:
            writer.writerow([row.get("id"), row.get("discipline"), row.get("semantic"), row.get("text"), row.get("layer"), row.get("block_name"), row.get("matched_token"), row.get("confidence"), row.get("method")])


def main() -> int:
    import pyboot
    pyboot.ensure_utf8_io()
    parser = argparse.ArgumentParser(description="按图例词库匹配识别工程图例候选。")
    parser.add_argument("inputs", nargs="+", help="cad_scan 生成的 --detail-json 文件")
    parser.add_argument("--out-dir", default="图例识图")
    parser.add_argument("--max-matches", type=int, default=2000)
    args = parser.parse_args()
    if args.max_matches <= 0:
        parser.error("--max-matches 必须大于 0")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    outputs = 0
    for value in args.inputs:
        src = Path(value)
        if not src.exists():
            raise FileNotFoundError(src)
        payload = analyze_file(src, args.max_matches)
        json_path = out_dir / f"{src.stem}.legends.json"
        md_path = out_dir / f"{src.stem}.legends.md"
        csv_path = out_dir / f"{src.stem}.legends.csv"
        json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        write_markdown(payload, md_path)
        write_csv(payload, csv_path)
        print(json.dumps({"source": str(src), "summary": payload["summary"], "outputs": [str(json_path), str(md_path), str(csv_path)]}, ensure_ascii=False))
        outputs += 1
    return 0 if outputs else 4


if __name__ == "__main__":
    raise SystemExit(main())
