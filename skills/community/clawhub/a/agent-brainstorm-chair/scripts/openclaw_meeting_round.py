#!/usr/bin/env python3
"""Run a stable Hermes → OpenClaw consultation round across multiple agents.

Generic version — inherits path discovery from openclaw_agent_query.py.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any

DEFAULT_AGENTS = ()  # Empty — user must specify


def load_bridge_module() -> Any:
    module_path = Path(__file__).resolve().with_name("openclaw_agent_query.py")
    spec = importlib.util.spec_from_file_location("openclaw_agent_query", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load bridge module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_agents(value: str) -> list[str]:
    raw_tokens = value.replace(",", " ").split()
    ordered: list[str] = []
    seen: set[str] = set()
    for token in raw_tokens:
        normalized = token.strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        ordered.append(normalized)
    if not ordered:
        raise SystemExit("At least one agent must be provided.")
    return ordered


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a stable Hermes → OpenClaw consultation round across multiple agents.",
    )
    parser.add_argument(
        "--agents",
        required=True,
        help="Comma- or space-separated agent ids in consultation order.",
    )
    parser.add_argument("--topic", help="Meeting topic. When set, build agent-specific prompts automatically.")
    parser.add_argument("--prompt", help="Prompt text to send to every consulted agent.")
    parser.add_argument("--prompt-file", type=Path, help="Read prompt text from a file.")
    parser.add_argument("--timeout-per-agent", type=int, default=120, help="Per-agent timeout in seconds.")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--cwd", type=Path, default=Path.home() / ".openclaw")
    parser.add_argument("--session-suffix", default="hermes-chair")
    parser.add_argument("--persistent", action="store_true", help="Unsupported. Use openclaw_agent_query.py directly.")
    parser.add_argument("--consult-template", dest="consult_template", action="store_true")
    parser.add_argument("--raw-prompt", dest="consult_template", action="store_false")
    parser.add_argument("--normalize-chair-prompt", dest="normalize_chair_prompt", action="store_true")
    parser.add_argument("--no-normalize-chair-prompt", dest="normalize_chair_prompt", action="store_false")
    parser.add_argument("--retry-on-empty", type=int, default=None)
    parser.add_argument("--reset-session", dest="reset_session", action="store_true")
    parser.add_argument("--no-reset-session", dest="reset_session", action="store_false")
    parser.add_argument("--require-all", action="store_true", help="Exit non-zero unless every agent returns a body.")
    parser.set_defaults(reset_session=None)
    parser.set_defaults(consult_template=True)
    parser.set_defaults(normalize_chair_prompt=True)
    return parser


def load_prompt(args: argparse.Namespace) -> str:
    if args.topic:
        if args.prompt or args.prompt_file:
            raise SystemExit("Use --topic or --prompt/--prompt-file, not both.")
        return args.topic.strip()
    if args.prompt and args.prompt_file:
        raise SystemExit("Use either --prompt or --prompt-file, not both.")
    if args.prompt_file:
        return args.prompt_file.read_text(encoding="utf-8").strip()
    if args.prompt:
        return args.prompt.strip()
    raise SystemExit("One of --topic, --prompt, or --prompt-file is required.")


def validate_meeting_args(args: argparse.Namespace) -> None:
    if args.persistent:
        raise SystemExit(
            "openclaw_meeting_round.py only supports isolated per-agent meeting sessions. "
            "Do not pass --persistent; use openclaw_agent_query.py for shared-session debugging."
        )
    if args.reset_session is False:
        raise SystemExit(
            "openclaw_meeting_round.py requires a fresh session for every consulted agent. "
            "Do not pass --no-reset-session."
        )


def build_agent_source_prompt(bridge: Any, *, agent_id: str, prompt_text: str, args: argparse.Namespace) -> str:
    if not args.topic:
        return prompt_text
    builder = getattr(bridge, "CHAIR_PROMPT_BUILDERS", {}).get(agent_id)
    if callable(builder):
        return builder(prompt_text)
    return f"议题：{prompt_text}。请直接给结论，并补职责口径下的依据或约束。"


def query_one_agent(bridge: Any, *, agent_id: str, prompt_text: str, args: argparse.Namespace) -> dict[str, Any]:
    normalized_agent_id = bridge.normalize_agent_id(agent_id)
    session_key = bridge.build_session_key(
        agent_id=normalized_agent_id,
        suffix=args.session_suffix,
        persistent=args.persistent,
    )
    reset_session = (not args.persistent) if args.reset_session is None else args.reset_session
    source_prompt = build_agent_source_prompt(
        bridge,
        agent_id=normalized_agent_id,
        prompt_text=prompt_text,
        args=args,
    )
    effective_prompt = (
        bridge.build_consult_prompt(normalized_agent_id, source_prompt)
        if args.consult_template
        else source_prompt
    )
    effective_prompt, prompt_normalized = (
        bridge.normalize_chair_prompt(normalized_agent_id, effective_prompt)
        if args.normalize_chair_prompt
        else (effective_prompt, False)
    )
    retry_on_empty = args.retry_on_empty if args.retry_on_empty is not None else (1 if prompt_normalized else 0)

    attempt_index = 0
    attempts_made = 0
    result: dict[str, Any] | None = None
    current_session_key = session_key
    while attempt_index <= retry_on_empty:
        current_session_key = bridge.build_retry_session_key(session_key, attempt_index, args.persistent)
        result = bridge.run_query(
            agent_id=normalized_agent_id,
            session_key=current_session_key,
            prompt_text=effective_prompt,
            timeout=args.timeout_per_agent,
            cwd=args.cwd,
            reset_session=reset_session,
        )
        attempts_made += 1
        if not bridge.should_retry_empty(result):
            break
        attempt_index += 1
    assert result is not None

    return {
        "ok": result["ok"],
        "agent_id": normalized_agent_id,
        "session_key": current_session_key,
        "reset_session": reset_session,
        "attempts": attempts_made,
        "prompt_normalized": prompt_normalized,
        "returncode": result["returncode"],
        "output": result["output"],
        "stop_reason": result["stop_reason"],
        "stderr": result["stderr"],
    }


def build_text_report(results: list[dict[str, Any]]) -> str:
    sections: list[str] = []
    for item in results:
        agent_id = str(item["agent_id"])
        sections.append(f"## {agent_id}")
        if item.get("ok"):
            sections.append(str(item.get("output") or "").strip())
        else:
            sections.append("内部协作链路暂不可用")
            detail = str(item.get("stderr") or item.get("output") or "").strip()
            if detail:
                sections.append(f"原因：{detail}")
        sections.append("")
    return "\n".join(sections).strip()


def count_successes(results: list[dict[str, Any]]) -> int:
    return sum(1 for item in results if item.get("ok"))


def main() -> int:
    args = build_parser().parse_args()
    validate_meeting_args(args)
    bridge = load_bridge_module()
    prompt_text = load_prompt(args)
    agent_ids = parse_agents(args.agents)

    results = [
        query_one_agent(bridge, agent_id=agent_id, prompt_text=prompt_text, args=args)
        for agent_id in agent_ids
    ]

    payload = {
        "ok": count_successes(results) == len(results) if args.require_all else count_successes(results) > 0,
        "agents": agent_ids,
        "success_count": count_successes(results),
        "results": results,
    }

    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if payload["ok"] else 1

    print(build_text_report(results))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
