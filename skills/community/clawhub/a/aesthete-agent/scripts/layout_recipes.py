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
import type_tokens  # AE-FONT-UP: 字号令牌唯一真源


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
    fr = ((0.92, ""), (0.78, ".5"), (0.66, ""), (0.54, ".5"), (0.40, ""))
    rings = "".join(f"<circle cx='{c}' cy='{c}' r='{c * f - stroke_w}' stroke-opacity='{o}'/>"
                    for f, o in fr)
    return (f"<svg width='{s}' height='{s}' viewBox='0 0 {s} {s}' aria-hidden='true' "
            f"style='display:block'>"
            f"<g fill='none' stroke='#{t['SAGE']}' stroke-width='{stroke_w}'>{rings}</g>"
            f"<g fill='none' stroke='#{accent}' stroke-width='{stroke_w}'>"
            f"<circle cx='{c}' cy='{c}' r='{c * 0.14}'/></g>"
            f"<circle cx='{c}' cy='{c}' r='{s * 0.02 + 2}' fill='#{center}'/></svg>")


def _placeholder(t, label, ratio="4/5", dark=False, big=False):
    """图版占位(0.25 二刀):底=反差面,加密年轮母题放大撑满版心,左下语义标签落角。
    不再自认占位(无"视觉位"角标)——读作设计好的编辑部图版;替换指引走 HTML 注释层。"""
    bg = "var(--night)" if dark else "var(--surface)"
    ink = "var(--mist)" if dark else "var(--ink2)"
    ring = _rings_svg(t, 230 if big else 140, 3 if big else 2)
    return (f"<div style='aspect-ratio:{ratio};background:{bg};border-radius:14px;"
            f"position:relative;display:flex;align-items:center;justify-content:center'>"
            f"{ring}"
            f"<span class='mono' style='position:absolute;left:14px;bottom:12px;color:{ink}'>{label}</span></div>")


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
  --sans-display:-apple-system,'SF Pro Display','Segoe UI Display','PingFang SC','Microsoft YaHei',sans-serif;
  --display:var(--sans);
  --mono:ui-monospace,'SF Mono',Consolas,monospace;
  --track-display:-0.011em; /* 0.28 展示级紧字距纪律(Linear 式克制;CJK 靠 palt 收标点,此值只动 display 级) */
}}
:lang(zh){{text-autospace:normal;line-break:strict}}
@supports (text-spacing-trim: space-all){{
  :lang(zh){{text-spacing-trim:space-all}} /* 0.28:全角标点挤压渐进增强(Chrome 123+;不支持则原样,clreq 口径) */
}}
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
.side-label{{position:absolute;writing-mode:vertical-rl;font:600 @FS_SMALL@/1.8 var(--mono);
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
.lift:hover{{transform:translateY(-5px);box-shadow:0 18px 44px rgba({t["INK_RGB"]},.12)}}
@media (prefers-reduced-motion:reduce){{.lift,.lift:hover{{transform:none;box-shadow:none;transition:none}}}}
figcaption{{font:400 12px/1.6 var(--mono);letter-spacing:.05em;color:var(--ink2);margin-top:10px}}
@supports (initial-letter:3){{.dropcap>p:first-of-type::first-letter{{initial-letter:3 2;
  font:700 1em var(--serif);color:var(--accent-ink,var(--accent));margin-right:10px}}}}
@media (max-width:900px){{.grid>*{{grid-column:1/-1!important}}section{{padding:64px 0}}.wrap{{padding:0 24px}}}}
/* ── 动效底座(0.21,M1/M2,渲染实证 _motionlab):终态=无动效版 ── */
/* 0.25 教训:此注释曾漏写关闭符,导致 CSS 注释吞掉其后全部配方规则,产物全裸
   (测试方视觉终审抓出;静态闸只看文本不看样式所以此前测试全绿);
   test_v01400 已加 css 注释与花括号平衡闸防复发 */
.reveal{{opacity:0;transform:translateY(24px);transition:opacity .7s ease,transform .7s ease}}
.reveal.in{{opacity:1;transform:none}}
.reveal.d1{{transition-delay:.09s}}.reveal.d2{{transition-delay:.18s}}
.btn{{transition:transform .18s ease,box-shadow .18s ease}}
.btn:hover{{transform:translateY(-2px);box-shadow:0 10px 26px rgba({t["INK_RGB"]},.14)}}
@media (prefers-reduced-motion:reduce){{.reveal,.btn,.lift{{opacity:1;transform:none;transition:none}}.reveal:hover{{transform:none}}}}
"""


def _io_script():
    """0.21 动效底座脚本:IntersectionObserver 加 .in;无 JS 时内容可见(CSS 基础态=完整)。"""
    return ('<script>const __io=new IntersectionObserver((es)=>{es.forEach((e)=>{'
            'if(e.isIntersecting){e.target.classList.add("in");__io.unobserve(e.target)}})},'
            '{threshold:.12});document.querySelectorAll(".reveal").forEach((el)=>__io.observe(el));</script>')


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


def _card(t, no, title, meta, price="¥ —", lead="周期 — 天"):
    return (f'<article class="lift" style="background:var(--card);border-radius:14px;padding:26px 26px 20px;'
            f'position:relative;overflow:hidden;display:flex;flex-direction:column;min-height:190px">'
            f'<span style="position:absolute;right:12px;top:0;font:900 84px var(--serif);color:var(--surface)">0{no}</span>'
            f'<h3 style="font:800 19px var(--serif);position:relative">{title}</h3>'
            f'<p style="font-size:13.5px;color:var(--ink2);position:relative;margin-top:6px">{meta}</p>'
            f'<div style="margin-top:auto;padding-top:16px;border-top:1px solid var(--line);'
            f'display:flex;justify-content:space-between;align-items:baseline;position:relative">'
            f'<span style="font:800 17px var(--serif)">{price}</span>'
            f'<span style="font-size:12.5px;color:var(--ink2)">{lead}</span></div></article>')


# ---------------------------------------------------------------- R1 EDIT-SPLIT

def build_edit_split(t):
    """v7 内容优先:hero 右列=本周出品真实菜单;色彩只承载意义
    (分类色标/KPI 阶梯/页顶色条);无抽象装饰。"""
    css = base_css(t) + """
body{background:#FFFFFF}
.hero{display:grid;grid-template-columns:6fr 5fr;gap:64px;align-items:start;padding:64px 0 88px}
.hero h1{font:800 clamp(40px,5.8vw,76px)/1.14 var(--sans);letter-spacing:var(--track-display);color:var(--ink)}
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
.menu-item .tag{display:inline-block;font:700 @FS_SMALL@ var(--sans);color:var(--accent-ink,var(--accent));
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
.cat-chip{display:inline-block;font:700 @FS_SMALL@ var(--sans);letter-spacing:.08em;
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
    kpi_steps = [(t["NIGHT"], "var(--pale)", "48h", "订单到出货"),
                 (t["INK2"], "var(--pale)", "12 道", "手工工序"),
                 (t["ACCENT"], "var(--pale)", "≤2%", "返修率"),
                 (t["SAGE"], "var(--ink)", "68%", "回头客")]
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
  <div><p class="kicker">{t["BRAND_EN"]} · 深松木作 · 三代手作</p>
    <h1 class="reveal">一块好木板，<br>要经得起十年。</h1>
    <p class="lede reveal d1">老料整板,榫卯无钉——<b>批次与木料来源可查证</b>。</p>
    <div style="display:flex;gap:14px;margin-bottom:8px">
      <a class="btn" style="background:var(--night);color:#fff" href="#cta">预约工坊</a>
      <a class="btn ghost" href="#s1">看方法</a></div>
    <div class="stats">
      <div><div class="n">48h</div><div class="l">订单到出货</div></div>
      <div><div class="n">12 道</div><div class="l">手工工序</div></div>
      <div><div class="n">3 代</div><div class="l">师徒相承</div></div></div></div>
  <aside class="menu-card reveal d2">
    <h3>本月出货</h3>
    <p class="season-note">老料有限,每周四更新余量;支持提前两周预约</p>
    <div class="menu-item"><div><span class="mi-name">胡桃砧板</span><span class="tag">本季</span>
      <p class="mi-desc">梅木心料 · 手工开槽 · 木蜡油面</p></div><span class="price">¥ 128 起</span></div>
    <div class="menu-item"><div><span class="mi-name">整木托盘</span>
      <p class="mi-desc">黑胡桃 · 榫卯无钉</p></div><span class="price">¥ 260 起</span></div>
    <div class="menu-item"><div><span class="mi-name">老榆餐桌</span>
      <p class="mi-desc">整板 · 六周交付</p></div><span class="price">¥ 3,600 起</span></div>
    <a class="menu-more" href="#s1">完整菜单 →</a>
  </aside>
</section>
<section class="sub" id="s1" style="position:relative">
  <div class="bg-motif" style="left:-60px;top:-20px">{_rings_svg(t, 300, 2)}</div>
  <div class="claim" style="position:relative">
  <p class="kicker">理念</p><h2>一节只说一件事，说透。</h2>
  <p style="color:var(--ink2)">工坊只有六双手,每一件都过三道手检;批次与木料来源写进随附卡,可查证。</p>
  <div class="claim-points">
    <div><span class="no">01</span><p>每周小批量,售完即止</p></div>
    <div><span class="no">02</span><p>配料表公开,可查证</p></div></div></div></section>
<section class="sub"><div class="features">
  {_card(t, 1, "砧板系列", "当季木料 · 手工开槽", "¥ 128 起", "周期 14 天")}
  {_card(t, 2, "婚礼定制", "刻字 · 礼盒包装", "¥ 520 起", "周期 21 天")}
  {_card(t, 3, "茶盘礼盒", "六件 · 当日发货", "¥ 388 起", "周期 7 天")}</div></section>
<section class="sub"><div class="grid"><div class="quoteband"><div class="quote">
  <p>「那只砧板用了两年,刀痕越深越好看。」</p>
  <footer style="margin-top:14px;font-size:13px;color:var(--ink2)">—— 老客回访 · 2025</footer>
</div></div></div></section>
<section class="sub"><div class="kpis">{kpis}</div></section>
</div>
<section class="dark-cta" id="cta"><div class="wrap" style="max-width:66ch;text-align:center">
  <h2 style="font:800 clamp(28px,3.6vw,44px)/1.25 var(--serif)">下周工坊档期,现在开约。</h2>
  <p style="color:var(--mist);margin:14px 0 26px">留下联系方式,48 小时内回电;先聊用途,再报工时与价。</p>
  <a class="btn" style="background:var(--pale);color:var(--night)" href="#">预约工坊</a></div></section>
<footer><div class="wrap" style="padding-top:26px;padding-bottom:40px;font-size:13px;color:var(--ink2);
  display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px">
  <span>© 2026 {t["BRAND"]}</span><!-- 0.30:引擎署名撤出可见页脚(配方 EDIT-SPLIT·四闸 PASS·本页实测) --><span>工坊预约 · 周三至周日</span></div></footer>
{_io_script()}</body></html>"""
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
    cells = [("main", "离线优先的配色引擎", "四道机械闸不过不交付;检查全部本地完成,零联网。",
              [("WCAG 对比", "AA 全过"), ("色盲模拟", "三型区分"), ("金标回归", "逐版可复现")]),
             ("", "命令行出稿", "audit 一条命令出体检。", None), ("", "配方模板库", "五配方 × 四语域。", None),
             ("", "渲染对账", "截图与声明逐像素核。", None), ("", "团队令牌表", "CSS 变量直接接线。", None)]
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
  <p class="kicker" style="justify-content:center;color:var(--sage)">{t["BRAND_EN"]} · ENGINEERING TOOLKIT</p>
  <h1 class="reveal">为严肃场景<br>造的工具。</h1>
  <p class="sub reveal d1">一条命令完成配色把关:对比、色盲、反俗套、评分——四闸不过不交付。</p>
  <a class="btn" style="background:var(--pale);color:var(--night)" href="#cta">开始使用</a>
  <a class="btn ghost" style="color:var(--pale);border-color:var(--mist);margin-left:12px" href="#s1">读文档</a>
</section>
<section class="sub" id="s1"><div class="bento">{''.join(bento)}</div></section>
<section class="sub"><div class="center8 code">
&lt;config&gt;<br>&nbsp;&nbsp;<b>engine</b>="outbound" <span class="cm">// 四道机械检查,不过不交付</span><br>
&nbsp;&nbsp;<b>gates</b>=["contrast","colorblind","slop","score"]<br>&lt;/config&gt;</div></section>
<section class="sub" id="price"><div class="lightzone">
  <p class="kicker">定价</p>
  <div class="grid" style="grid-template-columns:repeat(3,1fr)"> {tier_html} </div></div></section>
<section class="sub"><div class="center8">
  <p class="kicker" style="color:var(--sage)">FAQ</p>
  <details open><summary>静态闸会不会漏?</summary><p style="color:var(--mist);font-size:14px;padding-top:10px">双层:源码静态闸之外,渲染对账把实际画出来的颜色逐像素对回声明。</p></details>
  <details><summary>接什么栈?</summary><p style="color:var(--mist);font-size:14px;padding-top:10px">产物是纯 HTML/CSS,令牌表给出全套 CSS 变量;任何框架直接接。</p></details>
</div></section>
<section class="sub" id="cta" style="text-align:center;padding-bottom:96px">
  <h2 style="font:800 clamp(30px,4vw,48px)/1.2 var(--display)">下一个页面,让它配色。</h2>
  <p style="color:var(--mist);margin:12px 0 24px;font-size:14.5px">在线演示 · 打开就能用</p>
  <a class="btn" style="background:var(--pale);color:var(--night)" href="#">立即开始</a></section>
</div></div>
<footer><div class="wrap" style="padding-bottom:36px;font-size:12.5px;color:var(--mist);display:flex;justify-content:space-between">
  <span>© 2026 {t["BRAND"]}</span><!-- 0.30:引擎署名撤出可见页脚(配方 BLUEPRINT) --><span>outbound · 四闸验证的配色引擎</span></div></footer>
{_io_script()}</body></html>"""
    return html


# ---------------------------------------------------------------- R3 SWISS-POSTER

def build_swiss_poster(t):
    css = base_css(t) + """
/* 0.28:body 级正字距已废除(clreq 不给中文正文加字距;全局 0.01em=隐性松散)——display 级走 --track-display */
.rule{border-top:1px solid var(--ink)}
.masthead{display:flex;justify-content:space-between;align-items:baseline;padding:20px 0}
.giant{font:700 clamp(64px,14vw,200px)/1.04 var(--serif);letter-spacing:var(--track-display);
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
  <p class="kicker">MANIFESTO · 本季主张</p>
  <h1 class="giant reveal">不卖隔夜甜，<br>售完就收炉。</h1>
  <p class="giant-cap reveal d1" style="max-width:92%;margin-top:10px;font-size:15px;color:var(--ink2)">每周小批,售完即止——招牌卷与司康,周四 16:00 出炉。</p>
  <a class="btn cta" href="#cta">预订本季</a></div>
<hr class="rule">
<div class="wrap"><section class="sec3x9">
  <div><span class="no">01</span><span class="ghost-num" style="display:block">01</span></div>
  <div><h2>为什么小批量</h2><p style="color:var(--ink2);max-width:60ch">一天只烤两炉,面团当日现配;下午四点出炉,卖完收炉,不做存货。</p>
  <p style="color:var(--ink2);max-width:60ch;margin-top:12px">节令原料换季即换菜单;门店不设中央库存。</p></div>
</section><hr class="hairline">
<section class="sec9x3">
  <div><h2>甜度按季走</h2><p style="color:var(--ink2);max-width:60ch">春天莓果,入秋坚果;司康配当季果酱,甜度比连锁低两档。</p>
  <p style="color:var(--ink2);max-width:60ch;margin-top:12px">出炉时刻与余量,每晚 21:00 在门店小黑板更新。</p></div>
  <div><span class="no">02</span><span class="ghost-num" style="display:block">02</span></div>
</section><hr class="hairline">
<section class="bigquote"><p>「甜品上桌的那十分钟,是一天里最贵的一口空气。」</p>
  <footer style="margin-top:16px" class="mono">—— 主厨 · 2026</footer></section>
<section class="sec3x9" id="cta">
  <div><span class="no">03</span></div>
  <div><h2>预订与到店</h2>
    <p style="color:var(--ink2);max-width:48ch;margin-bottom:20px">周四 16:00 出炉;支持门店自提与同城配送。</p>
    <a class="btn" href="#">预订本季</a></div>
</section></div>
<footer><div class="wrap" style="padding-bottom:40px"><hr class="rule">
  <div style="display:flex;justify-content:space-between;padding-top:18px;font-size:12.5px;color:var(--ink2)">
  <span>© 2026 {t["BRAND"]}</span><!-- 0.30:引擎署名撤出可见页脚(配方 SWISS-POSTER) --><span>每周小批 · 售完即止</span></div></footer>
{_io_script()}</body></html>"""
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
  <span class="meta mono">ISSUE 01 — {t["BRAND_EN"]} — 器物与生活</span>
  <div class="art">{_rings_svg(t, 420, 3)}</div>
  <div class="cap">
    <h1 class="reveal" style="font:900 clamp(34px,5vw,64px)/1.15 var(--serif);color:var(--pale);max-width:20ch">开卷:一只碗的来路。</h1>
    <p class="reveal d1" style="margin-top:14px;font-size:14.5px;max-width:44ch">三位匠人、一间工作室、一只碗的完整来路。</p></div></div>
<div class="narrow dropcap" style="position:relative">
  <div class="bg-motif" style="right:-80px;top:-40px">{_rings_svg(t, 280, 2)}</div>
  <div style="display:flex;justify-content:space-between;align-items:baseline;border-top:1px solid var(--line);
       border-bottom:1px solid var(--line);padding:10px 2px;margin-bottom:26px">
    <span class="mono">VOL.01 — 器物特辑</span><span class="mono">{t["BRAND_EN"]}</span></div>
  <p class="kicker" style="position:relative">导语</p>
  <h2 style="position:relative">窄文节:一行一次呼吸的宽度。</h2>
  <p style="color:var(--ink2)">本期从一只碗开始:三位匠人,两窑釉色,一段与泥土相处的时间。</p>
</div>
<div class="wrap"><section style="padding-top:0"><div class="offset">
  <div style="background:var(--pale);border-radius:14px;padding:36px 32px">
    <p class="kicker">主理人手记</p>
    <p style="font:700 19px/1.7 var(--serif)">「器物的分寸,和日子的分寸一样——<br>多一分则满,少一分则空。」</p>
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
  <p><span style="color:var(--sage);font-size:1.3em">「</span>好的器物不说话,它只是等你用旧它。<span style="color:var(--sage);font-size:1.3em">」</span></p>
  <footer class="mono" style="margin-top:14px">—— 卷首 · 编辑部</footer></div></div></section>
<section class="sub"><div class="tri">
  <figure style="margin:0">{_placeholder(t, "拉坯 · 湿坯定形", "4/5")}<figcaption>图 01 — 拉坯 · 湿坯定形</figcaption></figure>
  <figure style="margin:0">{_placeholder(t, "施釉 · 前后对照", "4/5")}<figcaption>图 02 — 施釉 · 前后对照</figcaption></figure>
  <figure style="margin:0">{_placeholder(t, "成器 · 晨光下", "4/5")}<figcaption>图 03 — 成器 · 晨光下</figcaption></figure>
</div></section></div>
<section class="close-bar" id="cta"><div class="wrap" style="text-align:center;padding:96px 24px">
  <h2 style="font:800 clamp(28px,3.8vw,46px)/1.22 var(--serif)">下期预告:市集专辑。</h2>
  <p style="color:var(--mist);margin:12px 0 24px;font-size:14.5px">颗粒在暗幕上,故事在亮处讲完。</p>
  <a class="btn" style="background:var(--pale);color:var(--night)" href="#">订阅月刊</a></div></section>
<footer><div class="wrap" style="padding:22px 0 36px;font-size:12.5px;color:var(--ink2);display:flex;justify-content:space-between">
  <span>© 2026 {t["BRAND"]}</span><!-- 0.30:引擎署名撤出可见页脚(配方 EDITORIAL-MAG) --><span>晨柔手帖 · 月刊</span></div></footer>
{_io_script()}</body></html>"""
    return html


# ---------------------------------------------------------------- 调度

RECIPES = {
    "EDIT-SPLIT": build_edit_split,
    "BLUEPRINT": build_blueprint,
    "SWISS-POSTER": build_swiss_poster,
    "EDITORIAL-MAG": build_editorial_mag,
}


PAGE_SIGNALS = (
    # 0.26 页型信号词表:brief/use_when 文本命中即定配方(命中多者优先,同分按表序)
    ("DARK-FOUR-ACT", ("工作室", "品牌叙事", "匠人", "手作", "作品集", "narrative", "studio")),
    ("BLUEPRINT", ("工具", "工程", "开发者", "文档", "API", "SDK", "定价", "技术", "tech")),
    ("SWISS-POSTER", ("海报", "展览", "宣言", "活动", "发布", "开幕", "poster", "event")),
    ("EDITORIAL-MAG", ("杂志", "期刊", "月刊", "画册", "特辑", "编辑", "magazine", "editorial")),
    ("EDIT-SPLIT", ("门店", "菜单", "出品", "预约", "到店", "landing", "新品")),
)
DARK_FORCING = ("DARK-FOUR-ACT", "BLUEPRINT")


def pick_recipe(tokens, brief=""):
    """0.26 两级路由(明暗铁律不动,2026-10-21/22 用户令):
    ①页型信号:brief/use_when 文本命中 PAGE_SIGNALS 词表 → 定配方(命中数多者优先,同分按表序);
      但信号指向深色强制配方(BLUEPRINT/DARK-FOUR-ACT)而色板为浅优时,降级到 EDIT-SPLIT——
      明暗仍由色板气质决定,信号只定版式家族;
    ②无信号:按色板气质定明暗(0.16 判据不动):浅优(明度≥0.60 占比≥2/5)→EDIT-SPLIT,
      深色即品牌色→DARK-FOUR-ACT;近中性灰阶(饱和<0.15)按墨色戏剧走暗幕。
    判据用原始声明板(tokens["SRC"],非派生 PALETTE_DECL——card 恒浅/line 恒深会让派生集系统性偏向浅底)。
    返回 (recipe, rationale):理由必须进 stdout,AUTO 不做黑盒。"""
    import colorsys
    brief = " ".join(filter(None, [brief, tokens.get("USE_WHEN", "")]))
    src = tokens.get("SRC") or tokens["PALETTE_DECL"]
    hexes = [h for h in src.split(",") if h]
    light = False
    if hexes:
        light_n, max_sat = 0, 0.0
        for h in hexes:
            r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
            hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
            if ll >= 0.60:
                light_n += 1
            max_sat = max(max_sat, ss)
        light = max_sat >= 0.15 and light_n * 5 >= len(hexes) * 2
    temper = "浅优" if light else "深色/墨色"

    # ① 页型信号
    hits = []
    low = brief.lower()
    for name, words in PAGE_SIGNALS:
        n = sum(1 for w in words if w in brief or (w.isascii() and w in low))
        if n:
            hits.append((n, PAGE_SIGNALS.index((name, words)), name))
    if hits:
        hits.sort(reverse=True)
        recipe = hits[0][2]
        if light and recipe in DARK_FORCING:
            why = ("页型信号「%s」指向 %s,但色板气质=浅优(明暗铁律:浅优不进深色强制配方)"
                   " → 降级 EDIT-SPLIT(浅底编辑部骨架)" % (
                       "、".join(w for w in PAGE_SIGNALS[hits[0][1]][1] if w in brief or (w.isascii() and w in low))[:30],
                       recipe))
            return "EDIT-SPLIT", why
        why = "页型信号「%s」命中 %s(命中 %d 词);色板气质=%s,明暗随配方定" % (
            "、".join(w for w in PAGE_SIGNALS[hits[0][1]][1] if w in brief or (w.isascii() and w in low))[:30],
            recipe, hits[0][0], temper)
        return recipe, why
    # ② 色板气质兜底(0.16 判据原样)
    if not hexes:
        return "DARK-FOUR-ACT", "无声明板 → 默认暗幕叙事"
    if max_sat < 0.15:
        return "DARK-FOUR-ACT", "无页型信号;色板近中性(饱和<0.15)按墨色戏剧 → 暗幕叙事"
    if light:
        return "EDIT-SPLIT", "无页型信号;色板浅优(明度≥0.60 占比≥2/5) → 浅底编辑部骨架"
    return "DARK-FOUR-ACT", "无页型信号;深色即品牌色 → 暗幕叙事"


def build_recipe(tokens, recipe):
    """recipe 名 → 完整 HTML;AUTO(默认)=pick_recipe 两级路由(页型信号×色板气质);未知名 ValueError。"""
    recipe = (recipe or "AUTO").upper().strip()
    if recipe == "AUTO":
        recipe, _why = pick_recipe(tokens, tokens.get("USE_WHEN", ""))
    if recipe == "DARK-FOUR-ACT":
        import scaffold_kit
        return type_tokens.fill(scaffold_kit.build(tokens))
    fn = RECIPES.get(recipe)
    if fn is None:
        raise ValueError(f"未知配方: {recipe}——可选: AUTO, DARK-FOUR-ACT, EDIT-SPLIT, BLUEPRINT, SWISS-POSTER, EDITORIAL-MAG")
    return type_tokens.fill(fn(tokens))


def fingerprint(tokens, recipe):
    return hashlib.sha256(("aesthete-recipe/v1|" + recipe + "|" + tokens["PALETTE_DECL"])
                          .encode("utf-8")).hexdigest()
