"""
drawio_templates - 常用图表模板生成器
基于drawio_gen核心库，提供流程图、架构图、UML类图、ER图、树形图、时序图等快捷生成
"""

import math
from drawio_gen import DrawIOBuilder, Styles, Node, Edge, NodeStyle, EdgeStyle


# ============== 布局工具 ==============

def vertical_layout(count: int, start_x: float, start_y: float,
                    node_w: float = 120, node_h: float = 60, gap: float = 80) -> list[tuple]:
    """垂直排列节点坐标"""
    return [(start_x, start_y + i * (node_h + gap)) for i in range(count)]


def horizontal_layout(count: int, start_x: float, start_y: float,
                      node_w: float = 120, node_h: float = 60, gap: float = 40) -> list[tuple]:
    """水平排列节点坐标"""
    return [(start_x + i * (node_w + gap), start_y) for i in range(count)]


def grid_layout(rows: int, cols: int, start_x: float, start_y: float,
                node_w: float = 120, node_h: float = 60, gap_x: float = 40, gap_y: float = 40) -> list[tuple]:
    """网格排列节点坐标"""
    positions = []
    for r in range(rows):
        for c in range(cols):
            positions.append((start_x + c * (node_w + gap_x), start_y + r * (node_h + gap_y)))
    return positions


def center_x_of_nodes(nodes: list[Node]) -> float:
    """计算节点列表的中心X坐标"""
    if not nodes:
        return 0
    min_x = min(n.x for n in nodes)
    max_x = max(n.x + n.width for n in nodes)
    return (min_x + max_x) / 2


def auto_size_node(label: str, style: NodeStyle = None) -> tuple:
    """根据文本长度自动计算节点尺寸"""
    chars = len(label)
    w = max(120, chars * 10 + 40)
    h = 60 if chars < 15 else (80 if chars < 30 else 100)
    return w, h


# ============== 流程图 ==============

def create_flowchart(steps: list[str], title: str = "", direction: str = "vertical",
                     colors: list[NodeStyle] = None) -> DrawIOBuilder:
    """
    创建流程图

    Args:
        steps: 步骤列表，如 ["开始", "处理数据", "结束"]
        title: 图表标题
        direction: "vertical" 或 "horizontal"
        colors: 自定义每步颜色，None则使用默认渐变
    """
    builder = DrawIOBuilder(name=title or "Flowchart")

    default_colors = [Styles.GREEN_NODE, Styles.BLUE_NODE, Styles.ORANGE_NODE,
                      Styles.PURPLE_NODE, Styles.CYAN_NODE, Styles.RED_NODE]

    node_w, node_h = 140, 60

    if direction == "vertical":
        positions = vertical_layout(len(steps), 100, 100, node_w, node_h, gap=80)
    else:
        positions = horizontal_layout(len(steps), 100, 100, node_w, node_h, gap=50)

    prev_node = None
    for i, (step, pos) in enumerate(zip(steps, positions)):
        style = (colors[i] if colors and i < len(colors)
                 else default_colors[i % len(default_colors)])
        # 第一个和最后一个是圆角
        if i == 0 or i == len(steps) - 1:
            style = NodeStyle(shape=style.shape, fill_color=style.fill_color,
                              stroke_color=style.stroke_color, font_color=style.font_color,
                              font_size=style.font_size, arc_size=20)
        w, h = auto_size_node(step)
        node = builder.add_node(step, pos[0], pos[1], w, h, style=style)
        if prev_node:
            if direction == "vertical":
                builder.connect(prev_node, node, style=Styles.DEFAULT_EDGE,
                                src_port=2, tgt_port=0)
            else:
                builder.connect(prev_node, node, style=Styles.DEFAULT_EDGE,
                                src_port=1, tgt_port=3)
        prev_node = node

    return builder


