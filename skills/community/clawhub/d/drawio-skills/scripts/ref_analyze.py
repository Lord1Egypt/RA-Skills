# -*- coding: utf-8 -*-
"""
ref_analyze.py — 分析一张参考图，产出「参考报告」（风格 + 结构双模板），供 AI 参考生成新图。

与 extract_style.py 的区别：
    extract_style.py  提取「风格」→ 生成 style preset（批量，角色→色槽）
    ref_analyze.py    分析「风格 + 结构」→ 生成参考报告（单图，供 AI 参考画新图）

结构分析新增维度：页面尺寸 / 分组泳道层级 / 节点类型分布 / 边方向 / 布局模式。

用法：
    python ref_analyze.py <参考图.drawio> [-o 报告.md] [--json 报告.json] [--style styles/linlan.json]

    -o      输出 markdown 报告路径（默认 ./ref_report.md）
    --json  额外输出 JSON（供程序消费）
    --style 指定风格 preset 替代单图提取（可选，默认从参考图单图提取）

作者：六百（linlan-skills）
"""
import os
import re
import sys
import json
from collections import Counter
from xml.etree import ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')

# 复用 extract_style 的解码 + 风格提取能力
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extract_style as es

ROLE_CN = {
    'service': '服务', 'database': '数据库', 'queue': '队列', 'gateway': '网关',
    'error': '错误', 'external': '外部', 'security': '安全',
    'decision': '决策', 'container': '容器',
}

SHAPE_CN = {
    'rounded0': '直角矩形', 'rounded1': '圆角矩形', 'cylinder3': '圆柱(数据库)',
    'ellipse': '椭圆(起止)', 'rhombus': '菱形(决策)', 'swimlane': '泳道',
}


def _is_icon(style):
    """判断顶点是否为导入图标（AWS/自定义 stencil/图片），这些内部有子 cell，不能算分组。"""
    return ('mxgraph' in style) or ('aspect=fixed' in style) or \
           ('stencil(' in style) or ('shape=image' in style)


# ---------------------------------------------------------------------------
# 结构分析
# ---------------------------------------------------------------------------
def _center(c):
    g = c.find('mxGeometry')
    if g is None:
        return None
    x = float(g.get('x', 0) or 0)
    y = float(g.get('y', 0) or 0)
    w = float(g.get('width', 0) or 0)
    h = float(g.get('height', 0) or 0)
    return (x + w / 2, y + h / 2)


def analyze_layout(vertices):
    """坐标聚类判断布局方向：纵向分层 / 横向分层 / 网格。"""
    pts = [p for p in (_center(c) for c in vertices) if p]
    if len(pts) < 2:
        return {'direction': 'unknown', 'rows': 0, 'cols': 0, 'node_count': len(pts)}

    THRESH = 60  # 同一行/列的聚类间距阈值(px)
    ys = sorted(set(round(p[1]) for p in pts))
    rows, prev = 1, ys[0]
    for y in ys[1:]:
        if y - prev > THRESH:
            rows += 1
        prev = y
    xs = sorted(set(round(p[0]) for p in pts))
    cols, prev = 1, xs[0]
    for x in xs[1:]:
        if x - prev > THRESH:
            cols += 1
        prev = x

    if rows > cols * 1.5:
        direction = 'vertical'
    elif cols > rows * 1.5:
        direction = 'horizontal'
    else:
        direction = 'grid'
    return {'direction': direction, 'rows': rows, 'cols': cols, 'node_count': len(pts)}


