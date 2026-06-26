#!/usr/bin/env python3
"""
coverage_analyzer.py - CIS 规则与 OpenEuler 基线的覆盖分析

按配置项路径/名称进行精确匹配 → 模糊匹配，逐项判定覆盖状态：
  - 完全覆盖 (Fully Covered): 路径匹配 + OpenEuler 要求值 ≥ CIS（同等或更安全）
  - 部分覆盖 (Partially Covered): 路径匹配但值存在差异/无法判定
  - 未覆盖 (Not Covered): 路径在 OpenEuler 基线中不存在

用法:
    python coverage_analyzer.py --cis cis_rules.json --openeuler openeuler_items.json -o output.json
"""

import json
import argparse
import re
import sys
from pathlib import Path

try:
    from thefuzz import fuzz
except ImportError:
    print("警告: thefuzz 未安装，模糊匹配功能将不可用。"
          "请运行: pip install thefuzz python-Levenshtein", file=sys.stderr)
    fuzz = None


# ─────────────────────────────────────────────
# 匹配模块
# ─────────────────────────────────────────────

def normalize_path(path: str) -> str:
    """标准化路径：去空格、小写、统一分隔符"""
    if not path:
        return ""
    path = path.strip().lower().replace("\\", "/")
    # 去除多余的连续斜杠
    path = re.sub(r'/+', '/', path)
    # 去除末尾斜杠
    path = path.rstrip('/')
    return path


def normalize_param(param: str) -> str:
    """标准化参数名"""
    if not param:
        return ""
    return param.strip().lower()


def normalize_value(value: str) -> str:
    """标准化值"""
    if not value:
        return ""
    return value.strip().strip('"').strip("'").lower()


def exact_match(cis_item: dict, oe_items: list) -> dict:
    """
    精确匹配：同时匹配 config_path 和 config_param
    返回匹配结果或 None
    """
    cis_path = normalize_path(cis_item.get("config_path", ""))
    cis_param = normalize_param(cis_item.get("config_param", ""))

    for oe in oe_items:
        oe_path = normalize_path(oe.get("config_path", ""))
        oe_param = normalize_param(oe.get("config_param", ""))

        if cis_path and oe_path and cis_path == oe_path:
            # 如果双方都有参数名，匹配参数名
            if cis_param and oe_param:
                if cis_param == oe_param:
                    return oe
            # 如果只有路径匹配，且 CIS 无参数字段，也接受
            elif not cis_param and not oe_param:
                return oe
            elif not cis_param:
                return oe  # CIS 无参数时，路径匹配即可
    return None


def fuzzy_match(cis_item: dict, oe_items: list, threshold: int = 85) -> list:
    """
    模糊匹配：用 thefuzz 计算路径相似度
    返回匹配度从高到底的候选项列表
    """
    if fuzz is None:
        return []

    cis_path = normalize_path(cis_item.get("config_path", ""))
    if not cis_path:
        return []

    matches = []
    for oe in oe_items:
        oe_path = normalize_path(oe.get("config_path", ""))
        if not oe_path:
            continue
        ratio = fuzz.token_sort_ratio(cis_path, oe_path)
        if ratio >= threshold:
            matches.append({"item": oe, "score": ratio})

    # 按相似度降序排列
    matches.sort(key=lambda x: x["score"], reverse=True)
    return matches


# ─────────────────────────────────────────────
# 值安全性比较模块
# ─────────────────────────────────────────────

def _parse_numeric(val):
    """尝试将值转换为数值比较，失败返回 None"""
    try:
        return float(val)
    except (ValueError, TypeError):
        return None


def _is_bool_like(val):
    """检查值是否是布尔型"""
    true_vals = {"yes", "true", "1", "enabled", "on", "allow", "permit"}
    false_vals = {"no", "false", "0", "disabled", "off", "deny", "reject"}
    if val in true_vals:
        return True, True
    if val in false_vals:
        return True, False
    return False, None


def _parse_permission(val):
    """解析文件权限值，返回数值"""
    perm_match = re.match(r'^0?([0-7]{3,4})$', val)
    if perm_match:
        return int(perm_match.group(1), 8)
    return None


def _permission_stricter(cis_int, oe_int):
    """判断 OpenEuler 权限是否更严格（权限值越小越严格）"""
    return oe_int <= cis_int


