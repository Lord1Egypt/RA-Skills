#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gen_card_tile.py — 竖版「知识卡片长图」引擎（一图一知识点）

链路：cards.json → HTML →（weasyprint）PDF →（PyMuPDF/pdf2image）PNG
画布：**固定比例整版**，默认 3:4；先测量内容真实高度，超出则**整体等比缩小字号**，
      直到完整落入画布 —— 从根本上杜绝「固定高度容器溢出被静默裁剪」。

支持的画布比例（`--ratio`，`@192dpi` 输出为所示像素）：
    3:4  （默认）900×1200 → 1800×2400
    9:16        900×1600 → 1800×3200
    1:1         900×900  → 1800×1800
    4:3         1200×900 → 2400×1800
    16:9        1200×675 → 2400×1350

数据唯一事实源：cards.json（每卡 id/index/title/subtitle/accent/blocks，
可选顶层 group/footer/ratio）。改内容**只改 JSON**（建议用脚本改，勿手改）。

用法：
    python gen_card_tile.py --cards cards.json --outdir out
    python gen_card_tile.py --cards cards.json --outdir out --only c07,c08
    python gen_card_tile.py --cards cards.json --outdir out --ratio 9:16
    python gen_card_tile.py --cards cards.json --outdir out --check-only   # 只校验已有产物

内置**像素级校验**（每次生成后自动执行，失败即非 0 退出）：
    · 尺寸是否等于画布            · PDF 是否恰好 1 页（>1 页 = 内容溢出）
    · 是否空白图                  · 底部页脚底色带是否存在（内容溢出会把页脚挤到下一页）
    结果同时落盘 outdir/_check.json，含每张的自适应系数 k / 页数 / 内容墨迹 bbox。

⚠️ 校验**不能**用「底部有没有深色文字像素」判断页脚：溢出时正文文字同样会落在页 1 底部，
   造成假通过；必须用**页脚底色带**（颜色容差 <= 3，白底与页脚底色只差 8，容差大就会误判）。

⚠️ 视觉模型看卡片容易把「斜线 / 弯引号 / 细竖线」误判成「裁切 / 缺失」，
   复核一律**以本脚本的像素结果为准**，视觉只作辅助。
