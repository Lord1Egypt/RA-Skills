#!/usr/bin/env python3
"""doc-holmes CLI 启动器（skill 打包视图，唯一入口）。

用法：
  python3 scripts/doc_holmes_cli.py <triage|translate|batch|report|selfcheck> ...

依赖：
  pip install pymupdf            # 本体依赖
  pip install pdf2zh-next        # 翻译引擎（AGPL，独立进程调用）
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
# 打包视图：同目录 doc_holmes/；开发树未同步时回退 ../src（机器断言保证两者一致）
sys.path.insert(0, _HERE)
_DEV_SRC = os.path.join(os.path.dirname(_HERE), "src")
if os.path.isdir(os.path.join(_DEV_SRC, "doc_holmes")):
    sys.path.insert(0, _DEV_SRC)

from doc_holmes.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
