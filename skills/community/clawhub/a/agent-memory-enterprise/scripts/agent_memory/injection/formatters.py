"""Memory-to-prompt formatters."""

from __future__ import annotations

from typing import Any


def format_context_memory(window: Any) -> str:
    """Format conversation window as context history."""
    if not window or not window.messages:
        return ""
    lines = ["[Conversation History]"]
    for msg in window.messages:
        role = msg.role.value.upper()
        lines.append(f"{role}: {msg.content}")
    return "\n".join(lines)


def format_task_memory(task: Any) -> str:
    """Format task state as active task context."""
    if not task:
        return ""
    lines = [
        f"[Active Task] {task.goal}",
        f"Status: {task.status.value}, Step {task.current_step_index + 1}/{len(task.steps)}",
    ]
    for step in task.steps:
        marker = "x" if step.status.value == "done" else " " if step.status.value == "pending" else ">"
        lines.append(f"  [{marker}] Step {step.step_index + 1}: {step.description} ({step.status.value})")
    if task.result:
        lines.append(f"Result: {task.result}")
    return "\n".join(lines)


def format_user_profile(profile: Any) -> str:
    """Format user profile as preferences section."""
    if not profile:
        return ""
    lines = ["[User Preferences]"]
    if profile.preferences:
        for key, pref in profile.preferences.items():
            lines.append(f"  {key}: {pref.value} (confidence: {pref.confidence:.0%}, source: {pref.source})")
    if profile.usage_patterns:
        lines.append("[Usage Patterns]")
        for key, val in profile.usage_patterns.items():
            lines.append(f"  {key}: {val}")
    return "\n".join(lines)


def format_knowledge_result(result: Any) -> str:
    """Format a knowledge search result."""
    if not result:
        return ""
    source = f" (from: {result.document_title})" if result.document_title else ""
    return f"[Knowledge{source}]\n{result.content}"


def format_experience(record: Any) -> str:
    """Format an experience record."""
    if not record:
        return ""
    lines = [
        f"[Past Experience] {record.goal_description}",
        f"  Approach: {record.approach}",
        f"  Outcome: {record.outcome.value}",
    ]
    if record.steps_taken:
        lines.append(f"  Steps: {' -> '.join(record.steps_taken)}")
    if record.error_info:
        lines.append(f"  Error: {record.error_info}")
    if record.tags:
        lines.append(f"  Tags: {', '.join(record.tags)}")
    return "\n".join(lines)
