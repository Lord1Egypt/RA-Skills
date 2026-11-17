# -*- coding: utf-8 -*-
"""
extract_style.py — 从 .drawio 源文件提取个人绘制风格，生成 style preset JSON。

确定性算法（无 LLM 推断），参照 Agents365-ai/drawio-skill 的 XML 提取路径，
并针对中文标签做了本地化微调（角色词表补充中文关键词）。

用法：
    python extract_style.py <目录或单个.drawio> [--name <preset名>] [--out <输出.json>]

输出：
    - 符合 drawio-skill styles/schema.json 的 preset JSON（palette/roles/shapes/font/edges/extras）
    - 控制台打印提取摘要（含"留白+黑描边"等签名特征的统计，供人工复核）

作者：六百（linlan-skills）
"""
import os
import re
import sys
import json
import base64
import zlib
import urllib.parse
from collections import Counter
from xml.etree import ElementTree as ET
from datetime import date

sys.stdout.reconfigure(encoding='utf-8')

# ---------------------------------------------------------------------------
# 1. 压缩 drawio 解码
# ---------------------------------------------------------------------------
def decode_diagram(text):
    """解码 drawio 压缩的 diagram 内容，返回 mxGraphModel 的 XML 字符串。
    链路：URL解码 -> base64解码 -> raw deflate -> URL解码 -> XML"""
    if not text or not text.strip():
        return text
    s = urllib.parse.unquote(text.strip())
    pad = 4 - len(s) % 4
    if pad != 4:
        s += '=' * pad
    data = base64.b64decode(s)
    inflated = zlib.decompress(data, -15).decode('utf-8')
    return urllib.parse.unquote(inflated)


def load_models(filepath):
    """读取一个 .drawio 文件，返回所有 mxGraphModel 根元素列表（已解压）。"""
    raw = open(filepath, 'rb').read()
    root = ET.fromstring(raw)
    models = []
    for d in root.iter('diagram'):
        xml = decode_diagram(d.text)
        if xml and xml.strip():
            try:
                models.append(ET.fromstring(xml))
            except Exception:
                try:
                    models.append(ET.fromstring(d.text or ''))
                except Exception:
                    pass
    if not models:
        models = [root]
    return models


# ---------------------------------------------------------------------------
# 2. style 字符串解析
# ---------------------------------------------------------------------------
def parse_style(style):
    """把 style 字符串拆成 dict（key=value）与 bare 关键字集合。"""
    kv = {}
    bare = set()
    if not style:
        return kv, bare
    for part in style.split(';'):
        part = part.strip()
        if not part:
            continue
        if '=' in part:
            k, _, v = part.partition('=')
            kv[k.strip()] = v.strip()
        else:
            bare.add(part)
    return kv, bare


def shape_class(style):
    """按优先级判定形状类别：cylinder3 > ellipse > rhombus > swimlane > rounded=1 > rounded=0"""
    kv, bare = parse_style(style)
    shape_val = kv.get('shape', '')
    if 'cylinder' in shape_val or 'cylinder' in bare:
        return 'cylinder3'
    if 'ellipse' in bare or shape_val == 'ellipse':
        return 'ellipse'
    if 'rhombus' in bare or shape_val == 'rhombus':
        return 'rhombus'
    if 'swimlane' in bare or 'swimlane' in shape_val:
        return 'swimlane'
    if kv.get('rounded') == '1':
        return 'rounded1'
    return 'rounded0'


# 角色词表（英文原版 + 中文本地化补充）
ROLE_RE = [
    ('queue',    re.compile(r'queue|bus|kafka|rabbit|mq|队列|消息|订阅|消费|任务', re.I)),
    ('gateway',  re.compile(r'gateway|api\b|lb|load|网关|负载|反向代理|路由|入口', re.I)),
    ('security', re.compile(r'auth|login|jwt|oauth|token|认证|登录|鉴权|授权|权限|密码', re.I)),
    ('error',    re.compile(r'error|fail|alert|错误|失败|告警|异常|故障|超时', re.I)),
    ('database', re.compile(r'db|database|mysql|redis|mongo|存储|数据|缓存|库', re.I)),
]


def is_grey(hex_color):
    """判断颜色是否为近灰色（RGB 三通道偏差 <=16）。"""
    if not hex_color or len(hex_color) < 7 or hex_color.lower() in ('none', 'default'):
        return False
    h = hex_color.lstrip('#')
    if len(h) != 6:
        return False
    try:
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    except ValueError:
        return False
    return max(r, g, b) - min(r, g, b) <= 16


