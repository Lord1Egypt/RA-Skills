# -*- coding: utf-8 -*-
"""分析 drawio 源文件，提取个人绘制风格特征"""
import os, re, json, sys, base64, zlib, urllib.parse
from collections import Counter
from xml.etree import ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')

# 源文件目录（用户本地资源，不上传）——可用命令行参数覆盖
REF_DIR = r'C:\Users\Administrator\.openclaw\workspace\linlan-skills-input\drawio-res'

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

def parse_styles(filepath):
    """解析单个 drawio 文件，返回风格统计"""
    try:
        raw = open(filepath, 'rb').read()
        root = ET.fromstring(raw)
    except Exception as e:
        return {'file': os.path.basename(filepath), 'error': str(e)}
    
    # 收集所有 diagram，解码后重新解析，得到真正的 mxGraphModel
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
    
    stats = {
        'file': os.path.basename(filepath),
        'cells': 0,
        'vertices': 0,
        'edges': 0,
        'fill_colors': Counter(),
        'stroke_colors': Counter(),
        'fonts': Counter(),
        'font_sizes': Counter(),
        'rounded': Counter(),   # rounded=0/1
        'shape_types': Counter(),
        'fill_style': Counter(), # solid/gradient/none
        'stroke_width': Counter(),
        'shadow': Counter(),
        'dashed': Counter(),
        'labels': [],
        'page_width': None,
        'page_height': None,
        'grid': None,
    }
    
    # 提取页面尺寸
    for model in models:
        for mxGraphModel in model.iter('mxGraphModel'):
            stats['grid'] = mxGraphModel.get('grid')
            stats['page_width'] = mxGraphModel.get('pageWidth')
            stats['page_height'] = mxGraphModel.get('pageHeight')
            stats['pageScale'] = mxGraphModel.get('pageScale')
    
    # 收集所有 cell
    all_cells = []
    for model in models:
        all_cells.extend(model.iter('mxCell'))
    for cell in all_cells:
        stats['cells'] += 1
        style = cell.get('style', '')
        value = cell.get('value', '')
        if value and value.strip():
            stats['labels'].append(value.strip()[:60])
        
        vertex = cell.get('vertex')
        edge = cell.get('edge')
        if vertex == '1':
            stats['vertices'] += 1
        if edge == '1':
            stats['edges'] += 1
        
        # 解析 style 键值对
        for part in style.split(';'):
            if '=' not in part:
                continue
            k, _, v = part.partition('=')
            k = k.strip()
            v = v.strip()
            if k == 'fillColor':
                stats['fill_colors'][v.upper()] += 1
            elif k == 'strokeColor':
                stats['stroke_colors'][v.upper()] += 1
            elif k == 'fontFamily':
                stats['fonts'][v] += 1
            elif k == 'fontSize':
                stats['font_sizes'][v] += 1
            elif k == 'rounded':
                stats['rounded'][v] += 1
            elif k == 'strokeWidth':
                stats['stroke_width'][v] += 1
            elif k == 'shadow':
                stats['shadow'][v] += 1
            elif k == 'dashed':
                stats['dashed'][v] += 1
            elif k == 'shape':
                stats['shape_types'][v] += 1
            elif k == 'fillColor':
                stats['fill_style']['solid'] += 1
        
        # 渐变/纯色判断
        if 'gradientColor=' in style:
            stats['fill_style']['gradient'] += 1
        if 'shape=mxgraph' in style:
            stats['shape_types']['mxgraph.*'] += 1
    
    return stats

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else REF_DIR
    files = sorted([f for f in os.listdir(target) if f.endswith('.drawio')])
    all_stats = []
    
    print("=" * 70)
    print("DrawIO 个人风格分析报告")
    print("=" * 70)
    
    total_fill = Counter()
    total_stroke = Counter()
    total_fonts = Counter()
    total_shapes = Counter()
    total_rounded = Counter()
    total_fontsize = Counter()
    
    for f in files:
        s = parse_styles(os.path.join(target, f))
        all_stats.append(s)
        if 'error' in s:
            print(f"\n[错误] {s['file']}: {s['error']}")
            continue
        
        total_fill.update(s['fill_colors'])
        total_stroke.update(s['stroke_colors'])
        total_fonts.update(s['fonts'])
        total_shapes.update(s['shape_types'])
        total_rounded.update(s['rounded'])
        total_fontsize.update(s['font_sizes'])
        
        print(f"\n--- {s['file']} ---")
        print(f"  页面: {s['page_width']}x{s['page_height']} (scale={s.get('pageScale')}) | 顶点:{s['vertices']} 边:{s['edges']}")
        print(f"  填充色TOP5: {dict(s['fill_colors'].most_common(5))}")
        print(f"  描边色TOP5: {dict(s['stroke_colors'].most_common(5))}")
        print(f"  字体: {dict(s['fonts'].most_common(3))}")
        print(f"  字号: {dict(s['font_sizes'].most_common(5))}")
        print(f"  圆角: {dict(s['rounded'])}")
        print(f"  形状类型TOP5: {dict(s['shape_types'].most_common(5))}")
    
    print("\n" + "=" * 70)
    print(f"全局汇总（{len(files)}个文件合计）")
    print("=" * 70)
    print(f"\n填充色 TOP15: {dict(total_fill.most_common(15))}")
    print(f"描边色 TOP15: {dict(total_stroke.most_common(15))}")
    print(f"字体: {dict(total_fonts.most_common(10))}")
    print(f"字号: {dict(total_fontsize.most_common(10))}")
    print(f"圆角: {dict(total_rounded)}")
    print(f"形状类型 TOP20: {dict(total_shapes.most_common(20))}")
    
    # 保存 JSON
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'style_report.json')
    # Counter 转普通 dict 以便 JSON 序列化
    serializable = []
    for s in all_stats:
        if 'error' in s:
            serializable.append(s)
            continue
        d = {k: (dict(v) if isinstance(v, Counter) else v) for k, v in s.items()}
        serializable.append(d)
    with open(out, 'w', encoding='utf-8') as fp:
        json.dump(serializable, fp, ensure_ascii=False, indent=2)
    print(f"\n详细报告已保存: {out}")

if __name__ == '__main__':
    main()
