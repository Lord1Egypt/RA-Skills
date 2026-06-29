"""
drawio_layout - 统一布局计算引擎
从 architecture_microservice + tree_org_chart 中提炼的精确布局规范

所有时序图/流程图/UML类图/ER图/思维导图/拓扑图都基于这套规范做变体。
"""
import math
from drawio_gen import DrawIOBuilder, Styles, Node, NodeStyle, EdgeStyle


# ================================================================
# 统一布局常量 (从架构图 + 树形图验证)
# ================================================================
NODE_MIN_W = 100          # 节点最小宽度
NODE_H = 50               # 标准节点高度
GAP_X = 16                # 水平间距 (来自架构图: 子节点间16px)
GAP_Y = 30                # 垂直间距 (来自架构图: 层间30px)
MARGIN_X = 40             # 左右页边距
MARGIN_Y = 40             # 顶部页边距
PAD_X = 20                # 容器内左右内边距 (来自架构图)
PAD_Y = 12                # 容器header到子节点垂直间距 (来自架构图)
CANVAS_W = 1100           # 画布可用宽度
CONTAINER_W = CANVAS_W - MARGIN_X * 2  # 1020 (来自架构图)
CONTAINER_HEADER_H = 28   # swimlane header高度 (来自架构图)
FONT_SIZE = 11            # 标准字号

# 连线样式常量
EDGE_ORTHOGONAL = "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"


# ================================================================
# 1. 文本宽度计算
# ================================================================

def text_width(text: str, font_size: int = FONT_SIZE) -> float:
    """根据文本精确计算所需像素宽度（中文字符 ≈ 1.8倍字号）"""
    if not text:
        return 0
    cn = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    en = len(text) - cn
    # 中文字符宽 = font_size * 1.8，英文 = font_size * 0.6
    return cn * font_size * 1.8 + en * font_size * 0.6


def auto_node_size(label: str, font_size: int = FONT_SIZE,
                   min_w: float = NODE_MIN_W, max_w: float = 300,
                   min_h: float = NODE_H, line_h: float = 18) -> tuple:
    """
    自动计算节点尺寸。
    如果文本太长，自动换行，增加高度。
    """
    tw = text_width(label, font_size)
    # 所需宽度：文本宽 + 左右padding (16px)
    need_w = tw + 16
    w = max(min_w, min(need_w, max_w))

    # 如果文本超过最大宽度，需要换行
    if need_w > max_w:
        # 每行能容纳的字符数 (估算)
        usable_w = max_w - 16
        chars_per_line = usable_w / (font_size * 0.6)  # 按英文估算
        lines = max(1, math.ceil(len(label) / chars_per_line))
        h = max(min_h, lines * line_h + 12)
    else:
        h = min_h

    return w, h


# ================================================================
# 2. 等宽均匀分配 (从架构图提取)
# ================================================================

def equal_width_items(count: int, total_width: float, gap: float = GAP_X,
                      min_w: float = NODE_MIN_W) -> tuple:
    """
    等宽均匀分配: 计算每个子节点的宽度和起始x偏移

    来自架构图:
        item_w = (total_w - gap*(n-1)) / n
        start_x = left_pad + (inner_w - total_row_w) / 2  (居中对齐)

    Returns: (item_width, [x_offset_1, x_offset_2, ...])
    """
    if count <= 0:
        return 0, []
    inner_w = total_width - PAD_X * 2
    total_gap = gap * (count - 1)
    item_w = (inner_w - total_gap) / count
    item_w = max(min_w, item_w)

    # 重新计算行总宽（可能因min_w拉伸）
    row_w = count * item_w + total_gap
    start_x = PAD_X + (inner_w - row_w) / 2

    xs = [start_x + i * (item_w + gap) for i in range(count)]
    return item_w, xs


# ================================================================
# 3. 坐标/间隔工具
# ================================================================

def vertical_positions(count: int, start_y: float,
                       node_h: float = NODE_H, gap: float = GAP_Y) -> list:
    """垂直排列: 返回 [y1, y2, ...]"""
    return [start_y + i * (node_h + gap) for i in range(count)]


def horizontal_centered(count: int, total_width: float, node_w: float,
                        gap: float = GAP_X) -> list:
    """水平居中排列: 返回 [x1, x2, ...]"""
    if count <= 0:
        return []
    row_w = count * node_w + gap * (count - 1)
    start_x = (total_width - row_w) / 2
    return [start_x + i * (node_w + gap) for i in range(count)]


def center_in_container(node_w: float, container_w: float, pad: float = PAD_X) -> float:
    """在容器范围内居中一个节点, 返回起始x"""
    usable = container_w - pad * 2
    return pad + (usable - node_w) / 2


# ================================================================
# 4. 节点创建辅助 (统一风格)
# ================================================================

_STYLE_COLORS = [
    ("#dae8fc", "#6c8ebf"),  # 蓝
    ("#ffe6cc", "#d6b656"),  # 橙
    ("#d5e8d4", "#82b366"),  # 绿
    ("#e1d5e7", "#9673a6"),  # 紫
    ("#f8cecc", "#b85450"),  # 红
    ("#d4e1f5", "#6c8ebf"),  # 青
    ("#fff2cc", "#d6b656"),  # 黄
    ("#f5f5f5", "#666666"),  # 灰
]


def make_style(fill_color: str = "#dae8fc", stroke_color: str = "#6c8ebf",
               font_color: str = None, font_size: int = FONT_SIZE,
               font_style: int = 0, shape: str = "rounded=1;whiteSpace=wrap;html=1;",
               extra: str = "") -> NodeStyle:
    """统一创建节点样式"""
    return NodeStyle(
        shape=shape,
        fill_color=fill_color,
        stroke_color=stroke_color,
        font_color=font_color or stroke_color,
        font_size=font_size,
        font_style=font_style,
    )


