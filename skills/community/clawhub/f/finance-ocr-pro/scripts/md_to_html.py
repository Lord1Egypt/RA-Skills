"""
OCR Markdown (with HTML tables) → Side-by-side HTML Comparison Report
with Mermaid Diagram Rendering

Generates ONE self-contained HTML file that shows:
- Left:  source scanned page image (embedded as base64 data URL)
- Right: rendered OCR-extracted Markdown (OCR tables are already HTML <table> blocks)

Mermaid ```mermaid``` fenced code blocks are rendered as interactive SVG
diagrams via mermaid.js.

The output HTML is fully self-contained by embedding bundled local
MathJax and Mermaid assets inline. No network requests are performed
during report generation or while viewing the generated report.

File naming convention:
    Images:   <name>_<page>.png|jpeg|jpg|webp|gif   e.g. 陕国投年报_00001.png
    Markdown: <name>_<page>.md|markdown              e.g. 陕国投年报_00001.md
    where <name> is an arbitrary-length stem (may contain underscores) and
    <page> is a zero-padded page number (typically 5 digits).

Cross-platform: works on macOS, Windows, and Linux.

Dependencies: markdown2
Bundled locally: MathJax 3.2.2 (tex-svg-full), Mermaid 11.14.0
"""

from __future__ import annotations

import argparse
import base64
import html
import re
from pathlib import Path

import markdown2


# ==============================================================================
# Filename Parsing / Scanning Utilities
# ==============================================================================

_PATTERN_FILENAME = re.compile(
    r"^(?P<base>.+)_(?P<num>\d+)\.(?P<ext>[^.]+)$",
    re.IGNORECASE,
)

_IMG_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tif", ".tiff"}
_MD_EXTS = {".md", ".markdown"}

_EXT_PRIORITY = {
    ".png": 0,
    ".webp": 1,
    ".jpg": 2,
    ".jpeg": 3,
    ".gif": 4,
    ".md": 0,
    ".markdown": 1,
}


def _escape_attr(text: str) -> str:
    return html.escape(text, quote=True)


def _escape_text(text: str) -> str:
    return html.escape(text, quote=False)


def _scan_pages_by_base_and_num(folder: Path, allowed_exts: set) -> dict[tuple[str, str], Path]:
    """
    Scan a directory for files like XXXXX_00001.png / XXXXX_00001.md

    Returns:
        mapping[(base, page_num_str)] = Path
    """
    mapping: dict[tuple[str, str], Path] = {}
    if not folder.exists():
        return mapping

    for file_path in folder.iterdir():
        if not file_path.is_file():
            continue

        suffix = file_path.suffix.lower()
        if suffix not in allowed_exts:
            continue

        m = _PATTERN_FILENAME.match(file_path.name)
        if not m:
            continue

        base_name = m.group("base")
        num = m.group("num")

        key = (base_name, num)
        if key not in mapping:
            mapping[key] = file_path
        else:
            cur = mapping[key]
            cur_pri = _EXT_PRIORITY.get(cur.suffix.lower(), 999)
            new_pri = _EXT_PRIORITY.get(suffix, 999)
            if new_pri < cur_pri:
                mapping[key] = file_path

    return mapping


def _sorted_keys(keys: list[tuple[str, str]]) -> list[tuple[str, str]]:
    def _k(item: tuple[str, str]) -> tuple[str, int, str]:
        base_name, num = item
        try:
            n = int(num)
        except ValueError:
            n = 10**18
        return (base_name.lower(), n, num)

    return sorted(keys, key=_k)


# ==============================================================================
# Image Processing
# ==============================================================================

_MIME_MAP = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".gif": "image/gif",
    ".bmp": "image/bmp",
    ".tif": "image/tiff",
    ".tiff": "image/tiff",
}


