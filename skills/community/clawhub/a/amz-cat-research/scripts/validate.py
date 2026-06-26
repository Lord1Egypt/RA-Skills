#!/usr/bin/env python3
"""
validate.py — 校验 evaluate 提取结果

每个字段定义期望类型和空值判定规则。
返回: {valid: bool, missing: [...], suspicious: [...], report: str}

用法:
  python3 validate.py '<extracted_json>'
"""

import sys
import json
import re

# 字段期望定义：{field_id: {required, type, not_empty_pattern}}
FIELD_RULES = {
    "asin":             {"required": True,  "type": "text",  "not_empty": r"^[A-Z0-9]{10}$"},
    "title":            {"required": True,  "type": "text",  "not_empty": r".{10,}"},
    "price":            {"required": True,  "type": "text",  "not_empty": r"\$[\d.,]+"},
    "rating":           {"required": True,  "type": "text",  "not_empty": r"[\d.]+.*star"},
    "review_count":     {"required": True,  "type": "text",  "not_empty": r"[\d,]+"},
    "brand":            {"required": False, "type": "text",  "not_empty": r".{1,}"},
    "seller":           {"required": False, "type": "text",  "not_empty": r".{1,}"},
    "spirit_found":     {"required": False, "type": "bool",  "not_empty": None},
    "sif_found":        {"required": False, "type": "bool",  "not_empty": None},
    "has_variants":     {"required": False, "type": "bool",  "not_empty": None},
    "image_main":       {"required": False, "type": "text",  "not_empty": r"https?://"},
    "aplus_exists":     {"required": False, "type": "bool",  "not_empty": None},
    "video_exists":     {"required": False, "type": "bool",  "not_empty": None},
    "review_histogram": {"required": False, "type": "raw",   "not_empty": r"\d+%.*star"},
}

# 卖家精灵解析后字段的规则
SPIRIT_RULES = {
    "spirit_brand":          {"required": True, "type": "text"},
    "spirit_seller":         {"required": True, "type": "text"},
    "spirit_fba_fee":        {"required": True, "type": "text"},
    "spirit_sales_30d_parent": {"required": True, "type": "text"},
    "spirit_listing_date":   {"required": True, "type": "text"},
    "spirit_total_keywords": {"required": False, "type": "text"},
}


def validate(data: dict) -> dict:
    missing = []
    suspicious = []
    warnings = []

    all_rules = {**FIELD_RULES, **SPIRIT_RULES}

    for field_id, rule in all_rules.items():
        val = data.get(field_id)

        # 检查缺失
        if val is None or val == "" or val == "null":
            if rule["required"]:
                missing.append(field_id)
            continue

        # 检查可疑值
        not_empty = rule.get("not_empty")
        if not_empty and val:
            if not re.search(not_empty, str(val)):
                suspicious.append(f"{field_id}={val}")

    # 特殊校验：seller 字段不能是材质名
    seller = data.get("seller") or data.get("spirit_seller")
    material_words = ["Stainless Steel", "Metal", "SUS304", "Black", "Silver", "Gold"]
    if seller and any(w.lower() == seller.lower() for w in material_words):
        suspicious.append(f"seller={seller}(疑似错抓材质)")

    # 生成报告
    lines = []
    if missing:
        lines.append(f"❌ 缺失必填字段({len(missing)}): {', '.join(missing)}")
    if suspicious:
        lines.append(f"⚠️ 可疑值({len(suspicious)}): {', '.join(suspicious[:5])}")
    if not missing and not suspicious:
        lines.append("✅ 所有字段校验通过")

    # 插件可用性
    spirit_found = data.get("spirit_found")
    sif_found = data.get("sif_found")
    if not spirit_found:
        lines.append("⚠️ 卖家精灵插件未检测到")
    if not sif_found:
        lines.append("⚠️ SIF 插件未检测到")

    return {
        "valid": len(missing) == 0,
        "missing": missing,
        "suspicious": suspicious,
        "report": "\n".join(lines),
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 validate.py '<extracted_json>'")
        sys.exit(1)

    try:
        data = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        print(json.dumps({"valid": False, "error": "invalid_json"}))
        sys.exit(1)

    result = validate(data)
    print(json.dumps(result, ensure_ascii=False, indent=1))
    print(f"\n{result['report']}")
