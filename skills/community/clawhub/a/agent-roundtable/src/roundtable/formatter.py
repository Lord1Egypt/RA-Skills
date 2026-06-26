from __future__ import annotations

from typing import Any

from roundtable.models import ConvergenceRecord, Discussion, Participant, Speech


def format_history(speeches: list[Speech], participants_map: dict[str, Any]) -> str:
    """Format speech history into a human-readable string."""
    lines = []
    for s in speeches:
        p_info = participants_map.get(s.participant, {})
        display = p_info.get("display_name", s.participant)
        role = p_info.get("role", "")
        role_str = f"({role})" if role else ""
        ref_str = f" [引用 #{s.reply_to}]" if s.reply_to else ""
        lines.append(f"[#{s.id}] Round {s.round} | {display}{role_str}{ref_str}:\n  {s.content}")
    return "\n\n".join(lines) if lines else "(暂无发言)"


def build_structured_summary(
    disc: Discussion,
    participants: list[Participant],
    speeches: list[Speech],
    p_map: dict[str, Any],
    consensus_pts: list[str],
    disagreement_pts: list[str],
    new_points: list[str],
    final_score: float | None,
    conv_history: list[ConvergenceRecord],
) -> str:
    """Build a compact structured summary for LLM consumption.

    Returns a Markdown string (~500-2000 chars) that gives the coordinator
    enough context to write a conclusion document without re-reading all
    raw speech content.
    """
    lines = []
    lines.append(f"# 圆桌讨论摘要: {disc.topic}")
    if disc.context:
        lines.append(f"\n**背景**: {disc.context}")

    # Participants
    lines.append("\n## 参与者")
    for p in participants:
        name = p.display_name or p.participant
        role = p.role or "未指定"
        perspective = p.perspective or ""
        persp_str = f" — {perspective}" if perspective else ""
        lines.append(f"- **{name}** ({role}){persp_str}")

    # Per-round summary (key points only, truncate content)
    lines.append(f"\n## 讨论轮次 (共 {disc.current_round} 轮)")
    rounds_dict: dict[int, list[Speech]] = {}
    for s in speeches:
        rounds_dict.setdefault(s.round, []).append(s)

    for rnd in sorted(rounds_dict.keys()):
        round_speeches = rounds_dict[rnd]
        lines.append(f"\n### Round {rnd}")
        for s in round_speeches:
            p_info = p_map.get(s.participant, {})
            display = p_info.get("display_name", s.participant)
            role = p_info.get("role", "")
            role_str = f" ({role})" if role else ""
            # Truncate content to 300 chars for summary
            content = s.content
            if len(content) > 300:
                content = content[:297] + "..."
            lines.append(f"- **{display}**{role_str}: {content}")

    # Findings
    if consensus_pts:
        lines.append("\n## 共识点")
        for pt in consensus_pts:
            lines.append(f"- {pt}")

    if disagreement_pts:
        lines.append("\n## 分歧点")
        for pt in disagreement_pts:
            lines.append(f"- {pt}")

    if new_points:
        lines.append("\n## 新议题")
        for pt in new_points:
            lines.append(f"- {pt}")

    # Convergence
    if final_score is not None:
        lines.append(f"\n## 收敛度: {final_score:.2f}")
    if conv_history:
        for c in conv_history:
            lines.append(
                f"- Round {c.round}: score={c.score:.2f}, "
                f"consensus={c.consensus_count}, disagreement={c.disagreement_count}"
            )
    return "\n".join(lines)
