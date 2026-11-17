# -*- coding: utf-8 -*-
"""layout_recipes.py — 布局配方库(scaffold --recipe 的实现体,0.14.0)。

五套参数化整页配方(语法见 references/layout-composition.md):
  EDIT-SPLIT 编辑部非对称 / BLUEPRINT 工程蓝图 / SWISS-POSTER 瑞士海报 /
  EDITORIAL-MAG 杂志画册 / DARK-FOUR-ACT 暗幕叙事(原四幕,build())。
共享:derive() 令牌 + 排印底座(0.13) + 12 列容器 + 间距三级制(96/64/40)
     + 母题占位语言(年轮环 SVG+mono 注记——占位块不是空块)。
纪律:零渐变(网格/点阵用 SVG data-URI)、字号下限 12px、display 行高 ≤1.25、
中文禁负字距、产出只含派生令牌色。
v2(视觉回路修订,2026-10-21 渲染评审后):占位块全部母题化/巨字技术风改黑体栈/
BLUEPRINT 补导航+代码块对比度+定价区翻亮/卡片补底部行/引文幕加底色。
"""
import hashlib


# ---------------------------------------------------------------- 共享底座

def _grain():
    return ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='240' "
            "height='240'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' "
            "numOctaves='2'/%3E%3C/filter%3E%3Crect width='240' height='240' filter='url(%23n)' "
            "opacity='0.55'/%3E%3C/svg%3E\")")


def _grid_bg(line_color):
    svg = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24'%3E"
           "%3Cpath d='M24 0H0V24' fill='none' stroke='%23" + line_color + "' stroke-opacity='.10'/%3E%3C/svg%3E")
    return f"url(\"{svg}\")"


def _rings_svg(t, size, stroke_w=2, dark=False):
    """品牌母题:年轮环。dark=True 用浅描边+浅圆心(暗底可见)。"""
    s = size
    c = s / 2
    center = t["PALE"] if dark else t["INK"]
    accent = t["PALE"] if dark else t["ACCENT"]
    return (f"<svg width='{s}' height='{s}' viewBox='0 0 {s} {s}' aria-hidden='true' "
            f"style='display:block'>"
            f"<g fill='none' stroke='#{t['SAGE']}' stroke-width='{stroke_w}'>"
            f"<circle cx='{c}' cy='{c}' r='{c * 0.92 - stroke_w}'/>"
            f"<circle cx='{c}' cy='{c}' r='{c * 0.66}'/>"
            f"<circle cx='{c}' cy='{c}' r='{c * 0.40}'/></g>"
            f"<g fill='none' stroke='#{accent}' stroke-width='{stroke_w}'>"
            f"<circle cx='{c}' cy='{c}' r='{c * 0.14}'/></g>"
            f"<circle cx='{c}' cy='{c}' r='{s * 0.02 + 2}' fill='#{center}'/></svg>")


def _placeholder(t, label, ratio="4/5", dark=False, big=False):
    """母题占位块:底=反差面,中央年轮环+mono 标签。所有图片位统一用它。"""
    bg = "var(--night)" if dark else "var(--surface)"
    ink = "var(--mist)" if dark else "var(--ink2)"
    ring = _rings_svg(t, 180 if big else 96, 3 if big else 2)
    return (f"<div style='aspect-ratio:{ratio};background:{bg};border-radius:14px;"
            f"display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px'>"
            f"{ring}<span class='mono' style='color:{ink}'>{label}</span></div>")


def _stripe(t):
    """品牌色条:五色泊条(页顶 5px,色板第一时间亮相)。"""
    cols = [t["NIGHT"], t["INK2"], t["ACCENT"], t["SAGE"], t["PALE"]]
    spans = "".join(f"<span style='flex:1;background:#{c}'></span>" for c in cols)
    return f"<div style='display:flex;height:5px' aria-hidden='true'>{spans}</div>"


