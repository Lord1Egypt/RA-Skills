"""
generator_v6.py - draw.io XML 生成器 v6
完整实现分层布局算法 + 显式 waypoints，彻底解决线条重叠

核心原理（参考 diagrams-generator/Mermaid 分层布局）：
1. 最长路径分层：layer(n) = max(layer(parent) + 1)，处理收敛节点
2. 层内定位：同层节点水平排列，主轴居中，分支靠右
3. 显式 waypoints：强制正交路由，不依赖 draw.io 自动计算
"""
import xml.etree.ElementTree as ET
from xml.dom import minidom
import re
from collections import defaultdict, deque

# ============================================================
# 常量
# ============================================================
CANVAS_WIDTH = 850
CANVAS_RIGHT = 760
MAIN_X = CANVAS_WIDTH // 2  # 425
_LAYER_GAP_Y = 120    # 层间垂直间距
_NODE_GAP_X = 40      # 同层节点水平间距
_VERTEX_ID_BASE = 10
_EDGE_ID_BASE = 100

# ============================================================
# 节点尺寸
# ============================================================
NODE_DEFAULTS = {
    'start':    (120, 50),
    'end':      (120, 50),
    'process':  (160, 50),
    'decision': (190, 70),
    'document': (140, 50),
    'data':     (140, 50),
}

def calc_node_size(label, ntype):
    if ntype in NODE_DEFAULTS:
        w, h = NODE_DEFAULTS[ntype]
    else:
        w, h = 160, 50
    chinese = len(re.findall(r'[\u4e00-\u9fff]', label))
    english = len(re.findall(r'[a-zA-Z0-9]', label))
    other = len(label) - chinese - english
    char_px = chinese * 14 + english * 7 + other * 7
    lines = label.split('\n')
    num_lines = max(len(lines), 1)
    w = max(char_px + 32, w)
    w = min(w, 400)
    h = num_lines * 22 + 20
    h = max(h, 50)
    return round(w / 10) * 10, round(h / 10) * 10


# ============================================================
# 第一步：最长路径分层
# ============================================================
def assign_layers(nodes, edges):
    """
    为每个节点分配层号：layer(n) = max(layer(parent) + 1)
    处理汇聚节点（多父节点）时，取最大深度，确保不与祖先重叠。
    """
    # 构建图
    id_map = {str(n['id']): n for n in nodes}
    for n in nodes:
        n['_in'] = []
        n['_out'] = []
    for e in edges:
        src, tgt = str(e['source']), str(e['target'])
        if src in id_map and tgt in id_map:
            id_map[src]['_out'].append(tgt)
            id_map[tgt]['_in'].append(src)

    # 找所有起点（无入边）
    roots = [n for n in nodes if len(n['_in']) == 0]
    if not roots:
        roots = [nodes[0]] if nodes else []

    # BFS 计算最长路径
    layer = {}
    for root in roots:
        rid = str(root['id'])
        layer[rid] = 0
        queue = deque([rid])
        visited = {rid}
        while queue:
            nid = queue.popleft()
            cur_layer = layer[nid]
            for tgt in id_map.get(nid, {}).get('_out', []):
                if tgt not in layer or layer[tgt] < cur_layer + 1:
                    layer[tgt] = cur_layer + 1
                if tgt not in visited:
                    visited.add(tgt)
                    queue.append(tgt)

    # 分配层号（未访问的节点给个默认层）
    for n in nodes:
        nid = str(n['id'])
        n['layer'] = layer.get(nid, 0)

    return nodes


