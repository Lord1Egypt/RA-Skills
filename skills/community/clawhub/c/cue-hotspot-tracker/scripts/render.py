#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把追踪报告的 Markdown 渲染成「报告长图」(PNG)：保留报告自身章节结构，只做排版。

用法:
    python3 render.py <报告.md> [-o 输出.png] [--width 1242]

流程:
    Markdown -> HTML(内联 CSS) -> Chrome headless 截图 -> 缩放到目标宽度
    无 Chrome/Chromium/Edge 时退化为同名 .html（可自行打开截图）。
    跨平台：macOS 走 sips 缩放，Windows / Linux 用 device-scale-factor 直接截图。
"""

import argparse
import html as _html
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
  --bg:#EDEFF3; --card:#FFFFFF; --navy:#1F2D4D; --red:#D63031;
  --green:#1E8449; --ink:#1A1A1A; --body:#3A3A3A; --muted:#8A9099; --line:#E3E6EB;
}
*{box-sizing:border-box;}
body{margin:0;background:var(--bg);
  font-family:"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;
  color:var(--body);-webkit-font-smoothing:antialiased;}
.page{width:1080px;margin:0 auto;padding:44px 40px 56px;}

.hero{position:relative;padding-bottom:18px;margin-bottom:22px;border-bottom:3px solid var(--navy);}
.hero h1{margin:0;font-size:40px;line-height:1.25;font-weight:900;color:var(--ink);letter-spacing:.5px;}
.hero .meta{margin-top:10px;font-size:15px;color:var(--muted);}
.hero .chip{position:absolute;top:0;right:0;background:var(--navy);color:#fff;
  font-size:12.5px;font-weight:600;padding:7px 13px;border-radius:20px;letter-spacing:.3px;}

.card{background:var(--card);border:1px solid var(--line);border-radius:14px;
  margin-bottom:20px;overflow:hidden;box-shadow:0 1px 3px rgba(20,30,50,.05);}
.card-h{display:flex;align-items:center;gap:12px;background:var(--navy);color:#fff;
  padding:15px 20px;font-size:21px;font-weight:800;letter-spacing:.4px;}
.card-h .num{flex:0 0 auto;min-width:30px;height:30px;padding:0 8px;border-radius:8px;
  background:var(--red);color:#fff;font-size:16px;font-weight:800;
  display:flex;align-items:center;justify-content:center;}
.card-b{padding:20px 22px 24px;font-size:16px;line-height:1.75;}

.card-b h3{margin:22px 0 10px;font-size:17px;font-weight:800;color:var(--navy);
  padding-left:12px;border-left:4px solid var(--red);}
.card-b h3:first-child{margin-top:2px;}
.card-b p{margin:0 0 12px;}
.card-b strong{color:var(--ink);font-weight:800;}
.card-b em{color:#9AA1AA;font-style:normal;font-size:13px;}

.card-b ul{margin:4px 0 14px;padding-left:0;list-style:none;}
.card-b ul li{position:relative;padding-left:20px;margin-bottom:9px;}
.card-b ul li::before{content:"";position:absolute;left:4px;top:.62em;width:6px;height:6px;
  border-radius:50%;background:var(--red);}
.card-b ul li.lvl2{padding-left:42px;color:#555;}
.card-b ul li.lvl2::before{left:26px;background:var(--navy);opacity:.55;}

.card-b table{width:100%;border-collapse:collapse;margin:6px 0 16px;font-size:14px;}
.card-b th{background:#F5F7FA;color:var(--navy);font-weight:800;text-align:left;
  padding:10px 12px;border-bottom:2px solid var(--line);white-space:nowrap;}
.card-b td{padding:10px 12px;border-bottom:1px solid #EEF1F5;vertical-align:top;line-height:1.6;}
.card-b tr:nth-child(even) td{background:#FAFBFC;}
.card-b td:first-child{font-weight:700;color:var(--ink);}

.up{color:var(--red);font-weight:700;}
.down{color:var(--green);font-weight:700;}

.foot{margin-top:26px;border-top:2px solid var(--line);padding-top:16px;
  font-size:12.5px;line-height:1.7;color:var(--muted);}
.foot .foot-title{color:var(--navy);font-weight:700;font-size:13px;margin-bottom:6px;}
.foot .disc{color:#9AA1AA;}
"""

