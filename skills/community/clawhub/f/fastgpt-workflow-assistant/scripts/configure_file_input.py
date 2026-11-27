#!/usr/bin/env python3
"""为 FastGPT 工作流补齐文件上传配置和 userFiles 引用。"""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any


USER_FILES_OUTPUT = {
    "id": "userFiles",
    "key": "userFiles",
    "label": "app:workflow.user_file_input",
    "description": "app:workflow.user_file_input_desc",
    "type": "static",
    "valueType": "arrayString",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_json", type=Path)
    parser.add_argument("output_json", type=Path)
    parser.add_argument("--start-node-id", default="", help="开始节点ID；留空时自动定位唯一 workflowStart")
    parser.add_argument("--gate-node-id", default="", help="可选：需要绑定 userFiles 非空条件的判断节点ID")
    parser.add_argument("--ai-node-id", action="append", default=[], help="可重复：需要绑定文件链接的AI节点ID")
    parser.add_argument("--max-files", type=int, default=None, help="最大文件数；留空时保留现值，缺失配置时默认10")
    image_group = parser.add_mutually_exclusive_group()
    image_group.add_argument("--enable-images", dest="images", action="store_true")
    image_group.add_argument("--disable-images", dest="images", action="store_false")
    parser.set_defaults(images=None)
    pdf_group = parser.add_mutually_exclusive_group()
    pdf_group.add_argument("--pdf-enhanced", dest="pdf_enhanced", action="store_true")
    pdf_group.add_argument("--no-pdf-enhanced", dest="pdf_enhanced", action="store_false")
    parser.set_defaults(pdf_enhanced=None)
    parser.add_argument("--custom-extension", action="append", default=[], help="可重复，例如 xls；仅允许上传，不保证可解析")
    parser.add_argument("--clear-custom-extensions", action="store_true")
    parser.add_argument("--force", action="store_true", help="允许覆盖输出文件")
    parser.add_argument("--json", action="store_true", help="输出机器可读摘要")
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict) or not isinstance(value.get("nodes"), list):
        raise ValueError("输入必须是包含 nodes 数组的工作流 JSON")
    return value


def find_node(workflow: dict[str, Any], node_id: str, flow_type: str | None = None) -> dict[str, Any]:
    nodes = workflow["nodes"]
    if node_id:
        matches = [node for node in nodes if node.get("nodeId") == node_id]
    else:
        matches = [node for node in nodes if node.get("flowNodeType") == flow_type]
    if len(matches) != 1:
        label = node_id or flow_type
        raise ValueError(f"节点定位必须唯一：{label!r}，实际 {len(matches)} 个")
    return matches[0]


def set_or_append_input(node: dict[str, Any], key: str, value: Any, template: dict[str, Any]) -> None:
    inputs = node.setdefault("inputs", [])
    matches = [item for item in inputs if item.get("key") == key]
    if len(matches) > 1:
        raise ValueError(f"节点 {node.get('nodeId')} 存在重复输入键 {key}")
    if matches:
        matches[0]["value"] = copy.deepcopy(value)
        return
    item = copy.deepcopy(template)
    item["key"] = key
    item["value"] = copy.deepcopy(value)
    inputs.append(item)


def normalize_extensions(values: list[str]) -> list[str]:
    output: list[str] = []
    for value in values:
        extension = value.strip().lower().lstrip(".")
        if not extension:
            continue
        if not extension.replace("-", "").replace("_", "").isalnum():
            raise ValueError(f"非法扩展名：{value!r}")
        if extension not in output:
            output.append(extension)
    return output