# ============================================================
# 第二步：层内定位
# ============================================================
def assign_positions(nodes, edges):
    """
    每层内节点水平排列。
    规则：
    - 每个判断节点：其 N 分支节点紧邻其右，同层
    - Y 分支节点：在下一层，保持在主轴（Y 分支是主流程继续）
    - 同层多节点：按主轴 ± 偏移排列
    """
    # 建立邻接表
    out_edges = defaultdict(list)
    in_edges = defaultdict(list)
    for e in edges:
        src, tgt = str(e['source']), str(e['target'])
        out_edges[src].append((tgt, str(e.get('label', ''))))
        in_edges[tgt].append((src, str(e.get('label', ''))))

    # 找 N 分支父节点
    n_branch_parent = {}  # child_id -> parent_decision_id
    for e in edges:
        lbl = str(e.get('label', '')).strip()
        if lbl in ('否', 'N', 'n', 'false', 'no'):
            n_branch_parent[str(e['target'])] = str(e['source'])

    # 计算节点尺寸
    for n in nodes:
        w, h = calc_node_size(n.get('label', ''), n.get('type', 'process'))
        n['width'] = w
        n['height'] = h

    # 按层分组
    layers = defaultdict(list)
    for n in nodes:
        layers[n['layer']].append(n)

    # 对每层分配 x 坐标
    for layer_num, layer_nodes in sorted(layers.items()):
        # 分类
        decisions = [n for n in layer_nodes if n.get('type') == 'decision']
        processes = [n for n in layer_nodes if n.get('type') not in ('start', 'decision', 'end')]
        others = [n for n in layer_nodes if n not in decisions and n not in processes]

        # 同层的 N 分支节点：找到其判断父节点，紧靠父节点右侧
        # 先给判断节点分配 x（主轴居中）
        if decisions:
            # 取最左侧判断的 x
            first_x = MAIN_X - decisions[0]['width'] // 2
            for i, d in enumerate(decisions):
                d['x'] = first_x + i * (max(n['width'] for n in decisions) + _NODE_GAP_X)

        # N 分支节点：紧靠其判断父节点右侧
        for n in layer_nodes:
            nid = str(n['id'])
            if nid in n_branch_parent:
                parent_id = n_branch_parent[nid]
                parent = next((x for x in nodes if str(x.get('id')) == parent_id), None)
                if parent:
                    n['x'] = parent['x'] + parent['width'] + _NODE_GAP_X

        # 普通主轴节点：主轴居中
        # 找出该层所有"主轴"节点（不是 N 分支的节点）
        n_branch_children = set(n_branch_parent.keys())
        main_nodes = [n for n in layer_nodes if str(n['id']) not in n_branch_children]

        if main_nodes and not decisions:
            # 无判断时，主轴居中
            total_w = sum(n['width'] for n in main_nodes) + _NODE_GAP_X * (len(main_nodes) - 1)
            start_x = MAIN_X - total_w // 2
            cur_x = start_x
            for n in main_nodes:
                n['x'] = cur_x
                cur_x += n['width'] + _NODE_GAP_X

        # 分配 y = layer_num * _LAYER_GAP_Y + 40
        for n in layer_nodes:
            n['y'] = layer_num * _LAYER_GAP_Y + 40

    return nodes


