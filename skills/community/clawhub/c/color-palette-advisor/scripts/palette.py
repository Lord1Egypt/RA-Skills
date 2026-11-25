#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
color-palette-advisor 计算引擎

用 OKLCH 感知均匀色彩空间生成完整色板, 并做 WCAG 对比度实测校验。
不要用 HSL 线性混合 (mix white/black), 那个色阶感知不均匀。

用法:
    python3 palette.py --base "#0F62FE" --name "智慧园区"
    python3 palette.py --base "#0F62FE" --html
    python3 palette.py --base "#0F62FE" --export css   --out tokens.css
    python3 palette.py --base "#0F62FE" --export figma --out tokens.json
    python3 palette.py --base "#0F62FE" --export md    --out palette.md
"""
import argparse
import json
import math
import os
import sys

# ---------------------------------------------------------------- 色彩转换


def hex2rgb(h):
    h = h.lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb2hex(rgb):
    def f(x):
        return max(0, min(255, round(x)))
    return '#%02X%02X%02X' % (f(rgb[0]), f(rgb[1]), f(rgb[2]))


def srgb2lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def lin2srgb(c):
    c = max(0.0, min(1.0, c))
    v = 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055
    return v * 255.0


def rgb2oklch(rgb):
    r, g, b = [srgb2lin(x) for x in rgb]
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = [x ** (1 / 3) if x > 0 else -((-x) ** (1 / 3)) for x in (l, m, s)]
    L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    bb = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_
    C = math.hypot(a, bb)
    H = math.degrees(math.atan2(bb, a)) % 360
    return L, C, H


def oklch2rgb(L, C, H):
    a = C * math.cos(math.radians(H))
    bb = C * math.sin(math.radians(H))
    l_ = L + 0.3963377774 * a + 0.2158037573 * bb
    m_ = L - 0.1055613458 * a - 0.0638541728 * bb
    s_ = L - 0.0894841775 * a - 1.2914855480 * bb
    l, m, s = [x ** 3 for x in (l_, m_, s_)]
    r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    b = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
    return (lin2srgb(r), lin2srgb(g), lin2srgb(b))


def in_gamut(rgb, tol=0.6):
    return all(-tol <= x <= 255 + tol for x in rgb)


def clamp_to_gamut(L, C, H, iters=24):
    """超出 sRGB 色域时二分法降饱和"""
    rgb = oklch2rgb(L, C, H)
    if in_gamut(rgb):
        return rgb
    lo, hi = 0.0, C
    for _ in range(iters):
        mid = (lo + hi) / 2.0
        if in_gamut(oklch2rgb(L, mid, H)):
            lo = mid
        else:
            hi = mid
    return oklch2rgb(L, lo, H)


def oklch_hex(L, C, H):
    return rgb2hex(clamp_to_gamut(L, C, H))


# ---------------------------------------------------------------- 对比度


def rel_lum(rgb):
    r, g, b = [srgb2lin(x) for x in rgb]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(fg, bg):
    L1, L2 = rel_lum(hex2rgb(fg)), rel_lum(hex2rgb(bg))
    a, b = max(L1, L2), min(L1, L2)
    return (a + 0.05) / (b + 0.05)


def best_text(hexv):
    """底色配白字还是黑字"""
    w = contrast('#FFFFFF', hexv)
    k = contrast('#101418', hexv)
    return ('#FFFFFF', w) if w >= k else ('#101418', k)


# ---------------------------------------------------------------- 色阶


SCALE_L = {
    '050': 0.972, '100': 0.936, '200': 0.876, '300': 0.786, '400': 0.686,
    '500': None,
    '600': -0.085, '700': -0.155, '800': -0.215, '900': -0.275,
}
SCALE_C = {
    '050': 0.28, '100': 0.42, '200': 0.62, '300': 0.82, '400': 1.00,
    '500': 1.00, '600': 1.00, '700': 0.92, '800': 0.88, '900': 0.80,
}
SCALE_ORDER = ['050', '100', '200', '300', '400', '500', '600', '700', '800', '900']
SCALE_USAGE = {
    '050': '最浅背景 / hover 底', '100': '选中背景 / 徽标底', '200': '图标填充 / 进度条',
    '300': '链接 / 描边 / 深底高亮', '400': '次级按钮 / 深底链接',
    '500': '主按钮 / 选中态 / 品牌', '600': '按压态 / hover',
    '700': '重要强调 / 浅底品牌字', '800': '深底 / 品牌文字', '900': '品牌深色 / 页脚',
}


def build_scale(base_hex):
    L, C, H = rgb2oklch(hex2rgb(base_hex))
    out = {}
    for k in SCALE_ORDER:
        t = SCALE_L[k]
        if t is None:
            lt = L
        elif t > 0.5:
            lt = t
        else:
            lt = max(0.02, L + t)
        out[k] = oklch_hex(lt, C * SCALE_C[k], H)
    return out, L, C, H


# ---------------------------------------------------------------- 中性色


NEUTRAL_L = {
    '000': 1.000, '050': 0.975, '100': 0.945, '200': 0.905, '300': 0.825,
    '400': 0.695, '500': 0.545, '600': 0.445, '700': 0.355, '800': 0.235, '900': 0.165,
}
NEUTRAL_C = {
    '000': 0.000, '050': 0.008, '100': 0.010, '200': 0.012, '300': 0.015,
    '400': 0.020, '500': 0.025, '600': 0.030, '700': 0.035, '800': 0.040, '900': 0.045,
}
NEUTRAL_ORDER = ['000', '050', '100', '200', '300', '400', '500', '600', '700', '800', '900']
NEUTRAL_USAGE = {
    '000': '卡片 / 表面', '050': '页面背景', '100': 'hover / 浅底', '200': '细分隔线',
    '300': '边框', '400': '弱化图标', '500': '占位 / 禁用文字', '600': '弱化正文',
    '700': '次级文字', '800': '弱化标题', '900': '主文字',
}


def build_neutral(hue):
    return {k: oklch_hex(NEUTRAL_L[k], NEUTRAL_C[k], hue) for k in NEUTRAL_ORDER}


# ---------------------------------------------------------------- 语义色


SEM_BASE = {'success': '#16A34A', 'warning': '#E08C00', 'error': '#DC2626', 'info': '#0284C7'}
SEM_DARK = {'success': '#4ADE80', 'warning': '#FBBF24', 'error': '#F87171', 'info': '#60A5FA'}
SEM_CN = {'success': '成功', 'warning': '警告', 'error': '错误', 'info': '信息'}
DARK_BG = '#0B1118'


def text_safe(hexv, bg='#FFFFFF', target=4.5, steps=120, step=0.004):
    """保持色相, 逐步降明度直到达到目标对比度"""
    if contrast(hexv, bg) >= target:
        return hexv
    L, C, H = rgb2oklch(hex2rgb(hexv))
    for i in range(steps):
        lt = L - i * step
        if lt <= 0.05:
            break
        cand = oklch_hex(lt, C * 0.92, H)
        if contrast(cand, bg) >= target:
            return cand
    return oklch_hex(0.20, C * 0.9, H)


def build_semantic():
    out = {}
    for k, v in SEM_BASE.items():
        tv = text_safe(v, '#FFFFFF', 4.5)
        out[k] = {
            'cn': SEM_CN[k],
            'base': v,
            'base_contrast': round(contrast(v, '#FFFFFF'), 2),
            'text': tv,
            'text_contrast': round(contrast(tv, '#FFFFFF'), 2),
            'large': text_safe(v, '#FFFFFF', 3.0),
            'dark': SEM_DARK[k],
            'dark_contrast': round(contrast(SEM_DARK[k], DARK_BG), 2),
        }
    return out


# ---------------------------------------------------------------- 组装色板


def hue_shift(base_hex, deg, c_scale=1.0):
    L, C, H = rgb2oklch(hex2rgb(base_hex))
    return oklch_hex(L, C * c_scale, (H + deg) % 360)


def build_palette(base_hex, secondary_mode='analogous', with_accent=True, sec_deg=None, acc_deg=None):
    primary, L, C, H = build_scale(base_hex)
    sd = sec_deg if sec_deg is not None else (180.0 if secondary_mode == 'split' else 52.0)
    secondary_base = hue_shift(base_hex, sd, 0.95)
    secondary, _, _, _ = build_scale(secondary_base)

    if with_accent:
        ad = acc_deg if acc_deg is not None else 165.0
        accent_base = hue_shift(base_hex, ad, 1.12)
        accent, _, _, _ = build_scale(accent_base)
    else:
        accent_base, accent = None, None

    return {
        'base': base_hex.upper(),
        'base_oklch': {'L': round(L, 3), 'C': round(C, 3), 'H': round(H, 1)},
        'secondary_mode': secondary_mode,
        'secondary_base': secondary_base,
        'secondary_deg': sd,
        'accent_base': accent_base,
        'primary': primary,
        'secondary': secondary,
        'accent': accent,
        'neutral': build_neutral(H),
        'semantic': build_semantic(),
    }


# ---------------------------------------------------------------- 校验


def run_checks(p):
    pr, nu = p['primary'], p['neutral']
    checks = []

    def add(label, fg, bg, min_ratio, note=''):
        c = contrast(fg, bg)
        checks.append({'label': label, 'fg': fg, 'bg': bg, 'ratio': round(c, 2),
                       'min': min_ratio, 'pass': c >= min_ratio, 'note': note})

    add('白字 on primary-500', '#FFFFFF', pr['500'], 4.5, '主按钮')
    add('白字 on primary-600', '#FFFFFF', pr['600'], 4.5, 'hover/按压')
    add('白字 on primary-700', '#FFFFFF', pr['700'], 4.5, '重要强调')
    add('primary-500 大字/图标 on 白底', pr['500'], '#FFFFFF', 3.0, 'UI 组件')
    add('primary-700 文字 on 白底', pr['700'], '#FFFFFF', 4.5, '浅底品牌字')
    add('primary-100 底 + primary-700 字', pr['700'], pr['100'], 4.5, '标签')
    add('neutral-900 on 白底', nu['900'], '#FFFFFF', 4.5, '主文字')
    add('neutral-700 on 白底', nu['700'], '#FFFFFF', 4.5, '次级文字')
    add('neutral-500 on 白底', nu['500'], '#FFFFFF', 3.0, '占位/禁用')
    add('neutral-900 on neutral-050', nu['900'], nu['050'], 4.5, '页面正文')

    for k, v in p['semantic'].items():
        add(f"{v['cn']} 小字(text) on 白底", v['text'], '#FFFFFF', 4.5, '状态文字')
        add(f"{v['cn']} 图标/大字(base) on 白底", v['base'], '#FFFFFF', 3.0, 'UI 组件')
        add(f"{v['cn']} 深色模式 on 深底", v['dark'], DARK_BG, 4.5, 'dark')

    add('primary-300 on 深底', pr['300'], DARK_BG, 4.5, '大屏高亮')
    add('primary-400 on 深底', pr['400'], DARK_BG, 4.5, '大屏链接')
    add('#E5E7EB 深色主文字 on 深底', '#E5E7EB', DARK_BG, 4.5, 'dark 正文')
    return checks


# ---------------------------------------------------------------- HTML 预览


def render_html(p, name, checks, out_path):
    pr, sec, acc, nu, sem = p['primary'], p['secondary'], p['accent'], p['neutral'], p['semantic']

    def chips(group, order, prefix=''):
        cells = ''
        for k in order:
            v = group[k]
            txt, _ = best_text(v)
            cells += (f'<div class="sw"><div class="chip" style="background:{v};color:{txt}">'
                      f'{v}</div><div class="lbl">{prefix}{k}</div></div>')
        return cells

    sem_cells = ''
    for k, v in sem.items():
        sem_cells += (f'<div class="sw"><div class="chip" style="background:{v["base"]};color:#fff">'
                      f'{v["base"]}</div><div class="lbl">{v["cn"]} base {v["base_contrast"]}:1</div>'
                      f'<div class="chip sm" style="background:{v["text"]};color:#fff">{v["text"]}'
                      f'<br><span class="tiny">小字安全 {v["text_contrast"]}:1</span></div>'
                      f'<div class="chip sm" style="background:{DARK_BG};color:{v["dark"]}">{v["dark"]}'
                      f'<br><span class="tiny">深色 {v["dark_contrast"]}:1</span></div></div>')

    rows = ''
    for c in checks:
        icon = '✅' if c['pass'] else '❌'
        rows += (f'<tr class="{"" if c["pass"] else "bad"}"><td>{c["label"]}</td>'
                 f'<td><span class="dot" style="background:{c["fg"]}"></span>{c["fg"]}</td>'
                 f'<td><span class="dot" style="background:{c["bg"]}"></span>{c["bg"]}</td>'
                 f'<td><b>{c["ratio"]}:1</b></td><td>≥{c["min"]}</td><td>{icon}</td>'
                 f'<td class="nt">{c["note"]}</td></tr>')

    npass = sum(1 for c in checks if c['pass'])
    nfail = len(checks) - npass
    secname = '类似色' if p['secondary_mode'] == 'analogous' else '分裂互补'

    html = f'''<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>配色方案 — {name}</title>
<style>
*{{box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif;
background:{nu['050']};color:{nu['900']};margin:0;padding:28px}}
h1{{font-size:22px;margin:0 0 6px}}
h2{{font-size:14px;margin:0 0 12px;color:{nu['700']}}}
.sub{{color:{nu['500']};font-size:13px;margin-bottom:10px;line-height:1.7}}
.badge{{display:inline-block;background:{pr['100']};color:{pr['700']};border-radius:20px;
padding:3px 11px;font-size:11px;font-weight:600;margin:2px 6px 2px 0}}
.panel{{background:{nu['000']};border-radius:14px;padding:18px;margin-bottom:14px;
box-shadow:0 1px 3px rgba(16,20,24,.07)}}
.row{{display:flex;flex-wrap:wrap;gap:8px}}
.sw{{display:flex;flex-direction:column;min-width:98px;flex:1}}
.chip{{border-radius:10px;padding:15px 8px;text-align:center;font-size:12px;font-weight:600;
font-family:ui-monospace,Menlo,monospace;box-shadow:inset 0 0 0 1px rgba(16,20,24,.07)}}
.chip.sm{{margin-top:6px;padding:9px 6px;font-size:11px}}
.tiny{{font-size:9px;opacity:.8}}
.lbl{{font-size:10px;color:{nu['500']};text-align:center;margin-top:5px}}
.demo{{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-top:14px}}
.btn{{border-radius:9px;padding:10px 20px;font-size:13px;font-weight:600;border:none}}
.tag{{border-radius:6px;padding:4px 10px;font-size:12px;font-weight:600}}
.dark{{background:{DARK_BG};border-radius:14px;padding:18px;margin-bottom:14px}}
.dark h2{{color:#E5E7EB}} .dark .lbl{{color:#8B96A3}}
table{{width:100%;border-collapse:collapse;font-size:12px}}
th,td{{padding:8px 10px;text-align:left;border-bottom:1px solid {nu['200']}}}
th{{background:{nu['050']};font-size:11px;color:{nu['600']};letter-spacing:.04em}}
.dot{{display:inline-block;width:11px;height:11px;border-radius:3px;margin-right:6px;
vertical-align:middle;box-shadow:inset 0 0 0 1px rgba(16,20,24,.15)}}
td.nt{{color:{nu['500']}}}
tr.bad{{background:#FEF2F2}}
.guide{{font-size:12.5px;line-height:1.9;color:{nu['700']};margin-top:10px}}
.guide b{{color:{nu['900']}}}
code{{background:{nu['100']};padding:2px 6px;border-radius:5px;font-size:11.5px}}
.bar{{display:flex;height:28px;border-radius:8px;overflow:hidden;margin:6px 0}}
.bar div{{display:flex;align-items:center;justify-content:center;color:#fff;font-size:10px;font-weight:600}}
</style></head><body>

<h1>🎨 配色方案 — {name}</h1>
<div class="sub">基准色 <code>{p['base']}</code> · OKLCH L={p['base_oklch']['L']} / C={p['base_oklch']['C']} / H={p['base_oklch']['H']}°<br>
<span class="badge">OKLCH 感知均匀色阶</span><span class="badge">WCAG 2.1 AA 实测</span>
<span class="badge">辅助色 {secname} +{int(p['secondary_deg'])}°</span><span class="badge">含深色模式</span></div>

<div class="panel"><h2>主色 Primary</h2>
<div class="row">{chips(pr, SCALE_ORDER, 'primary-')}</div>
<div class="demo">
<div class="btn" style="background:{pr['500']};color:#fff">主按钮 500</div>
<div class="btn" style="background:{pr['600']};color:#fff">Hover 600</div>
<div class="btn" style="background:{pr['700']};color:#fff">按压 700</div>
<div class="tag" style="background:{pr['100']};color:{pr['700']}">标签 100/700</div>
<div class="btn" style="background:{nu['000']};color:{pr['600']};box-shadow:inset 0 0 0 1.5px {pr['600']}">次级按钮</div>
</div></div>

<div class="panel"><h2>辅助色 Secondary · {secname} (H+{int(p['secondary_deg'])}°, base {sec['500']})</h2>
<div class="row">{chips(sec, SCALE_ORDER, 'secondary-')}</div></div>
'''

    if acc:
        html += f'''<div class="panel"><h2>强调色 Accent (base {acc['500']})</h2>
<div class="row">{chips(acc, ['100','200','300','400','500','600','700','900'], 'accent-')}</div></div>
'''

    html += f'''<div class="panel"><h2>中性色 Neutral (带主色色相 H={p['base_oklch']['H']}°)</h2>
<div class="row">{chips(nu, NEUTRAL_ORDER, 'neutral-')}</div>
<div class="demo"><div style="background:{nu['000']};border:1px solid {nu['300']};border-radius:10px;padding:14px 18px;max-width:360px">
<div style="font-size:15px;font-weight:600;color:{nu['900']};margin-bottom:4px">卡片标题 900</div>
<div style="font-size:13px;color:{nu['700']};margin-bottom:8px">次级说明文字 700</div>
<div style="font-size:12px;color:{nu['500']}">占位文字 500</div>
</div></div></div>

<div class="panel"><h2>语义色 Semantic (基准 / 小字安全 / 深色模式 三版)</h2>
<div class="row">{sem_cells}</div></div>

<div class="dark"><h2>🌙 深色模式 (大屏 / dark mode)</h2><div class="row">
<div class="sw"><div class="chip" style="background:{DARK_BG};color:{pr['300']}">{pr['300']}</div><div class="lbl">主色300 数据高亮</div></div>
<div class="sw"><div class="chip" style="background:{DARK_BG};color:{pr['400']}">{pr['400']}</div><div class="lbl">主色400 链接线</div></div>
''' + (f'''<div class="sw"><div class="chip" style="background:{DARK_BG};color:{acc['400']}">{acc['400']}</div><div class="lbl">强调400 告警</div></div>
''' if acc else '') + f'''<div class="sw"><div class="chip" style="background:{DARK_BG};color:{sem['success']['dark']}">{sem['success']['dark']}</div><div class="lbl">上涨/成功</div></div>
<div class="sw"><div class="chip" style="background:{DARK_BG};color:{sem['error']['dark']}">{sem['error']['dark']}</div><div class="lbl">下跌/错误</div></div>
</div></div>

<div class="panel"><h2>🎯 对比度校验 (脚本实测, 非目测)</h2>
<div style="font-size:13px;margin-bottom:10px">共 {len(checks)} 项 · <b style="color:#16A34A">{npass} 通过</b> ·
{'<b style="color:#DC2626">%d 未达标</b>' % nfail if nfail else '<b style="color:#16A34A">全部达标</b>'}</div>
<table><thead><tr><th>组合</th><th>前景</th><th>背景</th><th>实测</th><th>要求</th><th></th><th>用途</th></tr></thead>
<tbody>{rows}</tbody></table></div>

<div class="panel"><h2>📐 使用比例与规范</h2>
<div class="bar">
<div style="flex:60;background:{pr['500']}">主色 60%</div>
<div style="flex:18;background:{sec['500']}">辅助 18%</div>
<div style="flex:12;background:{nu['300']};color:{nu['900']}">中性 12%</div>
<div style="flex:6;background:{sem['info']}">语义 6%</div>
''' + (f'''<div style="flex:4;background:{acc['500']}">强调 4%</div>
''' if acc else '') + f'''</div>
<div class="guide">
<b>层级原则</b>：主色 60%（品牌+主操作）· 辅助 18%（次操作/链接）· 中性 12%（文字/背景/边框）· 语义 6%（仅状态反馈）· 强调 ≤4%（促销/榜单）<br>
<b>关键规则</b>：<br>
• 主按钮 <code>primary-500</code> + 白字；不足 4.5:1 时改用 <code>600</code>/<code>700</code><br>
• 语义色做<b>小字</b>必须用 text 版；base 版仅限图标/大按钮/标签底<br>
• 深色模式主色调亮到 <code>300</code>/<code>400</code>，背景用 <code>{DARK_BG}</code> 而非纯黑，文字用 <code>#E5E7EB</code> 而非纯白<br>
• 大屏远距离阅读建议正文提到 ≥7:1 (AAA)<br>
• 标签 = <code>primary-100</code> 底 + <code>primary-700</code> 字；禁用态 = <code>neutral-200</code> 底 + <code>neutral-500</code> 字
</div></div>

<div class="panel" style="font-size:11px;color:{nu['500']};text-align:center">
由 color-palette-advisor 生成 · OKLCH 感知均匀算法 · 对比度为脚本实测值</div>
</body></html>'''

    d = os.path.dirname(out_path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return out_path


# ---------------------------------------------------------------- token 导出


def all_tokens(p):
    t = []
    for g in ('primary', 'secondary', 'accent', 'neutral'):
        if not p.get(g):
            continue
        for k, v in p[g].items():
            t.append((f'--{g}-{k}', v))
    for k, v in p['semantic'].items():
        t.append((f'--{k}', v['base']))
        t.append((f'--{k}-text', v['text']))
        t.append((f'--{k}-dark', v['dark']))
    return t


def export_css(p, name):
    lines = [f'/* 配色 token — {name} · by color-palette-advisor (OKLCH) */', ':root {']
    for k, v in all_tokens(p):
        lines.append(f'  {k}: {v};')
    lines.append('}')
    return '\n'.join(lines)


def export_figma(p, name):
    def grp(g):
        return {k: {'value': v, 'type': 'color'} for k, v in p[g].items()} if p.get(g) else None
    sem = {}
    for k, v in p['semantic'].items():
        sem[k] = {'value': v['base'], 'type': 'color'}
        sem[f'{k}-text'] = {'value': v['text'], 'type': 'color'}
        sem[f'{k}-dark'] = {'value': v['dark'], 'type': 'color'}
    out = {'$description': {'name': name, 'algorithm': 'OKLCH', 'base': p['base']},
           'color': {
               'primary': grp('primary'),
               'secondary': grp('secondary'),
               'accent': grp('accent'),
               'neutral': grp('neutral'),
               'semantic': sem,
           }}
    return json.dumps(out, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------- Markdown 导出


def export_md(p, name, checks):
    pr, sec, acc, nu, sem = p['primary'], p['secondary'], p['accent'], p['neutral'], p['semantic']
    npass = sum(1 for c in checks if c['pass'])
    lines = [
        f'# 🎨 配色方案 — {name}',
        '',
        f"> 基准色 `{p['base']}` · OKLCH L={p['base_oklch']['L']} C={p['base_oklch']['C']} H={p['base_oklch']['H']}°",
        f"> 辅助色 {'类似色' if p['secondary_mode']=='analogous' else '分裂互补'} +{int(p['secondary_deg'])}° · 含深色模式",
        '',
        '## 主色 Primary',
        '',
        '| 令牌 | HEX | 用途 |',
        '|------|-----|------|',
    ]
    for k in SCALE_ORDER:
        lines.append(f'| primary-{k} | {pr[k]} | {SCALE_USAGE[k]} |')
    lines += ['', '## 辅助色 Secondary', '', '| 令牌 | HEX | 用途 |', '|------|-----|------|']
    for k in SCALE_ORDER:
        lines.append(f'| secondary-{k} | {sec[k]} | {SCALE_USAGE[k]} |')
    if acc:
        lines += ['', '## 强调色 Accent', '', '| 令牌 | HEX |', '|------|-----|']
        for k in ['100','200','300','400','500','600','700','900']:
            lines.append(f'| accent-{k} | {acc[k]} |')
    lines += ['', '## 中性色 Neutral', '', '| 令牌 | HEX | 用途 |', '|------|-----|------|']
    for k in NEUTRAL_ORDER:
        lines.append(f'| neutral-{k} | {nu[k]} | {NEUTRAL_USAGE[k]} |')
    lines += ['', '## 语义色 Semantic', '',
              '| 类型 | base (图标/按钮) | text (小字安全) | dark (深色模式) |',
              '|------|----------------|----------------|------------------|']
    for k, v in sem.items():
        lines.append(f'| {v["cn"]} | {v["base"]} ({v["base_contrast"]}:1) | {v["text"]} ({v["text_contrast"]}:1) | {v["dark"]} ({v["dark_contrast"]}:1) |')
    lines += ['', f'## 对比度校验 ({npass}/{len(checks)} 通过)', '',
              '| 组合 | 前景 | 背景 | 实测 | 要求 | 结果 | 用途 |',
              '|------|------|------|------|------|------|------|']
    for c in checks:
        lines.append(f'| {c["label"]} | {c["fg"]} | {c["bg"]} | {c["ratio"]}:1 | ≥{c["min"]} | {"✅" if c["pass"] else "❌"} | {c["note"]} |')
    lines += ['', '## 使用比例', '',
              '- 主色 60% · 辅助 18% · 中性 12% · 语义 6% · 强调 ≤4%',
              '- 主按钮 primary-500 + 白字；不足 4.5:1 用 600/700',
              '- 语义色小字必须用 text 版',
              '- 深色模式主色用 300/400，背景 #0B1118，文字 #E5E7EB',
              '',
              '*由 color-palette-advisor 生成 · OKLCH 感知均匀算法*']
    return '\n'.join(lines)


# ---------------------------------------------------------------- main


def main():
    ap = argparse.ArgumentParser(description='color-palette-advisor 计算引擎')
    ap.add_argument('--base', required=True, help='基准色 HEX, 如 #0F62FE')
    ap.add_argument('--name', default='配色方案', help='项目名称')
    ap.add_argument('--secondary-mode', choices=['analogous', 'split'], default='analogous')
    ap.add_argument('--sec-deg', type=float, help='辅助色色相偏移 (覆盖 mode)')
    ap.add_argument('--acc-deg', type=float, help='强调色色相偏移')
    ap.add_argument('--no-accent', action='store_true', help='不生成强调色')
    ap.add_argument('--html', action='store_true', help='生成 HTML 预览')
    ap.add_argument('--export', choices=['css', 'figma', 'md'], help='导出格式')
    ap.add_argument('--out', help='输出文件路径')
    ap.add_argument('--dark', action='store_true', help='输出深色模式变体')
    args = ap.parse_args()

    p = build_palette(args.base.upper(), args.secondary_mode,
                      with_accent=not args.no_accent,
                      sec_deg=args.sec_deg, acc_deg=args.acc_deg)
    checks = run_checks(p)
    npass = sum(1 for c in checks if c['pass'])

    if args.export:
        if args.export == 'css':
            out = export_css(p, args.name)
            ext = 'css'
        elif args.export == 'figma':
            out = export_figma(p, args.name)
            ext = 'json'
        else:
            out = export_md(p, args.name, checks)
            ext = 'md'
        if args.out:
            with open(args.out, 'w', encoding='utf-8') as f:
                f.write(out)
            print(f'已导出 {args.out}')
        else:
            print(out)
        return

    if args.html:
        out_path = args.out or '/tmp/openclaw/palette-preview.html'
        render_html(p, args.name, checks, out_path)
        print(f'HTML 预览: {out_path}')
        return

    # 默认: JSON + 摘要
    summary = {
        'name': args.name,
        'base': p['base'],
        'oklch': p['base_oklch'],
        'palette': p,
        'checks': checks,
        'summary': f'{npass}/{len(checks)} 项对比度达标',
    }
    out = json.dumps(summary, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, 'w', encoding='utf-8') as f:
            f.write(out)
        print(f'已输出 {args.out}')
    else:
        print(out)


if __name__ == '__main__':
    main()