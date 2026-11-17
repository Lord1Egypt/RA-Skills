#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把「盘中 SOP」数据(JSON) 渲染成固定版式的看板长图(PNG)。

用法:
    python3 render_dashboard.py data.json [-o 输出.png] [--width 1242]

版式对齐 盘中.svg：0.数据校验 / 1.热点扫描 / 2.催化拆解 / 3.资金识别 / 4.盘中结论。
合规弱化版：不含市场评级、关注强度上限、看多/防守条件等带买卖倾向字段。
无 Chrome/Chromium/Edge 时退化为同名 .html（可自行打开截图）。
跨平台：macOS 走 sips 缩放，Windows / Linux 用 device-scale-factor 直接截图。
"""

import argparse
import html as _html
import json
import os
import re
import shutil
import subprocess
import webbrowser
from pathlib import Path

# 版面固定 1080px 宽；截图时用 device-scale-factor 把输出宽度定到目标宽度
PAGE_WIDTH = 1080


def _chrome_candidates():
    """各平台常见的 Chrome / Chromium / Edge 安装路径。"""
    cands = [
        # macOS
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        # Linux
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        "/usr/bin/microsoft-edge",
    ]
    # Windows：从环境变量拼出 Program Files / 用户目录下的安装路径
    for base in (os.environ.get("PROGRAMFILES"),
                 os.environ.get("PROGRAMFILES(X86)"),
                 os.environ.get("LOCALAPPDATA")):
        if base:
            cands.append(os.path.join(base, "Google", "Chrome", "Application", "chrome.exe"))
            cands.append(os.path.join(base, "Microsoft", "Edge", "Application", "msedge.exe"))
    return cands


CHROME_CANDIDATES = _chrome_candidates()

CSS = """
:root{
  --bg:#F4F5F7; --card:#FFFFFF; --navy:#1F2D4D; --red:#D63031;
  --green:#1E8449; --amber:#E67E22; --ink:#1A1A1A; --body:#444; --muted:#999;
  --line:#E3E6EB; --soft:#F0F2F5;
}
*{box-sizing:border-box;}
body{margin:0;background:var(--bg);
  font-family:"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;color:var(--body);}
.page{width:1080px;margin:0 auto;padding:32px 40px 40px;}

/* header */
.hd{position:relative;padding-bottom:12px;margin-bottom:16px;}
.hd h1{margin:0;font-size:44px;font-weight:900;color:var(--ink);letter-spacing:.5px;}
.hd .bar{width:560px;height:4px;background:var(--red);margin-top:8px;}
.hd .chip{position:absolute;top:0;right:0;width:230px;background:#fff;border:1px solid var(--line);
  border-radius:8px;padding:12px 14px;text-align:center;}
.hd .chip .d{font-size:18px;font-weight:700;color:var(--ink);}
.hd .chip .s{font-size:11px;color:var(--muted);margin-top:4px;line-height:1.5;}

/* decision chain */
.chain{background:var(--navy);color:#fff;border-radius:20px;height:40px;display:flex;
  align-items:center;justify-content:center;font-size:17px;font-weight:600;letter-spacing:1px;
  margin-bottom:16px;}

/* grid rows */
.row{display:grid;gap:15px;margin-bottom:15px;}
.row.split{grid-template-columns:330fr 655fr;}

/* card */
.card{background:#fff;border:1px solid var(--line);border-radius:10px;overflow:hidden;}
.card>.ch{background:var(--navy);color:#fff;padding:11px 18px;
  display:flex;align-items:center;gap:10px;justify-content:space-between;}
.card>.ch .t{font-size:19px;font-weight:700;}
.card>.ch .pill{font-size:12px;font-weight:600;background:rgba(255,255,255,.18);
  padding:4px 10px;border-radius:12px;}
.card>.cb{padding:16px 18px;}

/* kv rows (数据校验) */
.kv{display:grid;grid-template-columns:96px 1fr;gap:8px 10px;font-size:14px;line-height:1.5;}
.kv .k{font-weight:700;color:#444;}
.kv .v{color:#666;}
.tag{display:inline-block;font-size:12.5px;font-weight:700;padding:2px 9px;border-radius:5px;}
.tag.ok{background:#E8F5E9;color:var(--green);border:1px solid var(--green);}
.tag.warn{background:#FFF3E0;color:#E65100;border:1px solid #E65100;}

/* conclusion box */
.cbox{margin-top:14px;border-radius:8px;padding:10px 14px;background:#E8F5E9;border:1px solid var(--green);}
.cbox .l{font-size:13px;font-weight:700;color:var(--green);}
.cbox .m{font-size:15px;font-weight:700;color:var(--green);margin-top:2px;}

/* tables */
table{width:100%;border-collapse:collapse;font-size:13.5px;}
thead th{background:var(--soft);color:#555;font-weight:700;text-align:left;padding:8px 10px;}
tbody td{padding:9px 10px;border-top:1px solid #EDEFF2;vertical-align:top;line-height:1.45;}
tbody tr:nth-child(even){background:#FAFBFC;}
td:first-child{font-weight:700;color:#333;}
.up{color:var(--red);font-weight:700;}
.down{color:var(--green);font-weight:700;}
.amber{color:var(--amber);font-weight:700;}

/* strength / notes */
.note{margin-top:12px;background:var(--soft);border-radius:8px;padding:10px 14px;font-size:14px;}
.note .big{font-size:17px;font-weight:700;color:var(--red);}

/* catalysts */
.cat{margin-bottom:12px;}
.cat .ct{font-size:14px;font-weight:700;}
.cat .cd{font-size:13px;color:#555;line-height:1.55;margin-top:2px;}
.cat.tonel{color:var(--red);} .cat.tonel2{color:var(--amber);} .cat.tonel3{color:#5D6D7E;}

.risk{margin-top:12px;border-radius:8px;padding:10px 14px;background:#FDECEA;border:1px solid #E8A9A9;
  font-size:12.5px;font-weight:600;color:#C0392B;line-height:1.55;}

/* verdict */
.bar-full{background:var(--navy);color:#fff;border-radius:10px;height:40px;display:flex;
  align-items:center;padding:0 18px;font-size:19px;font-weight:700;margin-bottom:15px;}
.oneliner{background:#FDECEA;border:1px solid #E8A9A9;border-radius:8px;padding:14px 18px;
  font-size:15px;font-weight:700;color:#C0392B;line-height:1.6;margin-bottom:15px;text-align:center;}
.vcol{background:#fff;border:1px solid var(--line);border-radius:10px;overflow:hidden;}
.vcol .vh{padding:9px 14px;font-size:14px;font-weight:700;}
.vcol .vb{padding:12px 16px;font-size:13px;color:#444;line-height:1.7;}
.vcol.green .vh{background:#E8F5E9;color:var(--green);}
.vcol.red .vh{background:#FDECEA;color:#C0392B;}
.two{display:grid;grid-template-columns:1fr 1fr;gap:15px;}
.dot{padding-left:16px;position:relative;}
.dot::before{content:"";position:absolute;left:2px;top:.6em;width:6px;height:6px;border-radius:50%;background:var(--red);}

/* footer */
.foot{margin-top:18px;display:flex;justify-content:space-between;font-size:13px;color:var(--muted);}
"""

MEASURE_JS = (
    "<script>window.addEventListener('load',function(){"
    "document.title='H='+Math.ceil(document.documentElement.scrollHeight)});"
    "</script>"
)


def esc(t):
    return _html.escape(str(t), quote=False)


def cell(t):
    s = esc(t)
    if re.match(r"^\+", s) and re.search(r"\d", s):
        return f'<span class="up">{s}</span>'
    if re.match(r"^-", s) and re.search(r"\d", s):
        return f'<span class="down">{s}</span>'
    if "亿" in s:
        return f'<span class="amber">{s}</span>'
    return s


def table(head, rows):
    th = "".join(f"<th>{esc(h)}</th>" for h in head)
    trs = "".join("<tr>" + "".join(f"<td>{cell(c)}</td>" for c in r) + "</tr>" for r in rows)
    return f"<table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>"


def build_html(d):
    p = ['<!doctype html><html><head><meta charset="utf-8">', f"<style>{CSS}</style></head>",
         '<body><div class="page">']

    # header
    p.append('<div class="hd">')
    p.append(f"<h1>{esc(d['title'])}</h1><div class='bar'></div>")
    p.append('<div class="chip">')
    p.append(f"<div class='d'>{esc(d['date'])}</div>")
    p.append(f"<div class='s'>{esc(d['chip_line1'])}<br>{esc(d['chip_line2'])}</div>")
    p.append("</div></div>")

    # chain
    p.append('<div class="chain">' + esc(" → ".join(d["chain"])) + "</div>")

    # row1: 0 check | 1 hotspots
    p.append('<div class="row split">')
    c = d["check"]
    p.append('<div class="card"><div class="ch"><span class="t">数据校验</span></div><div class="cb">')
    p.append('<div class="kv">')
    for k, v in c["rows"]:
        cls = ""
        val = esc(v)
        if v in ("高", "中", "低"):
            val = f'<span class="tag {"ok" if v == "高" else "warn"}">{esc(v)}</span>'
        p.append(f'<div class="k">{esc(k)}：</div><div class="v">{val}</div>')
    p.append("</div>")
    p.append(f'<div class="cbox"><div class="l">{esc(c["conclusion_label"])}</div>'
             f'<div class="m">{esc(c["conclusion"])}</div></div>')
    p.append("</div></div>")

    h = d["hotspots"]
    p.append('<div class="card"><div class="ch"><span class="t">1. 热点扫描｜谁在领涨</span>'
             f'<span class="pill">{esc(h["pill"])}</span></div><div class="cb">')
    p.append(table(h["head"], h["rows"]))
    p.append(f'<div class="note">{esc(h["strength_label"])}：'
             f'<span class="big">{esc(h["strength_value"])}</span>（{esc(h["strength_note"])}）</div>')
    p.append("</div></div>")
    p.append("</div>")

    # row2: 2 catalysts | 3 funds
    p.append('<div class="row split">')
    cat = d["catalysts"]
    p.append('<div class="card"><div class="ch"><span class="t">2. 催化拆解｜驱动原因</span></div><div class="cb">')
    for it in cat["items"]:
        p.append(f'<div class="cat {it.get("tone","")}"><div class="ct">{esc(it["title"])}</div>'
                 f'<div class="cd">{esc(it["desc"])}</div></div>')
    p.append(f'<div class="cat"><div class="ct" style="color:#95A5A6">{esc(cat["noise_title"])}</div>'
             f'<div class="cd" style="color:#999">{esc(cat["noise_desc"])}</div></div>')
    p.append(f'<div class="note">{esc(cat["strength_label"])}：'
             f'<span class="big">{esc(cat["strength_value"])}</span>（{esc(cat["strength_note"])}）</div>')
    p.append("</div></div>")

    f = d["funds"]
    p.append('<div class="card"><div class="ch"><span class="t">3. 资金识别｜聪明钱去向</span></div><div class="cb">')
    p.append(table(f["head"], f["rows"]))
    p.append(f'<div class="note">{esc(f["conclusion_label"])}：{esc(f["conclusion"])}</div>')
    p.append(f'<div class="risk">{esc(f["risk"])}</div>')
    p.append("</div></div>")
    p.append("</div>")

    # row3: verdict
    v = d["verdict"]
    p.append('<div class="bar-full">4. 盘中结论</div>')
    p.append(f'<div class="oneliner">{esc(v["one_liner"])}</div>')
    p.append('<div class="two">')
    p.append('<div class="vcol green"><div class="vh">今日盘面主线</div><div class="vb">'
             + "".join(f'<div class="dot">{esc(x)}</div>' for x in v["focus"]) + "</div></div>")
    p.append('<div class="vcol red"><div class="vh">风险提示</div><div class="vb">'
             + "".join(f'<div class="dot">{esc(x)}</div>' for x in v["risk"]) + "</div></div>")
    p.append("</div>")

    # footer
    p.append(f'<div class="foot"><span>{esc(d["footer_left"])}</span>'
             f'<span>{esc(d["footer_right"])}</span></div>')

    p.append("</div>")
    p.append(MEASURE_JS)
    p.append("</body></html>")
    return "".join(str(x) for x in p if x is not None)


def find_chrome():
    for c in CHROME_CANDIDATES:
        if Path(c).exists():
            return c
    for name in ("google-chrome", "google-chrome-stable", "chromium",
                 "chromium-browser", "chrome", "microsoft-edge",
                 "msedge", "chrome.exe", "msedge.exe"):
        p = shutil.which(name)
        if p:
            return p
    return None


def _chrome(exe, args):
    return subprocess.run([exe, "--headless=new", "--disable-gpu", *args],
                          check=True, capture_output=True, text=True)


def render_png(chrome, html_path, png_path, width):
    # headless 只截视口，先量出内容真实高度
    dom = _chrome(chrome, ["--virtual-time-budget=3000", "--dump-dom", html_path.as_uri()])
    mt = re.search(r"H=(\d+)", dom.stdout)
    height = int(mt.group(1)) if mt else 1500
    if shutil.which("sips"):
        # macOS：2x 超采样后缩放到目标宽度，画质最佳
        raw = png_path.with_name(png_path.stem + ".2x.png")
        _chrome(chrome, ["--hide-scrollbars", "--force-device-scale-factor=2",
                         f"--window-size={PAGE_WIDTH},{height + 4}",
                         f"--screenshot={raw}", html_path.as_uri()])
        subprocess.run(["sips", "--resampleWidth", str(width), str(raw),
                        "--out", str(png_path)], check=True, capture_output=True)
        raw.unlink(missing_ok=True)
    else:
        # Windows / Linux：用 device-scale-factor 直接截到目标宽度
        scale = width / PAGE_WIDTH
        _chrome(chrome, ["--hide-scrollbars", f"--force-device-scale-factor={scale:g}",
                         f"--window-size={PAGE_WIDTH},{height + 4}",
                         f"--screenshot={png_path}", html_path.as_uri()])


def _open_html(path):
    """无浏览器可截图时，尽力用默认浏览器打开 HTML，让用户直接看到成品。"""
    try:
        webbrowser.open(path.as_uri())
    except Exception:
        pass


def main():
    ap = argparse.ArgumentParser(description="SOP JSON -> 看板长图")
    ap.add_argument("data", help="SOP 数据 JSON 路径")
    ap.add_argument("-o", "--out", help="输出路径（.png；无 Chrome 时输出同名 .html）")
    ap.add_argument("--width", type=int, default=1242, help="PNG 目标宽度（默认 1242）")
    a = ap.parse_args()

    dp = Path(a.data).expanduser()
    d = json.loads(dp.read_text(encoding="utf-8"))
    # 本 skill 只做盘中：兜底纠正标题/页脚里误写的「盘后」口径
    for k in ("title", "footer_left"):
        if isinstance(d.get(k), str):
            d[k] = d[k].replace("盘后", "盘中")
    doc = build_html(d)

    out = (Path(a.out).expanduser() if a.out else dp.with_suffix(".png")).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    # 中间产物 HTML 收进 <图名>.src/ 子目录，交付目录只留 PNG
    html_dir = out.parent / (out.stem + ".src")
    html_dir.mkdir(parents=True, exist_ok=True)
    html_out = html_dir / (out.stem + ".html")
    html_out.write_text(doc, encoding="utf-8")

    chrome = find_chrome()
    if not chrome:
        _open_html(html_out)
        print(f"未找到 Chrome/Chromium/Edge，已用默认浏览器打开 HTML（可直接截图）：{html_out}")
        return
    render_png(chrome, html_out, out, a.width)
    print(f"OK -> {out}   (HTML 源文件：{html_out})")


if __name__ == "__main__":
    main()
