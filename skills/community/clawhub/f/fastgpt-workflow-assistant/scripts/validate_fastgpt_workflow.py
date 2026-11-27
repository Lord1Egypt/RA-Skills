#!/usr/bin/env python3
"""离线校验 FastGPT/兼容平台导出的工作流 JSON，并输出稳定诊断码。"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import tempfile
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Any

from model_bindings import collect_model_bindings
from node_schema_checks import check as check_node_schema


SYSTEM_TYPES = {"userGuide", "systemConfig"}
SPECIAL_REFERENCE_IDS = {"VARIABLE_NODE_ID", "SYSTEM_VARIABLE_NODE_ID"}
SECRET_PATTERNS = [
    re.compile(r"\bBearer\s+(?!\{\{)[A-Za-z0-9._~-]{16,}", re.I),
    re.compile(r"\bsk-[A-Za-z0-9_-]{16,}"),
    re.compile(r"\bfastgpt-[A-Za-z0-9_-]{12,}", re.I),
    re.compile(r"\b(?:api[_-]?key|token|secret)\s*[:=]\s*[\"']?[A-Za-z0-9._~-]{16,}", re.I),
]
VARIABLE_REF_PATTERN = re.compile(r"\{\{([^{}]*?)\}\}")
VERSION_LABEL_PATTERN = re.compile(r"(?i)(?<![A-Za-z0-9])V?(\d+\.\d+(?:\.\d+)?)(?![A-Za-z0-9])")
CODE_NODE_TYPES = {"code", "coderun", "sandbox"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workflow", type=Path, help="工作流导出 JSON")
    parser.add_argument("--http-contract", type=Path, help="核对门禁与HTTP地址来源及异常出口的显式合同")
    parser.add_argument("--schema-baseline", type=Path, help="只读节点类型基线；未知扩展给出待核对警告")
    parser.add_argument("--baseline", type=Path, help="用于继承比较的上一版导出 JSON")
    parser.add_argument("--expect-preserve-layout", action="store_true", help="要求原节点坐标不变")
    parser.add_argument("--expect-preserve-models", action="store_true", help="要求模型配置不变")
    parser.add_argument("--node", help="用于 JavaScript 语法检查的 Node.js 可执行文件")
    parser.add_argument("--expected-app-version", help="检查全局变量显示标签中的应用版本，例如V3.5.14")
    parser.add_argument("--json", action="store_true", dest="json_output", help="输出机器可读 JSON")
    parser.add_argument("--strict", action="store_true", help="把 warning 也视为失败")
    return parser.parse_args()


def issue(
    code: str,
    severity: str,
    message: str,
    *,
    path: str = "$",
    node_id: str | None = None,
    suggested_fix: str = "",
) -> dict[str, Any]:
    item: dict[str, Any] = {
        "code": code,
        "severity": severity,
        "message": message,
        "path": path,
        "suggested_fix": suggested_fix,
    }
    if node_id:
        item["node_id"] = node_id
    return item


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as stream:
        data = json.load(stream)
    if not isinstance(data, dict):
        raise ValueError("顶层 JSON 必须是对象")
    return data


def node_id(node: dict[str, Any]) -> str:
    value = node.get("nodeId", node.get("id", ""))
    return str(value) if value is not None else ""


def edge_tuple(edge: dict[str, Any]) -> tuple[str, str, str, str]:
    return (
        str(edge.get("source", "")),
        str(edge.get("target", "")),
        str(edge.get("sourceHandle", "")),
        str(edge.get("targetHandle", "")),
    )


def input_value(node: dict[str, Any], key: str) -> Any:
    for item in node.get("inputs", []):
        if isinstance(item, dict) and item.get("key") == key:
            return item.get("value")
    return None


def collect_models(nodes: list[dict[str, Any]]) -> dict[str, str]:
    result: dict[str, str] = {}
    for node in nodes:
        value = input_value(node, "modelId")
        if value is None:
            value = input_value(node, "model")
        if isinstance(value, str) and value:
            result[node_id(node)] = value
    return result


def scan_strings(value: Any, path: str = "$"):
    if isinstance(value, str):
        yield path, value
    elif isinstance(value, dict):
        for key, child in value.items():
            yield from scan_strings(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from scan_strings(child, f"{path}[{index}]")


def normalize_app_version(value: str) -> str:
    match = VERSION_LABEL_PATTERN.search(str(value or "").strip())
    if not match:
        raise ValueError(f"无法解析应用版本：{value!r}，示例为V3.5.14")
    return match.group(1)


def validate_global_variable_versions(data: dict[str, Any], expected: str | None) -> list[dict[str, Any]]:
    if not expected:
        return []
    expected_normalized = normalize_app_version(expected)
    variables = data.get("chatConfig", {}).get("variables", [])
    if isinstance(variables, dict):
        variables = [variables]
    if not isinstance(variables, list):
        return [issue("FG084", "warning", "chatConfig.variables不是对象数组，无法检查全局变量版本标签", path="$.chatConfig.variables")]
    diagnostics: list[dict[str, Any]] = []
    for index, variable in enumerate(variables):
        if not isinstance(variable, dict):
            continue
        label = str(variable.get("label", ""))
        versions = {match.group(1) for match in VERSION_LABEL_PATTERN.finditer(label)}
        stale = sorted(version for version in versions if version != expected_normalized)
        if stale:
            key = str(variable.get("key", ""))
            diagnostics.append(issue(
                "FG084",
                "warning",
                f"全局变量显示标签仍包含旧版本{stale}，期望V{expected_normalized}；机器键{key!r}应保持稳定",
                path=f"$.chatConfig.variables[{index}].label",
                suggested_fix=f"只更新显示标签中的版本为V{expected_normalized}，不要在没有迁移方案时重命名变量key",
            ))
    return diagnostics


def compile_code_nodes(nodes: list[dict[str, Any]], node_executable: str | None) -> tuple[int, list[dict[str, Any]]]:
    diagnostics: list[dict[str, Any]] = []
    checked = 0
    node_path = node_executable or shutil.which("node")

    for index, node in enumerate(nodes):
        if str(node.get("flowNodeType", "")).lower() not in {"code", "coderun", "sandbox"}:
            continue
        current_id = node_id(node)
        code = input_value(node, "code")
        code_type = str(input_value(node, "codeType") or "js").lower()
        item_path = f"$.nodes[{index}].inputs"
        if not isinstance(code, str) or not code.strip():
            diagnostics.append(issue("FG070", "error", "代码节点没有代码", path=item_path, node_id=current_id, suggested_fix="填写代码或移除该节点"))
            continue
        if code_type in {"python", "py"}:
            try:
                compile(code, f"<{current_id}>", "exec")
                checked += 1
            except SyntaxError as exc:
                diagnostics.append(issue("FG071", "error", f"Python 语法错误：第 {exc.lineno} 行，{exc.msg}", path=item_path, node_id=current_id, suggested_fix="修复语法后重新校验"))
        elif code_type in {"js", "javascript"}:
            if not node_path:
                diagnostics.append(issue("FG072", "warning", "未找到 Node.js，已跳过 JavaScript 语法检查", path=item_path, node_id=current_id, suggested_fix="安装 Node.js 或通过 --node 指定可执行文件"))
                continue
            with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".js", delete=False) as stream:
                stream.write(code)
                temp_path = Path(stream.name)
            try:
                process = subprocess.run(
                    [node_path, "--check", str(temp_path)],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    timeout=20,
                )
                if process.returncode:
                    detail = (process.stderr or process.stdout).strip().splitlines()
                    diagnostics.append(issue("FG071", "error", f"JavaScript 语法错误：{' | '.join(detail[-3:])}", path=item_path, node_id=current_id, suggested_fix="修复语法后重新校验"))
                else:
                    checked += 1
            finally:
                temp_path.unlink(missing_ok=True)
        else:
            diagnostics.append(issue("FG073", "warning", f"暂不支持检查代码类型 {code_type!r}", path=item_path, node_id=current_id, suggested_fix="在目标平台手工验证该代码节点"))
    return checked, diagnostics


def get_code_outputs(node: dict[str, Any]) -> list[dict[str, Any]]:
    """从代码节点获取输出声明，优先读取顶层 outputs 字段，回退到 inputs。"""
    raw_outputs = node.get("outputs")
    if not isinstance(raw_outputs, list):
        raw_outputs = input_value(node, "outputs") or []
    if not isinstance(raw_outputs, list):
        return []
    return [item for item in raw_outputs if isinstance(item, dict)]


def collect_code_outputs(nodes: list[dict[str, Any]]) -> dict[str, set[str]]:
    """收集所有代码节点声明的输出变量名映射，用于校验跨节点变量引用。"""
    outputs_map: dict[str, set[str]] = {}
    for node in nodes:
        if str(node.get("flowNodeType", "")).lower() not in CODE_NODE_TYPES:
            continue
        current_id = node_id(node)
        names = {str(item.get("key", "")) for item in get_code_outputs(node)}
        outputs_map[current_id] = {name for name in names if name}
    return outputs_map


def parse_variable_refs(text: str) -> list[tuple[str, str, bool]]:
    """解析文本中的 {{...}} 变量引用，返回 (nodeId, varName, hasDollarSyntax) 列表。"""
    refs: list[tuple[str, str, bool]] = []
    for match in VARIABLE_REF_PATTERN.finditer(text):
        body = match.group(1).strip()
        if "." not in body:
            continue
        has_dollar = body.startswith("$") and body.endswith("$") and len(body) > 2
        inner = body[1:-1].strip() if has_dollar else body
        if "." not in inner:
            continue
        parts = inner.split(".", 1)
        refs.append((parts[0].strip(), parts[1].strip(), has_dollar))
    return refs


def validate_variable_references(
    nodes: list[dict[str, Any]],
    id_set: set[str],
    code_outputs: dict[str, set[str]],
) -> list[dict[str, Any]]:
    """扫描所有节点的字符串输入，校验跨节点变量引用语法与目标存在性。"""
    diagnostics: list[dict[str, Any]] = []
    for node_index, node in enumerate(nodes):
        current_id = node_id(node)
        for input_index, item in enumerate(node.get("inputs", [])):
            value = item.get("value") if isinstance(item, dict) else None
            if not isinstance(value, str):
                continue
            diagnostics.extend(
                _check_single_ref(value, node_index, input_index, current_id, id_set, code_outputs)
            )
    return diagnostics


def _check_single_ref(
    value: str,
    node_index: int,
    input_index: int,
    current_id: str,
    id_set: set[str],
    code_outputs: dict[str, set[str]],
) -> list[dict[str, Any]]:
    """对单个输入值中的所有变量引用生成诊断条目。"""
    items: list[dict[str, Any]] = []
    item_path = f"$.nodes[{node_index}].inputs[{input_index}].value"
    for ref_node, ref_var, has_dollar in parse_variable_refs(value):
        if not ref_node or not ref_var:
            items.append(issue("FG083", "error", f"变量引用缺少 nodeId 或 varName：{ref_node!r}.{ref_var!r}", path=item_path, node_id=current_id, suggested_fix="补全引用格式为 {{$nodeId.varName$}}"))
            continue
        if not has_dollar:
            items.append(issue("FG080", "warning", f"跨节点引用建议使用 {{{{$...$}}}} 语法：{{{{{ref_node}.{ref_var}}}}}", path=item_path, node_id=current_id, suggested_fix=f"改为 {{{{${ref_node}.{ref_var}$}}}}"))
        elif ref_node not in id_set:
            items.append(issue("FG081", "error", f"变量引用未知节点：{ref_node!r}", path=item_path, node_id=current_id, suggested_fix="修正节点 ID 或恢复上游节点"))
        elif ref_node in code_outputs and ref_var not in code_outputs[ref_node]:
            items.append(issue("FG082", "error", f"变量引用未声明的输出：{ref_node}.{ref_var}", path=item_path, node_id=current_id, suggested_fix=f"在节点 {ref_node} 的 outputs 中声明 {ref_var}"))
    return items


def validate(data: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    diagnostics: list[dict[str, Any]] = []
    nodes_raw = data.get("nodes")
    edges_raw = data.get("edges")
    if not isinstance(nodes_raw, list):
        diagnostics.append(issue("FG001", "error", "顶层 nodes 必须是数组", path="$.nodes", suggested_fix="从目标平台重新导出工作流基线"))
        nodes_raw = []
    if not isinstance(edges_raw, list):
        diagnostics.append(issue("FG002", "error", "顶层 edges 必须是数组", path="$.edges", suggested_fix="从目标平台重新导出工作流基线"))
        edges_raw = []

    # Target UI treats a blank manual variable assignment as a missing required value.
    for ni, node in enumerate(nodes_raw):
        if not isinstance(node, dict) or node.get("flowNodeType") != "variableUpdate":
            continue
        for ii, param in enumerate(node.get("inputs") or []):
            if param.get("key") != "updateList" or not isinstance(param.get("value"), list):
                continue
            for ui, update in enumerate(param["value"]):
                if not isinstance(update, dict) or update.get("renderType") != "input":
                    continue
                value = update.get("value")
                if value is None or isinstance(value, str) and not value.strip():
                    diagnostics.append(issue("FG085", "error", "变量更新的必填手动输入值为空", path=f"$.nodes[{ni}].inputs[{ii}].value[{ui}].value", node_id=node_id(node), suggested_fix="使用符合类型和下游解析的非空初始值，或引用已声明输出；到目标平台保存并回导验证"))

    nodes = [item for item in nodes_raw if isinstance(item, dict)]
    edges = [item for item in edges_raw if isinstance(item, dict)]
    if len(nodes) != len(nodes_raw):
        diagnostics.append(issue("FG010", "error", "一个或多个节点不是对象", path="$.nodes", suggested_fix="移除非法条目或重新导出"))
    if len(edges) != len(edges_raw):
        diagnostics.append(issue("FG010", "error", "一个或多个边不是对象", path="$.edges", suggested_fix="移除非法条目或重新导出"))

    ids = [node_id(node) for node in nodes]
    for index, current_id in enumerate(ids):
        if not current_id:
            diagnostics.append(issue("FG011", "error", "节点缺少 nodeId/id", path=f"$.nodes[{index}]", suggested_fix="从目标版本基线恢复节点 ID"))
    for duplicate in sorted(key for key, count in Counter(ids).items() if key and count > 1):
        diagnostics.append(issue("FG012", "error", f"节点 ID 重复：{duplicate}", path="$.nodes", node_id=duplicate, suggested_fix="为重复节点分配唯一 ID 并修复所有引用和连线"))
    id_set = {value for value in ids if value}

    edge_tuples = [edge_tuple(edge) for edge in edges]
    for duplicate in [item for item, count in Counter(edge_tuples).items() if count > 1]:
        diagnostics.append(issue("FG020", "error", f"边重复：{duplicate}", path="$.edges", suggested_fix="保留一条并确认 Handle 语义"))
    for index, (source, target, source_handle, target_handle) in enumerate(edge_tuples):
        path = f"$.edges[{index}]"
        if source not in id_set:
            diagnostics.append(issue("FG021", "error", f"边引用不存在的源节点：{source!r}", path=path, suggested_fix="修正 source 或恢复缺失节点"))
        if target not in id_set:
            diagnostics.append(issue("FG021", "error", f"边引用不存在的目标节点：{target!r}", path=path, suggested_fix="修正 target 或恢复缺失节点"))
        if source and source == target:
            diagnostics.append(issue("FG022", "warning", f"发现自环边：{source!r}", path=path, node_id=source, suggested_fix="确认循环是否由目标版本节点机制明确支持"))
        if not source_handle or not target_handle:
            diagnostics.append(issue("FG023", "warning", f"边 {source!r}->{target!r} 的 Handle 为空", path=path, suggested_fix="对照目标版本导出物核验 Handle"))

    starts = [node for node in nodes if "workflowstart" in str(node.get("flowNodeType", "")).lower()]
    if not starts:
        diagnostics.append(issue("FG030", "error", "未找到 workflowStart 节点", path="$.nodes", suggested_fix="恢复目标版本的开始节点"))
    elif len(starts) > 1:
        diagnostics.append(issue("FG031", "warning", f"发现多个 workflowStart 节点：{[node_id(node) for node in starts]}", path="$.nodes", suggested_fix="确认目标应用模式是否允许多个开始节点"))

    adjacency: dict[str, list[str]] = defaultdict(list)
    incoming: Counter[str] = Counter()
    for source, target, _, _ in edge_tuples:
        adjacency[source].append(target)
        incoming[target] += 1
    # loopRun enters its exported loopRunStart child without a canvas edge.
    # Require both ownership records; do not exempt arbitrary orphan children.
    node_by_id = {node_id(node): node for node in nodes}
    for child in nodes:
        if child.get("flowNodeType") != "loopRunStart":
            continue
        parent_id = child.get("parentNodeId")
        parent = node_by_id.get(parent_id, {})
        listed = next((item.get("value") for item in parent.get("inputs", [])
                       if item.get("key") == "childrenNodeIdList"), [])
        if parent.get("flowNodeType") == "loopRun" and isinstance(listed, list) and node_id(child) in listed:
            adjacency[parent_id].append(node_id(child))
            incoming[node_id(child)] += 1
    reachable: set[str] = set()
    queue = deque(node_id(node) for node in starts)
    while queue:
        current = queue.popleft()
        if current in reachable:
            continue
        reachable.add(current)
        queue.extend(adjacency.get(current, []))

    business_nodes = [
        node for node in nodes
        if str(node.get("flowNodeType", "")) not in SYSTEM_TYPES
        and "系统配置" not in str(node.get("name", ""))
    ]
    unreachable = [node_id(node) for node in business_nodes if node_id(node) not in reachable]
    if unreachable:
        diagnostics.append(issue("FG032", "error", f"业务节点无法从开始节点到达：{unreachable}", path="$.nodes", suggested_fix="修复连线或移除无用节点；注意未执行节点也可能影响平台校验"))
    no_incoming = [node_id(node) for node in business_nodes if node not in starts and incoming[node_id(node)] == 0]
    if no_incoming:
        diagnostics.append(issue("FG033", "error", f"业务节点没有入边：{no_incoming}", path="$.nodes", suggested_fix="补充连线或移除孤立节点"))

    coordinates: dict[tuple[Any, Any], list[str]] = defaultdict(list)
    for index, node in enumerate(nodes):
        position = node.get("position")
        current_id = node_id(node)
        if not isinstance(position, dict) or "x" not in position or "y" not in position:
            diagnostics.append(issue("FG040", "warning", "节点缺少完整坐标", path=f"$.nodes[{index}].position", node_id=current_id, suggested_fix="从基线恢复坐标或在画布中重新布局"))
            continue
        coordinates[(position.get("x"), position.get("y"))].append(current_id)
    for coordinate, overlapping in coordinates.items():
        if len(overlapping) > 1:
            diagnostics.append(issue("FG041", "warning", f"节点坐标精确重叠 {coordinate}：{overlapping}", path="$.nodes", suggested_fix="为新增分支预留空间并调整坐标"))

    for node_index, node in enumerate(nodes):
        for input_index, item in enumerate(node.get("inputs", [])):
            if not isinstance(item, dict) or "reference" not in item.get("renderTypeList", []):
                continue
            value = item.get("value")
            if not (isinstance(value, list) and value and isinstance(value[0], str)):
                continue
            source = value[0]
            if source not in id_set and source not in SPECIAL_REFERENCE_IDS:
                diagnostics.append(issue("FG050", "error", f"输入引用未知节点：{source}", path=f"$.nodes[{node_index}].inputs[{input_index}]", node_id=node_id(node), suggested_fix="修正引用节点 ID 或恢复上游节点"))

    for path, value in scan_strings(data):
        if any(pattern.search(value) for pattern in SECRET_PATTERNS):
            diagnostics.append(issue("FG060", "warning", "疑似硬编码密钥；未输出实际值", path=path, suggested_fix="改用平台凭据系统或受保护变量，并轮换已暴露凭据"))

    schema_path = getattr(args, "schema_baseline", None)
    diagnostics.extend(check_node_schema(nodes, edges, load_json(schema_path) if schema_path else None))
    http_contract = getattr(args, "http_contract", None)
    if http_contract:
        from check_http_contract import check as check_http
        http_report = check_http(data, load_json(http_contract))
        for case in http_report["cases"]:
            for error in case["errors"]:
                diagnostics.append(issue("FG098", "error", "HTTP执行合同不满足：" + error, suggested_fix="核对门禁与请求配置来源、异常输出和catch边；平台URL引用能力另行验证"))


    checked_code, code_diagnostics = compile_code_nodes(nodes, args.node)
    diagnostics.extend(code_diagnostics)

    code_outputs = collect_code_outputs(nodes)
    diagnostics.extend(validate_variable_references(nodes, id_set, code_outputs))
    diagnostics.extend(validate_global_variable_versions(data, args.expected_app_version))

    baseline_summary: dict[str, Any] | None = None
    if args.baseline:
        baseline = load_json(args.baseline)
        base_nodes = [item for item in baseline.get("nodes", []) if isinstance(item, dict)]
        base_edges = [item for item in baseline.get("edges", []) if isinstance(item, dict)]
        base_by_id = {node_id(node): node for node in base_nodes}
        current_by_id = {node_id(node): node for node in nodes}
        moved = sorted(current_id for current_id in set(base_by_id) & id_set if base_by_id[current_id].get("position") != current_by_id[current_id].get("position"))
        base_models = collect_model_bindings(base_nodes)
        current_models = collect_model_bindings(nodes)
        model_changes = {
            current_id: {"before": base_models.get(current_id), "after": current_models.get(current_id)}
            for current_id in sorted(set(base_models) | set(current_models))
            if base_models.get(current_id) != current_models.get(current_id)
        }
        base_edges_set = {edge_tuple(edge) for edge in base_edges}
        current_edges_set = set(edge_tuples)
        baseline_summary = {
            "added_nodes": sorted(id_set - set(base_by_id)),
            "removed_nodes": sorted(set(base_by_id) - id_set),
            "moved_nodes": moved,
            "model_changes": model_changes,
            "added_edges": sorted(current_edges_set - base_edges_set),
            "removed_edges": sorted(base_edges_set - current_edges_set),
        }
        if args.expect_preserve_layout and moved:
            diagnostics.append(issue("FG101", "error", f"要求保留布局，但节点发生移动：{moved}", path="$.nodes", suggested_fix="恢复原坐标或取消不适用的布局保留要求"))
        if args.expect_preserve_models and model_changes:
            diagnostics.append(issue("FG102", "error", f"要求保留模型，但配置发生变化：{model_changes}", path="$.nodes", suggested_fix="恢复模型值或明确记录并接受模型变更"))
    elif args.expect_preserve_layout or args.expect_preserve_models:
        diagnostics.append(issue("FG103", "error", "布局/模型保留检查需要 --baseline", suggested_fix="提供上一版导出 JSON"))

    counts = Counter(item["severity"] for item in diagnostics)
    var_ref_codes = {"FG080", "FG081", "FG082", "FG083"}
    summary = {
        "nodes": len(nodes),
        "edges": len(edges),
        "start_nodes": len(starts),
        "business_nodes": len(business_nodes),
        "reachable_business_nodes": len(business_nodes) - len(unreachable),
        "code_nodes_syntax_checked": checked_code,
        "code_nodes_with_outputs": len(code_outputs),
        "variable_ref_issues": sum(1 for item in diagnostics if item["code"] in var_ref_codes),
        "global_variable_version_issues": sum(1 for item in diagnostics if item["code"] == "FG084"),
        "models": collect_models(nodes),
        "model_bindings": collect_model_bindings(nodes),
        "baseline": baseline_summary,
        "diagnostic_counts": dict(counts),
    }
    return {"schema_version": "1.0", "summary": summary, "diagnostics": diagnostics}


def main() -> int:
    args = parse_args()
    try:
        report = validate(load_json(args.workflow), args)
    except Exception as exc:
        report = {
            "schema_version": "1.0",
            "summary": {"diagnostic_counts": {"error": 1}},
            "diagnostics": [issue("FG000", "error", f"{type(exc).__name__}: {exc}", suggested_fix="检查文件路径、UTF-8 编码和 JSON 语法")],
        }

    if args.json_output:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
        for item in report["diagnostics"]:
            location = item.get("node_id") or item.get("path") or "$"
            print(f"[{item['severity'].upper()}][{item['code']}][{location}] {item['message']}")
            if item.get("suggested_fix"):
                print(f"  修复建议：{item['suggested_fix']}")

    has_errors = any(item["severity"] == "error" for item in report["diagnostics"])
    has_warnings = any(item["severity"] == "warning" for item in report["diagnostics"])
    return 1 if has_errors or (args.strict and has_warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
