# -*- coding: utf-8 -*-
"""scaffold_kit.py — 0.9 表现力页面骨架生成器(scaffold 命令的实现体)。

把"惊艳公式"编码为代码:四幕明暗旅程(夜松/晨坊/夜话/夜约)+颗粒噪点+巨字对微字+
不对称编辑网格+滚动揭示(reduced-motion 全关)。对比度自动爬坡调墨,产出可直接过闸。
被 palette_forge.py 的 cmd_scaffold 调用;内容为待替换的成稿骨架,替换标记见 HTML 注释。
"""
import hashlib
import json


def _lum_lin(h):
    def lin(c):
        c /= 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def _contrast(a, b):
    l1, l2 = sorted((_lum_lin(a), _lum_lin(b)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def _darken(h, step=0.04, max_try=12):
    """向黑方向压明度(LAB 近似:等比压 RGB),返回第一个使步进生效的色。"""
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    for _ in range(max_try):
        r, g, b = int(r * 0.93), int(g * 0.93), int(b * 0.93)
        h2 = format((r << 16) | (g << 8) | b, "06X")
        yield h2


def tune_ink2(ink2, bg, surface, need=4.5):
    """次级墨自动调墨:不及标则逐级压暗,直到在 bg 与 surface 上双达标。"""
    if _contrast(ink2, bg) >= need and _contrast(ink2, surface) >= need:
        return ink2
    for cand in _darken(ink2):
        if _contrast(cand, bg) >= need and _contrast(cand, surface) >= need:
            return cand
    return ink2


def _sat(h):
    """HSL 饱和度(0-1)。角色分配用:高饱和=候选强调,低饱和=候选文字。"""
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    mx, mn = max(r, g, b), min(r, g, b)
    l = (mx + mn) / 2
    return 0 if mx == mn else (mx - mn) / (2 - mx - mn) if l > 0.5 else (mx - mn) / (mx + mn)


def derive(theme_colors, brand, brand_en, use_when):
    """主题色板 → 四幕骨架的全部 token(含暗幕三件套自动派生与调墨)。"""
    hexes = [h.upper().lstrip("#") for h in theme_colors["hexes"]]
    if len(set(hexes)) < 3:
        raise ValueError("色板至少 3 个不同颜色(两色板无法分配角色)——补色或先跑 harmony")
    src = list(hexes)                                   # 原始声明板(明暗策略路由判据用,不被派生污染)
    ranked = sorted(hexes, key=_lum_lin)
    pale = ranked[-1]                                   # 最浅 = 亮幕大底/暗幕主字
    # PALE 必须真的浅:中明度色作大面积背景显脏(用户铁律 2026-10-22)——向白推进至相对亮度≥0.87
    for _ in range(6):
        if _contrast(pale, "FFFFFF") <= 1.30:
            break
        pale = _mix(pale, "FFFFFF", 0.45)
    hexes = [h if h != ranked[-1] else pale for h in hexes]

    night = ranked[0]                                   # 最深 = 暗幕大底/亮幕正文
    mids = [h for h in hexes if h not in (pale, night)]
    surface = ranked[-2] if len(ranked) > 2 else mids[0]
    # 强调 = 中低明度、中高饱和(简化:中位深度的那块)
    accent = ranked[len(ranked) // 2] if len(mids) >= 2 else mids[0]
    # ink2 角色:排除霓虹区(高饱和+中亮=刺眼),其余取最暗(深色高饱和不刺眼)
    mids_by_lum = sorted(mids, key=_lum_lin)           # 深→浅
    def _neon(h):
        s = _sat(h)
        l = sum(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)) / 3
        return s >= 0.60 and l > 0.45
    cand = [h for h in mids_by_lum if not _neon(h)]
    ink2_base = theme_colors.get("ink2") or (cand[0] if cand
                                             else min(mids, key=_sat))
    ink2 = tune_ink2(ink2_base, pale, surface)
    mist = ink2                                          # 暗幕次字起点
    if _contrast(mist, night) < 4.5:
        # 向浅爬坡:与 pale 混合逼近
        pr, pg, pb = (int(pale[i:i + 2], 16) for i in (0, 2, 4))
        for k in range(1, 12):
            mr, mg, mb = (int(mist[i:i + 2], 16) for i in (0, 2, 4))
            mixed = _mix(mist, pale, k / 12)
            if _contrast(mixed, night) >= 4.5:
                mist = mixed
                break
    sage = theme_colors.get("sage") or _mix(accent, pale, 0.45)
    line = _mix(surface, night, 0.12)
    card = _mix(pale, "FFFFFF", 0.55)
    return {
        "BRAND": brand, "BRAND_EN": brand_en, "USE_WHEN": use_when,
        "SRC": ",".join(src),
        "NIGHT": night, "PALE": pale, "MIST": mist, "SAGE": sage,
        "SURFACE": surface, "INK": night, "INK2": ink2, "ACCENT": accent,
        "LINE": line, "CARD": card,
        "PALETTE_DECL": ",".join(sorted({night, pale, mist, sage, surface, ink2, accent, card, line})),
    }


def _mix(a, b, k):
    """a 向 b 混 k(0..1)。"""
    ar, ag, ab = (int(a[i:i + 2], 16) for i in (0, 2, 4))
    br, bg, bb = (int(b[i:i + 2], 16) for i in (0, 2, 4))
    return format((round(ar + (br - ar) * k) << 16) | (round(ag + (bg - ag) * k) << 8) | round(ab + (bb - ab) * k), "06X")


_RING_SETS = (
    ((32, 22, 12), ()),
    ((32, 25, 18, 11), (1,)),
    ((32, 21, 10), (0,)),
    ((32, 26, 20, 14, 8), (1, 3)),
    ((32, 19), ()),
    ((32, 16), (0,)),
)


def build(tokens, seed=20260101):
    """token → 完整单文件 HTML(四幕骨架)。内容含替换标记,供 agent 填充。"""
    t = tokens
    css = """:root{
  --night:#@NIGHT@;--pale:#@PALE@;--mist:#@MIST@;--sage:#@SAGE@;
  --surface:#@SURFACE@;--ink:#@INK@;--ink2:#@INK2@;--accent:#@ACCENT@;
  --card:#@CARD@;--line:#@LINE@;
  --serif:'Noto Serif SC','Source Han Serif SC','Songti SC',Georgia,serif;
  --sans:-apple-system,'PingFang SC','Microsoft YaHei','Segoe UI',sans-serif;
  --grain:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='240' height='240'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2'/%3E%3C/filter%3E%3Crect width='240' height='240' filter='url(%23n)' opacity='0.55'/%3E%3C/svg%3E");
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*,*::before,*::after{transition:none!important;animation:none!important}.reveal{opacity:1!important;transform:none!important}}
body{background:var(--pale);color:var(--ink);font:400 16px/1.8 var(--sans)}
.wrap{max-width:1140px;margin:0 auto;padding:0 24px}
a{color:inherit;text-decoration:none}
:focus-visible{outline:3px solid var(--sage);outline-offset:3px;border-radius:2px}
.skip{position:absolute;left:-999px;top:10px;background:var(--pale);color:var(--night);padding:10px 18px;border-radius:8px;font-weight:700;z-index:99}
.skip:focus{left:10px}
.micro{font:600 11px/1.6 var(--sans);letter-spacing:.34em;text-transform:uppercase}
.night-hero{position:relative;min-height:100svh;background:var(--night);color:var(--pale);overflow:hidden;display:flex;flex-direction:column}
.night-hero::after{content:"";position:absolute;inset:0;background-image:var(--grain);opacity:.07;pointer-events:none}
.night-hero .wrap{position:relative;z-index:2;flex:1;display:flex;flex-direction:column;justify-content:center;padding-top:110px;padding-bottom:80px;width:100%}
.night-top{position:absolute;top:0;left:0;right:0;z-index:3;display:flex;align-items:center;justify-content:space-between;gap:16px;padding:20px clamp(20px,4vw,48px)}
.night-top .brand{display:flex;align-items:center;gap:10px;font-family:var(--serif);font-weight:700;font-size:18px;color:var(--pale)}
.night-top .seal{width:30px;height:30px;border-radius:8px;background:var(--pale);color:var(--night);display:flex;align-items:center;justify-content:center;font-size:15px}
.night-top nav{display:flex;gap:26px;font-size:13.5px;font-weight:600}
.night-top nav a{color:var(--mist)}.night-top nav a:hover{color:var(--pale)}
.hero-eyebrow{color:var(--sage);margin-bottom:26px}
.night-hero h1{font-family:var(--serif);font-weight:900;font-size:clamp(56px,11.5vw,142px);line-height:1.06;margin-bottom:8px}
.night-hero h1 .dim{color:var(--mist)}
.hero-row{display:flex;align-items:flex-end;justify-content:space-between;gap:40px;margin-top:34px;flex-wrap:wrap}
.hero-lede{max-width:520px;font-size:16.5px;line-height:1.9;color:var(--mist)}
.hero-lede b{color:var(--pale);font-weight:600}
.hero-cta{display:flex;align-items:center;gap:22px;flex-wrap:wrap}
.btn-pale{display:inline-block;background:var(--pale);color:var(--night);font-weight:800;font-size:15px;padding:15px 34px;border-radius:12px;transition:transform .18s ease}
.btn-pale:hover{transform:translateY(-2px)}
.btn-ghost-d{border:1.5px solid var(--sage);color:var(--sage);padding:14px 30px;border-radius:12px;font-weight:700;font-size:14.5px;display:inline-block;transition:background .18s ease}
.btn-ghost-d:hover{background:rgba(174,195,176,.12)}
.hero-scarcity{font-size:12.5px;color:var(--mist)}
.hero-rings{position:absolute;right:-16vw;top:50%;transform:translateY(-50%);width:min(62vw,760px);height:min(62vw,760px);z-index:1;pointer-events:none}
.hero-rings circle{fill:none;stroke-width:1.6}
.r-grow{stroke-dasharray:2200;stroke-dashoffset:2200;animation:grow 2.6s cubic-bezier(.2,.6,.2,1) forwards}
.r-grow.d1{animation-delay:.15s}.r-grow.d2{animation-delay:.4s}.r-grow.d3{animation-delay:.7s}.r-grow.d4{animation-delay:1s}.r-grow.d5{animation-delay:1.3s}
@keyframes grow{to{stroke-dashoffset:0}}
.side-label{position:absolute;right:26px;bottom:120px;writing-mode:vertical-rl;letter-spacing:.5em;font:600 11px var(--sans);color:var(--mist);z-index:2}
@media (max-width:900px){.side-label,.hero-rings{display:none}.night-hero h1{font-size:clamp(52px,15vw,96px)}}
.scroll-cue{position:absolute;bottom:28px;left:50%;transform:translateX(-50%);z-index:2;color:var(--mist);font:600 11px var(--sans);letter-spacing:.3em;display:flex;flex-direction:column;align-items:center;gap:8px}
.scroll-cue i{display:block;width:1px;height:34px;background:var(--mist);animation:cue 1.8s ease-in-out infinite}
@keyframes cue{0%,100%{transform:scaleY(.35);transform-origin:top}50%{transform:scaleY(1);transform-origin:top}}
.reveal{opacity:0;transform:translateY(30px);transition:opacity .9s ease,transform .9s ease}
.reveal.in{opacity:1;transform:none}
.dawn{background:var(--pale);color:var(--ink)}
section{padding:96px 0 30px;scroll-margin-top:20px}
.shead{display:flex;align-items:baseline;gap:16px;flex-wrap:wrap}
.sno{font:800 13px var(--sans);color:var(--accent);letter-spacing:.16em}
.shead h2{font-family:var(--serif);font-weight:900;font-size:clamp(30px,4.4vw,46px)}
.ssub{color:var(--ink2);font-size:15.5px;max-width:620px;margin:14px 0 44px}
.works{display:grid;grid-template-columns:repeat(12,1fr);gap:26px}
.work{grid-column:span 4;background:var(--card);border-radius:16px;padding:26px 26px 20px;position:relative;overflow:hidden;transition:transform .2s ease,box-shadow .2s ease}
.work:nth-child(1){grid-column:span 5}
.work:nth-child(3){grid-column:span 3}
.work:hover{transform:translateY(-6px);box-shadow:0 24px 60px rgba(0,0,0,.16)}
.work .ghost{position:absolute;right:14px;top:2px;font:900 84px var(--serif);color:var(--surface);line-height:1;pointer-events:none}
.work .rings{width:74px;height:74px;display:block;margin:6px 0 16px;position:relative}
.work h3{font-family:var(--serif);font-size:20px;font-weight:900;margin-bottom:4px;position:relative}
.work .meta{font-size:13.5px;color:var(--ink2);position:relative}
.work .row{display:flex;justify-content:space-between;align-items:baseline;margin-top:16px;border-top:1px solid var(--line);padding-top:14px;position:relative}
.work .price{font-family:var(--serif);font-weight:900;font-size:19px}
.work .lead{font-size:12.5px;color:var(--ink2)}
@media (max-width:900px){.works{grid-template-columns:1fr 1fr}.work,.work:nth-child(1),.work:nth-child(3){grid-column:auto}}
@media (max-width:600px){.works{grid-template-columns:1fr}.work,.work:nth-child(1),.work:nth-child(3){grid-column:auto}}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:30px;counter-reset:step}
.step{border-top:3px solid var(--ink);padding-top:18px}
.step::before{counter-increment:step;content:"0" counter(step);font:900 15px var(--sans);color:var(--accent);letter-spacing:.12em}
.step h3{font-family:var(--serif);font-size:22px;margin:8px 0 10px}
.step p{font-size:14.5px;color:var(--ink2)}
.step .law{margin-top:14px;font-size:12.5px;background:var(--surface);border-radius:8px;padding:8px 13px;display:inline-block}
table.gridtable{width:100%;border-collapse:collapse;background:var(--card);border-radius:16px;overflow:hidden;font-size:14.5px}
.gridtable caption{text-align:left;font-size:13px;color:var(--ink2);padding:0 0 10px 4px}
.gridtable th{background:var(--surface);text-align:left;font-weight:700;padding:13px 20px}
.gridtable td{padding:13px 20px;border-top:1px solid var(--line)}
.gridtable td.num{font-variant-numeric:tabular-nums;font-weight:700}
.night-voice{position:relative;background:var(--night);color:var(--pale);padding:96px 0;overflow:hidden}
.night-voice::after{content:"";position:absolute;inset:0;background-image:var(--grain);opacity:.07;pointer-events:none}
.night-voice .wrap{position:relative;z-index:2}
.night-voice blockquote{font-family:var(--serif);font-weight:700;font-size:clamp(26px,4.6vw,46px);line-height:1.5;max-width:900px}
.night-voice blockquote em{font-style:normal;color:var(--sage)}
.night-voice footer{margin-top:26px;font:400 14px var(--sans);color:var(--mist)}
.night-book{position:relative;background:var(--night);color:var(--pale);padding:96px 0;overflow:hidden}
.night-book::after{content:"";position:absolute;inset:0;background-image:var(--grain);opacity:.07;pointer-events:none}
.night-book .wrap{position:relative;z-index:2;display:flex;gap:40px;align-items:center;justify-content:space-between;flex-wrap:wrap}
.night-book h2{font-family:var(--serif);font-weight:900;font-size:clamp(30px,4.6vw,50px);line-height:1.25;margin-bottom:14px}
.night-book h2 em{font-style:normal;color:var(--sage)}
.night-book p{color:var(--mist);font-size:15.5px;max-width:540px;line-height:1.9}
.night-book small{display:block;margin-top:14px;color:var(--mist);font-size:12.5px}
.night-book .btn-pale{font-size:16px;padding:17px 40px}
footer.site{background:var(--night);color:var(--mist);border-top:1px solid rgba(159,179,188,.22);padding:26px 0 54px;font-size:13px;display:flex;gap:12px 30px;flex-wrap:wrap;justify-content:space-between}
@media (max-width:640px){body{font-size:15px}section{padding:70px 0 16px}.night-top nav{display:none}}
"""
    css = css.replace("@NIGHT@", t["NIGHT"]).replace("@PALE@", t["PALE"]).replace("@MIST@", t["MIST"]) \
             .replace("@SAGE@", t["SAGE"]).replace("@SURFACE@", t["SURFACE"]).replace("@INK@", t["INK"]) \
             .replace("@INK2@", t["INK2"]).replace("@ACCENT@", t["ACCENT"]).replace("@CARD@", t["CARD"]) \
             .replace("@LINE@", t["LINE"])

    rings = []
    for i, (rs, marks) in enumerate(_RING_SETS):
        marks_att = " ".join(f'cx="37" cy="37" r="{r}" stroke="#ACCENT_LO"' for r in marks)
        base = " ".join(f'cx="37" cy="37" r="{r}"' for r in rs if r not in marks)
        g = f'<g fill="none" stroke="#SAGE_LO" stroke-width="3">{base}</g>'
        if marks:
            g += f'<g fill="none" stroke="#ACCENT_LO" stroke-width="3">{marks_att}</g>'
        rings.append(g.replace("#SAGE_LO", "#AEC3B0" if t["SAGE"] == "AEC3B0" else "#" + t["SAGE"])
                        .replace("#ACCENT_LO", "#" + t["ACCENT"]))
    cards = []
    for i, rg in enumerate(rings):
        cards.append(f'''        <article class="work reveal">
          <span class="ghost" aria-hidden="true">{i + 1}</span>
          <!-- 替换:以下为真实作品/条目 -->
          <svg class="rings" viewBox="0 0 74 74" aria-hidden="true">{rg}<circle cx="37" cy="37" r="4.5" fill="#{t["INK"]}"/></svg>
          <h3>条目标题 {i + 1}</h3>
          <p class="meta">属性一 · 属性二 · 规格</p>
          <div class="row"><span class="price">¥ —</span><span class="lead">周期 — 天</span></div>
        </article>''')
    cards_html = "\n".join(cards)

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t["BRAND"]} · {t["USE_WHEN"]}</title>
<!--
  scaffold 0.9(aesthete-agent 表现力骨架) · 主题色板(声明): {t["PALETTE_DECL"]}
  四幕明暗旅程 + 颗粒 + 巨字对微字 + 滚动揭示;渐变禁令已遵守。
  待替换处均标有"替换"注释;替换后跑 report/evidence 验收。
-->
<style>{css}</style>
</head>
<body>
<a class="skip" href="#main">跳到主要内容</a>
<header class="night-hero">
  <div class="night-top">
    <a class="brand" href="#"><span class="seal" aria-hidden="true">{t["BRAND"][0]}</span>{t["BRAND"]}</a>
    <nav aria-label="主导航"><a href="#works">作品</a><a href="#craft">方法</a><a href="#contact">预约</a></nav>
    <span class="micro">EST. 2026</span>
  </div>
  <svg class="hero-rings" viewBox="0 0 760 760" aria-hidden="true">
    <g stroke="#{t["SAGE"]}">
      <circle class="r-grow" cx="380" cy="380" r="360"/>
      <circle class="r-grow d1" cx="380" cy="380" r="290" stroke="#{t["MIST"]}"/>
      <circle class="r-grow d2" cx="380" cy="380" r="222"/>
      <circle class="r-grow d3" cx="380" cy="380" r="156" stroke="#{t["PALE"]}" stroke-width="2.2"/>
      <circle class="r-grow d4" cx="380" cy="380" r="96"/>
      <circle class="r-grow d5" cx="380" cy="380" r="44" stroke="#{t["PALE"]}" stroke-width="2.4"/>
    </g>
    <circle cx="380" cy="380" r="9" fill="#{t["PALE"]}"/>
  </svg>
  <span class="side-label" aria-hidden="true">{t["BRAND"]} —— {t["USE_WHEN"]}</span>
  <div class="wrap">
    <p class="micro hero-eyebrow reveal in">{t["BRAND_EN"]} · 一句话定位(替换)</p>
    <h1>巨字主张上行，<br><span class="dim">下行接住它。</span></h1>
    <div class="hero-row">
      <p class="hero-lede">两行以内的价值陈述,给一个具体的、可验证的承诺。<b>加粗句只给重点</b>——它会被读得最仔细。</p>
      <div class="hero-cta">
        <a class="btn-pale" href="#contact">主行动(替换)</a>
        <a class="btn-ghost-d" href="#works">次行动</a>
      </div>
    </div>
    <p class="hero-scarcity" style="margin-top:20px">真实稀缺注(替换):如"本周仅余 N 个档期"</p>
  </div>
  <div class="scroll-cue" aria-hidden="true">SCROLL<i></i></div>
</header>
<main id="main">
<div class="dawn">
  <div class="wrap">
    <section id="works">
      <div class="shead reveal"><span class="sno">01</span><h2>精选(替换节名)</h2></div>
      <p class="ssub reveal">节导语:两行以内,说清这一节给用户什么。</p>
      <div class="works">
{cards_html}
      </div>
    </section>
    <section id="craft">
      <div class="shead reveal"><span class="sno">02</span><h2>方法三步(替换节名)</h2></div>
      <p class="ssub reveal">为什么快不了/为什么必须这样做——写真实的约束,不写口号。</p>
      <div class="steps reveal">
        <div class="step"><h3>步骤一</h3><p>做什么,为什么不能省。</p><span class="law">规矩:一条可验证的标准</span></div>
        <div class="step"><h3>步骤二</h3><p>做什么,为什么不能省。</p><span class="law">规矩:一条可验证的标准</span></div>
        <div class="step"><h3>步骤三</h3><p>做什么,为什么不能省。</p><span class="law">规矩:一条可验证的标准</span></div>
      </div>
    </section>
  </div>
</div>
<section class="night-voice" aria-label="证言">
  <div class="wrap">
    <p class="micro" style="color:var(--mist);margin-bottom:30px">03 · 证言</p>
    <blockquote class="reveal">「一句客户原话,带时间与细节。<em>强调句用次级色。</em>」</blockquote>
    <footer>—— 客户署名,年份,回访时间</footer>
  </div>
</section>
<section class="night-book" id="contact">
  <div class="wrap">
    <div>
      <h2>收尾行动,<br>先<em>具体</em>,再干脆。</h2>
      <p>说明第一步做什么、成本与承诺;不合适也给出路。</p>
      <small>联系方式(替换)　|　营业/响应说明</small>
    </div>
    <a class="btn-pale" href="#">主行动</a>
  </div>
</section>
<footer class="site">
  <div class="wrap" style="display:flex;gap:12px 30px;flex-wrap:wrap;justify-content:space-between;width:100%">
    <span>© 2026 {t["BRAND"]} {t["BRAND_EN"]}</span>
    <span>配色:scaffold 机械验证(PASS · 指纹绑定)——替换内容后重跑 report</span>
  </div>
</footer>
</main>
<script>
document.documentElement.classList.add("js");
const io = new IntersectionObserver((es) => {{
  es.forEach((e) => {{ if (e.isIntersecting) {{ e.target.classList.add("in"); io.unobserve(e.target); }} }});
}}, {{ threshold: 0.12 }});
document.querySelectorAll(".reveal").forEach((el) => io.observe(el));
</script>
</body>
</html>
'''
    return html


def theme_tokens(theme_record, brand, brand_en):
    """themes.json 条目 → derive() 所需输入(hexes + 可选 voice 色提示)。"""
    c = theme_record["colors"]
    hexes = [v.lstrip("#").upper() for v in c.values()]
    return derive({"hexes": hexes, "ink2": c.get("ink2", "").lstrip("#").upper(),
                   "sage": c.get("honey", "").lstrip("#").upper()},
                  brand or theme_record.get("name_en") or theme_record["name"],
                  brand_en or theme_record.get("name_en", ""),
                  theme_record.get("use_when", ""))
