#!/usr/bin/env python3
"""源语言自动检测（v2.6.0）：从 PDF 文本统计字符集占比。

不再盲设 en：A/B 级 PDF 采样页文本 → 字符集统计 → 主导语言。
支持 en/zh/ja/ko/fr/de/es/ru/pt，其余回退 en。
"""

from __future__ import annotations

import re

import pymupdf

# 字符集范围 → ISO 639-1 代码
_RANGES = [
    ("zh", (0x4E00, 0x9FFF)), ("zh", (0x3400, 0x4DBF)),
    ("ja", (0x3040, 0x309F)), ("ja", (0x30A0, 0x30FF)),  # hiragana + katakana
    ("ko", (0xAC00, 0xD7AF)), ("ko", (0x1100, 0x11FF)),
    ("ru", (0x0400, 0x04FF)),
]

_LATIN_LANG_HINTS = {
    "fr": re.compile(r"\b(le|la|les|des|une|est|dans|pour|avec|sur|pas|plus)\b", re.I),
    "de": re.compile(r"\b(der|die|das|den|dem|ein|eine|und|ist|nicht|mit|für|auf)\b", re.I),
    "es": re.compile(r"\b(el|la|los|las|una|es|en|por|con|para|pero|más)\b", re.I),
    "pt": re.compile(r"\b(o|a|os|as|um|uma|é|em|para|com|não|mais|como)\b", re.I),
}


def detect_language(pdf_path: str, sample_pages: int = 3) -> dict:
    """从 PDF 采样页统计字符集占比，返回 {"lang": code, "confidence": float, ...}。"""
    doc = pymupdf.open(pdf_path)
    total_chars = 0
    counts = {"latin": 0, "cjk": 0, "hangul": 0, "cyrillic": 0}
    hint_counts = {k: 0 for k in _LATIN_LANG_HINTS}
    sample_text = ""
    indices = list(range(min(sample_pages, doc.page_count)))
    if doc.page_count > 6:
        mid = doc.page_count // 2
        if mid not in indices:
            indices.append(mid)
    for i in indices:
        text = doc[i].get_text()
        sample_text += text + "\n"
        for ch in text:
            total_chars += 1
            if "\u4e00" <= ch <= "\u9fff" or "\u3400" <= ch <= "\u4dbf":
                counts["cjk"] += 1
            elif "\uac00" <= ch <= "\ud7af":
                counts["hangul"] += 1
            elif "\u0400" <= ch <= "\u04ff":
                counts["cyrillic"] += 1
            elif ch.isascii() and ch.isalpha():
                counts["latin"] += 1
    doc.close()
    if total_chars == 0:
        return {"lang": "en", "confidence": 0.0, "total_chars": 0}
    # CJK 内部消歧：纯 CJK 无假名 → zh；有假名 → ja
    cjk_text = sample_text
    has_kana = any("\u3040" <= ch <= "\u30ff" for ch in cjk_text)
    best_non_latin = max(counts, key=lambda k: counts[k])
    best_ratio = counts[best_non_latin] / total_chars
    if best_non_latin == "latin" or best_ratio <= 0.15:
        # Latin 语种消歧
        best_hint, max_hits = "en", 0
        for code, pat in _LATIN_LANG_HINTS.items():
            n = len(pat.findall(sample_text))
            if n > max_hits:
                best_hint, max_hits = code, n
        if max_hits > 0:
            lang = best_hint
        else:
            lang = "en"   # Latin 字符占主导但无特定语种 hint → 默认 en
        confidence = round(min(max_hits / max(total_chars * 0.02, 1), 1.0), 2)
    elif best_non_latin == "cjk":
        lang = "ja" if has_kana else "zh"
        confidence = round(best_ratio, 2)
    else:
        lang = best_non_latin
        confidence = round(best_ratio, 2)
    return {"lang": lang, "confidence": confidence,
            "total_chars": total_chars, "counts": counts}
