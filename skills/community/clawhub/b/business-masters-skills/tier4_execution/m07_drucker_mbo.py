# -*- coding: utf-8 -*-
# =============================================================================
# 模块编号 : M07
# 模块名称 : 德鲁克目标管理(MBO)顾问 (Drucker's Management by Objectives Advisor)
# 技能矩阵 : 商业管理大师专家技能矩阵 · 模块 7 / 9
# 层级映射 : Tier4 目标管理与执行落地（行动层）· 目标管理
# 理论出处 : 彼得·德鲁克《管理的实践》(1954) 提出 MBO
#            —— 自我控制、目标链、SMART、周期复盘
# 版本信息 : v1.0.0
# 接口约定 : 输入组织目标与草稿目标；输出目标树、SMARTER校验、对齐度、复盘节奏
#            与矩阵其他模块松耦合，仅通过 SkillResult 交互
# =============================================================================
"""德鲁克目标管理(MBO)顾问：目标分解、SMARTER校验与对齐诊断。"""
from typing import Any, Dict, List
from common.interface import SkillResult, ParameterSpec, SkillContract, validate_params
from common.registry import register

MODULE_ID = "m07"
MODULE_NAME = "德鲁克目标管理(MBO)顾问"
MATRIX_MAPPING = "商业管理大师技能矩阵 / 模块7 / Tier4目标管理 / 彼得·德鲁克"

CONTRACT = SkillContract(
    module_id=MODULE_ID,
    module_name=MODULE_NAME,
    description="输入组织总目标与草稿目标(含负责人/指标/期限)，输出目标树、SMARTER校验、对齐度与复盘节奏。",
    parameters=[
        ParameterSpec(name="org_objective", type="str", required=True,
                      constraints="非空字符串，组织年度总目标", default=None, description="组织总目标"),
        ParameterSpec(name="draft_targets", type="list", required=True,
                      constraints="列表，元素 {owner:str, target:str, metric:str, deadline:str}；owner/metric/deadline 必填",
                      default=None, description="草稿目标清单"),
        ParameterSpec(name="department_goals", type="list", required=False,
                      constraints="列表，元素 {dept:str, goal:str}", default=[], description="部门目标(用于对齐)"),
    ],
    outputs=[
        {"field": "goal_tree", "type": "dict", "description": "组织->部门->个人的目标树"},
        {"field": "smarter_assessment", "type": "list", "description": "逐目标 SMARTER 通过情况"},
        {"field": "alignment_score", "type": "float", "description": "目标对齐度(0-1)"},
        {"field": "review_cadence", "type": "str", "description": "复盘节奏建议"},
    ],
)

SMARTER_DIMS = ["具体", "可衡量", "可达成", "相关", "有时限", "可激励", "可复盘"]


def _smarter_pass(t: Dict) -> Dict[str, bool]:
    return {
        "具体": bool(t.get("target")),
        "可衡量": bool(t.get("metric")),
        "可达成": "达成" in t.get("target", "") or len(str(t.get("target", ""))) > 4,
        "相关": bool(t.get("owner")),
        "有时限": bool(t.get("deadline")),
        "可激励": "激励" in t.get("target", "") or "贡献" in t.get("target", ""),
        "可复盘": bool(t.get("metric")) and bool(t.get("deadline")),
    }


def invoke(params: Dict[str, Any]) -> SkillResult:
    errors = validate_params(CONTRACT, params)
    if errors:
        return SkillResult(MODULE_ID, MODULE_NAME, "invalid_input", warnings=errors)

    targets = params["draft_targets"]
    for i, t in enumerate(targets):
        for key in ("owner", "metric", "deadline"):
            if not t.get(key):
                return SkillResult(MODULE_ID, MODULE_NAME, "invalid_input",
                                   warnings=["draft_targets[%d].%s 必填" % (i, key)])

    assessments = []
    passed = 0
    for t in targets:
        chk = _smarter_pass(t)
        ok = all(chk.values())
        passed += 1 if ok else 0
        assessments.append({"owner": t.get("owner"), "target": t.get("target"),
                            "smarter_pass": ok, "detail": chk})

    goal_tree = {"org": params["org_objective"], "departments": params["department_goals"],
                 "individuals": [{"owner": t.get("owner"), "target": t.get("target")} for t in targets]}

    alignment = round(passed / len(targets), 2) if targets else 0.0
    cadence = "月度复盘指标进展、季度校准目标与资源、年度重构目标树" if alignment >= 0.6 else "先补齐未通过 SMARTER 的目标再设节奏"

    return SkillResult(
        module_id=MODULE_ID, module_name=MODULE_NAME, status="success",
        data={
            "goal_tree": goal_tree,
            "smarter_assessment": assessments,
            "alignment_score": alignment,
            "review_cadence": cadence,
        },
        insights=[
            "SMARTER 通过率 %.0f%%（%d/%d）。" % (alignment * 100, passed, len(targets)),
        ],
        recommendations=[
            "对未通过 SMARTER 的目标补充指标与期限。",
            "上下级共同确认目标，以自我控制替代外部压制。",
            cadence,
        ],
        warnings=[],
    )


register(MODULE_ID, CONTRACT, invoke)


if __name__ == "__main__":
    import json
    sample = {
        "org_objective": "全年新增 200 家盈利门店",
        "draft_targets": [
            {"owner": "华东区", "target": "新增80家且单店盈利", "metric": "净增门店数", "deadline": "2026-12-31"},
            {"owner": "华南区", "target": "新增60家", "metric": "净增门店数", "deadline": "2026-12-31"},
        ],
    }
    print(json.dumps(invoke(sample).to_dict(), ensure_ascii=False, indent=2))
