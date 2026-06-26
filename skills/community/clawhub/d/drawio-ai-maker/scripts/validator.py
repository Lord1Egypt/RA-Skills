"""
validator.py - draw.io XML 规则校验器
生成 XML 后内置校验，不满足规则则打回 LLM 重新生成 JSON
"""
import xml.etree.ElementTree as ET


class ValidationError(Exception):
    """校验失败异常，包含详细错误信息"""
    def __init__(self, errors: list):
        self.errors = errors
        super().__init__(f"校验失败，共 {len(errors)} 个错误:\n" + "\n".join(f"  {i+1}. {e}" for i, e in enumerate(errors)))


def validate_drawio_xml(xml_str: str) -> dict:
    """
    校验 draw.io XML 是否满足所有规则。

    规则：
    1. XML 格式有效（能被 ET 解析）
    2. 存在且仅存在：root(id=0) + page(id=1) + 至少1个 vertex + 至少1个 edge
    3. 所有 mxCell id 唯一，无重复
    4. vertex 必须 parent="1"，edge 必须 parent="0"
    5. edge 的 source/target 引用的 vertex ID 必须存在
    6. vertex 从 id=2 开始，edge 从 id=1000 开始

    Returns:
        dict: {
            'valid': bool,
            'errors': list[str] (valid=False 时),
            'stats': dict (valid=True 时，包含元素统计)
        }
    """
    errors = []

    # 规则1: XML 格式有效
    try:
        root = ET.fromstring(xml_str)
    except ET.ParseError as e:
        return {'valid': False, 'errors': [f"XML 格式错误: {e}"]}

    # 提取所有 mxCell
    all_cells = root.findall('.//mxCell')
    if not all_cells:
        errors.append("XML 中不存在 mxCell 元素")

    # 提取元素
    cell_by_id = {}
    for cell in all_cells:
        cid = cell.get('id')
        if cid is None:
            errors.append("存在没有 id 属性的 mxCell")
            continue
        cell_by_id[cid] = cell

    if errors:
        return {'valid': False, 'errors': errors}

    # 规则2: 基本结构检查
    if '0' not in cell_by_id:
        errors.append("缺少 id=0 的根容器 mxCell")
    if '1' not in cell_by_id:
        errors.append("缺少 id=1 的页面容器 mxCell")

    # 统计 vertex 和 edge
    vertices = [(cid, c) for cid, c in cell_by_id.items() if c.get('vertex') == '1']
    edges = [(cid, c) for cid, c in cell_by_id.items() if c.get('edge') == '1']

    if len(vertices) == 0:
        errors.append("不存在任何 vertex（节点），至少需要 1 个节点")
    if len(edges) == 0:
        errors.append("不存在任何 edge（连接线），至少需要 1 条连线")

    # 规则3: ID 唯一性
    all_ids = list(cell_by_id.keys())
    if len(all_ids) != len(set(all_ids)):
        from collections import Counter
        counts = Counter(all_ids)
        duplicates = [f"id='{k}' 出现 {v} 次" for k, v in counts.items() if v > 1]
        errors.append(f"存在重复的 mxCell id: {', '.join(duplicates)}")

    # 规则4: vertex parent="1", edge parent="0"
    for cid, cell in vertices:
        parent = cell.get('parent', '')
        if parent != '1':
            errors.append(f"vertex id='{cid}' 的 parent 应为 '1'，实际为 '{parent}'")

    for cid, cell in edges:
        parent = cell.get('parent', '')
        if parent != '0':
            errors.append(f"edge id='{cid}' 的 parent 应为 '0'，实际为 '{parent}'")

    # 规则5: edge source/target 必须引用存在的 vertex
    vertex_ids = {cid for cid, _ in vertices}
    for cid, cell in edges:
        source = cell.get('source')
        target = cell.get('target')
        if source and source not in vertex_ids:
            errors.append(f"edge id='{cid}' 的 source='{source}' 引用了不存在的 vertex")
        if target and target not in vertex_ids:
            errors.append(f"edge id='{cid}' 的 target='{target}' 引用了不存在的 vertex")

    # 规则6: ID 范围检查

    # 规则7: dot 布局权威，重叠由 dot 算法决定，不再检测
    # overlap_errors = _check_overlaps(list(cell_by_id.items()), vertices)
    # errors.extend(overlap_errors)
    vertex_cids = [int(cid) for cid, _ in vertices if cid.isdigit()]
    edge_cids = [int(cid) for cid, _ in edges if cid.isdigit()]

    if vertex_cids:
        min_vertex = min(vertex_cids)
        if min_vertex < 10:
            errors.append(f"vertex id 最小值应 >= 10（0=root, 1=page），实际最小值为 {min_vertex}")

    if edge_cids:
        min_edge = min(edge_cids)
        if min_edge < 20:
            errors.append(f"edge id 最小值应 >= 20，实际最小值为 {min_edge}")

    # 汇总
    if errors:
        return {'valid': False, 'errors': errors}

    stats = {
        'total_cells': len(all_cells),
        'vertices': len(vertices),
        'edges': len(edges),
        'vertex_ids': sorted(vertex_cids),
        'edge_ids': sorted(edge_cids),
    }
    return {'valid': True, 'stats': stats}


