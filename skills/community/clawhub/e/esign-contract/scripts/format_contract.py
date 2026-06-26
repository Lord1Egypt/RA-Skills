"""将 Markdown 合同内容转换为排版 PDF。

用法:
    python3 format_contract.py <input.md> <output.pdf>

支持的自定义语法:
    :::parties ... --- ... :::   当事人信息双栏
    :::signature ... --- ... ::: 签署区域双栏

支持的 Markdown 语法:
    # 标题 → 合同标题
    ## 标题 → 章节标题
    **粗体** → <strong>
    *斜体* → <em>
    - 列表项 → <ul><li>
    | 表格 | → <table>
    （1）枚举 → 悬挂缩进
    X.Y 条款 → 条款样式
"""

import html as html_module
import json
import os
import re
import sys
from pathlib import Path

try:
    import weasyprint
except (ImportError, OSError) as e:
    print(
        json.dumps(
            {
                "success": False,
                "error": f"WeasyPrint 不可用: {e}",
                "fix": "macOS: brew install pango cairo libffi glib && pip install weasyprint; "
                "Linux: apt install libpango-1.0-0 libcairo2 && pip install weasyprint",
            },
            ensure_ascii=False,
        ),
        file=sys.stderr,
    )
    sys.exit(1)


_CONFIG_DIR = Path.home() / ".config" / "esign-contract"
_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
_FONTS_DIR = _CONFIG_DIR / "fonts"
_BASE_CSS = """
@page {
    size: A4;
    margin: 2cm 2.5cm;

    @bottom-center {
        content: "第 " counter(page) " 页 / 共 " counter(pages) " 页";
        font-size: 9pt;
        color: #666;
    }
}

body {
    font-family: "Songti SC", "STSong", "SimSun", "宋体", "Noto Serif CJK SC", serif;
    font-size: 12pt;
    line-height: 1.25;
    color: #000;
}

.contract-number {
    text-align: right;
    text-indent: 0;
    font-size: 11pt;
    color: #333;
    margin-bottom: 0.5em;
}

h1.contract-title {
    font-family: "Heiti SC", "STHeiti", "SimHei", "黑体", "Noto Sans CJK SC", sans-serif;
    font-size: 22pt;
    text-align: center;
    margin-bottom: 1em;
    font-weight: bold;
}

.preamble {
    margin-bottom: 0.8em;
}

.preamble p {
    text-indent: 2em;
}

.parties-info {
    display: flex;
    justify-content: space-between;
    margin-bottom: 1em;
    border: 1px solid #ccc;
    padding: 0.8em;
}

.party-column {
    width: 48%;
}

.party-column p {
    margin: 0.3em 0;
    font-size: 12pt;
    text-indent: 0;
}

h2 {
    font-family: "Heiti SC", "STHeiti", "SimHei", "黑体", "Noto Sans CJK SC", sans-serif;
    font-size: 15pt;
    font-weight: bold;
    margin-top: 0.6em;
    margin-bottom: 0.3em;
    page-break-after: avoid;
}

h3 {
    font-family: "Heiti SC", "STHeiti", "SimHei", "黑体", "Noto Sans CJK SC", sans-serif;
    font-size: 13pt;
    font-weight: bold;
    margin-top: 0.5em;
    margin-bottom: 0.2em;
    page-break-after: avoid;
}

p {
    text-indent: 2em;
    margin: 0.15em 0;
}

strong {
    font-weight: bold;
}

em {
    font-style: italic;
}

.clause-item {
    text-indent: 0;
    padding-left: 3em;
    position: relative;
}

.clause-item .clause-num {
    position: absolute;
    left: 0;
    width: 3em;
    text-align: left;
}

.enum-item {
    text-indent: -2em;
    padding-left: 4em;
}

ul {
    padding-left: 3em;
    margin: 0.2em 0;
}

ul li {
    text-indent: 0;
    margin: 0.3em 0;
    list-style-type: disc;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0;
    font-size: 11pt;
}

th, td {
    border: 1px solid #333;
    padding: 0.5em 0.8em;
    text-align: left;
    text-indent: 0;
}

th {
    background-color: #f5f5f5;
    font-weight: bold;
}

.signature-area {
    display: flex;
    justify-content: space-between;
    margin-top: 2em;
    padding-top: 1em;
    border-top: 1px solid #ccc;
    page-break-inside: avoid;
}

.signature-block {
    width: 45%;
}

.signature-block .sig-role {
    font-weight: bold;
    font-size: 13pt;
    text-indent: 0;
    margin-bottom: 0.8em;
}

.signature-block .seal-anchor {
    text-indent: 0;
    margin: 2em 0;
    min-height: 4em;
}

.signature-block .sig-label {
    text-indent: 0;
    margin: 0.8em 0;
}

.signature-block .sig-text {
    text-indent: 0;
    margin: 0.3em 0;
    font-size: 11pt;
    color: #555;
}

.appendix {
    break-before: page;
}

.appendix h2 {
    font-size: 15pt;
}
"""

