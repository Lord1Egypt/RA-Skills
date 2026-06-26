#!/usr/bin/env python3
"""
dxf2pdf.py - DXF 转矢量 PDF（v2.0，ezdxf原生渲染+多页+大样图）
用法: python3 dxf2pdf.py <输入.dxf> [输出.pdf] [--paper A3] [--dpi 300]

模块：
  1. 文字解码 - MBCS/Unicode/%%编码
  2. 预处理  - DIM修复/字体替换/圆圈编号补全
  3. 页面检测 - 粉紫色图框 + 大样图区域聚类
  4. 渲染    - ezdxf原生引擎，黑白输出
  5. 输出    - 多页PDF，按比例裁剪
"""

import sys, os, re
import ezdxf
from ezdxf.addons.drawing import Frontend, RenderContext
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.addons.drawing.config import Configuration, ColorPolicy, HatchPolicy, TextPolicy
from ezdxf.math import Vec3
from ezdxf.enums import TextEntityAlignment
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
from pathlib import Path
from collections import defaultdict


# ============================================================
# 常量
# ============================================================

PAPER_SIZES = {
    'A0': (1189, 841), 'A1': (841, 594), 'A2': (594, 420),
    'A3': (420, 297), 'A4': (297, 210),
}

ACAD_CHAR_MAP = {132: 'Φ', 133: 'Φ', 134: 'Φ', 178: '²', 179: '³'}

# 不可用字体列表（需替换为Noto Sans CJK）
BAD_FONTS = (
    'STXIHEI.TTF', 'STXINWEI.TTF', 'STKAITI.TTF', 'STSONG.TTF',
    'SIMHEI.TTF', 'SIMSUN.TTC', 'FZHTK.TTF', 'FZSTK.TTF',
    'HZTXT.SHX', 'TSSDENG.SHX', 'ZHCAD.SHX', '',
)


# ============================================================
# 模块1：文字解码
# ============================================================

def decode_text(text):
    """解码天正MBCS编码和AutoCAD特殊字符"""
    if not text:
        return text
    # 天正MBCS: \M+XXXXX → GBK（前1位标记位 + 4位GBK码）
    def decode_mbc(m):
        gbk_hex = m.group(1)[1:]  # 去掉第1位标记位
        try:
            return bytes.fromhex(gbk_hex).decode('gbk')
        except:
            return m.group(0)
    text = re.sub(r'\\M\+([0-9A-Fa-f]{5})', decode_mbc, text)
    # Unicode: \U+XXXX
    text = re.sub(r'\\U\+([0-9A-Fa-f]{4})', lambda m: chr(int(m.group(1), 16)), text)
    # AutoCAD特殊字符
    text = text.replace('%%c', 'Ø').replace('%%d', '°').replace('%%p', '±')
    text = text.replace('%%u', '').replace('%%o', '').replace('%%%', '%')
    text = re.sub(r'%%(\d{3})', lambda m: ACAD_CHAR_MAP.get(int(m.group(1)), f'[{m.group(1)}]'), text)
    return text


def decode_entity_text(entity):
    """解码单个实体的文字内容"""
    try:
        etype = entity.dxftype()
        if etype == 'TEXT':
            entity.dxf.text = decode_text(entity.dxf.text)
        elif etype == 'MTEXT':
            if hasattr(entity, 'text'):
                entity.text = decode_text(entity.text)
        elif etype == 'DIMENSION':
            if hasattr(entity.dxf, 'text') and entity.dxf.text:
                entity.dxf.text = decode_text(entity.dxf.text)
        elif etype == 'ATTRIB':
            entity.dxf.text = decode_text(entity.dxf.text)
    except:
        pass


# ============================================================
# 模块2：预处理
# ============================================================

