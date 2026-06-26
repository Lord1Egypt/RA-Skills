#!/usr/bin/env python3
"""
易企秀 eqxiu-h5-creator 对外 AIGC HTTP API 的轻量客户端。

依赖：requests（与项目 requirements.txt 一致）
环境变量：EQXIU_AIGC_API_BASE（默认 https://ai-api.eqxiu.com）

实现拆分为同目录包 `eqxiu_aigc/`（品类/大纲/场景模板、H5 正文配图、COS+素材库上传等），本文件仅作入口。
上传子命令需：`pip install cos-python-sdk-v5`；COS/素材接口域名为 `*.eqxiu.com`（与投票鸭脚本同源流程）。
"""

from __future__ import annotations

import sys
from pathlib import Path

_scripts_dir = Path(__file__).resolve().parent
if str(_scripts_dir) not in sys.path:
    sys.path.insert(0, str(_scripts_dir))

from eqxiu_aigc.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
