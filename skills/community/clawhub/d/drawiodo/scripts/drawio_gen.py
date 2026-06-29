"""
drawio_gen - draw.io XML文件自动生成核心库
支持节点、连线、分组、容器、样式等完整图表元素
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom
from dataclasses import dataclass, field
from typing import Optional
import uuid
import math


@dataclass
class NodeStyle:
    """draw.io节点样式配置"""
    shape: str = "rounded=1;whiteSpace=wrap;html=1;"  # 默认圆角矩形
    fill_color: str = "#FFFFFF"
    stroke_color: str = "#000000"
    font_color: str = "#000000"
    font_size: int = 12
    font_style: int = 0  # 0=normal, 1=bold, 2=italic, 3=bold+italic
    stroke_width: int = 1
    opacity: int = 100
    shadow: bool = False
    dash_pattern: str = ""  # 如 "5 5" 表示虚线
    arc_size: int = 10  # 圆角大小 (rounded=1时有效)
    spacing_top: int = -1
    spacing_bottom: int = -1
    spacing_left: int = -1
    spacing_right: int = -1

    def build(self, extra: str = "") -> str:
        s = self.shape
        s += f"fillColor={self.fill_color};"
        s += f"strokeColor={self.stroke_color};"
        s += f"fontColor={self.font_color};"
        s += f"fontSize={self.font_size};"
        if self.font_style:
            s += f"fontStyle={self.font_style};"
        if self.stroke_width != 1:
            s += f"strokeWidth={self.stroke_width};"
        if self.opacity != 100:
            s += f"opacity={self.opacity};"
        if self.shadow:
            s += "shadow=1;"
        if self.dash_pattern:
            s += f"dashed=1;dashPattern={self.dash_pattern};"
        if self.spacing_top >= 0:
            s += f"spacingTop={self.spacing_top};"
        if self.spacing_bottom >= 0:
            s += f"spacingBottom={self.spacing_bottom};"
        if self.spacing_left >= 0:
            s += f"spacingLeft={self.spacing_left};"
        if self.spacing_right >= 0:
            s += f"spacingRight={self.spacing_right};"
        if extra:
            s += extra
        return s


@dataclass
class EdgeStyle:
    """draw.io连线样式配置"""
    shape: str = "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"
    line_color: str = "#000000"
    font_color: str = "#000000"
    font_size: int = 11
    stroke_width: int = 1
    dash_pattern: str = ""
    end_arrow: str = "classic"  # classic, block, open, oval, diamond, none
    start_arrow: str = "none"
    end_fill: int = 1  # 1=filled, 0=open
    start_fill: int = 1

    def build(self, extra: str = "") -> str:
        s = self.shape
        s += f"strokeColor={self.line_color};"
        s += f"fontColor={self.font_color};"
        s += f"fontSize={self.font_size};"
        if self.stroke_width != 1:
            s += f"strokeWidth={self.stroke_width};"
        if self.dash_pattern:
            s += f"dashed=1;dashPattern={self.dash_pattern};"
        s += f"endArrow={self.end_arrow};"
        s += f"startArrow={self.start_arrow};"
        s += f"endFill={self.end_fill};"
        s += f"startFill={self.start_fill};"
        if extra:
            s += extra
        return s


# ============== 预设样式 ==============

class Styles:
    """常用样式预设"""

    # 节点预设
    DEFAULT_NODE = NodeStyle()
    BLUE_NODE = NodeStyle(fill_color="#dae8fc", stroke_color="#6c8ebf", font_color="#000000")
    GREEN_NODE = NodeStyle(fill_color="#d5e8d4", stroke_color="#82b366", font_color="#000000")
    ORANGE_NODE = NodeStyle(fill_color="#ffe6cc", stroke_color="#d6b656", font_color="#000000")
    RED_NODE = NodeStyle(fill_color="#f8cecc", stroke_color="#b85450", font_color="#000000")
    PURPLE_NODE = NodeStyle(fill_color="#e1d5e7", stroke_color="#9673a6", font_color="#000000")
    YELLOW_NODE = NodeStyle(fill_color="#fff2cc", stroke_color="#d6b656", font_color="#000000")
    CYAN_NODE = NodeStyle(fill_color="#d4e1f5", stroke_color="#6c8ebf", font_color="#000000")
    GRAY_NODE = NodeStyle(fill_color="#f5f5f5", stroke_color="#666666", font_color="#333333")
    PINK_NODE = NodeStyle(fill_color="#f8cecc", stroke_color="#b85450", font_color="#b85450")

    # 特殊形状
    DIAMOND = NodeStyle(shape="rhombus;whiteSpace=wrap;html=1;", fill_color="#fff2cc", stroke_color="#d6b656")
    CYLINDER = NodeStyle(shape="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;", fill_color="#dae8fc", stroke_color="#6c8ebf")
    CLOUD = NodeStyle(shape="ellipse;shape=cloud;whiteSpace=wrap;html=1;", fill_color="#f5f5f5", stroke_color="#666666")
    CIRCLE = NodeStyle(shape="ellipse;whiteSpace=wrap;html=1;", fill_color="#dae8fc", stroke_color="#6c8ebf")
    HEXAGON = NodeStyle(shape="shape=hexagon;perimeter=hexagonPerimeter2;whiteSpace=wrap;html=1;fixedSize=1;size=10;", fill_color="#ffe6cc", stroke_color="#d6b656")
    PARALLELOGRAM = NodeStyle(shape="shape=parallelogram;perimeter=parallelogramPerimeter;whiteSpace=wrap;html=1;fixedSize=1;size=10;", fill_color="#d5e8d4", stroke_color="#82b366")
    DOCUMENT = NodeStyle(shape="mxgraph.basic.doc;whiteSpace=wrap;html=1;size=0.15;", fill_color="#dae8fc", stroke_color="#6c8ebf")
    NOTE = NodeStyle(shape="shape=note;whiteSpace=wrap;html=1;backgroundOutline=1;size=15;", fill_color="#fff2cc", stroke_color="#d6b656")
    FOLDER = NodeStyle(shape="mxgraph.basic.folder;whiteSpace=wrap;html=1;", fill_color="#ffe6cc", stroke_color="#d6b656")

    # 标题节点
    HEADER_BLUE = NodeStyle(fill_color="#1ba1e2", stroke_color="#006EAF", font_color="#ffffff", font_size=14, font_style=1)
    HEADER_GREEN = NodeStyle(fill_color="#60a917", stroke_color="#2D7600", font_color="#ffffff", font_size=14, font_style=1)
    HEADER_ORANGE = NodeStyle(fill_color="#d79b00", stroke_color="#a68000", font_color="#ffffff", font_size=14, font_style=1)
    HEADER_RED = NodeStyle(fill_color="#a20025", stroke_color="#6D0000", font_color="#ffffff", font_size=14, font_style=1)
    HEADER_GRAY = NodeStyle(fill_color="#6c8ebf", stroke_color="#4A6FA5", font_color="#ffffff", font_size=14, font_style=1)

    # UML
    UML_CLASS = NodeStyle(shape="swimlane;startSize=26;html=1;fontStyle=1;align=center;fillColor=#dae8fc;strokeColor=#6c8ebf;",
                          fill_color="#dae8fc", stroke_color="#6c8ebf", font_style=1)

    # 连线预设
    DEFAULT_EDGE = EdgeStyle()
    BOLD_EDGE = EdgeStyle(stroke_width=2)
    DASHED_EDGE = EdgeStyle(dash_pattern="5 5")
    RED_EDGE = EdgeStyle(line_color="#b85450")
    BLUE_EDGE = EdgeStyle(line_color="#6c8ebf")
    GREEN_EDGE = EdgeStyle(line_color="#82b366")
    GRAY_EDGE = EdgeStyle(line_color="#999999")
    NO_ARROW = EdgeStyle(end_arrow="none")
    DIAMOND_ARROW = EdgeStyle(end_arrow="diamond", end_fill=1, line_color="#82b366")
    OPEN_ARROW = EdgeStyle(end_arrow="open", end_fill=0)

    # 容器/分组
    CONTAINER = NodeStyle(shape="swimlane;startSize=22;html=1;fillColor=#f5f5f5;strokeColor=#666666;fontStyle=1;",
                          fill_color="#f5f5f5", stroke_color="#666666", font_style=1)
    GROUP = NodeStyle(shape="rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#666666;dashed=1;dashPattern=3 3;",
                      fill_color="none", stroke_color="#666666", dash_pattern="3 3")


@dataclass
class Node:
    """图表节点"""
    id: str = ""
    label: str = ""
    x: float = 0
    y: float = 0
    width: float = 120
    height: float = 60
    style: NodeStyle = field(default_factory=NodeStyle)
    parent_id: str = "1"
    value: str = ""  # 用于HTML内容（UML类等）
    vertex: bool = True
    connectable: bool = True

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())[:8]


@dataclass
class Edge:
    """图表连线"""
    id: str = ""
    source_id: str = ""
    target_id: str = ""
    label: str = ""
    style: EdgeStyle = field(default_factory=EdgeStyle)
    parent_id: str = "1"
    value: str = ""

    # 连接点 0=顶部 1=右 2=底部 3=左
    source_port: Optional[int] = None
    target_port: Optional[int] = None
    # 偏移
    source_x: float = 0
    source_y: float = 0
    target_x: float = 0
    target_y: float = 0

    # 路径点 (用于曲线/折线控制)
    waypoints: list = field(default_factory=list)

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())[:8]


@dataclass
class Container:
    """分组容器"""
    id: str = ""
    label: str = ""
    x: float = 0
    y: float = 0
    width: float = 300
    height: float = 200
    style: NodeStyle = field(default_factory=lambda: Styles.CONTAINER)
    parent_id: str = "1"

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())[:8]


class DrawIOBuilder:
    """draw.io文件构建器"""

    def __init__(self, name: str = "Page-1"):
        self.name = name
        self.nodes: list[Node] = []
        self.edges: list[Edge] = []
        self.containers: list[Container] = []
        self._page_id = "1"

    def add_node(self, label: str, x: float, y: float, width: float = 120, height: float = 60,
                 style: NodeStyle = None, parent_id: str = "1", value: str = "",
                 node_id: str = "") -> Node:
        node = Node(label=label, x=x, y=y, width=width, height=height,
                    style=style or Styles.DEFAULT_NODE, parent_id=parent_id, value=value)
        if node_id:
            node.id = node_id
        self.nodes.append(node)
        return node

    def add_edge(self, source_id: str, target_id: str, label: str = "",
                 style: EdgeStyle = None, source_port: int = None, target_port: int = None,
                 waypoints: list = None, value: str = "") -> Edge:
        edge = Edge(source_id=source_id, target_id=target_id, label=label,
                    style=style or Styles.DEFAULT_EDGE, source_port=source_port,
                    target_port=target_port, waypoints=waypoints or [], value=value)
        self.edges.append(edge)
        return edge

    def add_container(self, label: str, x: float, y: float, width: float = 300, height: float = 200,
                      style: NodeStyle = None) -> Container:
        container = Container(label=label, x=x, y=y, width=width, height=height,
                              style=style or Styles.CONTAINER)
        self.containers.append(container)
        return container

    def connect(self, src: Node, tgt: Node, label: str = "", style: EdgeStyle = None,
                src_port: int = None, tgt_port: int = None) -> Edge:
        return self.add_edge(src.id, tgt.id, label, style, src_port, tgt_port)

    def _make_mx_cell(self, cell_id: str, value: str, style_str: str,
                      x: float = 0, y: float = 0, width: float = 0, height: float = 0,
                      parent: str = "1", vertex: bool = False, edge: bool = False,
                      source: str = None, target: str = None,
                      source_port: int = None, target_port: int = None,
                      waypoints: list = None) -> ET.Element:
        attrs = {
            "id": cell_id,
            "value": value,
            "style": style_str,
            "parent": parent,
        }
        if vertex:
            attrs["vertex"] = "1"
        if edge:
            attrs["edge"] = "1"
        if x or y or width or height:
            attrs["mxGeometry"] = ""  # will be child
            geom_attrs = {}
            if x is not None:
                geom_attrs["x"] = str(x)
            if y is not None:
                geom_attrs["y"] = str(y)
            if width is not None:
                geom_attrs["width"] = str(width)
            if height is not None:
                geom_attrs["height"] = str(height)
            if edge:
                geom_attrs["relative"] = "1"

        cell = ET.Element("mxCell", attrs)

        if x is not None or edge:
            geom = ET.SubElement(cell, "mxGeometry")
            if edge:
                geom.set("relative", "1")
            else:
                if x is not None:
                    geom.set("x", str(x))
                if y is not None:
                    geom.set("y", str(y))
                if width:
                    geom.set("width", str(width))
                if height:
                    geom.set("height", str(height))

        if source:
            cell.set("source", source)
        if target:
            cell.set("target", target)

        if source_port is not None:
            src_geom = ET.SubElement(cell, "mxCell")
            src_geom.set("as", "sourcePoint")
            sp = self._port_to_point(source_port)
            src_geom.set("mxGeometry", "")
            g = ET.SubElement(src_geom, "mxGeometry")
            g.set("relative", "1")
            g.set("x", str(sp[0]))
            g.set("y", str(sp[1]))

        if target_port is not None:
            tgt_geom = ET.SubElement(cell, "mxCell")
            tgt_geom.set("as", "targetPoint")
            tp = self._port_to_point(target_port)
            tgt_geom.set("mxGeometry", "")
            g = ET.SubElement(tgt_geom, "mxGeometry")
            g.set("relative", "1")
            g.set("x", str(tp[0]))
            g.set("y", str(tp[1]))

        if waypoints:
            array = ET.SubElement(cell, "Array")
            array.set("as", "points")
            for wx, wy in waypoints:
                mp = ET.SubElement(array, "mxPoint")
                mp.set("x", str(wx))
                mp.set("y", str(wy))

        return cell

    @staticmethod
    def _port_to_point(port: int) -> tuple:
        mapping = {0: (0.5, 0), 1: (1, 0.5), 2: (0.5, 1), 3: (0, 0.5)}
        return mapping.get(port, (0.5, 0.5))

    def build_xml(self) -> str:
        root = ET.Element("mxfile")
        root.set("host", "app.diagrams.net")
        root.set("modified", "2026")
        root.set("agent", "WorkBuddy drawio_gen")
        root.set("version", "24.0.0")
        root.set("type", "device")

        diag = ET.SubElement(root, "diagram")
        diag.set("id", self._page_id)
        diag.set("name", self.name)

        graph = ET.SubElement(diag, "mxGraphModel")
        graph.set("dx", "1422")
        graph.set("dy", "794")
        graph.set("grid", "1")
        graph.set("gridSize", "10")
        graph.set("guides", "1")
        graph.set("tooltips", "1")
        graph.set("connect", "1")
        graph.set("arrows", "1")
        graph.set("fold", "1")
        graph.set("page", "1")
        graph.set("pageScale", "1")
        graph.set("pageWidth", "1169")
        graph.set("pageHeight", "827")
        graph.set("math", "0")
        graph.set("shadow", "0")

        root_cell = ET.SubElement(graph, "root")
        ET.SubElement(root_cell, "mxCell", {"id": "0"})
        ET.SubElement(root_cell, "mxCell", {"id": "1", "parent": "0"})

        # Containers first (so nodes can be children)
        for c in self.containers:
            cell = ET.SubElement(root_cell, "mxCell", {
                "id": c.id,
                "value": c.label,
                "style": c.style.build(),
                "vertex": "1",
                "parent": c.parent_id,
            })
            geom = ET.SubElement(cell, "mxGeometry")
            geom.set("x", str(c.x))
            geom.set("y", str(c.y))
            geom.set("width", str(c.width))
            geom.set("height", str(c.height))
            geom.set("as", "geometry")

        # Nodes
        for n in self.nodes:
            cell = ET.SubElement(root_cell, "mxCell", {
                "id": n.id,
                "value": n.value if n.value else n.label,
                "style": n.style.build(),
                "vertex": "1",
                "parent": n.parent_id,
            })
            geom = ET.SubElement(cell, "mxGeometry")
            geom.set("x", str(n.x))
            geom.set("y", str(n.y))
            geom.set("width", str(n.width))
            geom.set("height", str(n.height))
            geom.set("as", "geometry")

        # Edges
        for e in self.edges:
            edge_style = e.style.build()

            # 设置 source/target 端口
            if e.source_port is not None:
                sp = self._port_to_point(e.source_port)
                edge_style += f"exitX={sp[0]};exitY={sp[1]};exitDx=0;exitDy=0;"
            if e.target_port is not None:
                tp = self._port_to_point(e.target_port)
                edge_style += f"entryX={tp[0]};entryY={tp[1]};entryDx=0;entryDy=0;"

            attrs = {
                "id": e.id,
                "value": e.value if e.value else e.label,
                "style": edge_style,
                "edge": "1",
                "parent": e.parent_id,
                "source": e.source_id,
                "target": e.target_id,
            }

            cell = ET.SubElement(root_cell, "mxCell", attrs)
            geom = ET.SubElement(cell, "mxGeometry")
            geom.set("relative", "1")
            geom.set("as", "geometry")

            # waypoints（仅中间点，不含source/target边缘点）
            if e.waypoints:
                array = ET.SubElement(cell, "Array")
                array.set("as", "points")
                for wx, wy in e.waypoints:
                    mp = ET.SubElement(array, "mxPoint")
                    mp.set("x", str(wx))
                    mp.set("y", str(wy))

        # Pretty print
        rough = ET.tostring(root, encoding="unicode")
        parsed = minidom.parseString(rough)
        pretty = parsed.toprettyxml(indent="  ")
        # Remove xml declaration line
        lines = pretty.split("\n")
        lines = [l for l in lines if not l.startswith("<?xml")]
        return "\n".join(lines).strip()

    def save(self, filepath: str) -> str:
        xml = self.build_xml()
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(xml)
        return filepath

    def open_in_drawio(self, filepath: str):
        """用本地draw.io打开文件"""
        import subprocess
        drawio_path = r"C:\Program Files\draw.io\draw.io.exe"
        try:
            subprocess.Popen([drawio_path, filepath])
        except FileNotFoundError:
            print(f"draw.io not found at {drawio_path}")