def create_decision_flowchart(
    steps: list[dict],
    title: str = "Decision Flowchart"
) -> DrawIOBuilder:
    """
    创建带判断的流程图

    Args:
        steps: 步骤字典列表
            - 普通步骤: {"type": "step", "label": "处理数据", "id": "s1"}
            - 判断: {"type": "decision", "label": "是否通过?", "id": "d1"}
            - 开始/结束: {"type": "terminal", "label": "开始", "id": "t1"}
        edges: 自动根据"next"和"yes"/"no"字段生成
    """
    builder = DrawIOBuilder(name=title)
    node_map = {}

    y = 60
    step_h = 60
    decision_h = 80
    terminal_h = 50
    gap = 80

    for s in steps:
        stype = s.get("type", "step")
        label = s.get("label", "")
        sid = s.get("id", "")

        if stype == "decision":
            w = 140
            h = decision_h
            style = Styles.DIAMOND
            node = builder.add_node(label, 200, y, w, h, style=style)
        elif stype == "terminal":
            w = 120
            h = terminal_h
            style = Styles.GREEN_NODE if "开始" in label else Styles.RED_NODE
            node = builder.add_node(label, 240, y, w, h, style=style)
        else:
            w, h = auto_size_node(label)
            style = Styles.BLUE_NODE
            node = builder.add_node(label, 220, y, w, h, style=style)

        if sid:
            node.id = sid
        node_map[sid] = node
        y += h + gap

    # Build edges from next/yes/no fields
    for s in steps:
        sid = s.get("id", "")
        if "next" in s:
            target = s["next"]
            if target in node_map:
                builder.connect(node_map[sid], node_map[target], style=Styles.DEFAULT_EDGE)
        if "yes" in s:
            target = s["yes"]
            if target in node_map:
                e = builder.connect(node_map[sid], node_map[target],
                                    label="Yes", style=Styles.GREEN_EDGE)
        if "no" in s:
            target = s["no"]
            if target in node_map:
                e = builder.connect(node_map[sid], node_map[target],
                                    label="No", style=Styles.RED_EDGE)

    return builder


# ============== 架构图 ==============

