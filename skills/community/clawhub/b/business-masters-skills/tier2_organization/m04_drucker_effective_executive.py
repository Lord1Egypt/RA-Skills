# -*- coding: utf-8 -*-
# =============================================================================
# 模块编号 : M04
# 模块名称 : 德鲁克卓有成效的管理者 (Drucker's Effective Executive)
# 技能矩阵 : 商业管理大师专家技能矩阵 · 模块 4 / 9
# 层级映射 : Tier2 组织效能与创新管理（中层支撑）· 管理有效性
# 理论出处 : 彼得·德鲁克《卓有成效的管理者》(1966)/《管理》(1973)
#            —— 时间管理、重视贡献、用人所长、要事优先、有效决策
# 版本信息 : v1.0.0
# 接口约定 : 输入时间日志/习惯评分/团队优势；输出有效性评分、时间诊断、贡献目标、要事清单
#            与矩阵其他模块松耦合，仅通过 SkillResult 交互
# =============================================================================
"""德鲁克卓有成效的管理者：管理者有效性诊断与效能提升方案。"""
from typing import Any, Dict, List
from common.interface import SkillResult, ParameterSpec, SkillContract, validate_params
from common.registry import register

MODULE_ID = "m04"
MODULE_NAME = "德鲁克卓有成效的管理者"
MATRIX_MAPPING = "商业管理大师技能矩阵 / 模块4 / Tier2管理有效性 / 彼得·德鲁克"

CONTRACT = SkillContract(
    module_id=MODULE_ID,
    module_name=MODULE_NAME,
    description="输入管理者时间日志、五项习惯评分与团队优势，输出有效性评分、时间诊断、贡献目标与要事清单。",
    parameters=[
        ParameterSpec(name="time_log", type="list", required=True,
                      constraints="列表，元素 {activity:str, hours:float}；hours>0", default=None,
                      description="时间使用记录"),
        ParameterSpec(name="current_habits", type="dict", required=True,
                      constraints="含 time_management/focus_contribution/people_strengths/prioritize/effective_decisions 五键，各 1-5 整数",
                      default=None, description="五项习惯自评"),
        ParameterSpec(name="team_strengths", type="list", required=False,
                      constraints="字符串列表，团队成员突出优势", default=[], description="团队优势清单"),
        ParameterSpec(name="contribution_goals", type="list", required=False,
                      constraints="字符串列表，期望贡献方向", default=[], description="贡献目标草稿"),
    ],
    outputs=[
        {"field": "effectiveness_score", "type": "float", "description": "有效性评分(0-5)"},
        {"field": "time_diagnosis", "type": "dict", "description": "时间生产性占比与非生产活动"},
        {"field": "contribution_target", "type": "str", "description": "贡献目标陈述"},
        {"field": "top_priorities", "type": "list", "description": "本季要事清单"},
    ],
)

HABIT_KEYS = ["time_management", "focus_contribution", "people_strengths", "prioritize", "effective_decisions"]


def invoke(params: Dict[str, Any]) -> SkillResult:
    errors = validate_params(CONTRACT, params)
    if errors:
        return SkillResult(MODULE_ID, MODULE_NAME, "invalid_input", warnings=errors)

    habits = params["current_habits"]
    for k in HABIT_KEYS:
        if k not in habits or not isinstance(habits[k], int) or not (1 <= habits[k] <= 5):
            return SkillResult(MODULE_ID, MODULE_NAME, "invalid_input",
                               warnings=["current_habits.%s 必须为 1-5 整数" % k])

    # 时间诊断：以 activity 是否含'会议/沟通/审批/邮件'等关键词估算非生产占比
    total = sum(max(float(t.get("hours", 0)), 0) for t in params["time_log"])
    non_prod_kw = ("会议", "审批", "邮件", "报表", "救火", "meeting", "mail")
    non_prod = sum(t.get("hours", 0) for t in params["time_log"]
                   if any(kw in str(t.get("activity", "")) for kw in non_prod_kw))
    productive_ratio = round(1 - (non_prod / total), 2) if total > 0 else 0.0
    non_prod_acts = [t.get("activity") for t in params["time_log"]
                     if any(kw in str(t.get("activity", "")) for kw in non_prod_kw)]

    eff_score = round(sum(habits[k] for k in HABIT_KEYS) / 5.0, 2)

    contrib = params["contribution_goals"]
    target = ("聚焦贡献：将精力从'为上司工作'转向对组织的成果贡献——" +
              (contrib[0] if contrib else "明确本季对团队/客户的可衡量贡献")) + "。"

    priorities = []
    if productive_ratio < 0.6:
        priorities.append("削减非生产活动(%.0f%%时间被会议/审批占用)，集中整块时间于要事" % (non_prod / total * 100 if total else 0))
    priorities.append("重写岗位贡献目标，对齐组织成果。")
    if params["team_strengths"]:
        priorities.append("按优势配置任务：%s" % "、".join(params["team_strengths"][:3]))
    priorities.append("本季锁定 1-3 件要事，建立有效决策纪律。")

    return SkillResult(
        module_id=MODULE_ID, module_name=MODULE_NAME, status="success",
        data={
            "effectiveness_score": eff_score,
            "time_diagnosis": {"total_hours": total, "productive_ratio": productive_ratio,
                               "non_productive_activities": non_prod_acts},
            "contribution_target": target,
            "top_priorities": priorities,
        },
        insights=[
            "有效性评分 %.2f（五项习惯均值）。" % eff_score,
            "时间生产性占比 %.0f%%，存在%.1f小时非生产活动。" % (productive_ratio * 100, non_prod),
        ],
        recommendations=priorities,
        warnings=[],
    )


register(MODULE_ID, CONTRACT, invoke)


if __name__ == "__main__":
    import json
    sample = {
        "time_log": [{"activity": "战略会议", "hours": 10}, {"activity": "客户交付", "hours": 18},
                     {"activity": "邮件审批", "hours": 8}],
        "current_habits": {"time_management": 3, "focus_contribution": 4,
                           "people_strengths": 4, "prioritize": 3, "effective_decisions": 4},
        "team_strengths": ["数据分析", "客户关系"],
    }
    print(json.dumps(invoke(sample).to_dict(), ensure_ascii=False, indent=2))
