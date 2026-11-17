# -*- coding: utf-8 -*-
# =============================================================================
# 模块编号 : M06
# 模块名称 : 芒格第一性原理决策顾问 (Munger's First-Principles Decision Advisor)
# 技能矩阵 : 商业管理大师专家技能矩阵 · 模块 6 / 9
# 层级映射 : Tier3 领导力与决策分析（能力层）· 决策分析
# 理论出处 : 查理·芒格《穷查理宝典》多元思维模型/倒置思维/Lollapalooza；
#            辅以卡尼曼《思考，快与慢》双系统
# 版本信息 : v1.0.0
# 接口约定 : 输入决策问题与候选方案；输出第一性拆解、倒置失败清单、偏差审计、推荐方案
#            与矩阵其他模块松耦合，仅通过 SkillResult 交互
# =============================================================================
"""芒格第一性原理决策顾问：多元思维模型 + 倒置 + 偏差审计的结构化决策。"""
from typing import Any, Dict, List
from common.interface import SkillResult, ParameterSpec, SkillContract, validate_params
from common.registry import register

MODULE_ID = "m06"
MODULE_NAME = "芒格第一性原理决策顾问"
MATRIX_MAPPING = "商业管理大师技能矩阵 / 模块6 / Tier3决策分析 / 查理·芒格"

CONTRACT = SkillContract(
    module_id=MODULE_ID,
    module_name=MODULE_NAME,
    description="输入决策问题、候选方案与已知偏差，输出第一性原理拆解、倒置失败清单、偏差审计与带杠杆点的推荐方案。",
    parameters=[
        ParameterSpec(name="decision_question", type="str", required=True,
                      constraints="非空字符串，待决策问题", default=None, description="决策问题"),
        ParameterSpec(name="options", type="list", required=True,
                      constraints="非空字符串列表，候选方案", default=None, description="候选方案"),
        ParameterSpec(name="known_biases", type="list", required=False,
                      constraints="字符串列表，已知的认知/激励偏差", default=[], description="已知偏差"),
        ParameterSpec(name="failure_modes", type="list", required=False,
                      constraints="字符串列表，已识别的失败因素", default=[], description="失败因素草稿"),
    ],
    outputs=[
        {"field": "first_principles_breakdown", "type": "list", "description": "从基本事实拆解的要素"},
        {"field": "inverted_failure_list", "type": "list", "description": "倒置得到的失败清单(须规避)"},
        {"field": "bias_audit", "type": "list", "description": "偏差/激励审计结论"},
        {"field": "recommendation", "type": "str", "description": "含Lollapalooza杠杆的推荐"},
    ],
)

DEFAULT_BIASES = ["确认偏误", "激励导致的偏见", "社会认同", "锚定效应", "过度自信"]


def invoke(params: Dict[str, Any]) -> SkillResult:
    errors = validate_params(CONTRACT, params)
    if errors:
        return SkillResult(MODULE_ID, MODULE_NAME, "invalid_input", warnings=errors)

    q = params["decision_question"]
    opts = params["options"]

    # 第一性原理拆解：将问题按'事实/假设/目标'三类切分
    breakdown = [
        "基本事实：抛开类比，列出该决策不可辩驳的前提(资源/约束/市场真相)。",
        "核心目标：用一句话定义'什么才算解决 %s'。" % q[:30],
        "候选方案映射到事实：逐方案检验是否建立在真实前提上。",
    ]

    # 倒置：先想怎样必定失败
    failures = list(params["failure_modes"])
    failures += [
        "因激励错位导致执行者为自身而非目标优化。",
        "被单一学科视角误导（拿锤子的人看什么都像钉子）。",
        "在证据不足时急于下注，缺乏可逆性评估。",
    ]
    failures = list(dict.fromkeys(failures))  # 去重保序

    biases = params["known_biases"] or DEFAULT_BIASES
    audit = ["审计激励结构：谁因该决策获利，激励是否指向正确结果。"]
    for b in biases[:3]:
        audit.append("检查 '%s' 是否在当前情境中被触发。" % b)

    reco = ("先规避倒置失败清单中的 %d 项风险；再用多元思维模型交叉验证；" % len(failures) +
            "在 %s 中识别Lollapalooza杠杆点——多因素同向叠加处即最大杠杆。" % ("/".join(opts[:3])))

    return SkillResult(
        module_id=MODULE_ID, module_name=MODULE_NAME, status="success",
        data={
            "first_principles_breakdown": breakdown,
            "inverted_failure_list": failures,
            "bias_audit": audit,
            "recommendation": reco,
        },
        insights=[
            "决策问题：%s；候选 %d 项。" % (q, len(opts)),
            "倒置识别出 %d 项潜在失败模式。" % len(failures),
        ],
        recommendations=[
            "反过来想：先列失败清单并逐条设防。",
            "用不少于 2 个学科模型审视同一问题。",
            "audit 激励结构优先于分析方案本身。",
        ],
        warnings=[],
    )


register(MODULE_ID, CONTRACT, invoke)


if __name__ == "__main__":
    import json
    sample = {"decision_question": "是否加盟挪瓦咖啡", "options": ["加盟A区", "加盟B区", "暂不加盟"],
              "known_biases": ["过度自信"]}
    print(json.dumps(invoke(sample).to_dict(), ensure_ascii=False, indent=2))
