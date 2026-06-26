"""
normalize.py — Text normalization for context-hawk

Applies the same 28-rule normalization pipeline as hawk-bridge's TypeScript layer.
This ensures standalone Python users (without hawk-bridge) also get full cleanup.
"""

import json
import re

# ─── Pre-compiled patterns ────────────────────────────────────────────────────

# 1. Invisible / zero-width / control characters
INVISIBLE_RE = re.compile(
    r'[\x00-\x1f\x7f-\x9f\u200b-\u200f\u2028-\u202f\ufeff]'
)

# 4. Markdown images: ![alt](url)
IMG_RE = re.compile(r'!\[([^\]]*)\]\([^)]+\)')

# 5. Markdown links: [text](url) → text
LINK_RE = re.compile(r'\[([^\]]+)\]\([^)]+\)')

# 6. Bold/italic/underline markers
BOLD_ITALIC_RE = re.compile(r'[*_]{1,3}([^*_]+)[*_]{1,3}')

# 7. Markdown headers
HEADER_RE = re.compile(r'^#{1,6}\s+', re.MULTILINE)

# 8. Markdown code fences — keep content
CODE_FENCE_RE = re.compile(r'```[\w]*\n([\s\S]*?)```')

# 9. Inline code markers
INLINE_CODE_RE = re.compile(r'`([^`]+)`')

# 10. Blockquote markers
BLOCKQUOTE_RE = re.compile(r'^>\s+', re.MULTILINE)

# 11. List markers
LIST_RE = re.compile(r'^[\s]*[-*+]\s+', re.MULTILINE)
LIST_NUM_RE = re.compile(r'^[\s]*\d+\.\s+', re.MULTILINE)

# 12. Debug log statements
LOG_RE = re.compile(r'\bconsole\s*\.\s*(log|debug|info|warn|error)\s*\([^)]*\)', re.IGNORECASE)
PRINT_RE = re.compile(r'\bprint\s*\([^)]*\)')
LOGGER_RE = re.compile(r'\blogger\s*\.\s*(debug|info|warn|error)\s*\([^)]*\)', re.IGNORECASE)

# 13. Stack traces — keep first + last frame
STACK_RE = re.compile(
    r'(^\tat [^\n]+\n)((\tat [^\n]+\n)*)(\tat [^\n]+$)',
    re.MULTILINE
)

# 14. Broken URLs merged across lines
BROKEN_URL_RE = re.compile(r'(https?://[^\s\n,，]+)[\n-]([^\s,，]+)')

# 15. Over-long URLs — keep domain + first 60 path chars
LONG_URL_RE = re.compile(r'(https?://[^\s\'"<>]+)/([^\s\'"<>]{0,60}[^\s\'"<>]*)')

# 16. Emoji — use explicit unicode escapes or compile separately
def _make_emoji_re():
    ranges = [
        (0x1F300, 0x1F9FF),
        (0x2600, 0x26FF),
        (0x2700, 0x27BF),
        (0x1F600, 0x1F64F),
        (0x1F680, 0x1F6FF),
        (0x1F1E0, 0x1F1FF),
        (0x2300, 0x23FF),
        (0x2B50, 0x2B50),
        (0x1FA00, 0x1FAFF),
        (0x1F900, 0x1F9FF),
    ]
    parts = []
    for start, end in ranges:
        if start == end:
            parts.append(r'\U%08x' % start)
        else:
            parts.append(r'[\U%08x-\U%08x]' % (start, end))
    return re.compile(''.join(parts))

EMOJI_RE = _make_emoji_re()

# 17. Chinese → English punctuation
CN_PUNCT_MAP = {
    '\u3002': '.',   # 。
    '\uff0c': ',',   # ，
    '\uff1b': ';',   # ；
    '\uff1a': ':',   # ：
    '\uff1f': '?',   # ？
    '\uff01': '!',   # ！
    '\u201c': '"',   # "
    '\u201d': '"',   # "
    '\u2018': "'",   # '
    '\u2019': "'",   # '
    '\uff08': '(',   # （
    '\uff09': ')',   # ）
    '\u3010': '[',   # 【
    '\u3011': ']',   # 】
    '\u300a': '<',   # 《
    '\u300b': '>',   # 》
    '\u3001': ',',   # 、
    '\u2026': '...', # …
    '\uff5e': '~',   # ～
}

# 18. Timestamps → [时间]
TIMESTAMP_RE = re.compile(
    r'\b(?:\d{4}[-/年]\d{1,2}[-/月]\d{1,2}[日]?\s*'
    r'(?:[时分]?\s*\d{1,2}[：:]\d{1,2}(?:[：:]\d{1,2})?\s*(?:AM|PM|am|pm)?)?|'
    r'\d{1,2}[-/月]\d{1,2}[日]?(?:\s*\d{1,2}:\d{2}(?::\d{2})?)?)\b'
)

# 19. Multiple spaces
SPACE_RE = re.compile(r'[ \t]{2,}')

# 23. Large number simplification
LARGE_NUM_RE = re.compile(r'\b(\d{1,3}(?:,\d{3}){2,})(?:\b|[^\d])')