def create_architecture(layers: list[dict], title: str = "System Architecture") -> DrawIOBuilder:
    """
    创建分层架构图

    Args:
        layers: 层级列表
            [{"name": "Frontend", "components": ["React", "Vue"], "color": Styles.BLUE_NODE},
             {"name": "Backend", "components": ["API", "Auth"], "color": Styles.GREEN_NODE}]
    """
    builder = DrawIOBuilder(name=title)

    # ============ 精确布局参数 ============
    # 画布
    CANVAS_W = 1100
    MARGIN_X = 40
    MARGIN_Y = 40

    # 容器
    CONTAINER_W = CANVAS_W - MARGIN_X * 2  # 1020
    CONTAINER_HEADER_H = 28   # swimlane header 高度
    CONTAINER_PAD_X = 20      # 容器内左右内边距
    CONTAINER_PAD_Y = 12      # header 到子节点的垂直间距
    CONTAINER_BOTTOM_PAD = 12 # 子节点到容器底部的间距

    # 子节点
    COMP_MIN_W = 100          # 子节点最小宽度
    COMP_H = 50               # 子节点高度
    COMP_GAP_X = 16           # 子节点之间的水平间距

    # 层间距
    LAYER_GAP = 30            # 层与层之间的间距

    # 颜色映射
    color_map = [Styles.BLUE_NODE, Styles.ORANGE_NODE, Styles.GREEN_NODE,
                 Styles.PURPLE_NODE, Styles.CYAN_NODE, Styles.RED_NODE,
                 Styles.YELLOW_NODE, Styles.PINK_NODE, Styles.GRAY_NODE]

    # 计算每个层的高度
    layer_heights = []
    for i, layer in enumerate(layers):
        components = layer.get("components", [])
        comp_count = len(components)
        if comp_count == 0:
            h = CONTAINER_HEADER_H + CONTAINER_PAD_Y + CONTAINER_BOTTOM_PAD
        else:
            h = CONTAINER_HEADER_H + CONTAINER_PAD_Y + COMP_H + CONTAINER_BOTTOM_PAD
        layer_heights.append(h)

    # 计算总高度
    total_height = sum(layer_heights) + (len(layers) - 1) * LAYER_GAP

    # 计算每个层的Y坐标
    current_y = MARGIN_Y
    layer_positions = []
    for h in layer_heights:
        layer_positions.append(current_y)
        current_y += h + LAYER_GAP

    # 计算子节点可用宽度
    inner_w = CONTAINER_W - CONTAINER_PAD_X * 2  # 980

    prev_container = None
    for i, layer in enumerate(layers):
        name = layer["name"]
        components = layer.get("components", [])
        color = layer.get("color", color_map[i % len(color_map)])
        header_color = layer.get("header_color", None)

        y = layer_positions[i]
        container_h = layer_heights[i]

        # ============ 容器节点 ============
        # swimlane: startSize 是 header 高度
        header_style = header_color or NodeStyle(
            fill_color=color.fill_color,
            stroke_color=color.stroke_color,
            font_color="#ffffff",
            font_size=13,
            font_style=1,
            shape=f"swimlane;startSize={CONTAINER_HEADER_H};html=1;"
        )
        cont = builder.add_container(name, MARGIN_X, y, CONTAINER_W, container_h, style=header_style)

        # ============ 子节点 ============
        comp_count = len(components)
        if comp_count > 0:
            # 计算子节点宽度：均匀分配，但不超过最小宽度
            available_w = inner_w - (comp_count - 1) * COMP_GAP_X
            comp_w = max(COMP_MIN_W, available_w / comp_count)
            # 如果计算出的宽度太小，就缩小间距
            if comp_w < COMP_MIN_W:
                comp_w = COMP_MIN_W
                total_comp_w = comp_count * comp_w + (comp_count - 1) * COMP_GAP_X
                if total_comp_w > inner_w:
                    comp_w = (inner_w - (comp_count - 1) * COMP_GAP_X) / comp_count

            # 子节点起始X：容器内居中（相对于容器坐标系）
            total_row_w = comp_count * comp_w + (comp_count - 1) * COMP_GAP_X
            start_comp_x_rel = CONTAINER_PAD_X + (inner_w - total_row_w) / 2

            # 子节点Y：header下方 + pad（相对于容器坐标系）
            comp_y_rel = CONTAINER_HEADER_H + CONTAINER_PAD_Y

            for j, comp in enumerate(components):
                cx_rel = start_comp_x_rel + j * (comp_w + COMP_GAP_X)
                builder.add_node(
                    comp, cx_rel, comp_y_rel, comp_w, COMP_H,
                    style=NodeStyle(
                        shape="rounded=1;whiteSpace=wrap;html=1;",
                        fill_color="#FFFFFF",
                        stroke_color=color.stroke_color,
                        font_color=color.stroke_color,
                        font_size=11,
                        stroke_width=1,
                    ),
                    parent_id=cont.id
                )

        # ============ 层间连接线 ============
        if prev_container:
            # 连接上一个容器的底部中心到当前容器的顶部中心
            builder.add_edge(
                prev_container.id, cont.id, "",
                style=EdgeStyle(
                    end_arrow="none",
                    line_color="#999999",
                    stroke_width=2,
                    dash_pattern="5 5",
                    shape="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"
                )
            )

        prev_container = cont

    return builder


# ============== UML类图 ==============

