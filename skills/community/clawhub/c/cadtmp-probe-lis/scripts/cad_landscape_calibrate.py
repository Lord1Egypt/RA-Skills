#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""设计院图例校准工具：把新设计院图纸详情转成可复用的块名→植物分类 + 植物名词扩展。

用法：
  scripts/cad_scan.sh 某设计院图.dwg --with-mtext --with-insert --with-blocks --detail-json 校准输入.json --format json -o 扫描
  scripts/cad_landscape_calibrate.sh 校准输入.json --institute 某设计院 --out-dir 校准输出
  # 同时把明确可自动写入的植物名扩进该院词库并一键复验：
  scripts/cad_landscape_calibrate.sh 校准输入.json --institute 某设计院 --write-override --write-text-words --verify

不输出算量；产物是 plant_block_aliases 覆盖与植物词列表扩展，供 cad_landscape_geometry.sh --institute <名> 使用。
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from cad_common import compact
from cad_landscape_geometry import (
    INSTITUTE_DIR,
    load_rules,
    plant_classify,
    plant_classify_by_block,
    plant_coverage_audit,
    read_records,
)

_TEXT_SUFFIX_RULES = (
    (("乔木", 0.80), ("树", "杉", "柏", "松", "楠", "桂", "樟", "榆", "桐", "杨", "柳", "槐", "枫", "樱", "梅", "栾", "榉", "朴", "乌桕")),
    (("灌木", 0.80), ("黄杨", "冬青", "月季", "女贞", "栀子", "海桐", "卫矛", "绣球", "紫荆", "木槿", "迎春", "连翘", "蔷薇", "石楠", "檗", "薇", "球", "灌", "花")),
    (("地被", 0.80), ("草", "麦冬", "鸢尾", "萱草", "玉簪", "葱兰", "景天", "三叶草", "结缕", "马尼拉", "百慕大", "高羊茅", "黑麦草", "沿阶", "佛甲", "地被")),
    (("其他", 0.65), ("竹", "绿篱", "花镜", "花钵", "树池", "种植池", "模纹", "荷花", "睡莲", "千屈菜", "再力花", "石菖蒲")),
)
_TEXT_CATEGORY_KEYS = {"乔木": "plant_trees", "灌木": "plant_shrubs", "地被": "plant_groundcover", "其他": "plant_other"}


def block_refs(data: dict[str, Any]) -> dict[str, int]:
    meta = data.get("meta") or {}
    refs = meta.get("block_refs") or {}
    out: dict[str, int] = {}
    if isinstance(refs, dict):
        for name, count in refs.items():
            out.setdefault(str(name), 0)
            out[str(name)] += int(count or 0)
    return out


def known_aliases(rules: dict[str, Any]) -> set[str]:
    out: set[str] = set()
    for key in ("plant_block_aliases", "plant_trees", "plant_shrubs", "plant_groundcover", "plant_other"):
        value = rules.get(key) or {}
        if isinstance(value, dict):
            out.update(str(k).upper() for k in value.keys())
        elif isinstance(value, list):
            out.update(str(s).upper() for s in value)
    return out


def suggest_from_name(name: str, rules: dict[str, Any]) -> tuple[str, str, float]:
    """按块名本身给出分类建议：优先命中已配置别名/植物词，否则按通用图例词推断。"""
    category, token = plant_classify_by_block(name, rules)
    if category:
        return category, token, 0.9
    upper = name.upper()
    generic = (
        ("乔木", ("乔", "树", "落叶", "常绿", "乔木")),
        ("灌木", ("灌", "绿篱", "球")),
        ("地被", ("草", "地被", "麦冬")),
    )
    for cat, tokens in generic:
        if any(t in upper for t in tokens):
            return cat, tokens[0], 0.55
    return "", "", 0.0


def _merge_lists(old: list, new: list) -> list:
    out = list(old)
    for x in new:
        if x and x not in out:
            out.append(x)
    return out


