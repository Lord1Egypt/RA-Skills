#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""六条已确认口径（caliber v2, 定稿 2026-09-12, 永久生效）

本模块是**唯一口径来源**。任何报告生成、过滤、评分都必须从这里取值，
不得在别处硬编码。口径变更时必须同时：
  1. 修改本文件并升级 CALIBER_VERSION；
  2. 全量重算所有历史结论（口径变更会使结论不可比）；
  3. 在报告首页显式写出当前口径版本。

口径 v2 与 v1 的三点差异（必须记录）：
  * 口径③ 净利润增长率：v1 用**年度**同比 → v2 用**半年**（最新中报年内同比）
  * 口径④ 单年亏损：v1 视为一票否决 → v2 降级为**减分项**（仅连续两年年报亏损才否决）
  * 口径⑥ 新增 **L2.5 基础可交易性校验**独立层（原先混在 L3 一票否决里）
"""

from __future__ import annotations

CALIBER_VERSION = "v2.3"          # v2.3 = v2 六条口径不变 + 知识蒸馏阈值表（2026-09-25）
CALIBER_CONFIRMED_ON = "2026-09-12"   # 六条口径定稿日；v2.3 只增不删，见 KNOWLEDGE

# ---------------------------------------------------------------- v3.0 扩展层（2026-11-11）
# ⚠️ 关键：CALIBER_VERSION 保持 "v2.3" **不变**。六条口径永久生效，
#    一旦改写会让不同日期的结论失去可比性（口径漂移）。v3.0 是叠加在
#    `strategy/v3_ext.py` 的**只读旁路层**：只输出标签 / 乘数 / 告警 / 白名单，
#    不改动本文件任何阈值、不改动四层漏斗硬门槛、不改动情绪五阶段仓位上限。
#    报告展示用 FRAMEWORK_VERSION，口径章节仍标注六条口径 v2.3。
EXTENSION_VERSION = "v3.0"
EXTENSION_CONFIRMED_ON = "2026-11-11"
FRAMEWORK_VERSION = "v3.1"       # v3.1 = v3.0 五模块 + GCCEO 全量整合层（只读映射，不动口径）
EXTENSION_MODULES = (
    "L0_macro_dashboard",        # 16 条宏观规则，只下调不上调
    "strategy_factor_layer",     # 13 条券商策略会因子，只乘 α 预算
    "X_theme_extension",         # 17 个 X- 扩展方向，三层白名单
    "shortline_rules",           # 24 条短线金手只读标签
    "fact_forecast_watermark",   # 事实 / 预测 / 口径差异水印隔离
)
EXTENSION_SOURCE_COUNT = 31      # 新增资料份数（knowledge_distill/new_sources/manifest.json）

# ---------------------------------------------------------------- GCCEO 全量整合层（v3.1, 2026-11-11）
# ⚠️ 关键：本层是叠加在 v3.0 之上的**第二只读旁路层**（strategy/gcceo_ext.py）。
#    GCCEO 是「企业管理能力体系」，映射为研判视角的提问 / 清单 / 风险项 / 叙事脚手架，
#    不作为选股因子。CALIBER_VERSION 仍为 "v2.3"、KNOWLEDGE 45 键、v3 五模块一律不改。
#    GCCEO 层无剔除权、无仓位上调权；gceo.enabled=false 正交回滚，不影响 v3.enabled。
GCCEO_EXT_VERSION = "v3.1"
GCCEO_SOURCE_VERSION = "4.0.0"   # 被整合的 GCCEO 源技能版本
GCCEO_CONFIRMED_ON = "2026-11-11"
GCCEO_MODULES = (
    "gceo_decision_os",          # 五步决策框架 → 研判决策工程
    "gceo_domain_map",           # 十域 91 技能 → 研判视角映射
    "gceo_ib_pe_map",            # 投行私募 A1-A10 → 资本运作映射
    "gceo_global_expansion",     # 出海 G1-G10 → 出海链映射
    "gceo_ai_superpowers",       # AI 超能力 8 模块 → 研判工作台
    "gceo_method_toolbox",       # 16 方法论工具 → 可审计推理链
    "gceo_governance_talent",    # 治理/人才/ESG → 定性尽调清单
    "gceo_risk_radar",           # 地缘/网络/气候风险 → 风险清单增补
    "gceo_narrative",            # 叙事与复盘纪律
    "gceo_watermark",            # 口径差异水印（96 vs 91）
)


def describe_gceo() -> str:
    """GCCEO 整合层摘要，供报告口径章节与框架说明文档引用。"""
    return (
        f"框架版本 {FRAMEWORK_VERSION} = 六条口径 {CALIBER_VERSION}（永久不变）"
        f" + v3.0 只读旁路五模块 + GCCEO {GCCEO_SOURCE_VERSION} 全量整合层 {GCCEO_EXT_VERSION}\n"
        f"  GCCEO 层 = {len(GCCEO_MODULES)} 个只读映射模块：十域 91 技能 / 投行 A1-A10 / "
        f"出海 G1-G10 / AI 超能力 8 / 方法论 16 / 五步决策框架\n"
        f"  定位为「研判视角映射」而非选股因子：只输出标签 / 清单 / 风险提问 / 叙事脚手架，"
        f"无剔除权、无仓位上调权\n"
        f"  技能数【口径差异】：frontmatter 96（含 2026 新增）vs skills.json 91（十域结构口径），"
        f"只取结构口径，绝对值不写阈值\n"
        f"  回滚正交：gceo.enabled=false → v3.0 16 页；v3.enabled=false → v2.3 14 页；互不影响\n"
    )


def describe_extension() -> str:
    """扩展层摘要，供报告口径章节与框架说明文档引用。"""
    return (
        f"框架版本 {FRAMEWORK_VERSION}（六条口径 {CALIBER_VERSION} 永久不变 + "
        f"知识蒸馏扩展层 {EXTENSION_VERSION}，{EXTENSION_CONFIRMED_ON}）\n"
        f"  扩展层 = {len(EXTENSION_MODULES)} 个只读旁路模块，来源 {EXTENSION_SOURCE_COUNT} 份新增资料\n"
        f"  只输出「标签 / 乘数 / 告警 / 白名单」，无剔除权；宏观层只下调、不上调仓位\n"
        f"  事实 / 预测 / 口径差异三类水印隔离；westock 取不到者标「外部数据缺口·仅定性」\n"
        f"  回滚：data.json 顶层 v3.enabled=false 即回到 14 页纯 v2.3 版式\n"
    )

# ---------------------------------------------------------------- 知识蒸馏阈值表（v2.3, 2026-09-25）
# 来源：11 本书蒸馏（knowledge_distill/distilled/*.md），由 strategy/knowledge.py 消费。
# 规则：v2.3 只**增**阈值与检查项，不改动 v2 六条口径的任何判定 —— 过会数量不受影响，
#      升级全部作用于「评分质量 / 风险拦截 / 预判模板」，保证跨期可比。
KNOWLEDGE: dict[str, float] = {
    # 1. 情绪周期（同花顺书 A1/A3/A4）
    "退潮_涨停上限": 40,            # 涨停 <40 家
    "退潮_炸板率下限": 0.40,        # 且炸板率 >40%
    "见顶_涨停峰值参考": 90,        # 峰值参考（可按市场自适应）
    "见顶_涨停萎缩比": 0.5,         # 涨停萎缩到峰值 50% 以下 → 见顶
    "见顶_高度回落前值": 4,         # 连板高度 <4（较高点断层）且连板率低于门槛 → 见顶
    "见顶_接力枯竭连板率": 0.25,    # 连板率 <25% = 接力枯竭（低于此才判见顶，避免误伤萌芽）
    "高潮_最低高度": 5,             # 连板最高 ≥5 板
    "高潮_炸板率上限": 0.30,
    "发酵_涨停下限": 50,
    "发酵_最低高度": 3,
    "打板_连板率门槛": 0.60,        # 连板率 ≥60% 才允许打板（同花顺 A3）
    # 3. 龙虎榜力量比（金手3 A1/A2 + 同花顺 D3/D4）
    "买1卖1_满分档": 2.0,
    "买1卖1_加分档": 1.5,
    "买5卖5_强档": 1.5,
    "机构共识比": 0.10,             # 机构买入/成交额 ≥10% = 共识加分
    "买一独大阈值": 0.30,           # 买一占成交 >30% = 砸盘预警
    "买1买2比阈值": 2.0,
    # 4. 封板质量（同花顺 C4 + 金手3 B2/B4）
    "封单成交比_优质": 0.20,
    "封单成交比_合格": 0.05,
    "封板早时限时": "10:30",
    "撤单风险阈值": 0.30,
    "涨停换手_坚决": 0.05,
    "涨停换手_合格上限": 0.10,
    "缩量板上限": 0.8,              # 涨停日量/前5日均量 ≤0.8 → 缩量板
    "放量分歧下限": 2.0,
    "封板质量_优质线": 70,
    "封板质量_合格线": 40,
    # 5. 利润含金量与造假红旗（穿透财报 + 简明财务 + 穿透叙事 R11）
    "扣非归母比下限": 0.50,         # 扣非/归母 <50% → 增速判定切扣非口径
    "扣非为负罚分": 10.0,           # 归母正而扣非负 → 减分（不否决，口径④精神）
    "净现比红旗": 0.5,              # 经营现金流/归母净利 <0.5 → 强红旗
    "销售收现率下限": 1.0,          # 销售收现率 <1 且走低 → 强红旗
    "应收营收背离pp": 20.0,
    "存货营收背离pp": 20.0,
    "商誉净资产比警戒": 0.30,
    "补助依赖度警戒": 0.30,
    "金融利润占比警戒": 0.30,
    "红旗否决线": 2,                # ≥2 条强红旗 → 一票否决级人工复核
    # 6. 估值锚（穿透估值 A4/B1/B2）
    "周期底PB上限": 1.2,
    "周期PB区间上限": 2.5,
    "红利股息率价值线": 0.04,
    # 8. 试错仓位（索罗斯 R5）与逃顶（凌鹏 C3/C4）
    "试探仓比例": 0.25,
    "试探仓总资金上限": 0.02,
    "验证溢价线": 0.03,
    "单题材风险上限": 0.02,
    "巨阴跌幅": 0.045,              # 单日跌幅 >4.5% 记巨阴
}

# ---------------------------------------------------------------- 口径①
# 国企央企背景 = **偏好项**，不是硬门槛。
# v1 曾把它当门槛，导致「民企 → 0 只」的假警报。
SOE_BACKGROUND_IS_GATE = False
SOE_BACKGROUND_IS_PREFERENCE = True
SOE_SCORE_BONUS = 6.0          # 命中控股股东/实控人为国企央企时的加分

# ---------------------------------------------------------------- 口径②
# 新兴科技成长优先：在同等技术形态下，新兴产业/科技成长股优先。
EMERGING_TECH_FIRST = True
EMERGING_TECH_BONUS = 8.0      # 命中六大新兴支柱 / 六大未来产业时的加分

# ---------------------------------------------------------------- 口径③
# 净利润增长率采用**半年口径**（最新中报年内同比），不是年度同比。
PROFIT_GROWTH_CALIBER = "half_year"      # "half_year" | "annual"
PROFIT_GROWTH_FIELD = "NPParentCompanyYOY_Q"   # 单季同比；中报累计同比用 NPParentCompanyYOY
PROFIT_GROWTH_FIELD_INTERIM = "NPParentCompanyYOY"

# 增速红线（量化）：
#   硬线：中报同比 <= 0  → 直接排除
#   减分项：中报同比 > 0 但 < 上一年度增速的 50% → 重大减分
GROWTH_HARD_LINE = 0.0
GROWTH_PENALTY_RELATIVE_LINE = 0.50      # 框架自定的默认值，非市场共识
GROWTH_PENALTY_SCORE = 15.0

# ---------------------------------------------------------------- 口径④
# 单年亏损 = 减分项；连续两年年报亏损 = 一票否决。
SINGLE_YEAR_LOSS_IS_VETO = False
TWO_CONSECUTIVE_LOSSES_IS_VETO = True
SINGLE_YEAR_LOSS_SCORE = 10.0

# ---------------------------------------------------------------- 口径⑤
# 「链」形态主题（如「算力网」「机器人产业链」）默认**跳过 L1 否决权**，
# 行业层只做定性描述，不因行业分位高而直接否决其中的个股。
CHAIN_THEME_SKIPS_L1_VETO = True

# 「链」形态主题名单（可扩展）
#
# ⚠️ v2.2 修正（2026-09-16）：原名单按「XX产业链」命名撰写，与实际在用的
#    18 方向 / AI 链 / 电力绿电 跟踪池命名对不上 —— 实测 18 个方向里只有
#    「六张网-3算力网」「六张网-4新一代通信网」2 个能命中，「新兴产业-1新能源汽车」
#    这类名字不含「新能源车产业链」，于是口径⑤在第 3~18 个方向上形同虚设：
#    产业主题股被行业分位（中位 59%~81%）整片挡在 L2 之外。
#    现按实际命名补齐前缀词，使口径⑤真正生效。
CHAIN_THEMES = (
    "算力网", "新一代通信网", "机器人链", "低空经济链",
    "半导体产业链", "新能源车产业链", "锂电池产业链", "光伏产业链",
    # —— 与在用的跟踪池命名对齐（18 方向 / AI 链 / 电力绿电）——
    "六张网", "新兴产业", "未来产业",
    "光模块", "PCB", "算力设备", "IDC", "大模型", "电力/绿电",
)

# ---------------------------------------------------------------- 口径⑥
# 新增「基础可交易性校验」独立层 L2.5，位置在 L2 与 L3 之间。
TRADABILITY_LAYER = "L2.5"

# 可交易性否决条件（命中任一即剔除，且**不计入** L3 一票否决统计）
NOTRADE_RULES = (
    "已退市 / 退市整理期",
    "ST / *ST",
    "停牌",
    "净资产为负（PB < 0）",
    "上市未满 60 个交易日",
    "近 20 交易日均成交额 < 3000 万元（流动性不足）",
)

# ---------------------------------------------------------------- 层定义
LAYERS = ("L1行业", "L2个股", "L2.5可交易", "L3基本面")

# 分层技术阈值
RANK_LOW_THRESHOLD = 25.0     # 历史分位低于 25% 视为「超低位」
VR_THRESHOLD = 1.0            # 额比 >= 1.0 视为「放量」
DISPERSION_ALERT = 60.0       # 个股分位离散度 >= 60pp = 内部严重分化

# 口径变更使结论不可比 —— 报告必须报告的敏感度
SENSITIVITY_MUST_REPORT = True
SENSITIVITY_TOLERANCE_STOCKS = 1   # ±1 只以内算可接受，但仍须写明


def describe() -> str:
    """人类可读的口径摘要，供报告首页直接引用。"""
    return (
        f"口径版本 {CALIBER_VERSION}（六条口径 {CALIBER_CONFIRMED_ON} 定稿；"
        f"v2.3 增补知识蒸馏阈值表 2026-09-25）\n"
        f"  ① 国企央企背景：{'硬门槛' if SOE_BACKGROUND_IS_GATE else '偏好项（非门槛）'}\n"
        f"  ② 产业偏好：{'新兴科技成长优先' if EMERGING_TECH_FIRST else '无偏好'}\n"
        f"  ③ 净利润增长率：{'半年口径（最新中报年内同比）' if PROFIT_GROWTH_CALIBER == 'half_year' else '年度口径'}\n"
        f"     硬线 中报同比 <= {GROWTH_HARD_LINE:.0%} → 排除；"
        f"减分 中报同比 > 0 但 < 上年度的 {GROWTH_PENALTY_RELATIVE_LINE:.0%}\n"
        f"  ④ 单年亏损：{'一票否决' if SINGLE_YEAR_LOSS_IS_VETO else '减分项'}；"
        f"连续两年年报亏损 = {'否决' if TWO_CONSECUTIVE_LOSSES_IS_VETO else '不否决'}\n"
        f"  ⑤ 「链」形态主题：{'跳过 L1 否决权（行业层仅定性）' if CHAIN_THEME_SKIPS_L1_VETO else '不跳过'}\n"
        f"  ⑥ 基础可交易性校验：作为独立层 {TRADABILITY_LAYER}（位于 L2 与 L3 之间）\n"
    )


def is_chain_theme(name: str) -> bool:
    """判断主题名是否属于「链」形态（口径⑤）。"""
    if not name:
        return False
    return any(k in name for k in CHAIN_THEMES)


if __name__ == "__main__":
    print(describe())
