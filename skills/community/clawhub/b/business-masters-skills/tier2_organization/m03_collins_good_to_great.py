# -*- coding: utf-8 -*-
# =============================================================================
# 模块编号 : M03
# 模块名称 : 柯林斯从优秀到卓越顾问 (Collins' Good to Great Advisor)
# 技能矩阵 : 商业管理大师专家技能矩阵 · 模块 3 / 9
# 层级映射 : Tier2 组织效能与创新管理（中层支撑）· 组织效能
# 理论出处 : 吉姆·柯林斯《从优秀到卓越》(2001)/《基业长青》/《选择卓越》
#            —— 第五级领导、刺猬概念(三环)、飞轮、先人后事、斯托克代尔悖论
# 版本信息 : v1.0.0
# 接口约定 : 输入领导力/三环/飞轮/纪律评分；输出卓越就绪度、刺猬概念、转型路线图
#            与矩阵其他模块松耦合，仅通过 SkillResult 交互
# =============================================================================
"""柯林斯从优秀到卓越顾问：基于三环/飞轮/第五级领导的卓越转型诊断。"""
from typing import Any, Dict, List
from common.interface import SkillResult, ParameterSpec, SkillContract, validate_params
from common.registry import register

MODULE_ID = "m03"
MODULE_NAME = "柯林斯从优秀到卓越顾问"
MATRIX_MAPPING = "商业管理大师技能矩阵 / 模块3 / Tier2组织效能 / 吉姆·柯林斯"

CONTRACT = SkillContract(
    module_id=MODULE_ID,
    module_name=MODULE_NAME,
    description="输入第五级领导评估、刺猬三环、飞轮活动与纪律文化评分，输出卓越就绪度、三环交集强度、飞轮动量与转型路线图。",
    parameters=[
        ParameterSpec(name="level5_assessment", type="dict", required=True,
                      constraints="含 humility(谦逊)与 will(专业意志)，各 1-5 整数", default=None,
                      description="第五级领导力自评"),
        ParameterSpec(name="three_circles", type="dict", required=True,
                      constraints="含 best_at(世界最好)/economic_engine(经济引擎)/passionate_about(热情) 三键字符串",
                      default=None, description="刺猬概念三环"),
        ParameterSpec(name="flywheel_activities", type="list", required=True,
                      constraints="非空字符串列表，业务增强回路各环节(有序)", default=None,
                      description="飞轮活动清单"),
        ParameterSpec(name="discipline_culture", type="int", required=False,
                      constraints="1-5 整数，文化纪律强度", default=3, description="纪律文化强度"),
    ],
    outputs=[
        {"field": "g2g_readiness", "type": "float", "description": "从优秀到卓越就绪度(0-5)"},
        {"field": "hedgehog_concept", "type": "dict", "description": "三环交集评估(强度+结论)"},
        {"field": "flywheel_design", "type": "dict", "description": "飞轮动量与闭环校验"},
        {"field": "transformation_roadmap", "type": "list", "description": "转型路线图步骤"},
    ],
)

def _chk15(d: Dict, key: str) -> int:
    v = d.get(key)
    if not isinstance(v, int) or not (1 <= v <= 5):
        return -1
    return v


def invoke(params: Dict[str, Any]) -> SkillResult:
    errors = validate_params(CONTRACT, params)
    if errors:
        return SkillResult(MODULE_ID, MODULE_NAME, "invalid_input", warnings=errors)

    l5 = params["level5_assessment"]
    h = _chk15(l5, "humility"); w = _chk15(l5, "will")
    if h == -1 or w == -1:
        return SkillResult(MODULE_ID, MODULE_NAME, "invalid_input",
                           warnings=["level5_assessment.humility/will 必须为 1-5 整数"])

    tc = params["three_circles"]
    circle_filled = sum(1 for k in ("best_at", "economic_engine", "passionate_about") if tc.get(k))
    hedgehog_strength = round(circle_filled / 3.0 * 5, 2)
    hedgehog = {"strength": hedgehog_strength,
                "verdict": "三环清晰交集成立" if circle_filled == 3 else "三环未完整，需数据打磨(%d/3)" % circle_filled}

    fw = params["flywheel_activities"]
    loop_closes = len(fw) >= 3
    momentum = round(min(len(fw), 5) / 5.0 * 5, 2) if loop_closes else 1.0
    flywheel = {"momentum": momentum, "loop_closed": loop_closes,
                "note": "飞轮闭环成立，持续推动" if loop_closes else "环节过少，未形成增强回路"}

    readiness = round((min(h, w) + hedgehog_strength + momentum + params["discipline_culture"]) / 4.0, 2)

    roadmap = [
        "先人后事：盘点关键岗位，确保'对的人上车'。",
        "用数据打磨三环，锁定刺猬概念。",
        "设计并持续转动飞轮，保持单一方向。",
        "建立 20 英里行军式纪律节奏，穿越突破临界点。",
    ]
    if min(h, w) < 4:
        roadmap.insert(0, "补强第五级领导力（谦逊+意志），这是跨越的前提。")

    return SkillResult(
        module_id=MODULE_ID, module_name=MODULE_NAME, status="success",
        data={
            "g2g_readiness": readiness,
            "hedgehog_concept": hedgehog,
            "flywheel_design": flywheel,
            "transformation_roadmap": roadmap,
        },
        insights=[
            "第五级领导评分(谦逊 %d / 意志 %d)，就绪度 %.2f。" % (h, w, readiness),
            hedgehog["verdict"],
            flywheel["note"],
        ],
        recommendations=roadmap,
        warnings=[],
    )


register(MODULE_ID, CONTRACT, invoke)


if __name__ == "__main__":
    import json
    sample = {
        "level5_assessment": {"humility": 5, "will": 5},
        "three_circles": {"best_at": "高性价比现制咖啡", "economic_engine": "单店模型盈利",
                          "passionate_about": "让好咖啡触手可及"},
        "flywheel_activities": ["开店", "口碑复购", "数据选品", "规模采购降本", "再投资开店"],
        "discipline_culture": 4,
    }
    print(json.dumps(invoke(sample).to_dict(), ensure_ascii=False, indent=2))