def base_css(t):
    """共享排印底座+通用元件。t = derive() 令牌。"""
    return f""":root{{
  --night:#{t["NIGHT"]};--pale:#{t["PALE"]};--mist:#{t["MIST"]};--sage:#{t["SAGE"]};
  --surface:#{t["SURFACE"]};--ink:#{t["INK"]};--ink2:#{t["INK2"]};--accent:#{t["ACCENT"]};
  --card:#{t["CARD"]};--line:#{t["LINE"]};
  --serif:'Noto Serif SC','Source Han Serif SC','Songti SC',Georgia,serif;
  --sans:-apple-system,'PingFang SC','Microsoft YaHei','Segoe UI',sans-serif;
  --display:var(--sans);
  --mono:ui-monospace,'SF Mono',Consolas,monospace;
}}
:lang(zh){{text-autospace:normal;line-break:strict}}
h1,h2{{text-wrap:balance}}
p{{text-wrap:pretty}}
:lang(zh) :is(h1,h2,h3){{font-feature-settings:"palt" 1}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--pale);color:var(--ink);font:400 16px/1.75 var(--sans)}}
a{{color:inherit;text-decoration:none}}
img{{max-width:100%;display:block}}
.wrap{{max-width:1200px;margin:0 auto;padding:0 48px}}
.grid{{display:grid;grid-template-columns:repeat(12,1fr);gap:24px}}
:focus-visible{{outline:3px solid var(--sage);outline-offset:3px}}
.kicker{{display:flex;align-items:center;gap:10px;font:700 12px/1.6 var(--sans);
         letter-spacing:.28em;color:var(--accent-ink,var(--accent));margin-bottom:14px}}
.kicker::before{{content:"";width:24px;height:1px;background:var(--accent)}}
.hairline{{border:0;border-top:1px solid var(--line)}}
.mono{{font:400 12px/1.6 var(--mono);letter-spacing:.05em;opacity:.62}}
.btn{{display:inline-block;background:var(--ink);color:var(--pale);font:700 15px/1 var(--sans);
      padding:16px 32px;border-radius:10px}}
.btn.ghost{{background:transparent;color:var(--ink);border:1.5px solid var(--ink)}}
.ghost-num{{font:900 clamp(96px,12vw,160px)/1 var(--serif);color:transparent;
            -webkit-text-stroke:1px var(--line);pointer-events:none}}
.cross{{position:absolute;width:11px;height:11px;pointer-events:none}}
.cross::before{{content:"";position:absolute;left:5px;top:0;width:1px;height:11px;background:var(--ink2);opacity:.5}}
.cross::after{{content:"";position:absolute;top:5px;left:0;width:11px;height:1px;background:var(--ink2);opacity:.5}}
.side-label{{position:absolute;writing-mode:vertical-rl;font:600 11px/1.8 var(--mono);
             letter-spacing:.3em;color:var(--ink2);opacity:.55;pointer-events:none}}
.bg-motif{{position:absolute;pointer-events:none;opacity:.07}}
.dark .bg-motif{{opacity:.12}}
section{{padding:96px 0}}
section .sub{{padding:64px 0 0}}
table{{width:100%;border-collapse:collapse;font-size:14.5px}}
th{{background:var(--surface);text-align:left;padding:12px 18px;font-weight:700}}
td{{padding:12px 18px;border-top:1px solid var(--line)}}
.num{{text-align:right;font-variant-numeric:tabular-nums;font-weight:600}}
.lift{{transition:transform .22s ease,box-shadow .22s ease}}
.lift:hover{{transform:translateY(-5px);box-shadow:0 18px 44px rgba(17,22,30,.12)}}
@media (prefers-reduced-motion:reduce){{.lift,.lift:hover{{transform:none;box-shadow:none;transition:none}}}}
figcaption{{font:400 12px/1.6 var(--mono);letter-spacing:.05em;color:var(--ink2);margin-top:10px}}
@supports (initial-letter:3){{.dropcap>p:first-of-type::first-letter{{initial-letter:3 2;
  font:700 1em var(--serif);color:var(--accent-ink,var(--accent));margin-right:10px}}}}
@media (max-width:900px){{.grid>*{{grid-column:1/-1!important}}section{{padding:64px 0}}.wrap{{padding:0 24px}}}}
"""


def _nav(t, dark=False):
    c1 = "var(--pale)" if dark else "var(--night)"
    c2 = "var(--night)" if dark else "var(--pale)"
    return (f'<header style="background:{c2}"><div class="wrap" style="display:flex;'
            f'justify-content:space-between;align-items:center;padding-top:20px;padding-bottom:20px">'
            f'<a href="#" style="font:700 17px var(--serif);color:{c1}">{t["BRAND"]}</a>'
            f'<nav style="display:flex;gap:24px;font-size:13.5px;font-weight:600">'
            f'<a style="color:var(--ink2)" href="#s1">一览</a>'
            f'<a style="color:var(--ink2)" href="#s2">方法</a>'
            f'<a style="color:var(--ink2)" href="#cta">联系</a></nav></div></header>')


def _card(t, no, title, meta):
    return (f'<article class="lift" style="background:var(--card);border-radius:14px;padding:26px 26px 20px;'
            f'position:relative;overflow:hidden;display:flex;flex-direction:column;min-height:190px">'
            f'<span style="position:absolute;right:12px;top:0;font:900 84px var(--serif);color:var(--surface)">0{no}</span>'
            f'<h3 style="font:800 19px var(--serif);position:relative">{title}</h3>'
            f'<p style="font-size:13.5px;color:var(--ink2);position:relative;margin-top:6px">{meta}</p>'
            f'<div style="margin-top:auto;padding-top:16px;border-top:1px solid var(--line);'
            f'display:flex;justify-content:space-between;align-items:baseline;position:relative">'
            f'<span style="font:800 17px var(--serif)">¥ —</span>'
            f'<span style="font-size:12.5px;color:var(--ink2)">周期 — 天</span></div></article>')


