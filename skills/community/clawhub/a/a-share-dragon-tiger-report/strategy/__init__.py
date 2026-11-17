#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A股龙虎榜深度研判 + 财富密码策略包。

模块分工：
  calibers  —— 六条已确认口径（唯一口径来源）
  formulas  —— 核心公式（S、α、仓位 N、斐波那契、凯利、熔断、冰点）
  filters   —— 硬闸门（L1 行业 / L2.5 可交易性 / L3 基本面）
  funnel    —— 四层漏斗 L1→L2→L2.5→L3（月线分位、区间位置、额比）
  risk      —— α 预算账本、回撤熔断、限额校验
  pipeline  —— 候选 → 过闸 → 评分 → 风控信号表
  playbook  —— 投资理念、PLAN_TARGET、盘前 6 项、账户骨架
  v3_ext    —— v3.0 只读旁路五模块（宏观/因子/X主题/短线/水印）
  gcceo_ext —— v3.1 GCCEO 全量整合只读旁路层（十域91技能映射，无剔除权）
"""

from __future__ import annotations

__version__ = "3.1.0"

from . import (calibers, filters, formulas, funnel, pipeline, playbook, risk,  # noqa: F401
               v3_ext, gcceo_ext)

__all__ = [
    "calibers",
    "formulas",
    "filters",
    "funnel",
    "risk",
    "pipeline",
    "playbook",
    "v3_ext",
    "gcceo_ext",
    "__version__",
]