def suggest_text_word(word: str, rules: dict[str, Any]) -> tuple[str, str, float]:
    """给未分类植物词做初判（带上下文审计词），供人工复核或明确后写入词库。

    先走 plant_classify（含非植物排除词），再按植物后缀规则；排除词命中立即拒绝，
    避免把“花砖/槐荫区分局”等误提为植物候选。
    """
    category, token = plant_classify(word, rules)
    if category:
        return category, token, 0.9
    for phrase in rules.get("plant_exclude_phrases") or []:
        if str(phrase).upper() in word.upper():
            return "", "", 0.0
    for (cat, conf), toks in _TEXT_SUFFIX_RULES:
        for tok in toks:
            if tok in word:
                return cat, tok, conf
    return "", "", 0.0


def calibrate(detail_path: Path, rules: dict[str, Any]) -> dict[str, Any]:
    data = json.loads(detail_path.read_text(encoding="utf-8"))
    refs = block_refs(data)
    known = known_aliases(rules)
    suggestions: list[dict[str, Any]] = []
    for name, count in sorted(refs.items(), key=lambda x: -x[1]):
        if not compact(name):
            continue
        if name.upper() in known:
            continue
        category, token, conf = suggest_from_name(name, rules)
        suggestions.append({
            "block_name": name, "instance_count": int(count),
            "suggested_category": category, "matched_token": token,
            "confidence": round(conf, 2),
            "status": "candidate" if category and conf >= 0.8 else "review",
            "note": "按块名字面推断" if category else "块名无可辨识植物词，需人工指定",
            "evidence": [{"kind": "block_name", "value": name, "instance_count": int(count)}],
        })
    applied: dict[str, str] = {}
    for row in suggestions:
        if row["suggested_category"] and row["confidence"] >= 0.8:
            applied[row["block_name"]] = row["suggested_category"]

    # 植物文字上下文词（未分类）建议：直接来自覆盖审计
    audit = plant_coverage_audit(read_records(data), rules)
    text_rows: list[dict[str, Any]] = []
    for item in audit.get("top") or []:
        word = compact(item.get("word"))
        if not word:
            continue
        category, token, conf = suggest_text_word(word, rules)
        text_rows.append({
            "word": word, "count": int(item.get("count") or 1), "sample": compact(item.get("sample")),
            "suggested_category": category, "matched_token": token, "confidence": round(conf, 2),
            "status": "candidate" if category and conf >= 0.8 else "review",
            "note": "按植物名后缀/关键词初判" if category else "无明确植物线索，需人工指定",
        })
    text_applied: dict[str, list[str]] = {}
    for row in text_rows:
        if row["suggested_category"] and row["confidence"] >= 0.8:
            cat = row["suggested_category"]
            text_applied.setdefault(cat, [])
            if row["word"] not in text_applied[cat]:
                text_applied[cat].append(row["word"])
    return {
        "schema": "cad-landscape-calibrate/v1",
        "source_file": detail_path.name,
        "summary": {"block_refs": sum(refs.values()), "unique_blocks": len(refs), "suggestions": len(suggestions), "auto_appliable": len(applied),
                    "text_audit_words": len(text_rows), "text_auto_appliable": sum(len(v) for v in text_applied.values())},
        "suggestions": suggestions,
        "text_word_suggestions": text_rows,
        "plant_block_aliases_override": applied,
        "plant_text_words_override": text_applied,
        "final_quantity": False,
    }


def verify_override(detail_path: Path, rules: dict[str, Any], institute: str, override_path: Path | None = None) -> dict[str, Any] | None:
    """用 --institute 覆盖复验：对比同一详情 base 与 institute 的块名/文字植物分类变化。"""
    from cad_landscape_geometry import block_plant_candidates, merge_override
    target = override_path if override_path is not None else INSTITUTE_DIR / f"{institute}.json"
    if not target.exists():
        return None
    data = json.loads(detail_path.read_text(encoding="utf-8"))
    merged = merge_override(rules, json.loads(target.read_text(encoding="utf-8")))
    base = {row.get("name"): row["category"] for row in block_plant_candidates(data, rules)}
    inst = {row.get("name"): row["category"] for row in block_plant_candidates(data, merged)}
    changes = []
    for name in sorted(set(base) | set(inst)):
        b, a = base.get(name), inst.get(name)
        if b != a:
            changes.append({"block_name": name, "before": b or "", "after": a or "", "status": "new" if not b else "changed"})
    return {"schema": "cad-landscape-calibrate-verify/v1", "source_file": detail_path.name,
            "summary": {"verified_blocks": len(inst), "changes": len(changes), "override": str(target)},
            "changes": changes, "final_quantity": False}


