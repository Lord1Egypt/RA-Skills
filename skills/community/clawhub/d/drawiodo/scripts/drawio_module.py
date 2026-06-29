"""
drawio_module.py — 模块化图生成框架

架构：
  LLM 加载模块 schema → 按用户需求构造数据 → 调用 module.build(data, theme)
  → layout() 只算坐标 → render() 按形状/主题拼装 → DrawIOBuilder

模块注册：
  registry["graph"] = GraphModule
  registry["gantt"] = GanttModule
  registry["grid"]  = GridModule
  ...
  module = registry.get("graph")
  module.build(data, theme="tech")
"""
from drawio_gen import DrawIOBuilder, NodeStyle, EdgeStyle
from drawio_route import Rect
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, field


# ================================================================
# 标准输出类型
# ================================================================

@dataclass
class LayoutResult:
    """布局计算输出（只有坐标，不含渲染信息）"""
    node_positions: Dict[str, Tuple[float, float, float, float]] = field(default_factory=dict)
    """{node_id: (x, y, width, height)}"""

    edge_routes: List[dict] = field(default_factory=list)
    """[{from, to, label, waypoints, src_port, tgt_port}]"""

    canvas_w: float = 1169
    canvas_h: float = 827


# ================================================================
# 主题
# ================================================================

THEMES = {
    "default": {
        "layers": [
            ("#dae8fc", "#6c8ebf"), ("#ffe6cc", "#d6b656"),
            ("#d5e8d4", "#82b366"), ("#e1d5e7", "#9673a6"),
            ("#f8cecc", "#b85450"), ("#d4e1f5", "#6c8ebf"),
            ("#fff2cc", "#d6b656"), ("#f5f5f5", "#666666"),
        ],
        "edges": ["#6c8ebf", "#82b366", "#d6b656", "#b85450",
                   "#9673a6", "#1ba1e2", "#60a917", "#a20025"],
        "desc": "默认彩色",
    },
    "tech": {
        "layers": [
            ("#e3f2fd", "#1565c0"), ("#bbdefb", "#1976d2"),
            ("#e0f2f1", "#00796b"), ("#f3e5f5", "#7b1fa2"),
            ("#fce4ec", "#c62828"), ("#e8eaf6", "#283593"),
            ("#e0f7fa", "#00838f"), ("#fff3e0", "#e65100"),
        ],
        "edges": ["#1565c0", "#00796b", "#7b1fa2", "#c62828",
                   "#283593", "#00838f", "#e65100", "#2e7d32"],
        "desc": "科技蓝",
    },
    "business": {
        "layers": [
            ("#c5cae9", "#3949ab"), ("#fff9c4", "#f9a825"),
            ("#c8e6c9", "#2e7d32"), ("#ffe0b2", "#e65100"),
            ("#f5f5f5", "#616161"), ("#e1bee7", "#6a1b9a"),
            ("#b2dfdb", "#004d40"), ("#ffcdd2", "#b71c1c"),
        ],
        "edges": ["#3949ab", "#2e7d32", "#e65100", "#6a1b9a",
                   "#004d40", "#b71c1c", "#f9a825", "#616161"],
        "desc": "商务沉稳",
    },
    "bw": {
        "layers": [
            ("#f5f5f5", "#333333"), ("#e0e0e0", "#424242"),
            ("#eeeeee", "#212121"), ("#bdbdbd", "#616161"),
            ("#9e9e9e", "#000000"), ("#e0e0e0", "#212121"),
            ("#f5f5f5", "#424242"), ("#eeeeee", "#333333"),
        ],
        "edges": ["#424242", "#616161", "#212121", "#000000",
                   "#757575", "#333333", "#9e9e9e", "#bdbdbd"],
        "desc": "黑白",
    },
    "nature": {
        "layers": [
            ("#e8f5e9", "#2e7d32"), ("#e3f2fd", "#1565c0"),
            ("#fff3e0", "#e65100"), ("#fce4ec", "#c62828"),
            ("#f3e5f5", "#6a1b9a"), ("#e0f2f1", "#004d40"),
            ("#fff8e1", "#f9a825"), ("#efebe9", "#4e342e"),
        ],
        "edges": ["#2e7d32", "#1565c0", "#e65100", "#c62828",
                   "#6a1b9a", "#004d40", "#f9a825", "#4e342e"],
        "desc": "自然清新",
    },
}