# ---------------------------------------------------------------- R1 EDIT-SPLIT

def build_edit_split(t):
    """v7 内容优先:hero 右列=本周出品真实菜单;色彩只承载意义
    (分类色标/KPI 阶梯/页顶色条);无抽象装饰。"""
    css = base_css(t) + """
body{background:#FFFFFF}
.hero{display:grid;grid-template-columns:6fr 5fr;gap:64px;align-items:start;padding:64px 0 88px}
.hero h1{font:800 clamp(40px,5.8vw,76px)/1.14 var(--sans);letter-spacing:0.01em;color:var(--ink)}
.hero h1 em{font-style:normal;color:var(--ink2)}
.hero .lede{font-size:16.5px;line-height:1.7;color:var(--ink2);margin:20px 0 26px;max-width:44ch}
.stats{display:flex;gap:44px;margin-top:36px}
.stats .n{font:800 clamp(26px,2.6vw,34px)/1 var(--sans);font-variant-numeric:tabular-nums;
          color:var(--accent-ink,var(--accent))}
.stats .l{font-size:12.5px;color:var(--ink2);margin-top:6px}
.menu-card{border:1px solid var(--line);border-radius:16px;padding:30px 30px 22px;background:#FFFFFF}
.menu-card h3{font:800 15px var(--sans);letter-spacing:.14em;margin-bottom:6px}
.menu-card .season-note{font-size:12px;color:var(--ink2);margin-bottom:14px}
.menu-item{display:flex;justify-content:space-between;align-items:baseline;gap:14px;
           padding:14px 0;border-top:1px solid var(--line)}
.menu-item .mi-name{font:700 15px var(--sans)}
.menu-item .mi-desc{font-size:12.5px;color:var(--ink2);margin-top:3px}
.menu-item .price{font:800 15px var(--sans);font-variant-numeric:tabular-nums;white-space:nowrap}
.menu-item .tag{display:inline-block;font:700 11px var(--sans);color:var(--accent-ink,var(--accent));
                background:var(--pale);border-radius:4px;padding:2px 8px;margin-left:8px;
                vertical-align:2px}
.menu-more{display:inline-block;margin-top:14px;font:700 13px var(--sans);color:var(--ink);
           border-bottom:1.5px solid var(--ink);padding-bottom:2px}
.claim{max-width:66ch;margin:0 auto}
.claim h2{font:700 clamp(28px,3.4vw,42px)/1.25 var(--serif);margin-bottom:14px;
          -webkit-text-stroke:.4px currentColor}
.claim-points{display:flex;gap:40px;margin-top:30px;flex-wrap:wrap}
.claim-points>div{max-width:230px}
.claim-points .no{font:700 13px var(--mono);color:var(--accent-ink,var(--accent))}
.claim-points p{font-size:13.5px;color:var(--ink2);margin-top:6px}
.features{display:grid;grid-template-columns:5fr 4fr 3fr;gap:24px}
.cat-chip{display:inline-block;font:700 11px var(--sans);letter-spacing:.08em;
          border-radius:4px;padding:3px 9px;margin-bottom:14px}
.quoteband{grid-column:1/-1;background:var(--pale);border-radius:16px;padding:56px 40px}
.quote{max-width:40ch;margin:0 auto;text-align:center}
.quote p{font:700 clamp(24px,3vw,38px)/1.5 var(--serif)}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.kpi{border-radius:14px;padding:26px 24px;min-height:150px;display:flex;flex-direction:column;
     justify-content:space-between}
.kpi .n{font:800 clamp(26px,2.4vw,34px)/1 var(--sans);font-variant-numeric:tabular-nums}
.kpi .l{font-size:12.5px;margin-top:8px;opacity:.82}
.dark-cta{background:var(--night);color:var(--pale)}
@media (max-width:900px){.hero{grid-template-columns:1fr}.kpis{grid-template-columns:1fr 1fr}}
"""
    kpi_steps = [(t["NIGHT"], "var(--pale)", "—", "指标一(替换)"),
                 (t["INK2"], "var(--pale)", "—", "指标二(替换)"),
                 (t["ACCENT"], "var(--pale)", "—", "指标三(替换)"),
                 (t["SAGE"], "var(--ink)", "—", "指标四(替换)")]
    kpis = "".join(
        f'<div class="kpi" style="background:#{bg};color:{fg}">'
        f'<span class="n">{n}</span><span class="l">{l}</span></div>'
        for bg, fg, n, l in kpi_steps)
    html = f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{t["BRAND"]}</title>
