#!/usr/bin/env python3
"""对比两个工作流导出 JSON 的版本差异，输出结构化变更报告。"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    """解析命令行参数：旧版、新版、输出格式。"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("old", type=Path, help="旧版工作流 JSON")
    parser.add_argument("new", type=Path, help="新版工作流 JSON")
    parser.add_argument("--json", action="store_true", dest="json_output", help="输出机器可读 JSON")
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    """读取工作流 JSON 并校验顶层结构。"""
    with path.open("r", encoding="utf-8-sig") as stream:
        data = json.load(stream)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: 顶层必须是对象")
    return data


def node_id(node: dict[str, Any]) -> str:
    """从节点对象中提取稳定 nodeId。"""
    value = node.get("nodeId", node.get("id", ""))
    return str(value) if value is not None else ""


def edge_tuple(edge: dict[str, Any]) -> tuple[str, str, str, str]:
    """将边对象归一为四元组以便集合比较。"""
    return (
        str(edge.get("source", "")),
        str(edge.get("target", "")),
        str(edge.get("sourceHandle", "")),
        str(edge.get("targetHandle", "")),
    )


def collect_nodes(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """构建 nodeId 到节点对象的映射。"""
    nodes = [item for item in data.get("nodes", []) if isinstance(item, dict)]
    return {node_id(node): node for node in nodes if node_id(node)}


def collect_edges(data: dict[str, Any]) -> set[tuple[str, str, str, str]]:
    """收集边的四元组集合。"""
    edges = [item for item in data.get("edges", []) if isinstance(item, dict)]
    return {edge_tuple(edge) for edge in edges}


def hash_code(code: str) -> str:
    """计算代码内容的短哈希，用于检测代码是否变更。"""
    return hashlib.sha256(code.encode("utf-8")).hexdigest()[:12] if code else ""


def stable_hash(value: Any) -> str:
    """对结构化值计算短哈希，报告差异但不回显可能含敏感信息的原值。"""
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:12]


def input_map(node: dict[str, Any]) -> dict[str, Any]:
    """提取有 key 的输入项；同一 key 重复时保留完整值列表。"""
    collected: dict[str, list[Any]] = {}
    for item in node.get("inputs", []):
        if not isinstance(item, dict) or not str(item.get("key", "")):
            continue
        collected.setdefault(str(item["key"]), []).append(item.get("value"))
    return {key: values[0] if len(values) == 1 else values for key, values in collected.items()}


def output_keys(node: dict[str, Any]) -> list[str]:
    raw = node.get("outputs", []) if isinstance(node.get("outputs"), list) else []
    return sorted(str(item.get("key", "")) for item in raw if isinstance(item, dict) and item.get("key"))


def extract_code_info(node: dict[str, Any]) -> dict[str, Any]:
    """从代码节点中提取代码哈希和输出声明。"""
    inputs = node.get("inputs", []) if isinstance(node.get("inputs"), list) else []
    code = ""
    for item in inputs:
        if isinstance(item, dict) and item.get("key") == "code":
            code = str(item.get("value", ""))
            break
    outputs = []
    raw_outputs = node.get("outputs", []) if isinstance(node.get("outputs"), list) else []
    for item in raw_outputs:
        if isinstance(item, dict):
            outputs.append(str(item.get("key", "")))
    return {"code_hash": hash_code(code), "outputs": sorted(outputs)}


def compare_node_details(
    node_id_str: str,
    old_node: dict[str, Any],
    new_node: dict[str, Any],
) -> list[str]:
    """比较单个节点的关键字段变更，返回变更描述列表。"""
    changes: list[str] = []
    if old_node.get("name") != new_node.get("name"):
        changes.append(f"name: {old_node.get('name')!r} -> {new_node.get('name')!r}")
    if old_node.get("flowNodeType") != new_node.get("flowNodeType"):
        changes.append(f"flowNodeType: {old_node.get('flowNodeType')} -> {new_node.get('flowNodeType')}")
    old_pos = old_node.get("position", {})
    new_pos = new_node.get("position", {})
    if old_pos != new_pos:
        changes.append(f"position: {old_pos} -> {new_pos}")
    old_model = _get_input_value(old_node, "model")
    new_model = _get_input_value(new_node, "model")
    if old_model != new_model:
        changes.append(f"model: {old_model!r} -> {new_model!r}")
    old_inputs = input_map(old_node)
    new_inputs = input_map(new_node)
    for key in sorted(set(old_inputs) | set(new_inputs)):
        if key in {"code", "model"}:
            continue
        old_value = old_inputs.get(key)
        new_value = new_inputs.get(key)
        if stable_hash(old_value) != stable_hash(new_value):
            changes.append(f"input:{key}_hash: {stable_hash(old_value)} -> {stable_hash(new_value)}")
    old_outputs = output_keys(old_node)
    new_outputs = output_keys(new_node)
    if old_outputs != new_outputs:
        changes.append(f"outputs: {old_outputs} -> {new_outputs}")
    if str(old_node.get("flowNodeType", "")).lower() in {"code", "coderun", "sandbox"}:
        old_info = extract_code_info(old_node)
        new_info = extract_code_info(new_node)
        if old_info["code_hash"] != new_info["code_hash"]:
            changes.append(f"code_hash: {old_info['code_hash']} -> {new_info['code_hash']}")
    return changes


