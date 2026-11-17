#!/usr/bin/env python3
"""Render an assessment.json into a self-contained, professionally-styled report.

Deterministic presentation layer: the model produces assessment.json (per
reference/assessment-prompt.md), this script turns it into a polished HTML report
(indigo accent, semantic amber/green, clean hairline tables — design language
adapted from an internal PRD). Brand-neutral: no product branding on the report.
No third-party dependencies.

Usage:
    python scripts/render_report.py assessment.json --out report.html
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys

# --- design tokens (indigo accent + semantic colors, adapted from a PRD) ------
CSS = """
:root{
  --ink:#111827; --navy:#1E293B; --muted:#6B7280; --faint:#9CA3AF;
  --line:#E9EBF0; --line2:#E5E7EB; --subtle:#F9FAFB;
  --blue:#2B54E0; --blue-ink:#1E40AF; --blue-bg:#EEF2FF;
  --green:#12A150; --green-bg:#E9F7EF;
  --amber:#B7791F; --amber-strong:#C77700; --amber-bg:#FDF3E5;
  --red:#DC2626; --red-bg:#FCEBEA; --gray-bg:#F3F4F6;
}
*{box-sizing:border-box}
body{margin:0;background:#F4F5F8;color:var(--ink);
  font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",
  "Segoe UI",Roboto,Helvetica,Arial,sans-serif;line-height:1.62;
  font-size:15px;-webkit-font-smoothing:antialiased;
  -webkit-print-color-adjust:exact;print-color-adjust:exact;}

/* one-click PDF export */
.print-btn{position:fixed;top:18px;right:18px;z-index:50;background:var(--blue);
  color:#fff;border:0;border-radius:8px;padding:9px 15px;font:700 13.5px inherit;
  font-family:inherit;cursor:pointer;box-shadow:0 2px 10px rgba(43,84,224,.35)}