<!-- layout-recipe: EDIT-SPLIT(0.14) 声明色板: {t["PALETTE_DECL"]} 跨度序列: 6+5/8/5+4+3/2+8+2/4xKPI/6 明暗: 全浅+深色点缀 -->
<style>{css}</style></head><body>
{_stripe(t)}
{_nav(t)}
<div class="wrap"><section class="hero" style="position:relative">
  <span class="cross" style="right:0;top:-6px"></span>
  <div><p class="kicker">{t["BRAND_EN"]} · 一句话定位(替换)</p>
    <h1>标题两行内，<br>说完一件事。</h1>
    <p class="lede">两行以内的价值陈述,给一个具体的、可验证的承诺。(替换)</p>
    <div style="display:flex;gap:14px;margin-bottom:8px">
      <a class="btn" style="background:var(--night);color:#fff" href="#cta">预约试吃</a>
      <a class="btn ghost" href="#s1">看方法</a></div>
    <div class="stats">
      <div><div class="n">—</div><div class="l">指标一(替换)</div></div>
      <div><div class="n">—</div><div class="l">指标二(替换)</div></div>
      <div><div class="n">—</div><div class="l">指标三(替换)</div></div></div></div>
  <aside class="menu-card">
    <h3>本周出品(替换)</h3>
    <p class="season-note">档期说明(替换)</p>
    <div class="menu-item"><div><span class="mi-name">品名一(替换)</span><span class="tag">本季</span>
      <p class="mi-desc">风味 · 要点(替换)</p></div><span class="price">¥ —(替换)</span></div>
    <div class="menu-item"><div><span class="mi-name">品名二(替换)</span>
      <p class="mi-desc">风味 · 要点(替换)</p></div><span class="price">¥ —(替换)</span></div>
    <div class="menu-item"><div><span class="mi-name">品名三(替换)</span>
      <p class="mi-desc">风味 · 要点(替换)</p></div><span class="price">¥ —(替换)</span></div>
    <a class="menu-more" href="#s1">完整菜单 →</a>
  </aside>
</section>
<section class="sub" id="s1" style="position:relative">
  <div class="bg-motif" style="left:-60px;top:-20px">{_rings_svg(t, 300, 2)}</div>
  <div class="claim" style="position:relative">
  <p class="kicker">理念</p><h2>一节只说一件事，说透。(替换)</h2>
  <p style="color:var(--ink2)">支持句:给出可验证的细节与数字,不写形容词。(替换)</p>
  <div class="claim-points">
    <div><span class="no">01</span><p>每周小批量,售完即止</p></div>
    <div><span class="no">02</span><p>配料表公开,可查证</p></div></div></div></section>
<section class="sub"><div class="features">
  {_card(t, 1, "季节限定", "当季莓果 · 轻乳脂")}
  {_card(t, 2, "婚礼定制", "三层 · 手工糖花")}
  {_card(t, 3, "下午茶礼盒", "六件 · 当日配送")}</div></section>
<section class="sub"><div class="grid"><div class="quoteband"><div class="quote">
  <p>「一句客户原话,带时间与细节。(替换)」</p>
  <footer style="margin-top:14px;font-size:13px;color:var(--ink2)">—— 署名,年份</footer>
</div></div></div></section>
<section class="sub"><div class="kpis">{kpis}</div></section>
</div>
<section class="dark-cta" id="cta"><div class="wrap" style="max-width:66ch;text-align:center">
  <h2 style="font:800 clamp(28px,3.6vw,44px)/1.25 var(--serif)">收尾行动,先具体,再干脆。(替换)</h2>
  <p style="color:var(--mist);margin:14px 0 26px">说明第一步做什么、成本与承诺。(替换)</p>
  <a class="btn" style="background:var(--pale);color:var(--night)" href="#">预约试吃</a></div></section>
<footer><div class="wrap" style="padding-top:26px;padding-bottom:40px;font-size:13px;color:var(--ink2);
  display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px">
  <span>© 2026 {t["BRAND"]}</span><span>配色与布局:aesthete-agent 配方 EDIT-SPLIT(四闸 PASS · 本页实测)</span></div></footer>
</body></html>"""
    return html


# ---------------------------------------------------------------- R2 BLUEPRINT


def build_blueprint(t):
    css = base_css(t) + f"""
body{{background:var(--night);color:var(--pale)}}
.frame{{background-image:{_grid_bg(t["PALE"])};background-size:24px 24px}}
nav.top{{display:flex;justify-content:space-between;align-items:center;padding:20px 0}}
nav.top a{{font-size:13.5px;font-weight:600;color:var(--mist)}}
nav.top a:hover{{color:var(--pale)}}
.brand{{font:700 17px var(--serif);color:var(--pale)}}
.center8{{max-width:820px;margin:0 auto}}
.hero{{text-align:center;padding:96px 0 72px}}
.hero h1{{font:800 clamp(44px,7vw,104px)/1.08 var(--display)}}
.hero .sub{{font-size:16.5px;line-height:1.6;color:var(--mist);max-width:52ch;margin:18px auto 30px}}
.bento{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}}
.cell{{background:rgba(255,255,255,.04);border:1px solid var(--line);border-radius:12px;padding:24px;min-height:150px}}
.cell.main{{grid-column:span 2;grid-row:span 2;border-color:var(--sage);display:flex;flex-direction:column}}
.cell.main ul{{list-style:none;margin:auto 0 0;padding:0}}
.cell.main li{{font-size:13px;color:var(--mist);padding:7px 0;border-top:1px solid var(--line);
               display:flex;justify-content:space-between;gap:12px}}
