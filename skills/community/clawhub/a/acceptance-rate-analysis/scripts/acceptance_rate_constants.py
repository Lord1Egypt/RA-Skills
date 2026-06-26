from __future__ import annotations


MODEL_SET_NAME = "fang_kuan_zi_jin_xiang_mu_bian_hua"
MAIN_ENTITY = "risk_tmp_qyl_cjlfi"
FUNDING_ENTITY = "risk_tmp_rey_last28d_fkzf"

METRIC_ACCEPTANCE_RATE = "m_cjl_hjktqx"
METRIC_ROUTING_AMOUNT = "m_lyje_9wgzqk"
METRIC_ROUTING_COUNT = "m_lydds_abuhr4"
METRIC_CAPITAL_COUNT = "m_zrzfgs_81ie82"
METRIC_FUNDING_AMOUNT = "m_fkje_d9x6b5"

TERMINAL_REASON_TEXT = {
    "R1": "大盘未下降",
    "R2": "一级切片结构迁移（路由金额结构变化是下降主因）",
    "R3": "资方总量明显减少",
    "R4a": "资方分布无整体下行（规则/通过率方向待核查）",
    "R4b": "资产维度未发现可解释下降的异常桶（授用信/规则方向待核查）",
    "R12": "五资产维度原始桶均呈体积规则普降（倾向资方准入/规则传导，本技能不自动跑资金项目）",
    "R5": "资产维度有异常，但没锁定到当前路由金额达到100万的最小因子范围",
    "R6": "资产维度最小因子范围未闭环到敏感资方",
    "R7": "敏感资方收缩",
    "R8": "证据不足 / 字段不足 / 口径异常",
    "R9": "目标客群未低于门槛",
    "R10": "目标客群已检查，但未形成继续下钻切片",
    "R11": "准入资方总量未下降",
}

# ==== 状态展示规范（方案A：状态树最小版） ====
# 状态符号字典：保持纯文本可渲染，不依赖前端
STATUS_SYMBOL_OK = "✅"
STATUS_SYMBOL_STOP = "🛑"
STATUS_SYMBOL_LOCKED = "🔒"
STATUS_SYMBOL_SHIFT = "🧩"
STATUS_SYMBOL_GAP = "⚠️"
STATUS_SYMBOL_PENDING = "⏳"

STAGE_LABELS = {
    "S1": "一级·客群入口",
    "S2": "二级·资方分布",
    "S3": "三级·资产维度",
    "S4": "四级·敏感资方闭环",
}

# terminal_reason -> 阶段编号 / 状态枚举 / 业务短语
# 阶段编号 SX 仅用于状态行展示；status 用于决定符号；label 用于跟在符号后说明终止原因
STAGE_STATUS_TOKENS = {
    "R1": {"stage": "S1", "status": "STOP", "label": "大盘未降"},
    "R2": {"stage": "S1", "status": "SHIFT", "label": "结构迁移"},
    "R3": {"stage": "S2", "status": "STOP", "label": "总量收缩"},
    "R4a": {"stage": "S2", "status": "STOP", "label": "分布未左移"},
    "R4b": {"stage": "S3", "status": "STOP", "label": "资产无信号"},
    "R12": {"stage": "S3", "status": "STOP", "label": "五维普降·资方倾向"},
    "R5": {"stage": "S3", "status": "STOP", "label": "无≥100万范围"},
    "R6": {"stage": "S4", "status": "STOP", "label": "资方未同步收缩"},
    "R7": {"stage": "S4", "status": "LOCKED", "label": "已闭环"},
    "R8": {"stage": "ANY", "status": "DATA-GAP", "label": "证据/字段不足"},
    "R9": {"stage": "S1", "status": "STOP", "label": "客群未触发"},
    "R10": {"stage": "S1", "status": "STOP", "label": "无可下钻切片"},
    "R11": {"stage": "S2", "status": "STOP", "label": "总量未降"},
}

