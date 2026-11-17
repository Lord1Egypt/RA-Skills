"""rare_disease_sources.py — 罕见病/遗传病专源检索 CLI 入口（薄包装）。

§16.9 出站调用收口：所有 urllib 出站实现已迁至 `adapters/rare_disease_sources.py`
（`adapters/` 为 ct-base 规定的出站调用唯一归宿）。本文件只保留 CLI 契约
（argparse 参数名、输出格式、退出行为完全不变），供 workbench server 以
subprocess 方式调用，也供存量 `import` 调用方继续使用。

数据源与降级策略见 adapters/rare_disease_sources.py 模块文档字符串。
"""

from __future__ import annotations

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from adapters.rare_disease_sources import *  # noqa: F401,F403  (re-export: CLI 契约兼容)
from adapters.rare_disease_sources import main  # noqa: F401

if __name__ == "__main__":
    main()