def create_class_diagram(classes: list[dict], title: str = "UML Class Diagram") -> DrawIOBuilder:
    """
    创建UML类图

    Args:
        classes: 类定义列表
            [{"name": "User", "x": 100, "y": 100,
              "attributes": ["- id: int", "- name: string"],
              "methods": ["+ login()", "+ logout()"]}]
    """
    builder = DrawIOBuilder(name=title)

    node_map = {}
    for cls in classes:
        name = cls["name"]
        x = cls.get("x", 100)
        y = cls.get("y", 100)
        attrs = cls.get("attributes", [])
        methods = cls.get("methods", [])

        # Calculate height
        line_count = 1 + len(attrs) + len(methods)
        height = max(60, line_count * 22 + 30)
        width = max(140, max(
            [len(name) * 9 + 30] +
            [len(a) * 7 + 20 for a in attrs] +
            [len(m) * 7 + 20 for m in methods]
        ))

        # Build HTML value
        html = f'<p style="margin:0px;margin-top:4px;text-align:center;"><b>{name}</b></p>'
        if attrs:
            html += '<hr size="1"/>'
            for a in attrs:
                html += f'<p style="margin:0px;margin-left:4px;font-size:11px;">{a}</p>'
        if methods:
            html += '<hr size="1"/>'
            for m in methods:
                html += f'<p style="margin:0px;margin-left:4px;font-size:11px;">{m}</p>'

        node = builder.add_node(name, x, y, width, height,
                                style=Styles.UML_CLASS, value=html)
        node_map[name] = node

    # Relationships
    for cls in classes:
        name = cls["name"]
        if "relations" in cls:
            for rel in cls["relations"]:
                target = rel.get("target", "")
                rel_type = rel.get("type", "association")  # association, inheritance, composition, aggregation
                label = rel.get("label", "")
                if target in node_map:
                    if rel_type == "inheritance":
                        style = EdgeStyle(end_arrow="block", end_fill=0, line_color="#6c8ebf")
                    elif rel_type == "composition":
                        style = EdgeStyle(end_arrow="diamond", end_fill=1, line_color="#82b366")
                    elif rel_type == "aggregation":
                        style = EdgeStyle(end_arrow="diamond", end_fill=0, line_color="#d6b656")
                    else:
                        style = EdgeStyle(end_arrow="classic", end_fill=1)
                    builder.connect(node_map[name], node_map[target], label=label, style=style)

    return builder


# ============== ER图 ==============

def create_er_diagram(entities: list[dict], title: str = "ER Diagram") -> DrawIOBuilder:
    """
    创建ER图

    Args:
        entities: 实体列表
            [{"name": "Users", "x": 100, "y": 100,
              "fields": [
                {"name": "id", "type": "INT", "pk": True},
                {"name": "email", "type": "VARCHAR(255)"}
              ]}]
        relations: 在entity中用"relations"定义
    """
    builder = DrawIOBuilder(name=title)
    node_map = {}

    for ent in entities:
        name = ent["name"]
        x = ent.get("x", 100)
        y = ent.get("y", 100)
        fields = ent.get("fields", [])

        # Build HTML
        html = f'<p style="margin:0px;margin-top:4px;text-align:center;"><b>{name}</b></p>'
        html += '<hr size="1"/>'
        for f in fields:
            fname = f.get("name", "")
            ftype = f.get("type", "")
            pk = f.get("pk", False)
            fk = f.get("fk", False)
            prefix = ""
            if pk:
                prefix = '<u style="color:#82b366;">PK</u> '
            elif fk:
                prefix = '<span style="color:#d6b656;">FK</span> '
            html += f'<p style="margin:0px;margin-left:4px;font-size:11px;">{prefix}{fname}: {ftype}</p>'

        height = max(60, (len(fields) + 1) * 22 + 30)
        width = max(160, max(len(f.get("name", "")) * 7 + len(f.get("type", "")) * 7 + 50
                            for f in fields) if fields else 160)

        node = builder.add_node(name, x, y, width, height,
                                style=NodeStyle(
                                    shape="swimlane;startSize=26;html=1;fontStyle=1;align=center;"
                                          "fillColor=#dae8fc;strokeColor=#6c8ebf;",
                                    fill_color="#dae8fc", stroke_color="#6c8ebf"),
                                value=html)
        node_map[name] = node

    # Relations
    for ent in entities:
        name = ent["name"]
        if "relations" in ent:
            for rel in ent["relations"]:
                target = rel.get("target", "")
                label = rel.get("label", "")
                rel_type = rel.get("type", "one-to-many")  # one-to-one, one-to-many, many-to-many
                if target in node_map:
                    if rel_type == "one-to-one":
                        style = EdgeStyle(end_arrow="classic", end_fill=1, line_color="#6c8ebf")
                    elif rel_type == "many-to-many":
                        style = EdgeStyle(end_arrow="classic", start_arrow="classic",
                                          end_fill=1, start_fill=1, line_color="#b85450")
                    else:
                        style = EdgeStyle(end_arrow="classic", end_fill=1, line_color="#6c8ebf",
                                          stroke_width=2)
                    builder.connect(node_map[name], node_map[target], label=label, style=style)

    return builder