def _get_input_value(node: dict[str, Any], key: str) -> Any:
    """从节点 inputs 列表中按 key 取值。"""
    for item in node.get("inputs", []):
        if isinstance(item, dict) and item.get("key") == key:
            return item.get("value")
    return None


def build_diff(old_data: dict[str, Any], new_data: dict[str, Any]) -> dict[str, Any]:
    """构建完整的版本差异报告。"""
    old_nodes = collect_nodes(old_data)
    new_nodes = collect_nodes(new_data)
    old_edges = collect_edges(old_data)
    new_edges = collect_edges(new_data)
    added_nodes = sorted(set(new_nodes) - set(old_nodes))
    removed_nodes = sorted(set(old_nodes) - set(new_nodes))
    common_nodes = sorted(set(old_nodes) & set(new_nodes))
    old_node_ids = [node_id(item) for item in old_data.get("nodes", []) if isinstance(item, dict) and node_id(item)]
    new_node_ids = [node_id(item) for item in new_data.get("nodes", []) if isinstance(item, dict) and node_id(item)]
    old_edge_items = [edge_tuple(item) for item in old_data.get("edges", []) if isinstance(item, dict)]
    new_edge_items = [edge_tuple(item) for item in new_data.get("edges", []) if isinstance(item, dict)]
    node_changes: dict[str, list[str]] = {}
    for nid in common_nodes:
        changes = compare_node_details(nid, old_nodes[nid], new_nodes[nid])
        if changes:
            node_changes[nid] = changes
    summary = {
        "old_node_count": len(old_nodes),
        "new_node_count": len(new_nodes),
        "old_edge_count": len(old_edges),
        "new_edge_count": len(new_edges),
        "added_nodes": added_nodes,
        "removed_nodes": removed_nodes,
        "changed_nodes": node_changes,
        "changed_node_count": len(node_changes),
        "added_edges": sorted(new_edges - old_edges),
        "removed_edges": sorted(old_edges - new_edges),
        "duplicate_node_ids": {
            "old": sorted(key for key, value in Counter(old_node_ids).items() if value > 1),
            "new": sorted(key for key, value in Counter(new_node_ids).items() if value > 1),
        },
        "duplicate_edges": {
            "old": sorted(key for key, value in Counter(old_edge_items).items() if value > 1),
            "new": sorted(key for key, value in Counter(new_edge_items).items() if value > 1),
        },
        "chat_config_changed": stable_hash(old_data.get("chatConfig")) != stable_hash(new_data.get("chatConfig")),
        "chat_config_hash": {
            "old": stable_hash(old_data.get("chatConfig")),
            "new": stable_hash(new_data.get("chatConfig")),
        },
    }
    return summary


def print_report(diff: dict[str, Any]) -> None:
    """以人类可读格式输出差异摘要。"""
    print(f"节点：{diff['old_node_count']} -> {diff['new_node_count']}")
    print(f"边：{diff['old_edge_count']} -> {diff['new_edge_count']}")
    if diff["added_nodes"]:
        print(f"新增节点：{diff['added_nodes']}")
    if diff["removed_nodes"]:
        print(f"删除节点：{diff['removed_nodes']}")
    if diff["changed_nodes"]:
        print("节点变更：")
        for nid, changes in diff["changed_nodes"].items():
            print(f"  {nid}:")
            for change in changes:
                print(f"    - {change}")
    if diff["added_edges"]:
        print(f"新增边：{diff['added_edges']}")
    if diff["removed_edges"]:
        print(f"删除边：{diff['removed_edges']}")
    if diff["chat_config_changed"]:
        print("chatConfig：已变更（仅报告哈希，不回显内容）")
    if diff["duplicate_node_ids"]["old"] or diff["duplicate_node_ids"]["new"]:
        print(f"重复节点 ID：{diff['duplicate_node_ids']}")
    if diff["duplicate_edges"]["old"] or diff["duplicate_edges"]["new"]:
        print(f"重复边：{diff['duplicate_edges']}")


def main() -> int:
    """主入口：读取两版 JSON、构建差异、输出报告。"""
    args = parse_args()
    try:
        old_data = load_json(args.old)
        new_data = load_json(args.new)
        diff = build_diff(old_data, new_data)
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}: {exc}")
        return 1
    if args.json_output:
        print(json.dumps(diff, ensure_ascii=False, indent=2))
    else:
        print_report(diff)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