def preprocess(doc):
    """
    全面预处理：
    1. 解码所有文字（模型空间 + 块定义）
    2. 修复DIMENSION insert点（0,0 → 实际位置）
    3. 替换不可用字体
    4. 补全DIM_IDEN圆圈内缺失的编号
    """
    msp = doc.modelspace()

    # --- 1. 解码所有文字 ---
    for e in msp:
        decode_entity_text(e)
    for block in doc.blocks:
        for e in block:
            decode_entity_text(e)

    # --- 2. 修复DIMENSION insert ---
    for e in msp:
        if e.dxftype() == 'DIMENSION':
            try:
                if e.dxf.insert.x == 0 and e.dxf.insert.y == 0:
                    dp1 = e.dxf.defpoint
                    dp2 = e.dxf.defpoint2 if hasattr(e.dxf, 'defpoint2') else dp1
                    mx = (dp1.x + dp2.x) / 2
                    my = (dp1.y + dp2.y) / 2
                    e.dxf.insert = Vec3(mx, my, 0)
            except:
                continue

    # --- 3. 替换不可用字体 ---
    for style in doc.styles:
        try:
            font = style.dxf.font if hasattr(style.dxf, 'font') else ''
            if font.upper() in BAD_FONTS:
                style.dxf.font = 'NotoSansCJK-Regular.ttc'
        except:
            continue

    # --- 3b. 过滤malformed TEXT实体（insert为None等） ---
    to_delete = []
    for e in msp:
        if e.dxftype() in ('TEXT', 'MTEXT'):
            try:
                _ = e.dxf.insert
                if e.dxf.insert is None:
                    to_delete.append(e)
            except:
                to_delete.append(e)
    for e in to_delete:
        msp.delete_entity(e)

    # --- 4. 补全DIM_IDEN圆圈编号 ---
    fix_dim_iden_circles(doc)

    return doc


def fix_dim_iden_circles(doc):
    """
    检测DIM_IDEN图层的圆圈，如果内部没有文字，自动补编号。
    ODA File Converter转DXF时会丢失SHX字体的编号文字，这里做fallback。
    """
    msp = doc.modelspace()

    # 收集DIM_IDEN图层的圆圈
    circles = []
    for e in msp:
        if e.dxftype() == 'CIRCLE' and e.dxf.layer == 'DIM_IDEN':
            cx, cy, r = e.dxf.center.x, e.dxf.center.y, e.dxf.radius
            if r > 30:  # 排除太小的圆（可能是钢筋截面等）
                circles.append((cx, cy, r))

    if not circles:
        return 0

    # 检查每个圆内部是否有TEXT
    needs_fix = []
    for cx, cy, r in circles:
        has_text = False
        for e in msp:
            if e.dxftype() in ('TEXT', 'MTEXT'):
                tx, ty = e.dxf.insert.x, e.dxf.insert.y
                dist = ((tx - cx)**2 + (ty - cy)**2)**0.5
                if dist <= r * 1.2:
                    has_text = True
                    break
        if not has_text:
            needs_fix.append((cx, cy, r))

    if not needs_fix:
        return 0

    # 按位置排序（先Y降序，再X升序）→ 符合从上到下、从左到右的阅读顺序
    needs_fix.sort(key=lambda p: (-p[1], p[0]))

    # 补编号
    fixed = 0
    for i, (cx, cy, r) in enumerate(needs_fix, 1):
        # 根据圆圈半径自适应文字高度
        h = r * 1.2
        txt = msp.add_text(
            str(i),
            dxfattribs={
                'height': h,
                'layer': 'DIM_IDEN',
                'color': 7,  # 白色/黑色
                'style': 'Standard',
            }
        )
        txt.set_placement((cx, cy), align=TextEntityAlignment.CENTER)
        fixed += 1

    return fixed


# ============================================================
# 模块3：页面检测
# ============================================================

def find_pink_frames(msp):
    """找颜色6(粉紫色)的闭合多段线作为主图框"""
    candidates = []
    for e in msp:
        if e.dxftype() == 'LWPOLYLINE' and e.closed and e.dxf.color == 6:
            pts = list(e.get_points(format='xy'))
            if len(pts) >= 4:
                xs = [p[0] for p in pts]
                ys = [p[1] for p in pts]
                w = max(xs) - min(xs)
                h = max(ys) - min(ys)
                if w > 500 and h > 500:
                    candidates.append({
                        'bbox': (min(xs), min(ys), max(xs), max(ys)),
                        'w': w, 'h': h, 'area': w * h,
                    })
    candidates.sort(key=lambda x: -x['area'])
    return candidates