TEXT_COLORS = {
    "default": "#000000",
    "tech": "#000000",
    "business": "#000000",
    "bw": "#000000",
    "nature": "#000000",
}


# ================================================================
# 基础接口
# ================================================================

class DiagramModule:
    """所有模块的基类"""
    name = ""
    description = ""
    schema = {}  # JSON Schema 描述输入格式

    def layout(self, data: dict) -> LayoutResult:
        """算位置（只算坐标，不渲染）"""
        raise NotImplementedError

    def render_node(self, nid: str, label: str,
                    x: float, y: float, w: float, h: float,
                    spec: dict, layer_idx: int,
                    layer_colors: list) -> Tuple[str, NodeStyle, str]:
        """
        渲染单个节点。
        Returns: (display_label, NodeStyle, value_html)
        """
        raise NotImplementedError

    def render(self, layout: LayoutResult,
               data: dict, theme: str) -> DrawIOBuilder:
        """基于布局结果 + 用户数据 + 主题，拼装 DrawIOBuilder"""
        builder = DrawIOBuilder(name=data.get("title", "Diagram"))
        theme_data = THEMES.get(theme, THEMES["default"])
        layer_colors = theme_data["layers"]
        edge_colors = theme_data["edges"]

        # 节点
        color_idx = 0
        for nid, (x, y, w, h) in layout.node_positions.items():
            node_spec = {}
            for nd in data.get("nodes", data.get("items", [])):
                if nd.get("id") == nid:
                    node_spec = nd
                    break
            label = node_spec.get("label", nid)
            layer_idx = node_spec.get("_layer", 0)
            dl, style, value = self.render_node(
                nid, label, x, y, w, h, node_spec, layer_idx, layer_colors)
            builder.add_node(dl, x, y, w, h, style=style, value=value, node_id=nid)

        # 边
        color_map = {}
        # 收集原始边数据用于箭头设置
        raw_edges = {f"{e['from']}→{e['to']}": e for e in data.get("edges", data.get("deps", []))}
        
        for er in layout.edge_routes:
            pair = f"{er['from']}→{er['to']}"
            if pair not in color_map:
                color_map[pair] = edge_colors[color_idx % len(edge_colors)]
                color_idx += 1
            color = color_map[pair]
            label = er.get("label", "")
            extra = "labelBackgroundColor=#FFFFFF;"
            if label:
                tw = text_width(label, 10)
                extra += f"labelPadding={min(20, max(8, int(tw/10)))};"
            ebase = "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"

            # 箭头设置
            raw = raw_edges.get(pair, {})
            arrow_mode = raw.get("arrow", "end")  # end/start/both/none
            arrow_style = raw.get("arrow_style", "classic")
            arrow_fill = raw.get("arrow_fill", True)
            
            if arrow_mode == "none":
                end_arrow, start_arrow, end_fill, start_fill = "none", "none", 1, 1
            elif arrow_mode == "start":
                end_arrow, start_arrow, end_fill, start_fill = "none", arrow_style, 1, 1 if arrow_fill else 0
            elif arrow_mode == "both":
                end_arrow, start_arrow, end_fill, start_fill = arrow_style, arrow_style, 1 if arrow_fill else 0, 1 if arrow_fill else 0
            else:  # end (default)
                end_arrow, start_arrow, end_fill, start_fill = arrow_style, "none", 1 if arrow_fill else 0, 1

            estyle = EdgeStyle(
                shape=ebase + extra,
                line_color=color, font_color=color, font_size=10,
                end_arrow=end_arrow, start_arrow=start_arrow,
                end_fill=end_fill, start_fill=start_fill,
            )
            builder.add_edge(
                er["from"], er["to"], label=label,
                style=estyle,
                source_port=er.get("src_port"),
                target_port=er.get("tgt_port"),
                waypoints=er.get("waypoints", []),
            )
        return builder

    def build(self, data: dict, theme: str = "default") -> DrawIOBuilder:
        """layout + render 一步完成"""
        layout = self.layout(data)
        return self.render(layout, data, theme)


# ================================================================
# 辅助函数
# ================================================================

def text_width(text: str, font_size: int = 12) -> float:
    if not text:
        return 0
    cn = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    en = len(text) - cn
    return cn * font_size * 1.8 + en * font_size * 0.6
