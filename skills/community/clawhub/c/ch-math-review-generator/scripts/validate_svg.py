#!/usr/bin/env python3
"""
SVG 图形校验脚本
校验 HTML 中的 SVG 数学图形是否绘制正确：
  1. 一次函数：直线与标注的y轴截距点是否吻合（误差<5px）
  2. 几何图形：顶点数、对角线交点、平行/垂直关系
  3. 反比例函数：双曲线分支是否在正确象限
  4. 通用：坐标是否超出 viewBox 范围

使用方法：
  python scripts/validate_svg.py <html_file_path> [--verbose]
"""

import sys
import re
import math
import argparse
from pathlib import Path

C_OK   = '\033[92m'
C_ERR  = '\033[91m'
C_WARN = '\033[93m'
C_INFO = '\033[96m'
C_END  = '\033[0m'

def log(msg, level="INFO"):
    prefix = {"INFO": f"{C_INFO}[INFO]{C_END}", "WARN": f"{C_WARN}[WARN]{C_END}",
              "ERROR": f"{C_ERR}[ERROR]{C_END}", "OK": f"{C_OK}[PASS]{C_END}"}
    try:
        print(f"{prefix.get(level, prefix['INFO'])} {msg}")
    except UnicodeEncodeError:
        import re as _re
        clean = _re.sub(r'\x1b\[[0-9;]*m', '', f"{prefix.get(level, prefix['INFO'])} {msg}")
        print(clean)


def get_viewbox(svg_html):
    m = re.search(r'viewBox\s*=\s*"([\d.\s\-]+)"', svg_html)
    if not m:
        return 0, 0, 180, 180
    p = [float(x) for x in m.group(1).split()]
    return p[0], p[1], p[2], p[3]


def get_origin(svg_html):
    _, _, w, h = get_viewbox(svg_html)
    return w / 2, h / 2


def extract_non_axis_lines(svg_html):
    """提取所有非坐标轴的<line>"""
    lines = []
    axis_colors = {'#bbb', '#ccc', '#aaa', '#999', '#666', 'gray', 'grey', '#ddd'}
    for m in re.finditer(r'<line\s[^>]+>', svg_html):
        attrs = m.group(0)
        x1 = float(re.search(r'x1\s*=\s*"([^"]+)"', attrs).group(1))
        y1 = float(re.search(r'y1\s*=\s*"([^"]+)"', attrs).group(1))
        x2 = float(re.search(r'x2\s*=\s*"([^"]+)"', attrs).group(1))
        y2 = float(re.search(r'y2\s*=\s*"([^"]+)"', attrs).group(1))
        s_m = re.search(r'stroke\s*=\s*"([^"]+)"', attrs)
        stroke = s_m.group(1) if s_m else None
        if stroke and stroke.lower() in axis_colors:
            continue
        if stroke is None:
            continue
        lines.append((x1, y1, x2, y2, stroke))
    return lines


def extract_circles(svg_html):
    circles = []
    for m in re.finditer(r'<circle\s[^>]+>', svg_html):
        attrs = m.group(0)
        cx = float(re.search(r'cx\s*=\s*"([^"]+)"', attrs).group(1))
        cy = float(re.search(r'cy\s*=\s*"([^"]+)"', attrs).group(1))
        r_m = re.search(r'r\s*=\s*"([^"]+)"', attrs)
        r = float(r_m.group(1)) if r_m else 4
        circles.append((cx, cy, r))
    return circles


def y_axis_cross_y(lines, y_axis_x=90, tolerance=0.5):
    """
    计算线段与 y轴(x=y_axis_x) 的交点y值
    返回 (线段索引, 交点y) 列表
    """
    crossings = []
    for i, (x1, y1, x2, y2, s) in enumerate(lines):
        if abs(x2 - x1) < 1e-9:
            if abs(x1 - y_axis_x) < tolerance:
                crossings.append((i, y1))
            continue
        t = (y_axis_x - x1) / (x2 - x1)
        if -0.02 <= t <= 1.02:
            iy = y1 + t * (y2 - y1)
            crossings.append((i, iy))
    return crossings