# ============================================================
# 第三步：计算显式 waypoints
# ============================================================
def compute_waypoints(sx, sy, sw, sh, tx, ty, tw, th, src_type, tgt_type, label, src_layer, tgt_layer, n_branch_of):
    """
    计算边的 waypoints，强制正交路由不重叠。
    策略：
    - Y边（是）或同层向下：底部出 → 垂直 → 目标顶部
    - N边（否）：右侧出 → 水平（绕到决策底部下方）→ 目标左侧
    - 回边（层号减小）：绕到最右侧下行
    """
    lbl = str(label).strip()
    is_n_edge = lbl in ('否', 'N', 'n', 'false', 'no')
    is_y_edge = lbl in ('是', 'Y', 'y', 'true', 'yes')
    is_backward = tgt_layer < src_layer

    waypoints = []

    if is_n_edge:
        # N边：从右侧出 → 水平 → 从左侧入（同层右侧）
        # 必须绕过 src 节点的底部
        mid_y = sy + sh + 30  # 在 src 底部下方走水平线
        waypoints = [
            (sx + sw, sy + sh * 0.5),   # 出口：右侧中间
            (sx + sw + 20, sy + sh * 0.5),  # 向右延伸
            (sx + sw + 20, mid_y),  # 垂直向下
            (tx - 20, mid_y),       # 水平向右到目标左侧
            (tx - 20, ty + th * 0.5),  # 垂直到目标中线
            (tx, ty + th * 0.5),   # 水平到目标左边缘
        ]
    elif is_y_edge or (tgt_layer > src_layer):
        # Y边：从底部出 → 垂直向下 → 从顶部入（下一层）
        waypoints = [
            (sx + sw * 0.5, sy + sh),  # 出口：底部中间
            (sx + sw * 0.5, sy + sh + 20),  # 向下延伸
            (tx + tw * 0.5, sy + sh + 20),  # 水平到目标 x
            (tx + tw * 0.5, ty - 20),   # 垂直向下到目标上方
            (tx + tw * 0.5, ty),        # 垂直到目标顶部
        ]
    elif is_backward:
        # 回边：绕到最右侧下行，再回来
        mid_y = sy + sh + 50
        waypoints = [
            (sx + sw * 0.5, sy + sh),
            (sx + sw * 0.5, mid_y),
            (tx + tw * 0.5, mid_y),
            (tx + tw * 0.5, ty - 20),
            (tx + tw * 0.5, ty),
        ]
    else:
        # 普通向下边
        waypoints = [
            (sx + sw * 0.5, sy + sh),
            (sx + sw * 0.5, sy + sh + 20),
            (tx + tw * 0.5, sy + sh + 20),
            (tx + tw * 0.5, ty - 20),
            (tx + tw * 0.5, ty),
        ]

    # 去重相邻重复点
    cleaned = [waypoints[0]]
    for p in waypoints[1:]:
        if p != cleaned[-1]:
            cleaned.append(p)
    return cleaned


