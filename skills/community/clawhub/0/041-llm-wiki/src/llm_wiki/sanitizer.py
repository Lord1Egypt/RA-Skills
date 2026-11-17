"""跨平台文件名清洗:wiki 页面 stem 与 sources/zotero 别名共用。

借鉴 ZotMoov(`lib/02-sanitize-filename.js`、`src/00-zotmoov-wildcard.js`):
非法字符清洗、Windows 保留名与尾部点/空格处理、UTF-8 字节级截断并
回溯至词边界、变音符去除(NFKD + 组合符剥离,不影响 CJK)。

本模块只约束**新增**命名;既有页面与别名是链接锚点,不做重命名。
"""

from __future__ import annotations

import re
import unicodedata

DEFAULT_MAX_BYTES = 120
FALLBACK_STEM = "untitled"

# Windows/跨平台非法字符(不含 '/',它按分隔符处理)与控制字符
_ILLEGAL_CHARS = re.compile(r'[\\:*?"<>|\x00-\x1f\x7f]')
_SEPARATORS = re.compile(r"[\s/]+")
_DASH_RUNS = re.compile(r"-{2,}")
_WINDOWS_RESERVED = re.compile(r"^(con|prn|aux|nul|com[0-9]|lpt[0-9])$", re.IGNORECASE)


def _strip_diacritics(text: str) -> str:
    """NFKD 分解后剥离组合音符;CJK 等表意字符(Lo)不受影响。"""
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")


def _truncate_to_bytes(stem: str, max_bytes: int) -> str:
    """按 UTF-8 字节截断,回溯至最近的词边界('-'),不截断多字节字符。"""
    raw = stem.encode("utf-8")
    if len(raw) <= max_bytes:
        return stem
    cut = raw[:max_bytes].decode("utf-8", errors="ignore")
    boundary = cut.rfind("-")
    if boundary > 0:
        cut = cut[:boundary]
    return cut


def sanitize_title_stem(title: str, max_bytes: int = DEFAULT_MAX_BYTES) -> str:
    """把任意标题清洗为跨平台安全的文件名 stem(不含扩展名)。

    - 去除变音符(NFKD + 组合符剥离),保留 CJK;
    - 空白与 '/' 归为 '-' 分隔符,其余非法字符与控制字符移除;
    - 折叠重复 '-',剥离首尾 '-'/'.'/空格;
    - Windows 保留名(CON/PRN/AUX/NUL/COM0-9/LPT0-9)追加 '_' 转义;
    - 超长时按 UTF-8 字节截断并回溯至词边界;
    - 清洗结果为空时回退为 "untitled"。
    """
    text = _strip_diacritics(str(title or ""))
    text = _ILLEGAL_CHARS.sub("", text)
    text = _SEPARATORS.sub("-", text)
    text = _DASH_RUNS.sub("-", text)
    text = text.strip("-. ")

    if _WINDOWS_RESERVED.match(text):
        text = f"{text}_"

    text = _truncate_to_bytes(text, max(1, max_bytes)).strip("-. ")
    return text or FALLBACK_STEM