# status 枚举到符号映射；用于 status_line / 汇总表渲染
STATUS_SYMBOL_MAP = {
    "OK": STATUS_SYMBOL_OK,
    "STOP": STATUS_SYMBOL_STOP,
    "LOCKED": STATUS_SYMBOL_LOCKED,
    "SHIFT": STATUS_SYMBOL_SHIFT,
    "DATA-GAP": STATUS_SYMBOL_GAP,
    "PENDING": STATUS_SYMBOL_PENDING,
}

FACTOR_LABELS = {
    "identity_effective_date": "身份证有效性",
    "age_rand": "高龄",
    "identity_province_name": "特殊区域",
    "edu_rand": "高额区间",
    "reloan_price_tag": "风险评级",
}

# 每个因子允许参与命中判断的桶标签白名单；None 表示该因子不做限制（所有桶均可命中）。
# 不在白名单内的桶仍会出现在展示表里作对比参照，但不会触发 is_hit / is_near_miss。
FACTOR_TARGET_BUCKETS: dict[str, set[str] | None] = {
    "identity_effective_date": {"身份证无效"},
    "age_rand": {"50-54", "55+"},
    "identity_province_name": {"新疆", "西藏"},
    "edu_rand": {"5W+"},
    "reloan_price_tag": None,
}

FUNDING_SUPPORTED_FACTORS = {
    "identity_effective_date",
    "age_rand",
    "identity_province_name",
}

ASSET_BUCKET_DRAG_ABSOLUTE_THRESHOLD = 50_000.0
ASSET_BUCKET_DRAG_RELATIVE_THRESHOLD = 0.03
ASSET_RANGE_ROUTE_ABSOLUTE_THRESHOLD = 1_000_000.0
# 原始桶体积规则门禁（五维普降）：可比桶/下降桶当期路由合计占比下限；下降桶个数不少于可比桶的给定比例（并设下限抬底）
ASSET_RAW_GATE_ROUTE_SHARE_THRESHOLD = 0.90
ASSET_RAW_GATE_DECLINING_BUCKET_RATIO = 0.50
ASSET_RAW_GATE_MIN_DECLINING_BUCKETS_FLOOR = 2
# 广谱要求：至少两个可比桶（单桶边际不参与「全维普降」门禁）
ASSET_RAW_GATE_MIN_COMPARABLE_BUCKETS = 2
# R7 实质性收缩判定：放款金额下降绝对值 >= 10万，或相对降幅 >= 5%，满足任一
FUNDING_CONTRACTION_ABSOLUTE_THRESHOLD = 100_000.0
FUNDING_CONTRACTION_RELATIVE_THRESHOLD = 0.05
SUPPORTED_GRANULARITIES = {"day", "week"}
PRIMARY_CUSTOMER_GROUP_DECLINE_THRESHOLD = 0.003
# R2 结构迁移检测：结构效应占大盘下降比例超过此阈值时触发 R2
PRIMARY_STRUCTURAL_DOMINANCE_THRESHOLD = 0.60
# R2 触发要求大盘承接率有实质性下降（绝对值）
PRIMARY_STRUCTURAL_MEANINGFUL_DECLINE = 0.002
CAPITAL_TOTAL_DROP_ABSOLUTE_THRESHOLD = 2.0
# 资方分布左移判断：≤3桶累计路由占比上升超过此阈值（绝对值）才触发
CAPITAL_LOW_BUCKET_SHARE_UP_THRESHOLD = 0.02
TARGET_CUSTOMER_GROUPS = (
    "01.惠选客群",
    "03.精优客群",
)
CUSTOMER_GROUP_ACCEPTANCE_THRESHOLDS = {
    "01.惠选客群": 0.99,
    "03.精优客群": 0.97,
}