def configure(workflow: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    start = find_node(workflow, args.start_node_id, "workflowStart")
    start_id = str(start.get("nodeId") or "")
    if not start_id:
        raise ValueError("开始节点缺少 nodeId")
    outputs = start.setdefault("outputs", [])
    if not any(item.get("key") == "userFiles" for item in outputs):
        outputs.append(copy.deepcopy(USER_FILES_OUTPUT))

    chat_config = workflow.setdefault("chatConfig", {})
    if not isinstance(chat_config, dict):
        raise ValueError("chatConfig 必须是对象")
    current = chat_config.get("fileSelectConfig")
    file_config = copy.deepcopy(current) if isinstance(current, dict) else {}
    defaults = {
        "maxFiles": 10,
        "canSelectFile": True,
        "canSelectImg": False,
        "canSelectVideo": False,
        "canSelectAudio": False,
        "canSelectCustomFileExtension": False,
        "customFileExtensionList": [],
        "customPdfParse": False,
    }
    for key, value in defaults.items():
        file_config.setdefault(key, copy.deepcopy(value))
    file_config["canSelectFile"] = True
    if args.max_files is not None:
        if args.max_files < 1:
            raise ValueError("--max-files 必须大于0")
        file_config["maxFiles"] = args.max_files
    if args.images is not None:
        file_config["canSelectImg"] = args.images
    if args.pdf_enhanced is not None:
        file_config["customPdfParse"] = args.pdf_enhanced

    custom_extensions = normalize_extensions(args.custom_extension)
    if args.clear_custom_extensions:
        file_config["customFileExtensionList"] = []
        file_config["canSelectCustomFileExtension"] = False
    elif custom_extensions:
        file_config["customFileExtensionList"] = custom_extensions
        file_config["canSelectCustomFileExtension"] = True
    chat_config["fileSelectConfig"] = file_config

    if args.gate_node_id:
        gate = find_node(workflow, args.gate_node_id)
        if gate.get("flowNodeType") != "ifElseNode":
            raise ValueError(f"{args.gate_node_id} 不是 ifElseNode")
        gate_value = [{
            "condition": "AND",
            "list": [{
                "variable": [start_id, "userFiles"],
                "condition": "isNotEmpty",
                "valueType": "input",
            }],
        }]
        set_or_append_input(gate, "ifElseList", gate_value, {
            "label": "", "valueType": "any", "renderTypeList": ["hidden"],
            "debugLabel": "", "description": "", "toolDescription": "",
        })

    for node_id in args.ai_node_id:
        ai = find_node(workflow, node_id)
        if ai.get("flowNodeType") not in {"chatNode", "agent", "tool"}:
            raise ValueError(f"{node_id} 不是已识别的AI/工具节点")
        set_or_append_input(ai, "fileUrlList", [[start_id, "userFiles"]], {
            "label": "app:workflow.user_file_input",
            "valueType": "arrayString",
            "renderTypeList": ["reference", "input"],
            "debugLabel": "文件链接",
            "description": "app:workflow.user_file_input_desc",
            "toolDescription": "",
        })
        set_or_append_input(ai, "aiChatExtractFiles", True, {
            "label": "", "valueType": "boolean", "renderTypeList": ["hidden"],
            "debugLabel": "", "toolDescription": "",
        })
        if file_config.get("canSelectImg"):
            set_or_append_input(ai, "aiChatVision", True, {
                "label": "", "valueType": "boolean", "renderTypeList": ["hidden"],
                "debugLabel": "", "toolDescription": "",
            })

    return {
        "start_node_id": start_id,
        "gate_node_id": args.gate_node_id or None,
        "ai_node_ids": args.ai_node_id,
        "file_select_config": file_config,
        "warning": "自定义扩展名只表示允许上传；解析能力仍需目标实例运行验证。" if custom_extensions else None,
    }


def main() -> int:
    args = parse_args()
    try:
        source = args.input_json.resolve()
        output = args.output_json.resolve()
        if not source.is_file():
            raise FileNotFoundError(source)
        if output.exists() and not args.force:
            raise FileExistsError(f"拒绝覆盖已存在文件：{output}")
        if source == output and not args.force:
            raise ValueError("原地修改必须显式使用 --force")
        workflow = load_json(source)
        summary = configure(workflow, args)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(workflow, ensure_ascii=False, indent=2), encoding="utf-8")
        result = {"status": "candidate_generated", "input": str(source), "output": str(output), **summary}
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"OK: {output}")
            print(f"START_NODE: {summary['start_node_id']}")
            print(f"GATE_NODE: {summary['gate_node_id'] or '-'}")
            print(f"AI_NODES: {','.join(summary['ai_node_ids']) or '-'}")
            print("STATUS: 候选JSON；仍需目标实例导入、保存、回导和运行验证")
        return 0
    except Exception as exc:
        if args.json:
            print(json.dumps({"status": "error", "error": f"{type(exc).__name__}: {exc}"}, ensure_ascii=False))
        else:
            print(f"ERROR: {type(exc).__name__}: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
