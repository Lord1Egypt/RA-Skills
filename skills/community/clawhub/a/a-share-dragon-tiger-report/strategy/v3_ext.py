#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v3.0 知识蒸馏扩展层（2026-11-11 落地）· 非破坏性叠加

来源：knowledge_distill/
  new_sources/   31 份新增资料纯文本（manifest.json，ok=31，3,016,766 字符）
  distilled_v3/  4 组蒸馏结论（宏观与增长 / 券商策略 / 短线 7 册 / 产业主题与财务核验）

═══════════════════════════ 六条设计契约（不可协商）═══════════════════════════
1. 六条口径 v2.3 的阈值、字段、判定结果一律不改；L1→L2→L2.5→L3 四层漏斗的
   输入成分与硬阈值（3 年分位 ≤25% / 额比 ≥1.0× / L2.5 剔除 / L3 半年归母同比）
   一律不改；情绪五阶段 30/60/70/20/0% 仓位上限一律不改。
2. 本模块只输出「标签 / 乘数 / 告警 / 白名单」，不产生任何剔除动作，
   不参与 scoring / funnel / predictions 的数值计算。
3. 宏观层只下调、不上调：alpha 乘数 ∈ (0, 1.0]，宏观标签永远是仓位天花板的
   折减系数，禁止因「宽松加码 / 活水」预测上调仓位（2027 数字全是预测）。
4. 事实 / 预测 / 口径差异三类水印隔离：研报 2027 数字只作分档边界的「预测锚」，
   不生成买卖信号、不进入回溯验收，不污染六条口径的历史绩效统计。
5. 频率对齐：宏观月/季频，非发布日沿用上次值；westock 取不到的项一律标
   「外部数据缺口 · 仅定性」，不得写成可计算判据。
6. 全部扩展可逐条停用（V3_SWITCHES），一键回滚到纯 v2.3 输出。