# ============== 树形图 ==============

def create_tree(root_label: str, children: list, x: float = 300, y: float = 40,
                node_w: float = 120, node_h: float = 50,
                h_gap: float = 20, v_gap: float = 80,
                style: NodeStyle = None, child_style: NodeStyle = None,
                edge_style: EdgeStyle = None) -> DrawIOBuilder:
    """
    创建树形图

    Args:
        root_label: 根节点标签
        children: 子节点列表，可以是字符串或嵌套字典:
            ["Child1", "Child2"]  - 简单列表
            [{"label": "Child1", "children": ["Grandchild1"]}]  - 嵌套
        x, y: 根节点位置
        style: 根节点样式
        child_style: 子节点样式
    """
    builder = DrawIOBuilder(name="Tree Diagram")

    def _count_leaves(node):
        if isinstance(node, str):
            return 1
        ch = node.get("children", [])
        if not ch:
            return 1
        return sum(_count_leaves(c) for c in ch)

    def _width(node):
        if isinstance(node, str):
            return node_w + h_gap
        ch = node.get("children", [])
        if not ch:
            return node_w + h_gap
        return sum(_width(c) for c in ch)

    def _add(node, x, y, depth, parent_node):
        if isinstance(node, str):
            label = node
            nstyle = child_style or Styles.BLUE_NODE
        else:
            label = node["label"]
            nstyle = child_style or Styles.BLUE_NODE

        n = builder.add_node(label, x, y, node_w, node_h, style=nstyle)
        if parent_node:
            builder.connect(parent_node, n, style=edge_style or Styles.DEFAULT_EDGE)

        if isinstance(node, dict) and "children" in node:
            ch = node["children"]
            total_w = _width(node)
            cx = x + node_w / 2 - total_w / 2
            for child in ch:
                cw = _width(child)
                child_x = cx + (cw - node_w) / 2
                _add(child, child_x, y + node_h + v_gap, depth + 1, n)
                cx += cw

    root_n = builder.add_node(root_label, x, y, node_w, node_h, style=style or Styles.GREEN_NODE)

    if children:
        total_w = sum(_width(c) for c in children)
        cx = x + node_w / 2 - total_w / 2
        for child in children:
            cw = _width(child)
            child_x = cx + (cw - node_w) / 2
            _add(child, child_x, y + node_h + v_gap, 1, root_n)
            cx += cw

    return builder


# ============== 时序图 ==============

