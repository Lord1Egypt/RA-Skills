# -*- coding: utf-8 -*-
"""type_kit.py — typescale 命令实现体:CJK 友好的字阶生成器。

模块等比(ratio 1.125-1.5)向上生成展示级、向下生成辅助级,12px 硬下限
(低于即钳制并留痕);行高配对(展示 1.15/标题 1.3/正文 1.7/辅助 1.5,CJK 正文区间);
数字场景给 tabular-nums 令牌。产出 tokens CSS + 中英混排样张 HTML。
零依赖 stdlib,被 palette_forge.py 的 cmd_typescale 调用。
"""
import hashlib
import json
import math

STEPS = ["3xl", "2xl", "xl", "lg", "base", "sm", "xs"]
FLUID_STEPS = ("3xl", "2xl", "xl", "lg")
LINE_HEIGHT = {"display": 1.15, "heading": 1.3, "body": 1.7, "caption": 1.5}
ROLES = {"3xl": "display", "2xl": "display", "xl": "heading", "lg": "heading",
         "base": "body", "sm": "caption", "xs": "caption"}


def _fluid(target_px, floor=12.0):
    """display 级流体字阶:375px 视口取 0.62×,1440px 视口取 1.15×,中段线性。"""
    lo = max(target_px * 0.62, floor)
    hi = target_px * 1.15
    vw = (hi - lo) / (14.40 - 3.75)
    base = lo - 3.75 * vw
    rem = lambda x: round(x / 16, 3)
    return (f"clamp({rem(lo)}rem, calc({rem(base)}rem + {round(vw, 3)}vw), {rem(hi)}rem)")


def build(base=16.0, ratio=1.25, floor=12.0, fluid=False):
    """→ (tokens dict, checks dict)。向上 4 级向下 2 级,低于下限钳制并记录。"""
    order = {"3xl": 4, "2xl": 3, "xl": 2, "lg": 1, "base": 0, "sm": -1, "xs": -2}
    tokens, clamped = {}, []
    for name in STEPS:
        raw = base * (ratio ** order[name])
        v = max(raw, floor)
        if v > raw + 1e-9:
            clamped.append(name)
        tokens[name] = {"px": round(v, 1), "lh": LINE_HEIGHT[ROLES[name]], "role": ROLES[name]}
        if fluid and name in FLUID_STEPS:
            tokens[name]["fluid"] = _fluid(v, floor)
    sizes = [tokens[s]["px"] for s in STEPS]
    checks = {
        "base": base, "ratio": ratio, "floor": floor, "fluid": bool(fluid),
        "monotonic": all(sizes[i] > sizes[i + 1] for i in range(len(sizes) - 1)),
        "clamped_steps": clamped,
        "display_vs_body": round(sizes[0] / sizes[4], 2),
    }
    checks["verdict"] = "PASS" if checks["monotonic"] else "FAIL"
    return tokens, checks