def analyze_structure(model):
    """分析单个 mxGraphModel：页面 / 分组泳道 / 节点类型 / 边 / 布局。"""
    page = {
        'width': model.get('dx', ''),
        'height': model.get('dy', ''),
        'grid': model.get('grid', ''),
        'gridSize': model.get('gridSize', ''),
    }

    cells = list(model.iter('mxCell'))
    vertices = [c for c in cells if c.get('vertex') == '1']
    edges = [c for c in cells if c.get('edge') == '1']

    containers = []
    nodes = []
    for c in vertices:
        style = c.get('style', '')
        kv, bare = es.parse_style(style)
        is_swimlane = 'swimlane' in bare or 'swimlane' in kv.get('shape', '')
        has_children = any(x.get('parent') == c.get('id') for x in cells)
        # 分组 = 有子节点且非图标/泳道（图标内部子 cell 是图形组成，非语义分组）
        is_group = has_children and not is_swimlane and not _is_icon(style)
        label = (c.get('value') or '').strip()
        # 分组名空时，从直属子节点推断（drawio 常用独立 text 子节点承载分组名，value 可能是 HTML）
        if not label and is_group:
            for x in cells:
                if x.get('parent') == c.get('id'):
                    v = (x.get('value') or '').strip()
                    if not v:
                        continue
                    text = re.sub(r'<[^>]+>', '', v).strip()
                    if text and len(text) <= 40:
                        label = text
                        break
        if is_swimlane or is_group:
            containers.append({
                'label': label,
                'type': 'swimlane' if is_swimlane else 'group',
            })
        else:
            nodes.append(c)

    role_dist = Counter()
    shape_dist = Counter()
    for c in nodes:
        style = c.get('style', '')
        sc = es.shape_class(style)
        role_dist[es.infer_role(sc, c.get('value', ''), style)] += 1
        shape_dist[sc] += 1

    ortho = dashed = arrowed = 0
    for e in edges:
        kv, _ = es.parse_style(e.get('style', ''))
        if 'orthogonal' in kv.get('edgeStyle', ''):
            ortho += 1
        if kv.get('dashed') == '1':
            dashed += 1
        if kv.get('endArrow') and kv.get('endArrow') != 'none':
            arrowed += 1

    return {
        'page': page,
        'containers': containers,
        'role_dist': dict(role_dist.most_common()),
        'shape_dist': dict(shape_dist.most_common()),
        'edges': {'total': len(edges), 'orthogonal': ortho, 'dashed': dashed, 'arrowed': arrowed},
        'layout': analyze_layout(nodes),
    }


# ---------------------------------------------------------------------------
# 报告渲染
# ---------------------------------------------------------------------------
def render_markdown(filename, style, structure):
    """把风格 preset + 结构 dict 渲染成 AI 友好的 markdown 报告。"""
    L = []
    L.append(f'# 参考图报告：{filename}')
    L.append('')

    # --- 风格 ---
    L.append('## 一、风格（套用此配色 / 字体 / 形状）')
    L.append('')
    f = style.get('font', {})
    font_str = f.get('fontFamily', 'Helvetica')
    size_str = str(f.get('fontSize', 12))
    if f.get('titleFontSize'):
        bold = '加粗' if f.get('titleBold') else ''
        size_str += f'（标题 {f["titleFontSize"]}{bold}）'
    L.append(f'- **字体**：`{font_str}`，字号 `{size_str}`')
    L.append(f'- **笔宽**：`{style.get("extras", {}).get("globalStrokeWidth", 1)}`')
    L.append('')
    L.append('| 角色 | 填充 | 描边 |')
    L.append('|------|------|------|')
    for slot, pair in style.get('palette', {}).items():
        if not pair:
            continue
        slot_cn = {'primary': '服务', 'success': '数据库', 'warning': '队列',
                   'accent': '网关', 'danger': '错误', 'neutral': '外部',
                   'secondary': '安全'}.get(slot, slot)
        L.append(f'| {slot_cn} | `{pair["fillColor"]}` | `{pair["strokeColor"]}` |')
    L.append('')
    shapes = style.get('shapes', {})
    if shapes:
        L.append('- **形状**：' + '，'.join(
            f'{k}→`{v}`' for k, v in shapes.items()))
    L.append('')

    # --- 结构 ---
    L.append('## 二、结构（复用此骨架）')
    L.append('')
    pg = structure['page']
    L.append(f'- **页面**：{pg["width"]}×{pg["height"]}（grid={pg["grid"]}，gridSize={pg["gridSize"]}）')

    cons = structure['containers']
    if cons:
        L.append(f'- **分组/泳道**：{len(cons)} 个')
        for i, c in enumerate(cons, 1):
            cn = '泳道' if c['type'] == 'swimlane' else '分组'
            lbl = c['label'] or f'(未命名)'
            L.append(f'  {i}. [{cn}] {lbl}')
    else:
        L.append('- **分组/泳道**：无（扁平结构）')

    rd = structure['role_dist']
    L.append('- **节点类型**：' + '、'.join(
        f'{ROLE_CN.get(k, k)}×{v}' for k, v in rd.items()))
    sd = structure['shape_dist']
    L.append('- **形状类型**：' + '、'.join(
        f'{SHAPE_CN.get(k, k)}×{v}' for k, v in sd.items()))

    eg = structure['edges']
    L.append(f'- **边**：{eg["total"]} 条（正交 {eg["orthogonal"]}，虚线 {eg["dashed"]}，带箭头 {eg["arrowed"]}）')

    ly = structure['layout']
    dir_cn = {'vertical': '纵向分层', 'horizontal': '横向分层', 'grid': '网格/混合',
              'unknown': '未知'}.get(ly['direction'], ly['direction'])
    L.append(f'- **布局**：{dir_cn}（约 {ly["rows"]} 行 × {ly["cols"]} 列，{ly["node_count"]} 节点）')
    L.append('')

    # --- 生成建议 ---
    L.append('## 三、生成建议（给 AI 的提示）')
    L.append('')
    L.append('- 复用上述配色 / 字体 / 形状 / 边样式，保持视觉一致')
    if cons:
        L.append(f'- 沿用 {len(cons)} 层分组泳道骨架，层级命名按新需求替换')
    L.append(f'- 布局沿用「{dir_cn}」模式，节点数量按新需求增减')
    L.append('- 新图节点若超出参考图类型，就近复用同色槽配色')
    L.append('')
    return '\n'.join(L)


