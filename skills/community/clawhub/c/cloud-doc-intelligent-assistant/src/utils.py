"""工具函数模块"""

import hashlib


def compute_content_hash(content: str) -> str:
    """计算内容的SHA256哈希值"""
    return hashlib.sha256(content.encode('utf-8')).hexdigest()
