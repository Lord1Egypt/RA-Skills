#!/usr/bin/env python3
"""
parse_raw.py — 解析卖家精灵 / SIF 插件 raw text 为结构化字段

用法:
  python3 parse_raw.py spirit "<raw_text_json>"   # 解析卖家精灵
  python3 parse_raw.py sif "<raw_text_json>"       # 解析 SIF
  python3 parse_raw.py all "<full_result_json>"    # 解析全量结果

输入: JSON 字符串（evaluate 返回的原始结果）
输出: 解析后的结构化 JSON
"""

import sys
import json
import re

from selector_registry import SPIRIT_PATTERNS, SIF_PATTERNS


def parse_spirit(raw_text: str) -> dict:
    """从卖家精灵 raw text 中提取子字段"""
    if not raw_text:
        return {"spirit_available": False}

    result = {"spirit_available": True, "spirit_raw_length": len(raw_text)}
    for field_id, pattern in SPIRIT_PATTERNS.items():
        m = re.search(pattern, raw_text)
        if m:
            if m.lastindex and m.lastindex >= 1:
                result[field_id] = m.group(1).strip()
                if m.lastindex >= 2:
                    result[field_id + "_extra"] = m.group(2).strip()
            else:
                result[field_id] = m.group(0).strip()
        else:
            result[field_id] = None

    return result


def parse_sif(raw_text: str) -> dict:
    """从 SIF raw text 中提取子字段"""
    if not raw_text:
        return {"sif_available": False}

    result = {"sif_available": True, "sif_raw_length": len(raw_text)}
    for field_id, pattern in SIF_PATTERNS.items():
        m = re.search(pattern, raw_text)
        if m:
            result[field_id] = m.group(1).strip() if m.lastindex else m.group(0).strip()
        else:
            result[field_id] = None

    return result


def parse_all(result_json: str) -> dict:
    """解析 evaluate 返回的全量结果"""
    try:
        data = json.loads(result_json)
    except json.JSONDecodeError:
        return {"error": "invalid_json", "raw": result_json[:200]}

    merged = dict(data)

    # 解析卖家精灵
    spirit_raw = data.get("spirit_raw")
    if spirit_raw:
        spirit_parsed = parse_spirit(spirit_raw)
        merged.update(spirit_parsed)
        del merged["spirit_raw"]  # 清理原始文本

    # 解析 SIF
    sif_raw = data.get("sif_raw")
    if sif_raw:
        sif_parsed = parse_sif(sif_raw)
        merged.update(sif_parsed)
        del merged["sif_raw"]

    return merged


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python3 parse_raw.py <spirit|sif|all> '<json_string>'")
        sys.exit(1)

    mode = sys.argv[1]
    input_data = sys.argv[2]

    if mode == "spirit":
        result = parse_spirit(input_data)
    elif mode == "sif":
        result = parse_sif(input_data)
    elif mode == "all":
        result = parse_all(input_data)
    else:
        result = {"error": f"unknown mode: {mode}"}

    print(json.dumps(result, ensure_ascii=False, indent=1))