"""
import argparse
import glob
import html
import json
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_common as rc  # noqa: E402

RATIOS = {
    '3:4': (900, 1200),
    '9:16': (900, 1600),
    '1:1': (900, 900),
    '4:3': (1200, 900),
    '16:9': (1200, 675),
}
DEFAULT_RATIO = '3:4'
DEFAULT_DPI = 192
MIN_K = 0.62          # 自适应缩字号下限（低于此值说明该卡内容该拆张）
BASE_W = 900          # 比例基准宽：所有尺寸按 W/BASE_W 放大
MEASURE_H = 4000      # 测量用超长页高度（CSS px）
PAGE_BG = (234, 238, 244)    # #eaeef4 页面底色
FOOT_BG = (247, 249, 251)    # #f7f9fb 页脚底色

COLORS = {
    'blue': '#0969da', 'green': '#1a7f37', 'orange': '#bf8700',
    'red': '#cf222e', 'purple': '#8250df', 'teal': '#0f766e',
}


def esc(s):
    return html.escape(s or '', quote=False)


def escm(s):
    """escape，并把换行转成 <br>（多行示例用）"""
    return esc(s).replace('\n', '<br>')


# ---------------------------------------------------------------- 图元 / 块
def render_cell(cell, s):
    w = cell.get('w', 1)
    cls = 'dg-cell'
    if w == 2:
        cls += ' dg-w2'
    elif w == 0.5:
        cls += ' dg-w05'
    if cell.get('tall'):
        cls += ' dg-tall'
    if cell.get('plain'):
        cls += ' dg-plain'

    if cell.get('vbar'):
        content = '<span class="dg-vbar"></span>'
    elif 'pair' in cell:
        a, b = cell['pair']
        content = (f'<div class="gl gl-tight"><span class="gl-c">{esc(a)}</span>'
                   f'<span class="gl-c">{esc(b)}</span></div>')
    elif 'base' in cell:
        if cell.get('lmark'):                     # 同格内左侧内嵌标记（专名号/浪线）
            content = (f'<span class="dg-lmark">{esc(cell["lmark"])}</span>'
                       f'<span class="dg-base dg-base-r">{esc(cell["base"])}</span>')
        else:
            content = f'<span class="dg-base">{esc(cell["base"])}</span>'
        if cell.get('mark'):
            content += f'<span class="dg-mk dg-mk-{cell.get("where", "c")}">{esc(cell["mark"])}</span>'
    elif 'glyph' in cell:
        ch = esc(cell['glyph'])
        if cell.get('under') == 'dot':
            content = f'<div class="gl gl-col"><span class="gl-c">{ch}</span><span class="gl-dot"></span></div>'
        elif cell.get('under') == 'line':
            content = f'<div class="gl gl-col"><span class="gl-c">{ch}</span><span class="gl-line"></span></div>'
        elif cell.get('side') == 'left':
            content = f'<div class="gl gl-sleft"><span class="gl-c">{ch}</span></div>'
        elif cell.get('side') == 'right':         # 着重号：右侧一个**正圆**
            content = f'<div class="gl gl-row"><span class="gl-c">{ch}</span><span class="gl-vdot"></span></div>'
        else:
            content = f'<span class="gl-c">{ch}</span>'
    elif 'vtext' in cell:
        content = f'<span class="dg-vtext">{escm(cell["vtext"])}</span>'
    elif 't' in cell:
        content = f'<span class="dg-t">{esc(cell["t"])}</span>'
    else:
        pos = cell.get('pos', 'c')
        extra = ' dg-sm' if w == 0.5 else ''
        content = f'<span class="dg-c dg-{pos}{extra}">{esc(cell.get("c", ""))}</span>'
    return f'<div class="{cls}">{content}</div>'


def render_blocks(blocks, s):
    out = []
    for b in blocks:
        tag = esc(b.get('tag', ''))
        color = COLORS.get(b.get('color', 'blue'), COLORS['blue'])
        t = b.get('type', 'text')

        if t == 'text':
            inner = f'<div class="txt">{escm(b.get("text", ""))}</div>'
        elif t == 'list':
            items = ''.join(f'<li>{escm(i)}</li>' for i in b.get('items', []))
            inner = f'<ul class="lst">{items}</ul>'
        elif t == 'compare':
            rows = ''
            for p in b.get('pairs', []):
                rows += (
                    '<div class="cmp">'
                    f'<div class="cmp-row bad"><span class="mk">误</span>'
                    f'<span class="cmp-txt">{escm(p.get("wrong", ""))}</span></div>'
                    f'<div class="cmp-row good"><span class="mk">正</span>'
                    f'<span class="cmp-txt">{escm(p.get("right", ""))}</span></div>'
                    '</div>'
                )
            inner = rows
        elif t == 'emphasis':
            inner = f'<div class="emph">{escm(b.get("text", ""))}</div>'
        elif t == 'marked':
            txt = b.get('text', '')
            if b.get('mark') == 'line':
                inner = f'<div class="mkbox"><span class="mk-line">{esc(txt)}</span></div>'
            else:
                chars = ''.join(
                    f'<span class="mk-char">{esc(ch)}<span class="mk-dot"></span></span>' for ch in txt
                )
                inner = f'<div class="mkbox">{chars}</div>'
        elif t == 'diagram':
            rows = ''
            for r in b.get('rows', []):
                cells = ''.join(render_cell(c, s) for c in r.get('cells', []))
                cellcls = 'dg-cells' + (' dg-col' if r.get('col') else '')
                note = f'<div class="dg-note">{escm(r["note"])}</div>' if r.get('note') else ''
                rows += (f'<div class="dg-item"><div class="dg-head">'
                         f'<div class="dg-label">{esc(r.get("label", ""))}</div>'
                         f'<div class="{cellcls}">{cells}</div></div>{note}</div>')
            inner = rows
        else:
            inner = ''

        out.append(
            '<div class="block">'
            f'<div class="block-head"><span class="btag" style="background:{color}">{tag}</span>'
            f'<div class="bline" style="background:linear-gradient(90deg,{color}55,transparent)"></div></div>'
            f'{inner}</div>'
        )
    return ''.join(out)


# ---------------------------------------------------------------- HTML
def build_html(card, k, W, H, group, footer_default, measure=False):
    u = W / float(BASE_W)          # 比例归一：1200 宽画布整体放大 1.33
    def s(v):
        return f'{v * u * k:.1f}px'

    idx = card.get('index', '?')
    total = card.get('total', '?')
    title = esc(card.get('title', ''))
    subtitle = esc(card.get('subtitle', ''))
    accent = COLORS.get(card.get('accent', 'blue'), COLORS['blue'])
    blocks = render_blocks(card.get('blocks', []), s)
    foot = card.get('footer') or footer_default or ''
    footer = esc(foot)
    ph = MEASURE_H if measure else H
    card_h = 'auto' if measure else f'{H}px'
    font = rc.body_font_family()

    return f'''<!DOCTYPE html><html lang="zh"><head><meta charset="UTF-8"><style>
@page {{ size: {W}px {ph}px; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: {W}px; }}
body {{ font-family: {font}; color: #1f2328; background: #eaeef4; }}
.card {{ width: {W}px; min-height: {card_h}; background: #fff; display: flex; flex-direction: column;
    border-left: {s(10)} solid {accent}; border-right: 1px solid #e3e6ea; border-bottom: 1px solid #e3e6ea; }}
.head {{ flex: 0 0 auto; background: linear-gradient(135deg, #1cb0f6, #0969da); color: #fff;
    padding: {s(26)} {s(40)} {s(22)} {s(36)}; border-bottom: {s(5)} solid #1a7f37; position: relative; }}
.badge {{ display: inline-block; font-size: {s(19)}; font-weight: 700; background: rgba(255,255,255,.22);
    padding: {s(4)} {s(16)}; border-radius: 99px; letter-spacing: 1px; }}
.head .title {{ font-size: {s(50)}; font-weight: 900; line-height: 1.12; margin-top: {s(10)}; letter-spacing: 1px; }}
.head .sub {{ font-size: {s(22)}; font-weight: 500; opacity: .9; margin-top: {s(8)}; }}
.body {{ flex: 1 1 auto; padding: {s(24)} {s(34)}; display: flex; flex-direction: column; gap: {s(15)}; }}
.block {{ flex: 0 0 auto; }}
.block-head {{ display: flex; align-items: center; gap: {s(12)}; margin-bottom: {s(9)}; }}
.btag {{ font-size: {s(22)}; font-weight: 800; color: #fff; padding: {s(4)} {s(15)}; border-radius: 8px; letter-spacing: 1px; white-space: nowrap; }}
.bline {{ flex: 1; height: {s(3)}; border-radius: 3px; }}
.txt {{ font-size: {s(26)}; line-height: 1.55; font-weight: 500; color: #24292f; background: #f6f9fc; border: 1px solid #dbe6f2; border-radius: 12px; padding: {s(15)} {s(20)}; }}
.lst {{ list-style: none; display: flex; flex-direction: column; gap: {s(7)}; }}
.lst li {{ font-size: {s(25)}; line-height: 1.46; font-weight: 500; padding: {s(9)} {s(16)} {s(9)} {s(18)}; background: #fffdf5; border: 1px solid #f0e0b0; border-left: {s(5)} solid #bf8700; border-radius: 10px; }}
.cmp {{ display: flex; flex-direction: column; gap: {s(5)}; margin-bottom: {s(10)}; }}
.cmp:last-child {{ margin-bottom: 0; }}
.cmp-row {{ display: flex; align-items: flex-start; gap: {s(12)}; padding: {s(9)} {s(16)}; border-radius: 10px; font-size: {s(25)}; line-height: 1.42; }}
.cmp-row .mk {{ flex-shrink: 0; width: {s(40)}; height: {s(40)}; line-height: {s(40)}; text-align: center; border-radius: 8px; color: #fff; font-size: {s(23)}; font-weight: 800; }}
.cmp-row.bad {{ background: #fdeceb; border: 1px solid #f5c2c0; }}
.cmp-row.bad .mk {{ background: #cf222e; }}
.cmp-row.good {{ background: #eaf6ec; border: 1px solid #b7e0c0; }}
.cmp-row.good .mk {{ background: #1a7f37; }}
.cmp-txt {{ flex: 1 1 auto; min-width: 0; color: #1f2328; font-weight: 600; }}
.emph {{ font-size: {s(25)}; font-weight: 800; color: #b42318; text-align: center; background: #fff5f4; border: 2px dashed #f1a9a2; border-radius: 12px; padding: {s(15)}; }}
.mkbox {{ text-align: center; padding: {s(10)} 0 {s(6)}; }}
.mk-char {{ display: inline-block; position: relative; font-size: {s(38)}; font-weight: 800; color: #1f2328; margin: 0 {s(4)}; padding-bottom: {s(14)}; }}
.mk-dot {{ position: absolute; left: 50%; bottom: 0; transform: translateX(-50%); width: {s(10)}; height: {s(10)}; border-radius: 50%; background: #cf222e; }}
.mk-line {{ display: inline-block; font-size: {s(38)}; font-weight: 800; color: #1f2328; border-bottom: {s(5)} solid #cf222e; padding-bottom: {s(2)}; }}
.dg-item {{ margin-bottom: {s(11)}; }}
.dg-head {{ display: flex; align-items: center; gap: {s(14)}; }}
.dg-label {{ flex: 0 0 60%; font-size: {s(23)}; font-weight: 700; color: #1f2328; line-height: 1.3; }}
.dg-cells {{ display: flex; gap: {s(3)}; flex: 1 1 auto; justify-content: flex-end; align-items: center; }}
.dg-col {{ flex-direction: column; }}
.dg-cell {{ width: {s(46)}; height: {s(46)}; border: 1.5px dashed #a9b7cc; border-radius: 8px; position: relative; background: #fbfdff; flex-shrink: 0; display: flex; align-items: center; justify-content: center; }}
.dg-tall {{ height: {s(92)}; }}
.dg-w2 {{ width: {s(95)}; }}
.dg-w05 {{ width: {s(26)}; }}
.dg-plain {{ border: none; background: transparent; }}
.dg-t {{ color: #9aa7b8; font-size: {s(23)}; font-weight: 700; }}
.dg-vtext {{ position: absolute; left: 50%; top: 50%; transform: translate(-50%,-50%); color: #cf222e; font-size: {s(26)}; font-weight: 800; line-height: 1.03; text-align: center; }}
.dg-base {{ position: absolute; left: 50%; top: 50%; transform: translate(-50%,-50%); color: #1f2328; font-size: {s(28)}; font-weight: 700; }}
.dg-base-r {{ left: 66%; }}
.dg-lmark {{ position: absolute; left: {s(4)}; top: 50%; transform: translateY(-50%); color: #cf222e; font-size: {s(24)}; font-weight: 800; line-height: 1; }}
.dg-c {{ position: absolute; left: 50%; top: 50%; transform: translate(-50%,-50%); color: #cf222e; font-size: {s(27)}; font-weight: 800; line-height: 1; }}
.dg-sm {{ font-size: {s(21)}; }}
.dg-bl {{ left: {s(4)}; top: auto; bottom: {s(1)}; transform: none; }}
.dg-br {{ left: auto; right: {s(4)}; top: auto; bottom: {s(1)}; transform: none; }}
.dg-bc {{ left: 50%; top: auto; bottom: {s(1)}; transform: translateX(-50%); }}
.dg-l {{ left: {s(5)}; top: 50%; transform: translateY(-50%); }}
.dg-r {{ left: auto; right: {s(5)}; top: 50%; transform: translateY(-50%); }}
.dg-top {{ left: 50%; top: {s(1)}; transform: translateX(-50%); }}
.dg-mk {{ position: absolute; color: #cf222e; font-size: {s(22)}; font-weight: 800; line-height: 1; }}
.dg-mk-c {{ left: 50%; top: 50%; transform: translate(-50%,-50%); }}
.dg-mk-br {{ right: 0; bottom: {s(1)}; }}
.dg-mk-bc {{ left: 50%; bottom: {s(1)}; transform: translateX(-50%); }}
.dg-vbar {{ width: {s(5)}; height: {s(70)}; background: #cf222e; border-radius: 3px; }}
.gl-col {{ display: flex; flex-direction: column; align-items: center; justify-content: center; }}
.gl-row {{ display: flex; align-items: center; gap: {s(6)}; }}
.gl-tight {{ display: flex; align-items: center; gap: {s(1)}; }}
.gl-sleft {{ display: flex; align-items: center; padding-left: {s(10)}; border-left: {s(5)} solid #cf222e; min-height: {s(40)}; }}
.gl-c {{ font-size: {s(28)}; font-weight: 700; color: #1f2328; line-height: 1; }}
.gl-dot {{ width: {s(12)}; height: {s(12)}; border-radius: 50%; background: #cf222e; margin-top: {s(6)}; }}
.gl-line {{ width: {s(42)}; height: {s(4)}; background: #cf222e; margin-top: {s(6)}; border-radius: 2px; }}
/* 着重号：正圆。必须 flex:0 0 auto + 固定宽高，否则会被 flex 拉伸成椭圆 */
.gl-vdot {{ width: {s(13)}; height: {s(13)}; border-radius: 50%; background: #cf222e; flex: 0 0 auto; align-self: center; display: block; }}
.dg-note {{ font-size: {s(20)}; color: #57606a; line-height: 1.42; margin-top: {s(3)}; }}
.foot {{ flex: 0 0 auto; padding: {s(10)} {s(34)}; font-size: {s(17)}; color: #8c959f; letter-spacing: .5px; border-top: 1px solid #e3e6ea; background: #f7f9fb; display: flex; justify-content: center; }}
</style></head><body>
<div class="card">
  <div class="head">
    <div class="badge">第 {idx} / {total} 张{f' · {esc(group)}' if group else ''}</div>
    <div class="title">{title}</div>
    {f'<div class="sub">{subtitle}</div>' if subtitle else ''}
  </div>
  <div class="body">{blocks}</div>
  <div class="foot"><span>{footer}</span></div>
</div>
</body></html>'''


# ---------------------------------------------------------------- 渲染
def _render_pdf(html_str, path):
    from weasyprint import HTML
    HTML(string=rc.patch_style(html_str)).write_pdf(path)


def measure_height(card, k, W, group, footer_default):
    """渲染一张超长页，量出卡片的真实内容高度（CSS px）。"""
    html_str = build_html(card, k, W, MEASURE_H, group, footer_default, measure=True)
    with tempfile.TemporaryDirectory() as td:
        pdf = os.path.join(td, 'm.pdf')
        _render_pdf(html_str, pdf)
        images, _ = rc.rasterize_pdf(pdf, dpi=96)
        if not images:
            return 0
        try:
            import numpy as np
        except ImportError:
            return H_fallback(images[0])
        a = np.asarray(images[0].convert('RGB')).astype(int)
        # 与**页面底色**比较（而不是"接近纯白"）——页脚底色是浅灰，用纯白判定会漏掉页脚
        diff = np.abs(a - np.array(PAGE_BG)).max(axis=2)
        rows = np.where((diff > 6).any(axis=1))[0]
        return int(rows[-1]) + 1 if len(rows) else 0


def H_fallback(img):
    """无 numpy 时的粗略回退：把页面底色做成同尺寸纯色图再求差（PIL getbbox 近似）。

    注意：不能用 `ImageChops.constant(img, 三元组)` —— Pillow 只接受 int 或单元素元组，
    传 (r,g,b) 会抛 "color must be int or single-element tuple"。
    """
    from PIL import Image, ImageChops
    rgb = img.convert('RGB')
    bg = Image.new('RGB', rgb.size, PAGE_BG)
    diff = ImageChops.difference(rgb, bg).convert('L').point(lambda v: 255 if v > 6 else 0)
    bb = diff.getbbox()
    return bb[3] if bb else 0


def gen_one(card, outdir, ratio, dpi, group, footer_default):
    W, H = RATIOS[ratio]
    k = 1.0
    h = measure_height(card, k, W, group, footer_default)
    if h <= 0:
        raise RuntimeError('%s: 内容高度测量失败（渲染结果为空？）' % card.get('id'))
    warn = None
    for _ in range(9):
        if h <= H:
            break
        k = max(MIN_K, k * (H - 6.0) / h)
        h = measure_height(card, k, W, group, footer_default)
    if h > H:
        warn = f'内容仍超出画布 (H={h} > {H}, k={k:.2f})：建议把这张卡拆成两张'

    html_str = build_html(card, k, W, H, group, footer_default)
    cid = card['id']
    idx = card.get('index')
    stem = card.get('filename', cid)
    name = f'{idx:02d}_{stem}.png' if isinstance(idx, int) else f'{stem}.png'
    png = os.path.join(outdir, name)
    with tempfile.TemporaryDirectory() as td:
        pdf = os.path.join(td, f'{cid}.pdf')
        _render_pdf(html_str, pdf)
        images, engine = rc.rasterize_pdf(pdf, dpi=dpi)
        if not images:
            raise RuntimeError('光栅化未产出图像')
        images[0].save(png, 'PNG')
    return png, k, h, len(images), warn


def check_png(path, ratio, dpi, pages=None):
    """像素级校验：尺寸 / 页数 / 空白 / 页脚是否存在。

    ⚠️ 页脚判定**不能**用「底部区域有没有深色文字像素」——内容溢出时，被切到页 1 底部的
    正文文字同样会带来深色像素，造成**假通过**（实测：5 页 PDF 被判 ok）。
    可靠判据是**页脚底色带**：页脚底色 #f7f9fb 与卡片正文底色 #fff 只差 8，
    所以颜色容差必须 <= 3（<= 10 会把白底算成页脚）。实测有页脚 ≈0.99、无页脚 0.00。
    """
    res = {'file': os.path.basename(path), 'ok': True, 'errors': [], 'warnings': []}
    W, H = RATIOS[ratio]
    scale = dpi / 96.0
    ew, eh = int(round(W * scale)), int(round(H * scale))
    if pages is not None:
        res['pages'] = pages
        if pages != 1:
            res['errors'].append('PDF 共 %d 页（>1 = 内容溢出画布，应拆成两张）' % pages)
    v = rc.verify_image(path)
    if not v.get('ok'):
        res['errors'].append('空白或损坏图：%s' % v.get('error'))
        res['ok'] = False
        return res
    w, h = v['width'], v['height']
    res['size'] = [w, h]
    if (w, h) != (ew, eh):
        res['errors'].append('尺寸 %dx%d ≠ 画布 %dx%d' % (w, h, ew, eh))
    try:
        from PIL import Image
        import numpy as np
    except ImportError:
        res['ok'] = not res['errors']
        return res
    a = np.asarray(Image.open(path).convert('RGB')).astype(int)
    diff = np.abs(a - np.array(PAGE_BG)).max(axis=2)
    ink = diff > 6
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    if len(rows):
        res['ink_bbox'] = {'top': int(rows[0]), 'bottom': int(rows[-1]),
                           'left': int(cols[0]), 'right': int(cols[-1])}
    # 页脚底色带：取底部 8~3 行（避开最底部 1px 边框），要求大部分像素就是页脚底色
    if h > 20:
        band = a[h - 8:h - 3]
        foot_bg = float((np.abs(band - np.array(FOOT_BG)).max(axis=2) <= 3).mean())
        res['footer_bg_ratio'] = round(foot_bg, 4)
        if foot_bg < 0.5:
            res['errors'].append('底部检测不到页脚底色带（页脚缺失 = 内容被裁到下一页）')
    res['ok'] = not res['errors']
    return res


def main():
    ap = argparse.ArgumentParser(description='竖版知识卡片长图引擎')
    ap.add_argument('--cards', required=True, help='cards.json（唯一事实源）')
    ap.add_argument('--outdir', required=True)
    ap.add_argument('--only', help='只生成指定卡 id（逗号分隔）')
    ap.add_argument('--ratio', default=None, choices=sorted(RATIOS), help='画布比例，默认 3:4')
    ap.add_argument('--dpi', type=int, default=DEFAULT_DPI)
    ap.add_argument('--group', default=None, help='卡组名（显示在角标，默认取 JSON group）')
    ap.add_argument('--footer', default=None, help='页脚来源文字（默认取 JSON footer）')
    ap.add_argument('--check-only', action='store_true', help='只校验已有产物，不重新生成')
    args = ap.parse_args()

    with open(args.cards, encoding='utf-8') as f:
        data = json.load(f)
    if isinstance(data, dict):
        cards = data.get('cards', [])
        ratio = args.ratio or data.get('ratio') or DEFAULT_RATIO
        group = args.group if args.group is not None else (data.get('group') or '')
        footer = args.footer if args.footer is not None else (data.get('footer') or '')
    else:
        cards = data
        ratio = args.ratio or DEFAULT_RATIO
        group, footer = args.group or '', args.footer or ''

    if ratio not in RATIOS:
        print(f'未知比例 {ratio}，可用：{", ".join(sorted(RATIOS))}', file=sys.stderr)
        return 1

    os.makedirs(args.outdir, exist_ok=True)
    only = set(args.only.split(',')) if args.only else None
    report, bad = [], 0

    if not args.check_only:
        for c in cards:
            if only and c['id'] not in only:
                continue
            c.setdefault('total', len(cards))
            png, k, h, pages, warn = gen_one(c, args.outdir, ratio, args.dpi, group, footer)
            row = {'id': c['id'], 'file': os.path.basename(png), 'k': round(k, 3), 'pages': pages}
            if warn:
                row['warnings'] = [warn]
                print(f'  [WARN] {c["id"]}: {warn}', file=sys.stderr)
            print(f'OK {png}  (k={k:.2f})')
            report.append(row)

    # 校验（默认全量：生成完的 + 已存在的）
    # check-only 时保留上一轮写下的 k / warnings，别把有用信息覆盖掉
    prev_path = os.path.join(args.outdir, '_check.json')
    prev = {}
    if os.path.exists(prev_path):
        try:
            prev = {i.get('file'): i for i in json.load(open(prev_path, encoding='utf-8')).get('items', [])}
        except Exception:
            prev = {}
    checks = []
    for c in cards:
        if only and c['id'] not in only:
            continue
        idx = c.get('index')
        stem = c.get('filename', c['id'])
        name = f'{idx:02d}_{stem}.png' if isinstance(idx, int) else f'{stem}.png'
        p = os.path.join(args.outdir, name)
        if not os.path.exists(p):
            checks.append({'file': name, 'ok': False, 'errors': ['产物缺失']})
            bad += 1
            continue
        by_id = next((x for x in report if x['file'] == name), None)
        old = prev.get(name, {})
        # 已知页数（本轮生成 or 上一轮记录）→ 直接作为硬判据；未知则靠页脚底色带判定
        known_pages = None
        for src in (by_id, old):
            if src and src.get('pages') is not None:
                known_pages = src['pages']
                break
        r = check_png(p, ratio, args.dpi, pages=known_pages)
        for key in ('k',):
            if by_id and by_id.get(key) is not None:
                r[key] = by_id[key]
            elif old.get(key) is not None:
                r[key] = old[key]
        extra = (by_id or old).get('warnings') or []
        r['warnings'] = list(r.get('warnings', [])) + list(extra)
        if not r['ok']:
            bad += 1
            print(f'  [FAIL] {r["file"]}: {"; ".join(r["errors"])}', file=sys.stderr)
        checks.append(r)

    with open(os.path.join(args.outdir, '_check.json'), 'w', encoding='utf-8') as f:
        json.dump({'ratio': ratio, 'dpi': args.dpi, 'total': len(checks),
                   'failed': bad, 'items': checks}, f, ensure_ascii=False, indent=2)

    print(f'校验：{len(checks) - bad}/{len(checks)} 通过（ratio={ratio}, dpi={args.dpi}）'
          f' -> {os.path.join(args.outdir, "_check.json")}')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
