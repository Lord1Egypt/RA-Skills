from __future__ import annotations


MODEL_SET_NAME = "fang_kuan_zi_jin_xiang_mu_bian_hua"
MAIN_ENTITY = "risk_tmp_qyl_cjlfi"
FUNDING_ENTITY = "risk_tmp_rey_last28d_fkzf"

METRIC_ACCEPTANCE_RATE = "m_cjl_hjktqx"
METRIC_ROUTING_AMOUNT = "m_lyje_9wgzqk"
METRIC_CAPITAL_COUNT = "m_zrzfgs_81ie82"
METRIC_FUNDING_AMOUNT = "m_fkje_d9x6b5"

TERMINAL_REASON_TEXT = {
    "R1": "大盘未下降",
    "R2": "一级切片结构迁移",
    "R3": "资方总量明显减少",
    "R4": "更像规则 / 授用信通过率变化",
    "R5": "资产维度有异常，但没形成达到第四阶段门槛的高影响组合",
    "R6": "资产维度组合未闭环到敏感资方",
    "R7": "敏感资方收缩",
    "R8": "证据不足 / 字段不足 / 口径异常",
}

FACTOR_LABELS = {
    "identity_effective_date": "身份证有效性",
    "age_rand": "高龄",
    "identity_province_name": "特殊区域",
    "edu_rand": "高额区间",
    "grade_level_round": "风险评级",
}

FUNDING_SUPPORTED_FACTORS = {
    "identity_effective_date",
    "age_rand",
    "identity_province_name",
}

ASSET_BUCKET_DRAG_ABSOLUTE_THRESHOLD = 100_000.0
ASSET_BUCKET_DRAG_RELATIVE_THRESHOLD = 0.05
ASSET_COMBO_DRAG_ABSOLUTE_THRESHOLD = 1_000_000.0
ASSET_COMBO_DRAG_RELATIVE_THRESHOLD = 0.15
SUPPORTED_GRANULARITIES = {"day", "week"}
PRIMARY_DRILL_DOWN_ABSOLUTE_THRESHOLD = 200_000.0
PRIMARY_DRILL_DOWN_RELATIVE_THRESHOLD = 0.05
PRIMARY_DRILL_DOWN_MAX_SLICES = 5
CAPITAL_TOTAL_DROP_RATIO_THRESHOLD = 0.30

PRIMARY_DISPLAY_TABLE_COLUMNS = [
    {"key": "analysis_rank", "label": "排名"},
    {"key": "slice_display", "label": "切片"},
    {"key": "current_acceptance_rate_text", "label": "当前承接率"},
    {"key": "baseline_acceptance_rate_text", "label": "对比期承接率"},
    {"key": "impact_route_amount_text", "label": "影响路由金额"},
    {"key": "drag_route_amount_text", "label": "拖累路由金额"},
    {"key": "acceptance_rate_delta_bp_text", "label": "承接率变化（bp）"},
]

ASSET_FACTOR_TABLE_COLUMNS = [
    {"key": "factor_label", "label": "维度"},
    {"key": "bucket_label", "label": "桶"},
    {"key": "current_route_amount_text", "label": "当前路由金额"},
    {"key": "baseline_route_amount_text", "label": "对比路由金额"},
    {"key": "current_acceptance_rate_text", "label": "当前承接率"},
    {"key": "baseline_acceptance_rate_text", "label": "对比承接率"},
    {"key": "current_route_share_text", "label": "当前占比"},
    {"key": "baseline_route_share_text", "label": "对比占比"},
    {"key": "share_delta_text", "label": "占比变化"},
    {"key": "impact_route_amount_text", "label": "影响路由金额"},
    {"key": "impact_threshold_text", "label": "门槛"},
    {"key": "is_hit_text", "label": "是否命中"},
    {"key": "decision_reason", "label": "结论"},
]

ASSET_COMBO_TABLE_COLUMNS = [
    {"key": "combo_id", "label": "组合ID"},
    {"key": "combo_display", "label": "组合"},
    {"key": "current_share_text", "label": "当前占比"},
    {"key": "baseline_share_text", "label": "对比占比"},
    {"key": "share_delta_text", "label": "占比变化"},
    {"key": "current_acceptance_rate_text", "label": "当前承接率"},
    {"key": "baseline_acceptance_rate_text", "label": "对比承接率"},
    {"key": "impact_route_amount_text", "label": "影响路由金额"},
    {"key": "impact_threshold_text", "label": "门槛"},
    {"key": "enter_next_stage_text", "label": "是否进入下一阶段"},
    {"key": "supported_for_funding_text", "label": "是否支持资金闭环"},
    {"key": "decision_reason", "label": "结论"},
]
