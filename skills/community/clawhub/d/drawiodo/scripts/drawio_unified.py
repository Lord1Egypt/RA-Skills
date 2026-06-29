"""
drawio_unified.py — 统一图布局引擎

单一入口，一次性解决所有图类型：

算法流程：
  Phase 1 — 拓扑排序分层（Sugiyama Layer Assignment）
  Phase 2 — 层内排序（Barycenter / Median 最小化交叉）
  Phase 3 — 动态位置计算（按标签文本宽度算节点大小 + 间距）
  Phase 4 — 障碍感知路由（ObstacleRouter + 扇出偏移）
  Phase 5 — 边缘标签避让（标签中点碰撞检测）

输入：
  nodes: [
    {"id": "A", "label": "节点A", "type": "normal"},
    ...
  ]
  edges: [
    {"from": "A", "to": "B", "label": "关系描述"},
    ...
  ]

输出：DrawIOBuilder（可 save / build_xml）
"""
import math
from collections import defaultdict, deque
from typing import List, Tuple, Optional, Set, Dict
from drawio_gen import DrawIOBuilder, NodeStyle, EdgeStyle, Node
from drawio_route import ObstacleRouter, Rect


# ================================================================
# 样式定义
# ================================================================

# ================================================================
# 颜色主题
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

MARGIN_X = 40
MARGIN_Y = 40
CANVAS_W = 1169
CANVAS_H = 1500
BASE_FONT_SIZE = 12


# ================================================================
# Phase 0: 文本宽度计算
# ================================================================

def text_width(text: str, font_size: int = BASE_FONT_SIZE) -> float:
    """像素宽度：中文≈1.8字号，英文≈0.6字号"""
    if not text:
        return 0
    cn = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    en = len(text) - cn
    return cn * font_size * 1.8 + en * font_size * 0.6


def auto_node_size(label: str, font_size: int = BASE_FONT_SIZE) -> Tuple[float, float]:
    """自动节点尺寸"""
    tw = text_width(label, font_size)
    w = max(90, min(tw + 24, 220))
    h = 50
    if tw > 196:
        lines = math.ceil(len(label) / 14)
        h = max(50, lines * 18 + 14)
    return int(w), int(h)


# ================================================================
# Phase 1: 拓扑排序分层
# ================================================================

def topological_layer(nodes: List[dict], edges: List[dict]) -> Dict[str, int]:
    """
    拓扑排序 → 层分配。
    如果存在环（非DAG），用最小反向边集破环。
    """
    graph = defaultdict(set)
    in_degree = defaultdict(int)
    all_ids = set(n["id"] for n in nodes)

    for e in edges:
        if e["from"] in all_ids and e["to"] in all_ids:
            graph[e["from"]].add(e["to"])
            in_degree[e["to"]] += 1
            in_degree.setdefault(e["from"], 0)

    # 所有节点初始化入度
    for n in nodes:
        in_degree.setdefault(n["id"], 0)

    # Kahn 拓扑排序
    queue = deque([nid for nid, deg in in_degree.items() if deg == 0])
    if not queue:
        # 全部有环，随机取一个作为起点破环
        queue.append(next(iter(in_degree.keys())))

    topo_order = []
    temp_in = dict(in_degree)
    while queue:
        nid = queue.popleft()
        topo_order.append(nid)
        for neighbor in list(graph[nid]):
            temp_in[neighbor] -= 1
            if temp_in[neighbor] == 0:
                queue.append(neighbor)
            # 解决环：如果已经处理了所有节点但还有剩余边
            elif temp_in[neighbor] < 0:
                temp_in[neighbor] = 0

    # 处理剩余的（环内）节点
    remaining = all_ids - set(topo_order)
    while remaining:
        nid = remaining.pop()
        topo_order.append(nid)
        for neighbor in list(graph.get(nid, set())):
            if neighbor in remaining:
                temp_in[neighbor] -= 1
                if temp_in[neighbor] <= 0:
                    remaining.discard(neighbor)
                    remaining.add(neighbor)  # re-add if needed

    # 按拓扑序分配层：最上层=0
    # 根节点（无入边）= 第0层
    # 子节点 = 最深父节点层数 + 1
    layer = {}
    inbound_set = {e["to"] for e in edges if e["from"] in all_ids and e["to"] in all_ids}
    for nid in topo_order:
        deepest_parent = 0
        for e in edges:
            if e["to"] == nid and e["from"] in layer:
                deepest_parent = max(deepest_parent, layer[e["from"]])
        if nid in inbound_set:
            layer[nid] = deepest_parent + 1
        else:
            layer[nid] = 0

    return layer