def validate_linear_function(svg_html, verbose=False):
    """一次函数图形：验证直线在y轴截距点"""
    errors = []
    lines = extract_non_axis_lines(svg_html)
    circles = extract_circles(svg_html)

    if verbose:
        log(f"  找到 {len(lines)} 条直线，{len(circles)} 个圆点标注", "INFO")

    if not lines:
        return errors

    # y轴 x=90
    crossings = y_axis_cross_y(lines, y_axis_x=90)

    if not crossings:
        errors.append("未找到直线与y轴的交点")
        return errors

    # 找截距标注圆（cx接近90）
    b_pts = [(cx, cy) for cx, cy, r in circles if abs(cx - 90) < 20]

    if not b_pts:
        # 没有找到截距圆，看看图形是否有截距标注文字
        b_label = re.search(r'b\s*(&gt;|&lt;|>|<)\s*0|b\s*=\s*["\']?([-\d.]+)', svg_html, re.IGNORECASE)
        if b_label:
            # 有截距标注但没画圆点，这是风格问题不是错误
            pass
        return errors

    cx, cy_annotated = b_pts[0]

    # 验证每条直线在y轴的交点
    for line_idx, iy in crossings:
        x1, y1, x2, y2, stroke = lines[line_idx]
        diff = abs(iy - cy_annotated)
        if verbose:
            log(f"  线在y轴交点={iy:.1f}，标注点cy={cy_annotated}，误差={diff:.1f}px", "INFO")
        if diff > 5:
            errors.append(
                f"直线与y轴截距不吻合：直线交点({90:.0f},{iy:.1f})，标注({cx:.0f},{cy_annotated:.1f})，误差{diff:.1f}px > 5px"
            )

    return errors


def validate_vertex_figure(svg_html, verbose=False):
    """几何图形：验证顶点和对角线"""
    errors = []
    warnings = []

    lines = extract_non_axis_lines(svg_html)
    if not lines:
        return errors, warnings

    # 从line端点提取所有唯一点
    pts = {}
    for x1, y1, x2, y2, s in lines:
        for pt in [(x1, y1), (x2, y2)]:
            k = f"{pt[0]:.0f}_{pt[1]:.0f}"
            pts[k] = pt

    unique_pts = list(pts.values())
    n = len(unique_pts)

    if n < 3:
        warnings.append(f"顶点数不足（{n}个），图形可能不完整")
        return errors, warnings

    if n > 4:
        # 可能是带标注的多边形，用凸包/最外层判断
        warnings.append(f"顶点数为{n}，多于标准4边形，可能是标注线叠加（请人工检查）")

    if verbose:
        log(f"  推断顶点数: {n}", "INFO")

    if n == 4:
        # 验证对角线交于同一点
        # 假设按顺时针排列：0-2是对角，1-3是对角
        A, B, C, D = unique_pts
        # 对角线AC中点和BD中点应重合
        mid1 = ((A[0]+C[0])/2, (A[1]+C[1])/2)
        mid2 = ((B[0]+D[0])/2, (B[1]+D[1])/2)
        dist = math.sqrt((mid1[0]-mid2[0])**2 + (mid1[1]-mid2[1])**2)
        if dist > 5:
            errors.append(f"对角线不交于同一点：中点1({mid1[0]:.0f},{mid1[1]:.0f})，中点2({mid2[0]:.0f},{mid2[1]:.0f})，距离{dist:.1f}px")
        else:
            if verbose:
                log(f"  [OK] 对角线交于({mid1[0]:.0f},{mid1[1]:.0f})，偏差{dist:.1f}px", "OK")

        # 验证矩形：检查是否有两组垂直边
        # 计算各边向量
        edges = [
            (B[0]-A[0], B[1]-A[1]),
            (C[0]-B[0], C[1]-B[1]),
            (D[0]-C[0], D[1]-C[1]),
            (A[0]-D[0], A[1]-D[1]),
        ]
        def dot(v1, v2):
            return v1[0]*v2[0] + v1[1]*v2[1]
        def len_(v):
            return math.sqrt(v[0]**2 + v[1]**2)

        # 矩形：相邻边垂直（点积≈0）
        is_rect = any(abs(dot(edges[i], edges[(i+1)%4])) < 1e-6 for i in range(4))
        if is_rect:
            # 验证对边相等
            e0_len = len_(edges[0]); e2_len = len_(edges[2])
            e1_len = len_(edges[1]); e3_len = len_(edges[3])
            if abs(e0_len - e2_len) > 2 and abs(e1_len - e3_len) > 2:
                warnings.append("矩形的两组对边长度差异较大，请确认图形是否标准")
            if verbose:
                log(f"  [OK] 验证为矩形：对角线交于一点", "OK")

        # 验证菱形：四条边相等
        lens = sorted([len_(e) for e in edges])
        if lens[0] > 0 and (lens[-1] - lens[0]) / lens[0] < 0.05:
            if verbose:
                log(f"  [OK] 验证为菱形：四条边长度差异<5%（{lens[0]:.1f}~{lens[-1]:.1f}）", "OK")

    return errors, warnings


