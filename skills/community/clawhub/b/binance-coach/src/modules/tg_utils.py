"""
tg_utils.py — Telegram HTML formatting helpers

Telegram supports a safe subset of HTML:
  <b>bold</b>  <i>italic</i>  <u>underline</u>  <s>strikethrough</s>
  <code>inline code</code>  <pre>code block</pre>
  <a href="url">link</a>  <tg-spoiler>spoiler</tg-spoiler>

Use parse_mode="HTML" everywhere.
DO NOT use Markdown or MarkdownV2 (too many escape requirements).

Usage:
    from modules.tg_utils import e, bold, italic, code, pre, md_to_html, split_html

    msg = bold("Portfolio Health") + ": " + code(f"${value:.2f}")
    await update.message.reply_text(msg, parse_mode="HTML")
"""

import re


# ── Low-level escaping ────────────────────────────────────────────────────────

def e(text) -> str:
    """Escape HTML special chars. Always call this on dynamic user/API data."""
    text = str(text)
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ── Formatting helpers ────────────────────────────────────────────────────────

def bold(text) -> str:
    return f"<b>{e(text)}</b>"

def italic(text) -> str:
    return f"<i>{e(text)}</i>"

def code(text) -> str:
    return f"<code>{e(text)}</code>"

def pre(text, lang: str = "") -> str:
    if lang:
        return f'<pre><code class="language-{lang}">{e(text)}</code></pre>'
    return f"<pre>{e(text)}</pre>"

def link(text, url: str) -> str:
    return f'<a href="{url}">{e(text)}</a>'

def spoiler(text) -> str:
    return f"<tg-spoiler>{e(text)}</tg-spoiler>"


# ── Markdown → Telegram HTML converter (for Claude output) ────────────────────

def md_to_html(text: str) -> str:
    """
    Convert Claude's Markdown output to Telegram-compatible HTML.

    Handles:
    - ```lang\\n...\\n```  → <pre><code>...</code></pre>
    - `inline code`        → <code>...</code>
    - **bold** / *bold*    → <b>...</b>
    - _italic_ / __italic__→ <i>...</i>
    - ### Heading          → <b>Heading</b>
    - - bullet / * bullet  → • bullet
    - 1. list              → 1. list (kept as-is)
    - ---                  → ──────
    - Escapes & < > outside tags
    """
    if not text:
        return ""

    lines = text.split("\n")
    out_lines = []
    in_code_block = False
    code_lang = ""
    code_lines: list[str] = []

    for line in lines:
        # ── Code fence open/close ────────────────────────────────────────
        fence = re.match(r"^```(\w*)\s*$", line)
        if fence:
            if not in_code_block:
                in_code_block = True
                code_lang = fence.group(1) or ""
                code_lines = []
            else:
                in_code_block = False
                block_content = "\n".join(code_lines)
                out_lines.append(pre(block_content, code_lang))
                code_lang = ""
                code_lines = []
            continue

        if in_code_block:
            code_lines.append(line)
            continue

        # ── Horizontal rule ───────────────────────────────────────────────
        if re.match(r"^-{3,}$|^={3,}$", line.strip()):
            out_lines.append("──────────────────────")
            continue

        # ── Headings ──────────────────────────────────────────────────────
        heading = re.match(r"^(#{1,3})\s+(.*)", line)
        if heading:
            level, content = heading.group(1), heading.group(2)
            processed = _inline_md(content)
            prefix = "┃ " if len(level) == 1 else ""
            out_lines.append(f"{prefix}<b>{processed}</b>")
            continue

        # ── Bullet list ───────────────────────────────────────────────────
        bullet = re.match(r"^[\-\*]\s+(.*)", line)
        if bullet:
            out_lines.append(f"• {_inline_md(bullet.group(1))}")
            continue

        # ── Numbered list ─────────────────────────────────────────────────
        numbered = re.match(r"^(\d+)\.\s+(.*)", line)
        if numbered:
            out_lines.append(f"{numbered.group(1)}. {_inline_md(numbered.group(2))}")
            continue

        # ── Blockquote ────────────────────────────────────────────────────
        blockquote = re.match(r"^>\s+(.*)", line)
        if blockquote:
            out_lines.append(f"<i>💬 {_inline_md(blockquote.group(1))}</i>")
            continue

        # ── Normal line ───────────────────────────────────────────────────
        out_lines.append(_inline_md(line))

    # Close unclosed code block
    if in_code_block and code_lines:
        out_lines.append(pre("\n".join(code_lines), code_lang))

    return "\n".join(out_lines)


def _inline_md(text: str) -> str:
    """
    Process inline Markdown within a line.
    Order matters: code first (so bold/italic inside code isn't converted).
    """
    # Extract inline code spans first to protect them
    parts: list[tuple[bool, str]] = []  # (is_code, text)
    remaining = text
    while remaining:
        m = re.search(r"`([^`]+)`", remaining)
        if m:
            # Part before code
            if m.start() > 0:
                parts.append((False, remaining[:m.start()]))
            parts.append((True, m.group(1)))
            remaining = remaining[m.end():]
        else:
            parts.append((False, remaining))
            break

    result = ""
    for is_code, chunk in parts:
        if is_code:
            result += f"<code>{e(chunk)}</code>"
        else:
            # Escape HTML chars first
            chunk = e(chunk)
            # Bold: **text** or __text__
            chunk = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", chunk)
            chunk = re.sub(r"__(.+?)__", r"<b>\1</b>", chunk)
            # Italic: *text* or _text_ (but not mid-word underscores)
            chunk = re.sub(r"(?<!\w)\*(.+?)\*(?!\w)", r"<i>\1</i>", chunk)
            chunk = re.sub(r"(?<!\w)_(.+?)_(?!\w)", r"<i>\1</i>", chunk)
            # Strikethrough: ~~text~~
            chunk = re.sub(r"~~(.+?)~~", r"<s>\1</s>", chunk)
            result += chunk

    return result


# ── Message splitter ──────────────────────────────────────────────────────────

def split_html(text: str, limit: int = 4096) -> list[str]:
    """
    Split a Telegram HTML message into chunks ≤ limit chars.
    Splits on paragraph breaks first, then lines, avoids cutting mid-tag.
    """
    if len(text) <= limit:
        return [text]

    chunks = []
    current = ""

    for paragraph in text.split("\n\n"):
        candidate = current + ("\n\n" if current else "") + paragraph
        if len(candidate) <= limit:
            current = candidate
        else:
            if current:
                chunks.append(current)
            # Paragraph itself too long? Split by lines
            if len(paragraph) > limit:
                for line in paragraph.split("\n"):
                    candidate = current + ("\n" if current else "") + line
                    if len(candidate) <= limit:
                        current = candidate
                    else:
                        if current:
                            chunks.append(current)
                        current = line
            else:
                current = paragraph

    if current:
        chunks.append(current)

    return chunks or [text[:limit]]
