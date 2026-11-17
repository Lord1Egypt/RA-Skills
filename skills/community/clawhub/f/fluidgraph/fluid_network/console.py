# -*- coding: utf-8 -*-
"""控制台输出辅助。

Windows 的 cmd/PowerShell 默认代码页是 GBK，直接 ``print`` 包含 ``³``、``✓``
等字符的文本会抛 :class:`UnicodeEncodeError` 并中断整个程序 —— 这显然不该
是一个物理计算问题的失败原因。这里提供两件事：

1. :func:`configure_stdout` —— 尽力把标准输出切到 UTF-8；
2. :func:`safe_print` —— 无论终端编码如何，都保证打得出来（打不出的字符降级）。
"""

from __future__ import annotations

import sys


def configure_stdout() -> None:
    """尽力把 stdout/stderr 切到 UTF-8；做不到就静默跳过。"""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is None:
            continue
        try:
            reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError, LookupError):  # pragma: no cover - 少数终端不支持
            pass


def safe_print(text: str = "", **kwargs) -> None:
    """打印文本；遇到终端不支持的字符时降级而不是崩溃。"""
    try:
        print(text, **kwargs)
    except UnicodeEncodeError:  # pragma: no cover - 仅在非 UTF-8 终端触发
        encoding = getattr(sys.stdout, "encoding", None) or "ascii"
        print(text.encode(encoding, errors="replace").decode(encoding, errors="replace"), **kwargs)
    except UnicodeError:  # pragma: no cover
        print(text.encode("ascii", errors="replace").decode("ascii"), **kwargs)


__all__ = ["configure_stdout", "safe_print"]
