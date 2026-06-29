"""
drawio_modules.py — 模块注册 + 各模块实现
"""
import math
from collections import defaultdict, deque
from typing import List, Tuple, Dict

from drawio_module import DiagramModule, LayoutResult, text_width, THEMES
from drawio_gen import DrawIOBuilder, NodeStyle, EdgeStyle
from drawio_route import ObstacleRouter, Rect


# ================================================================
# Module 1: GraphModule — 拓扑图（UML/ER/架构/网络/树形）
# ================================================================

class GraphModule(DiagramModule):
    name = "graph"
    description = "拓扑图：有向图自动分层布局 + 障碍感知路由"
    schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "图标题"},
            "nodes": {
                "type": "array",
                "description": "节点列表",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "label": {"type": "string"},
                        "shape": {"type": "string", "enum": ["uml", "cylinder", "diamond", "hexagon", "circle", "cloud", "note", "document", "folder", "header", ""], "description": "形状（不填=矩形）"},
                        "value": {"type": "string", "description": "HTML内容（覆盖label）"},
                        "fill": {"type": "string", "description": "填充色（如 #dae8fc）"},
                        "stroke": {"type": "string", "description": "边框色"},
                    },
                    "required": ["id", "label"],
                },
            },
            "edges": {
                "type": "array",
                "description": "边列表",
                "items": {
                    "type": "object",
                    "properties": {
                        "from": {"type": "string"},
                        "to": {"type": "string"},
                        "label": {"type": "string"},
                    },
                    "required": ["from", "to"],
                },
            },
        },
        "required": ["nodes", "edges"],
    }

    # ---------- layout ----------
    def _topological_layer(self, nodes, edges):
        graph = defaultdict(set)
        in_degree = defaultdict(int)
        all_ids = set(n["id"] for n in nodes)
        for e in edges:
            if e["from"] in all_ids and e["to"] in all_ids:
                graph[e["from"]].add(e["to"])
                in_degree[e["to"]] += 1
                in_degree.setdefault(e["from"], 0)
        for n in nodes:
            in_degree.setdefault(n["id"], 0)

        queue = deque([nid for nid, deg in in_degree.items() if deg == 0])
        if not queue:
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
                elif temp_in[neighbor] < 0:
                    temp_in[neighbor] = 0

        remaining = all_ids - set(topo_order)
        while remaining:
            nid = remaining.pop()
            topo_order.append(nid)
            for neighbor in list(graph.get(nid, set())):
                if neighbor in remaining:
                    temp_in[neighbor] -= 1
                    if temp_in[neighbor] <= 0:
                        remaining.discard(neighbor)

        layer = {}
        inbound_set = {e["to"] for e in edges if e["from"] in all_ids and e["to"] in all_ids}
        for nid in topo_order:
            deepest_parent = 0
            for e in edges:
                if e["to"] == nid and e["from"] in layer:
                    deepest_parent = max(deepest_parent, layer[e["from"]])
            layer[nid] = deepest_parent + 1 if nid in inbound_set else 0
        return layer

    def _barycenter_sort(self, layer_nodes, edges):
        result = {l: list(ns) for l, ns in layer_nodes.items()}
        for _ in range(10):
            changed = False
            for lvl in sorted(result.keys()):
                ns = result[lvl]
                if len(ns) <= 1:
                    continue
                bary = {}
                for nid in ns:
                    neighbors = []
                    for e in edges:
                        if e["to"] == nid and e["from"] in result.get(lvl - 1, []):
                            neighbors.append(result[lvl - 1].index(e["from"]))
                        elif e["from"] == nid and e["to"] in result.get(lvl + 1, []):
                            neighbors.append(result[lvl + 1].index(e["to"]))
                    bary[nid] = sum(neighbors) / len(neighbors) if neighbors else len(ns)
                sorted_ns = sorted(ns, key=lambda n: bary.get(n, len(ns)))
                if sorted_ns != ns:
                    result[lvl] = sorted_ns
                    changed = True
            if not changed:
                break
        return result

    def _auto_node_size(self, label, font_size=12):
        tw = text_width(label, font_size)
        w = max(90, min(tw + 24, 220))
        h = 50
        if tw > 196:
            lines = math.ceil(len(label) / 14)
            h = max(50, lines * 18 + 14)
        return int(w), int(h)

    def layout(self, data: dict) -> LayoutResult:
        nodes = data.get("nodes", [])
        edges = data.get("edges", [])
        title = data.get("title", "Diagram")

        # Phase 1: 拓扑分层
        node_layers = self._topological_layer(nodes, edges)
        layer_groups = defaultdict(list)
        for n in nodes:
            lvl = node_layers.get(n["id"], 0)
            layer_groups[lvl].append(n["id"])

        # Phase 2: 层内排序
        layer_order = self._barycenter_sort(dict(layer_groups), edges)

        # 动态水平间距
        max_parallel = 0
        pc = defaultdict(int)
        for e in edges:
            if e["from"] in node_layers and e["to"] in node_layers:
                sl, tl = node_layers[e["from"]], node_layers[e["to"]]
                if abs(tl - sl) <= 1:
                    k = (min(sl, tl), max(sl, tl))
                    pc[k] += 1
                    max_parallel = max(max_parallel, pc[k])
        GAP_X = max(30, min(max_parallel * 45, 180))

        # Phase 3: 位置计算
        node_sizes = {}
        for n in nodes:
            w, h = self._auto_node_size(n["label"])
            node_sizes[n["id"]] = (w, h)

        max_edge_label_w = 0
        for e in edges:
            if e.get("label"):
                tw = text_width(e["label"], 10)
                max_edge_label_w = max(max_edge_label_w, tw)
        gap_y = max(100, max_edge_label_w + 80)

        positions = {}
        y = 40
        for lvl in sorted(layer_order.keys()):
            nids = layer_order[lvl]
            if not nids:
                continue
            layer_h = max(node_sizes[nid][1] for nid in nids)
            total_w = sum(node_sizes[nid][0] for nid in nids) + GAP_X * (len(nids) - 1)
            start_x = 40 + (1169 - 80 - total_w) / 2
            x = start_x
            for nid in nids:
                w, h = node_sizes[nid]
                positions[nid] = (x, y, w, max(h, layer_h))
                x += w + GAP_X
            y += layer_h + gap_y

        # 保存层信息用于渲染
        layer_info = {}
        for n in nodes:
            layer_info[n["id"]] = node_layers.get(n["id"], 0)
        self._layer_info = layer_info

        # Phase 4: 路由
        router = ObstacleRouter(pad=1)
        all_nodes_map = {}
        temp_builder = type('tmp', (), {})()
        temp_builder.nodes = []
        for nid, (x, y, w, h) in positions.items():
            nd = type('nd', (), {'id': nid, 'x': x, 'y': y, 'width': w, 'height': h})()
            all_nodes_map[nid] = nd
            temp_builder.nodes.append(nd)
        router.add_obstacles(temp_builder.nodes)

        # 车道分配
        edge_groups = defaultdict(list)
        for e in edges:
            if e["from"] in node_layers and e["to"] in node_layers:
                sl = node_layers[e["from"]]; tl = node_layers[e["to"]]
                edge_groups[(sl, tl)].append(e)

        group_lanes = {}
        for key, group_edges in edge_groups.items():
            sl, tl = key
            n_ed = len(group_edges)
            crossing = abs(tl - sl) > 1
            if crossing:
                max_w = max(text_width(e.get("label", ""), 10) for e in group_edges)
                gap_ = max(50, max_w + 20)
                group_lanes[key] = {
                    "lanes": [15 + i * gap_ for i in range(n_ed)] + [1145 - i * gap_ for i in range(n_ed)],
                    "h_ys": [None] * (n_ed * 2),
                    "idx": 0, "crossing": True,
                }
            else:
                lo, hi = min(sl, tl), max(sl, tl)
                layer_intervals = defaultdict(list)
                for nid, (nx, ny, nw, nh) in positions.items():
                    lvl = layer_info.get(nid, 0)
                    if lo <= lvl <= hi:
                        layer_intervals[lvl].append((nx, nx + nw))
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
                first_lvl = sorted(layer_merged.keys())[0]
                occ = list(layer_merged[first_lvl])
                for lvl in sorted(layer_merged.keys())[1:]:
                    m2 = []
                    for l, r in occ:
                        for ol, or2 in layer_merged[lvl]:
                            ml = max(l, ol); mr = min(r, or2)
                            if ml < mr: m2.append((ml, mr))
                    occ = m2
                    if not occ: break
                gaps = []; prev = 20
                for l, r in occ:
                    if l > prev + 10: gaps.append((prev + l) / 2)
                    prev = max(prev, r)
                if 1149 > prev + 10: gaps.append((prev + 1149) / 2)

                lane_pos = []; lane_y = []
                if gaps:
                    mg = min(gaps); xg = max(gaps)
                    if len(gaps) >= n_ed:
                        for i in range(n_ed):
                            t = (i + 0.5) / n_ed
                            lane_pos.append(mg + t * (xg - mg))
                            lane_y.append(None)  # will be set in route
                    else:
                        for i, g in enumerate(gaps):
                            lane_pos.append(g); lane_y.append(None)
                        for i in range(n_ed - len(gaps)):
                            off = 30 * (i // 2 + 1)
                            lane_pos.append(20 - off if i % 2 == 0 else 1149 + off)
                            lane_y.append(None)
                else:
                    for i in range(n_ed):
                        lane_pos.append(20 if i % 2 == 0 else 1140)
                        lane_y.append(None)
                group_lanes[key] = {"lanes": lane_pos, "h_ys": lane_y, "idx": 0, "crossing": False}

        # 计算每条边的路径
        target_count = defaultdict(int)
        target_idx = defaultdict(int)
        edge_routes = []
        for e in edges:
            target_count[e["to"]] += 1

        for e in edges:
            sl = node_layers.get(e["from"]); tl = node_layers.get(e["to"])
            if sl is None or tl is None:
                continue
            src = all_nodes_map[e["from"]]
            tgt = all_nodes_map[e["to"]]
            label = e.get("label", "")
            crossing = abs(tl - sl) > 1
            key = (sl, tl)
            if key in group_lanes:
                gl = group_lanes[key]
                idx = gl["idx"]; gl["idx"] += 1
                lane_x = gl["lanes"][idx] if idx < len(gl["lanes"]) else gl["lanes"][-1]
                crossing = gl["crossing"]
            else:
                lane_x = (src.x + src.width / 2 + tgt.x + tgt.width / 2) / 2

            if tl > sl:
                sp, tp = 2, 0
            elif tl < sl:
                sp, tp = 0, 2
            elif tgt.x + tgt.width < src.x:
                sp, tp = 3, 1
            elif tgt.x > src.x + src.width:
                sp, tp = 1, 3
            else:
                sp, tp = 2, 0

            # 路径计算：使用预分配的车道lane_x, 走L-path
            # 对相邻层用lane_x（在节点间隙中），对跨层左右散开
            sx = src.x + src.width / 2; sy = src.y + src.height
            tx = tgt.x + tgt.width / 2; ty = tgt.y

            if crossing:
                # 跨层：按edge index交替左右
                all_left = min((r.left() for r, _ in router.obstacles if r is not None), default=20)
                all_right = max((r.right() for r, _ in router.obstacles if r is not None), default=1140)
                side = all_left - 40 if idx % 2 == 0 else all_right + 40
                gy = sy + 15; toff = ty - 15
                waypoints = [(side, gy), (side, toff)]
            else:
                # 相邻层：用lane_x
                gy = sy + 15; toff = ty - 15
                waypoints = [(lane_x, gy), (lane_x, toff)]

            edge_routes.append({
                "from": e["from"], "to": e["to"],
                "label": label, "waypoints": waypoints,
                "src_port": sp, "tgt_port": tp,
            })

        return LayoutResult(
            node_positions=positions,
            edge_routes=edge_routes,
            canvas_w=1169, canvas_h=y + 40,
        )

    def render_node(self, nid, label, x, y, w, h, spec, layer_idx, layer_colors):
        fc, sc = layer_colors[layer_idx % len(layer_colors)]
        shape = spec.get("shape", "")
        value = spec.get("value", "")
        fill = spec.get("fill", fc)
        stroke = spec.get("stroke", sc)

        if shape == "uml":
            fields = spec.get("fields", [])
            methods = spec.get("methods", [])
            fr = "".join(f'<tr><td style="border:1px solid {stroke};padding:4px;">{f}</td></tr>\n' for f in fields)
            mr = "".join(f'<tr><td style="border:1px solid {stroke};padding:4px;">{m}</td></tr>\n' for m in methods)
            value = (
                f'<table style="border-collapse:collapse;width:100%;">\n'
                f'<tr><td style="border:1px solid {stroke};padding:6px;text-align:center;'
                f'background-color:{fill};font-weight:bold;font-size:13px;">{label}</td></tr>\n'
                f'{fr}<tr><td style="border:1px solid {stroke};padding:2px;"></td></tr>\n{mr}</table>'
            )
            h = max(h, (1 + len(fields) + 1 + len(methods)) * 22 + 6)
            return "", NodeStyle(
                shape="rounded=1;whiteSpace=wrap;html=1;overflow=hidden;",
                fill_color="#FFFFFF", stroke_color=stroke, font_color="#000000",
            ), value
        elif shape == "cylinder":
            return label, NodeStyle(
                shape="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;",
                fill_color=fill, stroke_color=stroke, font_color=stroke,
            ), label
        elif shape == "diamond":
            return label, NodeStyle(
                shape="rhombus;whiteSpace=wrap;html=1;",
                fill_color="#fff2cc", stroke_color="#d6b656", font_color="#d6b656",
            ), label
        elif shape == "hexagon":
            return label, NodeStyle(
                shape="shape=hexagon;perimeter=hexagonPerimeter2;whiteSpace=wrap;html=1;fixedSize=1;size=10;",
                fill_color=fill, stroke_color=stroke, font_color=stroke,
            ), label
        elif shape == "circle":
            sz = max(w, h)
            return label, NodeStyle(
                shape="ellipse;whiteSpace=wrap;html=1;",
                fill_color=fill, stroke_color=stroke, font_color=stroke,
            ), label
        elif shape == "cloud":
            return label, NodeStyle(
                shape="ellipse;shape=cloud;whiteSpace=wrap;html=1;",
                fill_color="#f5f5f5", stroke_color="#666666", font_color="#666666",
            ), label
        elif shape == "note":
            return label, NodeStyle(
                shape="shape=note;whiteSpace=wrap;html=1;backgroundOutline=1;size=15;",
                fill_color="#fff2cc", stroke_color="#d6b656", font_color="#d6b656",
            ), label
        elif shape == "document":
            return label, NodeStyle(
                shape="mxgraph.basic.doc;whiteSpace=wrap;html=1;size=0.15;",
                fill_color=fill, stroke_color=stroke, font_color=stroke,
            ), label
        elif shape == "folder":
            return label, NodeStyle(
                shape="mxgraph.basic.folder;whiteSpace=wrap;html=1;",
                fill_color=fill, stroke_color=stroke, font_color=stroke,
            ), label
        elif shape == "header":
            return label, NodeStyle(
                fill_color=fill, stroke_color=stroke, font_color="#ffffff",
                font_size=14, font_style=1,
            ), label
        else:
            return label, NodeStyle(
                fill_color=fill, stroke_color=stroke, font_color=stroke,
            ), label


# ================================================================
# Module 2: GanttModule — 甘特图
# ================================================================

class GanttModule(DiagramModule):
    name = "gantt"
    description = "甘特图：时间轴 + 任务条 + 依赖线"
    schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "tasks": {
                "type": "array",
                "description": "任务列表",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "name": {"type": "string"},
                        "start": {"type": "integer", "description": "开始日期（day序号，0=第1天）"},
                        "end": {"type": "integer", "description": "结束日期（day序号）"},
                    },
                    "required": ["id", "name", "start", "end"],
                },
            },
            "deps": {
                "type": "array",
                "description": "依赖关系",
                "items": {
                    "type": "object",
                    "properties": {
                        "from": {"type": "string"},
                        "to": {"type": "string"},
                    },
                },
            },
        },
        "required": ["tasks"],
    }

    def layout(self, data: dict) -> LayoutResult:
        tasks = data.get("tasks", [])
        deps = data.get("deps", [])
        bar_h = 28
        row_h = 44
        left_margin = 140  # 左侧任务名区域
        day_w = 28         # 每天像素宽度
        header_h = 40      # 时间轴标题高度
        margin_top = 10

        if not tasks:
            return LayoutResult()

        min_day = min(t["start"] for t in tasks)
        max_day = max(t["end"] for t in tasks)
        total_days = max_day - min_day + 1
        canvas_w = left_margin + total_days * day_w + 40

        positions = {}
        y = margin_top + header_h + 10
        task_order = {}
        for i, t in enumerate(tasks):
            x = left_margin + (t["start"] - min_day) * day_w
            w = max(day_w, (t["end"] - t["start"] + 1) * day_w - 2)
            positions[t["id"]] = (x, y, w, bar_h)
            task_order[t["id"]] = i
            y += row_h

        # 依赖线
        edge_routes = []
        for d in deps:
            if d["from"] not in positions or d["to"] not in positions:
                continue
            fx, fy, fw, fh = positions[d["from"]]
            tx, ty, tw, th = positions[d["to"]]
            fr = fy + fh / 2; fc = fx + fw
            tr = ty + th / 2; tc = tx
            # 水平→垂直→水平
            mid_x = (fc + tc) / 2
            edge_routes.append({
                "from": d["from"], "to": d["to"], "label": "",
                "waypoints": [(mid_x, fr), (mid_x, tr)],
                "src_port": None, "tgt_port": None,
            })

        # 额外节点：任务名标签
        for i, t in enumerate(tasks):
            yp = margin_top + header_h + 10 + i * row_h
            positions[t["id"] + "_label"] = (5, yp, left_margin - 10, bar_h)

        return LayoutResult(
            node_positions=positions,
            edge_routes=edge_routes,
            canvas_w=canvas_w, canvas_h=y + 20,
        )

    def render_node(self, nid, label, x, y, w, h, spec, layer_idx, layer_colors):
        is_label = nid.endswith("_label")
        if is_label:
            return spec.get("name", label), NodeStyle(
                fill_color="none", stroke_color="none", font_color="#333333",
                font_size=11, font_style=1,
            ), ""
        fill = spec.get("fill", "#dae8fc")
        stroke = spec.get("stroke", "#6c8ebf")
        return "", NodeStyle(
            fill_color=fill, stroke_color=stroke, font_color=stroke,
        ), spec.get("name", label)

    def build(self, data: dict, theme: str = "default") -> DrawIOBuilder:
        layout = self.layout(data)
        # Override render to add timeline header
        builder = DrawIOBuilder(name=data.get("title", "Gantt Chart"))
        theme_data = THEMES.get(theme, THEMES["default"])
        layer_colors = theme_data["layers"]

        tasks = data.get("tasks", [])
        if not tasks:
            return builder
        min_day = min(t["start"] for t in tasks)
        max_day = max(t["end"] for t in tasks)
        total_days = max_day - min_day + 1
        day_w = 28
        left_margin = 140
        header_h = 40

        # 时间轴标题
        for d in range(total_days):
            day_num = min_day + d
            dx = left_margin + d * day_w + 2
            style = NodeStyle(fill_color="#f5f5f5", stroke_color="#cccccc",
                              font_color="#666666", font_size=9)
            builder.add_node(f"D{day_num}", dx, 10, day_w - 2, header_h - 5, style=style)

        # 任务条
        for t in tasks:
            x, y, w, h = layout.node_positions[t["id"]]
            fill = "#dae8fc"; stroke = "#6c8ebf"
            # 用不同层颜色
            idx = tasks.index(t) % len(layer_colors)
            fc, sc = layer_colors[idx]
            style = NodeStyle(fill_color=fc, stroke_color=sc, font_color=sc)
            builder.add_node(t["name"], x, y, w, h, style=style, node_id=t["id"])

            # 任务名
            lx, ly, lw, lh = layout.node_positions[t["id"] + "_label"]
            lstyle = NodeStyle(fill_color="none", stroke_color="none",
                               font_color="#333333", font_size=11, font_style=1)
            builder.add_node(t["name"], lx, ly, lw, lh, style=lstyle, node_id=t["id"] + "_label")
        else:
            pass

        # 依赖线

        # 依赖线
        edge_colors = theme_data["edges"]
        ci = 0
        for er in layout.edge_routes:
            color = edge_colors[ci % len(edge_colors)]; ci += 1
            estyle = EdgeStyle(
                shape="edgeStyle=orthogonalEdgeStyle;html=1;",
                line_color=color, font_color=color, font_size=9,
            )
            builder.add_edge(er["from"], er["to"], label="",
                             style=estyle, waypoints=er["waypoints"])

        return builder


# ================================================================
# 模块注册
# ================================================================

registry = {
    "graph": GraphModule(),
    "gantt": GanttModule(),
}


def get_module(name: str) -> DiagramModule:
    return registry.get(name)


def list_modules() -> list:
    return [{"name": m.name, "desc": m.description, "schema": m.schema}
            for m in registry.values()]
