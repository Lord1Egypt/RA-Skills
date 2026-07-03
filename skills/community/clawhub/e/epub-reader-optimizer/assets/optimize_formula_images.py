"""optimize_formula_images.py
处理"公式即图片"型 EPUB（出版社/Sigil 流水线产出，公式被栅格化为 GIF 图片）。

主要工作：
1. 识别 <img> 是公式还是普通插图（看 alt 属性）。
2. 把公式 img 包裹成 <span class="math-inline" data-latex="...">，CSS 即可按行内/块级双轨渲染。
3. 给非公式 img 加 class="content-img"，由 CSS 控制响应式尺寸。
4. 给 <pre> 加 class="code-block"，由 CSS 加边框/等宽字体。
5. 给"段落只含一个 img"的孤立公式段加 class="formula-block"，由 CSS 居中独占一行。

用法：
    python optimize_formula_images.py <xhtml_file_or_dir>

支持单文件或递归处理目录下所有 .xhtml/.html。
"""
import re
import sys
from pathlib import Path


# ---------- 公式识别 ----------

def has_math_formula(alt_text: str) -> bool:
    """判断 img 的 alt 是否是数学公式 / 数学符号。

    关键补丁：≤4 字符的纯拉丁/希腊字母/数字也视作数学符号（如 x、y、k、x_i、N1）。
    否则单字符公式图会被漏判，CSS 走 block 规则导致独占一行。
    """
    if alt_text is None:
        return False
    s = alt_text.strip()
    if s == "" or s == "{%}":
        return False
    # LaTeX 命令、上下标、大括号
    if re.search(r"\\[a-zA-Z]+|[\\{}_^]", s):
        return True
    # 常见数学符号 / 运算符 / 希腊字母
    math_chars = "=+−×÷≤≥≠≈∞√∑∫∈⊂⊆∩∪σμθβαλγδπωε∂"
    if any(c in s for c in math_chars):
        return True
    # 短(≤4)的纯字母/数字 — 视为数学符号
    if len(s) <= 4 and re.fullmatch(r"[A-Za-zα-ωΑ-Ω0-9\s,\.\;]+", s):
        return True
    # 单字母+1 位下标(如 x1, N2)
    if re.fullmatch(r"[A-Za-z][\d]?", s):
        return True
    return False


# ---------- HTML 转义 ----------

def html_escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
         .replace('"', "&quot;")
         .replace("<", "&lt;")
         .replace(">", "&gt;")
    )


# ---------- 主处理 ----------

def process(html: str) -> str:
    """对单个 xhtml 文档做转换，返回新内容。"""

    # 1. 处理所有 <img .../> —— 区分公式 vs 内容图
    def wrap_img(m):
        full = m.group(0)
        alt_m = re.search(r'alt="([^"]*)"', full)
        src_m = re.search(r'src="([^"]*)"', full)
        if not src_m:
            return full
        src = src_m.group(1)
        alt = alt_m.group(1) if alt_m else ""

        if has_math_formula(alt):
            return (
                f'<span class="math-inline" data-latex="{html_escape(alt)}">'
                f'<img src="{src}" alt="{html_escape(alt)}" class="formula-img" />'
                f"</span>"
            )
        # 普通内容图：加 content-img 类，由 CSS 控制行内/块级
        if 'class="' in full:
            return re.sub(r'class="([^"]*)"',
                          lambda x: f'class="{x.group(1)} content-img"',
                          full, count=1)
        return full.replace("<img ", '<img class="content-img" ', 1)

    html = re.sub(r"<img[^>]+/>", wrap_img, html)

    # 2. <pre> 加 code-block 类
    def tag_pre(m):
        tag = m.group(0)
        if 'class="' in tag:
            return re.sub(r'class="([^"]*)"',
                          lambda x: f'class="{x.group(1)} code-block"',
                          tag, count=1)
        return tag.replace("<pre", '<pre class="code-block"', 1)

    html = re.sub(r"<pre(?:\s[^>]*)?>", tag_pre, html)

    # 3. 给「段落只含一个公式 img」的孤立段落加 formula-block 类
    #    形态：<p>(可选空白)<span class="math-inline">...</span>(可选空白)</p>
    def tag_formula_block(m):
        attrs = m.group(1) or ""
        inner = m.group(2)
        if 'class="' in attrs:
            new_attrs = re.sub(r'class="([^"]*)"',
                               lambda x: f'class="{x.group(1)} formula-block"',
                               attrs, count=1)
        else:
            new_attrs = attrs + ' class="formula-block"'
        return f"<p{new_attrs}>{inner}</p>"

    html = re.sub(
        r'<p(\s[^>]*)?>\s*(<span class="math-inline"[^>]*>.*?</span>)\s*</p>',
        tag_formula_block,
        html,
        flags=re.DOTALL,
    )

    return html


def process_path(target: Path) -> int:
    """处理单文件或目录下所有 xhtml/html，返回处理文件数。"""
    if target.is_file():
        files = [target]
    elif target.is_dir():
        files = list(target.rglob("*.xhtml")) + list(target.rglob("*.html"))
    else:
        raise SystemExit(f"路径不存在：{target}")

    for f in files:
        src = f.read_text(encoding="utf-8")
        dst = process(src)
        f.write_text(dst, encoding="utf-8")
        print(f"  ✓ {f}  ({len(src):,} → {len(dst):,} bytes)")
    return len(files)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法：python optimize_formula_images.py <xhtml_file_or_dir>")
        sys.exit(1)
    n = process_path(Path(sys.argv[1]))
    print(f"完成，共处理 {n} 个文件。")