def make_swimlane_style(fill_color: str, stroke_color: str, font_size: int = 13) -> NodeStyle:
    """创建swimlane容器样式 (架构图风格)"""
    return NodeStyle(
        shape=f"swimlane;startSize={CONTAINER_HEADER_H};html=1;",
        fill_color=fill_color,
        stroke_color=stroke_color,
        font_color="#ffffff",
        font_size=font_size,
        font_style=1,
    )


def add_node(builder: DrawIOBuilder, label: str, x: float, y: float,
             w: float = None, h: float = NODE_H,
             color_idx: int = 0, font_size: int = FONT_SIZE,
             font_style: int = 0, parent_id: str = "1",
             value: str = "", shape: str = "rounded=1;whiteSpace=wrap;html=1;",
             fill_color: str = None, stroke_color: str = None) -> Node:
    """统一添加节点（自动处理样式和尺寸）"""
    if w is None:
        w, _ = auto_node_size(label, font_size)
    if fill_color is None:
        fc, sc = _STYLE_COLORS[color_idx % len(_STYLE_COLORS)]
    else:
        fc, sc = fill_color, stroke_color or fill_color

    style = NodeStyle(
        shape=shape,
        fill_color=fc,
        stroke_color=sc,
        font_color=sc,
        font_size=font_size,
        font_style=font_style,
    )
    return builder.add_node(label, x, y, w, h, style=style,
                            parent_id=parent_id, value=value)


def add_edge(builder: DrawIOBuilder, src, tgt, label: str = "",
             color: str = "#6c8ebf", width: int = 1, dashed: bool = False,
             end_arrow: str = "classic", start_arrow: str = "none",
             end_fill: int = 1, start_fill: int = 1,
             src_port: int = None, tgt_port: int = None) -> None:
    """统一添加连线"""
    style = EdgeStyle(
        shape=EDGE_ORTHOGONAL,
        line_color=color,
        stroke_width=width,
        dash_pattern="5 5" if dashed else "",
        end_arrow=end_arrow,
        start_arrow=start_arrow,
        end_fill=end_fill,
        start_fill=start_fill,
    )
    builder.add_edge(src.id, tgt.id, label, style=style,
                     source_port=src_port, target_port=tgt_port)


def make_connection(cx: float, cy: float, radius: float, angle: float,
                    obj_w: float, obj_h: float) -> tuple:
    """
    计算极坐标位置，返回 (x, y) 使得物体中心在(CX+cos, CY+sin)处
    
    用于思维导图的放射状布局
    """
    x = cx + radius * math.cos(angle) - obj_w / 2
    y = cy + radius * math.sin(angle) - obj_h / 2
    return x, y


# ================================================================
# 5. 容器创建辅助 (架构图风格)
# ================================================================

def create_layer_container(builder: DrawIOBuilder, name: str,
                           x: float, y: float, w: float, h: float,
                           fill_color: str, stroke_color: str) -> Node:
    """创建架构图层容器（swimlane）"""
    style = make_swimlane_style(fill_color, stroke_color)
    container = builder.add_container(name, x, y, w, h, style=style)
    return container


def fill_layer_components(builder: DrawIOBuilder, container: Node,
                          components: list, stroke_color: str,
                          container_w: float = CONTAINER_W) -> list:
    """在容器内均匀填充子节点（架构图风格）"""
    if not components:
        return []
    count = len(components)
    comp_w, xs = equal_width_items(count, container_w)

    nodes = []
    comp_y = CONTAINER_HEADER_H + PAD_Y
    for j, (comp, cx) in enumerate(zip(components, xs)):
        n = add_node(
            builder, comp, cx, comp_y, w=comp_w, h=NODE_H,
            fill_color="#FFFFFF", stroke_color=stroke_color,
            parent_id=container.id,
        )
        nodes.append(n)
    return nodes


# ================================================================
# 6. 网格布局
# ================================================================

def auto_grid(count: int, cols: int,
              cell_w: float, cell_h: float,
              gap_x: float = GAP_X, gap_y: float = GAP_Y,
              start_x: float = MARGIN_X, start_y: float = MARGIN_Y) -> list:
    """
    自动网格布局: 根据数量和列数计算每个元素位置
    返回 [(x, y), ...]
    """
    rows = math.ceil(count / cols)
    positions = []
    for i in range(count):
        r = i // cols
        c = i % cols
        x = start_x + c * (cell_w + gap_x)
        y = start_y + r * (cell_h + gap_y)
        positions.append((x, y))
    return positions


def auto_grid_centered(count: int, cols: int,
                       cell_w: float, cell_h: float,
                       total_w: float = 1100,
                       gap_x: float = GAP_X, gap_y: float = GAP_Y,
                       start_y: float = MARGIN_Y) -> list:
    """
    居中网格布局: 每行居中对齐
    返回 [(x, y), ...]
    """
    rows = math.ceil(count / cols)
    positions = []
    for r in range(rows):
        items_this_row = min(cols, count - r * cols)
        # 计算该行的总宽度
        row_w = items_this_row * cell_w + gap_x * (items_this_row - 1)
        row_start = (total_w - row_w) / 2
        for c in range(items_this_row):
            x = row_start + c * (cell_w + gap_x)
            y = start_y + r * (cell_h + gap_y)
            positions.append((x, y))
    return positions