接入点：data.json 顶层可选字段 `v3`。渲染器只读该字段，不 import 本模块，
保证 v2.3 生成器对本模块零依赖。
"""
from __future__ import annotations

import math
from typing import Any

# ─────────────────────────────── 版本与开关 ───────────────────────────────
EXT_VERSION = "v3.0"
EXT_CONFIRMED_ON = "2026-11-11"
CALIBER_VERSION_UNCHANGED = "v2.3"
OVERLAY_ONLY = True

V3_SWITCHES: dict[str, bool] = {
    "L0_macro_dashboard": True,
    "strategy_factor_layer": True,
    "X_theme_extension": True,
    "shortline_rules": True,
    "fact_forecast_watermark": True,
}

SOURCE_GROUPS: dict[str, dict] = {
    "宏观": {"n": 5, "chars": 650790, "tag": ["2027 年度展望", "2027 宏观形势", "2026Q3", "中国2049", "超常增长"]},
    "策略": {"n": 4, "chars": 135556, "tag": ["中信建投 2027 资本市场策略会 HTML/PDF/PPTX/XLSX"]},
    "主题": {"n": 8, "chars": 1099775, "tag": ["国资国企改革", "深圳创投", "双向投资", "数字贸易",
                                             "矿业全球化", "长三角未来独角兽", "全球私营公司", "上海 100 项首创"]},
    "资金": {"n": 3, "chars": 139790, "tag": ["租赁业调查", "银行理财季报", "00 后妈妈消费"]},
    "方法": {"n": 3, "chars": 630334, "tag": ["数据化决策", "达尔文投资知识", "WorkBuddy 提效"]},
    "财务核验": {"n": 1, "chars": 66783, "tag": ["税收风险管理（与利润质量红旗对齐）"]},
    "短线战法": {"n": 7, "chars": 293738, "tag": ["短线金手 1—7"]},
}

# ─────────────────────────── 保守闸门 / 乘数空间 ───────────────────────────
DOWNGRADE_ONLY = True
ALPHA_MULT_ALLOWED = (0.8, 0.9, 0.95, 1.0)
FACTOR_MULT_ALLOWED = (0.8, 0.9, 0.95, 1.0, 1.05, 1.1, 1.15, 1.2)
POSITION_CAP_BASE = {"萌芽": 0.30, "启动": 0.30, "发酵": 0.60,
                     "高潮": 0.70, "见顶": 0.20, "退潮": 0.00}
EVENT_BONUS_CAP = 0.20
THEME_DECAY_DAYS = 20
ALPHA_BUCKETS = {"核心": (0.50, 0.60), "成长": (0.30, 0.40), "种子": (0.05, 0.10)}

# ───────────────────── 预测锚登记簿（水印：预测，不是事实）────────────────────
MACRO_ANCHORS: list[dict] = [
    {"k": "2027 GDP 目标", "v": "≈4.5%", "src": "浙商 2027 展望", "kind": "预测"},
    {"k": "2027 CPI / PPI", "v": "+0.3% / +1.2%", "src": "浙商", "kind": "预测"},
    {"k": "2027 末 社融/M2/M1/信贷", "v": "6.2% / 6.2% / 4.0% / 3.7%", "src": "浙商", "kind": "预测"},
    {"k": "2027 降准 / 降息", "v": "50BP / 20BP", "src": "浙商", "kind": "预测"},
    {"k": "2027 新增专项债", "v": "4.7 万亿", "src": "浙商", "kind": "预测"},
    {"k": "10Y 国债破 1.5%", "v": "<1.5%", "src": "浙商", "kind": "预测"},
    {"k": "人民币兑美元", "v": "6.3–6.4", "src": "浙商", "kind": "预测"},
    {"k": "2027 AI 出口贡献回落", "v": "3–5pct（悲观 7–10pct）", "src": "申万 2027 展望", "kind": "预测"},
    {"k": "三情景概率", "v": "基准 55% / 乐观 20% / 压力 25%", "src": "中信建投", "kind": "主观概率"},
    {"k": "2027E 净利增速", "v": "海光 +58.5% / 沪电 +62.0% / 金山办公 -18.9%", "src": "中信建投附表", "kind": "一致预期"},
    {"k": "央企十五五数智化投入", "v": "有望突破 2 万亿", "src": "毕马威", "kind": "预测"},
    {"k": "2030 数据中心耗电/资本开支", "v": "翻番 / 31.6 万亿美元", "src": "普华永道引第三方", "kind": "预测"},
]
NO_INDEX_TARGET_NOTE = "两份 2027 宏观展望均未给出 A 股指数点位区间预测 —— 日报宏观模块不设指数目标位。"

FACT_ANCHORS: list[dict] = [
    {"k": "2026-08 PPI-CPI 剪刀差", "v": "+3.0pct（PPI 3.8% / CPI 0.8%）", "src": "北大汇丰 2026Q3", "kind": "事实"},
    {"k": "2026 前三季广义财政支出", "v": "约 -3.5%；债发行占额度 50.6%", "src": "申万 2027 展望", "kind": "事实"},
    {"k": "2026 截至 9 月出口累计同比", "v": "+22.1%；AI 相关商品贡献 10.7pct", "src": "申万 2027 展望", "kind": "事实"},
    {"k": "央企改革 88%/20+3+10%", "v": "88% 营收归集 20 个重点行业；主业 ≤3；非主业投资 ≤10%", "src": "毕马威", "kind": "事实"},
    {"k": "36 种关键矿产目录", "v": "能源 6 / 金属 25 / 非金属 5（2026-06 实施条例）", "src": "毕马威矿业", "kind": "事实"},
    {"k": "2025 数字贸易顺差", "v": "连续 7 年顺差；出口同比 +10.2% vs 进口 +1.0%", "src": "商务部", "kind": "事实"},
]

# ─────────────────────────── L0 宏观定位层规则 ───────────────────────────
MACRO_RULES: list[dict] = [
    {"id": "M01", "name": "M1-M2 流动性活化剪刀差", "key": ["m1_yoy", "m2_yoy"],
     "rule": "Δ=M1−M2；>0 活化；−3≤Δ≤0 边际改善；<−3 活化不足", "avail": "westock", "hook": "宏观定位 / α 乘数"},
    {"id": "M02", "name": "社融-信贷增速差", "key": ["social_fin_yoy", "loan_yoy"],
     "rule": "Δ≥2pct 政府债主导；0~2 中性；<0 信贷主导", "avail": "westock", "hook": "行业主线排序"},
    {"id": "M03", "name": "PPI-CPI 剪刀差收敛", "key": ["ppi_yoy", "cpi_yoy"],
     "rule": "G 由正转负或 3 月均值收窄 ≥1pct → 出清行业利润修复", "avail": "westock", "hook": "行业主线 / α 乘数"},
    {"id": "M04", "name": "低通胀约束下的政策空间", "key": ["cpi_yoy", "core_cpi_yoy"],
     "rule": "CPI<1% 且核心≤1.5% → 宽松空间打开；CPI≥2% → 收紧风险", "avail": "westock", "hook": "仓位上限修正"},
    {"id": "M05", "name": "降准降息事件计数", "key": ["ease_events_3m"],
     "rule": "滚动 3 月 ≥2 次宽松事件 → 宽松加码（事件表人工补录）", "avail": "gap", "hook": "宏观定位 / 次日预判"},
    {"id": "M06", "name": "10Y 国债破位", "key": ["cn10y"],
     "rule": "<1.5% 资产荒防御占优；1.5–2.0 中性；>2.0 再通胀", "avail": "westock", "hook": "α 乘数（高股息）"},
    {"id": "M07", "name": "红利-成长相对强弱", "key": ["dividend_ret20", "growth_ret20"],
     "rule": "R=中证红利20日−创业板20日；>3pct 上半场防御；<−3pct 下半场成长", "avail": "westock", "hook": "行业主线 / α 乘数"},
    {"id": "M08", "name": "指数波动率风险临界点", "key": ["hs300_vol20", "hs300_vol250_p90", "index_pct_1d"],
     "rule": "20 日实现波动 > 250 日 90% 分位，或单日跌幅 >2% → 风险暴露", "avail": "westock", "hook": "风险清单 / 仓位"},
    {"id": "M09", "name": "人民币汇率与结汇流向", "key": ["usdcny_3m"],
     "rule": "连续 3 月升值或 <6.5 → 结汇流入；破 7.0 → 资本外流压力", "avail": "gap", "hook": "风险清单"},
    {"id": "M10", "name": "美元指数与 10Y 美债双高", "key": ["dxy", "us10y"],
     "rule": "DXY>100 且 US10Y>4.5% → 高利率巨浪；US10Y<4.0% → 宽松阀门重启", "avail": "gap", "hook": "风险清单 / 仓位"},
    {"id": "M11", "name": "出口增速退坡与 AI 拉动收敛", "key": ["export_yoy", "export_yoy_prev"],
     "rule": "自 >20% 回落 ≥5pct 或跌破 10% → 外需退坡（出口链降权）", "avail": "westock", "hook": "行业主线 / 次日预判"},
    {"id": "M12", "name": "反内卷九大行业出清受益", "key": ["nine_sector_rank20", "nine_sector_vr"],
     "rule": "20 日涨幅进全市场前 30% 分位 且 板块额比 >1.2 → 出清受益", "avail": "westock", "hook": "行业主线 / α 乘数"},
    {"id": "M13", "name": "服务-商品消费剪刀差", "key": ["service_retail_yoy", "goods_retail_yoy"],
     "rule": "Δ>3pct → 服务消费占优（文旅/医疗提权）", "avail": "westock", "hook": "行业主线排序"},
    {"id": "M14", "name": "高技术制造 K 型分化", "key": ["tech_sector_rank20", "build_sector_rank20"],
     "rule": "计算机通信电子分位 >70% 且超额 >3pct → 新动能占优", "avail": "westock", "hook": "行业主线 / α 乘数"},
    {"id": "M15", "name": "财政脉冲", "key": ["fiscal_exp_yoy"],
     "rule": "公共财政支出累计同比 >0（或专项债同比 >0）→ 财政加码；仍 <0 → 审慎", "avail": "westock", "hook": "宏观定位 / 六张网"},
    {"id": "M16", "name": "宏观事件窗与仓位乘数", "key": ["macro_event_window", "sentiment_stage", "macro_tag"],
     "rule": "T+1 有发布窗 → α×0.9；宏观风险标签 × 情绪见顶/退潮 → 仓位再 ×0.8", "avail": "partial",
     "hook": "仓位上限 / 次日预判 / 风险清单"},
]

# ─────────────────────────── 券商策略会因子层 ───────────────────────────
STRATEGY_RULES: list[dict] = [
    {"id": "S01", "name": "四象限主线打分卡", "mult": 1.2, "note": "高景气进攻 +2 / 困境反转 +1 / 红利防御 +1 / 主题弹性 +0.5（20 日衰减）", "avail": "static"},
    {"id": "S02", "name": "参会热度加权", "mult": 1.2, "note": "板块参会占比 ≥7% → ×1.2；≥5% → ×1.1；<2% 不加权", "avail": "static"},
    {"id": "S03", "name": "高股息防御集群", "mult": 0.9, "note": "股息率 ≥4.0% 打红利底仓标签；3.5–4.0% ×0.95", "avail": "westock"},
    {"id": "S04", "name": "高景气成长兑现", "mult": 1.2, "note": "归母同比 >50% 或评分 ≥80 → ×1.15；>100% 且 ≥80 → ×1.20 封顶", "avail": "westock"},
    {"id": "S05", "name": "2027E 一致预期验证", "mult": 0.9, "note": "负增长 → 预期下修告警 ×0.9，不剔除；预测项带水印", "avail": "gap"},
    {"id": "S06", "name": "三层面 α 预算分桶", "mult": 1.0, "note": "核心 50–60% / 成长 30–40% / 种子 5–10%；种子 >10% 告警", "avail": "static"},
    {"id": "S07", "name": "三情景概率开关", "mult": 0.8, "note": "55/20/25 主观概率仅作风险开关，不单独触发调仓", "avail": "gap"},
    {"id": "S08", "name": "五大观察变量失效告警", "mult": 0.8, "note": "任一项命中 → 对应主线 ×0.8 + 风险清单新增", "avail": "gap"},
    {"id": "S09", "name": "AI 兑现链条分层与扩散过热", "mult": 0.9, "note": "算力1.0/智能体0.8/应用0.7/未来0.6；应用层涨停集中且算力净流出 → 告警", "avail": "westock"},
    {"id": "S10", "name": "政策催化窗口时效衰减", "mult": 1.15, "note": "事件 ±5 日 ×1.15，线性衰减至第 20 交易日归零", "avail": "gap"},
    {"id": "S11", "name": "红利—成长风格切换", "mult": 1.0, "note": "成长池连续 3 日净流出且红利净流入 → 次日预判标「切向防御」", "avail": "westock"},
    {"id": "S12", "name": "L1 后估值分位兼容校验", "mult": 0.9, "note": "不改 L1 门槛；已过 L1 且估值分位 >75% → 排序 ×0.9 并标透支", "avail": "westock"},
    {"id": "S13", "name": "分红率制度底线 / 科技盈利兑现", "mult": 1.1, "note": "分红率 ≥40% +0.5；科技板块 L3 之上加分 ×1.1（不改 L3 原判据）", "avail": "westock"},
]
QUADRANT = {
    "高景气·进攻": "国产半导体设备 / AI 算力与应用 / 创新药出海 BD / 具身智能机器人 / 军工",
    "困境反转·弹性": "化工 / 火电公用 / 白酒 / 航运 / 光伏链（周期底部）",
    "红利防御·底仓": "REITs / 银行 / 高股息消费 / 公用事业 / 运营商 / 央国企",
    "主题弹性·期权": "核聚变高温超导 / 类脑智能 / 生物制造 / AI 投研金融科技 / 物理 AI",
}

# ─────────────────── 短线金手 7 册：24 条只读规则标签 ───────────────────
SHORTLINE_RULES: list[dict] = [
    {"id": "R01", "g": "A 封板质量", "p": "P2", "src": "shortline_3", "name": "涨停日换手率 ≤10%", "key": "limitup_turnover", "kind": "明确规则"},
    {"id": "R02", "g": "A 封板质量", "p": "P2", "src": "shortline_3/5", "name": "缩量板加分 / 放量 ≥2× 判分歧", "key": "vol_ratio", "kind": "经验数值"},
    {"id": "R03", "g": "A 封板质量", "p": "P2/P5", "src": "shortline_2/5", "name": "封板 ≤10:30 为早板，13:00 后逐档扣分", "key": "seal_time", "kind": "明确+经验"},
    {"id": "R04", "g": "A 封板质量", "p": "P2", "src": "shortline_1-7", "name": "封单额/成交额比（书籍无阈值，按分位定档）", "key": "seal_amount_ratio", "kind": "补缺"},
    {"id": "R05", "g": "A 封板质量", "p": "P2/P3", "src": "shortline_1/2", "name": "买一 ≥ 卖一 2 倍；机构席位 ≥3 且合计 ≥1000 万", "key": "lhb_b1s1", "kind": "经验数值"},
    {"id": "R06", "g": "A 封板质量", "p": "P5/P6", "src": "shortline_3/5/7", "name": "回封加分 / 反复开板判筹码松散", "key": "reopen_count", "kind": "明确规则"},
    {"id": "R07", "g": "A 封板质量", "p": "P2", "src": "shortline_3", "name": "涨停后 10 日不破板价（中期确认，不参与当日打分）", "key": "hold_days_above", "kind": "经验数值"},
    {"id": "R08", "g": "B 打板许可", "p": "P5", "src": "shortline_2", "name": "9:25 与 9:40 双榜前 10 交集", "key": "auction_double_top10", "kind": "明确规则"},
    {"id": "R09", "g": "B 打板许可", "p": "P5", "src": "shortline_2", "name": "高开四档 <2% / 2–4% / 4–7% / >7%", "key": "open_gap", "kind": "明确规则"},
    {"id": "R10", "g": "B 打板许可", "p": "P5", "src": "shortline_2", "name": "集合竞价巨量八档（2019 股本口径，需无量纲重标定）", "key": "auction_vol", "kind": "经验数值·待重标定"},
    {"id": "R11", "g": "B 打板许可", "p": "P5", "src": "shortline_2", "name": "竞价选涨停五项前置（波段 <25% / 高开 ≥2% / 巨量 / 不破均价 / 均线多头）", "key": "precheck5", "kind": "明确规则"},
    {"id": "R12", "g": "B 打板许可", "p": "P5", "src": "shortline_3", "name": "涨幅 ≥9% 备买、必须真涨停、只追板块首板龙头", "key": "trigger", "kind": "明确规则"},
    {"id": "R13", "g": "B 打板许可", "p": "P5/P6", "src": "shortline_2/3", "name": "流通盘 ≤10 亿股、排除 ST 与高动态 PE", "key": "float_shares", "kind": "明确规则·待重标定"},
    {"id": "R14", "g": "B 打板许可", "p": "P1/P5", "src": "shortline_2", "name": "大盘斜率 <45% 可小仓、>60% 禁止打板；牛市 ≥8 成 / 熊市 ≤3 成", "key": "index_slope", "kind": "明确规则"},
    {"id": "R15", "g": "C 次日溢价", "p": "P4", "src": "shortline_2/3", "name": "次日开盘 0~3% 为可接力区（两册互证）", "key": "next_open_pct", "kind": "明确规则"},
    {"id": "R16", "g": "C 次日溢价", "p": "P4", "src": "shortline_5/7", "name": "次日高开兑现；地天板次日 ≥-6% 即算强", "key": "next_open_pct2", "kind": "经验数值"},
    {"id": "R17", "g": "C 次日溢价", "p": "P2/P4/P6", "src": "shortline_3", "name": "三外有三：3 板附近追、≥30% 空间、破第 2 板价止损", "key": "lianban_height", "kind": "明确规则"},
    {"id": "R18", "g": "C 次日溢价", "p": "P4/P6", "src": "shortline_7", "name": "5 日 ≥3 板、波段 ≥30%，回踩 0.382/0.5 买、破 10 日线卖", "key": "pullback", "kind": "明确规则"},
    {"id": "R19", "g": "C 次日溢价", "p": "P4", "src": "shortline_7", "name": "斐波那契 3/5/8/13/21/34 日变盘窗（8/13 最稳）", "key": "fib_window", "kind": "明确规则"},
    {"id": "R20", "g": "D 分时承接", "p": "P5", "src": "shortline_2/5", "name": "回调至均价线下 1–2% 买点；全程站上均价线为强", "key": "vwap_dev", "kind": "明确+经验"},
    {"id": "R21", "g": "D 分时承接", "p": "P5", "src": "shortline_3", "name": "14:30 后真上攻；30°→45–60° 放量攻击；角度 >80° 易抛压", "key": "intraday_angle", "kind": "明确规则"},
    {"id": "R22", "g": "D 分时承接", "p": "P5/P6", "src": "shortline_7", "name": "9:20 前竞价量/涨幅全部列为无效信号（时间闸门）", "key": "auction_before_920", "kind": "明确规则·口径补缺"},
    {"id": "R23", "g": "E 风险止损", "p": "P6", "src": "shortline_2/3", "name": "亏损 3% 必须止损；破涨停前收盘价 / 第 2 板价止损", "key": "stop_loss", "kind": "明确规则"},
    {"id": "R24", "g": "E 风险止损", "p": "P3/P6", "src": "shortline_2/3/7", "name": "涨幅 >70% 后量价+MACD 背离=赶顶；机构占成交 25–43% 且处反弹途中=假机构", "key": "lhb_fake_inst", "kind": "经验数值"},
]

# 书籍侧阈值校准建议：只登记，不覆盖 KNOWLEDGE 现有键。
KNOWLEDGE_BOOK_SUGGEST: dict[str, dict] = {
    "涨停换手_坚决 / 合格上限": {"now": "5% / 10%", "suggest": "10% / 15%（≥20% 判分歧）", "basis": "金手3 战法29", "status": "两册互证，建议回测后采信"},
    "封板早时限时": {"now": "10:30", "suggest": "≤10:30 早板；13:00 后逐档扣分；14:30 后标弱势", "basis": "金手2/5", "status": "建议回测后采信"},
    "验证溢价线": {"now": "0.03", "suggest": "0~3% 可接力区；地天板次日 ≥-6% 即算强", "basis": "金手2/3", "status": "与现值一致，仅补区间"},
    "巨阴跌幅": {"now": "0.045", "suggest": "大阴 ≥3.6%（中阴 1.6–3.5%）", "basis": "金手7 K线波动分档", "status": "仅登记，回测前不覆盖"},
    "缩量板上限 / 放量分歧下限": {"now": "0.8 / 2.0", "suggest": "维持，按成交量历史分位标定", "basis": "金手3/5", "status": "仅登记"},
    "买1卖1_满分档": {"now": "2.0", "suggest": "维持 2.0；补机构席位 ≥3 且合计 ≥1000 万", "basis": "金手1/2", "status": "仅补条件，不改数值"},
    "撤单风险阈值": {"now": "0.30", "suggest": "改为时间闸门：9:20 前竞价量全部不计入封单意愿", "basis": "金手7 交易所规则", "status": "口径补缺，需单独开关"},
    "封单成交比_优质 / 合格": {"now": "0.20 / 0.05", "suggest": "不改键；用封单额÷成交额分位数定档", "basis": "7 册均无比值", "status": "书籍侧缺口，需自行标定"},
}

# ──────────────────── X- 主题扩展层（三层白名单准入）────────────────────
X_THEME_EXT: list[dict] = [
    {"name": "央企重组与三个集中", "tier": "A", "kw": "央企重组/专业化整合/无偿划转/两非两资", "src": "毕马威国资改革"},
    {"name": "央企数智化 / 智能工厂", "tier": "A", "kw": "智能工厂梯度培育/财务数智化/工业互联网", "src": "毕马威国资改革"},
    {"name": "九大战新 + 六大未来产业（7 个 X- 子标签）", "tier": "A/B", "kw": "集成电路/生物医药/具身智能/脑机接口/6G/生物制造/氢能核聚变", "src": "毕马威+长三角榜单"},
    {"name": "X-关键矿产 36 种目录", "tier": "B", "kw": "稀土/钨/锑/锗/镓/铟/锂/钴/镍/铜/萤石/磷/石墨", "src": "毕马威矿业全球化"},
    {"name": "X-矿业全球化 / 资源+产业+基建出海", "tier": "B", "kw": "海外矿权/可换股债券/刚果金铜钴/印尼镍园", "src": "毕马威矿业全球化"},
    {"name": "数字贸易 / 跨境电商", "tier": "A/B", "kw": "全托管/海外仓/综试区 8 批 178 个/市场采购", "src": "商务部数字贸易"},
    {"name": "X-数据要素 / 数据跨境", "tier": "B", "kw": "10 地负面清单/国际数据加工贸易/数据交易所/可信数据空间", "src": "商务部数字贸易"},
    {"name": "X-数字文化 / 游戏网剧出海", "tier": "B", "kw": "游戏出海/网文网剧/数字文创/文化出口", "src": "商务部数字贸易实践篇"},
    {"name": "商业航天 / 低空经济", "tier": "A", "kw": "高光谱遥感/无人机/空天数据/低空经济链接力", "src": "商务部+毕马威"},
    {"name": "智能经济四赛道 / 工业智能体", "tier": "A", "kw": "AI 模型算法/算力云/芯片智能硬件/智能装备机器人/灯塔工厂", "src": "毕马威长三角榜单"},
    {"name": "X-创新药 BD / 技术出海", "tier": "A/B", "kw": "License-out/BD 交易/联合共创/开源模型", "src": "普华永道双向投资"},
    {"name": "X-绿电 / 绿色算力 / 出海产能", "tier": "A/B", "kw": "绿电直连/绿证/PPA/Token 出海/数据中心/海外建厂", "src": "普华永道双向投资"},
    {"name": "创投 / 专精特新 / 独角兽密度", "tier": "A/B", "kw": "20+8 集群/CVC/S 基金/深港跨境创投", "src": "北大汇丰深圳创投"},
    {"name": "特色服务出口基地 / 数字贸易示范区", "tier": "B", "kw": "国家数字服务/文化/地理信息/中医药服务出口基地", "src": "商务部实践篇 19 案例"},
    {"name": "长三角未来独角兽 30 家（影子股锚点）", "tier": "C", "kw": "非上市，仅影子股映射；每家 ≤3 只且须校验上市主体", "src": "毕马威长三角榜单"},
    {"name": "全球私营 65 家（BofA）", "tier": "C", "kw": "非上市/海外，不入可交易池；仅产业链映射", "src": "BofA private 65"},
    {"name": "上海 100 项首创（制度型事件）", "tier": "C", "kw": "2018 年历史资料，仅制度复刻事件标签，不参与景气打分", "src": "上海 100 项首创"},
]
WHITELIST_TIERS = {
    "A": "可交易层：A/H 上市且校验通过 → 允许参与个股分位/离散度计算（本期不回写主表）",
    "B": "事件标签层：只做新闻/主题命中与影子股映射，不参与分位数值",
    "C": "纯定性层：非上市主体/历史制度事件，仅文字标签，严禁混入 70 只代表个股",
}
GAPS_REGISTER = [
    "集合竞价逐笔委托与撤单明细 / 9:25 竞价量能八档（手数）",
    "封单额精确值、开板与回封次数、分时逐笔大单、板块内联动相关性",
    "MACD/KDJ 指标值、题材热度分、2027E 一致预期净利增速与目标价",
    "美元指数、10Y 美债、10Y 国债收益率、全球央行政策与地缘事件",
    "一级市场融资笔数/金额、AI 相关商品出口贡献细分、企业级 EBIT 影响率",
    "宏观发布日历、政策事件日历、36 种目录品种级库存/开工率、行业级 PPI",
    "降准降息公告事件表、主业项数与非主业投资占比（监管口径）",
]


def _num(v: Any, default: float | None = None) -> float | None:
    if v is None:
        return default
    try:
        f = float(v)
        return f if math.isfinite(f) else default
    except (TypeError, ValueError):
        return default


def _present(snap: dict, keys: list[str]) -> bool:
    return all(_num(snap.get(k)) is not None for k in keys)


def _closest(v: float, allowed: tuple[float, ...], ceiling: float = 1.0) -> float:
    v = min(max(float(v), min(allowed)), ceiling)
    return min(allowed, key=lambda x: abs(x - v))


# ─────────────────────────── L0 宏观定位层 ───────────────────────────
def macro_dashboard(ctx: dict, snapshot: dict | None = None,
                    prev_overlay: dict | None = None) -> dict:
    """L0：只输出标签 / α 折减系数 / 先验 / 告警，绝不改写仓位基准与漏斗。"""
    snap = dict(snapshot or {})
    prev = dict(prev_overlay or {})
    computed, qualitative, gaps, alerts, proxies = [], [], [], [], []
    mult, tag = 1.0, "中性"

    if _present(snap, ["m1_yoy", "m2_yoy"]):
        d = _num(snap["m1_yoy"]) - _num(snap["m2_yoy"])
        st = "活化" if d > 0 else ("边际改善" if d >= -3.0 else "活化不足/收缩")
        computed.append({"id": "M01", "v": f"Δ={d:+.1f}pct", "tag": st})
        if d > 0:
            tag = "下半场活水"
    if _present(snap, ["social_fin_yoy", "loan_yoy"]):
        d = _num(snap["social_fin_yoy"]) - _num(snap["loan_yoy"])
        computed.append({"id": "M02", "v": f"Δ={d:+.1f}pct",
                         "tag": "政府债主导" if d >= 2 else ("中性" if d >= 0 else "信贷主导")})
    if _present(snap, ["ppi_yoy", "cpi_yoy"]):
        g = _num(snap["ppi_yoy"]) - _num(snap["cpi_yoy"])
        computed.append({"id": "M03", "v": f"G={g:+.1f}pct",
                         "tag": "出清行业利润修复" if g <= 0 else "剪刀差仍为正"})
    if _present(snap, ["dividend_ret20", "growth_ret20"]):
        r = _num(snap["dividend_ret20"]) - _num(snap["growth_ret20"])
        st = "上半场·红利防御占优" if r > 3 else ("下半场·成长占优" if r < -3 else "震荡中性")
        computed.append({"id": "M07", "v": f"R={r:+.1f}pct", "tag": st})
        if r > 3:
            tag = "上半场防御"
    if _present(snap, ["hs300_vol20", "hs300_vol250_p90"]):
        v20, p90 = _num(snap["hs300_vol20"]), _num(snap["hs300_vol250_p90"])
        hit = v20 > p90 or (_num(snap.get("index_pct_1d")) or 0) < -2.0
        computed.append({"id": "M08", "v": f"vol20={v20:.2f} / p90={p90:.2f}",
                         "tag": "风险暴露" if hit else "波动正常"})
        if hit:
            tag, mult = "风险暴露/上半场", mult * 0.9
            alerts.append("指数波动率越过 250 日 90% 分位 → 宏观与情绪共振向下，仅折减 α，不改写情绪阶段")
    if _present(snap, ["export_yoy"]):
        ey, ep = _num(snap["export_yoy"]), _num(snap.get("export_yoy_prev"))
        decl = (ep is not None and ep > 20 and ep - ey >= 5) or ey < 10
        computed.append({"id": "M11", "v": f"出口同比 {ey:+.1f}%",
                         "tag": "外需退坡" if decl else "外需仍强"})
        if decl:
            alerts.append("出口链降权（仅行业主线排序，不剔除成分）")

    if _present(snap, ["cpi_yoy", "core_cpi_yoy"]):
        c, core = _num(snap["cpi_yoy"]), _num(snap["core_cpi_yoy"])
        st = ("物价约束弱、宽松空间打开" if c < 1 and core <= 1.5
              else ("政策收紧风险" if c >= 2 else "物价约束中等"))
        computed.append({"id": "M04", "v": f"CPI {c:.1f}% / 核心 {core:.1f}%", "tag": st})
    if _present(snap, ["cn10y"]):
        y = _num(snap["cn10y"])
        st = "资产荒、防御占优" if y < 1.5 else ("中性" if y <= 2.0 else "再通胀")
        computed.append({"id": "M06", "v": f"10Y 国债 {y:.4f}%", "tag": st})
        if y < 1.5:
            alerts.append("10Y 国债破 1.5% → 高股息权重提权（仅 α 乘数，不改仓位）")
    if _present(snap, ["fiscal_exp_yoy"]):
        fy = _num(snap["fiscal_exp_yoy"])
        computed.append({"id": "M15", "v": f"公共财政支出累计同比 {fy:+.1f}%",
                         "tag": "财政加码" if fy > 0 else "财政审慎"})

    if _present(snap, ["style_gap_1d"]):
        g = _num(snap["style_gap_1d"])
        proxies.append({"id": "M07-proxy", "v": f"当日风格差 {g:+.2f}pct",
                        "tag": "成长占优（当日代理，非 20 日口径）" if g < 0 else "红利占优（当日代理）"})
    if _present(snap, ["ai_hardware_flow_yi"]):
        f = _num(snap["ai_hardware_flow_yi"])
        proxies.append({"id": "S09-proxy", "v": f"AI 硬件三链净流入 {f:+.1f} 亿",
                        "tag": "算力层吸金，未触发扩散过热告警" if f > 0 else "算力层净流出，警惕扩散过热"})

    done = {c["id"] for c in computed}
    for r in MACRO_RULES:
        if r["id"] in done:
            continue
        gaps.append({"id": r["id"], "name": r["name"],
                     "why": "westock 无对应接口 / 需人工事件表" if r["avail"] == "gap"
                            else "本期未取数，沿用上次值或仅定性"})

    stage = str(ctx.get("prev_sentiment_stage") or ctx.get("sentiment_stage") or "")
    if tag in ("风险暴露/上半场", "上半场防御") and stage in ("见顶", "退潮"):
        mult *= 0.8
        alerts.append("宏观风险标签 × 情绪见顶/退潮 → 仓位上限在 v2.3 原值上再 ×0.8（只作乘数，不改档位）")
    if snap.get("macro_event_window"):
        mult *= 0.9
        alerts.append("T+1 存在宏观数据/政策发布窗 → α 预算系数 ×0.9，次日预判追加「宏观事件扰动」")

    mult = _closest(mult, ALPHA_MULT_ALLOWED, ceiling=1.0)
    base_stage = str(ctx.get("sentiment_stage") or "")
    base_cap = POSITION_CAP_BASE.get(base_stage)
    return {
        "enabled": bool(V3_SWITCHES["L0_macro_dashboard"]),
        "tag": tag, "alpha_multiplier": mult, "downgrade_only": DOWNGRADE_ONLY,
        "position_cap_base": base_cap,
        "position_cap_effective": round(base_cap * mult, 4) if base_cap is not None else None,
        "note": "宏观层只描述状态：不参与反身性强化/毁灭判定，不回写情绪阶段，不改写 30/60/70/20/0 任何一档。",
        "computed": computed, "proxies": proxies, "qualitative": qualitative,
        "gaps": gaps, "alerts": alerts, "rules_total": len(MACRO_RULES),
        "no_index_target": NO_INDEX_TARGET_NOTE,
        "anchors": MACRO_ANCHORS if V3_SWITCHES["fact_forecast_watermark"] else [],
        "fact_anchors": FACT_ANCHORS,
        "supplement": list(snap.get("supplement") or []),
        "cached_from_prev": bool(prev and not snap),
    }


# ─────────────────────────── 策略会因子层 ───────────────────────────
def strategy_factor_layer(ctx: dict, snapshot: dict | None = None,
                          funnel: dict | None = None) -> dict:
    """旁路因子层：只输出 α 预算乘数与告警，无否决权。"""
    snap, fn = dict(snapshot or {}), dict(funnel or {})
    mults, alerts, applied = [], [], []

    f_ai = _num(snap.get("ai_hardware_flow_yi"))
    if f_ai is not None:
        hit = f_ai < 0 and bool(snap.get("ai_app_limitup_cluster"))
        mults.append({"id": "S09", "m": 0.9 if hit else 1.0,
                      "why": "算力层净流出 + 应用层涨停集中 → 主题扩散/兑现缺口" if hit
                             else "算力层净流入，分层权重 1.0/0.8/0.7/0.6 维持"})
        applied.append("S09")
        if hit:
            alerts.append("AI 主题扩散、兑现缺口：应用层 α 乘数 ×0.9（仅 α 预算，不改选股结果）")

    seed = _num(snap.get("seed_bucket_share"))
    if seed is not None:
        over = seed > ALPHA_BUCKETS["种子"][1]
        alerts.append(f"种子层占比 {seed:.0%} > 10% 上限 → 期权层超配告警") if over else None
        mults.append({"id": "S06", "m": 0.95 if over else 1.0,
                      "why": "种子层超配，α 预算轻度折减" if over else "三层面分桶在 50–60/30–40/5–10% 区间内"})
        applied.append("S06")

    style = _num(snap.get("style_gap_1d"))
    if style is not None:
        mults.append({"id": "S11", "m": 1.0,
                      "why": f"当日风格差 {style:+.2f}pct → 次日预判仅输出风格倾向文字，不改仓位"})
        applied.append("S11")

    n_pass = int(_num(fn.get("pass_count"), 0) or 0)
    if n_pass:
        mults.append({"id": "S04", "m": 1.0,
                      "why": f"L3 过会 {n_pass} 只；成长兑现加分仅作标签，L3 半年归母同比判据不变"})
        applied.append("S04")

    alerts.append(f"事件型加分封顶 ≤{EVENT_BONUS_CAP:.0%} 主口径权重；主题催化 {THEME_DECAY_DAYS} 交易日线性衰减归零")
    return {
        "enabled": bool(V3_SWITCHES["strategy_factor_layer"]),
        "no_veto": True, "only_multiplies": "α 预算（不是仓位上限）",
        "allowed_multipliers": list(FACTOR_MULT_ALLOWED),
        "mults": mults, "applied": applied, "alerts": alerts,
        "quadrant": QUADRANT,
        "alpha_buckets": {k: list(v) for k, v in ALPHA_BUCKETS.items()},
        "rules_total": len(STRATEGY_RULES), "rules": STRATEGY_RULES,
        "note": "所有「剔除」类动作一律降级为「降权告警」；不改动 L1/L2/L2.5/L3 六条硬口径。",
    }


# ─────────────────────── 短线书籍规则（只读标签）───────────────────────
def book_rule_flags(snapshot: dict | None = None) -> dict:
    """24 条书籍规则的命中标签。冲突时以 seal_quality / lhb_power / sentiment_cycle 为准。"""
    snap = dict(snapshot or {})
    hits, missing, switchable, alerts = [], [], [], []
    for r in SHORTLINE_RULES:
        rec = {"id": r["id"], "name": r["name"], "g": r["g"], "p": r["p"],
               "src": r["src"], "kind": r["kind"], "switchable": True}
        v = snap.get(r["key"])
        if v is not None:
            rec["value"] = v
            rec["status"] = "命中"
            hits.append(rec)
        else:
            rec["status"] = "数据缺口/未取数"
            missing.append(rec)
        switchable.append(rec["id"])
    h = _num(snap.get("lianban_height"))
    if h is not None:
        if h >= 3:
            alerts.append(f"R17 三外有三：最高 {int(h)} 板已达 3 板结构，第 2 板价为参考止损位（仅标签，不改打板许可）")
        if h < 4:
            alerts.append(f"R17 高度 {int(h)} <4，接力空间受限；与 sentiment_cycle 的连板率判定解耦")
    return {"enabled": bool(V3_SWITCHES["shortline_rules"]), "hits": hits,
            "missing": missing, "alerts": alerts, "rules_total": len(SHORTLINE_RULES),
            "switchable": switchable,
            "note": "书籍规则只做标签/提示；冲突时以现有八模块结论为准，可逐条停用回滚。"}


# ─────────────────────────── X- 主题扩展层 ───────────────────────────
def theme_extension() -> dict:
    by_tier: dict[str, int] = {}
    for t in X_THEME_EXT:
        by_tier[t["tier"]] = by_tier.get(t["tier"], 0) + 1
    return {
        "enabled": bool(V3_SWITCHES["X_theme_extension"]),
        "namespace": "X- 前缀（第 19+ 扩展方向）",
        "unchanged": "18 方向 / 102 专题板块 / 31 申万一级行业 / 70 只代表个股成分一律不动",
        "tiers": WHITELIST_TIERS, "tier_counts": by_tier,
        "directions": X_THEME_EXT, "n_directions": len(X_THEME_EXT),
        "participates_in_percentile": False,
        "note": "扩展层只并行输出、不回写主表；非上市主体严禁混入可交易池。",
    }


# ───────────────────── 非侵入性自检（口径未被污染）────────────────────
EXPECTED_CALIBER = {
    "CALIBER_VERSION": "v2.3",
    "SOE_BACKGROUND_IS_GATE": False,
    "EMERGING_TECH_FIRST": True,
    "PROFIT_GROWTH_CALIBER": "half_year",
    "SINGLE_YEAR_LOSS_IS_VETO": False,
    "TWO_CONSECUTIVE_LOSSES_IS_VETO": True,
    "CHAIN_THEME_SKIPS_L1_VETO": True,
    "TRADABILITY_LAYER": "L2.5",
    "RANK_LOW_THRESHOLD": 25.0,
    "VR_THRESHOLD": 1.0,
    "DISPERSION_ALERT": 60.0,
}


def non_invasive_check(C=None, KN=None) -> dict:
    """对 calibers / knowledge 做只读快照比对，证明 v3.0 未污染 v2.3 口径。"""
    if C is None:
        from strategy import calibers as C  # noqa
    if KN is None:
        try:
            from strategy import knowledge as KN  # noqa
        except ImportError:
            KN = None
    checks = []
    for k, exp in EXPECTED_CALIBER.items():
        act = getattr(C, k, "<缺失>")
        checks.append({"item": k, "expected": exp, "actual": act, "ok": act == exp})
    k = getattr(C, "KNOWLEDGE", {}) or {}
    checks.append({"item": "KNOWLEDGE 键数", "expected": 45, "actual": len(k), "ok": len(k) == 45})
    checks.append({"item": "KNOWLEDGE 红旗否决线", "expected": 2,
                   "actual": k.get("红旗否决线"), "ok": k.get("红旗否决线") == 2})
    checks.append({"item": "KNOWLEDGE 打板连板率门槛", "expected": 0.60,
                   "actual": k.get("打板_连板率门槛"), "ok": k.get("打板_连板率门槛") == 0.60})
    return {"passed": sum(1 for c in checks if c["ok"]), "total": len(checks),
            "all_ok": all(c["ok"] for c in checks), "checks": checks,
            "knowledge_module_present": KN is not None}


# ─────────────────────────── 统一入口 ───────────────────────────
def build_overlay(data: dict, macro_snapshot: dict | None = None,
                  factor_snapshot: dict | None = None,
                  funnel: dict | None = None,
                  check_modules: bool = True) -> dict:
    """生成可 JSON 序列化的 `v3` 覆盖层，写入 data.json 顶层。只读，不改既有键。"""
    ctx = dict(data.get("context") or {})
    vi = data.get("v3_inputs") or {}
    m_snap = dict(macro_snapshot or vi.get("macro") or {})
    f_snap = dict(factor_snapshot or vi.get("factors") or {})
    fn = dict(funnel or vi.get("funnel") or {})

    macro = macro_dashboard(ctx, m_snap, prev_overlay=(data.get("v3_prev") or {}))
    factors = strategy_factor_layer(ctx, f_snap, fn)
    books = book_rule_flags({**m_snap, **f_snap, **ctx})
    themes = theme_extension()
    checks = non_invasive_check() if check_modules else {
        "passed": 0, "total": 0, "all_ok": True, "checks": []}

    return {
        "enabled": True,
        "overlay_only": OVERLAY_ONLY,
        "framework_version": EXT_VERSION,
        "ext_confirmed_on": EXT_CONFIRMED_ON,
        "caliber_version_unchanged": CALIBER_VERSION_UNCHANGED,
        "source_groups": SOURCE_GROUPS,
        "sources_total": sum(g["n"] for g in SOURCE_GROUPS.values()),
        "switches": dict(V3_SWITCHES),
        "macro": macro, "factors": factors, "shortline": books, "themes": themes,
        "book_suggest": KNOWLEDGE_BOOK_SUGGEST,
        "gaps_register": GAPS_REGISTER,
        "watermark": {
            "规则": "【事实】已发布数据 / 【预测】2027 前瞻与一致预期 / 【口径差异】同指标多来源冲突",
            "隔离": "预测项仅作分档边界与频次先验，不生成买卖信号、不进入回溯验收与六条口径绩效统计",
            "口径差异处理": "数字贸易 4323.1/4110.7 亿美元等三套口径一律改用「同比方向」判据，绝对值不写入阈值",
            "历史资料": "上海 100 项首创（2018）仅作制度复刻事件标签，不参与景气打分",
        },
        "non_invasive_check": checks,
        "rollback": "把 data.json 顶层 v3.enabled 置 false，或逐条关闭 V3_SWITCHES；渲染器自动回到 14 页纯 v2.3 版式",
        "frequency": "宏观月/季频（发布日更新、其余交易日沿用上次值）；情绪/漏斗/评分仍为日频",
    }


def report_blocks(ov: dict) -> dict:
    """把覆盖层压成渲染器可直接取用的文本块（避免模板里写逻辑）。"""
    m, f, b, t = ov["macro"], ov["factors"], ov["shortline"], ov["themes"]
    return {
        "headline": (f"v3.0 扩展层已生效 · 宏观定位「{m['tag']}」 · α 折减 ×{m['alpha_multiplier']:.2f}"
                     f" · 六条口径 v2.3 与 14 页主体结论零改动"),
        "macro_rows": [{"id": x["id"], "v": x["v"], "tag": x["tag"]} for x in m["computed"]]
                      + [{"id": x["id"], "v": x["v"], "tag": x["tag"]} for x in m["proxies"]],
        "macro_gaps": [f"{x['id']} {x['name']}" for x in m["gaps"]],
        "alerts": m["alerts"] + f["alerts"] + b["alerts"],
        "factor_rows": [{"id": x["id"], "m": f"×{x['m']:.2f}", "why": x["why"]} for x in f["mults"]],
        "theme_rows": [{"name": x["name"], "tier": x["tier"], "kw": x["kw"], "src": x["src"]}
                       for x in t["directions"]],
        "book_rows": [{"id": x["id"], "g": x["g"], "p": x["p"], "name": x["name"],
                       "kind": x["kind"], "status": x["status"]} for x in (b["hits"] + b["missing"])],
        "checks": ov["non_invasive_check"],
        "watermark": ov["watermark"],
        "gaps": ov["gaps_register"],
        "anchors": m["anchors"],
        "fact_anchors": m["fact_anchors"],
        "supplement": m["supplement"],
        "rollback": ov["rollback"],
        "quadrant": f["quadrant"],
        "buckets": f["alpha_buckets"],
        "book_suggest": ov["book_suggest"],
        "position_cap_base": m["position_cap_base"],
        "position_cap_effective": m["position_cap_effective"],
        "alpha_multiplier": m["alpha_multiplier"],
        "macro_tag": m["tag"],
        "counts": {
            "sources": ov["sources_total"], "macro_rules": m["rules_total"],
            "macro_computed": len(m["computed"]), "macro_proxies": len(m["proxies"]),
            "macro_gaps": len(m["gaps"]), "factor_rules": f["rules_total"],
            "book_rules": b["rules_total"], "book_hits": len(b["hits"]),
            "book_missing": len(b["missing"]), "themes": t["n_directions"],
            "supplement": len(m["supplement"]),
            "checks_passed": ov["non_invasive_check"]["passed"],
            "checks_total": ov["non_invasive_check"]["total"],
        },
    }


if __name__ == "__main__":
    demo = build_overlay({"context": {"sentiment_stage": "发酵"}},
                         macro_snapshot={"style_gap_1d": -2.65, "ai_hardware_flow_yi": 288.3,
                                         "lianban_height": 4},
                         factor_snapshot={"ai_hardware_flow_yi": 288.3, "style_gap_1d": -2.65},
                         funnel={"pass_count": 8}, check_modules=False)
    import json as _j
    print(_j.dumps(report_blocks(demo)["counts"], ensure_ascii=False, indent=2))
    print(demo["macro"]["tag"], demo["macro"]["alpha_multiplier"])