def _image_to_base64_data_url(img_path: Path) -> str:
    mime = _MIME_MAP.get(img_path.suffix.lower(), "image/png")
    b64 = base64.b64encode(img_path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


# ==============================================================================
# Markdown Preprocessing
# ==============================================================================

_FIGURE_PLACEHOLDER_LINE = re.compile(r"^\s*!\[(?P<desc>.*?)\]\s*$")


def _ensure_blank_lines_around_tables(md: str) -> str:
    """
    Ensure blank lines surround <table>...</table> blocks so that
    Markdown parsers treat them as block-level HTML (avoids <p><table>…).
    """
    lines = md.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip().lower()

        if stripped.startswith("<table>") or stripped.startswith("<table "):
            if out and out[-1].strip() != "":
                out.append("")
            out.append(line)

            if "</table>" not in stripped:
                i += 1
                while i < len(lines):
                    out.append(lines[i])
                    if "</table>" in lines[i].strip().lower():
                        i += 1
                        break
                    i += 1
            else:
                i += 1

            if i < len(lines) and out and out[-1].strip() != "":
                out.append("")
            continue

        out.append(line)
        i += 1

    return "\n".join(out)


def _convert_ocr_figure_placeholders(md: str) -> str:
    """
    OCR prompt uses a non-standard placeholder line:
      ![Concise description ≤20 words]
    Render it human-readably without requiring a URL.
    """
    out_lines: list[str] = []
    for line in md.splitlines():
        m = _FIGURE_PLACEHOLDER_LINE.match(line)
        if m:
            desc = m.group("desc")
            out_lines.append(f'> **Figure:** {desc}')
        else:
            out_lines.append(line)
    return "\n".join(out_lines)


def _normalize_indentation(markdown_text: str) -> str:
    """
    Prevent accidental code blocks from OCR-added indentation.

    Additionally: if a line looks like an HTML table tag but is indented 4+ spaces,
    de-indent it to avoid Markdown treating it as code.
    """
    lines = markdown_text.split("\n")
    result: list[str] = []
    in_fenced_code = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fenced_code = not in_fenced_code
            result.append(line)
            continue

        if in_fenced_code:
            result.append(line)
            continue

        indent_match = re.match(r"^( {4,}|\t+)", line)
        if indent_match:
            content = line.lstrip()

            if not content:
                result.append(line)
                continue

            if re.match(r"^</?(table|thead|tbody|tr|th|td)\b", content.strip(), re.IGNORECASE):
                result.append(content)
                continue

            if _is_likely_prose(content):
                result.append(content)
            else:
                result.append(line)
        else:
            result.append(line)

    return "\n".join(result)


_RE_NON_LATIN = re.compile(
    r"["
    r"\u0400-\u04FF"    # Cyrillic
    r"\u0600-\u06FF"    # Arabic
    r"\u0900-\u097F"    # Devanagari
    r"\u0980-\u09FF"    # Bengali
    r"\u0A00-\u0A7F"    # Gurmukhi
    r"\u0E00-\u0E7F"    # Thai
    r"\u1000-\u109F"    # Myanmar
    r"\u3040-\u309F"    # Hiragana
    r"\u30A0-\u30FF"    # Katakana
    r"\u4E00-\u9FFF"    # CJK Unified Ideographs
    r"\uAC00-\uD7AF"    # Hangul Syllables
    r"]"
)


_PROSE_PATTERNS = [re.compile(p) for p in (
    r"^注[*\d\s]*[:：]",
    r"^(资料|数据)?来源[:：]",
    r"^[备说]注[:：]",
    r"^[（\(][一二三四五六七八九十\d]+[）\)]",
    r"^[一二三四五六七八九十]+[、.]",
    r"^[\d]+[、.\)）]\s*\S",
    r"^[•·\-\*]\s+\S",
    r"^\*+\s*\S",
    r"^##+\s",
    r"^[A-Z][a-z].*[.!?]$",
)]

_CODE_PATTERNS = [re.compile(p, re.IGNORECASE) for p in (
    r"^(def|class|import|from|if|for|while|return|function|var|let|const|public|private)\s",
    r"^[{}\[\]<>]",
    r"[{}\[\];]$",
    r"^//",
    r"^\s*@\w+",
    r"^(SELECT|INSERT|UPDATE|DELETE|CREATE|DROP)\s",
    r"^\$\w+",
    r"^<\?",
    r"^<!",
)]

_RE_LETTERS = re.compile(r"[a-zA-Z]")


def _is_likely_prose(content: str) -> bool:
    """Heuristic: return True if *content* looks like natural-language prose rather than code."""
    if re.search(r"(?<!\\)\$", content):
        return True
    if re.search(r"\\\(|\\\)|\\\[|\\\]", content):
        return True

    has_non_latin = bool(_RE_NON_LATIN.search(content))

    if any(p.match(content) for p in _PROSE_PATTERNS):
        return True
    if any(p.search(content) for p in _CODE_PATTERNS):
        return False
    if has_non_latin:
        return True

    letter_ratio = len(_RE_LETTERS.findall(content)) / max(len(content), 1)
    return letter_ratio > 0.6


# ==============================================================================
# Math Protection (for Markdown conversion stability)
# ==============================================================================

def _protect_math_expressions(md: str) -> tuple[str, list[tuple[str, str]]]:
    """
    Shield LaTeX math ($...$ and $$...$$) from Markdown parsing, then restore as HTML
    wrappers so MathJax can reliably typeset.

    Important: do NOT match escaped dollars (\\$) used for currency/literals.
    """
    math_blocks: list[tuple[str, str]] = []
    protected = md

    def _ph(i: int) -> str:
        return f"\uE000MATH{i}\uE001"

    display_re = re.compile(r"(?<!\\)\$\$(.+?)(?<!\\)\$\$", re.DOTALL)
    matches = list(display_re.finditer(protected))
    for m in reversed(matches):
        idx = len(math_blocks)
        placeholder = _ph(idx)
        original = m.group(0)
        escaped = html.escape(original, quote=False)
        html_elem = f'<div class="math-display">{escaped}</div>'
        math_blocks.append((placeholder, html_elem))
        protected = protected[: m.start()] + placeholder + protected[m.end() :]

    inline_re = re.compile(r"(?<!\\)\$(?!\$)([^\$\n]+?)(?<!\\)\$")
    matches = list(inline_re.finditer(protected))
    for m in reversed(matches):
        idx = len(math_blocks)
        placeholder = _ph(idx)
        original = m.group(0)
        escaped = html.escape(original, quote=False)
        html_elem = f'<span class="math-inline">{escaped}</span>'
        math_blocks.append((placeholder, html_elem))
        protected = protected[: m.start()] + placeholder + protected[m.end() :]

    display_bracket_re = re.compile(r"^\\\[\s*\n(.*?)\n\s*\\\]\s*$", re.DOTALL | re.MULTILINE)
    matches = list(display_bracket_re.finditer(protected))
    for m in reversed(matches):
        idx = len(math_blocks)
        placeholder = _ph(idx)
        original = m.group(0)
        escaped = html.escape(original, quote=False)
        html_elem = f'<div class="math-display">{escaped}</div>'
        math_blocks.append((placeholder, html_elem))
        protected = protected[: m.start()] + placeholder + protected[m.end() :]

    inline_paren_re = re.compile(r"\\\((.+?)\\\)")
    matches = list(inline_paren_re.finditer(protected))
    for m in reversed(matches):
        idx = len(math_blocks)
        placeholder = _ph(idx)
        original = m.group(0)
        escaped = html.escape(original, quote=False)
        html_elem = f'<span class="math-inline">{escaped}</span>'
        math_blocks.append((placeholder, html_elem))
        protected = protected[: m.start()] + placeholder + protected[m.end() :]

    return protected, math_blocks


def _restore_math_expressions(html_content: str, math_blocks: list[tuple[str, str]]) -> str:
    for placeholder, html_elem in math_blocks:
        escaped_ph = html.escape(placeholder, quote=False)
        if html_elem.startswith("<div"):
            html_content = html_content.replace(f"<p>{placeholder}</p>", html_elem)
            html_content = html_content.replace(f"<p>{escaped_ph}</p>", html_elem)
        html_content = html_content.replace(placeholder, html_elem)
        html_content = html_content.replace(escaped_ph, html_elem)
    return html_content


# ==============================================================================
# Table Post-processing (wrapping + optional numeric classification + widths)
# ==============================================================================

def _get_text_display_length(text: str) -> float:
    """Approximate display width: wide characters (CJK, fullwidth, etc.) count as 1.8."""
    length = 0.0
    for char in text:
        cp = ord(char)
        if (
            0x4E00 <= cp <= 0x9FFF      # CJK Unified Ideographs
            or 0x3040 <= cp <= 0x309F    # Hiragana
            or 0x30A0 <= cp <= 0x30FF    # Katakana
            or 0xAC00 <= cp <= 0xD7AF    # Hangul Syllables
            or 0xFF00 <= cp <= 0xFFEF    # Fullwidth Forms
            or 0x3000 <= cp <= 0x303F    # CJK Symbols and Punctuation
            or 0x2E80 <= cp <= 0x2EFF    # CJK Radicals Supplement
            or 0xF900 <= cp <= 0xFAFF    # CJK Compatibility Ideographs
        ):
            length += 1.8
        else:
            length += 1.0
    return length


def _extract_cell_contents(table_html: str) -> tuple[int, list[list[str]]]:
    rows: list[list[str]] = []
    row_matches = re.findall(r"<tr[^>]*>(.*?)</tr>", table_html, re.DOTALL | re.IGNORECASE)

    for row_html in row_matches:
        cells: list[str] = []
        cell_matches = re.findall(r"<(?:th|td)[^>]*>(.*?)</(?:th|td)>", row_html, re.DOTALL | re.IGNORECASE)
        for cell_content in cell_matches:
            plain = re.sub(r"<[^>]+>", "", cell_content)
            plain = html.unescape(plain).strip()
            cells.append(plain)
        if cells:
            rows.append(cells)

    col_count = max((len(r) for r in rows), default=0)
    return col_count, rows


def _calculate_column_widths(col_count: int, rows: list[list[str]]) -> list[float]:
    if col_count == 0:
        return []

    effective: list[float] = []
    for c in range(col_count):
        lens: list[float] = []
        for r in rows:
            if c < len(r):
                t = r[c].strip()
                if t:
                    lens.append(_get_text_display_length(t))
        if lens:
            avg_len = sum(lens) / len(lens)
            max_len = max(lens)
            eff = avg_len * 0.7 + max_len * 0.3
        else:
            eff = 2.0
        effective.append(eff)

    total = sum(effective) or col_count
    raw = [(e / total) * 100 for e in effective]

    if col_count >= 5:
        min_w = 50 / col_count
        max_w = 250 / col_count
    else:
        min_w = 10
        max_w = 70

    clamped = [max(min_w, min(max_w, w)) for w in raw]
    s = sum(clamped)
    return [(w / s) * 100 for w in clamped] if s > 0 else [100 / col_count] * col_count


def _apply_column_widths_to_table(table_html: str, widths: list[float]) -> str:
    if not widths:
        return table_html
    col_elements = "".join(f'<col style="width:{w:.2f}%">' for w in widths)
    colgroup = f"<colgroup>{col_elements}</colgroup>"
    return re.sub(r"(<table[^>]*>)", r"\1" + colgroup, table_html, count=1, flags=re.IGNORECASE)


def _enhance_tables(html_content: str) -> str:
    def process_table(m: re.Match) -> str:
        table_html = m.group(0)
        col_count, rows = _extract_cell_contents(table_html)

        wrapper_open = '<div class="table-wrapper">'
        wrapper_close = "</div>"

        if col_count > 0:
            widths = _calculate_column_widths(col_count, rows)
            table_html2 = _apply_column_widths_to_table(table_html, widths)
            table_html2 = re.sub(
                r"<table([^>]*)>",
                rf'<table\1 data-cols="{col_count}">',
                table_html2,
                count=1,
                flags=re.IGNORECASE,
            )
        else:
            table_html2 = table_html

        return f"{wrapper_open}{table_html2}{wrapper_close}"

    return re.sub(r"<table[^>]*>.*?</table>", process_table, html_content, flags=re.DOTALL | re.IGNORECASE)


def _classify_numeric_cells(html_content: str) -> str:
    def classify(m: re.Match) -> str:
        tag = m.group(1)
        attrs = m.group(2) or ""
        content = m.group(3)

        if re.match(r"^[\s\-+$€¥£]?\(?[\d,]+(?:\.\d+)?\)?%?$", content.strip()):
            if 'class="' in attrs:
                attrs = re.sub(r'class="([^"]*)"', r'class="\1 numeric"', attrs)
            else:
                attrs = f'{attrs} class="numeric"'

        return f"<{tag}{attrs}>{content}</{tag}>"

    return re.sub(r"<(td|th)([^>]*)>([^<]*)</\1>", classify, html_content, flags=re.IGNORECASE)


# ==============================================================================
# JS Library Embedding (self-contained HTML — no external requests)
# ==============================================================================

_SCRIPT_DIR = Path(__file__).resolve().parent
_BUNDLED_JS_DIR = _SCRIPT_DIR / "vendor"
_BUNDLED_JS_FILES = {
    "mermaid.min.js": _BUNDLED_JS_DIR / "mermaid-11.14.0" / "mermaid.min.js",
    "tex-svg-full.js": _BUNDLED_JS_DIR / "mathjax-3.2.2" / "tex-svg-full.js",
}
# Embedded company logo so generated HTML stays self-contained even if repo assets are removed.
_COMPANY_LOGO_DATA_URL = (
    'data:image/webp;base64,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'
)

def _load_bundled_js(filename: str) -> str:
    """Return bundled JS content for inline embedding."""
    asset_path = _BUNDLED_JS_FILES[filename]
    if not asset_path.is_file():
        raise FileNotFoundError(
            f"Bundled JavaScript asset not found: {asset_path}. "
            "Reinstall or repackage the skill with scripts/vendor included."
        )
    return asset_path.read_text(encoding="utf-8")


def _safe_inline_js(js_content: str) -> str:
    r"""Escape sequences that would break an inline <script> block."""
    return (
        js_content
        .replace("</script>", r"<\/script>")
        .replace("</Script>", r"<\/Script>")
        # Vendored MathJax embeds legacy jsDelivr URL strings for optional SRE assets.
        # Neutralize them so generated HTML contains no third-party CDN references.
        .replace("https://cdn.jsdelivr.net/", "data:text/plain,")
    )


def _get_company_logo_data_url() -> str | None:
    """
    Return the company logo as a data URL.

    Priority:
      1) scripts/logo.png (hardcoded into HTML at generation time)
      2) built-in embedded fallback
    """
    candidate_paths = [
        _SCRIPT_DIR / "logo.png",
        _SCRIPT_DIR.parent / "logo.png",
    ]
    for logo_png in candidate_paths:
        if logo_png.exists() and logo_png.is_file():
            try:
                return _image_to_base64_data_url(logo_png)
            except Exception:
                continue
    return _COMPANY_LOGO_DATA_URL


# ==============================================================================
# Mermaid Block Protection / Restoration
# ==============================================================================

_MERMAID_FENCE_RE = re.compile(
    r"^(`{3,}|~{3,})\s*mermaid\s*\n(.*?)^\1\s*$",
    re.DOTALL | re.MULTILINE,
)


def _protect_mermaid_blocks(md: str) -> tuple[str, list[tuple[str, str]]]:
    """
    Extract ```mermaid ... ``` blocks, replace with PUA placeholders
    so they survive Markdown parsing intact.
    """
    blocks: list[tuple[str, str]] = []

    def _replace(m: re.Match) -> str:
        idx = len(blocks)
        ph = f"\uE000MERMAID{idx}\uE001"
        code = m.group(2).strip()
        blocks.append((ph, code))
        return ph

    protected = _MERMAID_FENCE_RE.sub(_replace, md)
    return protected, blocks


def _restore_mermaid_blocks(html_content: str, blocks: list[tuple[str, str]]) -> str:
    """Replace mermaid placeholders with <pre class="mermaid"> elements."""
    for ph, code in blocks:
        mermaid_html = (
            '<div class="mermaid-wrapper">'
            f'<pre class="mermaid">{html.escape(code)}</pre>'
            '</div>'
        )
        html_content = html_content.replace(f"<p>{ph}</p>", mermaid_html)
        html_content = html_content.replace(ph, mermaid_html)
        escaped_ph = html.escape(ph, quote=False)
        html_content = html_content.replace(f"<p>{escaped_ph}</p>", mermaid_html)
        html_content = html_content.replace(escaped_ph, mermaid_html)
    return html_content


# ==============================================================================
# Markdown → HTML Conversion (with Mermaid support)
# ==============================================================================

def _convert_markdown_to_html(raw_md: str) -> str:
    md = raw_md or ""
    md = _normalize_indentation(md)
    md = _convert_ocr_figure_placeholders(md)
    md = _ensure_blank_lines_around_tables(md)

    md, mermaid_blocks = _protect_mermaid_blocks(md)
    protected, math_blocks = _protect_math_expressions(md)

    processor = markdown2.Markdown(
        extras=[
            "fenced-code-blocks",
            "code-friendly",
            "cuddled-lists",
            "header-ids",
            "strike",
            "tables",
            "task_list",
        ]
    )

    html_content = processor.convert(protected)
    html_content = _restore_math_expressions(html_content, math_blocks)
    html_content = _restore_mermaid_blocks(html_content, mermaid_blocks)
    html_content = _enhance_tables(html_content)
    html_content = _classify_numeric_cells(html_content)
    return html_content


# ==============================================================================
# CSS / JS
# ==============================================================================

def _get_css_styles() -> str:
    return r''':root {
  --bg-primary: #eef3f7;
  --bg-secondary: #f7fbff;
  --surface: rgba(255, 255, 255, 0.72);
  --surface-strong: rgba(255, 255, 255, 0.88);
  --surface-soft: rgba(255, 255, 255, 0.58);
  --text: #0e1a26;
  --text-secondary: #314457;
  --muted: #536171;
  --brand-primary: #1e6ee8;
  --brand-secondary: #00c2b2;
  --brand-soft: rgba(30, 110, 232, 0.10);
  --brand-soft-2: rgba(0, 194, 178, 0.12);
  --border: rgba(14, 26, 38, 0.12);
  --border-strong: rgba(30, 110, 232, 0.18);
  --glass-stroke: rgba(255, 255, 255, 0.42);
  --shadow: 0 22px 48px rgba(8, 28, 61, 0.14);
  --shadow-soft: 0 10px 28px rgba(8, 28, 61, 0.10);
  --radius-xl: 22px;
  --radius-lg: 18px;
  --radius-md: 14px;
  --radius-sm: 10px;
  --maxw: 1680px;
  --header-maxw: 1160px;
  --code-bg: rgba(16, 33, 54, 0.05);
  --code-border: rgba(17, 54, 93, 0.12);
  --code-surface: linear-gradient(180deg, #1d2d43 0%, #142133 100%);
  --font-ui: "Avenir Next", "Segoe UI Variable", "IBM Plex Sans", "Helvetica Neue", Arial, sans-serif;
  --font-display: "Avenir Next", "Segoe UI Variable", "Trebuchet MS", sans-serif;
  --font-code: "JetBrains Mono", "SFMono-Regular", Menlo, Monaco, Consolas, monospace;
}

*, *::before, *::after { box-sizing: border-box; }

html, body {
  margin: 0;
  padding: 0;
  min-height: 100%;
}

body {
  font-family: var(--font-ui);
  font-size: 14px;
  line-height: 1.6;
  color: var(--text);
  background:
    radial-gradient(900px 560px at 8% 12%, rgba(0, 194, 178, 0.12), transparent 55%),
    radial-gradient(960px 620px at 88% -8%, rgba(30, 110, 232, 0.18), transparent 52%),
    linear-gradient(180deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
  background-attachment: fixed;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  overflow-x: hidden;
}

.blob {
  position: fixed;
  border-radius: 50%;
  filter: blur(88px);
  opacity: 0.58;
  pointer-events: none;
  z-index: 0;
}

.blob {
  width: 560px;
  height: 560px;
  right: -140px;
  top: -120px;
  background: linear-gradient(135deg, rgba(30, 110, 232, 0.30), rgba(0, 194, 178, 0.16));
  animation: float1 18s ease-in-out infinite;
}

.blob-2 {
  width: 520px;
  height: 520px;
  left: -120px;
  bottom: -180px;
  background: linear-gradient(135deg, rgba(0, 194, 178, 0.26), rgba(30, 110, 232, 0.16));
  animation: float2 22s ease-in-out infinite;
}

@keyframes float1 {
  0%, 100% { transform: translate(0, 0) scale(1); }
  50% { transform: translate(-18px, 22px) scale(1.05); }
}

@keyframes float2 {
  0%, 100% { transform: translate(0, 0) scale(1); }
  50% { transform: translate(22px, -16px) scale(0.96); }
}

@keyframes logoSheen {
  0% { transform: translateX(-120%) rotate(16deg); opacity: 0; }
  22% { opacity: 0.55; }
  100% { transform: translateX(320%) rotate(16deg); opacity: 0; }
}

.wrap {
  position: relative;
  z-index: 1;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

header {
  position: sticky;
  top: 0;
  z-index: 20;
  width: 100%;
  padding: 7px clamp(16px, 3vw, 30px);
  background: rgba(255, 255, 255, 0.44);
  border-bottom: 1px solid var(--glass-stroke);
  -webkit-backdrop-filter: blur(18px) saturate(180%);
  backdrop-filter: blur(18px) saturate(180%);
}

.header-content {
  max-width: var(--header-maxw);
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 0;
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  color: inherit;
  min-width: 0;
}

.logo {
  width: 222px;
  height: 76px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 18px;
  border-radius: 18px;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.97), rgba(244, 249, 255, 0.92));
  border: 1px solid rgba(255, 255, 255, 0.72);
  box-shadow: 0 14px 34px rgba(8, 28, 61, 0.11),
              0 1px 0 rgba(255, 255, 255, 0.82) inset;
  overflow: hidden;
  position: relative;
  transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1),
              box-shadow 0.2s cubic-bezier(0.4, 0.0, 0.2, 1);
}

.logo::before {
  content: "";
  position: absolute;
  inset: -40% auto -40% -70%;
  width: 48%;
  transform: rotate(16deg);
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.45), transparent);
  animation: logoSheen 2.8s ease-out 0.15s 1;
  pointer-events: none;
}

.logo:hover {
  transform: scale(1.03);
  box-shadow: 0 18px 42px rgba(8, 28, 61, 0.14),
              0 1px 0 rgba(255, 255, 255, 0.88) inset;
}

.logo img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: contain;
  object-position: center;
  transform: scale(1.08);
  transform-origin: center;
  opacity: 0;
  transition: opacity 0.56s ease, transform 0.72s cubic-bezier(0.22, 1, 0.36, 1);
}

.logo img.is-loaded {
  opacity: 1;
  transform: scale(1);
}

.logo.logo-error img {
  display: none;
}

.logo.logo-error::after {
  content: "";
  display: block;
  width: 84%;
  height: 18px;
  border-radius: 999px;
  background: linear-gradient(135deg, var(--brand-primary), var(--brand-secondary));
}

.logo-fallback {
  display: block;
  width: 100%;
  height: 22px;
  border-radius: 999px;
  background: linear-gradient(135deg, var(--brand-primary), var(--brand-secondary));
}

.brand-name {
  font-family: var(--font-display);
  font-size: clamp(20px, 2.4vw, 24px);
  font-weight: 700;
  line-height: 1.05;
  letter-spacing: 0.02em;
  background: linear-gradient(135deg, var(--brand-primary), var(--brand-secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.domain {
  margin-top: 4px;
  color: var(--muted);
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

.subtitle-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px 20px;
  border-radius: 9999px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.94), rgba(236, 246, 255, 0.92));
  box-shadow: 0 10px 24px rgba(8, 28, 61, 0.09);
  border: 1px solid rgba(30, 110, 232, 0.10);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  font-size: 12px;
  letter-spacing: 0.02em;
  transition: transform 0.2s ease;
}

.subtitle-badge:hover {
  transform: translateY(-1px);
  box-shadow: 0 12px 28px rgba(8, 28, 61, 0.12);
}

.subtitle-badge .text {
  font-family: "Avenir Next", "Segoe UI Variable", "IBM Plex Sans", "Helvetica Neue", Arial, sans-serif;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.045em;
  text-transform: none;
  color: #29506f;
  background: linear-gradient(135deg, #2c5f88 0%, #157d91 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

main {
  flex: 1;
  width: 100%;
  max-width: var(--maxw);
  margin: 0 auto;
  padding: 30px clamp(16px, 3vw, 32px) 44px;
}

.page-section {
  position: relative;
  margin-bottom: 24px;
  overflow: hidden;
  border-radius: var(--radius-xl);
  background: var(--surface);
  border: 1px solid var(--glass-stroke);
  box-shadow: var(--shadow);
  -webkit-backdrop-filter: blur(18px) saturate(160%);
  backdrop-filter: blur(18px) saturate(160%);
}

.page-section::before {
  content: "";
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at top right, rgba(0, 194, 178, 0.12), transparent 28%),
    radial-gradient(circle at bottom left, rgba(30, 110, 232, 0.08), transparent 32%);
  pointer-events: none;
}

.page-header {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 24px;
  background: linear-gradient(135deg, var(--brand-primary), var(--brand-secondary));
  color: white;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.09em;
  text-transform: uppercase;
  border-radius: 0 0 18px 18px;
  box-shadow: 0 4px 14px rgba(8, 28, 61, 0.11);
}

.page-indicator {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: white;
  box-shadow: 0 0 0 6px rgba(255, 255, 255, 0.18);
  flex: 0 0 auto;
}

.page-content {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: minmax(320px, 39%) minmax(0, 1fr);
  gap: 18px;
  padding: 18px;
  align-items: start;
}

.image-panel {
  position: sticky;
  top: 104px;
  align-self: start;
  overflow: hidden;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border);
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(244, 250, 255, 0.90));
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.72), var(--shadow-soft);
}

.image-panel img {
  display: block;
  width: 100%;
  height: auto;
  object-fit: contain;
  background: white;
}

.image-missing {
  padding: 20px;
  color: var(--muted);
  font-size: 13px;
}

.markdown-panel {
  min-height: 0;
  padding: 18px 20px;
  border-radius: var(--radius-lg);
  border: 1px solid rgba(14, 26, 38, 0.08);
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.94), rgba(248, 251, 255, 0.92));
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.84);
}

.markdown-content {
  color: var(--text);
  font-family: var(--font-ui);
  font-size: 14px;
  line-height: 1.72;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.markdown-content h1,
.markdown-content h2,
.markdown-content h3,
.markdown-content h4,
.markdown-content h5,
.markdown-content h6 {
  margin: 1.45em 0 0.6em;
  font-family: var(--font-display);
  line-height: 1.25;
  color: var(--text);
}

.markdown-content h1:first-child,
.markdown-content h2:first-child,
.markdown-content h3:first-child {
  margin-top: 0;
}

.markdown-content h1 {
  font-size: 1.9em;
  font-weight: 800;
  letter-spacing: -0.02em;
  padding-bottom: 0.28em;
  border-bottom: 1px solid rgba(30, 110, 232, 0.14);
}

.markdown-content h2 {
  font-size: 1.5em;
  font-weight: 700;
  padding-bottom: 0.24em;
  border-bottom: 1px solid rgba(14, 26, 38, 0.08);
}

.markdown-content h3 { font-size: 1.24em; font-weight: 700; }
.markdown-content h4 { font-size: 1.08em; font-weight: 700; }
.markdown-content h5 { font-size: 1em; font-weight: 700; }
.markdown-content h6 { font-size: 0.95em; color: var(--text-secondary); }

.markdown-content p { margin: 0 0 1em; }
.markdown-content p:last-child { margin-bottom: 0; }

.markdown-content a {
  color: var(--brand-primary);
  text-decoration: none;
  font-weight: 600;
}

.markdown-content a:hover { text-decoration: underline; }

.markdown-content strong { color: var(--text); font-weight: 700; }
.markdown-content em { font-style: italic; }

.markdown-content blockquote {
  margin: 1.15em 0;
  padding: 0.85em 1.1em;
  border-left: 4px solid var(--brand-primary);
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
  background: linear-gradient(135deg, rgba(30, 110, 232, 0.08), rgba(0, 194, 178, 0.08));
  color: var(--text-secondary);
}

.markdown-content blockquote p { margin: 0; }

.markdown-content ul,
.markdown-content ol {
  margin: 0.8em 0;
  padding-left: 1.75em;
}

.markdown-content li { margin: 0.3em 0; }
.markdown-content li > ul,
.markdown-content li > ol { margin: 0.3em 0; }

.markdown-content ul.task-list {
  list-style: none;
  padding-left: 0;
}

.markdown-content .task-list-item {
  display: flex;
  align-items: flex-start;
  gap: 0.5em;
}

.markdown-content .task-list-item input[type="checkbox"] {
  margin-top: 0.25em;
  accent-color: var(--brand-primary);
}

.markdown-content code {
  font-family: var(--font-code);
  font-size: 0.9em;
  padding: 0.18em 0.42em;
  color: #103760;
  background: rgba(30, 110, 232, 0.07);
  border: 1px solid rgba(30, 110, 232, 0.10);
  border-radius: 6px;
}

.markdown-content pre {
  margin: 1.15em 0;
  padding: 1.05em 1.25em;
  overflow-x: auto;
  border-radius: var(--radius-md);
  border: 1px solid rgba(17, 54, 93, 0.18);
  background: var(--code-surface);
  color: #dbe9f7;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.06);
  font-size: 13px;
  line-height: 1.55;
}

.markdown-content pre code {
  padding: 0;
  border: none;
  background: transparent;
  color: inherit;
  font-size: inherit;
  border-radius: 0;
}

.markdown-content hr {
  margin: 1.6em 0;
  border: none;
  border-top: 1px solid rgba(14, 26, 38, 0.10);
}

.markdown-content img {
  max-width: 100%;
  height: auto;
  border-radius: var(--radius-sm);
}

.markdown-content del {
  color: var(--muted);
  text-decoration: line-through;
}

.table-wrapper {
  margin: 1.15em 0;
  overflow-x: auto;
  border-radius: 16px;
  border: 1px solid rgba(30, 110, 232, 0.12);
  background: rgba(255, 255, 255, 0.92);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.80);
}

.markdown-content table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
  font-size: 13px;
  line-height: 1.5;
}

.markdown-content thead {
  background: linear-gradient(135deg, rgba(30, 110, 232, 0.11), rgba(0, 194, 178, 0.10));
}

.markdown-content th,
.markdown-content td {
  padding: 9px 14px;
  text-align: left;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.markdown-content th {
  color: var(--text);
  font-weight: 700;
  border-bottom: 1px solid rgba(30, 110, 232, 0.14);
  border-right: 1px solid rgba(14, 26, 38, 0.08);
}

.markdown-content td {
  color: var(--text);
  border-bottom: 1px solid rgba(14, 26, 38, 0.07);
  border-right: 1px solid rgba(14, 26, 38, 0.05);
  vertical-align: top;
}

.markdown-content th:last-child,
.markdown-content td:last-child { border-right: none; }

.markdown-content tbody tr:last-child td { border-bottom: none; }

.markdown-content tbody tr:nth-child(even) {
  background: rgba(30, 110, 232, 0.025);
}

.markdown-content tbody tr:hover {
  background: rgba(0, 194, 178, 0.06);
}

.markdown-content .numeric {
  font-family: var(--font-code);
  font-variant-numeric: tabular-nums;
}

.math-inline {
  display: inline-block;
  max-width: 100%;
  vertical-align: middle;
  padding: 0 2px;
  font-family: "Times New Roman", serif;
}

.math-display {
  display: block;
  margin: 1.25em 0;
  padding: 1em;
  text-align: center;
  overflow-x: auto;
  border-radius: var(--radius-md);
  border: 1px solid rgba(30, 110, 232, 0.12);
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.94), rgba(241, 249, 255, 0.92));
}

mjx-container { display: inline-block !important; margin: 0 !important; }
mjx-container[display="true"] { display: block !important; margin: 1em 0 !important; }

.mermaid-wrapper {
  margin: 1.4em 0;
  padding: 1.15em;
  overflow-x: auto;
  text-align: center;
  border-radius: 18px;
  border: 1px solid rgba(30, 110, 232, 0.14);
  background:
    radial-gradient(circle at top right, rgba(0, 194, 178, 0.10), transparent 30%),
    linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(240, 248, 255, 0.92));
  box-shadow: var(--shadow-soft);
}

.mermaid-wrapper pre.mermaid {
  margin: 0;
  padding: 0;
  background: transparent;
  border: none;
  color: var(--text);
  text-align: center;
  overflow: visible;
  font-size: 14px;
  line-height: 1.6;
}

.mermaid-wrapper pre.mermaid-rendered {
  padding: 14px 16px;
  overflow-x: auto;
  border-radius: 14px;
  border: 1px solid rgba(14, 26, 38, 0.08);
  background: rgba(255, 255, 255, 0.88);
}

.mermaid-wrapper svg {
  max-width: 100%;
  height: auto;
}

.mermaid-fallback {
  margin: 1em 0;
  overflow: hidden;
  border-radius: 14px;
  border: 1px solid rgba(30, 110, 232, 0.16);
}

.mermaid-fallback-label {
  padding: 7px 12px;
  color: white;
  font-size: 11px;
  font-family: var(--font-code);
  letter-spacing: 0.08em;
  text-transform: uppercase;
  background: linear-gradient(135deg, var(--brand-primary), var(--brand-secondary));
}

.mermaid-fallback pre {
  margin: 0;
  padding: 1em 1.2em;
  overflow-x: auto;
  font-size: 13px;
  line-height: 1.5;
  color: #15304b;
  background: rgba(255, 255, 255, 0.94);
  border-top: 1px solid rgba(30, 110, 232, 0.10);
}

.mermaid-fallback pre code {
  padding: 0;
  border: none;
  background: transparent;
  color: inherit;
  font-size: inherit;
  border-radius: 0;
  font-family: var(--font-code);
}

footer {
  margin-top: auto;
  padding: 0 clamp(16px, 3vw, 32px) 34px;
  color: var(--muted);
}

.foot {
  max-width: var(--maxw);
  margin: 0 auto;
  padding-top: 18px;
  text-align: center;
  font-size: 13px;
  border-top: 1px solid rgba(14, 26, 38, 0.08);
}

.foot-copy { color: var(--muted); }
.foot-copy strong { color: var(--text); }

.loading {
  padding: 3em;
  text-align: center;
  color: var(--muted);
  font-size: 14px;
}

@media (max-width: 1360px) {
  .page-content {
    grid-template-columns: minmax(280px, 38%) minmax(0, 1fr);
  }
}

@media (max-width: 1024px) {
  header {
    position: relative;
    top: auto;
  }

  .header-content {
    justify-content: center;
  }

  .page-content {
    grid-template-columns: 1fr;
  }

  .image-panel {
    position: static;
    top: auto;
    max-width: 860px;
    margin: 0 auto;
  }
}

@media (max-width: 768px) {
  header {
    padding: 12px 16px;
  }

  .brand {
    width: 100%;
    justify-content: center;
    flex-wrap: wrap;
    text-align: center;
  }

  .logo {
    width: 166px;
    height: 68px;
  }

  .subtitle-badge {
    width: 100%;
    margin-top: 8px;
  }

  .page-content {
    padding: 16px;
    gap: 16px;
  }

  .markdown-panel {
    padding: 16px;
  }

  .markdown-content {
    font-size: 13px;
  }

  .markdown-content table {
    font-size: 11px;
  }

  .markdown-content th,
  .markdown-content td {
    padding: 7px 10px;
  }
}

@media print {
  .blob, .blob-2 { display: none; }
  body { background: white; }
  header {
    position: static;
    background: white;
    border-bottom: 1px solid #ddd;
    -webkit-backdrop-filter: none;
    backdrop-filter: none;
  }
  .page-section {
    box-shadow: none;
    border: 1px solid #d8e1ea;
    background: white;
    page-break-inside: avoid;
  }
  .page-content { grid-template-columns: 1fr; }
  .image-panel {
    position: static;
    max-height: 400px;
    box-shadow: none;
  }
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}

@supports not ((-webkit-backdrop-filter: blur(10px)) or (backdrop-filter: blur(10px))) {
  header,
  .page-section {
    background: rgba(255, 255, 255, 0.94);
  }
}'''


def _get_mathjax_config() -> str:
    return r'''window.MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]']],
    processEscapes: true,
    processEnvironments: true,
    tags: 'ams',
    packages: {'[+]': ['ams', 'newcommand', 'configmacros']}
  },
  options: {
    skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code'],
    ignoreHtmlClass: 'tex2jax_ignore',
    processHtmlClass: 'tex2jax_process'
  },
  svg: {
    fontCache: 'global',
    scale: 1,
    displayAlign: 'center'
  },
  startup: {
    pageReady: () => MathJax.startup.defaultPageReady()
  }
};'''


def _get_page_scripts() -> str:
    return r'''document.getElementById('year').textContent = new Date().getFullYear();

document.addEventListener('DOMContentLoaded', function() {
  if (window.MathJax && window.MathJax.typesetPromise) {
    window.MathJax.typesetPromise().catch(function(err) {
      console.warn('MathJax typeset error:', err);
    });
  }
});

(function() {
  var prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  function toggleMotion(disable) {
    document.querySelectorAll('.blob, .blob-2').forEach(function(el) {
      el.style.animationPlayState = disable ? 'paused' : 'running';
    });
  }
  toggleMotion(prefersReduced.matches);
  prefersReduced.addEventListener('change', function(e) {
    toggleMotion(e.matches);
  });
})();

document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.logo').forEach(function(container) {
    var img = container.querySelector('img');
    if (!img) return;

    function markLoaded() {
      img.classList.add('is-loaded');
    }
    function markError() {
      container.classList.add('logo-error');
    }

    if (img.complete) {
      if (img.naturalWidth > 0) markLoaded();
      else markError();
    } else {
      img.addEventListener('load', markLoaded, { once: true });
      img.addEventListener('error', markError, { once: true });
    }
  });
});'''


_MERMAID_INIT_JS = r"""mermaid.initialize({
  startOnLoad: false,
  theme: 'base',
  securityLevel: 'loose',
  themeVariables: {
    background: '#f7fbff',
    primaryColor: '#ffffff',
    primaryBorderColor: '#1e6ee8',
    primaryTextColor: '#0e1a26',
    secondaryColor: '#eefaf8',
    secondaryBorderColor: '#00c2b2',
    secondaryTextColor: '#0e1a26',
    tertiaryColor: '#eef4ff',
    tertiaryBorderColor: '#7aa8f4',
    tertiaryTextColor: '#0e1a26',
    lineColor: '#2563c9',
    clusterBkg: '#f4faff',
    clusterBorder: '#93b9f4',
    defaultLinkColor: '#2563c9',
    edgeLabelBackground: '#ffffff',
    nodeTextColor: '#0e1a26',
    mainBkg: '#ffffff',
    noteBkgColor: '#eefaf8',
    noteBorderColor: '#00a99b',
    fontFamily: '"Avenir Next", "Segoe UI Variable", "IBM Plex Sans", "Helvetica Neue", Arial, sans-serif',
    fontSize: '15px'
  },
  flowchart: {
    useMaxWidth: true,
    htmlLabels: true,
    curve: 'basis',
    padding: 18,
    nodeSpacing: 34,
    rankSpacing: 44
  },
  fontFamily: '"Avenir Next", "Segoe UI Variable", "IBM Plex Sans", "Helvetica Neue", Arial, sans-serif'
});

function _mermaidEscHtml(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function _mermaidFallback(el) {
  var source = el.textContent;
  var wrapper = el.closest('.mermaid-wrapper');
  var container = wrapper || el;
  var fb = document.createElement('div');
  fb.className = 'mermaid-fallback';
  fb.innerHTML = '<div class="mermaid-fallback-label">mermaid</div>' +
    '<pre><code>' + _mermaidEscHtml(source) + '</code></pre>';
  container.parentNode.replaceChild(fb, container);
}

document.addEventListener('DOMContentLoaded', async function() {
  var elements = document.querySelectorAll('pre.mermaid');
  if (!elements.length) return;

  if (typeof mermaid === 'undefined' || typeof mermaid.render !== 'function') {
    console.warn('mermaid.js not available — displaying raw source');
    elements.forEach(function(el) { _mermaidFallback(el); });
    return;
  }

  for (var i = 0; i < elements.length; i++) {
    var el = elements[i];
    var source = el.textContent;
    var id = 'mmd-' + i;
    try {
      var result = await mermaid.render(id, source);
      el.innerHTML = result.svg;
      el.classList.remove('mermaid');
      el.classList.add('mermaid-rendered');
    } catch (err) {
      console.warn('Mermaid render failed for block ' + i + ':', err.message || err);
      _mermaidFallback(el);
      var orphan = document.getElementById('d' + id);
      if (orphan) orphan.remove();
    }
  }
});"""


# ==============================================================================
# HTML Page Section Generation
# ==============================================================================

def _generate_page_section(
    base: str,
    page_num_str: str,
    img_data_url: str | None,
    html_content: str,
) -> str:
    label = f"{base} — Page {page_num_str}"
    if img_data_url:
        img_html = f'''<img src="{_escape_attr(img_data_url)}"
           alt="{_escape_attr(label)} source image"
           loading="lazy"
           decoding="async" />'''
    else:
        img_html = f'''<div class="image-missing">Missing image for <strong>{_escape_text(label)}</strong></div>'''

    return f'''<section class="page-section" data-base="{_escape_attr(base)}" data-page="{_escape_attr(page_num_str)}" aria-labelledby="page-label-{_escape_attr(base)}-{_escape_attr(page_num_str)}">
  <div class="page-header" id="page-label-{_escape_attr(base)}-{_escape_attr(page_num_str)}">
    <span class="page-indicator" aria-hidden="true"></span>
    <span>{_escape_text(label)}</span>
  </div>
  <div class="page-content">
    <div class="image-panel">
      {img_html}
    </div>
    <div class="markdown-panel">
      <div class="markdown-content tex2jax_process">
        {html_content}
      </div>
    </div>
  </div>
</section>'''


# ==============================================================================
# Full HTML Document Generation (self-contained output)
# ==============================================================================

def _generate_html_document(page_sections: list[str], title: str) -> str:
    css = _get_css_styles()
    mathjax_config = _get_mathjax_config()
    scripts = _get_page_scripts()
    # The company logo is embedded in this script so HTML output stays standalone.
    logo_data_url = _get_company_logo_data_url()

    sections_html = (
        "\n".join(page_sections)
        if page_sections
        else '<div class="loading">No pages found</div>'
    )

    mathjax_js = _load_bundled_js("tex-svg-full.js")
    mermaid_js = _load_bundled_js("mermaid.min.js")
    mathjax_tag = f"<script>{_safe_inline_js(mathjax_js)}</script>"
    mermaid_tag = f"<script>{_safe_inline_js(mermaid_js)}</script>"

    if logo_data_url:
        logo_html = (
            f'<img src="{_escape_attr(logo_data_url)}" alt="RizMoon company logo" '
            'loading="eager" decoding="async">'
        )
    else:
        logo_html = '<span class="logo-fallback" aria-hidden="true"></span>'

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{_escape_text(title)}</title>
  <meta name="description" content="OCR Extraction Comparison Report - RizMoon">
  <meta name="color-scheme" content="light">
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Ccircle cx='32' cy='32' r='28' fill='%231e6ee8'/%3E%3Ccircle cx='32' cy='32' r='18' fill='%2300c2b2'/%3E%3C/svg%3E">
  <style>
{css}
  </style>
  <script>
{mathjax_config}
  </script>
  {mathjax_tag}
  {mermaid_tag}
  <script>
{_MERMAID_INIT_JS}
  </script>
</head>
<body>
  <div class="blob"></div>
  <div class="blob blob-2"></div>

  <div class="wrap">
    <header aria-label="Report header">
      <div class="header-content">
        <a class="brand" href="https://www.rizmoon.ai" rel="noopener">
          <div class="logo">
            {logo_html}
          </div>
        </a>
        <div class="subtitle-badge">
          <span class="text">{_escape_text(title)}</span>
        </div>
      </div>
    </header>

    <main role="main">
      {sections_html}
    </main>

    <footer>
      <div class="foot">
        <div class="foot-copy">
          &copy; <span id="year">Extracted by</span> <strong>RizMoon</strong>.
          contact@rizmoon.com.
        </div>
      </div>
    </footer>
  </div>

  <script>
{scripts}
  </script>
</body>
</html>'''


# ==============================================================================
# Main Entry Point
# ==============================================================================

def markdown_to_html(
    image_dir: str | Path,
    markdown_dir: str | Path,
    output_html: str | Path,
) -> None:
    """
    Build an HTML report with side-by-side source images and rendered OCR
    markdown.  Mermaid fenced code blocks are rendered as SVG diagrams.

    Args:
        image_dir:    folder containing scanned page images
        markdown_dir: folder containing OCR-extracted Markdown files
        output_html:  output HTML file path
    """
    img_dir = Path(image_dir)
    md_dir = Path(markdown_dir)
    out_path = Path(output_html)

    if not img_dir.is_dir():
        raise NotADirectoryError(f"Image directory not found: {img_dir}")
    if not md_dir.is_dir():
        raise NotADirectoryError(f"Markdown directory not found: {md_dir}")

    out_path.parent.mkdir(parents=True, exist_ok=True)

    title = f"AI Extracted Content — {out_path.stem}"

    img_map = _scan_pages_by_base_and_num(img_dir, _IMG_EXTS)
    md_map = _scan_pages_by_base_and_num(md_dir, _MD_EXTS)

    keys = _sorted_keys(list(set(img_map.keys()) | set(md_map.keys())))

    if not keys:
        print(f"Warning: No matching pages found in {img_dir} and {md_dir}")
        return

    page_sections: list[str] = []
    for base, num in keys:
        img_path = img_map.get((base, num))
        md_path = md_map.get((base, num))

        img_data_url: str | None = None
        if img_path and img_path.exists():
            img_data_url = _image_to_base64_data_url(img_path)

        if md_path and md_path.exists():
            raw_md = md_path.read_text(encoding="utf-8-sig", errors="replace")
            raw_md = re.sub(r"\nPage Number \d+:\n", "\n", raw_md, flags=re.IGNORECASE)
            rendered = _convert_markdown_to_html(raw_md)
            html_content = (
                rendered
                if rendered.strip()
                else '<div class="loading">Empty extracted content</div>'
            )
        else:
            html_content = '<div class="loading">Missing markdown for this page</div>'

        page_sections.append(
            _generate_page_section(base, num, img_data_url, html_content)
        )

    final_html = _generate_html_document(page_sections, title)
    out_path.write_text(final_html, encoding="utf-8")
    print(f"Report generated: {len(keys)} pages -> {out_path}")


# ==============================================================================
# CLI Entry Point
# ==============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Generate a side-by-side HTML report comparing scanned page "
            "images with OCR-extracted Markdown.  Mermaid diagram blocks "
            "are rendered as interactive SVG graphs."
        ),
    )
    parser.add_argument("image_dir", help="Directory of source page images")
    parser.add_argument("markdown_dir", help="Directory of OCR-extracted Markdown files")
    parser.add_argument("output_html", help="Output HTML file path")
    args = parser.parse_args()

    markdown_to_html(args.image_dir, args.markdown_dir, args.output_html)