.cell.main li b{{color:var(--pale);font-weight:600}}
.cell h3{{font:700 16px var(--sans);margin-bottom:8px}}
.cell p{{font-size:13px;color:var(--mist)}}
.code{{background:rgba(255,255,255,.04);border:1px solid var(--line);border-radius:12px;
       padding:22px;font:400 13.5px/1.9 var(--mono);color:var(--pale);overflow:auto}}
.code b{{color:var(--sage);font-weight:400}}
.code .cm{{color:var(--mist)}}
.tier{{background:rgba(255,255,255,.03);border:1px solid var(--line);border-radius:12px;padding:28px}}
.tier.hot{{border-color:var(--sage)}}
.tier .price{{font:800 34px/1 var(--display);font-variant-numeric:tabular-nums;margin:10px 0}}
details{{border-top:1px solid var(--line);padding:16px 4px}}
summary{{cursor:pointer;font-weight:700;font-size:15px}}
.lightzone{{background:var(--pale);color:var(--ink);border-radius:16px;padding:56px 40px}}
.lightzone .tier{{background:var(--card);border-color:var(--line)}}
.lightzone .tier .price{{color:var(--night)}}
@media (max-width:900px){{.bento{{grid-template-columns:1fr 1fr}}.cell.main{{grid-column:span 2}}}}
"""
    bento = []
    cells = [("main", "主角格:核心能力(替换)", "两行说明,具体可验证。",
              [("能力点一", "已验证"), ("能力点二", "4.5:1"), ("能力点三", "可复现")]),
             ("", "格:能力", "一句话。", None), ("", "格:能力", "一句话。", None),
             ("", "格:能力", "一句话。", None), ("", "格:能力", "一句话。", None)]
    for i, (cls, h3, ptxt, rows) in enumerate(cells):
        lis = ""
        if rows:
            lis = "<ul>" + "".join(
                f"<li><span>{a}</span><b>{b}</b></li>" for a, b in rows) + "</ul>"
        bento.append(f'<div class="cell {cls}" style="position:relative"><h3>{h3}</h3><p>{ptxt}</p>{lis}'
                     f'<span class="mono" style="position:absolute;right:16px;bottom:12px;opacity:.5">0{i + 1}</span></div>')
    tiers = [("入门", "¥0", "适合个人起步。"), ("专业", "¥49/月", "适合小团队。"), ("旗舰", "联系", "适合组织。")]
    tier_html = "".join(
        f'<div class="tier{" hot" if n == "专业" else ""}">'
        f'{"<span class=mono style=\"color:var(--pale);letter-spacing:.18em\">最受欢迎</span><br>" if n == "专业" else ""}'
        f'<strong style="font-size:16px">{n}</strong><div class="price">{pr}</div>'
        f'<p style="font-size:13px;color:var(--ink2)">{d}</p>'
        f'<a class="btn" style="margin-top:16px;background:var(--night);color:var(--pale);text-align:center" href="#">选择</a></div>'
        for n, pr, d in tiers)
    html = f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{t["BRAND"]}</title>
<!-- layout-recipe: BLUEPRINT(0.14) 声明色板: {t["PALETTE_DECL"]} 序列: 8居中/4x2bento/8居中/亮区定价/FAQ -->
<style>{css}</style></head><body>
<div class="frame">
<div class="wrap"><nav class="top">
  <span class="brand">{t["BRAND"]}</span>
  <div style="display:flex;gap:24px"><a href="#s1">能力</a><a href="#price">定价</a><a href="#cta">开始</a></div>
</nav></div>
<div class="wrap"><section class="hero center8" style="position:relative">
  <span class="cross" style="left:0;top:20px"></span>
  <span class="cross" style="right:0;bottom:20px"></span>
  <p class="kicker" style="justify-content:center;color:var(--sage)">{t["BRAND_EN"]} · ENGINEERING(替换)</p>
  <h1>为严肃场景<br>造的工具。(替换)</h1>
  <p class="sub">一句可验证的价值陈述:做什么、给谁、凭什么信。(替换)</p>
  <a class="btn" style="background:var(--pale);color:var(--night)" href="#cta">开始使用</a>
  <a class="btn ghost" style="color:var(--pale);border-color:var(--mist);margin-left:12px" href="#s1">读文档</a>
</section>
<section class="sub" id="s1"><div class="bento">{''.join(bento)}</div></section>
<section class="sub"><div class="center8 code">
&lt;config&gt;<br>&nbsp;&nbsp;<b>engine</b>="aesthete" <span class="cm">// 四道机械检查,不过不交付</span><br>
&nbsp;&nbsp;<b>gates</b>=["contrast","colorblind","slop","score"]<br>&lt;/config&gt;</div></section>
<section class="sub" id="price"><div class="lightzone">
  <p class="kicker">定价(替换)</p>
  <div class="grid" style="grid-template-columns:repeat(3,1fr)"> {tier_html} </div></div></section>
<section class="sub"><div class="center8">
  <p class="kicker" style="color:var(--sage)">FAQ</p>
  <details open><summary>问题一(替换)</summary><p style="color:var(--mist);font-size:14px;padding-top:10px">答案:具体、可验证。(替换)</p></details>
  <details><summary>问题二(替换)</summary><p style="color:var(--mist);font-size:14px;padding-top:10px">答案。(替换)</p></details>
</div></section>
<section class="sub" id="cta" style="text-align:center;padding-bottom:96px">
  <h2 style="font:800 clamp(30px,4vw,48px)/1.2 var(--display)">下一个页面,让它配色。(替换)</h2>
  <p style="color:var(--mist);margin:12px 0 24px;font-size:14.5px">在线演示 · 打开就能用</p>
  <a class="btn" style="background:var(--pale);color:var(--night)" href="#">立即开始</a></section>
</div></div>
<footer><div class="wrap" style="padding-bottom:36px;font-size:12.5px;color:var(--mist);display:flex;justify-content:space-between">
  <span>© 2026 {t["BRAND"]}</span><span>aesthete-agent 配方 BLUEPRINT</span></div></footer>
</body></html>"""
    return html


