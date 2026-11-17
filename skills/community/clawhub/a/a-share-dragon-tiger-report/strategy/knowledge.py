#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""知识蒸馏规则库（knowledge v2.3，2026-09-25）

来源：11 本投资类书籍蒸馏（同花顺短线实战 / 短线金手3涨停狙击 / 邹佩轩三部曲
穿透财报·穿透估值·穿透叙事 / 简明财务分析·故事的力量 / 凌鹏周期估值与人性 /
索罗斯投资哲学 / AI通胀与武器 / 李奇霖宏观经济数据分析手册）。

蒸馏全文与逐条出处见知识库：
  knowledge_distill/distilled/*.md（工作区）

设计原则（与 filters.py 一致）：
  * 纯函数、无 IO、无全局状态，便于 test_formulas.py 自检；
  * 所有阈值集中在 calibers.K（知识蒸馏阈值表），此处不硬编码；
  * 缺数据的判据**跳过而非猜测**（返回 None 或降级为中性），绝不编造；
  * 输出全部是「可复核的数值判定 + 理由字符串」，供报告逐条列示。

八个子模块（对应八条升级主线）：
  1. sentiment_cycle     情绪周期五阶段状态机（同花顺 A1-A4）
  2. reflexivity         反身性强化/毁灭标签（索罗斯 R1-R2）
  3. lhb_power           龙虎榜力量比三维（短线金手3 A1-A4 + 同花顺 D3-D5）
  4. seal_quality        封板质量分（同花顺 C4 + 金手3 B2/B4）
  5. profit_quality      利润含金量与造假红旗（穿透财报 A-K + 简明财务 A-C）
  6. valuation_anchor    商业模式估值锚与周期顶低PE陷阱（穿透估值 A4/B1/B2）
  7. macro_dashboard     宏观定位层四标签（宏观手册 + AI通胀与武器 R9）
  8. probe_position      试错仓位四步法（索罗斯 R5）+ 逃顶信号（凌鹏 C3/C4）
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from . import calibers as C

K = C.KNOWLEDGE  # 知识蒸馏阈值表（v2.3）


# ==================================================================
# 1. 情绪周期五阶段状态机（同花顺书 A1/A3/A4）
# ==================================================================
STAGES = ("萌芽", "发酵", "高潮", "见顶", "退潮")

# 阶段 → (推荐模式, 仓位上限占 α 预算比)
STAGE_PLAYBOOK: dict[str, dict[str, Any]] = {
    "萌芽": {"mode": "低吸/超跌反弹", "pos_cap": 0.30},
    "发酵": {"mode": "打板+龙头战法", "pos_cap": 0.60},
    "高潮": {"mode": "半路追涨（仅已确立龙头可打板）", "pos_cap": 0.70},
    "见顶": {"mode": "减少操作、不追高，可低吸偏离主线的低位股", "pos_cap": 0.20},
    "退潮": {"mode": "观望（一切操作风险倍增）", "pos_cap": 0.00},
}


@dataclass
class SentimentStage:
    stage: str
    mode: str
    pos_cap: float
    reasons: list[str] = field(default_factory=list)
    allow_da_ban: bool = False   # 是否允许打板
    note: str = ""


def sentiment_cycle(
    limit_up_count: int | None,
    broken_rate: float | None,
    lianban_height: int | None = None,
    lianban_rate: float | None = None,
    prev_premium: float | None = None,
    prev_stage: str | None = None,
) -> SentimentStage:
    """情绪周期五阶段判定。

    输入（缺任一项则降级为保守判定，不猜测）：
      limit_up_count   涨停家数
      broken_rate      炸板率（0-1）
      lianban_height   连板最高高度（板数）
      lianban_rate     连板率 = 连板家数/涨停家数（0-1）
      prev_premium     昨日涨停股今日平均溢价（0-1，可负）
      prev_stage       上一期阶段（状态机连续性用）

    判定顺序（自保守向激进）：退潮 → 见顶 → 高潮 → 发酵 → 萌芽。
    打板许可：发酵/高潮期且连板率 ≥ 阈值（默认 0.60）才允许。
    """
    reasons: list[str] = []

    # ---- 数据完整性：核心两要素缺失 → 退潮期保守处理
    if limit_up_count is None or broken_rate is None:
        return SentimentStage("退潮", STAGE_PLAYBOOK["退潮"]["mode"], 0.0,
                              reasons=["涨停家数或炸板率缺失 → 数据不足，按退潮期最保守处理"],
                              note="数据缺口")
    lu, br = int(limit_up_count), float(broken_rate)
    if lianban_rate is not None:
        reasons.append(f"涨停 {lu} 家 / 炸板率 {br:.0%} / 连板率 {float(lianban_rate):.0%}")
    else:
        reasons.append(f"涨停 {lu} 家 / 炸板率 {br:.0%}")

    # ---- 退潮：人气股炸板潮 / 涨停极少且炸板率高
    if lu < K["退潮_涨停上限"] and br > K["退潮_炸板率下限"]:
        return SentimentStage("退潮", STAGE_PLAYBOOK["退潮"]["mode"], 0.0, reasons,
                              note="涨停极少且炸板率高 → 退潮")

    # ---- 见顶：涨停缩水过半 / 高度断层 / 昨日溢价为负且涨停偏少 / 炸板率失控
    peak = K.get("见顶_涨停峰值参考", 90)
    if (lu < peak * K["见顶_涨停萎缩比"]) or (prev_premium is not None and prev_premium < 0 and lu < peak * 0.6):
        reasons.append(f"涨停 {lu} < 峰值参考 {peak} 的 {K['见顶_涨停萎缩比']:.0%}"
                       + (f"；昨日涨停溢价 {prev_premium:+.1%}" if prev_premium is not None else ""))
        return SentimentStage("见顶", STAGE_PLAYBOOK["见顶"]["mode"],
                              STAGE_PLAYBOOK["见顶"]["pos_cap"], reasons)
    # 炸板率失控 → 见顶（2026-10-19 补：此前 br 只参与「退潮」与「高潮」判定，
    # 中间地带无兜底，出现「涨停 50+ 但炸板率 42%、连板率 12%」仍被判发酵并允许打板）。
    if br > K["退潮_炸板率下限"]:
        reasons.append(f"炸板率 {br:.0%} > {K['退潮_炸板率下限']:.0%}（封板失败率高，接力赚钱效应差）")
        return SentimentStage("见顶", STAGE_PLAYBOOK["见顶"]["mode"],
                              STAGE_PLAYBOOK["见顶"]["pos_cap"], reasons,
                              note="涨停尚可但炸板率失控 → 见顶")

    # ---- 见顶（2026-10-20 补）：接力结构断层
    # 此前「见顶」只判涨停家数的萎缩比，完全没看**高度与连板率**。于是出现
    # 「涨停 86 家看似还行、但最高板 4→3 断板、连板率仅 19%」时，会直接落到
    # 「发酵」分支（条件为 lu≥50 且 height≥3），把已经断掉的接力梯队判成在发酵。
    # 收窄口径：高度断层 **且** 连板率低于「接力枯竭」门槛（0.25，远低于打板门槛
    # 0.60）才算见顶 —— 否则会把「萌芽期（涨停尚可、接力未成型）」误判进来。
    _h_prev = K.get("见顶_高度回落前值", 4)
    if (lianban_height is not None and lianban_height < _h_prev
            and lianban_rate is not None
            and float(lianban_rate) < K["见顶_接力枯竭连板率"]):
        reasons.append(f"高度 {lianban_height} < {_h_prev}（接力断层）；连板率 "
                       f"{float(lianban_rate):.0%} < {K['见顶_接力枯竭连板率']:.0%}（接力枯竭）")
        return SentimentStage("见顶", STAGE_PLAYBOOK["见顶"]["mode"],
                              STAGE_PLAYBOOK["见顶"]["pos_cap"], reasons,
                              note="高度断层且连板率枯竭 → 见顶（涨停家数是假象）")

    # ---- 高潮：高度 ≥ 阈值（默认 5 板）且炸板率低
    if lianban_height is not None and lianban_height >= K["高潮_最低高度"] and br < K["高潮_炸板率上限"]:
        reasons.append(f"连板高度 {lianban_height} ≥ {K['高潮_最低高度']} 且炸板率 {br:.0%} 受控")
        allow = lianban_rate is None or float(lianban_rate) >= K["打板_连板率门槛"]
        return SentimentStage("高潮", STAGE_PLAYBOOK["高潮"]["mode"],
                              STAGE_PLAYBOOK["高潮"]["pos_cap"], reasons, allow_da_ban=allow)

    # ---- 发酵：涨停放量 + 接力效应在
    # 打板许可必须同时满足连板率门槛；此前发酵分支硬编码 allow_da_ban=True，
    # 连板率 12%（门槛 60%）也照样放行 —— 2026-10-19 修正。
    if lu >= K["发酵_涨停下限"] and (
        (lianban_rate is not None and float(lianban_rate) >= K["打板_连板率门槛"])
        or (lianban_height is not None and lianban_height >= K["发酵_最低高度"])
    ):
        _allow = lianban_rate is not None and float(lianban_rate) >= K["打板_连板率门槛"]
        reasons.append(f"涨停 {lu} ≥ {K['发酵_涨停下限']} 且接力效应在（高度/连板率达标）"
                       + ("" if _allow else
                          f"；连板率 {float(lianban_rate):.0%} < {K['打板_连板率门槛']:.0%} → 禁止打板"))
        return SentimentStage("发酵", STAGE_PLAYBOOK["发酵"]["mode"],
                              STAGE_PLAYBOOK["发酵"]["pos_cap"], reasons, allow_da_ban=_allow)

    # ---- 萌芽：其余情形（有涨停但接力未成型）
    reasons.append("涨停存在但连板梯队/连板率未成型 → 萌芽期做低吸")
    return SentimentStage("萌芽", STAGE_PLAYBOOK["萌芽"]["mode"],
                          STAGE_PLAYBOOK["萌芽"]["pos_cap"], reasons)


# ==================================================================
# 2. 反身性标签（索罗斯 R1/R2：自我强化 vs 自我毁灭）
# ==================================================================
@dataclass
class ReflexivityLabel:
    stage: str          # "强化" | "毁灭" | "中性"
    reasons: list[str] = field(default_factory=list)


def reflexivity(
    ladder_height_today: int | None = None,
    ladder_height_prev: int | None = None,
    vr_slope_up: bool | None = None,
    margin_net3d: float | None = None,      # 融资余额 3 日净流向（亿元，可负）
    prev_premium: float | None = None,      # 昨日涨停平均溢价
) -> ReflexivityLabel:
    """反身性阶段标签：涨停梯队抬升 + 额比上行 + 融资净流入 = 强化；
    高度回落/炸板恶化 + 融资转流出 / 昨日溢价转负 = 毁灭。"""
    r: list[str] = []
    strengthen_votes, destroy_votes = 0, 0

    if ladder_height_today is not None and ladder_height_prev is not None:
        if ladder_height_today > ladder_height_prev:
            strengthen_votes += 1
            r.append(f"梯队高度 {ladder_height_prev}→{ladder_height_today} 抬升")
        elif ladder_height_today < ladder_height_prev:
            destroy_votes += 1
            r.append(f"梯队高度 {ladder_height_prev}→{ladder_height_today} 回落")
    if vr_slope_up is True:
        strengthen_votes += 1
        r.append("额比斜率上行")
    if margin_net3d is not None:
        if margin_net3d > 0:
            strengthen_votes += 1
            r.append(f"融资余额 3 日净流入 {margin_net3d:+.1f} 亿")
        else:
            destroy_votes += 1
            r.append(f"融资余额 3 日净流出 {margin_net3d:+.1f} 亿")
    if prev_premium is not None:
        if prev_premium > 0:
            strengthen_votes += 1
            r.append(f"昨日涨停溢价 {prev_premium:+.1%}")
        else:
            destroy_votes += 1
            r.append(f"昨日涨停溢价 {prev_premium:+.1%}（转负）")

    if strengthen_votes >= 2 and strengthen_votes > destroy_votes:
        return ReflexivityLabel("强化", r)
    if destroy_votes >= 2 and destroy_votes > strengthen_votes:
        return ReflexivityLabel("毁灭", r)
    return ReflexivityLabel("中性", r or ["观测项不足，维持中性"])


# ==================================================================
# 3. 龙虎榜力量比（金手3 A1/A2/A3 + 同花顺 D3/D4）
# ==================================================================
@dataclass
class LhbPower:
    buy1_sell1: float | None = None
    buy5_sell5: float | None = None
    inst_buy_ratio: float | None = None
    buy1_share: float | None = None        # 买一占成交额比
    score: float = 0.0                     # 0-100
    risks: list[str] = field(default_factory=list)
    bonuses: list[str] = field(default_factory=list)


def lhb_power(
    buy1: float | None, sell1: float | None,
    buy5_sum: float | None = None, sell5_sum: float | None = None,
    inst_buy: float | None = None, day_amount: float | None = None,
    buy2: float | None = None,
) -> LhbPower:
    """龙虎榜力量比。金额单位一致即可（元或亿元）。

    判据：
      买1/卖1 ≥2 满分档、≥1.5 加分档、<1 减分；
      买5合计/卖5合计 ≥1.5 为强；
      机构买入/成交额 ≥10% = 共识加分；
      买一占成交额 >30% 或 买1/买2 >2 = 独大砸盘预警。
    """
    p = LhbPower()
    if buy1 and sell1 and sell1 > 0:
        p.buy1_sell1 = round(buy1 / sell1, 3)
        if p.buy1_sell1 >= K["买1卖1_满分档"]:
            p.score += 40
            p.bonuses.append(f"买1/卖1 = {p.buy1_sell1:.2f} ≥ {K['买1卖1_满分档']}（主力大本营在买方）")
        elif p.buy1_sell1 >= K["买1卖1_加分档"]:
            p.score += 25
            p.bonuses.append(f"买1/卖1 = {p.buy1_sell1:.2f}（买方占优）")
        else:
            p.score -= 15
            p.risks.append(f"买1/卖1 = {p.buy1_sell1:.2f} < 1（卖一压过买一）")
    if buy5_sum and sell5_sum and sell5_sum > 0:
        p.buy5_sell5 = round(buy5_sum / sell5_sum, 3)
        if p.buy5_sell5 >= K["买5卖5_强档"]:
            p.score += 30
            p.bonuses.append(f"买5/卖5 = {p.buy5_sell5:.2f} ≥ {K['买5卖5_强档']}")
        elif p.buy5_sell5 >= 1.0:
            p.score += 15
        else:
            p.score -= 15
            p.risks.append(f"买5/卖5 = {p.buy5_sell5:.2f} < 1（卖方前五占优）")
    if inst_buy and day_amount and day_amount > 0:
        p.inst_buy_ratio = round(inst_buy / day_amount, 4)
        if p.inst_buy_ratio >= K["机构共识比"]:
            p.score += 30
            p.bonuses.append(f"机构买入占成交 {p.inst_buy_ratio:.1%} ≥ {K['机构共识比']:.0%}（中线资金共识）")
    if buy1 and day_amount and day_amount > 0:
        p.buy1_share = round(buy1 / day_amount, 4)
        if p.buy1_share > K["买一独大阈值"]:
            p.score -= 20
            p.risks.append(f"买一占成交 {p.buy1_share:.1%} > {K['买一独大阈值']:.0%}（单一席位独大，次日砸盘风险）")
        if buy2 and buy2 > 0 and buy1 / buy2 > K["买1买2比阈值"]:
            p.score -= 10
            p.risks.append(f"买1/买2 = {buy1/buy2:.1f} > {K['买1买2比阈值']}（头部集中）")
    p.score = round(max(0.0, min(100.0, p.score)), 1)
    return p


# ==================================================================
# 4. 封板质量分（同花顺 C4 + 金手3 B2/B4）
# ==================================================================
@dataclass
class SealQuality:
    score: float                  # 0-100
    grade: str                    # 优质 / 合格 / 风险
    reasons: list[str] = field(default_factory=list)


def seal_quality(
    seal_amount: float | None = None,
    day_amount: float | None = None,
    first_seal_time: str | None = None,     # "HH:MM"
    reopen_count: int | None = None,
    cancel_ratio_5min: float | None = None,  # 尾盘/关键 5 分钟撤单占比
    turnover: float | None = None,           # 涨停日换手率 0-1
    vol_vs_prev5: float | None = None,       # 涨停日量 / 前 5 日均量
) -> SealQuality:
    """封板质量三维度：封单/成交额 ≥20% 优质下限；10:30 前封板；
    开板 ≤2 次；5 分钟撤单 >30% 为风险板；换手 ≤10% 合格 ≤5% 坚决；缩量板次日连板概率上调。"""
    score, reasons = 0.0, []
    if seal_amount and day_amount and day_amount > 0:
        ratio = seal_amount / day_amount
        if ratio >= K["封单成交比_优质"]:
            score += 35
            reasons.append(f"封单/成交额 = {ratio:.0%} ≥ {K['封单成交比_优质']:.0%}（极强）")
        elif ratio >= K["封单成交比_合格"]:
            score += 20
            reasons.append(f"封单/成交额 = {ratio:.0%}（合格）")
        else:
            reasons.append(f"封单/成交额 = {ratio:.0%} 偏弱（< {K['封单成交比_合格']:.0%}）")
    if first_seal_time:
        early = first_seal_time <= K["封板早时限时"]
        score += 20 if early else 0
        reasons.append(f"首次封板 {first_seal_time}（{'早板' if early else '非早板'}）")
    if reopen_count is not None:
        if reopen_count <= 2:
            score += 20
            reasons.append(f"开板 {reopen_count} 次 ≤ 2")
        else:
            score -= 15
            reasons.append(f"开板 {reopen_count} 次 > 2（反复炸板）")
    if cancel_ratio_5min is not None and cancel_ratio_5min > K["撤单风险阈值"]:
        score -= 25
        reasons.append(f"5 分钟撤单 {cancel_ratio_5min:.0%} > {K['撤单风险阈值']:.0%}（撤单风险板）")
    if turnover is not None:
        t = float(turnover)
        if t <= K["涨停换手_坚决"]:
            score += 15
            reasons.append(f"涨停换手 {t:.1%} ≤ {K['涨停换手_坚决']:.0%}（封板坚决）")
        elif t > K["涨停换手_合格上限"]:
            score -= 10
            reasons.append(f"涨停换手 {t:.1%} 过高（> {K['涨停换手_合格上限']:.0%}，分歧大）")
    if vol_vs_prev5 is not None:
        if float(vol_vs_prev5) <= K["缩量板上限"]:
            score += 10
            reasons.append(f"量比前值 {vol_vs_prev5:.2f} ≤ {K['缩量板上限']}（缩量板 → 次日连板概率上调）")
        elif float(vol_vs_prev5) >= K["放量分歧下限"]:
            reasons.append(f"量比前值 {vol_vs_prev5:.2f} ≥ {K['放量分歧下限']}（放量板 → 分歧/卖压上调）")
    score = round(max(0.0, min(100.0, score)), 1)
    grade = "优质" if score >= K["封板质量_优质线"] else ("风险" if score < K["封板质量_合格线"] else "合格")
    return SealQuality(score, grade, reasons)


# ==================================================================
# 5. 利润含金量与造假红旗（穿透财报 + 简明财务 + 穿透叙事 R11）
# ==================================================================
@dataclass
class ProfitQuality:
    red_flags: list[str] = field(default_factory=list)     # 强红旗（造假嫌疑级）
    penalties: list[str] = field(default_factory=list)     # 减分项
    notes: list[str] = field(default_factory=list)
    use_deduct_growth: bool = False                         # 增速判定是否应切换扣非口径
    veto_suggest: bool = False                              # 建议 L3 一票否决级人工复核


def profit_quality(row: Mapping[str, Any]) -> ProfitQuality:
    """利润质量检查。字段全部可选——缺哪个跳哪个，绝不编造。

    已知字段（data.json 既有）：deduct_nonrecurring（扣非归母，元）。
    可选扩展字段（后续管线补采后自动生效）：
      net_cash_ratio          经营现金流净额/归母净利润（近 2 年最低值）
      sales_cash_ratio        销售收现率（销售商品收到现金/营收）
      recv_rev_gap            应收增速 − 营收增速（pp）
      inv_rev_gap             存货增速 − 营收增速（pp）
      goodwill_ratio          商誉/净资产
      minority_loss           True = 归母为正但合并净利为负（少数股东扛亏）
      gov_subsidy_ratio       其他收益/利润总额
      invest_income_ratio     (投资收益+公允价值变动)/净利润
    """
    q = ProfitQuality()
    name = str(row.get("name", ""))

    # ---- 扣非口径（易，现有数据即可）
    parent = row.get("parent_net_profit")     # 归母净利润（元），可选
    ded = row.get("deduct_nonrecurring")
    if ded is not None and parent:
        p, d = float(parent), float(ded)
        if p > 0 and d < 0:
            q.penalties.append(
                f"{name} 归母 {p/1e8:+.2f} 亿为正但扣非 {d/1e8:+.2f} 亿为负 —— 扭亏靠非经常性损益，"
                f"按口径以扣非为准（−{K['扣非为负罚分']} 分）")
            # v2.3 升级点 3 · 红旗 ⑤：扣非为负但归母为正
            q.red_flags.append("扣非为负但归母为正（非经常性损益撑利润）")
        elif p > 0 and d / p < K["扣非归母比下限"]:
            q.use_deduct_growth = True
            q.notes.append(f"{name} 扣非/归母 = {d/p:.0%} < {K['扣非归母比下限']:.0%} → "
                           f"增速红线判定应切换到扣非口径")
            # v2.3 升级点 3：扣非占比过低同属「利润含金量」红旗（与框架 F3 口径一致）
            q.red_flags.append(f"扣非占归母 <{K['扣非归母比下限']:.0%}（利润含金量不足）")
    elif ded is not None and float(ded) < 0:
        q.penalties.append(f"{name} 扣非归母为负（{float(ded)/1e8:+.2f} 亿）→ 盈利质量存疑")

    # ---- 净现比（穿透财报 #1 / 简明 #4）
    # v2.3：契约要求「连续两期 <0.5」才算强红旗；仅单期可观测时按单期记红旗（保守，
    # 但不满足「连续」语义，故不会单独构成否决）。
    ncr = row.get("net_cash_ratio")
    ncr_p = row.get("net_cash_ratio_prev")
    if ncr is not None and float(ncr) < K["净现比红旗"]:
        if ncr_p is not None and float(ncr_p) < K["净现比红旗"]:
            q.red_flags.append(
                f"净现比连续两期 <{K['净现比红旗']}（{float(ncr):.2f}/{float(ncr_p):.2f}，利润缺现金背书）")
        else:
            q.red_flags.append(f"净现比 {float(ncr):.2f} < {K['净现比红旗']}（利润缺现金背书）")

    # ---- 销售收现率（简明 #8：预收型模式蓄水枯竭）
    scr = row.get("sales_cash_ratio")
    if scr is not None and float(scr) < K["销售收现率下限"]:
        q.red_flags.append(f"销售收现率 {float(scr):.2f} < {K['销售收现率下限']}（收入含金量不足）")

    # ---- 应收/存货与营收背离（穿透财报 #6/#10）
    rr = row.get("recv_rev_gap")
    if rr is not None and float(rr) > K["应收营收背离pp"]:
        q.penalties.append(f"应收增速超营收 {float(rr):.0f}pp（信用政策恶化/压货冲收入嫌疑）")
        q.red_flags.append(f"应收增速超营收 {float(rr):.0f}pp")
    ir = row.get("inv_rev_gap")
    if ir is not None and float(ir) > K["存货营收背离pp"]:
        q.penalties.append(f"存货增速超营收 {float(ir):.0f}pp（跌价风险）")
        q.red_flags.append(f"存货增速超营收 {float(ir):.0f}pp")

    # ---- 商誉（穿透财报 #18/#19）
    gw = row.get("goodwill_ratio")
    if gw is not None and float(gw) > K["商誉净资产比警戒"]:
        q.penalties.append(f"商誉/净资产 {float(gw):.0%} > {K['商誉净资产比警戒']:.0%}（悬顶之剑；"
                           f"若当年已减值，次年连环减值概率 >50%）")
        q.red_flags.append(f"商誉/净资产 {float(gw):.0%} > {K['商誉净资产比警戒']:.0%}")

    # ---- 少数股东扛亏（穿透财报 #26 / 简明 #6，强红旗）
    if row.get("minority_loss"):
        q.red_flags.append("归母净利润为正但合并净利润为负（少数股东扛亏，暴风模式）")

    # ---- 政府补助依赖（穿透财报 #23）
    gs = row.get("gov_subsidy_ratio")
    if gs is not None and float(gs) > K["补助依赖度警戒"]:
        q.penalties.append(f"其他收益/利润总额 {float(gs):.0%}（补助依赖）")

    # ---- 金融利润占比（简明 #2/#3）
    ii = row.get("invest_income_ratio")
    if ii is not None and float(ii) > K["金融利润占比警戒"]:
        q.penalties.append(f"(投资收益+公允价值变动)/净利润 {float(ii):.0%} —— 利润主要来自理财/投资，"
                           f"估值逻辑应从 PE 切换 PB")

    # ---- 科目接力综合扫描（穿透财报 #32）：≥2 强红旗 → 建议否决级人工复核
    if len(q.red_flags) >= K["红旗否决线"]:
        q.veto_suggest = True
        q.notes.append(f"强红旗 {len(q.red_flags)} 条 ≥ {K['红旗否决线']}（科目接力嫌疑）→ 建议一票否决级人工复核")
    return q


# ==================================================================
# 6. 商业模式估值锚与周期顶陷阱（穿透估值 A4/B1/B2 + 凌鹏 B4）
# ==================================================================
BIZ_TYPES = ("周期", "成长", "红利")


@dataclass
class AnchorCheck:
    biz_type: str
    anchor_desc: str
    trap: str | None = None       # 触发的估值陷阱说明
    action: str = "正常"           # 正常 / 警惕 / 禁止超跌买入


def valuation_anchor(
    biz_type: str | None,
    pe_ttm: float | None = None,
    pb: float | None = None,
    dividend_yield: float | None = None,
    profit_at_cycle_peak: bool | None = None,   # 盈利处于周期顶（毛利率90分位等）
) -> AnchorCheck:
    """按商业模式选择估值锚，并拦截两类最危险陷阱：
      ① 周期顶低 PE（PE 最低时恰是卖点）；
      ② 用 PE 去套弱商业模式。"""
    bt = biz_type if biz_type in BIZ_TYPES else None
    if bt is None:
        return AnchorCheck("未知", "商业模式未标注 → 按成长锚 PE 参考比较，跨类比较不作为判据")

    if bt == "周期":
        if pb is not None and pb < K["周期底PB上限"]:
            if profit_at_cycle_peak:
                return AnchorCheck("周期", f"PB {pb:.2f} < {K['周期底PB上限']}（净资产重置成本附近）",
                                   trap="盈利处于周期顶 → 低 PE 是卖点不是买点（E 虚高）",
                                   action="警惕")
            return AnchorCheck("周期", f"PB {pb:.2f} < {K['周期底PB上限']} → 周期底部特征，PB 主导、PE 降权")
        if pe_ttm is not None and profit_at_cycle_peak:
            return AnchorCheck("周期", f"PE {pe_ttm:.1f}",
                               trap="周期顶低 PE 陷阱：盈利在顶 → PE 失真，不给超跌评分",
                               action="禁止超跌买入")
        return AnchorCheck("周期", f"PB {pb if pb is not None else '缺失'} 为锚（区间 "
                                   f"{K['周期底PB上限']}~{K['周期PB区间上限']}），PE 仅作对照")

    if bt == "红利":
        if dividend_yield is not None:
            if dividend_yield >= K["红利股息率价值线"]:
                return AnchorCheck("红利", f"股息率 {dividend_yield:.1%} ≥ {K['红利股息率价值线']:.0%} → 价值区（股息率锚）")
            return AnchorCheck("红利", f"股息率 {dividend_yield:.1%} < {K['红利股息率价值线']:.0%} → 股息率锚下不便宜")
        return AnchorCheck("红利", "股息率缺失 → 无法用红利锚判定")

    # 成长
    if pe_ttm is not None:
        return AnchorCheck("成长", f"PE_TTM {pe_ttm:.1f}（PEG ≤1 合理 / ≥2 泡沫警戒，需一致预期增速）")
    return AnchorCheck("成长", "PE 缺失 → 成长锚无法判定")


# ==================================================================
# 7. 宏观定位层四标签（宏观手册 + AI通胀与武器 R9）
# ==================================================================
MACRO_LABELS = ("通胀", "实际利率", "货币信用", "财政")

# 标签组合 → 风格指令
STYLE_DIRECTIVE: dict[tuple[str, str, str, str], str] = {
    ("回落", "下行", "宽货币宽信用", "扩张"): "成长/题材双进攻（最高风险偏好）",
    ("回落", "下行", "宽货币紧信用", "收缩"): "成长估值环境（分母驱动，注意波动）",
    ("回升", "上行", "紧货币宽信用", "扩张"): "顺周期/价值盈利驱动",
    ("回升", "上行", "紧货币紧信用", "收缩"): "只做题材脉冲 + 高股息防守（最低风险偏好）",
}


@dataclass
class MacroPosition:
    labels: dict[str, str]
    style: str
    missing: list[str] = field(default_factory=list)


def macro_dashboard(ind: Mapping[str, Any]) -> MacroPosition:
    """宏观定位层：4 个枚举标签 → 风格指令。

    期望输入键（缺项记入 missing，该轴降级为「未知」）：
      cpi_core_dir      核心 CPI 方向："回落"|"回升"|"平"
      real_rate_dir     实际利率 120 日斜率方向："下行"|"上行"|"平"
      currency_credit   货币信用象限："宽货币宽信用"|"宽货币紧信用"|"紧货币宽信用"|"紧货币紧信用"
      fiscal_cycle      财政周期："扩张"|"收缩"
    """
    keys = {"cpi_core_dir": "通胀", "real_rate_dir": "实际利率",
            "currency_credit": "货币信用", "fiscal_cycle": "财政"}
    labels, missing = {}, []
    for k, label in keys.items():
        v = ind.get(k)
        if v in ("回落", "回升", "下行", "上行", "平", "扩张", "收缩") or (
                isinstance(v, str) and v.startswith("宽") or
                isinstance(v, str) and v.startswith("紧")):
            labels[label] = str(v)
        else:
            labels[label] = "未知"
            missing.append(k)
    style = STYLE_DIRECTIVE.get(
        (labels["通胀"], labels["实际利率"], labels["货币信用"], labels["财政"]), "")
    if not style:
        style = "标签不全 → 维持中性配置，等关键标签补齐（缺：" + "、".join(missing) + "）" if missing \
            else "组合无历史强映射 → 中性"
    return MacroPosition(labels, style, missing)


# ==================================================================
# 8. 试错仓位四步法（索罗斯 R5）+ 逃顶信号（凌鹏 C3/C4）
# ==================================================================
@dataclass
class ProbePlan:
    probe_frac: float          # 试探仓占计划仓位比
    probe_cap_of_equity: float # 试探仓占总资金上限
    validate_premium: float    # 验证判据：次日溢价 ≥ 此值
    add_frac: float            # 验证后加至
    max_theme_risk: float      # 单题材最大风险占总资金
    steps: list[str] = field(default_factory=list)


def probe_position(plan_notional: float, equity: float) -> ProbePlan:
    """试错四步：1/4 试探 → 溢价 ≥3% 验证 → 金字塔加码 → 证伪清零。
    单题材最大风险锁定在总资金 2%。"""
    return ProbePlan(
        probe_frac=K["试探仓比例"],
        probe_cap_of_equity=K["试探仓总资金上限"],
        validate_premium=K["验证溢价线"],
        add_frac=1.0 - K["试探仓比例"],
        max_theme_risk=K["单题材风险上限"],
        steps=[
            f"① 试探：先建计划仓位的 {K['试探仓比例']:.0%}（且 ≤ 总资金 {K['试探仓总资金上限']:.0%}）",
            f"② 验证：次日龙头溢价 ≥ {K['验证溢价线']:.0%} 且板块涨停家数不缩 → 加仓；否则认赔退出",
            f"③ 加码：再次验证（第 3 日仍强）→ 加至满配（金字塔，不加倒金字塔）",
            f"④ 退出：任一日出现炸板潮/龙头跌停 → 无条件清零；单题材最大风险 ≤ 总资金 {K['单题材风险上限']:.0%}",
        ],
    )


@dataclass
class ExitSignal:
    triggered: bool
    name: str = ""
    reasons: list[str] = field(default_factory=list)


def top_exit_signal(
    big_drop_days: Sequence[float],     # 近 20 日单日跌幅序列（正数表示跌幅，如 0.05=5%）
    close_below_ma20: bool | None = None,
    good_news_open_high_close_red: bool | None = None,  # 利好日高开低走收绿
) -> ExitSignal:
    """逃顶信号（凌鹏 C3/C4）：
      ① 巨阴-反抽-再巨阴：20 日内 2 次单日跌幅 >4.5%，且第二次巨阴收盘 < MA20；
      ② 事件反应背离：重大利好日高开低走翻绿 = 熊尾/顶部脆弱特征（风控升一级）。"""
    big = [d for d in big_drop_days if d > K["巨阴跌幅"]]
    if len(big) >= 2 and close_below_ma20:
        return ExitSignal(True, "巨阴-反抽-再巨阴",
                          [f"20 日内出现 {len(big)} 次巨阴（>{K['巨阴跌幅']:.1%}）",
                           "第二次巨阴收盘 < MA20 → 必须大幅减仓"])
    if good_news_open_high_close_red:
        return ExitSignal(True, "利好高开低走（脆弱）",
                          ["重大利好日高开低走翻绿 → 顶部脆弱特征，风控升一级"])
    return ExitSignal(False)