def infer_role(shape_cls, label, style):
    """按优先级推断语义角色（先形状类，再 dashed+灰底=external，再标签词表，最后 service）。"""
    if shape_cls == 'cylinder3':
        return 'database'
    if shape_cls == 'rhombus':
        return 'decision'
    if shape_cls == 'swimlane':
        return 'container'
    # dashed + 灰底 -> external
    if 'dashed=1' in style:
        kv, _ = parse_style(style)
        if is_grey(kv.get('fillColor', '')):
            return 'external'
    for role, rx in ROLE_RE:
        if rx.search(label or ''):
            return role
    return 'service'


# 角色 -> 规范色槽 映射
ROLE_SLOT = {
    'service': 'primary',
    'database': 'success',
    'queue': 'warning',
    'gateway': 'accent',
    'error': 'danger',
    'external': 'neutral',
    'security': 'secondary',
}

# 形状词表输出键
SHAPE_KEY = {
    'service': 'service',
    'database': 'database',
    'queue': 'queue',
    'decision': 'decision',
    'external': 'external',
    'container': 'container',
}


def shape_string(shape_cls):
    """形状类别 -> drawio style 字符串。"""
    return {
        'cylinder3': 'shape=cylinder3',
        'ellipse': 'ellipse',
        'rhombus': 'rhombus',
        'swimlane': 'swimlane;startSize=30',
        'rounded1': 'rounded=1',
        'rounded0': 'rounded=0',
    }.get(shape_cls, 'rounded=0')