def is_value_stricter_or_equal(cis_val: str, oe_val: str) -> bool:
    """
    判断 OpenEuler 值是否 ≥ CIS 值（同等或更安全）
    返回 True/False/None（无法判定）
    """
    cis_clean = normalize_value(cis_val)
    oe_clean = normalize_value(oe_val)

    if not cis_clean or not oe_clean:
        return None

    # 1. 完全相等
    if cis_clean == oe_clean:
        return True

    # 2. 布尔值
    cis_bool = _is_bool_like(cis_clean)
    oe_bool = _is_bool_like(oe_clean)
    if cis_bool[0] and oe_bool[0]:
        # 如果 CIS 要求 "yes"，OpenEuler 也是 "yes" → 覆盖
        return cis_bool[1] == oe_bool[1]

    # 3. 数值比较
    cis_num = _parse_numeric(cis_clean)
    oe_num = _parse_numeric(oe_clean)
    if cis_num is not None and oe_num is not None:
        # 判断上下文：如果 CIS 规则是"设置上限"类型（如超时、重试次数），
        # 则 oe <= cis 更安全；如果是"设置下限"类型（如密码长度），则 oe >= cis 更安全
        # 通过规则标题中的关键词判断
        # 默认保守：严格相等才为覆盖
        return oe_num == cis_num

    # 4. 权限值比较
    cis_perm = _parse_permission(cis_clean)
    oe_perm = _parse_permission(oe_clean)
    if cis_perm is not None and oe_perm is not None:
        return _permission_stricter(cis_perm, oe_perm)

    # 5. 包含关系判断
    if cis_clean in oe_clean or oe_clean in cis_clean:
        return True

    return None


def _determine_direction(cis_item: dict) -> str:
    """
    根据规则标题和上下文确定数值比较方向。
    'upper' = 值越小越安全（超时、重试次数）
    'lower' = 值越大越安全（密码长度、密码复杂度）
    'exact' = 必须精确相等
    """
    title = (cis_item.get("title", "") + " " + cis_item.get("config_param", "")).lower()

    upper_keywords = [
        "timeout", "超时", "retry", "重试", "max", "最大", "limit", "限制",
        "lockout", "锁定", "attempt", "尝试", "expire", "过期",
        "maxauthtries", "clientalivecountmax", "clientaliveinterval",
        "logingracetime", "inactive", "不活跃"
    ]
    lower_keywords = [
        "length", "长度", "password", "密码", "complexity", "复杂度",
        "strength", "强度", "minlen", "difok", "minclass",
        "passlen", "passwdlen"
    ]

    for kw in upper_keywords:
        if kw in title:
            return "upper"
    for kw in lower_keywords:
        if kw in title:
            return "lower"

    return "exact"


def compare_values(cis_val: str, oe_val: str, cis_item: dict) -> str:
    """
    比较两个值，返回覆盖判定结果。
    Returns: "fully_covered", "partially_covered", or "not_applicable"
    """
    direction = _determine_direction(cis_item)
    cis_clean = normalize_value(cis_val)
    oe_clean = normalize_value(oe_val)
    cis_num = _parse_numeric(cis_clean)
    oe_num = _parse_numeric(oe_clean)

    if cis_clean == oe_clean:
        return "fully_covered"

    if cis_num is not None and oe_num is not None:
        if direction == "upper":
            # 值越小越安全: oe <= cis 才是覆盖
            return "fully_covered" if oe_num <= cis_num else "partially_covered"
        elif direction == "lower":
            # 值越大越安全: oe >= cis 才是覆盖
            return "fully_covered" if oe_num >= cis_num else "partially_covered"
        else:
            # 默认方向未知，精确匹配才算覆盖
            return "fully_covered" if oe_num == cis_num else "partially_covered"

    # 布尔/权限值比较
    result = is_value_stricter_or_equal(cis_val, oe_val)
    if result is True:
        return "fully_covered"
    elif result is False:
        return "partially_covered"

    return "partially_covered"  # 无法判定时，保守返回部分覆盖


# ─────────────────────────────────────────────
# 分析引擎
# ─────────────────────────────────────────────

