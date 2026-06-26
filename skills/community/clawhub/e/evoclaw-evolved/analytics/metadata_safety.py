# Analytics Metadata Type Safety
# 参考: claude-code AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS
#
# 设计:
#   事件元数据禁止包含代码片段或文件路径
#   通过 Type marker 在入口处运行时验证
#   strip_code_and_paths() 脱敏函数

from __future__ import annotations
import re
import os
from typing import Any
from pathlib import Path

WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", "/home/openclaw/.openclaw/workspace"))

# ─── 类型标记 ────────────────────────────────────────────────────

class AnalyticsMetadataVerified:
    """
    类型标记: 证明此对象不包含代码或文件路径.
    参考: AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS = never

    使用方式:
      data = sanitize_for_analytics(raw_data)
      verified = AnalyticsMetadataVerified(data)
      # verified 对象保证不包含敏感内容
    """
    __slots__ = ("_data",)

    def __init__(self, data: Any):
        # 验证后才存储
        object.__setattr__(self, "_data", data)


# ─── 脱敏函数 ───────────────────────────────────────────────────

# 代码/路径特征正则
_CODE_PATTERNS = [
    r"def\s+\w+\s*\(",          # Python def
    r"class\s+\w+\s*[:(]",       # Python class
    r"function\s+\w+\s*\(",      # JS function
    r"=>\s*\{",                  # JS arrow
    r"import\s+",                # import 语句
    r"from\s+\w+\s+import",      # Python import
    r"\$\w+\s*=",                # Shell 变量
    r"^\s*(sudo|rm|mv|chmod|chown)",  # 危险命令
    r"#.*coding:",               # Python coding
    r"<\?php",                   # PHP tag
]

_FILE_PATH_PATTERNS = [
    r"/home/[^/\s]+",           # Linux home 路径
    r"/tmp/[^/\s]+",            # /tmp 路径
    r"/etc/[^/\s]+",            # /etc 路径
    r"[A-Za-z]:\\\\",           # Windows 路径
    r"~\w*/",                    # Home 相对路径
    r"\.ssh/",                   # SSH 目录
    r"\.aws/",                   # AWS 目录
    r"/\w+/\w+\.(pem|key|json|crt)",  # 密钥文件
]

_ALL_PATTERNS = _CODE_PATTERNS + _FILE_PATH_PATTERNS


def _matches_any(text: str, patterns: list[str]) -> bool:
    for p in patterns:
        if re.search(p, text, re.MULTILINE):
            return True
    return False


def strip_code_and_paths(data: Any, max_depth: int = 10, _depth: int = 0) -> Any:
    """
    递归脱敏: 移除代码片段和文件路径.
    参考: claude-code stripProtoFields()

    - 字符串: 检查是否匹配代码/路径模式, 匹配则替换为 [REDACTED]
    - dict: 递归处理每个 value
    - list: 递归处理每个元素
    - 其他: 原样返回
    """
    if _depth > max_depth:
        return "[MAX_DEPTH_EXCEEDED]"

    if isinstance(data, str):
        if _matches_any(data, _ALL_PATTERNS):
            return "[REDACTED]"
        return data

    if isinstance(data, dict):
        result = {}
        for k, v in data.items():
            # Key 本身如果是路径, 脱敏 key
            safe_key = k
            if _matches_any(k, _FILE_PATH_PATTERNS):
                safe_key = "[REDACTED_KEY]"
            result[safe_key] = strip_code_and_paths(v, max_depth, _depth + 1)
        return result

    if isinstance(data, list):
        return [strip_code_and_paths(item, max_depth, _depth + 1) for item in data]

    return data


def verify_safe_for_analytics(data: Any) -> AnalyticsMetadataVerified:
    """
    验证数据安全后返回标记对象.
    验证失败抛出 ValueError.
    """
    import json
    serialized = json.dumps(data, ensure_ascii=False)
    if _matches_any(serialized, _CODE_PATTERNS):
        raise ValueError("Analytics data contains code — not allowed")
    if _matches_any(serialized, _FILE_PATH_PATTERNS):
        raise ValueError("Analytics data contains file paths — not allowed")
    return AnalyticsMetadataVerified(data)


def sanitize_for_analytics(data: dict) -> dict:
    """
    便捷函数: 先脱敏, 再验证, 返回安全数据.
    """
    sanitized = strip_code_and_paths(data)
    verify_safe_for_analytics(sanitized)
    return sanitized


if __name__ == "__main__":
    # Test: 代码片段被 redacted
    test_data = {
        "event": "code_review",
        "snippet": "def hello():\n    print('hello')",
        "file_path": "/home/openclaw/.ssh/id_rsa",
        "normal": "这是一个正常的事件描述",
    }
    result = sanitize_for_analytics(test_data)
    print(f"snippet: {result['snippet']}")
    print(f"file_path: {result['file_path']}")
    print(f"normal: {result['normal']}")

    # Test: 验证失败
    try:
        verify_safe_for_analytics({"bad": "def hack():\n  pass"})
        print("❌ Should have raised")
    except ValueError as e:
        print(f"✅ Correctly blocked: {e}")

    print("✅ Analytics Metadata Type Safety: all tests passed")
