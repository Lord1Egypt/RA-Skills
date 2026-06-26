"""Arxiv 论文处理 Agent Skill 模块"""

import sys
import io

__version__ = "2.0.1"


def setup_encoding():
    """
    配置标准输出编码为 UTF-8，解决 Windows 环境下的编码问题

    Windows 控制台默认使用 GBK 编码，无法正确显示 emoji 和其他 Unicode 字符。
    此函数强制使用 UTF-8 编码，确保跨平台兼容性。
    """
    if sys.platform == 'win32':
        try:
            # 重新包装 stdout 和 stderr，使用 UTF-8 编码
            if hasattr(sys.stdout, 'buffer'):
                sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
            if hasattr(sys.stderr, 'buffer'):
                sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
        except Exception:
            # 如果失败，保持默认编码（可能会在某些环境下丢失字符，但不会崩溃）
            pass


# 自动配置编码
setup_encoding()
