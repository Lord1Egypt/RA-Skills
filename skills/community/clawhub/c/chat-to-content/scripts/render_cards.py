#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
render_cards.py - 把结构化卡片数据渲染成竖版信息流贴图（PNG / JPG）。

数据源（JSON）示例见 references/card-schema.md，最简形式：
{
  "theme": "coral",
  "brand": "你的署名",
  "cards": [
    {"type":"cover","kicker":"AI 实战","title":"我把一次对话\n变成了爆款文章","subtitle":"..."},
    {"type":"points","heading":"三个关键转折","items":[{"t":"...","d":"..."}]},
    {"type":"quote","text":"金句","who":"来源"},
    {"type":"checklist","heading":"可复用经验","items":["...","..."]},
    {"type":"conclusion","heading":"写在最后","body":"...","highlight":"...","tags":["#AI"]}
  ]
}

用法:
    python render_cards.py --data cards.json --out-dir ./cards
    python render_cards.py --data cards.json --out-dir ./cards --size 1080x1920 --theme tech
    python render_cards.py --data cards.json --out-dir ./cards --format jpg --merge

依赖: 系统需存在 Edge 或 Chrome（headless 截图），或安装 playwright。
      JPG 输出 / 长图合并需要 Pillow（可选，缺失时自动跳过并提示）。
