#!/usr/bin/env python3
"""
inherit_layout.py — 「布局继承」模式

当输入已经是一份**布局优雅的成品 HTML**（自带栅格 / banner / 固定比例 / 精心间距）时，
不要把它打散重做成通用 data-role 骨架，而是**保留其原始布局与结构**，
只把它的「配色」接到主题系统，这样套 19 套主题时**布局原样不动、只换颜色**。

## 契约（agent 使用前需先做一步）

把源 HTML 的 `:root` 里所有硬编码颜色，改成引用这 7 个语义变量之一：

    --eh-primary         主色（强调 / 标题高亮 / banner / 编号底）
    --eh-primary-light   主色浅版（标签底 / hover 底 / 浅色块）
    --eh-bg              页面最外层背景
    --eh-surface         卡片 / 容器 / 内容面背景
    --eh-text            主文字
    --eh-text-muted      次要文字 / 说明文字
    --eh-border          分隔线 / 边框

例：源 HTML 原本
    :root{ --b:#1254C8; --d:#1A1D2E; --gy:#6B7280; --bg:#F5F6FA; ... }
改成
    :root{
      --eh-primary:#1254C8; --eh-text:#1A1D2E; --eh-text-muted:#6B7280; --eh-bg:#F5F6FA;
      /* 下面保持引用，原有 class 不用改 */
      --b:var(--eh-primary); --d:var(--eh-text); --gy:var(--eh-text-muted); --bg:var(--eh-bg);
    }
布局 CSS（.cols/.hdr/.it 等）一律不动。

## 本脚本做什么

`inherit_layout.py <html> --style <key> -o <out>`：
解析该主题的 7 个语义变量真实色值，在 </head> 前注入一个**覆盖 :root 块**：
    :root{ --eh-primary:<theme primary>; --eh-bg:<theme bg>; ... }
于是源 HTML 的所有颜色随主题切换，布局/结构完全保留。

不依赖 data-role，不调用主题引擎的 enhance（那会重排结构）；只读主题 .css 解析变量。
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _engine import load_engine  # noqa: E402

# 主题语义别名 → easy-html 继承变量
ALIAS_MAP = {
    "--eh-primary": "--primary",
    "--eh-primary-light": "--primary-light",
    "--eh-bg": "--bg-main",
    "--eh-surface": "--surface",
    "--eh-text": "--text-main",
    "--eh-text-muted": "--text-muted",
    "--eh-border": "--border-color",
}

# 字体语义别名 → 主题字体变量（按各主题命名前缀尝试，找不到则跳过）
# 继承时把主题的正文/标题字体栈也带过来，让 palace/ink/newspaper 等
# 特色字体主题在「布局继承」模式下也能古色古香（否则只换色、字体退化系统默认）
FONT_ALIAS_CANDIDATES = {
    # 正文字体：各主题正文字体变量的常见命名
    "--eh-font": ["--pl-body", "--ik-serif", "--np-body", "--sp-fb",
                  "--cp-ft", "--bl-fs", "--font-body", "--font-main"],
    # 标题字体：各主题标题字体变量的常见命名
    "--eh-font-head": ["--pl-serif", "--ik-serif", "--np-serif", "--sp-ft",
                       "--cp-ft", "--bl-fs", "--font-head", "--font-title"],
}


def _log(m):
    print(m, file=sys.stderr)


def load_enhancer():
    """复用 html-golive 的 css_style_enhancer 拿 load_css / STYLE_MAP。"""
    return load_engine()


def resolve_theme_vars(css):
    """把主题 css 里的 7 个语义别名解析成具体色值（递归解 var()）。"""
    defs = dict(re.findall(r'(--[a-z0-9-]+)\s*:\s*([^;!]+)', css))

    def resolve(v, depth=0):
        v = v.strip()
        if depth > 8:
            return v
        m = re.match(r'var\((--[a-z0-9-]+)\)', v)
        if m and m.group(1) in defs:
            return resolve(defs[m.group(1)], depth + 1)
        return v

    out = {}
    for eh, alias in ALIAS_MAP.items():
        if alias in defs:
            out[eh] = resolve(defs[alias])
    return out


def resolve_theme_fonts(css):
    """从主题 css 提取正文/标题字体栈 + 字体加载源（@font-face 块 + @import）。
    返回 (font_vars: dict, font_imports: list[str], font_faces: list[str])。"""
    defs = dict(re.findall(r'(--[a-z0-9-]+)\s*:\s*([^;!]+)', css))

    def resolve(v, depth=0):
        v = v.strip()
        if depth > 8:
            return v
        m = re.match(r'var\((--[a-z0-9-]+)\)', v)
        if m and m.group(1) in defs:
            return resolve(defs[m.group(1)], depth + 1)
        return v

    font_vars = {}
    for eh, candidates in FONT_ALIAS_CANDIDATES.items():
        for alias in candidates:
            if alias in defs:
                font_vars[eh] = resolve(defs[alias])
                break
    # 提取字体加载源（继承站点要带上才能加载特色字体）：
    # ① @font-face 块（自托管/CDN woff2）— 整块原样保留
    # ② @import url(...font...)（兼容用 Google Fonts @import 的主题）
    font_faces = re.findall(r"@font-face\s*\{[^}]*\}", css, re.I)
    imports = re.findall(r"@import\s+url\(['\"]?([^'\")]+)['\"]?\)\s*;", css)
    font_imports = [u for u in imports if "font" in u.lower()]
    return font_vars, font_imports, font_faces


def main():
    ap = argparse.ArgumentParser(description="布局继承：保留原 HTML 布局，只换主题配色")
    ap.add_argument("html", help="源 HTML（其 :root 颜色已改成引用 --eh-* 变量）")
    ap.add_argument("--style", help="主题 key（同 apply_style）；--check 时可省略")
    ap.add_argument("-o", "--output", help="输出路径，默认覆盖输入")
    ap.add_argument("--check", action="store_true",
                    help="只检查源 HTML 是否已用 --eh-* 变量，不写文件")
    args = ap.parse_args()

    html = open(args.html, encoding="utf-8").read()

    # 检查源是否已接入 --eh-* 契约
    used = [eh for eh in ALIAS_MAP if eh in html]
    if not used:
        _log("⚠️ 源 HTML 没有用任何 --eh-* 变量。布局继承要求先把源 :root 颜色改成引用 "
             "--eh-primary/--eh-bg/--eh-surface/--eh-text/--eh-text-muted/--eh-border/"
             "--eh-primary-light。详见脚本头部契约说明。")
        if args.check:
            sys.exit(1)
        sys.exit(1)
    if args.check:
        _log(f"✅ 源 HTML 已接入 {len(used)} 个继承变量：{', '.join(used)}")
        return

    if not args.style:
        _log("❌ 套色需要 --style <key>（或用 --check 仅校验）")
        sys.exit(1)

    enhancer = load_enhancer()
    if args.style not in enhancer.STYLE_MAP:
        _log(f"未知主题 {args.style}；可用：{', '.join(enhancer.STYLE_MAP.keys())}")
        sys.exit(1)
    css = enhancer.load_css(args.style)
    theme_vars = resolve_theme_vars(css)
    if not theme_vars:
        _log(f"❌ 主题 {args.style} 未解析到语义别名，无法继承")
        sys.exit(1)

    # 字体继承：把主题正文/标题字体栈 + 字体加载链接也带过来
    # 让 palace/ink/newspaper 等特色字体主题在「布局继承」模式下也能正确呈现字体
    # （否则只换色、字体退化系统默认 —— palace 会徒有金色而无毛笔字）
    font_vars, font_imports, font_faces = resolve_theme_fonts(css)
    # 也并入 FONT_PRELOADS（@import 与 preload 双源，确保字体加载）
    preload_url = enhancer.FONT_PRELOADS.get(args.style, "") if hasattr(enhancer, "FONT_PRELOADS") else ""

    decls = "\n".join(f"  {eh}: {val} !important;" for eh, val in theme_vars.items())
    # 字体变量 + 应用到 body/标题
    font_decls = ""
    font_apply = ""
    if font_vars:
        font_decls = "\n".join(f"  {eh}: {val} !important;" for eh, val in font_vars.items())
        body_font = font_vars.get("--eh-font", "")
        head_font = font_vars.get("--eh-font-head", body_font)
        if body_font:
            # 精确覆盖正文元素，避免误伤 <code>/<pre>/图标字体（如 Font Awesome <i class=fa-*>）
            font_apply += (
                f'body, p, li, td, th, blockquote, caption, label, [data-role] '
                f'{{ font-family: var(--eh-font) !important; }}\n'
                # 豁免：代码/等宽块 + 图标字体类（font-family: revert 回退到各自原始定义）
                f'code, pre, kbd, samp, '
                f'[class*="icon"], [class*="fa-"], [class*="iconfont"] '
                f'{{ font-family: revert !important; }}\n'
            )
        if head_font:
            font_apply += f'h1, h2, h3, h4, h5, h6, [data-role*="title"], [data-role*="head"] {{ font-family: var(--eh-font-head) !important; }}\n'
    # 字体加载块：CSS 规范要求 @import 必须在最前；@font-face 块随后原样保留
    font_load = ""
    seen = set()
    for u in font_imports + ([preload_url] if preload_url else []):
        if u and u not in seen:
            seen.add(u)
            font_load += f'@import url("{u}");\n'
    for face in font_faces:
        font_load += face + "\n"

    override = (
        f'\n<style data-eh-inherit="{args.style}">\n'
        f'{font_load}'
        f':root{{\n{decls}\n{font_decls}\n}}\n'
        f'{font_apply}'
        f'/* 布局继承：保留源布局，覆盖配色 + 字体 → 主题 {args.style} */\n'
        f'</style>\n'
    )

    # 先剥掉旧的继承覆盖块（幂等，支持反复换主题）
    html = re.sub(r'\n?<style data-eh-inherit="[^"]*">.*?</style>\n?', '\n', html,
                  flags=re.S)

    # 注入到 </head> 前（确保覆盖源 :root）
    if re.search(r'</head>', html, re.I):
        html = re.sub(r'</head>', override + '</head>', html, count=1, flags=re.I)
    else:
        html = override + html

    out = args.output or args.html
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    name = enhancer.STYLE_MAP[args.style]
    _log(f"✅ 已继承布局 + 套主题「{name}」({args.style}) → {out}")
    _log(f"   覆盖配色：{', '.join(theme_vars.keys())}")
    if font_vars:
        _log(f"   继承字体：{', '.join(font_vars.keys())}（{len(seen)} 个 @import + {len(font_faces)} 个 @font-face）")
    else:
        _log("   ⚠️ 该主题未解析到字体变量，沿用源 HTML 字体")


if __name__ == "__main__":
    main()
