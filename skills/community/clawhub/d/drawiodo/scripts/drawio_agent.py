"""
drawio_agent - draw.io 自动做图Agent
接收自然语言描述，自动解析并生成.drawio文件

用法:
    python drawio_agent.py "画一个用户登录流程图"
    python drawio_agent.py --file spec.json
    python drawio_agent.py "创建一个微服务架构图，包含API网关、用户服务、订单服务、数据库层"
"""

import sys
import json
import os
import re
import argparse
from pathlib import Path

from drawio_gen import DrawIOBuilder, Styles
from drawio_hooks import execute, HookPoint
from drawio_version import VersionManager
from drawio_templates import (
    create_flowchart,
    create_architecture,
    create_class_diagram,
    create_er_diagram,
    create_tree,
    create_sequence_diagram,
    create_mindmap,
    create_network_topology,
)


def detect_diagram_type(text: str) -> str:
    """从自然语言描述中检测图表类型"""
    t = text.lower()

    # 流程图
    if any(kw in t for kw in ["流程", "flowchart", "flow chart", "步骤", "审批", "顺序执行"]):
        return "flowchart"

    # 架构图
    if any(kw in t for kw in ["架构", "architecture", "分层", "layer", "微服务", "microservice",
                               "系统架构", "技术栈"]):
        return "architecture"

    # UML类图
    if any(kw in t for kw in ["类图", "class diagram", "uml", "继承", "接口", "面向对象"]):
        return "class_diagram"

    # ER图
    if any(kw in t for kw in ["er", "实体关系", "数据库设计", "表关系", "database schema",
                               "entity relationship"]):
        return "er_diagram"

    # 树形图
    if any(kw in t for kw in ["树", "tree", "组织架构", "目录结构", "层级结构", "树状"]):
        return "tree"

    # 时序图
    if any(kw in t for kw in ["时序", "sequence", "交互", "消息流", "调用链", "请求响应"]):
        return "sequence"

    # 思维导图
    if any(kw in t for kw in ["思维导图", "mind map", "mindmap", "脑图", "发散"]):
        return "mindmap"

    # 网络拓扑
    if any(kw in t for kw in ["网络", "network", "拓扑", "topology", "服务器", "集群",
                               "部署"]):
        return "network"

    return "flowchart"  # 默认


def parse_flowchart(text: str) -> dict:
    """从自然语言解析流程图规格"""
    steps = []
    # 按序号、箭头、逗号等分割
    patterns = [
        r'(?:^|\n)\s*(?:\d+[\.\)、]\s*|[-*]\s*)(.+?)(?=\n|$)',
        r'(?:\d+[\.\)、]?\s*[：:]?\s*)(.+?)(?=\n|$)',
    ]

    lines = re.split(r'[,\n;；]', text)
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # 去除序号前缀
        cleaned = re.sub(r'^\s*\d+[\.\)、:\s]+', '', line).strip()
        cleaned = re.sub(r'^[-*]\s+', '', cleaned).strip()
        if cleaned and len(cleaned) > 1:
            steps.append(cleaned)

    if not steps:
        # Fallback: split by common separators
        parts = re.split(r'[→->>]+', text)
        steps = [p.strip() for p in parts if p.strip() and len(p.strip()) > 1]

    return {"steps": steps}


