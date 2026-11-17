#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rules_helper_v2.py

兼容两类组合人群创建规则结构：

1) 旧版【扁平rule】（历史口径）：
   data = [{"op": "and|not|noop", "rule": {"audience":[], "tag":[]}}, ...]
   约束：最后一个元素 op 必须为 noop

2) 新版【group嵌套】（以用户提供的创建示例为准）：
   data = [{"op": "and|or|not|noop", "group": [ {"op": "and|or|not|noop", "rule": {...}}, ... ]}, ...]
   约束：
   - 每个 group 内最后一个元素 op 必须为 noop
   - 最外层最后一个组 op 必须为 noop

说明：当服务端要求 group 结构时，必须使用 build_grouped_data_http + validate_grouped_data_http。
"""

from typing import Any, Dict, List


# -------------------------
# 旧版：扁平rule
# -------------------------

def build_rules_http(or_groups: List[List[int]]) -> List[Dict[str, Any]]:
    if not or_groups:
        raise ValueError("or_groups不能为空")
    dims = [g for g in or_groups if g]
    if not dims:
        raise ValueError("or_groups中没有有效维度")

    rules: List[Dict[str, Any]] = []
    for i, dim_tags in enumerate(dims):
        op = "and" if i < len(dims) - 1 else "noop"
        rules.append({"op": op, "rule": {"audience": [], "tag": list(dim_tags)}})
    return rules


def validate_rules_http(rules: List[Dict[str, Any]]) -> List[str]:
    errors: List[str] = []
    if not isinstance(rules, list) or len(rules) == 0:
        return ["data必须为非空list"]

    for i, r in enumerate(rules):
        op = r.get("op")
        rule = r.get("rule")
        if op not in ("and", "not", "noop"):
            errors.append(f"元素[{i}]: op必须为and/not/noop，got {op}")
        if not isinstance(rule, dict):
            errors.append(f"元素[{i}]: 缺少rule字段")
            continue
        tag = rule.get("tag", [])
        aud = rule.get("audience", [])
        if not tag and not aud:
            errors.append(f"元素[{i}]: rule.tag和rule.audience不能同时为空")
        if isinstance(tag, list) and len(tag) > 100:
            errors.append(f"元素[{i}]: rule.tag最多100个标签")

    if rules and rules[-1].get("op") != "noop":
        errors.append("最后一个元素op必须为noop")
    for i, r in enumerate(rules[:-1]):
        if r.get("op") == "noop":
            errors.append(f"元素[{i}]: noop只能出现在最后一个位置")

    if len(rules) > 50:
        errors.append("规则总数不能超过50个")
    return errors


# -------------------------
# 新版：group嵌套
# -------------------------

def build_grouped_data_http(or_groups: List[List[int]], outer_op: str = "noop") -> List[Dict[str, Any]]:
    if not or_groups:
        raise ValueError("or_groups不能为空")
    dims = [g for g in or_groups if g]
    if not dims:
        raise ValueError("or_groups中没有有效维度")

    group_rules: List[Dict[str, Any]] = []
    for i, dim_tags in enumerate(dims):
        op = "and" if i < len(dims) - 1 else "noop"
        group_rules.append({"op": op, "rule": {"audience": [], "tag": list(dim_tags)}})

    return [{"op": str(outer_op).lower(), "group": group_rules}]


def validate_grouped_data_http(data: List[Dict[str, Any]]) -> List[str]:
    errors: List[str] = []
    if not isinstance(data, list) or len(data) == 0:
        return ["data必须为非空list"]

    for gi, g in enumerate(data):
        op = g.get("op")
        grp = g.get("group")
        if op not in ("and", "or", "not", "noop"):
            errors.append(f"组[{gi}]: op必须为and/or/not/noop，got {op}")
        if not isinstance(grp, list) or len(grp) == 0:
            errors.append(f"组[{gi}]: group必须为非空list")
            continue

        for ri, r in enumerate(grp):
            rop = r.get("op")
            rule = r.get("rule")
            if rop not in ("and", "or", "not", "noop"):
                errors.append(f"组[{gi}]元素[{ri}]: op必须为and/or/not/noop，got {rop}")
            if not isinstance(rule, dict):
                errors.append(f"组[{gi}]元素[{ri}]: 缺少rule字段")
                continue
            tag = rule.get("tag", [])
            aud = rule.get("audience", [])
            if not tag and not aud:
                errors.append(f"组[{gi}]元素[{ri}]: rule.tag和rule.audience不能同时为空")
            if isinstance(tag, list) and len(tag) > 100:
                errors.append(f"组[{gi}]元素[{ri}]: rule.tag最多100个标签")

        if grp and grp[-1].get("op") != "noop":
            errors.append(f"组[{gi}]: group内最后一个元素op必须为noop")

    if data and data[-1].get("op") != "noop":
        errors.append("最外层最后一个组的op必须为noop")

    return errors