# ---------------------------------------------------------------- R3 SWISS-POSTER

def build_swiss_poster(t):
    css = base_css(t) + """
body{letter-spacing:0.01em}
.rule{border-top:1px solid var(--ink)}
.masthead{display:flex;justify-content:space-between;align-items:baseline;padding:20px 0}
.giant{font:700 clamp(64px,14vw,200px)/1.04 var(--serif);letter-spacing:0.01em;
       -webkit-text-stroke:.6px currentColor}
.poster{padding:72px 0 96px;position:relative}
.poster .cta{position:absolute;right:48px;bottom:64px}
.sec3x9{display:grid;grid-template-columns:3fr 9fr;gap:32px;padding:64px 0}
.sec9x3{display:grid;grid-template-columns:9fr 3fr;gap:32px;padding:64px 0}
.sec3x9 .no,.sec9x3 .no{font:900 15px var(--sans);color:var(--accent)}
.sec3x9 h2,.sec9x3 h2{font:800 clamp(24px,2.8vw,34px)/1.25 var(--serif);margin:10px 0 12px}
.bigquote{padding:96px 0;border-top:1px solid var(--ink);border-bottom:1px solid var(--ink)}
.bigquote p{font:700 clamp(28px,4.4vw,52px)/1.35 var(--serif);max-width:22ch}
@media (max-width:900px){.sec3x9,.sec9x3{grid-template-columns:1fr}.poster .cta{position:static;margin-top:24px}}
"""
    html = f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{t["BRAND"]}</title>
<!-- layout-recipe: SWISS-POSTER(0.14) 声明色板: {t["PALETTE_DECL"]} 间距档: 120/80/48 -->
<style>{css}</style></head><body>
{_stripe(t)}
<div class="wrap"><header class="masthead">
  <strong style="font:700 18px var(--serif)">{t["BRAND"]}</strong>
  <span class="mono">SEC.00 — {t["BRAND_EN"]} — 2026</span></header>
<hr class="rule"></div>
<div class="wrap poster" style="position:relative">
  <span class="cross" style="right:0;top:36px"></span>
  <span class="cross" style="left:0;bottom:0"></span>
  <span class="side-label" style="right:-34px;top:20%">MANIFESTO — {t["BRAND_EN"]}</span>
  <p class="kicker">MANIFESTO(替换)</p>
  <h1 class="giant">一句话主张，<br>顶天立地。</h1>
  <p class="giant-cap" style="max-width:92%;margin-top:10px;font-size:15px;color:var(--ink2)">副题:两行内,给可验证的承诺。巨字占宽按内容自然生长。(替换)</p>
  <a class="btn cta" href="#cta">主行动(替换)</a></div>
<hr class="rule">
<div class="wrap"><section class="sec3x9">
  <div><span class="no">01</span><span class="ghost-num" style="display:block">01</span></div>
  <div><h2>第一节标题(替换)</h2><p style="color:var(--ink2);max-width:60ch">正文:说清这一节给用户什么,给可验证细节。版式纪律:每节一个幽灵序号,3+9 与 9+3 交替。(替换)</p>
  <p style="color:var(--ink2);max-width:60ch;margin-top:12px">补充段:密度要够,单节至少两段正文,否则瑞士风的留白会变空旷。(替换)</p></div>