"""

import argparse
import html as htmllib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(os.path.dirname(HERE), "assets", "card_template.html")

THEMES = {
    "coral": dict(bg="#FFF9F7", fg="#2B2320", muted="#8A7B74", accent="#FF6B6B",
                  accent_soft="#FFE7E3", panel="#FFFFFF", line="#F2E3DF"),
    "ink": dict(bg="#FFFFFF", fg="#111111", muted="#6B6B6B", accent="#111111",
                accent_soft="#F1F1F1", panel="#FAFAFA", line="#E6E6E6"),
    "tech": dict(bg="#0E1621", fg="#EAF1F8", muted="#93A4B8", accent="#4EA8FF",
                 accent_soft="#17314B", panel="#152232", line="#24374C"),
    "mint": dict(bg="#F6FBF8", fg="#1E2B24", muted="#6C8074", accent="#17A673",
                 accent_soft="#DFF3E9", panel="#FFFFFF", line="#E2EFE8"),
    "sun": dict(bg="#FFFCF3", fg="#2C2617", muted="#8C8467", accent="#F2A93B",
                accent_soft="#FDEBCB", panel="#FFFFFF", line="#F0E4C8"),
}

BROWSER_CANDIDATES = [
    # Windows：系统级安装
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    # Windows：用户级安装（非管理员安装、自定义目录），占位符在运行时展开
    r"%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe",
    r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe",
    r"%PROGRAMFILES%\Microsoft\Edge\Application\msedge.exe",
    r"%PROGRAMFILES%\Google\Chrome\Application\chrome.exe",
    # macOS
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    # Linux
    "/usr/bin/google-chrome",
    "/usr/bin/google-chrome-stable",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
    "/usr/bin/microsoft-edge",
    "/opt/google/chrome/chrome",
    "/opt/microsoft/msedge/msedge",
    "/snap/bin/chromium",
]

BROWSER_COMMANDS = (
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
    "microsoft-edge",
    "msedge",
    "chrome",
)

# 允许用环境变量覆盖浏览器位置，适配非标准安装
BROWSER_ENV_KEYS = ("CHROME_PATH", "CHROMIUM_PATH", "BROWSER")

EXECUTABLE_HINTS = ("chrome", "chromium", "msedge", "edge")


def _expand(path):
    return os.path.expandvars(os.path.expanduser(path))


def _looks_like_browser(path):
    base = os.path.basename(path).lower()
    return any(h in base for h in EXECUTABLE_HINTS)


def find_browser():
    """按 环境变量 → 固定路径 → PATH 命令 的顺序找可用浏览器。

    CHROME_PATH / CHROMIUM_PATH / BROWSER 可覆盖默认探测，适配非标准安装位置。
    """
    for key in BROWSER_ENV_KEYS:
        v = os.environ.get(key)
        if not v:
            continue
        v = _expand(v)
        if os.path.isfile(v) and _looks_like_browser(v):
            return v
    for b in BROWSER_CANDIDATES:
        p = _expand(b)
        if os.path.isfile(p):
            return p
    for name in BROWSER_COMMANDS:
        p = shutil.which(name)
        if p:
            return p
    return None


# ---------- 文本处理 ----------
def rich(text):
    """极简富文本： **加粗** -> <b>，[[高亮]] -> <em>，\n -> <br>"""
    if text is None:
        return ""
    t = htmllib.escape(str(text))
    t = re.sub(r"\[\[(.+?)\]\]", r"<em>\1</em>", t, flags=re.S)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t, flags=re.S)
    t = t.replace("\n", "<br>")
    return t


def plain(text):
    """去掉富文本标记后的纯文本，用于估算字号"""
    t = re.sub(r"\[\[|\]\]|\*\*", "", str(text or ""))
    return t


# 版式按 1080 宽设计；其它画布宽度按比例缩放字号，避免大画布下文字偏小
BASE_WIDTH = 1080.0


def scale_factor(size):
    return size[0] / BASE_WIDTH


def cover_title_size(title, k=1.0):
    n = len(plain(title).replace("\n", ""))
    if n <= 10:
        base = 96
    elif n <= 16:
        base = 82
    elif n <= 24:
        base = 70
    elif n <= 34:
        base = 60
    else:
        base = 52
    return int(round(base * k))


def quote_size(text, k=1.0):
    n = len(plain(text))
    if n <= 24:
        base = 64
    elif n <= 48:
        base = 54
    elif n <= 80:
        base = 46
    elif n <= 120:
        base = 40
    else:
        base = 34
    return int(round(base * k))


def point_text_size(items, k=1.0):
    longest = max([len(plain(i.get("d", ""))) for i in items] or [0])
    if longest <= 40:
        base = 32
    elif longest <= 70:
        base = 29
    else:
        base = 26
    return int(round(base * k))


# ---------- 卡片渲染 ----------
def render_cover(c, brand, page, k=1.0):
    sub = c.get("subtitle", "")
    return (
        '<div class="kicker">%s</div>' % rich(c.get("kicker", "笔记"))
        + '<h1 class="cover-title">%s</h1>' % rich(c.get("title", ""))
        + ('<div class="cover-rule"></div>' if sub else "")
        + ('<div class="cover-sub">%s</div>' % rich(sub) if sub else "")
    )


def render_points(c, brand, page, k=1.0):
    items = c.get("items", [])[:5]
    size = point_text_size(items, k)
    rows = []
    for i, it in enumerate(items, 1):
        rows.append(
            '<div class="point"><div class="n">%02d</div><div>'
            '<div class="tt">%s</div><div class="dd" style="font-size:%dpx">%s</div>'
            "</div></div>" % (i, rich(it.get("t", "")), size, rich(it.get("d", "")))
        )
    return (
        '<h2 class="h2">%s</h2>' % rich(c.get("heading", "关键要点"))
        + ('<div class="h2sub">%s</div>' % rich(c.get("sub", "")) if c.get("sub") else '<div style="height:calc(44px * var(--k))"></div>')
        + "".join(rows)
    )


def render_quote(c, brand, page, k=1.0):
    return (
        '<div class="quote-box"><div class="qm">&ldquo;</div>'
        '<div class="qtext" style="font-size:%dpx">%s</div>' % (quote_size(c.get("text", ""), k), rich(c.get("text", "")))
        + ('<div class="qwho">%s</div>' % rich(c.get("who", "")) if c.get("who") else "")
        + "</div>"
    )


def render_checklist(c, brand, page, k=1.0):
    items = c.get("items", [])[:7]
    rows = [
        '<div class="ck"><div class="tick">&#10003;</div><div class="txt">%s</div></div>' % rich(i)
        for i in items
    ]
    return (
        '<h2 class="h2">%s</h2>' % rich(c.get("heading", "可复用清单"))
        + ('<div class="h2sub">%s</div>' % rich(c.get("sub", "")) if c.get("sub") else '<div style="height:calc(44px * var(--k))"></div>')
        + "".join(rows)
    )


def render_steps(c, brand, page, k=1.0):
    items = c.get("items", [])[:5]
    rows = []
    for i, it in enumerate(items, 1):
        rows.append(
            '<div class="point"><div class="n">%d</div><div>'
            '<div class="tt">%s</div><div class="dd">%s</div>'
            "</div></div>" % (i, rich(it.get("t", "")), rich(it.get("d", "")))
        )
    return '<h2 class="h2">%s</h2>' % rich(c.get("heading", "流程")) + "".join(rows)


def render_conclusion(c, brand, page, k=1.0):
    tags = c.get("tags", [])[:6]
    tag_html = (
        '<div class="tags">' + "".join('<span class="tag">%s</span>' % rich(t) for t in tags) + "</div>"
        if tags
        else ""
    )
    return (
        '<h2 class="h2">%s</h2>' % rich(c.get("heading", "写在最后"))
        + ('<div class="lead">%s</div>' % rich(c.get("body", "")) if c.get("body") else "")
        + ('<div class="hlbox">%s</div>' % rich(c.get("highlight", "")) if c.get("highlight") else "")
        + tag_html
    )


RENDERERS = {
    "cover": render_cover,
    "points": render_points,
    "quote": render_quote,
    "checklist": render_checklist,
    "steps": render_steps,
    "conclusion": render_conclusion,
}


def foot_html(brand, page, total, show_page=True):
    right = ('<span>%02d / %02d</span>' % (page, total)) if show_page else ""
    return '<div class="foot"><span><span class="dot"></span>%s</span>%s</div>' % (
        htmllib.escape(brand or ""),
        right,
    )


def build_html(card, idx, total, theme, brand, size, show_page=True, template=TEMPLATE):
    w, h = size
    k = scale_factor(size)
    pad = int(round(w * 0.082))
    t = THEMES.get(theme, THEMES["coral"])
    with io.open(template, "r", encoding="utf-8") as f:
        tpl = f.read()
    ctype = card.get("type", "points")
    renderer = RENDERERS.get(ctype, render_points)
    body = renderer(card, brand, idx, k)
    # 封面 / 金句 / 结尾：内容垂直居中；其余信息密度高的卡片顶部对齐
    content_class = " center" if ctype in ("cover", "quote", "conclusion") else ""
    # 封面也带署名，但不显示页码
    foot = foot_html(brand, idx, total, show_page and ctype != "cover")
    mapping = {
        "{{BG}}": t["bg"], "{{FG}}": t["fg"], "{{MUTED}}": t["muted"],
        "{{ACCENT}}": t["accent"], "{{ACCENT_SOFT}}": t["accent_soft"],
        "{{PANEL}}": t["panel"], "{{LINE}}": t["line"],
        "{{W}}": str(w), "{{H}}": str(h), "{{PAD}}": str(pad),
        "{{K}}": "%.6f" % k,
        "{{COVER_TITLE}}": str(cover_title_size(card.get("title", ""), k)),
        "{{QUOTE_SIZE}}": str(quote_size(card.get("text", ""), k)),
        "{{CONTENT_CLASS}}": content_class,
        "{{CONTENT}}": body,
        "{{FOOT}}": foot,
    }
    for key, val in mapping.items():
        tpl = tpl.replace(key, val)
    return tpl


# ---------- 截图 ----------
def screenshot_browser(html_path, out_path, size, scale=1, timeout=90):
    w, h = size
    exe = find_browser()
    if not exe:
        return False, "未找到 Edge / Chrome（可用 playwright 回退，或安装其中之一）"
    profile = tempfile.mkdtemp(prefix="cardshot_")
    try:
        cmd = [
            exe, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-sandbox",
            "--disable-extensions", "--disable-dev-shm-usage", "--no-first-run",
            "--user-data-dir=%s" % profile,
            "--force-device-scale-factor=%s" % scale,
            "--window-size=%d,%d" % (w, h),
            "--screenshot=%s" % os.path.abspath(out_path),
            Path(os.path.abspath(html_path)).as_uri(),
        ]
        try:
            r = subprocess.run(cmd, timeout=timeout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception as e:
            return False, "浏览器截图异常: %s" % e
        if not os.path.isfile(out_path):
            err = (r.stderr or b"").decode("utf-8", "replace")[:300]
            return False, "截图失败: %s" % err
        return True, "browser"
    finally:
        shutil.rmtree(profile, ignore_errors=True)


def screenshot_playwright(html_path, out_path, size, scale=1, timeout=90):
    try:
        from playwright.sync_api import sync_playwright
    except Exception as e:
        return False, "playwright 不可用: %s" % e
    try:
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page(viewport={"width": size[0], "height": size[1]}, device_scale_factor=scale)
            pg.goto(Path(os.path.abspath(html_path)).as_uri())
            pg.wait_for_timeout(400)
            pg.screenshot(path=out_path)
            b.close()
        return True, "playwright"
    except Exception as e:
        return False, "playwright 截图失败: %s" % e


def to_jpg(png_path, quality=92):
    try:
        from PIL import Image
    except Exception:
        return None
    out = os.path.splitext(png_path)[0] + ".jpg"
    im = Image.open(png_path).convert("RGB")
    im.save(out, "JPEG", quality=quality)
    return out


def merge_long(pngs, out_path):
    try:
        from PIL import Image
    except Exception:
        return None
    ims = [Image.open(p) for p in pngs]
    w = max(i.width for i in ims)
    total = sum(int(i.height * w / i.width) for i in ims)
    canvas = Image.new("RGB", (w, total), "white")
    y = 0
    for i in ims:
        nw = w
        nh = int(i.height * w / i.width)
        canvas.paste(i.resize((nw, nh)), (0, y))
        y += nh
    canvas.save(out_path)
    return out_path


def parse_size(s):
    m = re.match(r"(\d+)\s*[xX*]\s*(\d+)", s)
    if not m:
        raise ValueError("尺寸格式应为 宽x高，如 1080x1440")
    return int(m.group(1)), int(m.group(2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="卡片 JSON 文件路径，- 表示从 stdin 读取")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--size", default=None)
    ap.add_argument("--theme", default=None, help="coral / ink / tech / mint / sun")
    ap.add_argument("--brand", default=None)
    ap.add_argument("--prefix", default="card")
    ap.add_argument("--format", default="png", choices=["png", "jpg"])
    ap.add_argument("--scale", type=int, default=2, help="输出倍率，2 = 2 倍高清")
    ap.add_argument("--merge", action="store_true", help="额外输出一张纵向拼接长图")
    ap.add_argument("--keep-html", action="store_true", help="保留中间 HTML 便于微调")
    ap.add_argument("--no-page", action="store_true", help="不显示页码")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.data == "-" else io.open(args.data, "r", encoding="utf-8").read()
    data = json.loads(raw)
    theme = args.theme or data.get("theme") or "coral"
    if theme not in THEMES:
        print(json.dumps({
            "ok": False,
            "reason": "未知主题 %r，可选：%s" % (theme, " / ".join(THEMES)),
        }, ensure_ascii=False))
        return 2
    brand = args.brand or data.get("brand") or ""
    size = parse_size(args.size or data.get("size") or "1080x1440")
    cards = data.get("cards") or []
    if not cards:
        print(json.dumps({"ok": False, "reason": "cards 为空"}, ensure_ascii=False))
        return 2

    os.makedirs(args.out_dir, exist_ok=True)
    keep_dir = os.path.join(args.out_dir, "_html") if args.keep_html else tempfile.mkdtemp(prefix="cards_html_")
    os.makedirs(keep_dir, exist_ok=True)
    try:
        outputs, modes = [], []
        for i, card in enumerate(cards, 1):
            html_path = os.path.join(keep_dir, "%s-%02d.html" % (args.prefix, i))
            with io.open(html_path, "w", encoding="utf-8") as f:
                f.write(build_html(card, i, len(cards), theme, brand, size, not args.no_page))
            out = os.path.join(args.out_dir, "%s-%02d.png" % (args.prefix, i))
            ok, why = screenshot_browser(html_path, out, size, args.scale)
            if not ok:
                ok2, why2 = screenshot_playwright(html_path, out, size, args.scale)
                if not ok2:
                    print(json.dumps({"ok": False, "reason": "%s | %s" % (why, why2)}, ensure_ascii=False))
                    return 3
                modes.append(why2)
            else:
                modes.append(why)
            outputs.append(out)

        if args.format == "jpg":
            converted = []
            for p in outputs:
                j = to_jpg(p)
                if j:
                    converted.append(j)
            if not converted:
                print(json.dumps({"ok": True, "warning": "Pillow 不可用，已保持 PNG 输出",
                                  "files": outputs}, ensure_ascii=False))
                return 0
            outputs = converted

        merged = None
        if args.merge:
            pngs = [os.path.join(args.out_dir, "%s-%02d.png" % (args.prefix, i)) for i in range(1, len(cards) + 1)]
            merged = merge_long(pngs, os.path.join(args.out_dir, "%s-long.png" % args.prefix))

        # JPG 模式下清理中间 PNG，避免输出目录里两种格式混在一起
        if args.format == "jpg" and outputs and outputs[0].lower().endswith(".jpg"):
            for i in range(1, len(cards) + 1):
                p = os.path.join(args.out_dir, "%s-%02d.png" % (args.prefix, i))
                if os.path.isfile(p):
                    try:
                        os.remove(p)
                    except OSError:
                        pass

        print(json.dumps({
            "ok": True,
            "count": len(cards),
            "theme": theme,
            "size": "%dx%d" % size,
            "renderer": sorted(set(modes)),
            "files": outputs,
            "merged": merged,
            "html_dir": keep_dir if args.keep_html else None,
        }, ensure_ascii=False, indent=2))
        return 0
    finally:
        # 中间 HTML 用临时目录时用完即删，避免每次渲染泄漏一批目录
        if not args.keep_html:
            shutil.rmtree(keep_dir, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