INLINE_LINK = re.compile(r"\[[^\]]*\]\(\s*<[^>]*>\s*\)|\[[^\]]*\]\([^)]*\)")
BOLD = re.compile(r"\*\*(.+?)\*\*")
ITALIC = re.compile(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)")
CODE = re.compile(r"`(.+?)`")
UP = re.compile(r"\+\d+(?:\.\d+)?%")
DOWN = re.compile(r"(?<![\w.])-\d+(?:\.\d+)?%")
BULLET = re.compile(r"^\s*[-*]\s+")
SEC_NUM = re.compile(r"^(\d+)[.、]\s*(.*)$")
SEP = re.compile(r"[\s:|-]+")
GEN_TIME = re.compile(r"(\d{4}-\d{2}-\d{2})\s+(\d{1,2}:\d{2})")


def inline(text: str) -> str:
    text = INLINE_LINK.sub("", text)
    text = _html.escape(text, quote=False)
    text = BOLD.sub(r"<strong>\1</strong>", text)
    text = ITALIC.sub(r"<em>\1</em>", text)
    text = CODE.sub(r"<code>\1</code>", text)
    text = UP.sub(lambda m: f'<span class="up">{m.group(0)}</span>', text)
    text = DOWN.sub(lambda m: f'<span class="down">{m.group(0)}</span>', text)
    return text.strip()


def render_table(rows):
    def cells(r):
        r = r.strip()
        if r.startswith("|"):
            r = r[1:]
        if r.endswith("|"):
            r = r[:-1]
        return [c.strip() for c in r.split("|")]

    if not rows:
        return ""
    header = cells(rows[0])
    body = rows[2:] if len(rows) > 1 and SEP.fullmatch(rows[1]) else rows[1:]
    out = ["<table><thead><tr>"]
    out += [f"<th>{inline(c)}</th>" for c in header]
    out.append("</tr></thead><tbody>")
    for r in body:
        out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cells(r)) + "</tr>")
    out.append("</tbody></table>")
    return "".join(out)


def parse(report: str):
    lines = report.split("\n")
    title = ""
    date_line = ""
    sections = []
    footer = []
    cur = None
    buf = []
    i, n = 0, len(lines)

    def flush():
        nonlocal buf
        if cur is not None and buf:
            cur["html"] += "\n".join(buf)
        buf = []

    while i < n:
        raw = lines[i]
        stripped = raw.strip()

        if not stripped:
            i += 1
            continue

        if stripped.startswith("<!--"):
            # 报告头注释里的「| YYYY-MM-DD HH:MM」= Cue 报告生成时间，优先取它
            m = GEN_TIME.search(stripped)
            if m and not date_line:
                date_line = f"{m.group(1)} 盘中（报告生成 {m.group(2)}）"
            i += 1
            continue

        if stripped.startswith("### "):
            flush()
            if cur is not None:
                cur["html"] += f"<h3>{inline(stripped[4:])}</h3>"
            i += 1
            continue

        if stripped.startswith("## "):
            flush()
            if cur is not None:
                sections.append(cur)
            t = stripped[3:].strip()
            m = SEC_NUM.match(t)
            num, name = (m.group(1), m.group(2)) if m else ("", t)
            cur = {"num": num, "title": name, "html": ""}
            i += 1
            continue

        if stripped.startswith("# "):
            title = stripped[2:].strip()
            i += 1
            continue

        if stripped.startswith("数据截至"):
            # 兜底：报告头没有生成时间注释时，才退回「数据截至」那行
            if not date_line:
                date_line = stripped
            i += 1
            continue

        if re.fullmatch(r"-{3,}", stripped):
            i += 1
            continue

        if stripped.startswith("|"):
            tbl = []
            while i < n and lines[i].strip().startswith("|"):
                tbl.append(lines[i].strip())
                i += 1
            flush()
            html_tbl = render_table(tbl)
            if cur is not None:
                cur["html"] += html_tbl
            else:
                footer.append(html_tbl)
            continue

        if stripped.startswith(">"):
            flush()
            qt = []
            while i < n and lines[i].strip().startswith(">"):
                qt.append(lines[i].strip().lstrip(">").strip())
                i += 1
            footer.append('<p class="disc">' + inline(" ".join(qt)) + "</p>")
            continue

        if BULLET.match(raw):
            flush()
            lis = []
            while i < n and BULLET.match(lines[i].rstrip("\n")):
                r = lines[i].rstrip("\n")
                indent = len(r) - len(r.lstrip(" "))
                content = BULLET.sub("", r, count=1)
                cls = ' class="lvl2"' if indent >= 2 else ""
                lis.append(f"<li{cls}>{inline(content)}</li>")
                i += 1
            buf.append("<ul>" + "".join(lis) + "</ul>")
            continue

        flush()
        buf.append(f"<p>{inline(stripped)}</p>")
        i += 1

    flush()
    if cur is not None:
        sections.append(cur)
    return title, date_line, sections, footer


