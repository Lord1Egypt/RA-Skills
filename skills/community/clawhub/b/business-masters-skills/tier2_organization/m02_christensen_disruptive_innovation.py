# -*- coding: utf-8 -*-
# =============================================================================
# 模块编号 : M02
# 模块名称 : 克里斯坦森颠覆式创新顾问 (Christensen's Disruptive Innovation Advisor)
# 技能矩阵 : 商业管理大师专家技能矩阵 · 模块 2 / 9
# 层级映射 : Tier2 组织效能与创新管理（中层支撑）· 创新管理
# 理论出处 : 克莱顿·克里斯坦森《创新者的窘境》(1997)/《与运气竞争》(JTBD)/RPV框架
# 版本信息 : v1.0.0
# 接口约定 : 输入市场类型+JTBD+组织RPV；输出市场分类、任务画像、RPV适配、颠覆/防御路线
#            与矩阵其他模块松耦合，仅通过 SkillResult 交互
# =============================================================================
"""克里斯坦森颠覆式创新顾问：基于JTBD与RPV框架的创新定位与攻防策略。"""
from typing import Any, Dict, List
from common.interface import SkillResult, ParameterSpec, SkillContract, validate_params
from common.registry import register

MODULE_ID = "m02"
MODULE_NAME = "克里斯坦森颠覆式创新顾问"
MATRIX_MAPPING = "商业管理大师技能矩阵 / 模块2 / Tier2创新管理 / 克莱顿·克里斯坦森"

CONTRACT = SkillContract(
    module_id=MODULE_ID,
    module_name=MODULE_NAME,
    description="输入目标市场类型、用户待办任务(JTBD)与组织RPV评估，输出市场分类、任务画像、RPV适配诊断与颠覆/防御策略。",
    parameters=[
        ParameterSpec(name="market_type", type="enum", required=True,
                      constraints="non_consumption|new_market|low_end", default=None,
                      description="市场类型：非消费/新市场/低端"),
        ParameterSpec(name="jtbd_statements", type="list", required=True,
                      constraints="非空字符串列表，描述用户'雇佣'产品完成的任务", default=None,
                      description="用户待办任务陈述"),
        ParameterSpec(name="existing_solutions", type="list", required=False,
                      constraints="字符串列表，现有解决方案名称", default=[], description="现有解决方案"),
        ParameterSpec(name="rpv_assessment", type="dict", required=True,
                      constraints="含 resources/processes/values 三键，各 1-5 整数；评估组织对创新市场的适配度",
                      default=None, description="资源-流程-价值观评估"),
        ParameterSpec(name="performance_overshoot", type="bool", required=False,
                      constraints="bool，产品性能是否已超出主流客户需求", default=False, description="性能过度供给标志"),
    ],
    outputs=[
        {"field": "market_classification", "type": "str", "description": "市场分类结论与依据"},
        {"field": "jtbd_profiles", "type": "list", "description": "任务画像(任务/现有方案/缺口)"},
        {"field": "rpv_fit", "type": "dict", "description": "RPV适配评分与诊断"},
        {"field": "disruption_recommendation", "type": "str", "description": "颠覆进攻或防御策略"},
        {"field": "positioning_value_prop", "type": "str", "description": "颠覆性价值主张"},
    ],
)

MARKET_RATIONALE = {
    "non_consumption": "用户因复杂度/成本完全未消费，存在'非消费'空白市场。",
    "new_market": "面向被过度服务或未被满足的新人群，从市场边缘起步。",
    "low_end": "主流客户被过度服务，低端市场存在更简单/便宜的切入点。",
}


def invoke(params: Dict[str, Any]) -> SkillResult:
    errors = validate_params(CONTRACT, params)
    if errors:
        return SkillResult(MODULE_ID, MODULE_NAME, "invalid_input", warnings=errors)

    mt = params["market_type"]
    rpv = params["rpv_assessment"]
    for k in ("resources", "processes", "values"):
        if k not in rpv or not isinstance(rpv[k], int) or not (1 <= rpv[k] <= 5):
            return SkillResult(MODULE_ID, MODULE_NAME, "invalid_input",
                               warnings=["rpv_assessment.%s 必须为 1-5 整数" % k])

    classification = "%s：%s" % (mt, MARKET_RATIONALE[mt])

    exist = params["existing_solutions"]
    profiles = []
    for i, job in enumerate(params["jtbd_statements"]):
        cur = exist[i] if i < len(exist) else "（无现有方案）"
        profiles.append({"job": job, "current_solution": cur,
                         "gap": "现有方案未充分满足" if cur == "（无现有方案）" or "不足" in cur else "存在改进空间"})

    rpv_score = round(sum(rpv[k] for k in ("resources", "processes", "values")) / 3.0, 2)
    # 新市场/非消费更依赖价值观(是否愿意服务小市场)与流程(能否灵活)
    rpv_diag = "组织RPV平均 %.2f。" % rpv_score
    if mt in ("new_market", "non_consumption") and rpv["values"] <= 2:
        rpv_diag += "价值观偏向服务大客户，难以服务新市场——需独立业务单元。"
    elif rpv["processes"] <= 2:
        rpv_diag += "现有流程僵化，无法支撑新市场实验——需重建流程。"
    else:
        rpv_diag += "RPV对新市场基本适配。"

    if mt == "low_end":
        reco = "以更简单/更便宜的方案从低端切入，沿性能轨迹持续改进，待主流客户被过度服务时上移。"
        vprop = "够用就好、更便捷/更便宜，先服务被过度服务或价格敏感客户。"
    elif mt == "new_market":
        reco = "开辟新市场，用边缘独立单元避开主流资源分配流程的挤压。"
        vprop = "为从未被服务的人群提供'第一个够用方案'。"
    else:
        reco = "激活非消费市场，把'不会做/太贵'变为'能轻松做到'。"
        vprop = "消除消费门槛，让非用户低成本完成待办任务。"

    if params["performance_overshoot"]:
        reco += "（注：主流性能已过度供给，竞争基础正转向便捷/价格，是颠覆窗口。）"

    return SkillResult(
        module_id=MODULE_ID, module_name=MODULE_NAME, status="success",
        data={
            "market_classification": classification,
            "jtbd_profiles": profiles,
            "rpv_fit": {"score": rpv_score, "diagnosis": rpv_diag},
            "disruption_recommendation": reco,
            "positioning_value_prop": vprop,
        },
        insights=[
            "市场归类为 %s。" % mt,
            rpv_diag,
        ],
        recommendations=[
            "从 JTBD 出发设计最小可行方案，而非堆叠产品特性。",
            "在位企业应以独立单元承载创新，避免被主流价值观同化。",
        ],
        warnings=[],
    )


register(MODULE_ID, CONTRACT, invoke)


if __name__ == "__main__":
    import json
    sample = {
        "market_type": "low_end",
        "jtbd_statements": ["上班路上快速喝到一杯咖啡"],
        "existing_solutions": ["门店现磨(贵且慢)"],
        "rpv_assessment": {"resources": 4, "processes": 3, "values": 3},
        "performance_overshoot": True,
    }
    print(json.dumps(invoke(sample).to_dict(), ensure_ascii=False, indent=2))