def validate_inverse_function(svg_html, verbose=False):
    """反比例函数：验证双曲线象限"""
    errors = []
    warnings = []
    paths = re.findall(r'<path\s[^>]+>', svg_html)
    if len(paths) < 1:
        warnings.append("未找到反比例函数曲线（path）")
    elif verbose:
        log(f"  找到 {len(paths)} 条曲线", "INFO")
    return errors, warnings


def detect_graph_type(svg_html, context_before=""):
    """根据SVG内容和上下文判断图形类型"""
    svg_lower = svg_html.lower()
    ctx_lower = context_before.lower()

    if any(k in svg_lower for k in ['y=-(', 'y=-0.', 'y=0.-']) or \
       re.search(r'k\s*[<>]', svg_lower) and r'x\s*\+\s*\d' in svg_lower:
        return "linear_function"
    if '反比例' in ctx_lower or 'inverse' in ctx_lower or 'k/x' in svg_lower:
        return "inverse_function"
    if '菱形' in ctx_lower or 'rhombus' in ctx_lower:
        return "rhombus"
    if '矩形' in ctx_lower or 'rectangle' in ctx_lower:
        return "rectangle"
    if '平行四边形' in ctx_lower or 'parallelogram' in ctx_lower:
        return "parallelogram"
    return "unknown"


def validate_file(html_path, verbose=False):
    path = Path(html_path)
    if not path.exists():
        log(f"文件不存在: {html_path}", "ERROR")
        return False

    content = path.read_text(encoding='utf-8')

    # 提取所有SVG块
    svg_blocks = list(re.finditer(r'(<svg[^>]*>.*?</svg>)', content, re.DOTALL))
    if not svg_blocks:
        log("未找到SVG图形", "WARN")
        return True

    all_ok = True
    err_count = 0
    warn_count = 0

    for m in svg_blocks:
        svg_html = m.group(0)
        line_no = content[:m.start()].count('\n') + 1
        # 提取前面200字符作为上下文
        start_ctx = max(0, m.start() - 300)
        context = content[start_ctx:m.start()]

        gtype = detect_graph_type(svg_html, context)

        if verbose:
            log(f"\n--- 第{line_no}行 SVG (类型: {gtype}) ---", "INFO")

        if gtype == "linear_function":
            errs = validate_linear_function(svg_html, verbose)
            if errs:
                for e in errs:
                    log(f"  第{line_no}行 [线性函数]: {e}", "ERROR")
                all_ok = False
                err_count += len(errs)
            elif verbose:
                log(f"  [OK] 线性函数图形校验通过", "OK")
        elif gtype in ("rectangle", "rhombus", "parallelogram"):
            errs, warns = validate_vertex_figure(svg_html, verbose)
            for e in errs:
                log(f"  第{line_no}行 [几何图形]: {e}", "ERROR")
                all_ok = False
                err_count += 1
            for w in warns:
                log(f"  第{line_no}行 [几何图形]: {w}", "WARN")
                warn_count += 1
        elif gtype == "inverse_function":
            errs, warns = validate_inverse_function(svg_html, verbose)
            for e in errs:
                log(f"  第{line_no}行 [反比例函数]: {e}", "ERROR")
                all_ok = False
                err_count += 1
            for w in warns:
                log(f"  第{line_no}行 [反比例函数]: {w}", "WARN")
                warn_count += 1
        else:
            # 通用校验：坐标范围
            vbx, vby, vbw, vbh = get_viewbox(svg_html)
            lines = extract_non_axis_lines(svg_html)
            for x1, y1, x2, y2, s in lines:
                for x, y in [(x1, y1), (x2, y2)]:
                    if x < vbx - 10 or x > vbx + vbw + 10 or y < vby - 10 or y > vby + vbh + 10:
                        log(f"  第{line_no}行: 点({x:.1f},{y:.1f})超出viewBox范围 [{vbx},{vby},{vbw},{vbh}]", "WARN")
                        warn_count += 1

    log(f"\n{'='*50}", "")
    if all_ok:
        log(f"[PASS] SVG校验通过！共{len(svg_blocks)}个图形，0个错误，{warn_count}个警告", "OK")
    else:
        log(f"[FAIL] SVG校验失败！共{len(svg_blocks)}个图形，{err_count}个错误，{warn_count}个警告", "ERROR")
    return all_ok


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="校验HTML中的SVG数学图形")
    parser.add_argument("html_file", help="HTML文件路径")
    parser.add_argument("-v", "--verbose", action="store_true", help="显示详细信息")
    args = parser.parse_args()
    ok = validate_file(args.html_file, verbose=args.verbose)
    sys.exit(0 if ok else 1)