def parse_architecture(text: str) -> dict:
    """从自然语言解析架构图规格"""
    layers = []
    current_layer = None

    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Detect layer headers
        layer_match = re.match(r'^(?:第?[\一二三四五六七八九十\d]+[层部分]|[\w\s]+[层部]|[\w\s]+[Ll]ayer)\s*[:：]?\s*(.+)', line, re.IGNORECASE)
        if layer_match:
            if current_layer and current_layer["components"]:
                layers.append(current_layer)
            current_layer = {"name": layer_match.group(1).strip(), "components": [], "color": None}
            continue

        # Detect components (comma-separated within a layer)
        if current_layer:
            # Check for layer keywords in the line
            if any(kw in line for kw in ["层", "Layer", "前端", "后端", "数据库", "中间件",
                                          "网关", "服务", "缓存", "消息", "存储", "安全",
                                          "监控", "日志", "负载"]):
                if current_layer["components"]:
                    layers.append(current_layer)
                current_layer = {"name": line, "components": [], "color": None}
                continue

        # Extract component names
        if current_layer:
            if '，' in line or ',' in line:
                parts = re.split(r'[，,、]', line)
                for p in parts:
                    p = p.strip()
                    if p:
                        current_layer["components"].append(p)
            elif len(line) > 1 and len(line) < 50:
                current_layer["components"].append(line)

    if current_layer and current_layer["components"]:
        layers.append(current_layer)

    # If no layers detected, try to split by common layer keywords
    if not layers:
        keywords = ["前端", "网关", "后端", "服务", "数据", "缓存", "消息", "中间件", "存储",
                    "安全", "监控", "基础设施"]
        found_layers = []
        current_parts = []
        for line in text.replace('\n', '，').replace(';', '，').split('，'):
            line = line.strip()
            if not line:
                continue
            is_keyword_line = any(kw in line for kw in keywords)
            if is_keyword_line and current_parts:
                found_layers.append(current_parts)
                current_parts = [line]
            else:
                current_parts.append(line)
        if current_parts:
            found_layers.append(current_parts)

        color_map = [Styles.BLUE_NODE, Styles.GREEN_NODE, Styles.ORANGE_NODE,
                     Styles.PURPLE_NODE, Styles.CYAN_NODE, Styles.RED_NODE,
                     Styles.YELLOW_NODE, Styles.PINK_NODE]
        for i, parts in enumerate(found_layers):
            layer_name = parts[0] if len(parts) > 1 else f"Layer {i + 1}"
            components = parts[1:] if len(parts) > 1 else parts
            layers.append({
                "name": layer_name,
                "components": components,
                "color": color_map[i % len(color_map)]
            })

    return {"layers": layers}


def parse_json_spec(spec: dict) -> DrawIOBuilder:
    """从JSON规格生成图表"""
    diag_type = spec.get("type", "flowchart")
    title = spec.get("title", "Diagram")

    if diag_type == "flowchart":
        return create_flowchart(spec.get("steps", []), title,
                                spec.get("direction", "vertical"))
    elif diag_type == "architecture":
        return create_architecture(spec.get("layers", []), title)
    elif diag_type == "class_diagram":
        return create_class_diagram(spec.get("classes", []), title)
    elif diag_type == "er_diagram":
        return create_er_diagram(spec.get("entities", []), title)
    elif diag_type == "tree":
        return create_tree(spec.get("root", "Root"), spec.get("children", []),
                           title=title)
    elif diag_type == "sequence":
        return create_sequence_diagram(spec.get("actors", []),
                                       spec.get("messages", []), title)
    elif diag_type == "mindmap":
        return create_mindmap(spec.get("center", "Center"),
                              spec.get("branches", []), title)
    elif diag_type == "network":
        return create_network_topology(spec.get("devices", []),
                                       spec.get("connections", []), title)
    else:
        return create_flowchart(spec.get("steps", []), title)