.print-btn:hover{background:#2247c9}
@page{size:A4;margin:12mm}
@media print{
  html,body{background:#fff}
  .print-btn{display:none}
  .page{box-shadow:none;margin:0;max-width:none;border-radius:0;padding:0}
  .hero,.call,.q,.hi li,.check li,tr,.sec{break-inside:avoid}
  h1.title,h2,.sec{break-after:avoid}
}
.page{max-width:860px;margin:32px auto;background:#fff;border-radius:14px;
  box-shadow:0 1px 3px rgba(17,24,39,.06),0 8px 32px rgba(17,24,39,.06);
  padding:56px 60px 64px;}
@media(max-width:640px){.page{padding:32px 22px;margin:0;border-radius:0}}

/* header */
.eyebrow{display:inline-block;font-size:11.5px;font-weight:700;letter-spacing:.08em;
  color:var(--blue);background:var(--blue-bg);padding:4px 11px;border-radius:6px}
h1.title{font-size:30px;font-weight:800;letter-spacing:-.01em;margin:18px 0 6px}
.subtitle{color:var(--muted);font-size:15px;margin:0 0 22px}
.meta{display:grid;grid-template-columns:repeat(4,1fr);border:1px solid var(--line2);
  border-radius:10px;overflow:hidden}
.meta div{padding:12px 16px;border-right:1px solid var(--line2)}
.meta div:last-child{border-right:0}
.meta .k{font-size:11px;color:var(--faint);letter-spacing:.04em;margin-bottom:3px}
.meta .v{font-weight:700;font-size:14px}
@media(max-width:640px){.meta{grid-template-columns:repeat(2,1fr)}
  .meta div:nth-child(2){border-right:0}}

hr.rule{border:0;border-top:1px solid var(--line2);margin:34px 0 26px}

/* section heads */
.sec{display:flex;align-items:baseline;gap:10px;margin:32px 0 16px}
.sec .n{color:var(--blue);font-weight:800;font-size:13px;font-variant-numeric:tabular-nums}
.sec h2{font-size:19px;font-weight:800;margin:0}

/* hero conclusion */
.hero{display:flex;gap:26px;align-items:center;background:var(--subtle);
  border:1px solid var(--line);border-radius:12px;padding:22px 26px}
.score{flex:0 0 auto;text-align:center;min-width:132px}
.ring{width:118px;height:118px;border-radius:50%;display:flex;align-items:center;
  justify-content:center;margin:0 auto}
.ring .inner{width:96px;height:96px;border-radius:50%;background:#fff;
  display:flex;flex-direction:column;align-items:center;justify-content:center}
.ring .num{font-size:34px;font-weight:800;line-height:1;font-variant-numeric:tabular-nums}
.ring .of{font-size:11px;color:var(--faint);margin-top:3px}
.hero .right{flex:1}
.pill{display:inline-block;padding:5px 14px;border-radius:999px;font-weight:700;
  font-size:13.5px;letter-spacing:.01em}
.hero .oneline{margin:12px 0 0;color:var(--navy);font-size:15px;
  padding-left:13px;border-left:3px solid var(--line2)}

/* generic pills / badges */
.badge{display:inline-flex;align-items:center;gap:5px;padding:3px 11px;border-radius:999px;
  font-size:12.5px;font-weight:700}
.b-green{background:var(--green-bg);color:var(--green)}
.b-blue{background:var(--blue-bg);color:var(--blue-ink)}
.b-amber{background:var(--amber-bg);color:var(--amber-strong)}
.b-red{background:var(--red-bg);color:var(--red)}
.b-gray{background:var(--gray-bg);color:var(--muted)}

/* callout */
.call{border-radius:10px;padding:14px 18px;margin:6px 0 4px;font-size:14.5px}
.call .h{font-weight:700;font-size:13px;margin-bottom:5px}
.call.blue{background:var(--blue-bg)}.call.blue .h{color:var(--blue-ink)}
.call.green{background:var(--green-bg)}.call.green .h{color:var(--green)}
.call.amber{background:var(--amber-bg);border-left:3px solid var(--amber-strong)}
.call.amber .h{color:var(--amber-strong)}

/* tables */
table{width:100%;border-collapse:collapse;margin:6px 0;font-size:14px}
th{text-align:left;font-size:11.5px;font-weight:600;color:var(--faint);
  letter-spacing:.04em;padding:8px 12px;border-bottom:1px solid var(--line2)}
td{padding:12px;border-bottom:1px solid var(--line);vertical-align:top}
tr:last-child td{border-bottom:0}
.dim-name{font-weight:700}
.w{color:var(--faint);font-size:12px;font-variant-numeric:tabular-nums}
.bar{height:6px;border-radius:4px;background:var(--line2);margin-top:7px;overflow:hidden}
.bar > i{display:block;height:100%;border-radius:4px}
.sc{font-weight:800;font-size:16px;font-variant-numeric:tabular-nums}
.pos{color:var(--green);font-weight:700}.neg{color:var(--amber-strong);font-weight:700}
.lbl{font-weight:700}
/* eligibility checklist */
.check{list-style:none;padding:0;margin:14px 0 0}
.check li{display:flex;gap:11px;padding:11px 2px;border-bottom:1px solid var(--line);
  align-items:flex-start}
.check li:last-child{border-bottom:0}
.check .ic{flex:0 0 auto;font-size:15px;line-height:1.55}
.check .txt{flex:1}
.check .note{color:var(--muted);font-size:13px;margin-top:3px;line-height:1.5}

.hi{list-style:none;padding:0;margin:0}
.hi li{background:var(--blue-bg);border-radius:9px;padding:11px 15px;margin:8px 0;
  color:var(--navy);font-size:14.5px}
.q{margin:10px 0;padding:13px 16px;border:1px solid var(--line);border-radius:10px;
  background:var(--subtle)}
.q .topic{font-size:11.5px;color:var(--blue-ink);background:var(--blue-bg);
  padding:2px 9px;border-radius:999px;font-weight:700;margin-right:8px}
.foot{margin-top:40px;padding-top:16px;border-top:1px solid var(--line2);
  color:var(--faint);font-size:12px;display:flex;justify-content:space-between}
strong{font-weight:700}
"""

GRADE_CLASS = {"强烈推荐": "b-green", "推荐面试": "b-blue",
               "保持观望": "b-amber", "建议拒绝": "b-red"}
ELIG = {"通过": ("b-green", "✅ 通过"), "存在疑点": ("b-amber", "🟡 存在疑点"),
        "不通过": ("b-red", "❌ 不通过")}
RISK_CLASS = {"高": "b-red", "中": "b-amber", "低": "b-gray"}


def _item_icon(st) -> str:
    if st in (True, "pass", "通过", "yes", "ok"):
        return "✅"
    if st in ("doubt", "疑点", "存在疑点", "warn"):
        return "🟡"
    if st in (False, "fail", "不通过", "no"):
        return "❌"
    return "•"


_HALF2FULL = {",": "，", ";": "；", ":": "：", "!": "！", "?": "？"}


def _is_cjk(ch: str) -> bool:
    if not ch:
        return False
    o = ord(ch)
    return (0x4E00 <= o <= 0x9FFF or 0x3400 <= o <= 0x4DBF   # ideographs
            or 0x3000 <= o <= 0x303F or 0xFF00 <= o <= 0xFFEF)  # CJK/fullwidth punct


def cjk_punct(s: str) -> str:
    """Half-width , ; : ! ? adjacent to CJK → full-width, so Chinese text isn't
    cramped. Latin contexts (URLs, 'MySQL,Redis') keep half-width."""
    out = []
    for i, ch in enumerate(s):
        if ch in _HALF2FULL:
            prev = s[i - 1] if i else ""
            nxt = s[i + 1] if i + 1 < len(s) else ""
            if _is_cjk(prev) or _is_cjk(nxt):
                out.append(_HALF2FULL[ch])
                continue
        out.append(ch)
    return "".join(out)


def esc(s) -> str:
    """Normalize CJK punctuation, HTML-escape, honor **bold** and newlines."""
    s = cjk_punct(str(s or ""))
    s = html.escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return s.replace("\n", "<br>")


def score_color(n: int) -> str:
    if n >= 80:
        return "var(--green)"
    if n >= 65:
        return "var(--blue)"
    if n >= 50:
        return "var(--amber-strong)"
    return "var(--red)"


def ring(n: int) -> str:
    c = score_color(n)
    deg = max(0, min(100, n)) * 3.6
    return (f'<div class="ring" style="background:conic-gradient({c} {deg}deg,'
            f'var(--line2) 0)"><div class="inner"><div class="num" '
            f'style="color:{c}">{n}</div><div class="of">/ 100</div></div></div>')


def render(a: dict) -> str:
    cand = esc(a.get("candidate", "候选人"))
    pos = esc(a.get("position", "目标岗位"))
    conc = a.get("conclusion", {})
    score = int(conc.get("score", 0))
    grade = conc.get("grade", "")
    gcls = GRADE_CLASS.get(grade, "b-gray")

    # meta box
    meta_date = esc(a.get("date", ""))
    src = esc(a.get("source", ""))
    meta = (
        f'<div class="meta">'
        f'<div><div class="k">候选人</div><div class="v">{cand}</div></div>'
        f'<div><div class="k">目标岗位</div><div class="v">{pos}</div></div>'
        f'<div><div class="k">评估等级</div><div class="v">{esc(grade)}</div></div>'
        f'<div><div class="k">综合匹配分</div><div class="v">{score} / 100</div></div>'
        f'</div>'
    )

    # 1. conclusion hero
    hero = (
        f'<div class="hero"><div class="score">{ring(score)}</div>'
        f'<div class="right"><span class="pill {gcls}">{esc(grade)}</span>'
        f'<p class="oneline">{esc(conc.get("summary",""))}</p></div></div>'
    )

    # 2. eligibility — checklist if provided, else fall back to a paragraph
    elig = a.get("eligibility", {})
    ecls, elabel = ELIG.get(elig.get("status", ""), ("b-gray", esc(elig.get("status", "—"))))
    checks = elig.get("checks")
    if checks:
        lis = ""
        for c in checks:
            note = (f'<div class="note">{esc(c.get("note",""))}</div>'
                    if c.get("note") else "")
            lis += (f'<li><span class="ic">{_item_icon(c.get("status", c.get("ok")))}'
                    f'</span><span class="txt">{esc(c.get("item",""))}{note}</span></li>')
        inner = f'<ul class="check">{lis}</ul>'
        if elig.get("note"):
            inner += f'<p class="w" style="margin-top:12px">{esc(elig["note"])}</p>'
    else:
        inner = f'<p style="margin:14px 0 0">{esc(elig.get("analysis",""))}</p>'
    elig_html = f'<span class="badge {ecls}">{elabel}</span>{inner}'

    # 3. dimensions table
    rows = ""
    for d in a.get("dimensions", []):
        sc = int(d.get("score", 0))
        c = score_color(sc)
        detail = f'<span class="lbl">{esc(d.get("pos_label","优势"))}:</span> ' \
                 f'<span class="pos">{esc(d.get("pos",""))}</span>'
        if d.get("neg"):
            detail += f'<br><span class="lbl">{esc(d.get("neg_label","差距"))}:</span> ' \
                      f'<span class="neg">{esc(d.get("neg",""))}</span>'
        rows += (
            f'<tr><td class="dim-name">{esc(d.get("name",""))}<div class="w">'
            f'权重 {esc(d.get("weight",""))}%</div></td>'
            f'<td><span class="sc" style="color:{c}">{sc}</span>'
            f'<div class="bar"><i style="width:{max(0,min(100,sc))}%;background:{c}"></i></div></td>'
            f'<td>{detail}</td></tr>'
        )
    dims = (
        '<table><thead><tr><th>评估维度</th><th style="width:120px">得分</th>'
        '<th>详细分析</th></tr></thead><tbody>' + rows + '</tbody></table>'
    )

    # 4. highlights
    hi = "".join(f'<li>{esc(h)}</li>' for h in a.get("highlights", []))
    hi_html = f'<ul class="hi">{hi}</ul>' if hi else '<p class="w">—</p>'

    # 5. risks
    rrows = ""
    for r in a.get("risks", []):
        lv = r.get("level", "低")
        rrows += (
            f'<tr><td><span class="badge {RISK_CLASS.get(lv,"b-gray")}">{esc(lv)}</span></td>'
            f'<td class="lbl">{esc(r.get("category",""))}</td>'
            f'<td>{esc(r.get("desc",""))}</td></tr>'
        )
    risks = (
        '<table><thead><tr><th style="width:64px">风险等级</th>'
        '<th style="width:120px">类别</th><th>风险描述</th></tr></thead><tbody>'
        + (rrows or '<tr><td colspan="3" class="w">未识别明显风险。</td></tr>')
        + '</tbody></table>'
    )

    # 6. interview questions
    qs = ""
    for i, q in enumerate(a.get("interview_questions", []), 1):
        topic = f'<span class="topic">{esc(q.get("topic"))}</span>' if q.get("topic") else ""
        qs += f'<div class="q"><strong>{i}.</strong> {topic}{esc(q.get("question",""))}</div>'

    body = f"""
<div class="eyebrow">内部评估 · 保密</div>
<h1 class="title">候选人内部评估报告</h1>
<p class="subtitle">{cand} · 目标岗位「{pos}」 — 首席人才顾问深度评估</p>
{meta}
<hr class="rule">

<div class="sec"><span class="n">01</span><h2>核心结论</h2></div>
{hero}

<div class="sec"><span class="n">02</span><h2>准入资格审查</h2></div>
{elig_html}

<div class="sec"><span class="n">03</span><h2>深度匹配度分析</h2></div>
{dims}

<div class="sec"><span class="n">04</span><h2>候选人独特亮点</h2></div>
{hi_html}

<div class="sec"><span class="n">05</span><h2>潜在风险与「红灯」</h2></div>
{risks}

<div class="sec"><span class="n">06</span><h2>下一步行动建议 · 面试官核心探查问题</h2></div>
{qs or '<p class="w">—</p>'}

<div class="foot"><span>候选人内部评估报告 · 保密</span><span>来源：{src or "—"} · {meta_date or ""}</span></div>
"""
    return (
        f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">'
        f'<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>候选人评估 · {cand} · {pos}</title><style>{CSS}</style></head>'
        f'<body><button class="print-btn" onclick="window.print()">⬇ 导出 PDF</button>'
        f'<div class="page">{body}</div></body></html>'
    )


CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
]


def _find_chrome() -> str | None:
    for c in CHROME_CANDIDATES:
        if os.path.exists(c):
            return c
    for name in ("google-chrome", "chromium", "chromium-browser", "chrome",
                 "microsoft-edge"):
        p = shutil.which(name)
        if p:
            return p
    return None


def html_to_pdf(html_path: str, pdf_path: str) -> str:
    """Print the HTML to PDF via headless Chrome (backgrounds preserved)."""
    chrome = _find_chrome()
    if not chrome:
        raise SystemExit(
            "No Chrome/Chromium/Edge found for --pdf. Open the HTML and use the "
            "「导出 PDF」button (Print → Save as PDF) instead."
        )
    url = "file://" + os.path.abspath(html_path)
    base = ["--headless=new", "--disable-gpu", f"--print-to-pdf={pdf_path}", url]
    # --no-pdf-header-footer strips the browser's date/URL chrome (Chrome 111+).
    try:
        subprocess.run([chrome, "--no-pdf-header-footer", *base], check=True,
                       timeout=90, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        subprocess.run([chrome, *base], check=True, timeout=90,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if not os.path.exists(pdf_path):
        raise SystemExit("Headless Chrome did not produce a PDF.")
    return pdf_path


def main() -> int:
    ap = argparse.ArgumentParser(description="Render assessment.json to HTML.")
    ap.add_argument("assessment", help="assessment.json path")
    ap.add_argument("--out", default="report.html", help="output HTML path")
    ap.add_argument("--pdf", action="store_true",
                    help="also export a PDF (via headless Chrome) next to --out")
    args = ap.parse_args()

    with open(args.assessment, encoding="utf-8") as f:
        data = json.load(f)
    html_out = render(data)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(html_out)
    print(f"wrote {args.out}")

    if args.pdf:
        pdf_path = os.path.splitext(args.out)[0] + ".pdf"
        html_to_pdf(args.out, pdf_path)
        print(f"wrote {pdf_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
