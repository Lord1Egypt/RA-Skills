#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_variants.py — 候选纪律的机制:≥2 个整页候选合成一张对比页。

用法:
  python make_variants.py a.html b.html [c.html ...] --labels "暗夜" "素雅" --out compare.html
  python make_variants.py a.html b.html --cards cards.json --out compare.html
    cards.json = [{"label":"素雅","hexes":["555B6E",...],"tags":["light","pastel"]}, ...]
    (与候选页一一对应;给了元数据,每格带色板条与最优对比度,按钮回传完整指令)
  (对比页与候选文件放同目录即可;iframe 同源直接渲染)

纪律:交付用户裁决前必须 ≥2 个候选;只有 1 个方案 = 退出码 1。
用户点名后,把该格「选它」回传句原样作为下一步指令——不转述,不替用户决定。
"""
import argparse
import json
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def _contrast(a, b):
    def lin(c):
        c /= 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    def lum(h):
        r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
        return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)
    l1, l2 = sorted((lum(a), lum(b)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pages", nargs="+", help="候选页面(≥2)")
    ap.add_argument("--labels", nargs="+", default=None, help="每个候选的名字")
    ap.add_argument("--cards", default=None, help="元数据 JSON(与 pages 一一对应)")
    ap.add_argument("--out", default="compare.html")
    args = ap.parse_args()

    if len(args.pages) < 2:
        print("候选纪律:只有 1 个方案不得送审——至少给 2 个候选(replace/mutate/harmony 换种子再来)")
        sys.exit(1)
    labels = args.labels or [f"候选 {chr(0x41+i)}" for i in range(len(args.pages))]
    assert len(labels) == len(args.pages), "labels 数量与 pages 不一致"

    cards = None
    if args.cards:
        cards = json.load(open(args.cards, encoding="utf-8"))
        assert isinstance(cards, list) and len(cards) == len(args.pages), "cards 数量与 pages 不一致"

    cells = []
    for i, (p, lab) in enumerate(zip(args.pages, labels)):
        c = cards[i] if cards else None
        letters = chr(0x41 + i)
        if c:
            hexes = [h.lstrip("#").upper() for h in c.get("hexes", [])]
            tags = c.get("tags", [])
            best = max((_contrast(a, b) for j, a in enumerate(hexes) for b in hexes[j + 1:]),
                       default=0) if len(hexes) >= 2 else 0
            chips = "".join(f"<span class='hx' style='background:#{h}'></span>" for h in hexes)
            info = (f"{' · '.join(tags)} · 最优对比 {best:.2f}:1" if tags
                    else f"最优对比 {best:.2f}:1")
            say = (f"就用候选 {letters}「{c.get('label', lab)}」:色板 "
                   f"{','.join('#' + h for h in hexes)}。按 60-30-10 出页面,再过 report 四道检查。")
        else:
            chips, info = "", ""
            say = f"就用候选 {letters}「{lab}」的方向继续。"
        say_js = say.replace("\\", "\\\\").replace("'", "\\'").replace('"', "&quot;")
        sub = f"<span>{os.path.basename(p)}</span>"
        meta = (f"<div class='meta'>{chips}<span class='hexlist'>{' '.join('#' + h for h in hexes)}"
                f" · {info}</span></div>") if c else ""
        cells.append(f"""
    <div class="cell">
      <div class="cap"><b>候选 {letters} · {lab}</b>{sub}</div>
      {meta}
      <iframe src="{p}" loading="lazy"></iframe>
      <div class="pick"><button onclick="pick(this)" data-say="{say_js}">选它 — 复制回传句</button></div>
    </div>""")
    html = f"""<!doctype html><html lang="zh"><head><meta charset="utf-8">
<title>候选对比 — pick one</title><style>
  body{{margin:0;background:#20242B;font-family:system-ui;color:#E8EEF6}}
  header{{padding:18px 26px;font-size:15px;letter-spacing:.08em;
         border-bottom:1px solid rgba(255,255,255,.12)}}
  header b{{color:#F2CC8F}}
  .grid{{display:grid;grid-template-columns:repeat({min(len(cells), 2)},1fr);gap:14px;padding:14px}}
  .cell{{border:1px solid rgba(255,255,255,.14);border-radius:8px;overflow:hidden}}
  .cap{{display:flex;justify-content:space-between;padding:9px 14px;font-size:13px;
       background:rgba(255,255,255,.06)}}
  .cap span{{opacity:.55;font-family:monospace;font-size:12px}}
  .meta{{display:flex;align-items:center;gap:4px;padding:7px 14px;
        border-bottom:1px solid rgba(255,255,255,.08)}}
  .hx{{width:22px;height:22px;border-radius:5px;display:inline-block;
      border:1px solid rgba(255,255,255,.25)}}
  .hexlist{{margin-left:auto;font:11px monospace;opacity:.6}}
  iframe{{width:100%;height:74vh;border:0;display:block;background:#fff}}
  .pick{{padding:8px 14px;background:rgba(255,255,255,.06)}}
  button{{background:#F2CC8F;color:#20242B;border:0;border-radius:6px;padding:6px 14px;
         font:600 12px system-ui;cursor:pointer}}
  #say{{position:fixed;left:50%;bottom:18px;transform:translateX(-50%);max-width:80vw;
       background:#F2CC8F;color:#20242B;padding:10px 16px;border-radius:8px;
       font:13px system-ui;display:none;white-space:pre-wrap}}
</style></head><body>
<header>候选对比 —— 看完点名;点「选它」把回传句发给智能体,<b>不要替用户决定</b></header>
<div class="grid">{''.join(cells)}
</div><div id="say"></div>
<script>
function pick(btn){{
  var s = btn.getAttribute('data-say');
  var box = document.getElementById('say');
  box.textContent = s; box.style.display = 'block';
  if (navigator.clipboard) {{ navigator.clipboard.writeText(s).catch(function(){{}}); }}
  clearTimeout(box._t); box._t = setTimeout(function(){{ box.style.display = 'none'; }}, 6000);
}}
</script></body></html>"""
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"对比页: {args.out}({len(args.pages)} 候选)")
    print("送审语:把对比页发给用户,等点名;点名后把该格回传句原样作为下一步指令。")


if __name__ == "__main__":
    main()