def generate_from_text(text: str, output: str = None) -> str:
    """
    从自然语言描述生成drawio文件

    Args:
        text: 自然语言描述
        output: 输出文件路径，None则自动生成

    Returns:
        生成的文件路径
    """
    # ── pre_think hooks: 输入校验 ──
    execute(HookPoint.PRE_THINK, {"input": text, "type": "text"})

    if not output:
        workspace = Path(__file__).parent
        output = str(workspace / "output.drawio")

    diag_type = detect_diagram_type(text)

    if diag_type == "flowchart":
        spec = parse_flowchart(text)
        builder = create_flowchart(spec["steps"])

    elif diag_type == "architecture":
        spec = parse_architecture(text)
        builder = create_architecture(spec["layers"])

    elif diag_type == "class_diagram":
        # For class diagrams, prefer JSON input
        builder = DrawIOBuilder(name="UML Class Diagram")
        builder.add_node("Tip: Use JSON spec for class diagrams", 100, 100,
                         style=Styles.NOTE)

    elif diag_type == "tree":
        builder = create_tree("Root", ["Child 1", "Child 2", "Child 3"])

    elif diag_type == "sequence":
        builder = create_sequence_diagram(
            ["Client", "Server", "DB"],
            [{"from": 0, "to": 1, "label": "Request", "type": "sync"},
             {"from": 1, "to": 2, "label": "Query", "type": "sync"},
             {"from": 2, "to": 1, "label": "Result", "type": "return"},
             {"from": 1, "to": 0, "label": "Response", "type": "return"}]
        )

    elif diag_type == "mindmap":
        spec = parse_flowchart(text)
        center = spec["steps"][0] if spec["steps"] else "Center"
        branches = [{"label": s, "sub": []} for s in spec["steps"][1:]] if len(spec["steps"]) > 1 else []
        builder = create_mindmap(center, branches)

    elif diag_type == "network":
        builder = create_network_topology(
            [{"label": "Router", "type": "cloud", "x": 300, "y": 50},
             {"label": "Server 1", "type": "cylinder", "x": 150, "y": 200},
             {"label": "Server 2", "type": "cylinder", "x": 350, "y": 200},
             {"label": "DB", "type": "cylinder", "x": 250, "y": 350}],
            [{"from": "Router", "to": "Server 1"},
             {"from": "Router", "to": "Server 2"},
             {"from": "Server 1", "to": "DB"},
             {"from": "Server 2", "to": "DB"}]
        )

    else:
        builder = create_flowchart(["Step 1", "Step 2", "Step 3"])

    # ── post_think hooks: 方案校验 ──
    execute(HookPoint.POST_THINK, {"diagram_type": diag_type, "nodes": len(builder.nodes)})

    # ── pre_iterate hooks: 文件存在则自动备份 ──
    is_update = os.path.exists(output)
    execute(HookPoint.PRE_ITERATE, {"output_path": output, "is_update": is_update})

    filepath = builder.save(output)

    # ── post_iterate hooks: 生成文件校验 + 预览 ──
    execute(HookPoint.POST_ITERATE, {"output_path": filepath, "nodes": len(builder.nodes)})

    return filepath


def generate_from_json(spec_path: str, output: str = None) -> str:
    """从JSON文件生成drawio文件"""
    with open(spec_path, 'r', encoding='utf-8') as f:
        spec = json.load(f)

    if not output:
        output = str(Path(spec_path).with_suffix('.drawio'))

    builder = parse_json_spec(spec)
    filepath = builder.save(output)
    return filepath


def open_in_drawio(filepath: str):
    """用draw.io打开文件"""
    import subprocess
    drawio_path = r"C:\Program Files\draw.io\draw.io.exe"
    if os.path.exists(drawio_path):
        subprocess.Popen([drawio_path, filepath])
    else:
        # Try web version
        print(f"draw.io desktop not found. Opening in browser...")
        os.startfile(filepath)


def main():
    parser = argparse.ArgumentParser(description="draw.io Auto Diagram Generator")
    parser.add_argument("input", help="Description text or JSON spec file path")
    parser.add_argument("-o", "--output", help="Output .drawio file path")
    parser.add_argument("--open", action="store_true", help="Open in draw.io after generation")
    parser.add_argument("--json", action="store_true", help="Force JSON mode")

    args = parser.parse_args()

    if args.json or (Path(args.input).exists() and args.input.endswith('.json')):
        filepath = generate_from_json(args.input, args.output)
    else:
        filepath = generate_from_text(args.input, args.output)

    print(f"Generated: {filepath}")

    if args.open:
        open_in_drawio(filepath)


if __name__ == "__main__":
    main()