# ============================================================
# 主生成函数
# ============================================================
def generate_drawio_xml(structured: dict) -> str:
    nodes = structured.get('nodes', [])
    edges = structured.get('edges', [])
    title = structured.get('title', 'Diagram')
    chart_type = structured.get('type', 'flowchart')

    # 备份原始 ID
    for n in nodes:
        n['_orig_id'] = str(n['id'])

    # 建立 ID 映射
    vertex_id_map = {}
    for idx, n in enumerate(nodes):
        vertex_id_map[str(n['_orig_id'])] = str(_VERTEX_ID_BASE + idx)

    # 建立邻接表（用于层算法）
    out_edges_map = defaultdict(list)
    in_edges_map = defaultdict(list)
    for e in edges:
        src, tgt = str(e['source']), str(e['target'])
        lbl = str(e.get('label', ''))
        out_edges_map[src].append((tgt, lbl))
        in_edges_map[tgt].append((src, lbl))

    # 第一步：最长路径分层
    nodes = assign_layers(nodes, edges)

    # 第二步：层内定位
    # 先找出 N 分支关系
    n_branch_of = {}
    for e in edges:
        lbl = str(e.get('label', '')).strip()
        if lbl in ('否', 'N', 'n', 'false', 'no'):
            n_branch_of[str(e['target'])] = str(e['source'])

    nodes = assign_positions(nodes, edges)

    # 动态画布高度
    max_layer = max((n.get('layer', 0) for n in nodes), default=0)
    canvas_h = (max_layer + 2) * _LAYER_GAP_Y + 100
    canvas_w = CANVAS_WIDTH

    # 样式
    STYLE = {
        'start':    'ellipse;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#000000;fontSize=12;fontStyle=1;',
        'end':      'ellipse;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#000000;fontSize=12;fontStyle=1;',
        'process':  'rounded=1;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#000000;fontSize=12;',
        'decision': 'rhombus;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#000000;fontSize=12;',
        'document': 'shape=document;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#000000;fontSize=12;',
        'data':     'shape=parallelogram;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#000000;fontSize=12;',
    }
    preset = STYLE

    # 构建 XML
    mxfile = ET.Element('mxfile')
    mxfile.set('host', 'drawio-generator-v6')
    diagram = ET.SubElement(mxfile, 'diagram')
    diagram.set('name', title)
    mxGraphModel = ET.SubElement(diagram, 'mxGraphModel')
    for k, v in [
        ('dx', str(canvas_w + 200)),
        ('dy', str(canvas_h + 200)),
        ('grid', '1'), ('gridSize', '10'), ('guides', '1'),
        ('connect', '1'), ('arrows', '1'), ('fold', '1'),
        ('page', '1'), ('pageScale', '1'),
        ('pageWidth', str(canvas_w)), ('pageHeight', str(canvas_h)),
        ('math', '0'), ('shadow', '0')
    ]:
        mxGraphModel.set(k, v)
    root = ET.SubElement(mxGraphModel, 'root')
    ET.SubElement(root, 'mxCell', {'id': '0'})
    ET.SubElement(root, 'mxCell', {'id': '1', 'parent': '0'})

    # 节点
    for idx, n in enumerate(nodes):
        nid = str(_VERTEX_ID_BASE + idx)
        label = n.get('label', '')
        ntype = n.get('type', 'process')
        x = n.get('x', 0)
        y = n.get('y', 0)
        w = n.get('width', 120)
        h = n.get('height', 50)

        cell = ET.SubElement(root, 'mxCell')
        cell.set('id', nid)
        cell.set('value', label)
        cell.set('style', preset.get(ntype, preset.get('process', '')))
        cell.set('vertex', '1')
        cell.set('parent', '1')
        geo = ET.SubElement(cell, 'mxGeometry')
        geo.set('x', str(x))
        geo.set('y', str(y))
        geo.set('width', str(w))
        geo.set('height', str(h))
        geo.set('as', 'geometry')

    # 边
    for idx, e in enumerate(edges):
        eid = str(_EDGE_ID_BASE + idx)
        src_id = str(e['source'])
        tgt_id = str(e['target'])
        src_vid = vertex_id_map.get(src_id)
        tgt_vid = vertex_id_map.get(tgt_id)
        if not src_vid or not tgt_vid:
            continue

        src_node = next((n for n in nodes if str(n.get('_orig_id')) == src_id), None)
        tgt_node = next((n for n in nodes if str(n.get('_orig_id')) == tgt_id), None)
        if not src_node or not tgt_node:
            continue

        sx = src_node.get('x', 0)
        sy = src_node.get('y', 0)
        sw = src_node.get('width', 100)
        sh = src_node.get('height', 50)
        tx = tgt_node.get('x', 0)
        ty = tgt_node.get('y', 0)
        tw = tgt_node.get('width', 100)
        th = tgt_node.get('height', 50)
        src_layer = src_node.get('layer', 0)
        tgt_layer = tgt_node.get('layer', 0)
        lbl = str(e.get('label', ''))

        waypoints = compute_waypoints(
            sx, sy, sw, sh, tx, ty, tw, th,
            src_node.get('type', 'process'),
            tgt_node.get('type', 'process'),
            lbl, src_layer, tgt_layer, n_branch_of
        )

        cell = ET.SubElement(root, 'mxCell')
        cell.set('id', eid)
        cell.set('value', lbl)
        cell.set('style', 'edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#000000;strokeWidth=1;endArrow=block;endFill=1;startArrow=none;')
        cell.set('edge', '1')
        cell.set('parent', '0')
        cell.set('source', src_vid)
        cell.set('target', tgt_vid)
        geo = ET.SubElement(cell, 'mxGeometry')
        geo.set('relative', '0')
        geo.set('as', 'geometry')

        # 添加 waypoints（去掉首尾，由 source/target 决定）
        if len(waypoints) >= 2:
            pts_el = ET.SubElement(geo, 'Array')
            pts_el.set('as', 'points')
            for wx, wy in waypoints[1:-1]:
                pt = ET.SubElement(pts_el, 'mxPoint')
                pt.set('x', str(int(wx)))
                pt.set('y', str(int(wy)))
                pt.set('as', 'geometry')

    xml_str = ET.tostring(mxfile, encoding='unicode')
    return minidom.parseString(xml_str).toprettyxml(indent='  ')
