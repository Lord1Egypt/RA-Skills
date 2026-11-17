# -*- coding: utf-8 -*-
# =============================================================================
# 模块编号 : M09
# 模块名称 : 战略顾问专家 (Strategic Advisor Expert · 整合入口)
# 技能矩阵 : 商业管理大师专家技能矩阵 · 模块 9 / 9
# 层级映射 : 汇聚层 · 体系高阶整合入口
# 理论出处 : 整合波特/柯林斯/克里斯坦森/德鲁克/芒格全部方法论
# 版本信息 : v1.0.0
# 接口约定 : 输入问题层级与各方模块入参；经公共加载器调用各模块公开接口，
#            输出分层诊断、行动地图、调用路径与跨层一致性检查。
#            松耦合：仅通过 common.loader.load_skill() 取用模块，绝不 import 模块内部实现。
# =============================================================================
"""战略顾问专家：矩阵汇聚层，路由并整合各专家模块，输出端到端行动方案。"""
from typing import Any, Dict, List
from common.interface import SkillResult, ParameterSpec, SkillContract, validate_params
from common.registry import register
from common.loader import load_skill

MODULE_ID = "m09"
MODULE_NAME = "战略顾问专家"
MATRIX_MAPPING = "商业管理大师技能矩阵 / 模块9 / 汇聚层整合入口 / 综合"

# 层级 -> 默认路由模块
LAYER_ROUTE = {
    "strategy": ["m01"],
    "organization": ["m02", "m03", "m04"],
    "leadership": ["m05", "m06"],
    "execution": ["m07", "m08"],
    "diagnosis": ["m01", "m02", "m03", "m04", "m05", "m06", "m07", "m08"],
}

CONTRACT = SkillContract(
    module_id=MODULE_ID,
    module_name=MODULE_NAME,
    description="输入问题层级与各模块入参，路由并调用对应专家模块，输出分层诊断、行动地图、调用路径与跨层一致性检查。",
    parameters=[
        ParameterSpec(name="problem_layer", type="enum", required=True,
                      constraints="strategy|organization|leadership|execution|diagnosis", default=None,
                      description="问题所处层级"),
        ParameterSpec(name="module_inputs", type="dict", required=True,
                      constraints="键为模块编号(m01..m08)，值为该模块入参 dict", default=None,
                      description="各方模块入参"),
        ParameterSpec(name="focus_modules", type="list", required=False,
                      constraints="可选，显式指定要调用的模块编号列表，覆盖默认路由", default=[],
                      description="聚焦模块"),
    ],
    outputs=[
        {"field": "skill_call_path", "type": "list", "description": "实际调用的模块路径"},
        {"field": "layered_action_map", "type": "dict", "description": "各模块建议汇总(分层)"},
        {"field": "consistency_check", "type": "list", "description": "跨层配称/断层检查"},
        {"field": "integrated_recommendation", "type": "str", "description": "端到端整合建议"},
    ],
)

# 模块 -> 层级归类（用于行动地图分组）
MODULE_TIER = {
    "m01": "战略", "m02": "组织效能与创新", "m03": "组织效能与创新", "m04": "组织效能与创新",
    "m05": "领导力与决策", "m06": "领导力与决策", "m07": "目标与执行", "m08": "目标与执行",
}


def invoke(params: Dict[str, Any]) -> SkillResult:
    errors = validate_params(CONTRACT, params)
    if errors:
        return SkillResult(MODULE_ID, MODULE_NAME, "invalid_input", warnings=errors)

    layer = params["problem_layer"]
    targets = params.get("focus_modules") or LAYER_ROUTE.get(layer, [])
    if not targets:
        return SkillResult(MODULE_ID, MODULE_NAME, "invalid_input",
                           warnings=["无法确定调用模块，请检查 problem_layer 或 focus_modules"])

    results = {}
    call_path = []
    for mid in targets:
        try:
            entry = load_skill(mid)
        except Exception as e:  # 加载失败不阻断其他模块
            results[mid] = {"status": "error", "warning": str(e)}
            continue
        sub = params["module_inputs"].get(mid, {})
        try:
            res = entry["invoke"](sub)
            results[mid] = res.to_dict() if hasattr(res, "to_dict") else res
        except Exception as e:
            results[mid] = {"status": "error", "warning": str(e)}
        call_path.append(mid)

    # 分层行动地图
    action_map = {}
    for mid, res in results.items():
        if isinstance(res, dict) and res.get("status") == "success":
            tier = MODULE_TIER.get(mid, "其他")
            action_map.setdefault(tier, []).extend(res.get("recommendations", []))

    # 跨层一致性检查（基于公共结果结构，不触碰模块内部）
    consistency = []
    if "m01" in results and "m03" in results:
        r1 = results["m01"].get("data", {})
        r3 = results["m03"].get("data", {})
        if r1.get("recommended_strategy") == "focus" and r3.get("g2g_readiness", 5) < 3:
            consistency.append("战略选择'聚焦'但组织卓越就绪度偏低，须先补组织能力再收口细分。")
    if "m07" in results and "m08" in results:
        a7 = results["m07"].get("data", {}).get("alignment_score", 1)
        m8 = results["m08"].get("data", {}).get("momentum_score", 5)
        if a7 < 0.6 and m8 < 3:
            consistency.append("目标对齐不足且飞轮动量弱，执行层存在双重风险。")
    if not consistency:
        consistency.append("各被调用模块间未发现显著断层，配称基本成立。")

    rec = "按层级 %s 路由调用 %s；建议优先处理一致性检查中的断层项，再进入闭环复盘。" % (layer, "→".join(call_path))

    return SkillResult(
        module_id=MODULE_ID, module_name=MODULE_NAME, status="success",
        data={
            "skill_call_path": call_path,
            "layered_action_map": action_map,
            "consistency_check": consistency,
            "integrated_recommendation": rec,
        },
        insights=[
            "调用路径：%s" % " → ".join(call_path),
            "跨层检查：%s" % consistency[0],
        ],
        recommendations=[rec] + consistency,
        warnings=[],
    )


register(MODULE_ID, CONTRACT, invoke)


if __name__ == "__main__":
    import json
    sample = {
        "problem_layer": "diagnosis",
        "module_inputs": {
            "m01": {"industry_description": "连锁咖啡", "five_forces": {"competitors": 5, "new_entrants": 4,
                      "substitutes": 4, "buyer_power": 4, "supplier_power": 2}},
            "m03": {"level5_assessment": {"humility": 5, "will": 5},
                    "three_circles": {"best_at": "x", "economic_engine": "y", "passionate_about": "z"},
                    "flywheel_activities": ["a", "b", "c", "d", "e"], "discipline_culture": 4},
        },
    }
    print(json.dumps(invoke(sample).to_dict(), ensure_ascii=False, indent=2))