def create_sequence_diagram(
    actors: list[str],
    messages: list[dict],
    title: str = "Sequence Diagram"
) -> DrawIOBuilder:
    """
    创建时序图

    Args:
        actors: 参与者列表, 如 ["Client", "Server", "Database"]
        messages: 消息列表
            [{"from": 0, "to": 1, "label": "HTTP Request", "type": "sync"},
             {"from": 1, "to": 2, "label": "SELECT *", "type": "sync"},
             {"from": 2, "to": 1, "label": "Results", "type": "return", "dashed": True}]
            type: "sync" | "async" | "return"
    """
    builder = DrawIOBuilder(name=title)

    actor_w = 100
    actor_h = 40
    x_gap = 180
    start_x = 80
    start_y = 40

    actor_nodes = []
    lifeline_bottom = start_y + actor_h + 40 + len(messages) * 50 + 20

    for i, actor in enumerate(actors):
        ax = start_x + i * x_gap
        # Actor box at top
        node = builder.add_node(actor, ax, start_y, actor_w, actor_h,
                                style=NodeStyle(shape="rounded=1;whiteSpace=wrap;html=1;",
                                                fill_color="#dae8fc", stroke_color="#6c8ebf",
                                                font_style=1))
        actor_nodes.append(node)

        # Actor box at bottom (mirror)
        builder.add_node(actor, ax, lifeline_bottom, actor_w, actor_h,
                         style=NodeStyle(shape="rounded=1;whiteSpace=wrap;html=1;",
                                         fill_color="#dae8fc", stroke_color="#6c8ebf",
                                         font_style=1))

        # Lifeline (dashed vertical)
        line_x = ax + actor_w / 2
        line_node = builder.add_node("", line_x - 1, start_y + actor_h + 10, 2,
                                     lifeline_bottom - start_y - actor_h - 10,
                                     style=NodeStyle(shape="line;strokeWidth=1;fillColor=none;align=left;verticalAlign=middle;spacingTop=-1;spacingLeft=3px;spacingRight=3px;rotatable=0;labelPosition=left;points=[];portConstraint=eastwest;dashed=1;",
                                                     fill_color="none", stroke_color="#999999"))

    # Messages
    for i, msg in enumerate(messages):
        from_idx = msg.get("from", 0)
        to_idx = msg.get("to", 1)
        label = msg.get("label", "")
        msg_type = msg.get("type", "sync")
        is_dashed = msg.get("dashed", msg_type == "return")

        from_x = start_x + from_idx * x_gap + actor_w
        to_x = start_x + to_idx * x_gap
        msg_y = start_y + actor_h + 50 + i * 50

        style = EdgeStyle(
            line_color="#000000",
            stroke_width=1,
            dash_pattern="5 5" if is_dashed else "",
            end_arrow="open" if is_dashed else "classic",
            end_fill=0 if is_dashed else 1,
        )

        builder.add_edge(actor_nodes[from_idx].id, actor_nodes[to_idx].id,
                         label=label, style=style)

    return builder


# ============== 思维导图 ==============