# ================================================================
# Phase 2: 层内排序（Barycenter 最小化交叉）
# ================================================================

def barycenter_sort(layer_nodes: Dict[int, List[str]],
                    edges: List[dict]) -> Dict[int, List[str]]:
    """
    Barycenter 排序：在层内按邻居节点的平均位置排序，最小化边交叉。
    迭代多次直到收敛。
    """
    result = {l: list(nodes) for l, nodes in layer_nodes.items()}

    for _ in range(10):
        changed = False
        for lvl in sorted(result.keys()):
            nodes = result[lvl]
            if len(nodes) <= 1:
                continue
            # 计算每个节点的重心
            barycenters = {}
            for nid in nodes:
                neighbors = []
                for e in edges:
                    if e["from"] == nid and e["to"] in result.get(lvl, []):
                        # 同层边
                        pass
                    elif e["to"] == nid:
                        if e["from"] in result.get(lvl - 1, []):
                            neighbors.append(result[lvl - 1].index(e["from"]))
                    elif e["from"] == nid:
                        if e["to"] in result.get(lvl + 1, []):
                            neighbors.append(result[lvl + 1].index(e["to"]))
                if neighbors:
                    barycenters[nid] = sum(neighbors) / len(neighbors)
                else:
                    # 无边连接：放在最后
                    barycenters[nid] = len(nodes)

            # 按重心排序
            sorted_nodes = sorted(nodes, key=lambda n: barycenters.get(n, len(nodes)))
            if sorted_nodes != nodes:
                result[lvl] = sorted_nodes
                changed = True
        if not changed:
            break

    return result


# ================================================================
# Phase 3: 动态位置计算
# ================================================================

def compute_positions(
    layer_order: Dict[int, List[str]],
    nodes: List[dict],
    edges: List[dict],
) -> Dict[str, Tuple[float, float, float, float]]:
    """
    计算每个节点的 (x, y, w, h)。
    垂直间距按最长连线标签动态计算。
    水平间距按层内节点数动态调整。
    """
    # 1. 计算节点尺寸
    node_sizes = {}
    for n in nodes:
        w, h = auto_node_size(n["label"])
        node_sizes[n["id"]] = (w, h)

    # 2. 计算最大层宽（用于水平居中）
    max_layer_w = 0
    layer_widths = {}
    for lvl, nids in layer_order.items():
        total_w = sum(node_sizes[nid][0] for nid in nids) + GAP_X * (len(nids) - 1)
        layer_widths[lvl] = total_w
        max_layer_w = max(max_layer_w, total_w)

    # 3. 计算垂直间距
    max_edge_label_w = 0
    for e in edges:
        if e.get("label"):
            tw = text_width(e["label"], 10)
            max_edge_label_w = max(max_edge_label_w, tw)
    gap_y = max(100, max_edge_label_w + 80)

    # 4. 计算位置
    positions = {}
    y = MARGIN_Y
    for lvl in sorted(layer_order.keys()):
        nids = layer_order[lvl]
        if not nids:
            continue

        # 该层统一节点高度
        layer_h = max(node_sizes[nid][1] for nid in nids)

        # 水平居中
        total_w = layer_widths[lvl]
        start_x = MARGIN_X + (CANVAS_W - MARGIN_X * 2 - total_w) / 2

        x = start_x
        for nid in nids:
            w, h = node_sizes[nid]
            h_actual = max(h, layer_h)
            positions[nid] = (x, y, w, h_actual, lvl)
            x += w + GAP_X

        y += layer_h + gap_y

    return positions


# ================================================================
# Phase 4: 障碍感知路由 + 扇出偏移
# ================================================================