def build_html(title, date_line, sections, footer):
    p = ['<!doctype html><html><head><meta charset="utf-8">',
         f"<style>{CSS}</style></head><body><div class=\"page\">"]
    p.append('<div class="hero">')
    p.append(f"<h1>{inline(title)}</h1>")
    if date_line:
        p.append(f'<div class="meta">{inline(date_line)}</div>')
    p.append('<div class="chip">AI 自动生成 · 不构成投资建议</div>')
    p.append("</div>")
    for s in sections:
        num = f'<span class="num">{_html.escape(s["num"])}</span>' if s["num"] else ""
        p.append('<section class="card">')
        p.append(f'<div class="card-h">{num}<span>{inline(s["title"])}</span></div>')
        p.append(f'<div class="card-b">{s["html"]}</div>')
        p.append("</section>")
    p.append('<div class="foot">')
    p.append('<div class="foot-title">由 Cue 全天候盯盘助手生成</div>')
    p.append("".join(footer))
    p.append("</div>")
    p.append("</div>")
    p.append(MEASURE_JS)
    p.append("</body></html>")
    return "".join(p)


MEASURE_JS = (
    "<script>window.addEventListener('load',function(){"
    "document.title='H='+Math.ceil(document.documentElement.scrollHeight)});"
    "</script>"
)


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


def _png_size(path):
    """读 PNG 头拿宽高（跨平台，不依赖 sips / 图像库）。"""
    try:
        with open(path, "rb") as f:
            head = f.read(24)
        if head[:8] == b"\x89PNG\r\n\x1a\n":
            return int.from_bytes(head[16:20], "big"), int.from_bytes(head[20:24], "big")
    except OSError:
        pass
    return None


def render_png(chrome, html_path, png_path, width):
    # headless 只截视口，先量出内容真实高度
    dom = _chrome(chrome, ["--virtual-time-budget=3000", "--dump-dom", html_path.as_uri()])
    m = re.search(r"H=(\d+)", dom.stdout)
    h = int(m.group(1)) if m else 1500
    if shutil.which("sips"):
        # macOS：2x 超采样后缩放到目标宽度，画质最佳
        raw = png_path.with_name(png_path.stem + ".2x.png")
        _chrome(chrome, ["--hide-scrollbars", "--force-device-scale-factor=2",
                         f"--window-size={PAGE_WIDTH},{h + 4}",
                         f"--screenshot={raw}", html_path.as_uri()])
        subprocess.run(["sips", "--resampleWidth", str(width), str(raw),
                        "--out", str(png_path)], check=True, capture_output=True)
        raw.unlink(missing_ok=True)
    else:
        # Windows / Linux：用 device-scale-factor 直接截到目标宽度
        scale = width / PAGE_WIDTH
        _chrome(chrome, ["--hide-scrollbars", f"--force-device-scale-factor={scale:g}",
                         f"--window-size={PAGE_WIDTH},{h + 4}",
                         f"--screenshot={png_path}", html_path.as_uri()])
    size = _png_size(png_path)
    return f"{size[0]} {size[1]}" if size else "?"


def _open_html(path):
    """无浏览器可截图时，尽力用默认浏览器打开 HTML，让用户直接看到成品。"""
    try:
        webbrowser.open(path.as_uri())
    except Exception:
        pass


def main():
    ap = argparse.ArgumentParser(description="报告 -> 报告长图")
    ap.add_argument("report", help="Markdown 报告路径")
    ap.add_argument("-o", "--out", help="输出路径（.png；无 Chrome 时输出同名 .html）")
    ap.add_argument("--width", type=int, default=1242, help="PNG 目标宽度（默认 1242）")
    a = ap.parse_args()

    rp = Path(a.report).expanduser()
    text = rp.read_text(encoding="utf-8")
    title, date_line, sections, footer = parse(text)
    doc = build_html(title, date_line, sections, footer)

    out = (Path(a.out).expanduser() if a.out else rp.with_suffix(".report.png")).resolve()
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
    dims = render_png(chrome, html_out, out, a.width)
    print(f"OK -> {out}  ({dims})   (HTML 源文件：{html_out})")


if __name__ == "__main__":
    main()
