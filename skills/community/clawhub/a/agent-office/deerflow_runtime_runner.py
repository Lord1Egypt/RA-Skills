#!/usr/bin/env python3
"""Standalone embedded DeerFlow runner for Agent Office workers."""
from __future__ import annotations

import argparse
import asyncio
import json
import os
from typing import Any


def _extract_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                text = item.get("text")
                if isinstance(text, str):
                    parts.append(text)
        return "\n".join(part for part in parts if part)
    if isinstance(content, dict):
        text = content.get("text")
        if isinstance(text, str):
            return text
    return str(content)


def _normalize_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    result: list[str] = []
    for item in value:
        text = _extract_text(item).strip()
        if text:
            result.append(text)
    return result


def _extract_json_block(text: str) -> dict[str, Any] | None:
    raw = text.strip()
    if not raw:
        return None
    candidates = [raw]
    if "```json" in raw:
        candidates.extend(chunk.strip() for chunk in raw.split("```json") if chunk.strip())
    if "```" in raw:
        candidates.extend(chunk.strip() for chunk in raw.split("```") if chunk.strip())
    for candidate in candidates:
        cleaned = candidate[4:].strip() if candidate.startswith("json") else candidate
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            start = cleaned.find("{")
            end = cleaned.rfind("}")
            if start != -1 and end != -1 and end > start:
                snippet = cleaned[start : end + 1]
                try:
                    return json.loads(snippet)
                except json.JSONDecodeError:
                    continue
    return None


def _summarize_event(event: dict[str, Any], task_labels: dict[str, str]) -> str | None:
    event_type = str(event.get("type") or "")
    task_id = str(event.get("task_id") or "")
    label = task_labels.get(task_id) or task_id
    if event_type == "task_started":
        description = str(event.get("description") or label)
        task_labels[task_id] = description
        return f"subagent started: {description}"
    if event_type == "task_running":
        message = event.get("message")
        content = ""
        if isinstance(message, dict):
            content = _extract_text(message.get("content") or "")
        if not content:
            return None
        return f"subagent running: {label} -> {content[:200]}"
    if event_type == "task_completed":
        result = _extract_text(event.get("result") or "")
        summary = result[:200] if result else "completed"
        return f"subagent completed: {label} -> {summary}"
    if event_type == "task_failed":
        error = _extract_text(event.get("error") or "")
        return f"subagent failed: {label} -> {error[:200]}"
    if event_type == "task_cancelled":
        return f"subagent cancelled: {label}"
    if event_type == "task_timed_out":
        error = _extract_text(event.get("error") or "")
        return f"subagent timed out: {label} -> {error[:200]}"
    return None


async def _run(args: argparse.Namespace) -> dict[str, Any]:
    os.environ["DEER_FLOW_HOME"] = args.home
    os.environ["DEER_FLOW_CONFIG_PATH"] = args.config

    from langchain_core.messages import AIMessage, HumanMessage
    from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

    from deerflow.client import DeerFlowClient

    task_labels: dict[str, str] = {}
    delegation_trace: list[str] = []
    last_ai_text = ""
    parse_note = ""
    checkpoint_path = os.path.join(args.home, "checkpoints.sqlite")
    os.makedirs(args.home, exist_ok=True)

    async with AsyncSqliteSaver.from_conn_string(checkpoint_path) as saver:
        client = DeerFlowClient(
            agent_name=args.agent_name,
            subagent_enabled=True,
            model_name=args.model,
            checkpointer=saver,
        )
        config = client._get_runnable_config(
            args.thread_id,
            subagent_enabled=True,
            model_name=args.model,
            recursion_limit=args.recursion_limit,
        )
        client._ensure_agent(config)

        state = {"messages": [HumanMessage(content=args.prompt)]}
        context = {"thread_id": args.thread_id, "agent_name": args.agent_name}
        async for item in client._agent.astream(
            state,
            config=config,
            context=context,
            stream_mode=["values", "custom"],
        ):
            if isinstance(item, tuple) and len(item) == 2:
                mode, chunk = item
                mode = str(mode)
            else:
                mode, chunk = "values", item

            if mode == "custom":
                if isinstance(chunk, dict):
                    summary = _summarize_event(chunk, task_labels)
                    if summary:
                        delegation_trace.append(summary)
                continue

            messages = chunk.get("messages", []) if isinstance(chunk, dict) else []
            for msg in messages:
                if isinstance(msg, AIMessage):
                    text = client._extract_text(msg.content)
                    if text:
                        last_ai_text = text

    parsed = _extract_json_block(last_ai_text)
    if parsed is None:
        parse_note = "DeerFlow returned non-JSON text; preserved raw_team_output for inspection."
        parsed = {
            "team_summary": last_ai_text[:2000] or f"{args.agent_name} 已接到《{args.title}》。",
            "collaboration_mode": "deerflow_team",
            "current_scope": [
                "当前以 DeerFlow 2.0 团队形态接单",
                "本次运行返回了非 JSON 文本，已按原始回复收下",
            ],
            "next_step_suggestions": [
                "检查 DeerFlow prompt 是否要求最终只返回 JSON",
            ],
            "handoff_note": "DeerFlow 返回了非 JSON 文本，已保留原始回复供排查。",
            "raw_team_output": last_ai_text[:12000],
            "parse_note": parse_note,
        }
    else:
        raw_team_output = str(parsed.get("raw_team_output") or "")
        if raw_team_output:
            parsed["raw_team_output"] = raw_team_output[:12000]
        if parsed.get("parse_note"):
            parse_note = str(parsed.get("parse_note") or "")

    return {
        "team_summary": str(parsed.get("team_summary") or ""),
        "collaboration_mode": str(parsed.get("collaboration_mode") or "deerflow_team"),
        "current_scope": _normalize_string_list(parsed.get("current_scope", [])),
        "next_step_suggestions": _normalize_string_list(
            parsed.get("next_step_suggestions", [])
        ),
        "handoff_note": str(parsed.get("handoff_note") or ""),
        "delegation_trace": delegation_trace,
        "runtime_backend": "deerflow2_embedded",
        "team_thread_id": args.thread_id,
        "raw_team_output": str(parsed.get("raw_team_output") or ""),
        "parse_note": parse_note,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run an embedded DeerFlow team task.")
    parser.add_argument("--config", required=True)
    parser.add_argument("--home", required=True)
    parser.add_argument("--agent-name", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--thread-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--recursion-limit", type=int, default=48)
    parser.add_argument("--reasoning-effort", default="medium")
    args = parser.parse_args()

    result = asyncio.run(_run(args))
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
