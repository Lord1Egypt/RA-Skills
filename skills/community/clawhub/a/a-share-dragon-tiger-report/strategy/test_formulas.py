#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""公式自检。零外部依赖，直接 `python3 strategy/test_formulas.py` 或
`python3 -m strategy.test_formulas` 运行。全部通过则退出码 0。
"""

from __future__ import annotations

import pathlib
import sys

# 允许以脚本方式直接运行（此时没有包上下文）
if __package__ in (None, ""):
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from strategy import calibers as C          # noqa: E402
from strategy import filters as FLT         # noqa: E402
from strategy import formulas as F          # noqa: E402
from strategy import funnel as FN           # noqa: E402
from strategy import risk as RK             # noqa: E402

PASS, FAIL = 0, 0
FAILURES: list[str] = []


def ok(label: str, cond: bool, detail: str = "") -> None:
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  \033[32mPASS\033[0m {label}")
    else:
        FAIL += 1
        FAILURES.append(label)
        print(f"  \033[31mFAIL\033[0m {label} {detail}")


def close(a: float, b: float, tol: float = 1e-6) -> bool:
    return abs(a - b) <= tol


def raises(fn, exc=Exception) -> bool:
    try:
        fn()
    except exc:
        return True
    except Exception:
        return False
    return False


def section(t: str) -> None:
    print(f"\n\033[1m{t}\033[0m")


# ------------------------------------------------------------------ S 公式
section("综合分 S = 0.30·tech + 0.25·flow + 0.20·fund + 0.15·cycle + 0.10·fib")
bd = F.composite_score(tech=80, flow=60, fund=40, cycle=100, fib=0)
ok("加权和 = 24 + 15 + 8 + 15 + 0 = 62", close(bd.total, 62.0), f"实际 {bd.total}")
bd2 = F.composite_score(100, 100, 100, 100, 100)
ok("满分输入 → 100", close(bd2.total, 100.0), f"实际 {bd2.total}")
bd3 = F.composite_score(0, 0, 0, 0, 0, bonus=6, penalty=15)
ok("0 分 + 加分 6 − 减分 15 → 裁剪到 0", close(bd3.total, 0.0), f"实际 {bd3.total}")
ok("越界子项抛错", raises(lambda: F.composite_score(101, 0, 0, 0, 0), ValueError))
ok("None 子项抛错", raises(lambda: F.composite_score(None, 0, 0, 0, 0), ValueError))  # type: ignore[arg-type]
ok("拆解表 5 行", len(F.weighted_parts(bd)) == 5)

# ------------------------------------------------------------------ α 预算
section("α_max = 阶段上限（冰点 ×0.5）")
ok("阶段 I = 40%", close(F.alpha_max("I"), 0.40))
ok("阶段 II = 30%", close(F.alpha_max("II"), 0.30))
ok("阶段 III = 15%", close(F.alpha_max("III"), 0.15))
ok("阶段 IV = 5%", close(F.alpha_max("IV"), 0.05))
ok("阶段 II 冰点 = 15%", close(F.alpha_max("II", ice_point=True), 0.15))
ok("小写 'ii' 可识别", close(F.alpha_max("ii"), 0.30))
ok("非法阶段抛错", raises(lambda: F.alpha_max("V"), ValueError))
ok("累计 α 未超限通过", F.cumulative_alpha_ok(250_000, 1_000_000, 0.30))
ok("累计 α 超限不通过", not F.cumulative_alpha_ok(310_000, 1_000_000, 0.30))
ok("剩余额度 = 30 万 − 25 万 = 5 万",
   close(F.alpha_remaining(250_000, 1_000_000, 0.30), 50_000))
ok("权益为 0 抛错", raises(lambda: F.alpha_remaining(0, 0, 0.3), ValueError))

# ------------------------------------------------------------------ 仓位 N
section("仓位 N = floor(权益 × r ÷ (entry − stop))")
ok("常态 r=1%：(100万×1%) / (10−9) = 10000 股 → 10000",
   F.position_size(1_000_000, 10, 9, ice_point=False) == 10000)
ok("冰点 r=0.5%：(100万×0.5%) / (10−9) = 5000 股 → 5000",
   F.position_size(1_000_000, 10, 9, ice_point=True) == 5000)
ok("止损很近：(100万×1%) / (10−9.9) = 100000 股",
   F.position_size(1_000_000, 10, 9.9) == 100000)
ok("entry <= stop 抛错", raises(lambda: F.position_size(1_000_000, 9, 10), ValueError))
ok("自定义 r=2% → 20000 股", F.position_size(1_000_000, 10, 9, r=0.02) == 20000)
ok("名义金额 = 股数 × 价格", close(F.position_notional(10000, 10), 100_000))

# ------------------------------------------------------------------ 斐波那契
section("斐波那契回撤")
fibs = F.fib_retracement(high=100, low=0)
ok("0.618 档 = 100 − 61.8 = 38.2", close(fibs["0.618"], 38.2, 1e-9))
ok("0.382 档 = 100 − 38.2 = 61.8", close(fibs["0.382"], 61.8, 1e-9))
ok("0.500 档 = 50", close(fibs["0.500"], 50.0, 1e-9))
ok("high <= low 抛错", raises(lambda: F.fib_retracement(0, 100), ValueError))
ok("价格恰在 0.618 回撤位（自底向上 38.2）→ 位置分 100",
   close(F.fib_score(38.2, 100, 0), 100.0, 1e-6))
ok("价格在区间顶 → 位置分 0", close(F.fib_score(100, 100, 0), 0.0, 1e-9))
ok("价格在区间底 → 位置分约 38.2（破位风险，非满分）",
   close(F.fib_score(0, 100, 0), 38.188, 1e-3))
ok("位置分随接近高点而单调下降",
   F.fib_score(45, 100, 0) > F.fib_score(75, 100, 0) > F.fib_score(95, 100, 0))

# ------------------------------------------------------------------ 凯利
section("凯利 = min(p − (1−p)/b, 0.25) × 0.5")
ok("p=0.6,b=2 → (0.6−0.4/2)=0.4 → min(0.4,0.25)=0.25 → ×0.5=0.125",
   close(F.kelly_fraction(0.6, 2.0), 0.125))
ok("p=0.5,b=1 → 0 → 0", close(F.kelly_fraction(0.5, 1.0), 0.0))
ok("负凯利归零：p=0.3,b=1 → −0.4 → 0", close(F.kelly_fraction(0.3, 1.0), 0.0))
ok("胜率越界抛错", raises(lambda: F.kelly_fraction(1.2, 2.0), ValueError))
ok("赔率 <=0 抛错", raises(lambda: F.kelly_fraction(0.6, 0), ValueError))

# ------------------------------------------------------------------ 熔断
section("熔断：≥15% 减仓，≥25% 停机")
ok("回撤 5% → NORMAL", F.circuit_breaker(0.05).action == "NORMAL")
ok("回撤 15% → REDUCE", F.circuit_breaker(0.15).action == "REDUCE")
ok("回撤 18% → REDUCE", F.circuit_breaker(0.18).action == "REDUCE")
ok("回撤 25% → HALT", F.circuit_breaker(0.25).action == "HALT")
ok("回撤 40% → HALT", F.circuit_breaker(0.40).action == "HALT")
ok("risk_check 峰值 120 万 → 现值 96 万 = 回撤 20% → REDUCE",
   RK.risk_check(1_200_000, 960_000)["action"] == "REDUCE")
ok("risk_check 峰值非正抛错", raises(lambda: RK.risk_check(0, 1), ValueError))

# ------------------------------------------------------------------ 冰点
section("冰点判定：涨停 <40 家 且 炸板率 >40% 且 指数跌幅 >1%")
ok("三项全中 → 冰点", F.is_ice_point(28, 0.52, -1.8))
ok("仅两项 → 非冰点", not F.is_ice_point(28, 0.52, -0.5))
ok("涨停家数够 → 非冰点", not F.is_ice_point(55, 0.52, -1.8))

# ------------------------------------------------------------------ 月线工具
section("历史分位 / 区间位置 / 下 1/4 阈值（保留当月未完结月）")
closes = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10]
ok("当前 10 为最低 → 分位 0%", close(FN.rank_percentile(closes, 10), 0.0))
ok("当前 100 为最高 → 分位 90%（9/10 低于它）", close(FN.rank_percentile(closes, 100), 90.0))
ok("当前 55 → 分位 50%（50/60/70/80/90 五档低于？实际 5 个）",
   close(FN.rank_percentile(closes, 55), 50.0))
ok("当前 10 → 区间位置 0", close(FN.interval_position(closes, 10), 0.0))
ok("当前 55 → 区间位置 0.5", close(FN.interval_position(closes, 55), 0.5))
ok("下 1/4 阈值 = 10 + 0.25×90 = 32.5", close(FN.lower_quarter_threshold(closes), 32.5))
ok("现价 20 还需跌 (32.5/20−1)×100 = 62.5%",
   close(FN.downside_to_lower_quarter(closes, 20), 62.5))
ok("现价 40 已在下 1/4 内 → 负值",
   FN.downside_to_lower_quarter(closes, 40) < 0)

section("额比（必须剔除未完结的当月，且必须用 amount）")
amounts = [100.0] * 12 + [200.0, 200.0, 200.0]   # 前 12 月均值 100，近 3 月均值 200
ok("额比 = 200/100 = 2.0", close(FN.amount_ratio(amounts), 2.0))
ok("不足 15 个月抛错", raises(lambda: FN.amount_ratio([100.0] * 14), ValueError))
ok("个股分位离散度 = max − min",
   close(FN.dispersion([12.0, 88.4, 41.0]), 76.4))
ok("离散度 ≥60pp → 报警", "严重分化" in FN.dispersion_alert(76.4))
ok("离散度 <60pp → 正常", "严重分化" not in FN.dispersion_alert(22.0))

# ------------------------------------------------------------------ 口径
section("六条口径常量（v2 定稿，v2.3 增补知识蒸馏阈值）")
ok("口径版本 = v2.3", C.CALIBER_VERSION == "v2.3")
ok("① 国企背景非门槛", C.SOE_BACKGROUND_IS_GATE is False)
ok("② 新兴科技优先", C.EMERGING_TECH_FIRST is True)
ok("③ 增速口径 = 半年", C.PROFIT_GROWTH_CALIBER == "half_year")
ok("④ 单年亏损非否决", C.SINGLE_YEAR_LOSS_IS_VETO is False)
ok("④ 连续两年亏损 = 否决", C.TWO_CONSECUTIVE_LOSSES_IS_VETO is True)
ok("⑤ 链主题跳过 L1", C.CHAIN_THEME_SKIPS_L1_VETO is True)
ok("⑤ 算力网识别为链", C.is_chain_theme("算力网") is True)
ok("⑥ L2.5 位于 L2 与 L3 之间", C.TRADABILITY_LAYER == "L2.5")
ok("层顺序正确", C.LAYERS == ("L1行业", "L2个股", "L2.5可交易", "L3基本面"))
ok("口径摘要含版本号", "v2" in C.describe())

# ------------------------------------------------------------------ 闸门
section("闸门行为")
g = FLT.gate_industry("医药生物", rank=18.4, vr=1.28)
ok("行业 分位 18.4% + 额比 1.28× → 入池", g.passed)
g2 = FLT.gate_industry("计算机", rank=22.6, vr=0.86)
ok("行业 分位低但额比 0.86× → 否决", not g2.passed)
g3 = FLT.gate_industry("新一代通信网", rank=33.8, vr=0.92)
ok("链主题 → 跳过 L1 否决", g3.passed)

ok("L2.5 退市 → 剔除", not FLT.gate_tradability({"code": "x", "name": "x", "delisted": True}).passed)
ok("L2.5 ST → 剔除", not FLT.gate_tradability({"code": "x", "name": "x", "is_st": True}).passed)
ok("L2.5 PB 为负 → 剔除", not FLT.gate_tradability({"code": "x", "name": "x", "pb": -2.71}).passed)
ok("L2.5 流动性不足 → 剔除",
   not FLT.gate_tradability({"code": "x", "name": "x", "avg_turnover_20d": 2_000_000}).passed)
ok("L2.5 上市不足 60 日 → 剔除",
   not FLT.gate_tradability({"code": "x", "name": "x", "listed_days": 30}).passed)
ok("L2.5 正常 → 通过", FLT.gate_tradability({"code": "x", "name": "x", "pb": 3.0, "listed_days": 900}).passed)

# 注：以下两条测的是「亏损口径」，必须同时给足中报同比 ——
# 否则会先撞上「关键数据缺失 → 一票否决」（契约第七章第 3 条），测不到想测的分支。
ok("L3 连续两年亏损 → 否决",
   not FLT.gate_fundamental({"code": "x", "name": "x", "annual_loss_years": [2024, 2025],
                             "interim_yoy": 0.05}).passed)
ok("L3 间隔亏损（2023,2025）→ 不否决",
   FLT.gate_fundamental({"code": "x", "name": "x", "annual_loss_years": [2023, 2025],
                         "interim_yoy": 0.05}).passed)
gg = FLT.gate_fundamental({"code": "x", "name": "x", "annual_loss_years": [2025],
                           "interim_yoy": 0.05})
ok("L3 单年亏损 → 减分 10 且不否决", gg.passed and close(gg.score_penalty, 10.0))

ok("L3 中报 −5.4% ≤0 → 触发增速硬线",
   not FLT.gate_fundamental({"code": "x", "name": "x", "interim_yoy": -0.054, "prior_fy_yoy": 0.178}).passed)
gp = FLT.gate_fundamental({"code": "x", "name": "x", "interim_yoy": 0.003, "prior_fy_yoy": 0.217})
ok("L3 中报 +0.3% < 21.7% 的 50% → 减分 15 且通过",
   gp.passed and close(gp.score_penalty, 15.0))
gl = FLT.gate_fundamental({"code": "x", "name": "x", "interim_yoy": 0.15, "prior_fy_yoy": 0.20})
ok("L3 中报 +15% ≥ 20% 的 50% → 不减分", gl.passed and close(gl.score_penalty, 0.0))
gs = FLT.gate_fundamental({"code": "x", "name": "x", "interim_yoy": 0.05, "soe_background": True})
ok("L3 国企背景 → 加分 6", close(gs.score_bonus, 6.0))
ge = FLT.gate_fundamental({"code": "x", "name": "x", "interim_yoy": 0.05, "emerging_tech": True})
ok("L3 新兴科技 → 加分 8", close(ge.score_bonus, 8.0))
gn = FLT.gate_fundamental({"code": "x", "name": "x"})
ok("L3 中报缺失 → 一票否决（关键数据缺失无法验证，不得默认通过）",
   not gn.passed and any("中报同比缺失" in x for x in gn.reasons))

# ------------------------------------------------------------------ 风控账本
section("α 账本三道限额（用 stage=I α=40% 隔离出单行业上限测试）")
led = RK.AlphaLedger(equity=1_000_000, stage="I")     # α 40% 才能塞下 3 笔医药 + 1 笔机械
ok("单票 15% 超 10% 上限 → 拒绝", not led.can_open(150_000)[0])
ok("拒绝原因含『单票上限』", "单票上限" in led.can_open(150_000)[1])
ok("单票 10% → 通过", led.can_open(100_000)[0])
led.add(RK.Position("a", "A", 10000, 10, 9, "医药生物"))
led.add(RK.Position("b", "B", 10000, 10, 9, "医药生物"))
led.add(RK.Position("c", "C", 10000, 10, 9, "医药生物"))
ok("同行业累计 30% 已用 = cap", close(led.snapshot()["used_pct"], 0.30, 1e-6))
ok("同行业再加 10% → 单行业 30% 上限触发 → 拒绝",
   not led.can_open(100_000, "医药生物")[0])
ok("拒绝原因含『单行业上限』", "单行业上限" in led.can_open(100_000, "医药生物")[1])
ok("换行业加 10% → 通过", led.can_open(100_000, "机械设备")[0])
led.add(RK.Position("d", "D", 10000, 10, 9, "机械设备"))   # total 40% = α cap
ok("账本快照已用 40%", close(led.snapshot()["used_pct"], 0.40, 1e-6))
ok("α 上限 40% 已满 → 任何加仓被拒", not led.can_open(1)[0])
ok("拒绝原因含『α 预算』", "α 预算" in led.can_open(1)[1])
led_ice = RK.AlphaLedger(equity=1_000_000, stage="II", ice_point=True)
ok("冰点 α 上限 = 15%", close(led_ice.alpha_budget, 0.15))

# ------------------------------------------------------------------ 四层漏斗
section("四层漏斗端到端（口径 v2）")
fr = FN.run_funnel(
    industries=[FN.Industry("i1", "医药生物", 18.4, 1.28)],
    stocks=[
        FN.Stock("sh600276", "恒瑞医药", "医药生物", 18.4, 1.28,
                 {"interim_yoy": 0.003, "prior_fy_yoy": 0.217, "pb": 7.8, "listed_days": 4800}),
        FN.Stock("sz300124", "汇川技术", "医药生物", 21.0, 0.99,
                 {"interim_yoy": -0.054, "prior_fy_yoy": 0.178, "pb": 5.4, "listed_days": 3600}),
        FN.Stock("sz300760", "迈瑞医疗", "医药生物", 19.7, 1.12,
                 {"interim_yoy": -0.054, "prior_fy_yoy": 0.062, "pb": 6.9, "listed_days": 3100}),
        FN.Stock("sh688287", "观典防务", "医药生物", 2.9, 1.16,
                 {"delisted": True, "pb": 0.4}),
    ],
)
ok("L2 入池 3 只（额比 0.99× 的汇川技术被剔）", len(fr.l2_pass) == 3, f"实际 {len(fr.l2_pass)}")
ok("L2.5 剔除 1 只（观典防务）",
   len(fr.l2_5_removed) == 1 and fr.l2_5_removed[0].name == "观典防务")
ok("L3 否决 1 只（迈瑞医疗 −5.4% 触发硬线）",
   len(fr.l3_vetoed) == 1 and fr.l3_vetoed[0].name == "迈瑞医疗")
ok("最终通过 1 只 = 恒瑞医药",
   len(fr.l3_pass) == 1 and fr.l3_pass[0].name == "恒瑞医药")
ok("未入池的汇川不在 L2 池中",
   all(s.name != "汇川技术" for s in fr.l2_pass))
ok("已退市的观典未进入 L3 统计",
   all(g.name != "观典防务" for g in fr.l3_vetoed))

fr_strict = FN.run_funnel(
    industries=[FN.Industry("i1", "医药生物", 18.4, 1.28)],
    stocks=[
        FN.Stock("sh600276", "恒瑞医药", "医药生物", 18.4, 1.28,
                 {"interim_yoy": 0.003, "prior_fy_yoy": 0.217, "pb": 7.8, "listed_days": 4800}),
    ],
    strict_growth=True,
)
ok("严格口径（任何减速即排除）→ 0 只", len(fr_strict.l3_pass) == 0)
ok("敏感度字段齐备",
   "rule_50pct_relative" in fr.sensitivity and "rule_any_deceleration" in fr.sensitivity)

# ------------------------------------------------------------------ 汇总
print(f"\n{'='*56}")
print(f"  通过 {PASS} / 失败 {FAIL}")
if FAILURES:
    print("  失败项：")
    for f in FAILURES:
        print(f"    - {f}")
print(f"{'='*56}")
sys.exit(1 if FAIL else 0)
