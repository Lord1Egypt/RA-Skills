"""
drawio - draw.io 自动做图命令行工具

用法:
    python drawio.py flowchart "开始 → 验证 → 处理 → 结束"
    python drawio.py architecture "前端:React,Vue;后端:API,Auth;数据:MySQL,Redis"
    python drawio.py er "spec.json"
    python drawio.py custom "我的自定义图表描述"
    python drawio.py open "path/to/file.drawio"

快捷方式 (已加到 PATH 则直接用):
    drawio flowchart "开始 → 处理 → 结束"
"""

import sys
import os
import json
import re

# 确保能找到核心库
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from drawio_gen import DrawIOBuilder, Styles, NodeStyle, EdgeStyle
from drawio_templates import (
    create_flowchart, create_architecture, create_class_diagram,
    create_er_diagram, create_tree, create_sequence_diagram,
    create_mindmap, create_network_topology,
    horizontal_layout, vertical_layout, auto_size_node,
)

DRAWIO_EXE = r"C:\Program Files\draw.io\draw.io.exe"
OUT_DIR = os.getcwd()


def open_file(filepath: str):
    """用draw.io打开文件"""
    if os.path.exists(DRAWIO_EXE):
        os.startfile(filepath)
    else:
        os.startfile(filepath)  # 系统默认打开器


def cmd_flowchart(desc: str, title: str = "Flowchart", vertical: bool = True):
    """生成流程图"""
    steps = re.split(r'[→\->>]+', desc)
    steps = [s.strip() for s in steps if s.strip()]
    if not steps:
        print("Error: 无法解析步骤，请用 → 或 -> 分隔")
        return
    builder = create_flowchart(steps, title=title,
                               direction="vertical" if vertical else "horizontal")
    path = os.path.join(OUT_DIR, f"flowchart_{title.lower().replace(' ', '_')}.drawio")
    builder.save(path)
    open_file(path)
    print(f"Flowchart saved: {path}")


def cmd_architecture(desc: str, title: str = "Architecture"):
    """生成分层架构图

    格式: "层名:组件1,组件2;层名2:组件3,组件4"
    """
    layers = []
    color_map = [Styles.BLUE_NODE, Styles.ORANGE_NODE, Styles.GREEN_NODE,
                 Styles.PURPLE_NODE, Styles.CYAN_NODE, Styles.RED_NODE,
                 Styles.YELLOW_NODE, Styles.PINK_NODE, Styles.GRAY_NODE]

    parts = desc.split(';')
    for i, part in enumerate(parts):
        part = part.strip()
        if ':' in part:
            name, comps = part.split(':', 1)
            components = [c.strip() for c in comps.split(',') if c.strip()]
        else:
            name = part
            components = []
        layers.append({
            "name": name.strip(),
            "components": components,
            "color": color_map[i % len(color_map)]
        })

    if not layers:
        print("Error: 无法解析层级，格式: 层名:组件1,组件2;层名2:组件3")
        return

    builder = create_architecture(layers, title=title)
    path = os.path.join(OUT_DIR, f"architecture_{title.lower().replace(' ', '_')}.drawio")
    builder.save(path)
    open_file(path)
    print(f"Architecture saved: {path}")


def cmd_class_diagram(spec_file: str, title: str = "UML Class Diagram"):
    """从JSON生成UML类图"""
    with open(spec_file, 'r', encoding='utf-8') as f:
        spec = json.load(f)
    builder = create_class_diagram(spec.get("classes", []), title)
    path = os.path.join(OUT_DIR, f"class_{title.lower().replace(' ', '_')}.drawio")
    builder.save(path)
    open_file(path)
    print(f"Class Diagram saved: {path}")


def cmd_er_diagram(spec_file: str, title: str = "ER Diagram"):
    """从JSON生成ER图"""
    with open(spec_file, 'r', encoding='utf-8') as f:
        spec = json.load(f)
    builder = create_er_diagram(spec.get("entities", []), title)
    path = os.path.join(OUT_DIR, f"er_{title.lower().replace(' ', '_')}.drawio")
    builder.save(path)
    open_file(path)
    print(f"ER Diagram saved: {path}")


def cmd_tree(desc: str, title: str = "Tree"):
    """生成树形图

    格式: "根节点 | 子1,子2,子3"
    """
    parts = desc.split('|')
    root = parts[0].strip() if parts else "Root"
    children = []
    if len(parts) > 1:
        children = [c.strip() for c in parts[1].split(',') if c.strip()]

    builder = create_tree(root, children, title=title)
    path = os.path.join(OUT_DIR, f"tree_{title.lower().replace(' ', '_')}.drawio")
    builder.save(path)
    open_file(path)
    print(f"Tree saved: {path}")