def emit(name="", brand="", base=16.0, ratio=1.25, floor=12.0, out_base="typescale", fluid=False):
    """tokens CSS + 样张 HTML + JSON。fluid=True:display 级发出流体 clamp。"""
    tokens, checks = build(base, ratio, floor, fluid=fluid)
    verdict = checks["verdict"]
    lines = [
        "/* %s — aesthete-agent typescale(0.13.0)" % (name or "type ramp"),
        "   基准 %.0fpx · 等比 %.3f · 下限 %.0fpx%s · %s" % (base, ratio, floor,
          ("(钳制: %s)" % ", ".join(checks["clamped_steps"])) if checks["clamped_steps"] else "",
          "流体字阶(display 级 clamp)" if checks["fluid"] else "固定字阶"),
        "   行高:展示 1.15 / 标题 1.3 / 正文 1.7(CJK 区间) / 辅助 1.5 */",
        ":root{",
    ]
    for s in STEPS:
        t = tokens[s]
        var = "--text-" + s
        val = t.get("fluid") or ("%gpx" % t["px"])
        lines.append("  %s:%s/%s;" % (var, val, t["lh"]))
    lines += [
        "  --lh-body:1.7;  /* 中文正文 1.65-1.8;行长约 35-42 字 */",
        "  --track-display:-0.02em;  /* Latin 巨标收紧 */",
        "  --track-caps:0.1em;       /* 全大写小标签放宽(字号越小加越多) */",
        "  --track-zh-display:0.01em;/* 中文巨标;中文禁负字距 */",
        "  --font-tnum:{font-variant-numeric:tabular-nums};  /* 数据表/指标列专用 */",
        "}",
        "/* 排印底座(语法见 references/typography-system.md;均渐进/安全) */",
        ":lang(zh){text-autospace:normal;line-break:strict}",
        "h1,h2{text-wrap:balance;max-inline-size:18ch}",
        "p{text-wrap:pretty}",
        ':lang(zh) :is(h1,h2,h3){font-feature-settings:"palt" 1}',
        "/* 用法:display 级令牌已含流体 clamp;减动效:@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}} */",
    ]
    css = "\n".join(lines) + "\n"

    spec = []
    sample = [("3xl", "巨字主张,一屏一句", "Display 144"),
              ("2xl", "章节大标", "Heading XL"),
              ("xl", "小节标题:说清这一节给什么", "Heading L"),
              ("lg", "卡片标题与重点句", "Heading S"),
              ("base", "正文:两行以内说清一件事,给可验证的承诺。数字 0123456789 对齐靠 tabular-nums。", "Body"),
              ("sm", "辅助说明:注脚、来源、单位。", "Caption"),
              ("xs", "最小字号:仅限徽标/时间戳,正文禁用。", "Micro")]
    for s, zh, en in sample:
        t = tokens[s]
        spec.append(
            f'<p style="font-size:{t["px"]}px;line-height:{t["lh"]};margin:0 0 14px">'
            f'<b>{zh}</b> <span style="opacity:.55">{en}</span></p>')
    tnum = '<table style="font-size:15px;border-collapse:collapse"><tr><th style="text-align:left;padding:4px 14px 4px 0">指标</th><th style="text-align:right">数值</th></tr>'
    for k, v in (("对比度", "12.63:1"), ("系列数", "8"), ("达标率", "100%")):
        tnum += f'<tr><td style="padding:4px 14px 4px 0">{k}</td><td style="text-align:right;font-variant-numeric:tabular-nums">{v}</td></tr>'
    tnum += "</table>"
    html = f"""<!doctype html><html lang="zh"><head><meta charset="utf-8"><title>typescale · {name or "ramp"}</title></head>
<body style="font:16px/1.7 system-ui,'PingFang SC','Microsoft YaHei',sans-serif;margin:0;padding:32px;background:#FAFAF7;color:#222;max-width:860px">
<h2 style="margin:0 0 4px">typescale · {name or "ramp"} <span style="font-size:13px;color:#777">裁决 {verdict}</span></h2>
<p style="color:#666;margin:0 0 24px">展示级与辅助级共用一条等比;中文正文行高 1.7,行长约 35-42 字。</p>
{''.join(spec)}
<h3 style="font-size:15px;margin:24px 0 8px">数字列(tabular-nums)</h3>
{tnum}
<p style="font-size:12.5px;color:#888;margin-top:24px">指纹暂无·纯排版产物 · aesthete-agent typescale(0.10.0)</p>
</body></html>"""
    payload = {"name": name, "tokens": {k: v for k, v in tokens.items()},
               "checks": checks, "verdict": verdict, "fluid": bool(fluid)}
    payload["fingerprint"] = hashlib.sha256(
        ("aesthete-typescale/v1|%.1f|%.3f|%.0f|%s" % (base, ratio, floor, verdict)).encode("utf-8")).hexdigest()
    with open(out_base + ".css", "w", encoding="utf-8", newline="\n") as f:
        f.write(css)
    with open(out_base + ".html", "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    with open(out_base + ".json", "w", encoding="utf-8", newline="\n") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)
    return payload