def analyze_coverage(cis_rules: list, oe_items: list, fuzzy_threshold: int = 85) -> list:
    """
    执行完整覆盖分析
    返回每条 CIS 规则的覆盖状态列表
    """
    results = []

    for rule in cis_rules:
        result = {
            "rule_id": rule.get("rule_id", ""),
            "title": rule.get("title", ""),
            "config_path": rule.get("config_path", ""),
            "config_param": rule.get("config_param", ""),
            "cis_expected_value": rule.get("expected_value", ""),
            "level": rule.get("level", ""),
            "scoring": rule.get("scoring", ""),
            "oe_config_path": "",
            "oe_config_param": "",
            "oe_expected_value": "",
            "oe_description": "",
            "coverage_status": "not_covered",
            "match_type": "",
            "remarks": ""
        }

        # 步骤 1：精确匹配
        oe_match = exact_match(rule, oe_items)
        if oe_match:
            result["oe_config_path"] = oe_match.get("config_path", "")
            result["oe_config_param"] = oe_match.get("config_param", "")
            result["oe_expected_value"] = oe_match.get("expected_value", "")
            result["oe_description"] = oe_match.get("description", "")
            result["match_type"] = "exact"

            # 比较值
            cis_val = rule.get("expected_value", "")
            oe_val = oe_match.get("expected_value", "")
            if cis_val and oe_val:
                status = compare_values(cis_val, oe_val, rule)
                result["coverage_status"] = status
                if status == "partially_covered":
                    result["remarks"] = f"值不匹配: CIS={cis_val}, OpenEuler={oe_val}"
            elif cis_val and not oe_val:
                result["coverage_status"] = "partially_covered"
                result["remarks"] = "CIS 有期望值，但 OpenEuler 未定义"
            else:
                result["coverage_status"] = "fully_covered"
                result["remarks"] = "路径匹配，无值要求差异"

            results.append(result)
            continue

        # 步骤 2：模糊匹配
        fuzzy_matches = fuzzy_match(rule, oe_items, fuzzy_threshold)
        best_match = fuzzy_matches[0] if fuzzy_matches else None

        if best_match:
            oe_match = best_match["item"]
            result["oe_config_path"] = oe_match.get("config_path", "")
            result["oe_config_param"] = oe_match.get("config_param", "")
            result["oe_expected_value"] = oe_match.get("expected_value", "")
            result["oe_description"] = oe_match.get("description", "")
            result["match_type"] = f"fuzzy ({best_match['score']}%)"

            # 模糊匹配可能需要人工确认
            cis_val = rule.get("expected_value", "")
            oe_val = oe_match.get("expected_value", "")
            if cis_val and oe_val:
                status = compare_values(cis_val, oe_val, rule)
                result["coverage_status"] = status
                result["remarks"] = f"模糊匹配 (相似度 {best_match['score']}%)，建议人工确认"
            else:
                result["coverage_status"] = "partially_covered"
                result["remarks"] = f"模糊匹配 (相似度 {best_match['score']}%)，建议人工确认"
            results.append(result)
            continue

        # 步骤 3：无匹配 → 未覆盖
        result["coverage_status"] = "not_covered"
        result["remarks"] = "OpenEuler 基线中未找到对应项"
        result["match_type"] = "none"
        results.append(result)

    return results


def main():
    parser = argparse.ArgumentParser(
        description="CIS 规则与 OpenEuler 基线覆盖分析")
    parser.add_argument("--cis", required=True,
                        help="CIS 规则 JSON 文件路径 (parse_cis_pdf.py 输出)")
    parser.add_argument("--openeuler", required=True,
                        help="OpenEuler 基线条目 JSON 文件路径 (parse_openeuler_md.py 输出)")
    parser.add_argument("-o", "--output", default="analysis_result.json",
                        help="分析结果 JSON 输出路径 (默认: analysis_result.json)")
    parser.add_argument("--threshold", type=int, default=85,
                        help="模糊匹配相似度阈值 (默认: 85)")
    args = parser.parse_args()

    # 加载数据
    with open(args.cis, "r", encoding="utf-8") as f:
        cis_rules = json.load(f)
    with open(args.openeuler, "r", encoding="utf-8") as f:
        oe_items = json.load(f)

    print(f"[*] CIS 规则: {len(cis_rules)} 条")
    print(f"[*] OpenEuler 基线: {len(oe_items)} 条")
    print(f"[*] 模糊匹配阈值: {args.threshold}%")

    # 执行分析
    print("[*] 执行覆盖分析...")
    results = analyze_coverage(cis_rules, oe_items, args.threshold)

    # 统计
    status_counts = {}
    for r in results:
        status = r["coverage_status"]
        status_counts[status] = status_counts.get(status, 0) + 1

    print(f"\n📊 覆盖统计:")
    for status, count in sorted(status_counts.items(), key=lambda x: -x[1]):
        label = {"fully_covered": "✅ 完全覆盖",
                 "partially_covered": "⚠️ 部分覆盖",
                 "not_covered": "❌ 未覆盖"}.get(status, status)
        print(f"   {label}: {count} 条")

    # 输出 JSON
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({
            "summary": {
                "cis_total": len(cis_rules),
                "oe_total": len(oe_items),
                "fully_covered": status_counts.get("fully_covered", 0),
                "partially_covered": status_counts.get("partially_covered", 0),
                "not_covered": status_counts.get("not_covered", 0),
            },
            "results": results
        }, f, ensure_ascii=False, indent=2)

    print(f"\n[✓] 分析结果已保存: {output_path}")


if __name__ == "__main__":
    main()