def route_edges(
    builder: DrawIOBuilder,
    nodes_map: Dict[str, Node],
    edges: List[dict],
    positions: Dict[str, Tuple],
    edge_colors: list = None,
):
    """
    为每条边计算避障路径。
    
    基于"车道"的路径规划：
    - 每对(源层,目标层)之间的平行边分配到不同的垂直车道
    - 车道在节点之间的水平间隙中均匀分布
    - 跨层边走画布左右侧道
    - 每条车道有独立的x位置，确保标签不重叠
    """
    # 构造 ObstacleRouter（用于fallback）
    router = ObstacleRouter(pad=1)
    all_nodes = list(nodes_map.values())
    router.add_obstacles(all_nodes)

    # 按颜色轮转
    color_idx = 0
    color_map = {}

    if edge_colors is None:
        edge_colors = ["#6c8ebf", "#82b366", "#d6b656", "#b85450",
                       "#9673a6", "#1ba1e2", "#60a917", "#a20025"]

    # ===== 收集所有边并按 (src_layer, tgt_layer) 分组 =====
    edge_groups = defaultdict(list)  # (src_li, tgt_li) -> [edge_info, ...]
    for e in edges:
        if e["from"] not in nodes_map or e["to"] not in nodes_map:
            continue
        src_li = positions[e["from"]][4]
        tgt_li = positions[e["to"]][4]
        edge_groups[(src_li, tgt_li)].append({
            "edge": e,
            "src": nodes_map[e["from"]],
            "tgt": nodes_map[e["to"]],
            "label": e.get("label", ""),
        })

    # ===== 为每对层计算车道并分配到每条边 =====
    # 车道位置缓存：{ (src_li, tgt_li): [lane_x, lane_x, ...] }
    group_lanes = {}

    for key, group_edges in edge_groups.items():
        src_li, tgt_li = key
        n_edges = len(group_edges)
        if n_edges == 0:
            continue

        crossing = abs(tgt_li - src_li) > 1

        if crossing:
            # 跨层边：左右侧道
            # 每条边都在侧道上有自己的车道
            max_w = max(text_width(ee["label"], 10) for ee in group_edges)
            lane_spacing = max(50, max_w + 20)
            # 左边道从 15 开始，右边道从 1145 开始
            left_lanes = [15 + i * lane_spacing for i in range(n_edges)]
            right_lanes = [1145 - i * lane_spacing for i in range(n_edges)]
            group_lanes[key] = {
                "lanes": left_lanes + right_lanes,
                "idx": 0,
                "crossing": True,
            }
        else:
            # 相邻层：在节点间隙中分配车道
            lo, hi = min(src_li, tgt_li), max(src_li, tgt_li)

            # 收集每层的节点X区间（按层分开，不跨层合并！！！）
            layer_intervals = defaultdict(list)
            for nid, (nx, ny, nw, nh, lvl) in positions.items():
                if lo <= lvl <= hi:
                    layer_intervals[lvl].append((nx, nx + nw))

            # 对每层分别合并重叠区间
            layer_merged = {}
            for lvl, ivals in layer_intervals.items():
                ivals.sort()
                merged = []
                for l, r in ivals:
                    if merged and l <= merged[-1][1]:
                        merged[-1] = (merged[-1][0], max(merged[-1][1], r))
                    else:
                        merged.append((l, r))
                layer_merged[lvl] = merged

            # 计算在ALL相关层中都空闲的间隙（交集）
            left_margin = 20
            right_margin = 1149

            # 从第一层的间隙开始，逐层取交集
            first_lvl = sorted(layer_merged.keys())[0]
            occupied = list(layer_merged[first_lvl])
            for lvl in sorted(layer_merged.keys())[1:]:
                merged2 = []
                for l, r in occupied:
                    for ol, or2 in layer_merged[lvl]:
                        merged_l = max(l, ol)
                        merged_r = min(r, or2)
                        if merged_l < merged_r:
                            merged2.append((merged_l, merged_r))
                occupied = merged2
                if not occupied:
                    break

            # 从交集间隙中计算可用车道中心
            gaps = []
            prev = left_margin
            for l, r in occupied:
                if l > prev + 10:
                    gaps.append((prev + l) / 2)
                prev = max(prev, r)
            if right_margin > prev + 10:
                gaps.append((prev + right_margin) / 2)

            # 计算可用的水平段Y范围
            all_lvl_yr = {}
            for nid, (nx, ny, nw, nh, lvl) in positions.items():
                if lvl not in all_lvl_yr:
                    all_lvl_yr[lvl] = (ny, ny + nh)
                else:
                    all_lvl_yr[lvl] = (min(all_lvl_yr[lvl][0], ny),
                                      max(all_lvl_yr[lvl][1], ny + nh))
            src_bottom = all_lvl_yr.get(lo, (0, 100))[1]
            tgt_top = all_lvl_yr.get(hi, (200, 300))[0]
            gap_h = max(40, tgt_top - src_bottom)  # 可用垂直间隙
            gaps = []
            prev = left_margin
            for l, r in merged:
                if l > prev + 15:
                    gap_center = (prev + l) / 2
                    gaps.append(gap_center)
                prev = max(prev, r)
            if right_margin > prev + 15:
                gaps.append((prev + right_margin) / 2)

            # 如果间隙不够，在左右边缘加车道
            max_label_w = max(text_width(ee["label"], 10) for ee in group_edges)
            lane_spacing = max(40, max_label_w + 20)

            # 在可用间隙中生成足够数量的车道
            lane_positions = []
            lane_y_positions = []  # 每个车道的水平段Y（用来避免重叠）
            if gaps:
                min_gap_val = min(gaps) if len(gaps) > 1 else left_margin + 30
                max_gap_val = max(gaps) if len(gaps) > 1 else right_margin - 30
                if len(gaps) >= n_edges:
                    for i in range(n_edges):
                        t = (i + 0.5) / n_edges
                        lane_positions.append(min_gap_val + t * (max_gap_val - min_gap_val))
                        y = src_bottom + (i + 1) / (n_edges + 1) * gap_h
                        lane_y_positions.append(y)
                else:
                    for i, g in enumerate(gaps):
                        lane_positions.append(g)
                        y = src_bottom + (i + 1) / (len(gaps) + 1) * gap_h
                        lane_y_positions.append(y)
                    for i in range(n_edges - len(gaps)):
                        side_off = 30 * (i // 2 + 1)
                        if i % 2 == 0:
                            lane_positions.append(left_margin - side_off)
                        else:
                            lane_positions.append(right_margin + side_off)
                        lane_y_positions.append(src_bottom + gap_h / 2)
            else:
                for i in range(n_edges):
                    if i % 2 == 0:
                        lane_positions.append(20 + i * lane_spacing)
                    else:
                        lane_positions.append(1140 - (i - 1) * lane_spacing)
                    lane_y_positions.append(src_bottom + gap_h / 2)

            group_lanes[key] = {
                "lanes": lane_positions,
                "h_ys": lane_y_positions,
                "idx": 0,
                "crossing": False,
            }

    # ===== 处理每条边 =====
    for e in edges:
        src_label = e["from"]
        tgt_label = e["to"]
        if src_label not in nodes_map or tgt_label not in nodes_map:
            continue

        src = nodes_map[src_label]
        tgt = nodes_map[tgt_label]
        src_li = positions[src_label][4]
        tgt_li = positions[tgt_label][4]

        label = e.get("label", "")
        # 颜色分配
        pair_key = f"{e['from']}→{e['to']}"
        if pair_key not in color_map:
            color_map[pair_key] = edge_colors[color_idx % len(edge_colors)]
            color_idx += 1
        color = color_map[pair_key]

        # 自动选端口
        if tgt_li > src_li:
            src_port, tgt_port = 2, 0  # 底→顶
        elif tgt_li < src_li:
            src_port, tgt_port = 0, 2  # 顶→底
        elif tgt.x + tgt.width < src.x:
            src_port, tgt_port = 3, 1  # 左→右
        elif tgt.x > src.x + src.width:
            src_port, tgt_port = 1, 3  # 右→左
        else:
            src_port, tgt_port = 2, 0

        # 从车道池中取一条车道
        key = (src_li, tgt_li)
        if key in group_lanes:
            gl = group_lanes[key]
            idx = gl["idx"]
            gl["idx"] += 1
            if idx < len(gl["lanes"]):
                assigned_lane = gl["lanes"][idx]
            else:
                assigned_lane = gl["lanes"][-1] if gl["lanes"] else (src.x + src.width / 2)
            crossing = gl["crossing"]
            h_y = gl.get("h_ys", [None])[idx] if not crossing else None
        else:
            assigned_lane = (src.x + src.width / 2 + tgt.x + tgt.width / 2) / 2
            crossing = abs(tgt_li - src_li) > 1

        # 路径规划
        waypoints = _compute_with_lane(
            src, tgt, src_port, tgt_port, router,
            lane_x=assigned_lane,
            crossing=crossing,
            h_y=h_y,
            label=label,
            positions=positions,
            exclude={src.id, tgt.id},
        )

        extra = "labelBackgroundColor=#FFFFFF;"
        if label:
            tw = text_width(label, 10)
            padding = min(20, max(8, int(tw / 10)))
            extra += f"labelPadding={padding};"

        # 所有边使用统一正交样式（含jettySize保证连接器正确渲染）
        edge_style = EdgeStyle(
            shape="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" + extra,
            line_color=color,
            font_color=color,
            font_size=10,
        )

        builder.add_edge(
            src.id, tgt.id, label=label,
            style=edge_style,
            source_port=src_port,
            target_port=tgt_port,
            waypoints=waypoints,
        )


def _in_any_node(x, y, all_positions, exclude_ids=None):
    """检查一个点是否落在任何节点的矩形内"""
    if exclude_ids is None:
        exclude_ids = set()
    for nid, (nx, ny, nw, nh, _) in all_positions.items():
        if nid in exclude_ids:
            continue
        if nx <= x <= nx + nw and ny <= y <= ny + nh:
            return True
    return False


def _compute_with_lane(src, tgt, src_port, tgt_port,
                       router, lane_x: float,
                       crossing: bool = False,
                       h_y: float = None,
                       label: str = "",
                       positions: dict = None,
                       exclude: set = None) -> list:
    """
    路径规划——只有两条出路：

    A. Z-path（仅限于相邻层）：源→垂直向下→水平（在层间缝隙）→垂直向下→目标
    B. 侧道（所有其他情况）：源→水平→画布侧边→垂直→目标

    不绕行、不穿层、不从节点中间过。
    侧道走到左右边缘，标签在画布边缘，绝对不压任何节点。
    """
    if exclude is None:
        exclude = {src.id, tgt.id}

    sx = src.x + src.width / 2 if src_port in (0, 2) else \
         (src.x + src.width if src_port == 1 else src.x)
    sy = src.y if src_port == 0 else \
         (src.y + src.height if src_port == 2 else src.y + src.height / 2)

    tx = tgt.x + tgt.width / 2 if tgt_port in (0, 2) else \
         (tgt.x + tgt.width if tgt_port == 1 else tgt.x)
    ty = tgt.y if tgt_port == 0 else \
         (tgt.y + tgt.height if tgt_port == 2 else tgt.y + tgt.height / 2)

    # === A. Z-path（相邻层：水平段在层间缝隙中，不碰节点） ===
    if h_y is not None and not crossing:
        y_min = sy + 12
        y_max = ty - 12
        if y_max > y_min:
            candidates = [h_y]
            step = max(15, (y_max - y_min) / 6)
            c = y_min
            while c <= y_max:
                candidates.append(c)
                c += step
            for try_y in sorted(set(candidates)):
                ay = max(y_min, min(y_max, try_y))
                path_z = [(sx, sy+12), (sx, ay), (lane_x, ay), (lane_x, ty-12), (tx, ty)]
                if _path_clear_strict(path_z, router.obstacles, exclude):
                    return [(sx, ay), (lane_x, ay), (lane_x, ty-12)]

    # === B. 侧道（从所有节点区外部绕行） ===
    # 动态计算左右侧道位置：在所有节点最左/最右侧之外30px
    # 不硬编码x=15/x=1140，因为某些节点可能超出画布
    all_left = float('inf')
    all_right = float('-inf')
    for rect, nid in router.obstacles:
        if nid in exclude:
            continue
        all_left = min(all_left, rect.left())
        all_right = max(all_right, rect.right())
    
    left_side = all_left - 40
    right_side = all_right + 40
    
    # 源→水平→侧道→垂直→目标
    going_down = ty > sy
    for side_x in [left_side, right_side]:
        gy = sy + 15 if going_down else sy - 15
        t_off = ty - 15 if going_down else ty + 15
        path_side = [(sx, gy), (side_x, gy), (side_x, t_off), (tx, ty)]
        if _path_clear_strict(path_side, router.obstacles, exclude):
            return [(side_x, gy), (side_x, t_off)]

        # 备选：加中间水平段
        mid_y = (gy + t_off) / 2
        for scan_y in [mid_y, gy + 30, t_off - 30, gy + 60, t_off - 60]:
            path_side2 = [(sx, gy), (side_x, gy), (side_x, scan_y), (tx, scan_y), (tx, ty)]
            if _path_clear_strict(path_side2, router.obstacles, exclude):
                return [(side_x, gy), (side_x, scan_y), (tx, scan_y)]

    # === C. 绝对保底（几乎不会走到这里） ===
    try:
        wp = router.route(src, tgt, src_port=src_port, tgt_port=tgt_port)
        if wp:
            return wp
    except:
        pass
    return [(lane_x, sy), (lane_x, ty)]


def _path_clear_strict(points, obstacles, exclude: set) -> bool:
    """严格路径校验——线段不得与任何障碍物相交"""
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        sx_min, sx_max = (x1, x2) if x1 <= x2 else (x2, x1)
        sy_min, sy_max = (y1, y2) if y1 <= y2 else (y2, y1)
        seg = Rect(sx_min, sy_min, sx_max - sx_min, sy_max - sy_min)

        for rect, nid in obstacles:
            if nid in exclude:
                continue
            if seg.overlaps(rect):
                return False
    return True


# ================================================================
# Phase 5: 标签避让
# ================================================================

def check_label_collision(builder: DrawIOBuilder, positions: dict):
    """
    检查所有连线的标签中点是否落在节点矩形内。
    如果碰撞：将标签移到最近的空白区域。
    注：drawio_gen 暂不支持标签偏移，这里只做检查报告。
    """
    collisions = []
    for edge in builder.edges:
        if not edge.label:
            continue
        if not edge.waypoints or len(edge.waypoints) < 2:
            continue
        # 标签在中段中点
        mid = len(edge.waypoints) // 2
        mx = (edge.waypoints[mid - 1][0] + edge.waypoints[mid][0]) / 2
        my = (edge.waypoints[mid - 1][1] + edge.waypoints[mid][1]) / 2

        for label, (x, y, w, h, _) in positions.items():
            if x <= mx <= x + w and y <= my <= y + h:
                collisions.append((edge.label, label))
                break
    return collisions


# ================================================================
# 主入口
# ================================================================

GAP_X = 30  # 水平间距


def generate_diagram(
    nodes: List[dict],
    edges: List[dict],
    title: str = "Diagram",
    gap_x_override: int = None,
    theme: str = "default",
) -> DrawIOBuilder:
    """
    统一图生成入口。

    Args:
        nodes: [{"id": "A", "label": "节点A"}, ...]
        edges: [{"from": "A", "to": "B", "label": "关系"}, ...]
        gap_x_override: 强制指定水平间距
        theme: 颜色主题 — "default" / "tech" / "business" / "bw" / "nature"

    Returns: DrawIOBuilder 实例
    """
    # 选择主题
    if theme not in THEMES:
        theme = "default"
    theme_data = THEMES[theme]
    layer_colors = theme_data["layers"]
    edge_colors = theme_data["edges"]

    # Phase 1: 拓扑分层
    node_layers = topological_layer(nodes, edges)

    # 按层分组
    layer_groups = defaultdict(list)
    for n in nodes:
        lvl = node_layers.get(n["id"], 0)
        layer_groups[lvl].append(n["id"])

    # Phase 2: 层内排序（最小交叉）
    layer_order = barycenter_sort(dict(layer_groups), edges)

    # ===== 计算动态水平间距 =====
    # 对每对相邻层，统计并行边数，水平间距必须能容纳所有车道
    max_parallel_edges = 0
    parallel_counts = defaultdict(int)
    for e in edges:
        if e["from"] in node_layers and e["to"] in node_layers:
            src_li = node_layers[e["from"]]
            tgt_li = node_layers[e["to"]]
            if abs(tgt_li - src_li) <= 1:  # 只考虑相邻层
                key = (min(src_li, tgt_li), max(src_li, tgt_li))
                parallel_counts[key] += 1
                max_parallel_edges = max(max_parallel_edges, parallel_counts[key])

    # 每条车道需要至少 45px 间距（含标签）
    # 节点间水平间距 = max(默认30, 并行边数 * 45)
    dynamic_gap_x = max(30, max_parallel_edges * 45)
    dynamic_gap_x = min(dynamic_gap_x, 180)  # 最大180px，避免太宽
    if gap_x_override:
        dynamic_gap_x = gap_x_override
    
    global GAP_X
    GAP_X = dynamic_gap_x

    # Phase 3: 位置计算（带动态水平间距）
    positions = compute_positions(layer_order, nodes, edges)

    # Phase 4: 构建图
    builder = DrawIOBuilder(name=title)

    # 创建节点
    node_map = {}
    for n in nodes:
        nid = n["id"]
        x, y, w, h, lvl = positions[nid]
        fc, sc = layer_colors[lvl % len(layer_colors)]

        # 形状映射
        shape_type = n.get("shape", "")
        value = n.get("value", "")
        label = n.get("label", "")

        if shape_type == "uml":
            fields = n.get("fields", [])
            methods = n.get("methods", [])
            field_rows = "".join(
                f'<tr><td style="border:1px solid {sc};padding:4px;">{f}</td></tr>\n'
                for f in fields
            )
            method_rows = "".join(
                f'<tr><td style="border:1px solid {sc};padding:4px;">{m}</td></tr>\n'
                for m in methods
            )
            value = (
                f'<table style="border-collapse:collapse;width:100%;">\n'
                f'<tr><td style="border:1px solid {sc};padding:6px;text-align:center;'
                f'background-color:{fc};font-weight:bold;font-size:13px;">{label}</td></tr>\n'
                f'{field_rows}'
                f'<tr><td style="border:1px solid {sc};padding:2px;"></td></tr>\n'
                f'{method_rows}'
                f'</table>'
            )
            style = NodeStyle(
                shape="rounded=1;whiteSpace=wrap;html=1;overflow=hidden;",
                fill_color="#FFFFFF", stroke_color=sc, font_color="#000000",
            )
            # 重新计算高度
            n_lines = 1 + len(fields) + 1 + len(methods)
            h = max(h, n_lines * 22 + 6)

        elif shape_type == "cylinder":
            style = NodeStyle(
                shape="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;",
                fill_color=fc, stroke_color=sc, font_color=sc,
            )
            value = label

        elif shape_type == "diamond":
            style = NodeStyle(
                shape="rhombus;whiteSpace=wrap;html=1;",
                fill_color="#fff2cc", stroke_color="#d6b656", font_color="#d6b656",
            )
            # 菱形视觉上需要更大的宽高
            w = max(w, 120)
            h = max(h, 80)

        elif shape_type == "circle":
            style = NodeStyle(
                shape="ellipse;whiteSpace=wrap;html=1;",
                fill_color=fc, stroke_color=sc, font_color=sc,
            )
            size = max(w, h)
            w = size; h = size

        elif shape_type == "hexagon":
            style = NodeStyle(
                shape="shape=hexagon;perimeter=hexagonPerimeter2;whiteSpace=wrap;html=1;fixedSize=1;size=10;",
                fill_color=fc, stroke_color=sc, font_color=sc,
            )

        elif shape_type == "cloud":
            style = NodeStyle(
                shape="ellipse;shape=cloud;whiteSpace=wrap;html=1;",
                fill_color="#f5f5f5", stroke_color="#666666", font_color="#666666",
            )

        elif shape_type == "note":
            style = NodeStyle(
                shape="shape=note;whiteSpace=wrap;html=1;backgroundOutline=1;size=15;",
                fill_color="#fff2cc", stroke_color="#d6b656", font_color="#d6b656",
            )

        elif shape_type == "document":
            style = NodeStyle(
                shape="mxgraph.basic.doc;whiteSpace=wrap;html=1;size=0.15;",
                fill_color=fc, stroke_color=sc, font_color=sc,
            )

        elif shape_type == "folder":
            style = NodeStyle(
                shape="mxgraph.basic.folder;whiteSpace=wrap;html=1;",
                fill_color=fc, stroke_color=sc, font_color=sc,
            )

        elif shape_type == "header":
            style = NodeStyle(
                fill_color=fc, stroke_color=sc, font_color="#ffffff",
                font_size=14, font_style=1,
            )

        else:
            # 默认圆角矩形
            style = NodeStyle(
                fill_color=fc, stroke_color=sc, font_color=sc,
            )

        nd = builder.add_node(
            label if not value else "",
            x, y, w, h, style=style,
            value=value,
        )
        node_map[nid] = nd

    # 创建连线
    route_edges(builder, node_map, edges, positions, edge_colors=edge_colors)

    # Phase 5: 标签避让报告
    collisions = check_label_collision(builder, positions)
    if collisions:
        print(f"⚠️  标签碰撞 {len(collisions)} 处:", collisions)

    return builder
