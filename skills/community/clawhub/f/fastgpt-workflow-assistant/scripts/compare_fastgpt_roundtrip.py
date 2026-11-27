#!/usr/bin/env python3
"""比较工作流导入前与平台重新导出后的关键结构，发现 Round-trip 漂移。"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from model_bindings import model_bindings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("before", type=Path, help="导入前 JSON")
    parser.add_argument("after", type=Path, help="平台保存后重新导出的 JSON")
    parser.add_argument("--allow-layout-change", action="store_true")
    parser.add_argument("--allow-model-change", action="store_true")
    parser.add_argument("--json", action="store_true", dest="json_output")
    parser.add_argument("--strict", action="store_true", help="把 warning 也视为失败")
    return parser.parse_args()


def load(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: 顶层必须为对象")
    return value


def node_id(node: dict[str, Any]) -> str:
    return str(node.get("nodeId", node.get("id", "")))


def input_value(node: dict[str, Any], key: str) -> Any:
    for item in node.get("inputs", []):
        if isinstance(item, dict) and item.get("key") == key:
            return item.get("value")
    return None


def edge_tuple(edge: dict[str, Any]) -> tuple[str, str, str, str]:
    return tuple(str(edge.get(key, "")) for key in ("source", "target", "sourceHandle", "targetHandle"))  # type: ignore[return-value]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def issue(code: str, severity: str, message: str, suggested_fix: str) -> dict[str, str]:
    return {"code": code, "severity": severity, "message": message, "suggested_fix": suggested_fix}


def compare(before: dict[str, Any], after: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    diagnostics: list[dict[str, str]] = []
    before_nodes = {node_id(node): node for node in before.get("nodes", []) if isinstance(node, dict)}
    after_nodes = {node_id(node): node for node in after.get("nodes", []) if isinstance(node, dict)}
    before_ids, after_ids = set(before_nodes), set(after_nodes)
    if before_ids != after_ids:
        diagnostics.append(issue("RT001", "error", f"节点集合变化；新增={sorted(after_ids-before_ids)}，移除={sorted(before_ids-after_ids)}", "确认是否为预期迁移；否则恢复缺失节点或移除平台自动新增内容"))

    before_edges = {edge_tuple(edge) for edge in before.get("edges", []) if isinstance(edge, dict)}
    after_edges = {edge_tuple(edge) for edge in after.get("edges", []) if isinstance(edge, dict)}
    if before_edges != after_edges:
        diagnostics.append(issue("RT002", "error", f"边四元组变化；新增={sorted(after_edges-before_edges)}，移除={sorted(before_edges-after_edges)}", "对照画布核验 source/target 及两个 Handle"))

    for current_id in sorted(before_ids & after_ids):
        left, right = before_nodes[current_id], after_nodes[current_id]
        if left.get("flowNodeType") != right.get("flowNodeType"):
            diagnostics.append(issue("RT003", "error", f"节点 {current_id} 类型变化：{left.get('flowNodeType')} -> {right.get('flowNodeType')}", "使用目标版本节点重新配置并执行回归"))
        left_keys = sorted(item.get("key") for item in left.get("inputs", []) if isinstance(item, dict) and item.get("key") is not None)
        right_keys = sorted(item.get("key") for item in right.get("inputs", []) if isinstance(item, dict) and item.get("key") is not None)
        if left_keys != right_keys:
            diagnostics.append(issue("RT004", "error", f"节点 {current_id} 输入键变化：{left_keys} -> {right_keys}", "核验版本迁移和变量引用，更新兼容性矩阵"))
        if model_bindings(left) != model_bindings(right) and not args.allow_model_change:
            diagnostics.append(issue("RT005", "error", f"节点 {current_id} 模型绑定变化：{model_bindings(left)} -> {model_bindings(right)}", "核验旧名称与新 ID 的资源映射；恢复原绑定或用 --allow-model-change 接受值变化（不会忽略输入键迁移）"))
        if left.get("position") != right.get("position") and not args.allow_layout_change:
            diagnostics.append(issue("RT006", "warning", f"节点 {current_id} 坐标变化：{left.get('position')} -> {right.get('position')}", "恢复布局或使用 --allow-layout-change 明确接受"))

    counts = Counter(item["severity"] for item in diagnostics)
    return {
        "schema_version": "1.0",
        "summary": {
            "before_sha256": sha256(args.before),
            "after_sha256": sha256(args.after),
            "before_nodes": len(before_nodes),
            "after_nodes": len(after_nodes),
            "before_edges": len(before_edges),
            "after_edges": len(after_edges),
            "diagnostic_counts": dict(counts),
        },
        "diagnostics": diagnostics,
    }


def main() -> int:
    args = parse_args()
    try:
        report = compare(load(args.before), load(args.after), args)
    except Exception as exc:
        report = {"schema_version": "1.0", "summary": {"diagnostic_counts": {"error": 1}}, "diagnostics": [issue("RT000", "error", f"{type(exc).__name__}: {exc}", "检查文件路径、编码和 JSON 语法")]}
    if args.json_output:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
        for item in report["diagnostics"]:
            print(f"[{item['severity'].upper()}][{item['code']}] {item['message']}")
            print(f"  修复建议：{item['suggested_fix']}")
    has_errors = any(item["severity"] == "error" for item in report["diagnostics"])
    has_warnings = any(item["severity"] == "warning" for item in report["diagnostics"])
    return 1 if has_errors or (args.strict and has_warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