def create_mindmap(center_label: str, branches: list[dict],
                   title: str = "Mind Map") -> DrawIOBuilder:
    """
    创建思维导图（精确布局版）

    布局规则：
    - 中心节点在画布中央
    - 分支节点均匀分布在中心周围（半径200）
    - 子节点在分支节点外侧呈扇形展开
    - 所有节点宽度根据文本自适应
    - 子节点间距根据数量动态调整，避免重叠
    - 连线使用正交路由

    Args:
        center_label: 中心主题
        branches: 分支列表
            [{"label": "Branch1", "sub": ["Sub1", "Sub2"]},
             {"label": "Branch2", "sub": ["Sub3"]}]
    """
    builder = DrawIOBuilder(name=title)

    # ============ 精确布局参数 ============
    # 画布中心
    CANVAS_W, CANVAS_H = 1169, 827
    cx, cy = CANVAS_W / 2, CANVAS_H / 2

    # 中心节点
    CENTER_W = 140
    CENTER_H = 60
    CENTER_FONT = 16

    # 分支节点
    BRANCH_RADIUS = 220          # 中心到分支的距离
    BRANCH_H = 50                # 分支节点高度
    BRANCH_FONT = 13
    BRANCH_PAD_X = 24            # 文本左右内边距

    # 子节点
    SUB_RADIUS_BASE = 180        # 分支到子节点的基础距离
    SUB_H = 40                   # 子节点高度
    SUB_FONT = 11
    SUB_PAD_X = 20               # 文本左右内边距
    SUB_ANGLE_SPAN_BASE = 0.55   # 子节点扇形展开角度（弧度）
    SUB_MIN_GAP = 30             # 子节点之间的最小间距（像素）

    # 颜色
    branch_colors = [Styles.BLUE_NODE, Styles.GREEN_NODE, Styles.ORANGE_NODE,
                     Styles.PURPLE_NODE, Styles.RED_NODE, Styles.CYAN_NODE,
                     Styles.PINK_NODE, Styles.YELLOW_NODE]

    def _text_width(text: str, font_size: int, pad_x: int) -> float:
        """根据文本长度计算节点宽度"""
        chars = len(text)
        # 中文字符按1.8倍宽度计算
        cn_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
        en_chars = chars - cn_chars
        w = cn_chars * font_size * 1.8 + en_chars * font_size * 0.6 + pad_x * 2
        return max(80, w)

    def _sub_layout(subs: list, branch_angle: float, branch_w: float) -> list:
        """
        计算子节点的布局参数
        返回列表: [(x, y, w, h), ...]
        子节点在分支节点外侧按水平/垂直方向排列
        """
        count = len(subs)
        if count == 0:
            return []

        # 子节点统一高度
        sub_h = SUB_H

        # 计算每个子节点的宽度
        sub_widths = [_text_width(s, SUB_FONT, SUB_PAD_X) for s in subs]
        max_sub_w = max(sub_widths)

        # 判断分支方向（上/下/左/右）
        # angle: -pi/2=上, 0=右, pi/2=下, pi=左
        is_up = -math.pi * 0.75 < branch_angle < -math.pi * 0.25
        is_down = math.pi * 0.25 < branch_angle < math.pi * 0.75
        is_left = branch_angle < -math.pi * 0.75 or branch_angle > math.pi * 0.75
        is_right = -math.pi * 0.25 <= branch_angle <= math.pi * 0.25

        # 子节点排列方向：与分支方向垂直
        # 上下分支 → 水平排列子节点
        # 左右分支 → 垂直排列子节点
        if is_up or is_down:
            # 水平排列
            total_w = sum(sub_widths) + (count - 1) * SUB_MIN_GAP
            start_x = -total_w / 2
            positions = []
            current_x = start_x
            for j, (sub, sw) in enumerate(zip(subs, sub_widths)):
                # 子节点在分支节点外侧
                if is_up:
                    # 分支在上，子节点在分支上方
                    sx = current_x
                    sy = -sub_h - 20  # 分支节点上方20px
                else:
                    # 分支在下，子节点在分支下方
                    sx = current_x
                    sy = BRANCH_H + 20  # 分支节点下方20px
                positions.append((sx, sy, sw, sub_h))
                current_x += sw + SUB_MIN_GAP
            return positions
        else:
            # 垂直排列（左右分支）
            total_h = count * sub_h + (count - 1) * SUB_MIN_GAP
            start_y = -total_h / 2
            positions = []
            current_y = start_y
            for j, (sub, sw) in enumerate(zip(subs, sub_widths)):
                if is_left:
                    # 分支在左，子节点在分支左侧
                    sx = -sw - 20
                    sy = current_y
                else:
                    # 分支在右，子节点在分支右侧
                    sx = branch_w + 20
                    sy = current_y
                positions.append((sx, sy, sw, sub_h))
                current_y += sub_h + SUB_MIN_GAP
            return positions

    # ============ 中心节点 ============
    center_w = _text_width(center_label, CENTER_FONT, 30)
    center = builder.add_node(
        center_label, cx - center_w / 2, cy - CENTER_H / 2, center_w, CENTER_H,
        style=NodeStyle(fill_color="#1ba1e2", stroke_color="#006EAF",
                        font_color="#ffffff", font_size=CENTER_FONT, font_style=1)
    )

    # ============ 分支节点 ============
    n = len(branches)
    for i, branch in enumerate(branches):
        angle = (2 * math.pi * i) / n - math.pi / 2
        color = branch_colors[i % len(branch_colors)]

        # 分支节点位置
        branch_w = _text_width(branch["label"], BRANCH_FONT, BRANCH_PAD_X)
        bx = cx + BRANCH_RADIUS * math.cos(angle) - branch_w / 2
        by = cy + BRANCH_RADIUS * math.sin(angle) - BRANCH_H / 2

        # 判断分支方向（用于连线）
        branch_is_up = -math.pi * 0.75 < angle < -math.pi * 0.25
        branch_is_down = math.pi * 0.25 < angle < math.pi * 0.75
        branch_is_left = angle < -math.pi * 0.75 or angle > math.pi * 0.75
        branch_is_right = -math.pi * 0.25 <= angle <= math.pi * 0.25

        bnode = builder.add_node(
            branch["label"], bx, by, branch_w, BRANCH_H,
            style=NodeStyle(shape=color.shape, fill_color=color.fill_color,
                            stroke_color=color.stroke_color,
                            font_color=color.stroke_color,
                            font_size=BRANCH_FONT, font_style=1)
        )

        # 中心→分支连线：根据方向指定连接点
        # angle: -pi/2=上, 0=右, pi/2=下, pi=左
        if branch_is_up:
            center_src, branch_tgt = 0, 2  # 中心顶部 → 分支底部
        elif branch_is_down:
            center_src, branch_tgt = 2, 0  # 中心底部 → 分支顶部
        elif branch_is_left:
            center_src, branch_tgt = 3, 1  # 中心左侧 → 分支右侧
        else:  # branch_is_right
            center_src, branch_tgt = 1, 3  # 中心右侧 → 分支左侧

        builder.connect(center, bnode,
                        style=EdgeStyle(shape="edgeStyle=none;html=1;", line_color=color.stroke_color, stroke_width=2),
                        src_port=center_src, tgt_port=branch_tgt)

        # ============ 子节点 ============
        subs = branch.get("sub", [])
        sub_positions = _sub_layout(subs, angle, branch_w)

        for j, (sub, (rel_x, rel_y, sub_w, sub_h)) in enumerate(zip(subs, sub_positions)):
            # 子节点位置：相对于分支节点的偏移
            sx = bx + rel_x
            sy = by + rel_y

            snode = builder.add_node(
                sub, sx, sy, sub_w, sub_h,
                style=NodeStyle(shape="rounded=1;whiteSpace=wrap;html=1;",
                                fill_color=color.fill_color,
                                stroke_color=color.stroke_color,
                                font_color=color.stroke_color,
                                font_size=SUB_FONT)
            )

            # 分支→子节点连线：根据子节点相对位置指定连接点
            if branch_is_up:
                # 子节点在分支上方，水平排列
                branch_src, sub_tgt = 0, 2  # 分支顶部 → 子节点底部
            elif branch_is_down:
                # 子节点在分支下方，水平排列
                branch_src, sub_tgt = 2, 0  # 分支底部 → 子节点顶部
            elif branch_is_left:
                # 子节点在分支左侧，垂直排列
                branch_src, sub_tgt = 3, 1  # 分支左侧 → 子节点右侧
            else:  # branch_is_right
                # 子节点在分支右侧，垂直排列
                branch_src, sub_tgt = 1, 3  # 分支右侧 → 子节点左侧

            builder.connect(bnode, snode,
                            style=EdgeStyle(shape="edgeStyle=none;html=1;", line_color=color.stroke_color, stroke_width=1),
                            src_port=branch_src, tgt_port=sub_tgt)

    return builder


