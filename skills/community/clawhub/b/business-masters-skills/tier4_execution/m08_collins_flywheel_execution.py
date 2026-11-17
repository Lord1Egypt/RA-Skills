# -*- coding: utf-8 -*-
# =============================================================================
# 模块编号 : M08
# 模块名称 : 柯林斯执行飞轮顾问 (Collins' Flywheel Execution Advisor)
# 技能矩阵 : 商业管理大师专家技能矩阵 · 模块 8 / 9
# 层级映射 : Tier4 目标管理与执行落地（行动层）· 执行落地
# 理论出处 : 吉姆·柯林斯《从优秀到卓越》飞轮效应 / 《选择卓越》20英里行军
#            —— 增强回路、一致性纪律、临界点突破
# 版本信息 : v1.0.0
# 接口约定 : 输入飞轮环节与行军指标；输出飞轮图、动量、纪律评估、突破信号
#            与矩阵其他模块松耦合，仅通过 SkillResult 交互
# =============================================================================
"""柯林斯执行飞轮顾问：飞轮闭环、20英里行军纪律与突破信号诊断。"""
from typing import Any, Dict, List
from common.interface import SkillResult, ParameterSpec, SkillContract, validate_params
from common.registry import register

MODULE_ID = "m08"
MODULE_NAME = "柯林斯执行飞轮顾问"
MATRIX_MAPPING = "商业管理大师技能矩阵 / 模块8 / Tier4执行落地 / 吉姆·柯林斯"

CONTRACT = SkillContract(
    module_id=MODULE_ID,
    module_name=MODULE_NAME,
    description="输入飞轮有序环节与20英里行军指标，输出飞轮闭环图、动量评分、纪律评估与突破信号。",
    parameters=[
        ParameterSpec(name="flywheel_steps", type="list", required=True,
                      constraints="非空有序字符串列表，业务增强回路各环节", default=None,
                      description="飞轮环节"),
        ParameterSpec(name="twenty_mile_targets", type="dict", required=False,
                      constraints="可选 {min:float, max:float}，最低/最高绩效线", default={},
                      description="20英里行军指标"),
        ParameterSpec(name="momentum_signals", type="list", required=False,
                      constraints="可选，{metric:str, trend:str(up|flat|down)} 列表", default=[],
                      description="动量信号"),
    ],
    outputs=[
        {"field": "flywheel_map", "type": "dict", "description": "有序飞轮闭环图"},
        {"field": "momentum_score", "type": "float", "description": "飞轮动量(0-5)"},
        {"field": "discipline_assessment", "type": "str", "description": "20英里行军纪律评估"},
        {"field": "breakthrough_signal", "type": "str", "description": "突破临界点信号"},
    ],
)

def invoke(params: Dict[str, Any]) -> SkillResult:
    errors = validate_params(CONTRACT, params)
    if errors:
        return SkillResult(MODULE_ID, MODULE_NAME, "invalid_input", warnings=errors)

    steps = params["flywheel_steps"]
    n = len(steps)
    loop_closed = n >= 3
    momentum = round(min(n, 5) / 5.0 * 5, 2) if loop_closed else 1.0

    tgt = params.get("twenty_mile_targets") or {}
    if tgt:
        discipline = "已设20英里行军线(%.1f~%.1f)，保持'坏年景不落底线、好年景不越顶线'的一致节奏。" % (
            tgt.get("min", 0), tgt.get("max", 0))
    else:
        discipline = "尚未设20英里行军线，建议定义最低/最高绩效线以约束情绪波动。"

    signals = params.get("momentum_signals") or []
    down = [s for s in signals if s.get("trend") == "down"]
    breakthrough = ("动量下行信号 %d 项，需排查飞轮断点而非转向。" % len(down) if down
                   else "各环节动量上行/平稳，飞轮持续积累，逼近突破临界点。")

    fw_map = {"steps": steps, "loop_closed": loop_closed,
              "note": "飞轮首尾相接形成增强回路" if loop_closed else "环节不足，未形成闭环"}

    return SkillResult(
        module_id=MODULE_ID, module_name=MODULE_NAME, status="success",
        data={
            "flywheel_map": fw_map,
            "momentum_score": momentum,
            "discipline_assessment": discipline,
            "breakthrough_signal": breakthrough,
        },
        insights=[
            "飞轮动量 %.2f，闭环%s。" % (momentum, "成立" if loop_closed else "不成立"),
            discipline,
        ],
        recommendations=[
            "保持单一方向持续推动，避免频繁转向陷入厄运循环。",
            "设定20英里行军指标，用纪律替代英雄式冲刺。",
            "监控临界点信号，转够圈数后迎来质变。",
        ],
        warnings=[],
    )


register(MODULE_ID, CONTRACT, invoke)


if __name__ == "__main__":
    import json
    sample = {"flywheel_steps": ["开店", "口碑复购", "数据选品", "规模采购降本", "再投资开店"],
              "twenty_mile_targets": {"min": 50, "max": 80}}
    print(json.dumps(invoke(sample).to_dict(), ensure_ascii=False, indent=2))