# ---------------------------------------------------------------------------
# 主入口
# ---------------------------------------------------------------------------
def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)

    target = args[0]
    if not os.path.isfile(target):
        print('参考图文件不存在:', target)
        sys.exit(1)

    out = None
    json_out = None
    style_path = None
    self_extract = False
    i = 1
    while i < len(args):
        if args[i] == '-o' and i + 1 < len(args):
            out = args[i + 1]; i += 2
        elif args[i] == '--json' and i + 1 < len(args):
            json_out = args[i + 1]; i += 2
        elif args[i] == '--style' and i + 1 < len(args):
            style_path = args[i + 1]; i += 2
        elif args[i] == '--self':
            self_extract = True; i += 1
        else:
            i += 1

    filename = os.path.basename(target)

    # 结构分析（复用解码）
    models = es.load_models(target)
    if not models:
        print('无法解析:', target)
        sys.exit(1)
    structure = analyze_structure(models[0])

    # 风格：默认用人工复核的 linlan preset（单图重提取会失真）；--style 指定；--self 单图提取
    if self_extract:
        style, summary = es.extract([target])
        if style is None:
            print('风格提取失败:', summary)
            sys.exit(1)
    elif style_path and os.path.isfile(style_path):
        with open(style_path, 'r', encoding='utf-8') as fp:
            style = json.load(fp)
    else:
        default = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'styles', 'linlan.json')
        if os.path.isfile(default):
            with open(default, 'r', encoding='utf-8') as fp:
                style = json.load(fp)
        else:
            style, summary = es.extract([target])
            if style is None:
                print('风格提取失败:', summary)
                sys.exit(1)

    # 渲染 markdown
    md = render_markdown(filename, style, structure)

    # 输出
    if not out:
        out = os.path.join(os.getcwd(), 'ref_report.md')
    out = os.path.abspath(out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w', encoding='utf-8') as fp:
        fp.write(md)

    if json_out:
        json_out = os.path.abspath(json_out)
        os.makedirs(os.path.dirname(json_out), exist_ok=True)
        payload = {
            'file': filename,
            'style': {k: style.get(k) for k in ('palette', 'roles', 'shapes', 'font', 'edges', 'extras')},
            'structure': structure,
        }
        with open(json_out, 'w', encoding='utf-8') as fp:
            json.dump(payload, fp, ensure_ascii=False, indent=2)

    print(md)
    print('=' * 70)
    print(f'已保存 markdown: {out}')
    if json_out:
        print(f'已保存 json: {json_out}')


if __name__ == '__main__':
    main()