</section><hr class="hairline">
<section class="sec9x3">
  <div><h2>第二节标题(替换)</h2><p style="color:var(--ink2);max-width:60ch">正文:方向翻转,形成 zigzag 节奏。(替换)</p>
  <p style="color:var(--ink2);max-width:60ch;margin-top:12px">补充段:如配数据,数字列 tabular-nums 右对齐。(替换)</p></div>
  <div><span class="no">02</span><span class="ghost-num" style="display:block">02</span></div>
</section><hr class="hairline">
<section class="bigquote"><p>「一句大引文,占满画面的呼吸。(替换)」</p>
  <footer style="margin-top:16px" class="mono">—— 署名 · 年份</footer></section>
<section class="sec3x9" id="cta">
  <div><span class="no">03</span></div>
  <div><h2>收尾行动(替换)</h2>
    <p style="color:var(--ink2);max-width:48ch;margin-bottom:20px">先具体,再干脆。(替换)</p>
    <a class="btn" href="#">主行动(替换)</a></div>
</section></div>
<footer><div class="wrap" style="padding-bottom:40px"><hr class="rule">
  <div style="display:flex;justify-content:space-between;padding-top:18px;font-size:12.5px;color:var(--ink2)">
  <span>© 2026 {t["BRAND"]}</span><span>aesthete-agent 配方 SWISS-POSTER</span></div></footer>
</body></html>"""
    return html


# ---------------------------------------------------------------- R4 EDITORIAL-MAG

def build_editorial_mag(t):
    css = base_css(t) + f"""
.bleed{{height:60vh;background:var(--night);position:relative;overflow:hidden;
        display:flex;align-items:flex-end}}
.bleed::after{{content:"";position:absolute;inset:0;background-image:{_grain()};opacity:.07}}
.bleed .art{{position:absolute;right:6vw;top:50%;transform:translateY(-50%);opacity:.5}}
.bleed .meta{{position:absolute;left:48px;top:40px;z-index:2;color:var(--mist)}}
.bleed .cap{{position:relative;z-index:2;color:var(--mist);padding:0 48px 40px;width:100%}}
.narrow{{max-width:66ch;margin:0 auto;padding:72px 24px}}
.narrow h2{{font:800 clamp(26px,3vw,38px)/1.25 var(--serif);margin:10px 0 14px}}
.offset{{display:grid;grid-template-columns:5fr 7fr;gap:32px;align-items:start}}
.offset .drop{{margin-bottom:-64px;position:relative;z-index:2}}
.pull{{grid-column:3/span 9;padding:64px 0}}
.pull p{{font:700 clamp(26px,3.6vw,44px)/1.4 var(--serif)}}
.tri{{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}}
.close-bar{{background:var(--night);color:var(--pale)}}
@media (max-width:900px){{.offset{{grid-template-columns:1fr}}.tri{{grid-template-columns:1fr}}.bleed{{height:48vh}}}}
"""
    html = f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{t["BRAND"]}</title>
<!-- layout-recipe: EDITORIAL-MAG(0.14) 声明色板: {t["PALETTE_DECL"]} 裁切: 16:9/3:2/4:5 -->
<style>{css}</style></head><body>
{_stripe(t)}
<div class="bleed">
  <span class="meta mono">ISSUE 01 — {t["BRAND_EN"]} — 三代手作</span>
  <div class="art">{_rings_svg(t, 420, 3)}</div>
  <div class="cap">
    <h1 style="font:900 clamp(34px,5vw,64px)/1.15 var(--serif);color:var(--pale);max-width:20ch">开篇大标,像杂志封面一样说话。(替换)</h1>
    <p style="margin-top:14px;font-size:14.5px;max-width:44ch">副题一行:本期给读者什么。(替换)</p></div></div>
<div class="narrow dropcap" style="position:relative">
  <div class="bg-motif" style="right:-80px;top:-40px">{_rings_svg(t, 280, 2)}</div>
  <div style="display:flex;justify-content:space-between;align-items:baseline;border-top:1px solid var(--line);
       border-bottom:1px solid var(--line);padding:10px 2px;margin-bottom:26px">
    <span class="mono">VOL.01 — 手作特辑(替换)</span><span class="mono">{t["BRAND_EN"]}</span></div>
  <p class="kicker" style="position:relative">导语</p>
  <h2 style="position:relative">窄文节:66ch 的阅读宽度。(替换)</h2>
  <p style="color:var(--ink2)">导语两行,说清本期给读者什么。图像主导的页面里,文字节是呼吸点——一节只做一件事。(替换)</p>
</div>
<div class="wrap"><section style="padding-top:0"><div class="offset">
  <div style="background:var(--pale);border-radius:14px;padding:36px 32px">
    <p class="kicker">主理人手记</p>
    <p style="font:700 19px/1.7 var(--serif)">「甜点的分寸,和做人的分寸一样——<br>多一分则腻,少一分则寡。」</p>
    <footer style="margin-top:16px;font-size:12.5px;color:var(--ink2)">—— 主理人 · 每周手记</footer></div>
  <div class="drop" style="background:var(--card);border-radius:14px;padding:36px 32px">
    <p class="kicker">到店信息</p>
    <div style="display:flex;justify-content:space-between;padding:9px 0;border-bottom:1px solid var(--line);font-size:14px">
      <span>营业</span><b>周三至周日 11:00-19:00</b></div>
    <div style="display:flex;justify-content:space-between;padding:9px 0;border-bottom:1px solid var(--line);font-size:14px">
      <span>地址</span><b style="text-align:right">湖畔路 12 号 · 一层</b></div>
    <div style="display:flex;justify-content:space-between;padding:9px 0;font-size:14px">
      <span>预约</span><b>建议提前 48 小时</b></div></div>
</div></section>
<section class="sub"><div class="grid"><div class="pull">
  <p><span style="color:var(--sage);font-size:1.3em">「</span>跨栏大引文,3+9 的留白就是它的音量。<span style="color:var(--sage);font-size:1.3em">」</span>(替换)</p>
  <footer class="mono" style="margin-top:14px">—— 署名 · 年份</footer></div></div></section>
<section class="sub"><div class="tri">
  <figure style="margin:0">{_placeholder(t, "4:5(替换)", "4/5")}<figcaption>图 01 — 木纹研究(替换)</figcaption></figure>
  <figure style="margin:0">{_placeholder(t, "4:5(替换)", "4/5")}<figcaption>图 02 — 榫卯细节(替换)</figcaption></figure>
  <figure style="margin:0">{_placeholder(t, "4:5(替换)", "4/5")}<figcaption>图 03 — 成品全貌(替换)</figcaption></figure>
</div></section></div>
<section class="close-bar" id="cta"><div class="wrap" style="text-align:center;padding:96px 24px">
  <h2 style="font:800 clamp(28px,3.8vw,46px)/1.22 var(--serif)">出血收尾 + 一句 CTA。(替换)</h2>
  <p style="color:var(--mist);margin:12px 0 24px;font-size:14.5px">颗粒在暗幕上,故事在亮处讲完。</p>
  <a class="btn" style="background:var(--pale);color:var(--night)" href="#">主行动(替换)</a></div></section>
<footer><div class="wrap" style="padding:22px 0 36px;font-size:12.5px;color:var(--ink2);display:flex;justify-content:space-between">
  <span>© 2026 {t["BRAND"]}</span><span>aesthete-agent 配方 EDITORIAL-MAG</span></div></footer>
</body></html>"""
    return html