def find_detail_views(msp, frame_bboxes, min_entities=20, grid_size=2000):
    """
    检测图框外的实体聚集区域（大样图）。
    用网格聚类找密集区域，返回每个区域的bounding box。
    """
    outside = []
    for e in msp:
        try:
            ex, ey = None, None
            etype = e.dxftype()
            if etype == 'LINE':
                ex = (e.dxf.start.x + e.dxf.end.x) / 2
                ey = (e.dxf.start.y + e.dxf.end.y) / 2
            elif etype == 'CIRCLE':
                ex, ey = e.dxf.center.x, e.dxf.center.y
            elif etype == 'ARC':
                ex, ey = e.dxf.center.x, e.dxf.center.y
            elif etype in ('TEXT', 'MTEXT', 'INSERT', 'DIMENSION'):
                ex, ey = e.dxf.insert.x, e.dxf.insert.y
            elif etype == 'LWPOLYLINE':
                pts = list(e.get_points(format='xy'))
                if pts:
                    ex = sum(p[0] for p in pts) / len(pts)
                    ey = sum(p[1] for p in pts) / len(pts)
            elif etype == 'HATCH':
                continue  # 跳过HATCH，避免重复计数

            if ex is None:
                continue

            # 检查是否在主图框内
            inside = False
            for fb in frame_bboxes:
                if fb[0]-200 <= ex <= fb[2]+200 and fb[1]-200 <= ey <= fb[3]+200:
                    inside = True
                    break
            if not inside:
                outside.append((ex, ey))
        except:
            pass

    if len(outside) < min_entities:
        return []

    # 网格聚类
    clusters = defaultdict(list)
    for ex, ey in outside:
        gx = int(ex // grid_size) * grid_size
        gy = int(ey // grid_size) * grid_size
        clusters[(gx, gy)].append((ex, ey))

    # 找密度足够的聚类
    detail_views = []
    for (gx, gy), points in clusters.items():
        if len(points) >= min_entities:
            xs = [p[0] for p in points]
            ys = [p[1] for p in points]
            margin = 500
            detail_views.append({
                'bbox': (min(xs)-margin, min(ys)-margin, max(xs)+margin, max(ys)+margin),
                'w': max(xs)-min(xs)+2*margin,
                'h': max(ys)-min(ys)+2*margin,
                'count': len(points),
            })

    detail_views.sort(key=lambda x: -x['count'])
    return detail_views


# ============================================================
# 模块4：渲染
# ============================================================

def create_ezdxf_config():
    """创建ezdxf渲染配置：黑白 + HATCH显示 + 文字填充"""
    return Configuration(
        color_policy=ColorPolicy.BLACK,
        hatch_policy=HatchPolicy.SHOW_APPROXIMATE_PATTERN,
        text_policy=TextPolicy.FILLING,
    )


def render_page(doc, ax, config):
    """用ezdxf原生引擎渲染全部实体到指定axes"""
    ctx = RenderContext(doc)
    out = MatplotlibBackend(ax)
    frontend = Frontend(ctx, out, config=config)
    frontend.draw_entities(doc.modelspace())


# ============================================================
# 模块5：输出
# ============================================================

def build_pages(frame_bboxes, detail_views):
    """合并主图框和大样图为统一的页面列表"""
    pages = []
    for i, bbox in enumerate(frame_bboxes, 1):
        pages.append({'bbox': bbox, 'type': f'主图{i}'})
    for i, dv in enumerate(detail_views, 1):
        pages.append({'bbox': dv['bbox'], 'type': f'大样{i}'})
    return pages


def export_pdf(doc, output, pages, paper='A3', dpi=300):
    """多页PDF输出"""
    pw, ph = PAPER_SIZES.get(paper, PAPER_SIZES['A3'])
    config = create_ezdxf_config()

    with PdfPages(output) as pdf:
        for page_idx, page in enumerate(pages, 1):
            bbox = page['bbox']
            fxmin, fymin, fxmax, fymax = bbox
            frame_w = fxmax - fxmin
            frame_h = fymax - fymin

            # 按图框比例计算纸张高度（保持A3宽度，高度自适应）
            actual_ph = pw * (frame_h / frame_w)
            fig_w = pw / 25.4
            fig_h = actual_ph / 25.4

            fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
            ax.set_facecolor('white')
            fig.patch.set_facecolor('white')

            render_page(doc, ax, config)

            ax.set_xlim(fxmin, fxmax)
            ax.set_ylim(fymin, fymax)
            ax.set_aspect('equal')
            ax.axis('off')

            plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
            fig.savefig(pdf, format='pdf', dpi=dpi, facecolor='white')
            plt.close(fig)

            print(f"  第{page_idx}页({page['type']}): 渲染完成")


# ============================================================
# 主入口
# ============================================================

def main():
    if len(sys.argv) < 2:
        print("用法: python3 dxf2pdf.py <输入.dxf> [输出.pdf] [--paper A3] [--dpi 300]")
        sys.exit(1)

    infile = sys.argv[1]
    outfile = None
    paper = 'A3'
    dpi = 300

    i = 2
    while i < len(sys.argv):
        a = sys.argv[i]
        if a == '--paper' and i+1 < len(sys.argv):
            paper = sys.argv[i+1]; i += 2
        elif a == '--dpi' and i+1 < len(sys.argv):
            dpi = int(sys.argv[i+1]); i += 2
        elif not a.startswith('--'):
            outfile = a; i += 1
        else:
            i += 1

    if not outfile:
        outfile = str(Path(infile).with_suffix('.pdf'))

    # --- 读取 ---
    print(f"读取: {infile}")
    doc = ezdxf.readfile(infile)
    msp = doc.modelspace()

    # --- 统计 ---
    n = sum(1 for _ in msp)
    n_hatch = sum(1 for e in msp if e.dxftype() == 'HATCH')
    n_dim = sum(1 for e in msp if e.dxftype() == 'DIMENSION')
    n_text = sum(1 for e in msp if e.dxftype() in ('TEXT', 'MTEXT'))
    n_insert = sum(1 for e in msp if e.dxftype() == 'INSERT')
    print(f"  实体: {n} (文字{n_text}, 填充{n_hatch}, 标注{n_dim}, 块引用{n_insert})")

    # --- 预处理 ---
    print("预处理: 解码文字 / 修复标注 / 替换字体 / 补全编号")
    doc = preprocess(doc)
    msp = doc.modelspace()

    # --- 页面检测 ---
    print(f"渲染: {paper} {dpi}DPI → {outfile}")

    frame_bboxes = [f['bbox'] for f in find_pink_frames(msp)]
    detail_views = find_detail_views(msp, frame_bboxes)

    if not frame_bboxes:
        print("  未找到粉紫色图框")
        sys.exit(1)

    print(f"  主图框: {len(frame_bboxes)}个")
    for i, f in enumerate(find_pink_frames(msp), 1):
        print(f"    #{i}: {f['w']:.0f} x {f['h']:.0f}")

    if detail_views:
        print(f"  大样图: {len(detail_views)}个")
        for i, dv in enumerate(detail_views, 1):
            print(f"    #{i}: {dv['w']:.0f} x {dv['h']:.0f} ({dv['count']}个实体)")

    # --- 输出 ---
    pages = build_pages(frame_bboxes, detail_views)
    export_pdf(doc, outfile, pages, paper=paper, dpi=dpi)

    # --- 完成 ---
    if os.path.exists(outfile):
        kb = os.path.getsize(outfile) / 1024
        print(f"✅ 完成: {outfile} ({kb:.0f}KB, {len(pages)}页)")
    else:
        print("❌ 失败")
        sys.exit(1)


if __name__ == '__main__':
    main()
