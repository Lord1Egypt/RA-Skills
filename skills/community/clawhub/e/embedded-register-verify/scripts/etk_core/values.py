"""数值与取值解析：SVD 数值、枚举模式（含 x 占位位）、dimIndex 展开。"""

from __future__ import annotations

import re

_BIT_PATTERN = re.compile(r"[01xX]+")


def parse_number(text):
    """解析 SVD 或用户输入的整数：0x 十六进制、0b 或 # 二进制、其余为十进制。非法或负数抛 ValueError。"""
    s = str(text).strip().replace("_", "")
    if not s:
        raise ValueError("空数值")
    low = s.lower()
    if low.startswith("0x"):
        value = int(low[2:], 16)
    elif low.startswith("0b"):
        value = int(low[2:], 2)
    elif low.startswith("#"):
        value = int(low[1:], 2)
    else:
        value = int(s, 10)
    if value < 0:
        raise ValueError("数值不能为负")
    return value


def parse_enum_value(text, width):
    """返回 (value, mask)。`#01x` 形式里的 x 表示任意值，对应位的 mask 为 0。"""
    s = str(text).strip()
    if s.startswith("#") and _BIT_PATTERN.fullmatch(s[1:]):
        value = 0
        mask = 0
        for ch in s[1:]:
            value <<= 1
            mask <<= 1
            if ch in "01":
                mask |= 1
                value |= int(ch)
        return value, mask
    return parse_number(s), (1 << width) - 1


def dim_indices(dim, dim_index=None):
    """展开 dimIndex：支持 '0,1,2'、'0-3'、'A-H' 与混合写法；未给出时取 0..dim-1。"""
    if not dim_index:
        return [str(i) for i in range(dim)]
    out = []
    for part in dim_index.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            lo, hi = (x.strip() for x in part.split("-", 1))
            if lo.isdigit() and hi.isdigit():
                out.extend(str(i) for i in range(int(lo), int(hi) + 1))
                continue
            if len(lo) == 1 and len(hi) == 1 and lo.isalpha() and hi.isalpha():
                lower = lo.islower()
                for code in range(ord(lo.upper()), ord(hi.upper()) + 1):
                    ch = chr(code)
                    out.append(ch.lower() if lower else ch)
                continue
        out.append(part)
    return out