# ---------------------------------------------------------------------------
# 3. 提取
# ---------------------------------------------------------------------------
def extract(paths):
    vertices = []   # dict: {fill, stroke, style, label, shape_cls, role, font, size, fontstyle, strokeWidth}
    edges = []

    for fp in paths:
        for model in load_models(fp):
            for cell in model.iter('mxCell'):
                style = cell.get('style', '')
                if not style:
                    continue
                if cell.get('vertex') == '1':
                    kv, _ = parse_style(style)
                    fill = kv.get('fillColor', '')
                    stroke = kv.get('strokeColor', '')
                    sc = shape_class(style)
                    vertices.append({
                        'fill': fill,
                        'stroke': stroke,
                        'style': style,
                        'label': cell.get('value', ''),
                        'shape_cls': sc,
                        'role': infer_role(sc, cell.get('value', ''), style),
                        'font': kv.get('fontFamily', ''),
                        'size': kv.get('fontSize', ''),
                        'fontstyle': kv.get('fontStyle', ''),
                        'strokeWidth': kv.get('strokeWidth', ''),
                        'rounded': kv.get('rounded', ''),
                    })
                elif cell.get('edge') == '1':
                    edges.append({
                        'style': style,
                        'label': cell.get('value', ''),
                    })

    if not vertices:
        return None, {'error': 'no vertices'}

    # ---- 3a. 调色板：统计 (fill,stroke) 对（跳过 fill=none 的留白描边样式）----
    pair_counter = Counter()
    none_fill_counter = Counter()  # 留白 + 描边色的签名统计
    solid_pairs = []               # 有效 (fill,stroke) 对（fill 为 #RRGGBB）
    for v in vertices:
        fill = v['fill']
        stroke = v['stroke']
        if not fill or fill.lower() in ('none', 'default', ''):
            none_fill_counter[stroke] += 1
            continue
        if not re.fullmatch(r'#[0-9A-Fa-f]{6}', fill or ''):
            continue
        pair_counter[(fill.upper(), (stroke or '').upper())] += 1

    palette = {}
    top_pairs = pair_counter.most_common(7)

    # ---- 3b. 形状词表 + 角色->色槽映射 ----
    # 每种角色的 (role, color-pair) 频次，用于把最常用颜色对绑到该角色的规范色槽
    role_pair_counter = {}
    for v in vertices:
        fill = v['fill']
        if not re.fullmatch(r'#[0-9A-Fa-f]{6}', fill or ''):
            continue
        role = v['role']
        pair = (fill.upper(), (v['stroke'] or '').upper())
        role_pair_counter.setdefault(role, Counter())[pair] += 1

    roles = {}
    slot_taken = {}   # slot -> pair
    for role, slot in ROLE_SLOT.items():
        c = role_pair_counter.get(role)
        if not c:
            continue
        # 取该角色最常用的、且尚未被占用的颜色对
        for pair, _ in c.most_common():
            if slot not in slot_taken:
                slot_taken[slot] = pair
                roles[role] = slot
                break

    # 决策/容器形状词表
    shapes = {}
    for v in vertices:
        cls = v['shape_cls']
        if cls in ('rhombus', 'swimlane') and 'decision' not in shapes and cls == 'rhombus':
            shapes['decision'] = 'rhombus'
        if cls == 'swimlane' and 'container' not in shapes:
            shapes['container'] = 'swimlane;startSize=30'
    # service 形状 = 最常用形状类（除 rhombus/swimlane 外）
    svc_classes = Counter(v['shape_cls'] for v in vertices
                          if v['shape_cls'] not in ('rhombus', 'swimlane', 'cylinder3', 'ellipse'))
    if svc_classes:
        shapes['service'] = shape_string(svc_classes.most_common(1)[0][0])
    else:
        shapes['service'] = 'rounded=0'
    # database / queue / external 形状
    db_cls = Counter(v['shape_cls'] for v in vertices if v['shape_cls'] == 'cylinder3')
    shapes['database'] = 'shape=cylinder3' if db_cls else 'shape=cylinder3'
    shapes['queue'] = shapes['service']
    shapes['external'] = shapes['service'] + ';dashed=1'

    # ---- 3c. 填充调色板 7 色槽 ----
    # 先用角色绑定的颜色对填对应槽，剩余颜色对按频次填空槽
    slot_order = ['primary', 'success', 'warning', 'accent', 'danger', 'neutral', 'secondary']
    def pair_obj(pair):
        if not pair:
            return None
        f, s = pair
        return {'fillColor': f, 'strokeColor': (s if s else '#666666')}

    for slot in slot_order:
        if slot in slot_taken:
            palette[slot] = pair_obj(slot_taken[slot])
        else:
            palette[slot] = None

    # 剩余颜色对填空槽
    used_pairs = set(slot_taken.values())
    idx = 0
    for pair, _ in top_pairs:
        if pair in used_pairs:
            continue
        # 找第一个空槽
        while idx < len(slot_order) and palette[slot_order[idx]] is not None:
            idx += 1
        if idx >= len(slot_order):
            break
        palette[slot_order[idx]] = pair_obj(pair)
        used_pairs.add(pair)
        idx += 1

    # ---- 3d. 字体 ----
    font_counter = Counter(v['font'] for v in vertices if v['font'])
    size_counter = Counter(v['size'] for v in vertices if v['size'])
    font_family = font_counter.most_common(1)[0][0] if font_counter else 'Helvetica'
    try:
        font_size = int(size_counter.most_common(1)[0][0]) if size_counter else 12
    except (ValueError, TypeError):
        font_size = 12

    # 标题检测：加粗(fontStyle=1) 且字号更大的子集
    bold_sizes = Counter(v['size'] for v in vertices
                         if '1' in (v['fontstyle'] or '') and v['size'])
    title_font_size = None
    title_bold = False
    if bold_sizes:
        try:
            title_font_size = int(bold_sizes.most_common(1)[0][0])
        except (ValueError, TypeError):
            title_font_size = None
        if title_font_size and title_font_size > font_size:
            title_bold = True

    # ---- 3e. 边默认样式 ----
    COORD_KEYS = ('entryX', 'entryY', 'exitX', 'exitY', 'entryDx', 'entryDy', 'exitDx', 'exitDy')
    def strip_coords(style):
        parts = []
        for p in style.split(';'):
            p = p.strip()
            if not p:
                continue
            k = p.split('=', 1)[0].strip() if '=' in p else p
            if k in COORD_KEYS:
                continue
            parts.append(p)
        return ';'.join(parts)

    edge_style_counter = Counter(strip_coords(e['style']) for e in edges)
    arrow_counter = Counter()
    dashed_labels = []
    for e in edges:
        kv, _ = parse_style(e['style'])
        arrow = 'endArrow=' + kv.get('endArrow', 'classic') + ';endFill=' + kv.get('endFill', '1')
        arrow_counter[arrow] += 1
        if kv.get('dashed') == '1' and e['label']:
            dashed_labels.append(e['label'].strip())

    edge_style = edge_style_counter.most_common(1)[0][0] if edge_style_counter else \
        'edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1'
    arrow = arrow_counter.most_common(1)[0][0] if arrow_counter else 'endArrow=classic;endFill=1'

    # dashedFor：>=2 条虚线边共享同一标签词
    dashedFor = []
    if len(dashed_labels) >= 2:
        dc = Counter(dashed_labels)
        for tok, n in dc.most_common():
            if n >= 2:
                dashedFor.append(tok)
                break

    # ---- 3f. extras ----
    sketch = any('sketch=1' in v['style'] for v in vertices) or \
             any('sketch=1' in e['style'] for e in edges)
    sw_counter = Counter(v['strokeWidth'] for v in vertices if v['strokeWidth'])
    global_sw = 1
    if sw_counter:
        try:
            global_sw = float(sw_counter.most_common(1)[0][0])
        except (ValueError, TypeError):
            global_sw = 1

    extras = {'sketch': sketch, 'globalStrokeWidth': global_sw}

    # ---- 3g. 置信度 ----
    distinct_pairs = len(pair_counter)
    confidence = 'high'
    if distinct_pairs < 3:
        confidence = 'medium'

    summary = {
        'vertices': len(vertices),
        'edges': len(edges),
        'distinct_color_pairs': distinct_pairs,
        'none_fill_top': dict(none_fill_counter.most_common(8)),
        'font_counter': dict(font_counter.most_common(5)),
        'size_counter': dict(size_counter.most_common(6)),
        'role_dist': dict(Counter(v['role'] for v in vertices).most_common(10)),
    }

    preset = {
        'name': None,  # 由 main 填入
        'version': 1,
        'default': False,
        'source': {'type': 'xml', 'path': '', 'extracted_at': str(date.today())},
        'confidence': confidence,
        'palette': palette,
        'roles': roles,
        'shapes': shapes,
        'font': {'fontFamily': font_family, 'fontSize': font_size},
        'edges': {'style': edge_style, 'arrow': arrow, 'dashedFor': dashedFor},
        'extras': extras,
    }
    if title_font_size:
        preset['font']['titleFontSize'] = title_font_size
        preset['font']['titleBold'] = title_bold

    return preset, summary


