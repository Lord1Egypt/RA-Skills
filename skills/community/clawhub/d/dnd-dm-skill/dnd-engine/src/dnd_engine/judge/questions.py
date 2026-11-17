"""标准判定问题集：一次请求批量扇出多个原子问题。

沿用 System One 的写法——每问只问一个"看一眼就能答"的判断，
答案由 judge.compose 用代码组合，而不是让模型一次输出整段决策。
"""

from __future__ import annotations

from typing import Any

from .check_rules import load_rules
from .contracts import Question

INTENTS = ["探索", "社交", "战斗", "施法", "使用物品", "休息", "剧情推进", "元问题(出戏)"]
ADVANTAGES = ["优势", "普通", "劣势"]
NO_TARGET = "无"

BAND_LABEL_TO_KEY = {
    "轻松(10)": "easy",
    "普通(15)": "normal",
    "困难(20)": "hard",
    "极难(25)": "very_hard",
}


def skill_labels(rules: dict[str, Any] | None = None) -> list[str]:
    table = rules or load_rules()
    return [info.get("name", key) for key, info in table["skills"].items()]


def label_to_skill(label: str, rules: dict[str, Any] | None = None) -> str:
    table = rules or load_rules()
    for key, info in table["skills"].items():
        if info.get("name") == label or key == label:
            return key
    return ""


def build_questions(state: dict[str, Any], action: str,
                    rules: dict[str, Any] | None = None) -> list[Question]:
    table = rules or load_rules()
    party = [str(name) for name in (state.get("acting_options") or [])] or ["(唯一角色)"]
    targets = [str(name) for name in (state.get("targets") or [])] + [NO_TARGET]
    labels = [str(item) for item in table.get("band_labels", [])] or ["普通(15)"]

    return [
        Question("intent", "choice",
                 f"玩家这句话的主要意图是哪一类？\n玩家输入：{action}", INTENTS),
        Question("acting_character", "choice",
                 "这句话里由哪名角色执行？", party),
        Question("requires_check", "noul",
                 "这次行动是否需要掷一次检定/豁免才能决定成败？"),
        Question("check_skill", "choice",
                 "如果需要检定，投哪一项技能？", skill_labels(table)),
        Question("dc_band", "score",
                 "该检定的难度属于哪一档？", labels),
        Question("advantage", "choice",
                 "这次检定是优势、普通还是劣势？", ADVANTAGES),
        Question("target", "choice",
                 "行动的目标是谁或什么？", targets),
        Question("rule_lookup", "noul",
                 "是否必须查规则书/SRD 才能确定机制（而非常识可判）？"),
        Question("module_conflict", "noul",
                 "该行动是否与已知模组事实或当前场景设定冲突？"),
    ]
