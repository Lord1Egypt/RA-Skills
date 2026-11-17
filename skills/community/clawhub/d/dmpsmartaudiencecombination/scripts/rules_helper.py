#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rules_helper.py

组合人群规则构建工具（统一入口，防止AND/OR格式错误）。

提供两种格式的构建函数：
1. build_rules_http()：HTTP API格式（通过dmp_api_client.py调用）
   格式：[{"op":"and","rule":{"audience":[],"tag":[tid]}}, ..., {"op":"noop","rule":{...}}]
2. build_rules_mcp()：MCP工具格式（通过DMP_MCP__create_combined_audience调用）
   格式：[{"audiences":[],"tags":[...]},{"op":"and"},{"audiences":[],"tags":[...]}]

⚠️ 两种格式不可混用！
- 技能脚本（create_must_baseline/calc_overlap/build_combinations/create_combined_crowd）走HTTP API → 用build_rules_http
- 直接通过MCP工具创建 → 用build_rules_mcp

核心规则：
- 同维度OR的标签放在同一个rule/tag（HTTP）或tags（MCP）数组里
- 跨维度AND用op:"and"连接
- 创建前必须用validate_rules()校验
"""

from typing import Any, Dict, List, Optional


def build_rules_http(or_groups: List[List[int]]) -> List[Dict[str, Any]]:
    """构建HTTP API格式的组合规则（供dmp_api_client.py使用）。
    
    HTTP API格式：
      [{"op":"and","rule":{"audience":[],"tag":[id1,id2]}},  // OR关系
       {"op":"noop","rule":{"audience":[],"tag":[id3]}}]     // 最后一个op=noop
    
    Args:
        or_groups: 二维列表，每个子列表是同维度OR的tagIds。
                   例如 [[15705],[15687,15688,15689],[34080,34082]] 表示
                   女 AND (20-24 OR 25-29 OR 30-34) AND (一线 OR 二线)
    """
    if not or_groups:
        raise ValueError("or_groups不能为空")
    dims = [g for g in or_groups if g]
    if not dims:
        raise ValueError("or_groups中没有有效维度")
    rules = []
    for i, dim_tags in enumerate(dims):
        op = "and" if i < len(dims) - 1 else "noop"
        rules.append({"op": op, "rule": {"audience": [], "tag": list(dim_tags)}})
    return rules


def build_rules_mcp(or_groups: List[List[int]]) -> List[Dict[str, Any]]:
    """构建MCP工具格式的组合规则（供DMP_MCP__create_combined_audience使用）。
    
    MCP格式：
      [{"audiences":[],"tags":[id1,id2]},  // OR关系
       {"op":"and"},
       {"audiences":[],"tags":[id3]}]      // 不需要noop，奇数长度
    
    Args:
        or_groups: 同build_rules_http
    """
    if not or_groups:
        raise ValueError("or_groups不能为空")
    dims = [g for g in or_groups if g]
    if not dims:
        raise ValueError("or_groups中没有有效维度")
    rules = []
    for i, dim_tags in enumerate(dims):
        rules.append({"audiences": [], "tags": list(dim_tags)})
        if i < len(dims) - 1:
            rules.append({"op": "and"})
    return rules


def validate_rules_http(rules: List[Dict]) -> List[str]:
    """校验HTTP API格式规则，返回错误列表（空列表=通过）。"""
    errors = []
    if not isinstance(rules, list) or len(rules) == 0:
        errors.append("data必须为非空list")
        return errors
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
        if len(tag) > 100:
            errors.append(f"元素[{i}]: rule.tag最多100个标签")
    # 最后一个op必须是noop
    if rules and rules[-1].get("op") != "noop":
        errors.append(f"最后一个元素op必须为noop")
    # op=and/not后面不能是最后一个元素
    for i, r in enumerate(rules[:-1]):
        if r.get("op") == "noop":
            errors.append(f"元素[{i}]: noop只能在最后一个位置")
    if len(rules) > 50:
        errors.append(f"规则总数不能超过50个")
    return errors


def validate_rules_mcp(rules: List[Dict]) -> List[str]:
    """校验MCP格式规则，返回错误列表（空列表=通过）。"""
    errors = []
    if not isinstance(rules, list) or len(rules) == 0:
        errors.append("data必须为非空list")
        return errors
    if len(rules) % 2 == 0:
        errors.append(f"规则列表长度必须为奇数（资源-op-资源-...-资源），当前{len(rules)}")
    expect_resource = True
    for i, r in enumerate(rules):
        if expect_resource:
            if "op" in r:
                errors.append(f"元素[{i}]: 应为资源元素，但包含op字段")
            tags = r.get("tags", [])
            auds = r.get("audiences", [])
            if not tags and not auds:
                errors.append(f"元素[{i}]: 资源元素tags和audiences不能同时为空")
            if len(tags) > 100:
                errors.append(f"元素[{i}]: tags最多100个")
        else:
            if r.get("op") not in ("and", "not"):
                errors.append(f"元素[{i}]: 操作元素op必须为and/not")
        expect_resource = not expect_resource
    if len(rules) > 99:
        errors.append(f"规则总数不能超过99个元素")
    return errors


if __name__ == "__main__":
    # 自检
    # HTTP格式：女 AND 美妆个护
    r1 = build_rules_http([[15705], [15564]])
    assert len(r1) == 2 and r1[-1]["op"] == "noop"
    assert not validate_rules_http(r1), f"HTTP校验失败: {validate_rules_http(r1)}"
    # HTTP格式：女 AND (20-24 OR 25-29 OR 30-34) AND (一线 OR 二线)
    r2 = build_rules_http([[15705], [15687,15688,15689], [34080,34082], [15564]])
    assert not validate_rules_http(r2), f"HTTP校验失败: {validate_rules_http(r2)}"
    # MCP格式
    r3 = build_rules_mcp([[15705], [15564]])
    assert len(r3) == 3
    assert not validate_rules_mcp(r3), f"MCP校验失败: {validate_rules_mcp(r3)}"
    r4 = build_rules_mcp([[15705], [15687,15688,15689], [34080,34082], [15564]])
    assert not validate_rules_mcp(r4), f"MCP校验失败: {validate_rules_mcp(r4)}"
    print("✅ rules_helper 所有自检通过")


def validate_selected_groups(selected: Dict[str, List[int]]) -> List[str]:
    """校验用户按维度选择的标签分组是否合理，返回错误列表（空=通过）。
    
    selected格式：{"维度名": [tagId1, tagId2, ...], ...}
    核心校验：
    - 性别维度通常只有1个标签（互斥）
    - 年龄段多个标签是OR（正常）
    - 核心维度（性别/核心兴趣）不能为空
    """
    errors = []
    # 核心维度非空
    for required_dim in ["性别", "核心兴趣"] if "性别" in selected else []:
        if required_dim in selected and not selected[required_dim]:
            errors.append(f"{required_dim}维度不能为空")
    # 性别通常只选一个
    if "性别" in selected and len(selected["性别"]) > 1:
        errors.append(f"性别维度选择了{len(selected['性别'])}个标签（{selected['性别']}），通常只能选一个，是否确认OR关系？")
    # 单维度标签数过多警告
    for dim, tags in selected.items():
        if len(tags) > 10:
            errors.append(f"{dim}维度选择了{len(tags)}个标签，数量过多可能导致人群过小")
    return errors
