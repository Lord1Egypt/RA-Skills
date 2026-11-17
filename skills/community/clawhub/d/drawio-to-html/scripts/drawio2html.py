#!/usr/bin/env python3
"""
drawio-to-html: Convert drawio/diagrams.net XML files to self-contained HTML with SVG rendering.

Usage:
    python3 drawio2html.py <input.drawio> [output.html]

If output.html is omitted, it defaults to <input>.html in the same directory.
"""

import sys
import os
import xml.etree.ElementTree as ET
import re


def parse_style(style_str):
    """Parse mxCell style string into a dict."""
    result = {}
    if not style_str:
        return result
    for part in style_str.split(';'):
        if '=' in part:
            k, v = part.split('=', 1)
            result[k] = v
        elif part:
            result[part] = True
    return result


def parse_color(c):
    """Parse drawio color to CSS color."""
    if not c:
        return None
    if c.startswith('#'):
        return c
    if re.match(r'^[0-9A-Fa-f]{6}$', c):
        return '#' + c
    return c


def drawio_to_html(input_path, output_path=None):
    if output_path is None:
        base, _ = os.path.splitext(input_path)
        output_path = base + '.html'

    tree = ET.parse(input_path)
    root = tree.getroot()

    # Extract diagram name from <diagram> element
    diagram_elem = root.find('diagram')
    diagram_name = diagram_elem.get('name', 'Flowchart') if diagram_elem is not None else 'Flowchart'

    # Find all mxCell elements
    cells = root.findall('.//mxCell')

    vertices = {}
    edges = []

    for cell in cells:
        cell_id = cell.get('id', '')
        if cell_id in ('0', '1'):
            continue

        style_str = cell.get('style', '')
        style = parse_style(style_str)
        value = cell.get('value', '')
        geometry = cell.find('mxGeometry')

        if cell.get('vertex') == '1':
            if geometry is not None:
                x = float(geometry.get('x', 0))
                y = float(geometry.get('y', 0))
                w = float(geometry.get('width', 100))
                h = float(geometry.get('height', 60))
                vertices[cell_id] = {
                    'id': cell_id,
                    'value': value,
                    'style': style,
                    'x': x, 'y': y, 'w': w, 'h': h,
                }

        elif cell.get('edge') == '1':
            source = cell.get('source', '')
            target = cell.get('target', '')
            points = []
            if geometry is not None:
                pt_elem = geometry.find('Array')
                if pt_elem is not None:
                    for pt in pt_elem.findall('mxPoint'):
                        px = pt.get('x')
                        py = pt.get('y')
                        if px is not None and py is not None:
                            points.append((float(px), float(py)))
            edges.append({
                'id': cell_id,
                'source': source,
                'target': target,
                'value': value,
                'style': style,
                'points': points,
            })

    # Compute bounding box
    all_x, all_y = [], []
    for v in vertices.values():
        all_x.extend([v['x'], v['x'] + v['w']])
        all_y.extend([v['y'], v['y'] + v['h']])
    for e in edges:
        for px, py in e['points']:
            all_x.append(px)
            all_y.append(py)

    min_x = min(all_x) if all_x else 0
    min_y = min(all_y) if all_y else 0
    max_x = max(all_x) if all_x else 800
    max_y = max(all_y) if all_y else 700

    padding = 60
    vb_x = min_x - padding
    vb_y = min_y - padding
    vb_w = max_x - min_x + padding * 2
    vb_h = max_y - min_y + padding * 2

    # Build SVG
    svg_parts = []
    svg_parts.append('''    <defs>
      <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
        <path d="M0,0 L0,6 L9,3 z" fill="#333" />
      </marker>
      <marker id="arrow-dashed" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
        <path d="M0,0 L0,6 L9,3 z" fill="#666" />
      </marker>
    </defs>''')

    # Draw edges
    for e in edges:
        src = vertices.get(e['source'])
        tgt = vertices.get(e['target'])
        if not src or not tgt:
            continue

        sx = src['x'] + src['w'] / 2
        sy = src['y'] + src['h'] / 2
        tx = tgt['x'] + tgt['w'] / 2
        ty = tgt['y'] + tgt['h'] / 2

        exitX = e['style'].get('exitX')
        exitY = e['style'].get('exitY')
        entryX = e['style'].get('entryX')
        entryY = e['style'].get('entryY')

        if exitX is not None:
            sx = src['x'] + float(exitX) * src['w']
        if exitY is not None:
            sy = src['y'] + float(exitY) * src['h']
        if entryX is not None:
            tx = tgt['x'] + float(entryX) * tgt['w']
        if entryY is not None:
            ty = tgt['y'] + float(entryY) * tgt['h']

        path_pts = [(sx, sy)]
        for px, py in e['points']:
            path_pts.append((px, py))
        path_pts.append((tx, ty))

        d = f"M{path_pts[0][0]},{path_pts[0][1]}"
        for px, py in path_pts[1:]:
            d += f" L{px},{py}"

        is_dashed = 'dashed' in e['style']
        stroke = '#666' if is_dashed else '#333'
        dash_attr = 'stroke-dasharray="5,5"' if is_dashed else ''
        marker = 'url(#arrow-dashed)' if is_dashed else 'url(#arrow)'

        svg_parts.append(f'    <path d="{d}" fill="none" stroke="{stroke}" stroke-width="1.5" {dash_attr} marker-end="{marker}"/>')

        if e['value']:
            mid_idx = len(path_pts) // 2
            lx = path_pts[mid_idx][0]
            ly = path_pts[mid_idx][1] - 8
            svg_parts.append(f'    <text x="{lx}" y="{ly}" text-anchor="middle" font-size="12" fill="#333">{e["value"]}</text>')

    # Draw vertices
    for v in vertices.values():
        style = v['style']
        x, y, w, h = v['x'], v['y'], v['w'], v['h']
        fill = parse_color(style.get('fillColor')) or '#ffffff'
        stroke = parse_color(style.get('strokeColor')) or '#333333'
        is_rhombus = 'rhombus' in style
        is_rounded = 'rounded=1' in style or 'arcSize' in style
        font_weight = 'bold' if style.get('fontStyle') == '1' else 'normal'

        if is_rhombus:
            cx = x + w / 2
            cy = y + h / 2
            pts = f"{cx},{y} {x+w},{cy} {cx},{y+h} {x},{cy}"
            svg_parts.append(f'    <polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        elif is_rounded:
            rx = 20 if 'arcSize=50' in str(style) else 8
            svg_parts.append(f'    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" ry="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        else:
            svg_parts.append(f'    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" ry="4" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')

        cx = x + w / 2
        lines = v['value'].split('\n')
        line_height = 16
        start_y = y + h / 2 - (len(lines) - 1) * line_height / 2 + 5
        for idx, line in enumerate(lines):
            ty = start_y + idx * line_height
            svg_parts.append(f'    <text x="{cx}" y="{ty}" text-anchor="middle" font-size="13" font-weight="{font_weight}" fill="#1f2937">{line}</text>')

    svg_content = '\n'.join(svg_parts)

    html_doc = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{diagram_name}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            min-height: 100vh;
        }}
        .container {{
            background: #fff;
            border-radius: 12px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
            padding: 30px;
            max-width: 100%;
            overflow: auto;
        }}
        h1 {{
            text-align: center;
            color: #1f2937;
            margin-bottom: 24px;
            font-size: 1.5rem;
        }}
        svg {{
            display: block;
            max-width: 100%;
            height: auto;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{diagram_name}</h1>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb_x} {vb_y} {vb_w} {vb_h}" width="{vb_w}" height="{vb_h}">
{svg_content}
        </svg>
    </div>
</body>
</html>'''

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_doc)

    return output_path


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 drawio2html.py <input.drawio> [output.html]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    result = drawio_to_html(input_file, output_file)
    print(f'✅ Converted: {result}')
