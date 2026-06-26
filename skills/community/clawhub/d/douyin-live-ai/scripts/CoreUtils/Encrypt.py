import hashlib


def md5_encrypt(text: str) -> str:
    """对字符串进行 MD5 加密，返回十六进制字符串"""
    return hashlib.md5(text.encode('utf-8')).hexdigest()
