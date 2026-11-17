#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Playbook：投资理念、PLAN_TARGET、METHOD_PLAN、盘前 6 项、账户骨架。

内容型模块 —— 供报告 §16+ 财富密码融合层直接引用。
"""

from __future__ import annotations

from typing import Any

from . import calibers as C
from . import formulas as F

# ------------------------------------------------------------------ 投资理念
PHILOSOPHY = """\
以公司的基本面为核心，侧重投资具有高增长潜力的新兴产业，寻求市场价格低于企业内在价值的投资机会。
自上而下：先寻找低估值行业 → 再从行业寻找低估值股票 → 最后从公司基本面再次筛选精准到个股。
以中长期逻辑为主，中短线波段赚取差价。"""

PRODUCT_FEATURES = (
    "全方位市场分析：行业动态 + 公司基本面双维度，保证投资建议的科学性与合理性",
    "自上而下选股模式：低估值行业 → 低估值个股 → 基本面复核",
    "长期跟踪新兴科技领域：中长期逻辑为主，中短线波段赚差价",
)

SERVICES = ("市场趋势", "热点板块", "个股投资建议")

# ------------------------------------------------------------------ 目标与考核
PLAN_TARGET: dict[str, Any] = {
    "annual_return_low": F.TARGET_ANNUAL_LOW,
    "annual_return_high": F.TARGET_ANNUAL_HIGH,
    "compounding": "按年复利",
    "dashboard": ("执行完整率", "风控合规率"),
    "note": "考核带年化 12%–25%。低于下限说明执行不足，高于上限说明承担了超预算风险，两者都要复盘。",
}

# ------------------------------------------------------------------ 方法总纲
METHOD_PLAN: dict[str, Any] = {
    "0_口径": f"口径版本 {C.CALIBER_VERSION}，报告首页必须写死；口径变更须全量重算并报告 ±N 只敏感度",
    "1_行业": "周线/月线长期下跌至超低位（3 年月线收盘历史分位 ≤25%）且行业指数低位放量（额比 ≥1.0×）；有政策支持优先",
    "2_个股": "与行业同法：历史分位 ≤25% 且额比 ≥1.0×；分位是主判据，区间位置仅作辅助",
    "2.5_可交易性": "剔除退市/ST/停牌/PB 为负/上市不足 60 日/近 20 日均额 <3000 万",
    "3_基本面": "连续两年年报亏损否决；中报同比 ≤0 否决；单年亏损与增速大幅下滑为减分项",
    "4_主题": "「链」形态主题跳过 L1 否决权，行业层仅定性",
    "5_评分": "S = 0.30·tech + 0.25·flow + 0.20·fund + 0.15·cycle + 0.10·fib",
    "6_仓位": "N = floor(权益 × r ÷ (entry − stop))，r = 冰点 0.5% / 常态 1%；单票 ≤10%、单行业 ≤30%",
    "7_风控": "Σ开仓名义 ≤ α_max × 权益；回撤 ≥15% 减仓、≥25% 停机",
    "8_复核": "每条预判都要可证伪，次日盘后自动核验",
}

# ------------------------------------------------------------------ 盘前 6 项
PRE_OPEN_CHECKLIST: tuple[dict[str, str], ...] = (
    {"no": "1", "item": "市场阶段", "how": "判定 I/II/III/IV 并确认是否冰点（涨停 <40 家 且 炸板率 >40% 且 指数跌幅 >1%）", "output": "α_max 取值"},
    {"no": "2", "item": "α 预算", "how": "权益 × α_max，扣除已开仓名义，算出今日剩余额度", "output": "今日可开仓额度"},
    {"no": "3", "item": "回撤校验", "how": "对比权益峰值，确认是否触发 15% / 25% 熔断", "output": "NORMAL / REDUCE / HALT"},
    {"no": "4", "item": "候选复核", "how": "重跑 L1→L2→L2.5→L3，确认前一日入池标的未被新公告否决", "output": "今日候选清单"},
    {"no": "5", "item": "入场与止损", "how": "为每只候选写明 entry / stop / 斐波那契位置，校验 entry > stop", "output": "下单卡"},
    {"no": "6", "item": "公告与解禁", "how": "核查减持、解禁、业绩预告、监管问询等事件", "output": "风险事件清单"},
)

# ------------------------------------------------------------------ 账户骨架
ACCOUNT_SKELETON: dict[str, Any] = {
    "layers": (
        {"name": "核心仓（60%）", "rule": "四层全通过 + 综合分 ≥70，单票 ≤10%", "horizon": "中长期"},
        {"name": "卫星仓（30%）", "rule": "L1/L2 通过但综合分 55–70，单票 ≤5%", "horizon": "中短线波段"},
        {"name": "现金（10%）", "rule": "含冰点期额外保有的现金垫", "horizon": "—"},
    ),
    "single_name_cap": 0.10,
    "single_sector_cap": 0.30,
    "rule": "任何情况下不得突破单票 10% / 单行业 30%；突破需书面复盘。",
}

# ------------------------------------------------------------------ 五层图谱
FIVE_LAYER_MAP: tuple[dict[str, str], ...] = (
    {"layer": "① 制度层", "content": "十五五规划六张网 + 六大新兴支柱 + 六大未来产业", "watch": "政策落地节奏"},
    {"layer": "② 资金层", "content": "龙虎榜净买、主力净流入、北向/两融变动", "watch": "连续性与集中度"},
    {"layer": "③ 产业层", "content": "行业历史分位、额比、个股分位离散度", "watch": "分化是否扩大"},
    {"layer": "④ 公司层", "content": "盈利质量、增速红线、筹码集中度、国企背景", "watch": "增速是否失速"},
    {"layer": "⑤ 交易层", "content": "S 评分、α 预算、仓位 N、熔断阶梯", "watch": "纪律是否执行"},
)


def playbook() -> dict[str, Any]:
    """导出完整 playbook，供报告生成器一次性取用。"""
    return {
        "caliber_version": C.CALIBER_VERSION,
        "philosophy": PHILOSOPHY,
        "product_features": PRODUCT_FEATURES,
        "services": SERVICES,
        "plan_target": PLAN_TARGET,
        "method_plan": METHOD_PLAN,
        "pre_open_checklist": PRE_OPEN_CHECKLIST,
        "account_skeleton": ACCOUNT_SKELETON,
        "five_layer_map": FIVE_LAYER_MAP,
        "disclaimer": "本内容仅供教育与研究，不构成投资建议。市场有风险，投资需谨慎。",
    }


def render_checklist_md() -> str:
    lines = ["| # | 检查项 | 做法 | 产出 |", "|---|---|---|---|"]
    for c in PRE_OPEN_CHECKLIST:
        lines.append(f"| {c['no']} | {c['item']} | {c['how']} | {c['output']} |")
    return "\n".join(lines)


def render_method_md() -> str:
    lines = ["| 步骤 | 规则 |", "|---|---|"]
    for k, v in METHOD_PLAN.items():
        lines.append(f"| {k.replace('_', ' ')} | {v} |")
    return "\n".join(lines)


def render_five_layer_md() -> str:
    lines = ["| 层 | 内容 | 观察点 |", "|---|---|---|"]
    for x in FIVE_LAYER_MAP:
        lines.append(f"| {x['layer']} | {x['content']} | {x['watch']} |")
    return "\n".join(lines)
