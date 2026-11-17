# -*- coding: utf-8 -*-
# =============================================================================
# 模块编号 : M01
# 模块名称 : 波特竞争战略顾问 (Porter's Competitive Strategy Advisor)
# 技能矩阵 : 商业管理大师专家技能矩阵 · 模块 1 / 9
# 层级映射 : Tier1 战略思维（顶层设计）· 战略规划
# 理论出处 : 迈克尔·波特《竞争战略》(1980)/《竞争优势》(1985)/《什么是战略》(HBR 1996)
#            —— 五力模型、价值链、三大通用战略（成本领先/差异化/聚焦）
# 版本信息 : v1.0.0
# 接口约定 : 输入 five_forces 评分(1-5) + 行业描述；输出行业吸引力、推荐战略、取舍清单
#            与其他模块松耦合，仅通过 common.interface.SkillResult 交互
# =============================================================================
"""波特竞争战略顾问：基于五力模型与三大通用战略的结构化行业诊断与定位。"""
from typing import Any, Dict, List
from common.interface import SkillResult, ParameterSpec, SkillContract, validate_params
from common.registry import register

MODULE_ID = "m01"
MODULE_NAME = "波特竞争战略顾问"
MATRIX_MAPPING = "商业管理大师技能矩阵 / 模块1 / Tier1战略规划 / 迈克尔·波特"

CONTRACT = SkillContract(
    module_id=MODULE_ID,
    module_name=MODULE_NAME,
    description="输入行业五力强度评分与行业描述，输出行业吸引力、推荐通用战略、配称取舍清单与定位陈述。",
    parameters=[
        ParameterSpec(name="industry_description", type="str", required=True,
                      constraints="非空字符串，简述行业与竞争环境", default=None,
                      description="行业与竞争环境描述"),
        ParameterSpec(name="five_forces", type="dict", required=True,
                      constraints="含5个键，取值1-5整数：competitors(现有竞争)、new_entrants(潜在进入)、"
                                  "substitutes(替代品)、buyer_power(买方议价)、supplier_power(供方议价)；值越大威胁越强",
                      default=None, description="五力强度评分"),
        ParameterSpec(name="candidate_strategies", type="list", required=False,
                      constraints="可选枚举子集：[cost_leadership|differentiation|focus]；为空则由模型自动推荐",
                      default=[], description="候选战略约束"),
        ParameterSpec(name="current_position", type="str", required=False,
                      constraints="字符串，描述当前战略定位", default="", description="当前战略定位（用于对比）"),
    ],
    outputs=[
        {"field": "industry_attractiveness", "type": "float", "description": "行业吸引力评分(0-5)，越高利润池越充裕"},
        {"field": "profit_pool", "type": "str", "description": "利润池评估结论"},
        {"field": "recommended_strategy", "type": "str", "description": "推荐通用战略：成本领先/差异化/聚焦"},
        {"field": "five_forces_diagnosis", "type": "dict", "description": "逐力诊断(等级+启示)"},
        {"field": "positioning_statement", "type": "str", "description": "战略定位陈述"},
        {"field": "tradeoffs", "type": "list", "description": "必须放弃的业务边界(取舍清单)"},
    ],
)

FORCE_KEYS = ["competitors", "new_entrants", "substitutes", "buyer_power", "supplier_power"]
FORCE_LABELS = {
    "competitors": "现有竞争者对抗", "new_entrants": "潜在进入者威胁",
    "substitutes": "替代品威胁", "buyer_power": "买方议价能力", "supplier_power": "供方议价能力",
}
TRADEOFF_MAP = {
    "cost_leadership": ["不盲目追加非必要产品功能", "不在非规模市场打差异化"],
    "differentiation": ["不以价格战回应竞争", "不削减支撑溢价的质量/服务投入"],
    "focus": ["不盲目拓展至全市场", "不为规模牺牲细分深耕"],
}


def _diagnose_force(key: str, score: int) -> Dict[str, str]:
    level = "高" if score >= 4 else ("中" if score >= 3 else "低")
    impl = {
        "competitors": "价格战/营销战频发，利润被吞噬" if score >= 4 else "竞争格局相对稳定",
        "new_entrants": "壁垒不足，新玩家持续涌入" if score >= 4 else "进入壁垒有效",
        "substitutes": "替代方案挤压需求与定价权" if score >= 4 else "替代压力可控",
        "buyer_power": "客户议价强，倒逼降价" if score >= 4 else "客户黏性较好",
        "supplier_power": "供给集中，成本被抬升" if score >= 4 else "供给端议价有限",
    }[key]
    return {"score": score, "level": level, "implication": impl}


