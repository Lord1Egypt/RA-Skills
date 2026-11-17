#!/usr/bin/env python3
"""
expert2skill — 访谈产物 → 规范化 rule_library JSON（distill 步骤）

作用：
  1. 读取访谈确认的规则定义（AI 整理的中间产物，JSON 或 Python dict）
  2. 补全默认值（score_if_pass/fail、severity、evidence_required 等）
  3. 校验必需字段与 v2 schema 一致性
  4. 输出规范化 rule_library JSON

用法：
  python3 distill.py input.json -o output.json     # 读取中间产物
  python3 distill.py -c input.json                 # 只校验，不输出
  python3 distill.py --schema v2                   # 打印当前支持的 schema 版本

注意：这是骨架版本，聚焦校验与规范化。访谈引导由 AI 按 SKILL.md / references 执行。
"""
import argparse
import json
import os
import sys

SCHEMA_VERSION = "v2"

# 题型白名单
QUESTION_TYPES = {
    "binary", "scale", "numeric", "text", "conditional", "self_check", "multi_select",
}

# judge.mode 白名单
JUDGE_MODES = {"direct", "threshold", "option_map", "expert_review"}

# 允许的 when 表达式操作符（防止任意代码）
WHEN_OPS = {"==", "!=", ">", "<", ">=", "<=", "contains", "in"}


def default_item(item, category_id):
    """补全 item 的默认字段，返回副本。"""
    it = dict(item)
    it.setdefault("category", category_id)
    it.setdefault("type", "binary")
    it.setdefault("score_if_pass", 1.0)
    it.setdefault("score_if_fail", 0.0)
    it.setdefault("weight", 1.0)
    it.setdefault("severity", "medium")
    it.setdefault("applies_when", None)
    it.setdefault("evidence_required", False)
    it.setdefault("judge", {"mode": "direct"})
    # 确保 judge 结构完整
    j = dict(it["judge"])
    if j.get("mode") == "expert_review":
        j.setdefault("note", "开放题由评估者自评，AI 不自动判分")
    it["judge"] = j
    return it


def validate_item(it, category_id, idx):
    """校验单个 item，返回错误列表。"""
    errs = []
    if not it.get("id"):
        errs.append(f"{category_id}[{idx}] item 缺少 id")
    if not it.get("name"):
        errs.append(f"{category_id}[{idx}] item 缺少 name")
    if not it.get("question"):
        errs.append(f"{category_id}[{idx}] '{it.get('id')}' 缺少 question")
    t = it.get("type")
    if t not in QUESTION_TYPES:
        errs.append(f"{category_id}[{idx}] 未知题型 '{t}'（允许：{sorted(QUESTION_TYPES)}）")
    mode = it.get("judge", {}).get("mode")
    if mode not in JUDGE_MODES:
        errs.append(f"{category_id}[{idx}] judge.mode '{mode}' 未知（允许：{sorted(JUDGE_MODES)}）")
    # v2: judge.reference 必须引用 subject_profile 字段
    ref = it.get("judge", {}).get("reference")
    if ref and not ref.startswith("subject_profile."):
        errs.append(f"{category_id}[{idx}] judge.reference 应为 'subject_profile.xxx'，实际 '{ref}'")
    # weight_conditions 校验
    for wc in it.get("weight_conditions", []) or []:
        when = wc.get("when", "")
        if not any(f" {op} " in f" {when} " for op in WHEN_OPS):
            errs.append(f"{category_id}[{idx}] weight_conditions.when 表达式 '{when}' 不含受支持操作符 {sorted(WHEN_OPS)}")
    return errs


def validate(doc):
    """校验完整 rule_library 文档，返回 (errors, warnings)。"""
    errs, warns = [], []
    rl = doc.get("rule_library", {})
    if not rl.get("id"):
        errs.append("rule_library 缺少 id")
    if not rl.get("title"):
        errs.append("rule_library 缺少 title")
    # v2: subject_profile 字段 key 唯一性
    seen = set()
    for f_ in rl.get("subject_profile", {}).get("fields", []) or []:
        key = f_.get("key")
        if not key:
            errs.append("subject_profile.fields 有字段缺少 key")
        elif key in seen:
            errs.append(f"subject_profile 字段 key 重复: {key}")
        seen.add(key)
    # categories + items
    cats = doc.get("categories", [])
    if not cats:
        errs.append("categories 为空")
    item_ids = set()
    for cat in cats:
        cid = cat.get("id", "?")
        if not cat.get("name"):
            errs.append(f"category '{cid}' 缺少 name")
        for idx, it in enumerate(cat.get("items", [])):
            errs += validate_item(it, cid, idx)
            iid = it.get("id")
            if iid and iid in item_ids:
                warns.append(f"item id 跨类别重复: {iid}")
            item_ids.add(iid)
    return errs, warns


def normalize(doc):
    """规范化：补默认值 + 排序。返回新 doc。"""
    out = json.loads(json.dumps(doc))  # deep copy
    rl = out["rule_library"]
    rl.setdefault("version", "0.1.0")
    rl.setdefault("library_type", "expert")
    rl.setdefault("question_types_supported", sorted(QUESTION_TYPES))
    rl.setdefault("scoring", {
        "weights": {"pass": 1.0, "partial": 0.5, "fail": 0.0},
        "na_excluded": True,
        "formula": "score = round((passed + partial*0.5) / applicable * 100)",
    })
    for cat in out["categories"]:
        cat.setdefault("weight", 1.0)
        for idx, it in enumerate(cat["items"]):
            cat["items"][idx] = default_item(it, cat.get("id", "?"))
    return out


def main():
    ap = argparse.ArgumentParser(description="expert2skill distill: 规范化 + 校验 rule_library")
    ap.add_argument("input", nargs="?", help="访谈中间产物 JSON 文件")
    ap.add_argument("-o", "--output", help="输出规范化 JSON 路径")
    ap.add_argument("-c", "--check", action="store_true", help="只校验不输出")
    ap.add_argument("--schema", action="store_true", help="打印支持的 schema 版本并退出")
    args = ap.parse_args()

    if args.schema:
        print(f"expert2skill schema 支持版本: {SCHEMA_VERSION}")
        return 0
    if not args.input:
        ap.error("需要输入文件")

    with open(args.input, encoding="utf-8") as f:
        doc = json.load(f)

    errs, warns = validate(doc)
    for w in warns:
        print(f"⚠️  WARN: {w}")
    if errs:
        for e in errs:
            print(f"❌ ERROR: {e}")
        print(f"校验失败：{len(errs)} 个错误")
        return 1
    print("✅ 校验通过")

    if not args.check:
        norm = normalize(doc)
        out_path = args.output or f"{os.path.splitext(args.input)[0]}.normalized.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(norm, f, ensure_ascii=False, indent=2)
        n_items = sum(len(c["items"]) for c in norm["categories"])
        print(f"✅ 已输出 {out_path}  （{len(norm['categories'])} 维度 / {n_items} 项 / schema {SCHEMA_VERSION}）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