PRIMARY_CUSTOMER_GROUP_TABLE_COLUMNS = [
    {"key": "if_irr", "label": "客群"},
    {"key": "baseline_acceptance_rate_text", "label": "对比期"},
    {"key": "current_acceptance_rate_text", "label": "当前期"},
    {"key": "acceptance_rate_delta_text", "label": "变化"},
]

PRIMARY_GROUP_SLICE_TABLE_COLUMNS = [
    {"key": "cp_dj_new", "label": "cp_dj_new"},
    {"key": "baseline_acceptance_rate_text", "label": "对比期承接率"},
    {"key": "current_acceptance_rate_text", "label": "当前期承接率"},
    {"key": "acceptance_rate_delta_text", "label": "承接率变化"},
    {"key": "baseline_route_amount_text", "label": "对比期路由金额"},
    {"key": "current_route_amount_text", "label": "当前期路由金额"},
    {"key": "enter_drill_down_text", "label": "是否下钻"},
]


CAPITAL_BUCKET_TABLE_COLUMNS = [
    {"key": "bucket_label", "label": "资方桶"},
    {"key": "current_route_amount_text", "label": "当前路由金额"},
    {"key": "baseline_route_amount_text", "label": "对比路由金额"},
    {"key": "current_route_share_text", "label": "当前路由占比"},
    {"key": "baseline_route_share_text", "label": "对比路由占比"},
    {"key": "route_share_delta_text", "label": "占比变化"},
    {"key": "current_acceptance_rate_text", "label": "当前承接率"},
    {"key": "baseline_acceptance_rate_text", "label": "对比期承接率"},
]

ASSET_FACTOR_TABLE_COLUMNS = [
    {"key": "bucket_label", "label": "桶"},
    {"key": "current_acceptance_rate_text", "label": "当前承接率"},
    {"key": "baseline_acceptance_rate_text", "label": "对比承接率"},
    {"key": "current_route_amount_text", "label": "当前路由金额"},
    {"key": "share_delta_text", "label": "占比变化"},
    {"key": "structural_impact_text", "label": "结构迁移影响"},
    {"key": "perf_decline_impact_text", "label": "性能下降影响"},
    {"key": "signal_type_text", "label": "信号类型"},
    {"key": "is_hit_text", "label": "是否命中"},
    {"key": "decision_reason", "label": "结论"},
]

ASSET_FACTOR_OVERVIEW_TABLE_COLUMNS = [
    {"key": "factor_label", "label": "维度"},
    {"key": "top_bucket_label", "label": "最强桶"},
    {"key": "current_acceptance_rate_text", "label": "最强桶当前承接率"},
    {"key": "baseline_acceptance_rate_text", "label": "最强桶对比承接率"},
    {"key": "signal_type_text", "label": "信号类型"},
    {"key": "structural_impact_text", "label": "结构迁移影响"},
    {"key": "perf_decline_impact_text", "label": "性能下降影响"},
    {"key": "impact_threshold_text", "label": "单桶影响门槛"},
    {"key": "is_hit_text", "label": "是否命中"},
    {"key": "has_entering_range_text", "label": "候选范围进入第四阶段"},
    {"key": "decision_reason", "label": "维度结论"},
]

ASSET_RANGE_TABLE_COLUMNS = [
    {"key": "range_display", "label": "候选范围"},
    {"key": "range_key", "label": "range_key（传给第四阶段脚本）"},
    {"key": "factor_count_text", "label": "维度数"},
    {"key": "current_acceptance_rate_text", "label": "当前承接率"},
    {"key": "baseline_acceptance_rate_text", "label": "对比承接率"},
    {"key": "current_route_amount_text", "label": "当前路由金额"},
    {"key": "route_amount_threshold_text", "label": "进入门槛"},
    {"key": "enter_next_stage_text", "label": "是否进入下一阶段"},
    {"key": "supported_for_funding_text", "label": "支持资金闭环"},
    {"key": "decision_reason", "label": "结论"},
]