# 24. Over-long base64
BASE64_RE = re.compile(r'\b[A-Za-z0-9+/]{100,}={0,2}\b')

# 25. JSON compression
JSON_RE = re.compile(r'\{[^{}]*"[^"]+"\s*:\s*"[^"]+"[^{}]*\}')

# 28. CJK-English spacing
CJK_EN_PRE = re.compile(r'([\u4e00-\u9fff])([A-Za-z])')
CJK_EN_POST = re.compile(r'([A-Za-z])([\u4e00-\u9fff])')


def normalize(text: str) -> str:
    """Full normalization pipeline — mirrors hawk-bridge TypeScript normalizeText()."""
    t = text

    # 1. Remove invisible / zero-width chars
    t = INVISIBLE_RE.sub('', t)

    # 2. Normalize line endings
    t = t.replace('\r\n', '\n').replace('\r', '\n')

    # 3. Remove HTML/XML tags
    t = re.sub(r'<[^>]+>', '', t)

    # 4. Markdown images → [图片]
    t = IMG_RE.sub('[图片]', t)

    # 5. Markdown links (keep text)
    t = LINK_RE.sub(r'\1', t)

    # 6. Remove bold/italic/underline markers
    t = BOLD_ITALIC_RE.sub(r'\1', t)

    # 7. Remove Markdown headers
    t = HEADER_RE.sub('', t)

    # 8. Code fences — keep content
    t = CODE_FENCE_RE.sub(lambda m: m.group(1).strip(), t)

    # 9. Inline code markers
    t = INLINE_CODE_RE.sub(r'\1', t)

    # 10. Blockquotes
    t = BLOCKQUOTE_RE.sub('', t)

    # 11. List markers
    t = LIST_RE.sub('', t)
    t = LIST_NUM_RE.sub('', t)

    # 12. Debug logs → [日志]
    t = LOG_RE.sub('[日志]', t)
    t = PRINT_RE.sub('[日志]', t)
    t = LOGGER_RE.sub('[日志]', t)

    # 13. Stack traces — keep first + last frame
    def collapse_stack(m):
        head = m.group(1)
        middle = m.group(2)
        tail = m.group(3)
        return head + ('...\n' if middle else '') + tail
    t = STACK_RE.sub(collapse_stack, t)

    # 14. Merge broken URLs
    t = BROKEN_URL_RE.sub(r'\1\2', t)

    # 15. Compress over-long URLs
    def trunc_url(m):
        domain, path = m.group(1), m.group(2)
        path = path[:60] + ('...' if len(path) > 60 else '')
        return domain + '/' + path
    t = LONG_URL_RE.sub(trunc_url, t)

    # 16. Remove Emoji
    t = EMOJI_RE.sub('', t)

    # 17. Chinese → English punctuation (must be BEFORE sentence split)
    for cn, en in CN_PUNCT_MAP.items():
        t = t.replace(cn, en)

    # 18. Timestamps → [时间]
    t = TIMESTAMP_RE.sub('[时间]', t)

    # 19. Collapse multiple spaces
    t = SPACE_RE.sub(' ', t)

    # 20. Collapse multiple newlines to max 2
    t = re.sub(r'\n{3,}', '\n\n', t)

    # 21. Trim each line
    t = '\n'.join(line.strip() for line in t.split('\n'))

    # 22. Remove blank lines at start/end
    t = t.strip()

    # 23. Simplify large numbers
    def fmt_num(m):
        num_str = m.group(1).replace(',', '')
        num = int(num_str)
        if num >= 1_000_000_000:
            return f'{num / 1_000_000_000:.1f}B'
        if num >= 1_000_000:
            return f'{num / 1_000_000:.1f}M'
        if num >= 1_000:
            return f'{num / 1_000:.1f}K'
        return m.group(0)
    t = LARGE_NUM_RE.sub(fmt_num, t)

    # 24. Over-long base64 → [BASE64数据]
    t = BASE64_RE.sub('[BASE64数据]', t)

    # 25. Compress JSON
    def compress_json(m):
        try:
            return json.dumps(json.loads(m.group(0)))
        except Exception:
            return m.group(0)
    t = JSON_RE.sub(compress_json, t)

    # 26. Remove exact duplicate sentences
    sentences = re.split(r'(?<=[.!?])\s+', t)
    seen_sent = set()
    filtered_sents = []
    for s in sentences:
        norm = s.lower().strip()
        if norm and norm not in seen_sent:
            seen_sent.add(norm)
            filtered_sents.append(s)
    t = ' '.join(filtered_sents)

    # 27. Remove exact duplicate paragraphs
    paras = re.split(r'\n\n+', t)
    seen_para = set()
    filtered_paras = []
    for p in paras:
        norm = p.strip().lower()
        if norm and norm not in seen_para:
            seen_para.add(norm)
            filtered_paras.append(p)
    t = '\n\n'.join(filtered_paras)

    # 28. Minimize CJK-English spacing
    t = CJK_EN_PRE.sub(r'\1\2', t)
    t = CJK_EN_POST.sub(r'\1\2', t)

    return t


__all__ = ['normalize']
