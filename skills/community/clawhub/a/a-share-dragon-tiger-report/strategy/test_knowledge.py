#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""knowledge v2.3 知识蒸馏模块自检（2026-09-25）

运行：python3 strategy/test_knowledge.py
覆盖：情绪周期状态机 / 反身性 / 龙虎榜力量比 / 封板质量 / 利润质量与红旗 /
     估值锚陷阱 / 宏观定位层 / 试错仓位 / 逃顶信号 / L3 闸门集成回归。
"""
from __future__ import annotations

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from strategy import knowledge as KN
from strategy import filters as FLT
from strategy import calibers as C

passed = failed = 0
def ok(cond, msg):
    global passed, failed
    if cond:
        passed += 1
    else:
        failed += 1
        print(f"  ✗ FAIL: {msg}")

# ---------- 1. 情绪周期 ----------
s = KN.sentiment_cycle(91, 0.10, lianban_height=6, lianban_rate=0.65)
ok(s.stage == "高潮" and s.pos_cap == 0.70, f"高潮判定: {s.stage}")
ok(s.allow_da_ban is True, "高潮+连板率65% 允许打板")
s = KN.sentiment_cycle(30, 0.45)
ok(s.stage == "退潮" and s.pos_cap == 0.0, f"退潮判定: {s.stage}")
s = KN.sentiment_cycle(45, 0.20, lianban_height=2, lianban_rate=0.3)
ok(s.stage == "萌芽", f"萌芽判定: {s.stage}")
s = KN.sentiment_cycle(55, 0.15, lianban_height=4, lianban_rate=0.65)
ok(s.stage == "发酵" and s.allow_da_ban, f"发酵判定: {s.stage}")
s = KN.sentiment_cycle(20, 0.25)
ok(s.stage == "见顶", f"涨停萎缩至峰值50%以下 → 见顶: {s.stage}")
s = KN.sentiment_cycle(None, None)
ok(s.stage == "退潮" and "数据缺口" in s.note, "核心数据缺失 → 退潮保守")

# ---------- 2. 反身性 ----------
r = KN.reflexivity(ladder_height_today=6, ladder_height_prev=4,
                   vr_slope_up=True, margin_net3d=12.0, prev_premium=0.02)
ok(r.stage == "强化", f"强化: {r.stage} {r.reasons}")
r = KN.reflexivity(ladder_height_today=3, ladder_height_prev=6,
                   margin_net3d=-8.0, prev_premium=-0.01)
ok(r.stage == "毁灭", f"毁灭: {r.stage}")
r = KN.reflexivity()
ok(r.stage == "中性", "无观测 → 中性")

# ---------- 3. 龙虎榜力量比 ----------
p = KN.lhb_power(buy1=2e8, sell1=0.5e8, buy5_sum=8e8, sell5_sum=3e8,
                 inst_buy=1.2e8, day_amount=9e8, buy2=0.3e8)
ok(p.buy1_sell1 == 4.0 and p.score == 90.0, f"力量比: {p.score}")
ok(any("独大" in x for x in p.risks) is False, "买一占成交22% 未超30% → 无独大预警")
p = KN.lhb_power(buy1=4e8, sell1=1e8, day_amount=9e8, buy2=0.5e8)
ok(any("独大" in x for x in p.risks), "买一占44% > 30% → 独大预警")
ok(p.score < 100, "独大扣分生效")

# ---------- 4. 封板质量 ----------
q = KN.seal_quality(seal_amount=2.2e8, day_amount=9e8, first_seal_time="09:52",
                    reopen_count=1, cancel_ratio_5min=0.1, turnover=0.04, vol_vs_prev5=0.6)
ok(q.score == 100.0 and q.grade == "优质", f"优质板: {q.score} {q.grade}")
q = KN.seal_quality(seal_amount=0.2e8, day_amount=9e8, first_seal_time="14:50",
                    reopen_count=4, cancel_ratio_5min=0.5, turnover=0.3, vol_vs_prev5=2.5)
ok(q.grade == "风险", f"风险板: {q.score} {q.grade}")
ok(any("撤单" in x for x in q.reasons), "撤单风险命中")

# ---------- 5. 利润质量 ----------
pq = KN.profit_quality({"name": "X", "deduct_nonrecurring": -3e7, "parent_net_profit": 5e7})
ok(len(pq.penalties) == 1 and "扣非" in pq.penalties[0], "归母正扣非负 → 减分")
ok(pq.use_deduct_growth is False, "扣非为负不触发口径切换（直接以扣非为准）")
pq = KN.profit_quality({"name": "X", "deduct_nonrecurring": 2e7, "parent_net_profit": 1e8})
ok(pq.use_deduct_growth is True, "扣非/归母 20% < 50% → 增速切扣非口径")
pq = KN.profit_quality({"name": "Y", "net_cash_ratio": 0.3, "minority_loss": True,
                        "sales_cash_ratio": 0.8})
ok(len(pq.red_flags) == 3 and pq.veto_suggest, "三红旗 → 否决级复核")
pq = KN.profit_quality({"name": "Z", "goodwill_ratio": 0.45, "recv_rev_gap": 30})
# v2.3 口径（2026-10-21 对齐）：商誉 + 应收背离 属 5 类红旗中的 2 类 → 触发 veto_suggest，
# 同时仍保留罚分语义（penalties 2 条）。旧断言「不误报红旗」与 v2.3 契约冲突，已按契约更新。
ok(len(pq.penalties) == 2 and pq.veto_suggest, "两红旗 → 否决级复核（v2.3）")
pq = KN.profit_quality({"name": "W", "deduct_nonrecurring": 4.26e9})
ok(not pq.penalties and not pq.red_flags, "扣非为正无异常 → 干净")

# ---------- 6. 估值锚 ----------
a = KN.valuation_anchor("周期", pe_ttm=8, pb=2.0, profit_at_cycle_peak=True)
ok(a.action == "禁止超跌买入" and "周期顶" in (a.trap or ""), "周期顶低PE陷阱")
a = KN.valuation_anchor("周期", pb=1.0, profit_at_cycle_peak=False)
ok(a.action == "正常" and "PB 主导" in a.anchor_desc, "周期底 PB 主导")
a = KN.valuation_anchor("红利", dividend_yield=0.05)
ok("价值区" in a.anchor_desc, "股息率 5% ≥ 4% → 价值区")
a = KN.valuation_anchor("红利", dividend_yield=0.02)
ok("不便宜" in a.anchor_desc, "股息率 2% → 不便宜")
a = KN.valuation_anchor("成长", pe_ttm=45)
ok("PEG" in a.anchor_desc, "成长锚")
a = KN.valuation_anchor(None)
ok("未知" in a.biz_type, "未标注 → 降级说明")

# ---------- 7. 宏观定位层 ----------
m = KN.macro_dashboard({"cpi_core_dir": "回落", "real_rate_dir": "下行",
                        "currency_credit": "宽货币宽信用", "fiscal_cycle": "扩张"})
ok(m.style == "成长/题材双进攻（最高风险偏好）", f"风格指令: {m.style}")
m = KN.macro_dashboard({"cpi_core_dir": "回升", "real_rate_dir": "上行",
                        "currency_credit": "紧货币紧信用", "fiscal_cycle": "收缩"})
ok("高股息防守" in m.style, "双紧 → 防守")
m = KN.macro_dashboard({})
ok(m.labels["通胀"] == "未知" and len(m.missing) == 4, "全缺 → 未知+missing")

# ---------- 8. 试错仓位 + 逃顶 ----------
pp = KN.probe_position(100000, 1000000)
ok(pp.probe_frac == 0.25 and pp.validate_premium == 0.03, "试探 1/4 · 验证 3%")
ok(len(pp.steps) == 4, "四步完整")
e = KN.top_exit_signal([0.05, 0.03, 0.048], close_below_ma20=True)
ok(e.triggered and e.name == "巨阴-反抽-再巨阴", "两次巨阴+破MA20 → 逃顶")
e = KN.top_exit_signal([0.05], close_below_ma20=True)
ok(not e.triggered, "单次巨阴不触发")
e = KN.top_exit_signal([0.02], good_news_open_high_close_red=True)
ok(e.triggered and "高开低走" in e.name, "利好高开低走 → 脆弱信号")

# ---------- 9. L3 闸门集成回归（老 schema 行为不变）----------
row = {"code": "sh600276", "name": "恒瑞医药", "interim_yoy": 0.003,
       "prior_fy_yoy": 0.217, "deduct_nonrecurring": 4.26e9}
g = FLT.gate_fundamental(row)
ok(g.passed, "恒瑞（扣非为正）仍通过")
ok(g.score_penalty == C.GROWTH_PENALTY_SCORE, f"罚分仍为增速减分 {g.score_penalty}")
row_bad = {"code": "sz000000", "name": "假数据", "interim_yoy": 0.5,
           "prior_fy_yoy": 0.6, "deduct_nonrecurring": -1e8, "parent_net_profit": 5e8}
g2 = FLT.gate_fundamental(row_bad)
ok(g2.passed and any("扣非" in w for w in g2.warnings), "归母正扣非负 → 通过但罚分+标注")
ok(g2.score_penalty == C.KNOWLEDGE["扣非为负罚分"], f"扣非罚分 {C.KNOWLEDGE['扣非为负罚分']} 生效")
row_veto = {"code": "sz000001", "name": "雷股", "interim_yoy": 0.5,
            "prior_fy_yoy": 0.6, "net_cash_ratio": 0.2, "minority_loss": True,
            "sales_cash_ratio": 0.6}
g3 = FLT.gate_fundamental(row_veto)
ok(not g3.passed and "科目接力" in g3.reasons[0], "三红旗 → L3 否决级人工复核")

# ---------- 10. 口径版本 ----------
ok(C.CALIBER_VERSION == "v2.3", f"口径版本 {C.CALIBER_VERSION}")
ok(len(C.KNOWLEDGE) >= 30, f"知识阈值表 {len(C.KNOWLEDGE)} 条")

print(f"\nknowledge v2.3 自检：{passed} 通过 / {failed} 失败")
sys.exit(1 if failed else 0)