# ---------------------------------------------------------------- 调度

RECIPES = {
    "EDIT-SPLIT": build_edit_split,
    "BLUEPRINT": build_blueprint,
    "SWISS-POSTER": build_swiss_poster,
    "EDITORIAL-MAG": build_editorial_mag,
}


def pick_recipe(tokens):
    """明暗策略路由(0.16,用户铁律 2026-10-21/22):明暗由色板气质决定——
    浅优色板浅底优先(EDIT-SPLIT),深色即品牌色的板走暗幕叙事(DARK-FOUR-ACT);
    近中性灰阶(饱和<0.15)按墨色戏剧处理走暗幕。
    判据用原始声明板(tokens["SRC"],非派生 PALETTE_DECL——card 恒浅/line 恒深会让派生集系统性偏向浅底):
    HSL 明度≥0.60 占比≥2/5 视为浅优(Deep Pine 浅色占 2/5 先例,用户 v59 裁决)。"""
    import colorsys
    src = tokens.get("SRC") or tokens["PALETTE_DECL"]
    hexes = [h for h in src.split(",") if h]
    if not hexes:
        return "DARK-FOUR-ACT"
    light_n = 0
    max_sat = 0.0
    for h in hexes:
        r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
        hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
        if ll >= 0.60:
            light_n += 1
        max_sat = max(max_sat, ss)
    if max_sat < 0.15:
        return "DARK-FOUR-ACT"
    return "EDIT-SPLIT" if light_n * 5 >= len(hexes) * 2 else "DARK-FOUR-ACT"


def build_recipe(tokens, recipe):
    """recipe 名 → 完整 HTML;AUTO(默认)=pick_recipe 按色板气质路由;未知名 ValueError。"""
    recipe = (recipe or "AUTO").upper().strip()
    if recipe == "AUTO":
        recipe = pick_recipe(tokens)
    if recipe == "DARK-FOUR-ACT":
        import scaffold_kit
        return scaffold_kit.build(tokens)
    fn = RECIPES.get(recipe)
    if fn is None:
        raise ValueError(f"未知配方: {recipe}——可选: AUTO, DARK-FOUR-ACT, EDIT-SPLIT, BLUEPRINT, SWISS-POSTER, EDITORIAL-MAG")
    return fn(tokens)


def fingerprint(tokens, recipe):
    return hashlib.sha256(("aesthete-recipe/v1|" + recipe + "|" + tokens["PALETTE_DECL"])
                          .encode("utf-8")).hexdigest()