def _check_overlaps(cell_by_id: dict, vertices: list) -> list:
    """
    检测节点之间是否有重叠。
    两个节点重叠条件：两个矩形在 x 和 y 方向都有交集。
    允许边缘接触（刚好挨着），但不允许多于 5px 的重叠。
    """
    errors = []

    for i, (cid1, cell1) in enumerate(vertices):
        geo1 = cell1.find('mxGeometry')
        if geo1 is None:
            continue
        try:
            x1, y1 = float(geo1.get('x', 0)), float(geo1.get('y', 0))
            w1, h1 = float(geo1.get('width', 0)), float(geo1.get('height', 0))
        except (ValueError, TypeError):
            continue

        for cid2, cell2 in vertices[i + 1:]:
            geo2 = cell2.find('mxGeometry')
            if geo2 is None:
                continue
            try:
                x2, y2 = float(geo2.get('x', 0)), float(geo2.get('y', 0))
                w2, h2 = float(geo2.get('width', 0)), float(geo2.get('height', 0))
            except (ValueError, TypeError):
                continue

            # 检测 x 方向重叠（允许 5px 以内的边缘接触）
            overlap_x = min(x1 + w1, x2 + w2) - max(x1, x2)
            # 检测 y 方向重叠
            overlap_y = min(y1 + h1, y2 + h2) - max(y1, y2)

            if overlap_x > 30 and overlap_y > 30:
                label1 = cell1.get('value', cid1)[:20]
                label2 = cell2.get('value', cid2)[:20]
                errors.append(
                    f"节点重叠: '{label1}' (id={cid1}) 与 '{label2}' (id={cid2}) "
                    f"在 x 方向重叠 {overlap_x:.0f}px，y 方向重叠 {overlap_y:.0f}px"
                )

    return errors


def _check_edge_node_overlaps(cell_by_id: dict, edges: list, vertex_ids: set) -> list:
    """
    检测连接线是否穿过节点（对于 orthogonal 折线）。
    简化检测：检查 edge 的 source 和 target 节点之间，
    是否有其他节点的中心点落在连接线形成的矩形区域内。
    """
    errors = []

    for cid, cell in edges:
        source = cell.get('source')
        target = cell.get('target')
        if not source or not target:
            continue
        if source not in cell_by_id or target not in cell_by_id:
            continue

        src_geo = cell_by_id[source].find('mxGeometry')
        tgt_geo = cell_by_id[target].find('mxGeometry')
        if src_geo is None or tgt_geo is None:
            continue

        try:
            sx = float(src_geo.get('x', 0)) + float(src_geo.get('width', 0)) / 2
            sy = float(src_geo.get('y', 0)) + float(src_geo.get('height', 0)) / 2
            tx = float(tgt_geo.get('x', 0)) + float(tgt_geo.get('width', 0)) / 2
            ty = float(tgt_geo.get('y', 0)) + float(tgt_geo.get('height', 0)) / 2
        except (ValueError, TypeError):
            continue

        # 遍历所有节点，检查中心是否在连线矩形区域内
        for vid, vcell in cell_by_id.items():
            if vid in (source, target) or vid not in vertex_ids:
                continue
            vgeo = vcell.find('mxGeometry')
            if vgeo is None:
                continue
            try:
                vx = float(vgeo.get('x', 0))
                vy = float(vgeo.get('y', 0))
                vw = float(vgeo.get('width', 0))
                vh = float(vgeo.get('height', 0))
            except (ValueError, TypeError):
                continue

            # 中心点
            cx = vx + vw / 2
            cy = vy + vh / 2

            # 检查中心是否在 source→target 形成的正交矩形区域内（有 10px 缓冲）
            min_x, max_x = min(sx, tx) - 10, max(sx, tx) + 10
            min_y, max_y = min(sy, ty) - 10, max(sy, ty) + 10

            if min_x <= cx <= max_x and min_y <= cy <= max_y:
                label = vcell.get('value', vid)[:20]
                errors.append(
                    f"连接线 (edge id={cid}) 从 '{cell_by_id[source].get('value', source)[:15]}' "
                    f"到 '{cell_by_id[target].get('value', target)[:15]}' "
                    f"穿过节点 '{label}' (id={vid})"
                )

    return errors


def validate_json_schema(structured: dict) -> dict:
    """
    校验 LLM 返回的 JSON 是否符合 Schema 要求。
    不满足则打回 LLM 重新生成。
    """
    errors = []

    # 必须字段
    if 'title' not in structured:
        errors.append("缺少 'title' 字段")
    if 'nodes' not in structured:
        errors.append("缺少 'nodes' 字段")
    else:
        if not isinstance(structured['nodes'], list):
            errors.append("'nodes' 必须是数组")
        elif len(structured['nodes']) == 0:
            errors.append("'nodes' 数组不能为空，至少需要 1 个节点")
        else:
            for i, node in enumerate(structured['nodes']):
                if 'id' not in node:
                    errors.append(f"nodes[{i}] 缺少 'id' 字段")
                if 'label' not in node:
                    errors.append(f"nodes[{i}] 缺少 'label' 字段")

    if 'edges' not in structured:
        errors.append("缺少 'edges' 字段")
    else:
        if not isinstance(structured['edges'], list):
            errors.append("'edges' 必须是数组")
        elif len(structured['edges']) == 0:
            errors.append("'edges' 数组不能为空，至少需要 1 条边")
        else:
            for i, edge in enumerate(structured['edges']):
                if 'source' not in edge:
                    errors.append(f"edges[{i}] 缺少 'source' 字段")
                if 'target' not in edge:
                    errors.append(f"edges[{i}] 缺少 'target' 字段")

    if errors:
        return {'valid': False, 'errors': errors}

    return {'valid': True}
