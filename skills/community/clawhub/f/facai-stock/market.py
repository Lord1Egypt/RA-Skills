"""股票市场前缀工具（雪球格式：SH / SZ / BJ）"""

_PREFIX_MAP = {
    "6": "SH",  # 上交所：60xxxx、68xxxx
    "0": "SZ",  # 深交所主板：000xxx、002xxx、003xxx
    "3": "SZ",  # 深交所创业板：300xxx、301xxx
    "4": "BJ",  # 北交所：4xxxxx
    "8": "BJ",  # 北交所：8xxxxx
    "9": "BJ",  # 北交所：9xxxxx
}


def add_prefix(code: str) -> str:
    """6位纯数字代码 → 雪球格式，如 000001 → SZ000001"""
    return f"{_PREFIX_MAP.get(code[0] if code else '', 'SH')}{code}"


def strip_prefix(raw: str) -> str:
    """去除市场前缀，返回纯6位数字代码"""
    raw = raw.strip().upper()
    for prefix in ("SH", "SZ", "BJ"):
        if raw.startswith(prefix):
            return raw[len(prefix):]
    return raw


def is_valid_code(s: str) -> bool:
    """判断字符串是否为合法的6位股票代码（去除前缀后）"""
    cleaned = strip_prefix(s)
    return cleaned.isdigit() and len(cleaned) == 6
