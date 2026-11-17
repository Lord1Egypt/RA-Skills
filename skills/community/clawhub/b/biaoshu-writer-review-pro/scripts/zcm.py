#!/usr/bin/env python3
"""百炼®标书开放 API 轻客户端入口。

实际 CLI 实现在 zcm_lib.cli；本文件保留旧路径兼容。
"""
from __future__ import annotations

from zcm_lib import cli as _cli

globals().update({name: getattr(_cli, name) for name in dir(_cli) if not name.startswith("__")})


if __name__ == "__main__":
    main()