# ============== 网络拓扑图 ==============

def create_network_topology(devices: list[dict], connections: list[dict],
                            title: str = "Network Topology") -> DrawIOBuilder:
    """
    创建网络拓扑图

    Args:
        devices: 设备列表
            [{"label": "Router", "type": "cloud", "x": 300, "y": 50},
             {"label": "Server", "type": "cylinder", "x": 200, "y": 200}]
            type: cloud, cylinder, circle, hexagon, default
        connections: 连接列表
            [{"from": "Router", "to": "Server", "label": "1Gbps"}]
    """
    builder = DrawIOBuilder(name=title)

    type_to_style = {
        "cloud": Styles.CLOUD,
        "cylinder": Styles.CYLINDER,
        "circle": Styles.CIRCLE,
        "hexagon": Styles.HEXAGON,
        "document": Styles.DOCUMENT,
        "note": Styles.NOTE,
        "default": Styles.DEFAULT_NODE,
    }

    node_map = {}
    for dev in devices:
        label = dev["label"]
        dtype = dev.get("type", "default")
        x = dev.get("x", 100)
        y = dev.get("y", 100)
        w = dev.get("width", 120)
        h = dev.get("height", 60)
        style = type_to_style.get(dtype, Styles.DEFAULT_NODE)
        node = builder.add_node(label, x, y, w, h, style=style)
        node_map[label] = node

    for conn in connections:
        src = conn.get("from", "")
        tgt = conn.get("to", "")
        label = conn.get("label", "")
        if src in node_map and tgt in node_map:
            builder.connect(node_map[src], node_map[tgt], label=label,
                            style=Styles.DEFAULT_EDGE)

    return builder