def _load_or_new(target: Path) -> dict[str, Any]:
    if target.exists():
        try:
            return json.loads(target.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def main() -> int:
    import pyboot
    pyboot.ensure_utf8_io()
    parser = argparse.ArgumentParser(description="把新设计院 CAD 详情转成块名+文字词库覆盖。")
    parser.add_argument("inputs", nargs="+")
    parser.add_argument("--institute", default="design_a", help="设计院目录名，写入 institutes/<名>.json")
    parser.add_argument("--out-dir", default="校准")
    parser.add_argument("--rules", default=str(INSTITUTE_DIR.parent / "rules.json"))
    parser.add_argument("--override-path", default=None,
                        help="覆盖写入/复验的目标文件路径（默认 institutes/<名>.json；用于沙盒/临时目录）")
    parser.add_argument("--write-override", action="store_true", help="生成 institutes/<名>.json 块名覆盖文件（含自动可用项）")
    parser.add_argument("--write-text-words", action="store_true", help="把可自动写入的植物名词扩进 institutes/<名>.json（需人工复核后使用）")
    parser.add_argument("--verify", action="store_true", help="覆盖写入后自动用 --institute 复验分类变化")
    args = parser.parse_args()
    rules = load_rules(Path(args.rules))
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    merged: dict[str, str] = {}
    text_merged: dict[str, list[str]] = {}
    for value in args.inputs:
        src = Path(value)
        if not src.exists():
            raise FileNotFoundError(src)
        result = calibrate(src, rules)
        jp = out_dir / f"{src.stem}.calibrate.json"
        jp.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        merged.update(result.get("plant_block_aliases_override") or {})
        for cat, words in (result.get("plant_text_words_override") or {}).items():
            text_merged.setdefault(cat, [])
            text_merged[cat] = _merge_lists(text_merged[cat], words)
        print(json.dumps({"source": src.name, "summary": result["summary"], "output": str(jp)}, ensure_ascii=False))

    if args.write_override or args.write_text_words:
        target = Path(args.override_path) if args.override_path else INSTITUTE_DIR / f"{args.institute}.json"
        override = _load_or_new(target)
        if args.write_override and merged:
            old = dict(override.get("plant_block_aliases") or {})
            old.update(merged)
            override["plant_block_aliases"] = dict(sorted(old.items(), key=lambda x: (x[1], x[0])))
        if args.write_text_words and text_merged:
            for cat, words in text_merged.items():
                key = _TEXT_CATEGORY_KEYS.get(cat)
                if not key:
                    continue
                override.setdefault(key, [])
                override[key] = _merge_lists(override.get(key) or [], words)
        override.setdefault("name", args.institute)
        override.setdefault("description", "由 cad_landscape_calibrate 生成，请人工复核补充")
        target.write_text(json.dumps(dict(sorted(override.items())), ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps({"wrote_override": str(target), "alias_count": len(merged),
                          "text_word_count": sum(len(v) for v in text_merged.values())}, ensure_ascii=False))
        if args.verify:
            verify_path = out_dir / "calibrate_verify.json"
            verifies = []
            for value in args.inputs:
                res = verify_override(Path(value), rules, args.institute, Path(args.override_path) if args.override_path else None)
                if res:
                    verifies.append(res)
                    print(json.dumps({"verify": res["source_file"], "summary": res["summary"]}, ensure_ascii=False))
            if verifies:
                verify_path.write_text(json.dumps(verifies, ensure_ascii=False, indent=2), encoding="utf-8")
                print(json.dumps({"wrote_verify": str(verify_path)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