# ---------------------------------------------------------------------------
# 4. 主入口
# ---------------------------------------------------------------------------
def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)

    target = args[0]
    name = 'linlan'
    out = None
    i = 1
    while i < len(args):
        if args[i] == '--name' and i + 1 < len(args):
            name = args[i + 1].lower()
            i += 2
        elif args[i] == '--out' and i + 1 < len(args):
            out = args[i + 1]
            i += 2
        else:
            i += 1

    # 收集输入文件
    paths = []
    if os.path.isdir(target):
        paths = sorted(os.path.join(target, f) for f in os.listdir(target)
                       if f.endswith('.drawio'))
    else:
        paths = [target]

    if not paths:
        print('未找到 .drawio 文件:', target)
        sys.exit(1)

    preset, summary = extract(paths)
    if preset is None:
        print('提取失败:', summary)
        sys.exit(1)

    preset['name'] = name
    preset['source']['path'] = target

    # 输出 JSON
    if not out:
        here = os.path.dirname(os.path.abspath(__file__))
        out = os.path.join(here, '..', 'styles', f'{name}.json')
    out = os.path.abspath(out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(preset, f, ensure_ascii=False, indent=2)

    # 打印摘要
    print('=' * 70)
    print(f'风格提取完成：{len(paths)} 个文件，顶点 {summary["vertices"]}，边 {summary["edges"]}')
    print('=' * 70)
    print(f'角色分布: {summary["role_dist"]}')
    print(f'字体: {summary["font_counter"]}')
    print(f'字号: {summary["size_counter"]}')
    print(f'留白+描边色(签名): {summary["none_fill_top"]}')
    print(f'有效配色对数: {summary["distinct_color_pairs"]} | 置信度: {preset["confidence"]}')
    print(f'调色板: {json.dumps(preset["palette"], ensure_ascii=False)}')
    print(f'角色映射: {json.dumps(preset["roles"], ensure_ascii=False)}')
    print(f'形状: {json.dumps(preset["shapes"], ensure_ascii=False)}')
    print(f'字体设置: {json.dumps(preset["font"], ensure_ascii=False)}')
    print(f'边: {json.dumps(preset["edges"], ensure_ascii=False)}')
    print(f'extras: {json.dumps(preset["extras"], ensure_ascii=False)}')
    print(f'\n已保存: {out}')


if __name__ == '__main__':
    main()
