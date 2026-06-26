"""Dongchedi font-based number obfuscation decoder.

Dongchedi replaces digits and the '万' character with Private Use Area (PUA)
unicode codepoints rendered by a custom web font.  The mapping is static and
extracted from the font file.
"""

import re

# PUA codepoint -> real character
_CHAR_MAP: dict[str, str] = {
    "\ue439": "0",
    "\ue54c": "1",
    "\ue463": "2",
    "\ue49d": "3",
    "\ue41d": "4",
    "\ue411": "5",
    "\ue534": "6",
    "\ue3eb": "7",
    "\ue4e3": "8",
    "\ue45d": "9",
    "\ue40a": "万",
}

_PUA_PATTERN = re.compile("[" + "".join(_CHAR_MAP.keys()) + "]")


def decode_text(text: str) -> str:
    """Replace all PUA codepoints in *text* with their real characters."""
    return _PUA_PATTERN.sub(lambda m: _CHAR_MAP[m.group()], text)


def decode_number(text: str) -> float | None:
    """Decode obfuscated text and parse it as a float.

    Returns None when the decoded text contains no numeric content.
    """
    decoded = decode_text(text).replace("万", "").replace(",", "").strip()
    if not decoded:
        return None
    try:
        return float(decoded)
    except ValueError:
        return None