def cmd_mindmap(desc: str, title: str = "Mind Map"):
    """生成思维导图

    格式: "中心主题 | 分支1:子1,子2;分支2:子3,子4"
    """
    parts = desc.split('|')
    center = parts[0].strip() if parts else "Center"
    branches = []
    if len(parts) > 1:
        for b in parts[1].split(';'):
            b = b.strip()
            if ':' in b:
                name, subs = b.split(':', 1)
                subs_list = [s.strip() for s in subs.split(',') if s.strip()]
            else:
                name = b
                subs_list = []
            branches.append({"label": name, "sub": subs_list})

    builder = create_mindmap(center, branches, title=title)
    path = os.path.join(OUT_DIR, f"mindmap_{title.lower().replace(' ', '_')}.drawio")
    builder.save(path)
    open_file(path)
    print(f"Mind Map saved: {path}")


def cmd_network(spec_file: str, title: str = "Network Topology"):
    """从JSON生成网络拓扑图"""
    with open(spec_file, 'r', encoding='utf-8') as f:
        spec = json.load(f)
    builder = create_network_topology(spec.get("devices", []),
                                      spec.get("connections", []), title)
    path = os.path.join(OUT_DIR, f"network_{title.lower().replace(' ', '_')}.drawio")
    builder.save(path)
    open_file(path)
    print(f"Network saved: {path}")


def cmd_open(filepath: str):
    """打开已有的drawio文件"""
    if not os.path.exists(filepath):
        # 尝试在工作目录下查找
        alt = os.path.join(OUT_DIR, filepath)
        if os.path.exists(alt):
            filepath = alt
        else:
            print(f"Error: 文件不存在 - {filepath}")
            return
    open_file(filepath)
    print(f"Opened: {filepath}")


def print_usage():
    print("""
draw.io 自动做图工具
====================

用法: python drawio.py <命令> <参数> [--title 标题]

命令:
  flowchart  <步骤描述>          流程图，步骤用 → 或 -> 分隔
  architecture <层级描述>        架构图，格式: 层名:组件1,组件2;层名:组件3
  class      <json文件>          UML类图
  er         <json文件>          ER实体关系图
  tree       <树描述>            树形图，格式: 根 | 子1,子2,子3
  mindmap    <导图描述>          思维导图，格式: 中心 | 分支1:子1,子2;分支2
  network    <json文件>          网络拓扑图
  open       <文件路径>          用draw.io打开文件

示例:
  python drawio.py flowchart "开始 → 输入 → 验证 → 处理 → 结束"
  python drawio.py architecture "前端:React,Vue,小程序;网关:Nginx;后端:API,Auth,Order;数据:MySQL,Redis,MongoDB"
  python drawio.py tree "公司 | 技术,产品,市场"
  python drawio.py mindmap "AI | NLP:翻译,摘要;CV:检测,分割;RL:机器人,游戏"
  python drawio.py open test_architecture.drawio
    """)


def main():
    if len(sys.argv) < 2:
        print_usage()
        return

    cmd = sys.argv[1].lower()

    # Parse --title
    title = ""
    args = sys.argv[2:]
    if "--title" in args:
        idx = args.index("--title")
        if idx + 1 < len(args):
            title = args[idx + 1]
            args = args[:idx] + args[idx + 2:]

    desc = " ".join(args)

    commands = {
        "flowchart": lambda: cmd_flowchart(desc, title or "Flowchart"),
        "flow": lambda: cmd_flowchart(desc, title or "Flowchart"),
        "architecture": lambda: cmd_architecture(desc, title or "Architecture"),
        "arch": lambda: cmd_architecture(desc, title or "Architecture"),
        "class": lambda: cmd_class_diagram(desc, title or "Class Diagram"),
        "uml": lambda: cmd_class_diagram(desc, title or "Class Diagram"),
        "er": lambda: cmd_er_diagram(desc, title or "ER Diagram"),
        "tree": lambda: cmd_tree(desc, title or "Tree"),
        "mindmap": lambda: cmd_mindmap(desc, title or "Mind Map"),
        "mind": lambda: cmd_mindmap(desc, title or "Mind Map"),
        "network": lambda: cmd_network(desc, title or "Network"),
        "topo": lambda: cmd_network(desc, title or "Network"),
        "open": lambda: cmd_open(desc),
    }

    if cmd in commands:
        commands[cmd]()
    elif cmd in ["-h", "--help", "help"]:
        print_usage()
    else:
        # 尝试自动检测类型
        print(f"未知命令: {cmd}")
        print("运行 python drawio.py help 查看用法")


if __name__ == "__main__":
    main()