def _recommend(five_forces: Dict[str, int], candidates: List[str]) -> str:
    """基于五力 heuristic 选择最契合的通用战略。"""
    c = five_forces
    scores = {
        "cost_leadership": 0.0,
        "differentiation": 0.0,
        "focus": 0.0,
    }
    # 买方/供方强 -> 差异化更优（建立溢价护城河）
    if c["buyer_power"] >= 4 or c["supplier_power"] >= 4:
        scores["differentiation"] += 2
    # 现有竞争强 + 规模可能 -> 成本领先
    if c["competitors"] >= 4:
        scores["cost_leadership"] += 1.5
    # 替代品/新进入强 -> 聚焦细分建立壁垒
    if c["substitutes"] >= 4 or c["new_entrants"] >= 4:
        scores["focus"] += 1.5
    if c["competitors"] <= 2:
        scores["differentiation"] += 1
    pool = candidates if candidates else list(scores.keys())
    return max(pool, key=lambda s: scores.get(s, 0.0))


def invoke(params: Dict[str, Any]) -> SkillResult:
    errors = validate_params(CONTRACT, params)
    if errors:
        return SkillResult(MODULE_ID, MODULE_NAME, "invalid_input", warnings=errors)

    ff = params["five_forces"]
    # 范围校验
    for k in FORCE_KEYS:
        if k not in ff or not isinstance(ff[k], int) or not (1 <= ff[k] <= 5):
            return SkillResult(MODULE_ID, MODULE_NAME, "invalid_input",
                               warnings=["five_forces.%s 必须为 1-5 整数" % k])

    diagnosis = {k: _diagnose_force(k, ff[k]) for k in FORCE_KEYS}
    avg_threat = sum(ff[k] for k in FORCE_KEYS) / 5.0
    attractiveness = round(5 - avg_threat, 2)
    profit_pool = ("利润池充裕，结构吸引力强" if attractiveness >= 3.5
                   else "利润池中等，需靠定位突围" if attractiveness >= 2.5
                   else "利润池被结构性侵蚀，须谨慎进入或重构")
    strategy = _recommend(ff, params["candidate_strategies"])
    pos = "在%s中，以【%s】为战略主线，围绕%s构建相互强化的活动系统。" % (
        params["industry_description"][:40], strategy, FORCE_LABELS.get("competitors", "竞争"))
    tradeoffs = TRADEOFF_MAP.get(strategy, []) + ["避免'骑墙'：不在成本领先与差异化间摇摆"]

    return SkillResult(
        module_id=MODULE_ID, module_name=MODULE_NAME, status="success",
        data={
            "industry_attractiveness": attractiveness,
            "profit_pool": profit_pool,
            "recommended_strategy": strategy,
            "five_forces_diagnosis": diagnosis,
            "positioning_statement": pos,
            "tradeoffs": tradeoffs,
        },
        insights=[
            "五力平均威胁强度 %.2f，行业结构性利润空间%s。" % (avg_threat, "有限" if avg_threat >= 3 else "较大"),
            "推荐主线战略：%s（依据五力特征 heuristic 判定）。" % strategy,
        ],
        recommendations=[
            "以 %s 为定位核心，明确价值主张与取舍边界。" % strategy,
            "绘制价值链配称图，确保各项活动相互强化而非相互抵消。",
            "建立竞争监控仪表盘，跟踪五力变化。",
        ],
        warnings=["current_position 未参与评分，仅用于人工对比。"],
    )


register(MODULE_ID, CONTRACT, invoke)


if __name__ == "__main__":
    import json
    sample = {
        "industry_description": "中式连锁咖啡赛道，价格战激烈",
        "five_forces": {"competitors": 5, "new_entrants": 4, "substitutes": 4,
                        "buyer_power": 4, "supplier_power": 2},
    }
    print(json.dumps(invoke(sample).to_dict(), ensure_ascii=False, indent=2))
