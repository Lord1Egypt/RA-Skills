#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""r_code_policy.py — 免费技能 R 代码输出策略（2026-10-13 产品决策）

策略：过于复杂/高级的检验方法不向用户提供 R 代码，改提示联系作者。
命中名单时：
  - skill 展示层不渲染 R 源码，改渲染 info.r_code_unavailable 提示（zh/en）
  - coze 引擎侧（src/r_engine/run_task.R 顶部 .R_CODE_DENYLIST）已在信封源头
    将 repro.r 替换为提示文案——两侧同源维护，增删方法必须同步改两处。

分层依据（与用户确认的提案一致）：
  A 类（提供 R 代码，38 个）= 经典教科书方法（封闭公式或单一权威包调用）
  B 类（不提供，27 个）  = 序贯/自适应/蒙特卡洛模拟/先验借用/新兴复杂设计
                         （2026-10-19 追加：meta_planning 纯商业保护划入，非复杂度依据）
"""
from __future__ import annotations

import os

#: 不提供 R 代码的高级方法名单（与 coze 引擎 node 出口
#: src/graphs/nodes/samplesize.py::_R_CODE_GATED_TESTS 严格一致）
R_CODE_UNAVAILABLE_TESTS = frozenset({
    # 成组序贯（rpact 精确边界 + 消耗函数 + 无效边界）
    "group_sequential", "gsd_proportion", "gsd_survival", "gsd_hazard",
    "gsd_poisson", "gsd_survival_sim", "gsd_hazard_sim",
    # 自适应设计 / 多臂多阶段 / 条件功效
    "adaptive", "adaptive_simulate", "mams", "conditional_power",
    # 贝叶斯 / 保证度 / 剂量递增（模拟驱动）
    "bayesian", "assurance", "dose_escalation",
    # 胜率 / 必须赢 / 多终点
    "win_ratio", "must_win", "multiple_endpoints",
    # 历史对照借用 / 混合模型（simr）
    "historical_controls", "survival_historical", "mixed_model",
    # 生存高级（非劣效 / 等效 / 优效 / 精确 / 竞争风险 / 复发事件）
    "ni_survival", "survival_equivalence", "survival_superiority",
    "survival_exact", "competing_risks", "recurrent_events",
    # Meta 分析前瞻性规划（2026-10-19 产品决策：纯商业保护划入 B 类，
    # 非复杂度依据 —— 该检验为 Hedges & Pigott (2001) 封闭公式法）
    "meta_planning",
})

#: 提示文案（与用户确认的版本一致；i18n 的 info.r_code_unavailable 同文）
HINT_ZH = "该分析方法属于高级功能，免费技能不提供对应的 R 代码，请联系作者解决此问题。"
HINT_EN = ("This is an advanced method: the R code is not provided in the free "
           "skill. Please contact the author to resolve this.")


def is_paid_env() -> bool:
    """本地付费标记判定（ct-base §20.12）：环境变量 CTSS_ACCOUNT_ID /
    CTSS_BILLING_TOKEN 任一非空即视为付费用户。当前无标记发放渠道 → False
    （架构位先行，全部按免费拦截）。coze 端 node 出口按请求信封的
    account_id/billing_token 做同样判定（attach_billing 会把 env 标记
    随请求透传，两侧行为一致）。"""
    return bool((os.environ.get("CTSS_ACCOUNT_ID") or "").strip()
                or (os.environ.get("CTSS_BILLING_TOKEN") or "").strip())


def r_code_unavailable(test: str, paid: bool = False) -> bool:
    """该 test 是否属于「不提供 R 代码」的高级方法。

    paid=True（付费用户）→ 一律放行（返回 False）；默认按免费名单拦截。
    """
    if paid:
        return False
    return test in R_CODE_UNAVAILABLE_TESTS