# ── 字体检测 ─────────────────────────────────────────────────

# 宋体（正文用）和黑体（标题用）的候选列表，按优先级排列
_SERIF_CANDIDATES = [
    "Songti SC",
    "STSong",
    "SimSun",
    "宋体",
    "Noto Serif CJK SC",
    "Noto Serif SC",
    "AR PL UMing CN",
    "WenQuanYi Zen Hei",
]
_SANS_CANDIDATES = [
    "Heiti SC",
    "STHeiti",
    "SimHei",
    "黑体",
    "Noto Sans CJK SC",
    "Noto Sans SC",
    "WenQuanYi Micro Hei",
    "Droid Sans Fallback",
]


def _detect_cjk_fonts() -> tuple[str, str]:
    """检测系统可用的中文宋体和黑体，返回 (serif_family, sans_family) CSS 声明。

    macOS/Linux：使用 fontconfig 的 fc-list 查询已安装的中文字体。
    Windows：枚举注册表 HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Fonts。
    如果完全找不到 CJK 字体，回退到 serif/sans-serif。
    """
    import subprocess
    import sys as _sys

    available = set()

    if _sys.platform == "win32":
        # Windows：从注册表读取已安装字体名称
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts",
            )
            i = 0
            while True:
                try:
                    name, _, _ = winreg.EnumValue(key, i)
                    # 去掉括号内的文件名后缀，如 "SimSun & NSimSun (TrueType)"
                    clean = name.split("(")[0].strip()
                    available.add(clean)
                    i += 1
                except OSError:
                    break
            winreg.CloseKey(key)
        except Exception:
            pass
    else:
        # macOS / Linux：使用 fontconfig fc-list
        try:
            result = subprocess.run(
                ["fc-list", ":lang=zh", "family"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            for line in result.stdout.strip().split("\n"):
                for name in line.split(","):
                    available.add(name.strip().strip("\\"))
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

    # 也检查 fonts/ 目录下的自带字体
    local_fonts = []
    if _FONTS_DIR.exists():
        for f in _FONTS_DIR.glob("*.otf"):
            local_fonts.append(f)
        for f in _FONTS_DIR.glob("*.ttf"):
            local_fonts.append(f)

    def pick(candidates, fallback):
        matched = []
        for name in candidates:
            if any(name.lower() in a.lower() for a in available):
                matched.append(f'"{name}"')
        if not matched:
            matched.append(fallback)
        return ", ".join(matched) + f", {fallback}"

    serif = pick(_SERIF_CANDIDATES, "serif")
    sans = pick(_SANS_CANDIDATES, "sans-serif")
    return serif, sans


def _build_css(serif_family: str, sans_family: str) -> str:
    """构建基础 CSS，动态替换字体声明，注册本地字体。"""
    base_css = _BASE_CSS

    # 注册 fonts/ 目录下的本地字体文件
    font_faces = []
    if _FONTS_DIR.exists():
        for ext in ("*.otf", "*.ttf"):
            for font_file in _FONTS_DIR.glob(ext):
                font_name = font_file.stem
                font_faces.append(
                    f'@font-face {{ font-family: "{font_name}"; '
                    f'src: url("file://{font_file.resolve()}"); }}'
                )
    if font_faces:
        base_css = "\n".join(font_faces) + "\n" + base_css

    # 替换所有 font-family 中的宋体系列（匹配任何候选宋体名称开头的声明）
    _serif_pattern = "|".join(re.escape(c) for c in _SERIF_CANDIDATES)
    base_css = re.sub(
        rf'font-family:\s*(?:"?(?:{_serif_pattern})"?)[^;]*;',
        f"font-family: {serif_family};",
        base_css,
    )
    # 替换所有 font-family 中的黑体系列
    _sans_pattern = "|".join(re.escape(c) for c in _SANS_CANDIDATES)
    base_css = re.sub(
        rf'font-family:\s*(?:"?(?:{_sans_pattern})"?)[^;]*;',
        f"font-family: {sans_family};",
        base_css,
    )
    return base_css


# ── Inline 格式化 ──────────────────────────────────────────────


def _inline(text: str) -> str:
    """处理行内 Markdown 格式：粗体、斜体、HTML 转义。"""
    text = html_module.escape(text)
    # 粗体 **text**
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    # 斜体 *text*（不匹配已处理的 strong 标签）
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", text)
    return text


# ── Block 解析 ─────────────────────────────────────────────────

# 条款编号模式：1.1 / 2.3 / 10.1 等
_CLAUSE_RE = re.compile(r"^(\d+\.\d+)\s+(.+)")
# 枚举模式：（1）/ (1) / （一）等
_ENUM_RE = re.compile(r"^[（(][\d一二三四五六七八九十]+[）)]\s*(.+)")
# 自定义块语法：三个及以上冒号
_FENCE_PARTIES_RE = re.compile(r"^:{3,}parties$")
_FENCE_SIGNATURE_RE = re.compile(r"^:{3,}signature$")
_FENCE_END_RE = re.compile(r"^:{3,}$")
# 合同编号行
_CONTRACT_NUM_RE = re.compile(r"^合同编号[：:]\s*(.+)")
# 鉴于条款
_PREAMBLE_RE = re.compile(r"^鉴于[：:]?\s*")


def _is_special_line(stripped: str) -> bool:
    """判断是否为需要特殊处理的行（非普通段落文本）。"""
    if not stripped:
        return True
    if stripped in (":::parties", ":::signature", ":::"):
        return True
    if (
        _FENCE_PARTIES_RE.match(stripped)
        or _FENCE_SIGNATURE_RE.match(stripped)
        or _FENCE_END_RE.match(stripped)
    ):
        return True
    if stripped.startswith(("# ", "## ", "### ", "- ", "|")):
        return True
    if _CONTRACT_NUM_RE.match(stripped):
        return True
    if _PREAMBLE_RE.match(stripped):
        return True
    if _CLAUSE_RE.match(stripped):
        return True
    if _ENUM_RE.match(stripped):
        return True
    return False


def markdown_to_html(md: str) -> str:
    """将合同 Markdown 转换为带样式类的 HTML。"""
    lines = md.strip().split("\n")
    html_parts = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # 空行
        if not stripped:
            i += 1
            continue

        # 当事人信息块
        if _FENCE_PARTIES_RE.match(stripped):
            i += 1
            html_parts.append(_parse_parties(lines, i))
            i = _skip_to_end_fence(lines, i)
            continue

        # 签署区域块
        if _FENCE_SIGNATURE_RE.match(stripped):
            i += 1
            html_parts.append(_parse_signature(lines, i))
            i = _skip_to_end_fence(lines, i)
            continue

        # 合同编号
        m = _CONTRACT_NUM_RE.match(stripped)
        if m:
            html_parts.append(f'<p class="contract-number">{_inline(stripped)}</p>')
            i += 1
            continue

        # 标题 h1 → 合同标题
        if stripped.startswith("# "):
            title = stripped[2:].strip()
            html_parts.append(f'<h1 class="contract-title">{_inline(title)}</h1>')
            i += 1
            continue

        # 标题 h2 → 章节标题
        if stripped.startswith("## "):
            title = stripped[3:].strip()
            html_parts.append(f"<h2>{_inline(title)}</h2>")
            i += 1
            continue

        # 标题 h3
        if stripped.startswith("### "):
            title = stripped[4:].strip()
            html_parts.append(f"<h3>{_inline(title)}</h3>")
            i += 1
            continue

        # 无序列表
        if stripped.startswith("- "):
            items = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                items.append(lines[i].strip()[2:].strip())
                i += 1
            li_html = "".join(f"<li>{_inline(item)}</li>" for item in items)
            html_parts.append(f"<ul>{li_html}</ul>")
            continue

        # 表格
        if stripped.startswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1
            html_parts.append(_parse_table(table_lines))
            continue

        # 鉴于条款
        if _PREAMBLE_RE.match(stripped):
            # 收集鉴于段落（可能多行）
            preamble_lines = [stripped]
            i += 1
            while (
                i < len(lines)
                and lines[i].strip()
                and not lines[i].strip().startswith("##")
            ):
                preamble_lines.append(lines[i].strip())
                i += 1
            preamble_text = "".join(_inline(l) for l in preamble_lines)
            html_parts.append(f'<div class="preamble"><p>{preamble_text}</p></div>')
            continue

        # 条款编号 X.Y
        m = _CLAUSE_RE.match(stripped)
        if m:
            num, text = m.group(1), m.group(2)
            html_parts.append(
                f'<p class="clause-item"><span class="clause-num">{num}</span> {_inline(text)}</p>'
            )
            i += 1
            continue

        # 枚举项 （1）...
        m = _ENUM_RE.match(stripped)
        if m:
            # 保留完整行（含编号）
            html_parts.append(f'<p class="enum-item">{_inline(stripped)}</p>')
            i += 1
            continue

        # 普通段落 — 合并连续非特殊行为一个 <p>
        para_lines = [stripped]
        i += 1
        while (
            i < len(lines)
            and lines[i].strip()
            and not _is_special_line(lines[i].strip())
        ):
            para_lines.append(lines[i].strip())
            i += 1
        html_parts.append(f"<p>{_inline(' '.join(para_lines))}</p>")

    body = "\n".join(html_parts)
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"></head>
<body>
{body}
</body>
</html>"""


def _parse_parties(lines, start):
    """解析 :::parties 块 — 当事人信息双栏。"""
    left_lines = []
    right_lines = []
    current = left_lines

    i = start
    while i < len(lines) and not _FENCE_END_RE.match(lines[i].strip()):
        if lines[i].strip() == "---":
            current = right_lines
        elif lines[i].strip():
            current.append(lines[i].strip())
        i += 1

    def render_column(col_lines):
        parts = []
        for line in col_lines:
            parts.append(f"<p>{_inline(line)}</p>")
        return "".join(parts)

    left_html = render_column(left_lines)
    right_html = render_column(right_lines)

    return f"""<div class="parties-info">
  <div class="party-column">{left_html}</div>
  <div class="party-column">{right_html}</div>
</div>"""


def _parse_signature(lines, start):
    """解析 :::signature 块 — 签署区域双栏，结构化输出。"""
    left_lines = []
    right_lines = []
    current = left_lines

    i = start
    while i < len(lines) and not _FENCE_END_RE.match(lines[i].strip()):
        if lines[i].strip() == "---":
            current = right_lines
        elif lines[i].strip():
            current.append(lines[i].strip())
        i += 1

    # 字段标签模式：以冒号结尾的行（签署人：、日期：、地址：等）
    _sig_label_re = re.compile(r"^.+[：:]$")

    def render_sig_block(sig_lines):
        if not sig_lines:
            return ""
        parts = []
        for line in sig_lines:
            if line.startswith("【") and line.endswith("】"):
                # 签章锚点（如【甲方签章处】）
                parts.append(f'<p class="seal-anchor">{_inline(line)}</p>')
            elif _sig_label_re.match(line):
                # 字段标签（签署人：、日期：等）
                parts.append(f'<p class="sig-label">{_inline(line)}</p>')
            elif any(kw in line for kw in ("签章", "盖章", "签字")):
                # 角色标题（甲方（签章）、乙方（盖章）等）
                parts.append(f'<p class="sig-role">{_inline(line)}</p>')
            else:
                # 其他说明文字
                parts.append(f'<p class="sig-text">{_inline(line)}</p>')
        return "".join(parts)

    left_html = render_sig_block(left_lines)
    right_html = render_sig_block(right_lines)

    return f"""<div class="signature-area">
  <div class="signature-block">{left_html}</div>
  <div class="signature-block">{right_html}</div>
</div>"""


def _parse_table(lines):
    """将 Markdown 表格转为 HTML table。"""
    if len(lines) < 2:
        return ""

    rows = []
    for line in lines:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows.append(cells)

    header = rows[0]
    data_rows = rows[2:] if len(rows) > 2 else []

    th = "".join(f"<th>{_inline(c)}</th>" for c in header)
    tbody = ""
    for row in data_rows:
        td = "".join(f"<td>{_inline(c)}</td>" for c in row)
        tbody += f"<tr>{td}</tr>\n"

    return f"""<table>
<thead><tr>{th}</tr></thead>
<tbody>{tbody}</tbody>
</table>"""


def _skip_to_end_fence(lines, start):
    """跳到 ::: 结束标记之后（兼容三个及以上冒号）。"""
    i = start
    while i < len(lines) and not _FENCE_END_RE.match(lines[i].strip()):
        i += 1
    return i + 1


def markdown_to_pdf(md: str, output_path: str):
    """Markdown → HTML → PDF（含样式，自动检测系统字体）。"""
    html_str = markdown_to_html(md)
    serif_family, sans_family = _detect_cjk_fonts()
    dynamic_css = _build_css(serif_family, sans_family)
    css = weasyprint.CSS(string=dynamic_css)
    weasyprint.HTML(string=html_str).write_pdf(output_path, stylesheets=[css])


def _cli():
    if len(sys.argv) < 3:
        print(
            json.dumps(
                {"error": "用法: python3 format_contract.py <input.md> <output.pdf>"}
            )
        )
        sys.exit(1)

    input_path, output_path = sys.argv[1], sys.argv[2]
    try:
        md = Path(input_path).read_text(encoding="utf-8")
        markdown_to_pdf(md, output_path)
        print(
            json.dumps(
                {
                    "output": output_path,
                    "size": os.path.getsize(output_path),
                }
            )
        )
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    _cli()
