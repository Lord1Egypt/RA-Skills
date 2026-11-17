"""Tier 1+2 校验 Fill Contract。

Tier 1（结构完整性）:
- placeholders 非空，id 唯一
- location 引用有效（para_index/table_index 存在于 raw_structure）

Tier 2（约束满足）:
- 占位符已识别 is_placeholder 标记
- 静态文本已标记 is_static
- content_constraint 可追溯到 original_text（关键词出现于原文）
"""

import argparse
import json
import sys
from pathlib import Path


def _build_location_index(raw_structure):
    """构建可用 location 索引：段落索引集合 + 表格单元格索引集合。"""
    para_indices = {p["index"] for p in raw_structure.get("paragraphs", [])}
    table_cells = set()
    for tbl in raw_structure.get("tables", []):
        ti = tbl["table_index"]
        for row in tbl.get("grid", []):
            for cell in row.get("cells", []):
                if not cell.get("merged_from"):
                    table_cells.add((ti, cell["row"], cell["col"]))
    return para_indices, table_cells


def _check_keyword_traceable(constraint, original_text):
    """Tier 2: content_constraint 中的关键词应可追溯至 original_text。"""
    if not constraint or not original_text:
        return True, None
    # 提取约束中的关键名词（简化启发式：长度>=3 的中文词、英文词）
    # 这里采用粗匹配：约束中任一 3+ 字符的子串在原文中出现
    keywords_in_constraint = []
    # 提取 quoted 关键词
    for kw in constraint.replace("“", "\"").replace("”", "\"").split("\"")[1::2]:
        if len(kw) >= 2:
            keywords_in_constraint.append(kw)
    # 抽取约束中的中文片段
    import re
    cn_fragments = re.findall(r"[\u4e00-\u9fa5]{3,}", constraint)
    keywords_in_constraint.extend(cn_fragments)
    # 检查每个关键词是否在原文中
    missing = []
    for kw in keywords_in_constraint:
        if kw not in original_text and kw.lower() not in original_text.lower():
            missing.append(kw)
    if missing:
        return False, f"约束关键词 {missing} 未在 original_text 中出现，疑似擅自生成"
    return True, None


def validate_contract(contract: dict, raw_structure: dict) -> dict:
    failed_checks = []
    tier_failed = None

    # === Tier 1: 结构完整性 ===
    placeholders = contract.get("placeholders", [])

    if not placeholders:
        failed_checks.append({
            "check": "placeholders_empty",
            "fix_hint": "未识别任何占位符，请检查模板是否含可填充位置",
        })
        tier_failed = 1

    ids = [p.get("id") for p in placeholders]
    duplicates = set([i for i in ids if i and ids.count(i) > 1])
    if duplicates:
        failed_checks.append({
            "check": "duplicate_ids",
            "fix_hint": f"占位符 id 重复: {duplicates}",
        })
        if tier_failed is None:
            tier_failed = 1

    para_indices, table_cells = _build_location_index(raw_structure)

    for p in placeholders:
        loc = p.get("location", {})
        if "para_index" in loc and loc["para_index"] not in para_indices:
            failed_checks.append({
                "check": f"invalid_para_index_{p.get('id')}",
                "fix_hint": f"para_index={loc['para_index']} 不存在于 raw_structure",
            })
            if tier_failed is None:
                tier_failed = 1
        if "table_index" in loc:
            key = (loc["table_index"], loc.get("row", -1), loc.get("col", -1))
            if key not in table_cells:
                failed_checks.append({
                    "check": f"invalid_table_cell_{p.get('id')}",
                    "fix_hint": f"表格位置 {key} 不存在于 raw_structure",
                })
                if tier_failed is None:
                    tier_failed = 1

    # === Tier 2: 约束满足 ===
    if tier_failed is None:
        for p in placeholders:
            if "is_placeholder" not in p:
                failed_checks.append({
                    "check": f"missing_is_placeholder_{p.get('id')}",
                    "fix_hint": f"占位符 {p.get('id')} 缺少 is_placeholder 字段",
                })
                if tier_failed is None:
                    tier_failed = 2
            if "is_static" not in p:
                failed_checks.append({
                    "check": f"missing_is_static_{p.get('id')}",
                    "fix_hint": f"占位符 {p.get('id')} 缺少 is_static 字段",
                })
                if tier_failed is None:
                    tier_failed = 2

            # content_constraint 可追溯性
            constraint = p.get("content_constraint", "")
            original = p.get("original_text", "")
            if constraint and original:
                ok, hint = _check_keyword_traceable(constraint, original)
                if not ok:
                    failed_checks.append({
                        "check": f"untraceable_constraint_{p.get('id')}",
                        "fix_hint": hint,
                    })
                    if tier_failed is None:
                        tier_failed = 2

    return {
        "passed": len(failed_checks) == 0,
        "tier_failed": tier_failed,
        "failed_checks": failed_checks,
    }


def main():
    parser = argparse.ArgumentParser(description="Tier 1+2 校验 Fill Contract")
    parser.add_argument("--contract", required=True, help="fill_contract.json 路径")
    parser.add_argument("--structure", required=True, help="raw_structure.json 路径")
    args = parser.parse_args()

    contract = json.loads(Path(args.contract).read_text(encoding="utf-8"))
    raw_structure = json.loads(Path(args.structure).read_text(encoding="utf-8"))

    result = validate_contract(contract, raw_structure)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
