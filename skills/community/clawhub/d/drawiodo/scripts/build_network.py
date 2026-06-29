"""
build_network.py — 数据中心网络拓扑图生成器
使用 Sugiyama 分层布局 + 每边独立路径 + 扇出路由避免线重叠
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))

from drawio_gen import DrawIOBuilder, NodeStyle, EdgeStyle, Styles
from drawio_layout import text_width
from drawio_route import ObstacleRouter, Rect


# ================================================================
# 颜色配置（按连接类型）
# ================================================================
CONNECTION_COLORS = {
    "core_dist":    "#1ba1e2",  # 蓝 — Core→Distribution
    "dist_access":  "#82b366",  # 绿 — Distribution→Access
    "access_srv":   "#6c8ebf",  # 深蓝 — Access→Server
    "redundant":    "#b85450",  # 红 — 冗余链路
    "mgmt":         "#9673a6",  # 紫 — 管理链路
    "default":      "#666666",  # 灰 — 默认
}

ORTHO_BASE = (
    "edgeStyle=orthogonalEdgeStyle;rounded=0;"
    "orthogonalLoop=1;jettySize=auto;html=1;"
)

LAYER_FILL_COLORS = [
    ("#dae8fc", "#6c8ebf"),  # Core Layer
    ("#ffe6cc", "#d6b656"),  # Distribution Layer
    ("#d5e8d4", "#82b366"),  # Access Layer
    ("#e1d5e7", "#9673a6"),  # Server Layer
    ("#f8cecc", "#b85450"),  # Extra
    ("#fff2cc", "#d6b656"),  # Extra
]


# ================================================================
# 1. 动态尺寸计算
# ================================================================

def auto_node_size(label: str, font_size: int = 12) -> tuple:
    """根据标签文本自动计算节点宽高"""
    tw = text_width(label, font_size)
    w = max(100, min(tw + 24, 200))
    h = 50
    # 如果文本太长自动换行撑高
    if tw > 176:  # 200-24
        lines = math.ceil(len(label) / 12)
        h = max(50, lines * 18 + 14)
    return w, h


def calc_edge_label_gap(connections: list, font_size: int = 10) -> float:
    """根据最长连线标签计算层间距"""
    max_tw = 0
    for conn in connections:
        label = conn.get("label", "")
        if label:
            tw = text_width(label, font_size)
            max_tw = max(max_tw, tw)
    # 层间距 = max(80, 最长标签宽 + 60)
    return max(120, max_tw + 80)


# ================================================================
# 2. 分层布局
# ================================================================

def layout_layers(layers: list, margin_x: int = 40, margin_y: int = 40,
                  canvas_w: int = 1100, gap_y: float = None):
    """
    计算所有节点的位置。
    每层内节点水平居中均匀分布。
    层间垂直排列。

    Returns: {label: (x, y, w, h, layer_idx)}
    """
    if gap_y is None:
        gap_y = 120  # 默认层间距

    result = {}  # label -> (x, y, w, h, layer_idx)

    y = margin_y
    for li, layer in enumerate(layers):
        nodes = layer["nodes"]
        n = len(nodes)
        if n == 0:
            continue

        # 计算该层的节点宽度
        node_sizes = [auto_node_size(nd["label"]) for nd in nodes]
        node_ws = [s[0] for s in node_sizes]
        node_hs = [s[1] for s in node_sizes]

        # 该层统一节点宽 = max(所有节点宽)
        layer_w = max(node_ws)
        layer_h = max(node_hs)

        # 层内水平居中均匀分布
        total_w = n * layer_w + GAP_X * (n - 1)
        start_x = margin_x + (canvas_w - margin_x * 2 - total_w) / 2

        x = start_x
        for j, nd in enumerate(nodes):
            result[nd["label"]] = (x, y, layer_w, layer_h, li)
            x += layer_w + GAP_X

        # 该层高度 = 节点高 + header空间
        y += layer_h + gap_y

    return result


# ================================================================
# 3. 每边独立路径规划（扇出路由避免重叠）
# ================================================================

def build_network_topology(layers: list, connections: list,
                           title: str = "Network Topology",
                           canvas_w: int = 1100, margin_x: int = 40,
                           margin_y: int = 40) -> DrawIOBuilder:
    """
    生成数据中心网络拓扑图。

    layers = [
        {"name": "Core层", "nodes": [{"label": "Core-SW1"}, ...]},
        ...
    ]
    connections = [
        {"from": "Core-SW1", "to": "Dist-SW1",
         "label": "10Gbps", "type": "core_dist"},
        ...
    ]
    """
    global GAP_X
    # 计算动态间距
    max_label_gap = calc_edge_label_gap(connections)
    gap_y = max(120, max_label_gap)

    # 布局节点
    pos = layout_layers(layers, margin_x, margin_y, canvas_w, gap_y)

    builder = DrawIOBuilder(name=title)

    # --- 创建节点 ---
    node_map = {}  # label -> Node
    for label, (x, y, w, h, li) in pos.items():
        fc, sc = LAYER_FILL_COLORS[li % len(LAYER_FILL_COLORS)]
        style = NodeStyle(fill_color=fc, stroke_color=sc, font_color=sc)
        node = builder.add_node(label, x, y, w, h, style=style)
        node_map[label] = node

    # --- 准备障碍物 ---
    router = ObstacleRouter(pad=5)
    for label, (x, y, w, h, _) in pos.items():
        n = node_map[label]
        router.add_obstacles([n])

    # --- 统计各目标节点的入边数（用于扇出） ---
    target_edge_count = {}
    for conn in connections:
        tgt = conn["to"]
        target_edge_count[tgt] = target_edge_count.get(tgt, 0) + 1

    # 已处理到某目标的边计数（分配偏移量）
    target_edge_idx = {}

    # --- 创建连线 ---
    for conn in connections:
        src_label = conn["from"]
        tgt_label = conn["to"]
        conn_type = conn.get("type", "default")
        label = conn.get("label", "")

        if src_label not in node_map or tgt_label not in node_map:
            continue

        src_node = node_map[src_label]
        tgt_node = node_map[tgt_label]

        # 获取颜色
        color = CONNECTION_COLORS.get(conn_type, CONNECTION_COLORS["default"])

        # 获取层索引
        src_li = pos[src_label][4]
        tgt_li = pos[tgt_label][4]

        # ===== 端口选择 =====
        # 基础规则：同层用 右→左，跨层用 底→顶
        if src_li == tgt_li:
            src_port = 1  # 右
            tgt_port = 3  # 左
        elif tgt_li > src_li:
            src_port = 2  # 底
            tgt_port = 0  # 顶
        else:
            src_port = 0  # 顶
            tgt_port = 2  # 底

        # ===== 扇出偏移（多边到同一目标时分散路径） =====
        idx = target_edge_idx.get(tgt_label, 0)
        target_edge_idx[tgt_label] = idx + 1
        total_to_target = target_edge_count[tgt_label]
        fan_offset = 0
        if total_to_target > 1:
            # 扇出偏移 = (idx - (total-1)/2) * 偏移单位
            fan_offset = (idx - (total_to_target - 1) / 2) * 18

        # ===== 计算 waypoints =====
        sx = src_node.x + src_node.width / 2
        sy = src_node.y + src_node.height
        tx = tgt_node.x + tgt_node.width / 2
        ty = tgt_node.y

        # 计算路径
        waypoints = _calc_edge_path(
            src_node, tgt_node,
            src_port, tgt_port,
            src_li, tgt_li,
            router, pos,
            fan_offset,
            label,
        )

        # ===== 构建 edge style =====
        extra_str = ""
        if label:
            extra_str += "labelBackgroundColor=#FFFFFF;"
            tw = text_width(label)
            if tw > 60:
                extra_str += f"labelPadding={min(20, max(8, int(tw / 10)))};"
            else:
                extra_str += "labelPadding=8;"

        # EdgeStyle 的 shape 只放基础路由样式，build() 会自动加 strokeColor/fontColor
        edge_style = EdgeStyle(
            shape=ORTHO_BASE + extra_str,
            line_color=color,
            font_color=color,
            font_size=10,
        )

        # 添加连线
        builder.add_edge(
            src_node.id, tgt_node.id, label=label,
            style=edge_style,
            source_port=src_port,
            target_port=tgt_port,
            waypoints=waypoints,
        )

    return builder


def _calc_edge_path(src_node, tgt_node, src_port, tgt_port,
                    src_li, tgt_li, router, pos,
                    fan_offset: float, label: str):
    """
    计算每条边的独立路径（waypoints），避免线重叠+穿过节点。
    使用多级策略：
    1. 标准 L-path
    2. 带扇出偏移的 Z-path
    3. 使用 ObstacleRouter
    """
    sx = src_node.x + src_node.width / 2
    sy = src_node.y + src_node.height if src_port == 2 else src_node.y
    tx = tgt_node.x + tgt_node.width / 2
    ty = tgt_node.y if tgt_port == 0 else tgt_node.y + tgt_node.height

    exclude = {src_node.id, tgt_node.id}

    # Strategy 1: 标准 L-path (水平→垂直)
    # 使用扇出偏移来分散平行边
    mid_x = (sx + tx) / 2 + fan_offset
    path1 = [(sx, sy), (mid_x, sy), (mid_x, ty), (tx, ty)]
    if _path_clear(path1, router.obstacles, exclude):
        return [(mid_x, sy), (mid_x, ty)]

    # Strategy 1b: 垂直 L-path
    mid_y = (sy + ty) / 2 + fan_offset
    path1b = [(sx, sy), (sx, mid_y), (tx, mid_y), (tx, ty)]
    if _path_clear(path1b, router.obstacles, exclude):
        return [(sx, mid_y), (tx, mid_y)]

    # Strategy 2: 偏移 Z-path (多个偏移值尝试)
    for offset in [30, 60, 90, 120, -30, -60, -90, -120]:
        mx = (sx + tx) / 2 + offset + fan_offset
        p2 = [(sx, sy), (mx, sy), (mx, ty), (tx, ty)]
        if _path_clear(p2, router.obstacles, exclude):
            return [(mx, sy), (mx, ty)]

    # Strategy 3: 使用 ObstableRouter
    try:
        wp = router.route(src_node, tgt_node,
                          src_port=src_port,
                          tgt_port=tgt_port)
        if wp:
            return wp
    except Exception:
        pass

    # Strategy 4: 绝对保底 — 从图边缘绕行
    # 从目标节点上方来，但偏左/偏右
    lane_x = tgt_node.x + tgt_node.width / 2 + fan_offset
    lane_x = max(20, min(1080, lane_x))
    return [(lane_x, sy), (lane_x, ty)]


def _path_clear(points, obstacles, exclude: set) -> bool:
    """检查路径是否不与任何障碍物相交(排除source/target)"""
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        # 线段AABB
        sx_min, sx_max = (x1, x2) if x1 <= x2 else (x2, x1)
        sy_min, sy_max = (y1, y2) if y1 <= y2 else (y2, y1)
        seg = Rect(sx_min, sy_min, sx_max - sx_min, sy_max - sy_min)

        for rect, nid in obstacles:
            if nid in exclude:
                continue
            if seg.overlaps(rect):
                return False
    # 检查边标签中点是否在障碍物内
    # 取最中间段的中间点作为标签位置
    if len(points) >= 3:
        mid_seg = len(points) // 2
        mx = (points[mid_seg - 1][0] + points[mid_seg][0]) / 2
        my = (points[mid_seg - 1][1] + points[mid_seg][1]) / 2
        for rect, nid in obstacles:
            if nid in exclude:
                continue
            if rect.expanded(0).contains(mx, my):
                return False

    return True


# ================================================================
# 常量
# ================================================================
GAP_X = 30  # 节点水平间距
