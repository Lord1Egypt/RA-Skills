#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
theme_inject.py —— 把一份 BII 个股简报 HTML 重定向为「贝莱德智库风格」，并注入结构装饰。

设计要点（为什么这么写）：

1) **只做两件事**：全局色板重定向 + 结构装饰注入。
   不改文字、不改字号、不改行高。
   原因：BII 简报的 22 页版式是像素级调平的，任何字号增量都会让某页溢出到第二页，
   破坏硬门「PDF 页数 == section 数」。

2) **装饰注入用定点正则，不用 bs4 全量解析**。
   416KB 的 HTML 里内联了 205KB 的 Chart.js；全量解析再序列化有改写 <script>、
   重排属性、转义字符的风险，会静默破坏图表。定点正则可保证其余字节不变。

3) **三条硬断言**（不满足直接非零退出，不产出半成品）：
   - section 数 == 期望页数
   - 每个 .runfoot / .cv-foot 恰好 2 个 <span>（否则 br-code 会插错位置）
   - 注入后无禁用色残留

用法：
  python3 theme_inject.py IN.html OUT.html \
      [--pages 22] [--brand-line "BII · EQUITY NOTE"] [--source-code BII-NZ-20260917-SZ] \
      [--report report.json] [--no-style-note]
"""
import argparse
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOKENS_PATH = os.path.normpath(os.path.join(HERE, '..', 'assets', 'br_tokens.json'))
CSS_PATH = os.path.normpath(os.path.join(HERE, '..', 'assets', 'blackrock-theme.css'))

STYLE_ID = 'br-theme'


# ──────────────────────────────────────────────────────────────────────────────
# 第一层：全局色板重定向
# ──────────────────────────────────────────────────────────────────────────────
def build_hex_sub(remap):
    """单趟正则替换 —— 单趟天然不会级联（目标色即使又是源色也不会被二次改写）。"""
    pat = re.compile(r'#([0-9A-Fa-f]{6})\b')

    def _sub(m):
        key = '#' + m.group(1).upper()
        return remap.get(key, m.group(0))

    return (lambda s: pat.sub(_sub, s)), pat


def retarget_palette(html, tokens):
    remap = {k.upper(): v for k, v in tokens['palette_remap'].items()
             if not k.startswith('_')}
    sub, pat = build_hex_sub(remap)
    before = pat.findall(html)
    html2 = sub(html)
    after = pat.findall(html2)

    def norm(xs):
        c = {}
        for x in xs:
            c['#' + x.upper()] = c.get('#' + x.upper(), 0) + 1
        return c

    b, a = norm(before), norm(after)
    # 逐条统计「本次真正打掉的源色」
    hits = {}
    for src in remap:
        n = b.get(src, 0)
        if n:
            hits[src] = n

    # rgba 重定向
    rgba_hits = {}
    for old, new in tokens.get('rgba_remap', {}).items():
        if old.startswith('_'):
            continue
        nums = re.findall(r'\d+', old)
        flex = r'rgba\(\s*' + r'\s*,\s*'.join(re.escape(n) for n in nums) + r'\s*,'
        rx = re.compile(flex, re.I)
        cnt = len(rx.findall(html2))
        if cnt:
            rgba_hits[old] = cnt
            html2 = rx.sub(new, html2)

    return html2, hits, rgba_hits, a


# ──────────────────────────────────────────────────────────────────────────────
# 第二层：结构装饰注入
# ──────────────────────────────────────────────────────────────────────────────
SECTION_OPEN = re.compile(r'<section\b[^>]*>')


def _clean_tab(text):
    t = re.sub(r'<[^>]+>', '', text)
    t = t.replace('&nbsp;', ' ').replace('\u00a0', ' ')
    return re.sub(r'\s+', ' ', t).strip()


def inject_section_tabs(html, cover_tab):
    """给每个 <section class="page|cover"> 补 data-br-tab（书签文案取自页眉 .rh-l）。"""
    tabs = []
    out = []
    pos = 0
    for i, m in enumerate(SECTION_OPEN.finditer(html)):
        cls = re.search(r'class="([^"]*)"', m.group(0))
        cls = cls.group(1) if cls else ''
        is_cover = 'cover' in cls.split()
        if not (is_cover or 'page' in cls.split()):
            continue
        end = html.find('</section>', m.end())
        if end < 0:
            raise SystemExit('!! 有未闭合的 <section>')
        body = html[m.end():end]
        if is_cover:
            label = cover_tab
        else:
            rh = re.search(r'<span class="rh-l">(.*?)</span>', body, re.S)
            label = _clean_tab(rh.group(1)) if rh else ''
        if not label:
            raise SystemExit('!! 第 %d 个 section 取不到书签文案' % (i + 1))
        tag = m.group(0)
        # 插到 class 属性后面，保持属性顺序可读
        newtag = re.sub(r'(class="[^"]*")', r'\1 data-br-tab="%s"' % label.replace('"', '&quot;'),
                        tag, count=1)
        out.append(html[pos:m.start()])
        out.append(newtag)
        pos = m.end()
        tabs.append({'kind': 'cover' if is_cover else 'page', 'tab': label})
    out.append(html[pos:])
    return ''.join(out), tabs


FOOT_BLOCK = re.compile(r'<div class="(runfoot|cv-foot)">(.*?)</div>', re.S)


def inject_footer_code(html, source_code, total_pages, style_note=None):
    """给每个页脚补第三段「文件编号」；封面额外补一行版式来源声明。"""
    stats = {'footers': 0, 'cover_notes': 0}

    def _repl(m):
        kind, inner = m.group(1), m.group(2)
        n_span = inner.count('<span')
        if n_span != 2:
            raise SystemExit(
                '!! .%s 里有 %d 个 <span>（期望 2）—— br-code 会插错位置。'
                '请检查源 HTML 的页脚结构是否被改动。' % (kind, n_span))
        code = ('<span class="br-code">文件编号 %s · 共 %d 页</span>'
                % (source_code, total_pages))
        if kind == 'cv-foot' and style_note:
            # 追加到 inner 末尾（br-code 之前）：声明 absolute 出流，不占 grid 轨道；
            # 也不能插在两个 span 中间——那会让 nth-child(2) 失配，右件掉到第二行
            # （22 页稿有封面余量掩盖了此 bug，10 页卡线稿实测爆页 +4.3px）
            inner = inner + '<span class="br-style-note">%s</span>' % style_note
            stats['cover_notes'] += 1
        stats['footers'] += 1
        return '<div class="%s">%s%s</div>' % (kind, inner, code)

    return FOOT_BLOCK.sub(_repl, html), stats


CV_BRAND = re.compile(r'(<div class="cv-brand">)([^<]*)(<span>)(.*?)(</span>)', re.S)


def retarget_cover_brand(html, brand_line, prefix='贝莱德智库风格 · '):
    m = CV_BRAND.search(html)
    if not m:
        return html, None
    old_line, old_sub = m.group(2).strip(), m.group(4).strip()
    sub = old_sub if old_sub.startswith('贝莱德智库风格') else prefix + old_sub
    new = '%s%s%s%s%s' % (m.group(1), brand_line, m.group(3), sub, m.group(5))
    return html[:m.start()] + new + html[m.end():], {'brand_line': [old_line, brand_line],
                                                     'brand_sub': [old_sub, sub]}


def inject_theme_css(html, css, tokens):
    """把主题层注入 </head> 之前；并把令牌变量摊平进 :root（便于体检脚本核对）。"""
    if 'id="%s"' % STYLE_ID in html:
        html = re.sub(r'<style id="%s">.*?</style>' % STYLE_ID, '', html, flags=re.S)
    block = '<style id="%s">\n%s\n</style>\n' % (STYLE_ID, css)
    if '</head>' not in html:
        raise SystemExit('!! 源 HTML 里找不到 </head>')
    return html.replace('</head>', block + '</head>', 1)


# ──────────────────────────────────────────────────────────────────────────────
# 主流程
# ──────────────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(description='BII 简报 → 贝莱德智库风格 HTML')
    ap.add_argument('src')
    ap.add_argument('dst')
    ap.add_argument('--pages', type=int, default=None,
                    help='期望页数（section 数）；缺省则取 tokens.geometry.expected_pages')
    ap.add_argument('--brand-line', default=None)
    ap.add_argument('--source-code', default=None)
    ap.add_argument('--report', default=None, help='把注入报告写成 JSON')
    ap.add_argument('--no-style-note', action='store_true')
    args = ap.parse_args()

    tokens = json.load(io.open(TOKENS_PATH, encoding='utf-8'))
    css = io.open(CSS_PATH, encoding='utf-8').read()
    fm = tokens['front_matter']

    expected = args.pages or tokens['geometry']['expected_pages']
    brand_line = args.brand_line or fm['brand_line']

    src = io.open(args.src, encoding='utf-8').read()
    orig_len = len(src)

    # ---- 校验源件形态 -------------------------------------------------------
    def _sec_class(tag):
        c = re.search(r'class="([^"]*)"', tag)
        return c.group(1).split() if c else []

    sec_classes = [c for c in (_sec_class(m.group(0))
                               for m in SECTION_OPEN.finditer(src))
                   if 'cover' in c or 'page' in c]
    sec_classes = [('cover' if 'cover' in c else 'page') for c in sec_classes]
    if len(sec_classes) != expected:
        raise SystemExit('!! section 数 = %d，期望 %d。源 HTML 结构不符，先核对。'
                         % (len(sec_classes), expected))

    # ---- 自动推导文件编号 / 报告编号 ---------------------------------------
    report_no = None
    m = re.search(r'报告编号\s*[:：]?\s*([A-Za-z0-9][A-Za-z0-9\-_]{2,})', src)
    if m:
        report_no = m.group(1)
    source_code = args.source_code or ('BII-%s' % report_no if report_no
                                       else 'BII-UNSPECIFIED')

    # ---- 第一层：色板 -------------------------------------------------------
    html, hex_hits, rgba_hits, survived = retarget_palette(src, tokens)

    # ---- 第二层：装饰 -------------------------------------------------------
    html, tabs = inject_section_tabs(html, brand_line)
    html, foot_stats = inject_footer_code(
        html, source_code, expected,
        style_note=None if args.no_style_note else fm['style_note'])
    html, brand_delta = retarget_cover_brand(html, brand_line)
    html = inject_theme_css(html, css, tokens)

    # ---- 断言：禁用色残留 ---------------------------------------------------
    forbidden = []
    for bad in tokens['forbidden_after_inject']:
        n = len(re.findall(re.escape(bad), html, re.I))
        if n:
            forbidden.append({'color': bad, 'count': n})
    if forbidden:
        raise SystemExit('!! 注入后仍有禁用色残留：%s' % forbidden)

    # ---- 断言：必备结构 -----------------------------------------------------
    missing = [k for k in tokens['required_structures'] if k not in html]
    if missing:
        raise SystemExit('!! 注入后缺少必备结构：%s' % missing)

    io.open(args.dst, 'w', encoding='utf-8').write(html)

    report = {
        'src': args.src,
        'dst': args.dst,
        'src_bytes': orig_len,
        'out_bytes': len(html),
        'sections': len(sec_classes),
        'expected_pages': expected,
        'report_no': report_no,
        'source_code': source_code,
        'brand_line': brand_line,
        'cover_brand_delta': brand_delta,
        'palette_hits': hex_hits,
        'rgba_hits': rgba_hits,
        'tabs': tabs,
        'footers': foot_stats,
        'forbidden_residual': forbidden,
        'missing_structures': missing,
    }
    if args.report:
        io.open(args.report, 'w', encoding='utf-8').write(
            json.dumps(report, ensure_ascii=False, indent=2))

    print('✓ 注入完成：%s' % args.dst)
    print('  section %d / 期望 %d' % (len(sec_classes), expected))
    print('  色板重定向 %d 类（共 %d 处），rgba %d 类'
          % (len(hex_hits), sum(hex_hits.values()), len(rgba_hits)))
    print('  书签 %d 个，页脚 %d 个，封面风格声明 %d 处'
          % (len(tabs), foot_stats['footers'], foot_stats['cover_notes']))
    print('  体积 %d → %d 字节（+%d，主题层）'
          % (orig_len, len(html), len(html) - orig_len))
    return 0


if __name__ == '__main__':
    sys.exit(main())
