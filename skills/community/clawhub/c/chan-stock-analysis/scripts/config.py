# -*- coding: utf-8 -*-
"""
chan-stock-analysis 技能配置文件
所有硬编码的 token、路径等敏感/可变配置均在此处集中管理。

优先级（从高到低）：
  1. 环境变量（推荐生产/多机部署时使用）
  2. 本文件中的默认值（本地开发时直接修改此处）

环境变量说明：
  ITICK_TOKEN          itick.org API Token（XAUUSD 行情）
  OBSIDIAN_STOCK_DIR   Obsidian 股票分析仓库绝对路径（分析报告/图表保存位置）
  CZSC_PATH            czsc 框架本地克隆路径（含 .venv）
"""

import os
from pathlib import Path

# ─────────────────────────────────────────────
# itick.org API
# ─────────────────────────────────────────────
ITICK_TOKEN: str = os.environ.get(
    "ITICK_TOKEN",
    "",
)
ITICK_API: str = "https://api.itick.org/forex/kline"

# ─────────────────────────────────────────────
# Obsidian 仓库路径
# ─────────────────────────────────────────────
OBSIDIAN_STOCK_DIR: Path = Path(
    os.environ.get("OBSIDIAN_STOCK_DIR", r"D:\knowledge\stock")
)

# ─────────────────────────────────────────────
# czsc 框架路径
# ─────────────────────────────────────────────
CZSC_PATH: str = os.environ.get(
    "CZSC_PATH",
    r"D:\QClawData\workspace\czsc",
)
