# -*- coding: utf-8 -*-
# =============================================================================
# 模块编号 : M05
# 模块名称 : 柯林斯第五级领导力顾问 (Collins' Level 5 Leadership Advisor)
# 技能矩阵 : 商业管理大师专家技能矩阵 · 模块 5 / 9
# 层级映射 : Tier3 领导力与决策分析（能力层）· 领导力发展
# 理论出处 : 吉姆·柯林斯《从优秀到卓越》第2章 · 第五级领导力实证研究
#            —— 五级阶梯、谦逊+意志悖论、窗口与镜子
# 版本信息 : v1.0.0
# 接口约定 : 输入谦逊/意志/归因自评；输出领导层级、第五级差距、发展计划、窗镜指数
#            与矩阵其他模块松耦合，仅通过 SkillResult 交互
# =============================================================================
"""柯林斯第五级领导力顾问：领导力层级诊断与第五级特质发展。"""
from typing import Any, Dict, List
from common.interface import SkillResult, ParameterSpec, SkillContract, validate_params
from common.registry import register

MODULE_ID = "m05"
MODULE_NAME = "柯林斯第五级领导力顾问"
MATRIX_MAPPING = "商业管理大师技能矩阵 / 模块5 / Tier3领导力 / 吉姆·柯林斯"

CONTRACT = SkillContract(
    module_id=MODULE_ID,
    module_name=MODULE_NAME,
    description="输入谦逊、专业意志与归因模式自评，输出当前领导层级、第五级差距分析、发展计划与窗口-镜子指数。",
    parameters=[
        ParameterSpec(name="self_rating", type="dict", required=True,
                      constraints="含 humility(谦逊)/professional_will(意志)/credit_to_others(功于他人)/blame_self(责于己)，各 1-5 整数",
                      default=None, description="第五级特质自评"),
        ParameterSpec(name="current_level", type="int", required=False,
                      constraints="1-5 整数，当前所处领导阶梯层级", default=0, description="当前层级(0=未知待诊断)"),
        ParameterSpec(name="feedback_360", type="dict", required=False,
                      constraints="可选，{peer:int, subordinate:int, superior:int} 1-5", default={},
                      description="360度反馈"),
    ],
    outputs=[
        {"field": "current_level", "type": "int", "description": "诊断得到的领导层级(1-5)"},
        {"field": "level5_gap", "type": "dict", "description": "第五级差距(谦逊缺口/意志缺口)"},
        {"field": "window_mirror_index", "type": "float", "description": "窗口与镜子指数(0-5)"},
        {"field": "development_plan", "type": "list", "description": "第五级发展计划"},
    ],
)

def _chk15(d: Dict, k: str) -> int:
    v = d.get(k)
    return v if isinstance(v, int) and 1 <= v <= 5 else -1


def invoke(params: Dict[str, Any]) -> SkillResult:
    errors = validate_params(CONTRACT, params)
    if errors:
        return SkillResult(MODULE_ID, MODULE_NAME, "invalid_input", warnings=errors)

    r = params["self_rating"]
    for k in ("humility", "professional_will", "credit_to_others", "blame_self"):
        if _chk15(r, k) == -1:
            return SkillResult(MODULE_ID, MODULE_NAME, "invalid_input",
                               warnings=["self_rating.%s 必须为 1-5 整数" % k])

    # 层级诊断：层级由最低短板决定，第五级要求谦逊与意志双高
    level = params.get("current_level") or 0
    if level == 0:
        floor = min(r["humility"], r["professional_will"], r["credit_to_others"], r["blame_self"])
        level = max(1, min(5, floor))

    humility_gap = round(5 - r["humility"], 2)
    will_gap = round(5 - r["professional_will"], 2)
    wm_index = round((r["credit_to_others"] + r["blame_self"]) / 2.0, 2)

    plan = []
    if r["humility"] < 4:
        plan.append("练习'窗口与镜子'：成功对外归因、失败对内归因，降低自我标榜。")
    if r["professional_will"] < 4:
        plan.append("锤炼专业意志：对恒久卓越结果保持不屈不挠的承诺。")
    if r["credit_to_others"] < 4:
        plan.append("建立功劳外推习惯，把聚光灯让给团队。")
    if not plan:
        plan.append("维持第五级：以制度替代个人英雄，培养继任者。")
    plan.append("用 360 反馈持续校准，避免层级回落。")

    return SkillResult(
        module_id=MODULE_ID, module_name=MODULE_NAME, status="success",
        data={
            "current_level": level,
            "level5_gap": {"humility_gap": humility_gap, "will_gap": will_gap,
                           "is_level5": level >= 5},
            "window_mirror_index": wm_index,
            "development_plan": plan,
        },
        insights=[
            "诊断层级 L%d；窗口-镜子指数 %.2f。" % (level, wm_index),
            "谦逊缺口 %.2f / 意志缺口 %.2f。" % (humility_gap, will_gap),
        ],
        recommendations=plan,
        warnings=[],
    )


register(MODULE_ID, CONTRACT, invoke)


if __name__ == "__main__":
    import json
    sample = {"self_rating": {"humility": 4, "professional_will": 5,
                              "credit_to_others": 4, "blame_self": 4}}
    print(json.dumps(invoke(sample).to_dict(), ensure_ascii=False, indent=2))
