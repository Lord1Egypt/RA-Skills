"""玩家视图 vs 开发视图：确保系统内部信息不出现在玩家面前。

为什么重要：`advance_to` / `ch1.004` / `conflicts_with_canon` 这类东西对玩家毫无意义，
而且会破坏沉浸感（模组规则里明确要求"不出戏"）。

两道防线：
1. **生成后过滤**：`player_view()` 只输出叙事文本（可选行动提示），绝不带类型化字段；
2. **生成时拦截**：`internal_leaks()` 扫叙事文本，命中则视为契约违规 → 触发一次修复。
"""

from __future__ import annotations

import re
from typing import Any

from .contracts import TurnResult

# 内部术语（出现在玩家可见文本里即视为泄漏）
LEAK_TERMS = (
    "advance_to", "events", "npc_attitude", "conflicts_with_canon", "conflict_reason",
    "player_hooks", "narration", "delta", "plot_state", "module_plot", "schema",
    "json", "可达节点", "节点", "剧情骨架", "自检",
)
# 节点 id 形如 ch1.004 / mod.034 / appd.007
NODE_ID_RE = re.compile(r"\b[a-z]{2,6}\d*\.\d{2,4}\b")


def internal_leaks(text: str, extra_terms: tuple[str, ...] = ()) -> list[str]:
    """返回玩家可见文本里的内部信息片段（空列表 = 干净）。"""
    raw = str(text or "")
    found: list[str] = []
    lowered = raw.lower()
    for term in LEAK_TERMS + tuple(extra_terms):
        if term.lower() in lowered:
            found.append(term)
    found.extend(match.group(0) for match in NODE_ID_RE.finditer(raw))
    return sorted(set(found))


def player_view(result: TurnResult, include_hooks: bool = False) -> str:
    """玩家可见文本：只有叙事（以及可选的、已过泄漏检查的行动提示）。"""
    lines = [str(result.narration or "").strip()]
    if include_hooks:
        hooks = [hook for hook in (result.delta.player_hooks or [])
                 if not internal_leaks(hook)]
        if hooks:
            lines.append("")
            lines.extend(f"- {hook}" for hook in hooks)
    return "\n".join(line for line in lines if line).strip()


def dev_view(result: TurnResult) -> str:
    """开发者视图：叙事 + 完整 delta（只在调试/复盘时用）。"""
    import json
    return (f"=== 叙事 ===\n{result.narration}\n\n=== delta ===\n"
            f"{json.dumps(result.delta.to_dict(), ensure_ascii=False, indent=2)}")


def assert_player_safe(text: str) -> None:
    """给调用方的便捷断言：玩家文本必须干净。"""
    leaks = internal_leaks(text)
    if leaks:
        raise ValueError(f"player-facing text leaks internals: {leaks}")


def audit_turn(result: TurnResult, extra_terms: tuple[str, ...] = ()) -> dict[str, Any]:
    """审计一轮结果：叙事是否泄漏、玩家视图是否干净。"""
    narration_leaks = internal_leaks(result.narration, extra_terms)
    view = player_view(result)
    return {
        "narration_leaks": narration_leaks,
        "player_view_leaks": internal_leaks(view, extra_terms),
        "safe": not narration_leaks and not internal_leaks(view, extra_terms),
    }
