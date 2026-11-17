#!/usr/bin/env python3
"""Resolve and record an adaptive image-generation backend."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from handoff_common import BACKENDS, load_json, refresh_run_status, save_json, utc_now


def viability(backend: str, runtime: dict[str, Any]) -> tuple[str, str]:
    if backend == "chatgpt_computer_use":
        if runtime["chatgpt_transmission"] == "denied":
            return "unavailable", "ChatGPT transmission was declined"
        if runtime["computer_use"] == "unknown":
            return "unknown", "Computer Use has not been checked"
        if runtime["computer_use"] == "unavailable":
            return "unavailable", "Computer Use is unavailable"
        if runtime["chatgpt_session"] == "unknown":
            return "unknown", "the ChatGPT session has not been checked"
        if runtime["chatgpt_session"] == "login_required":
            return "unavailable", "the active ChatGPT session requires user action"
        return "viable", "Computer Use is available and the ChatGPT session is authenticated"

    if backend == "built_in_imagegen":
        if runtime["built_in_imagegen"] == "unknown":
            return "unknown", "built-in ImageGen health has not been checked"
        if runtime["built_in_imagegen"] != "healthy":
            return "unavailable", "built-in ImageGen is unavailable or unhealthy"
        return "viable", "built-in ImageGen is available and healthy"

    if backend == "manual_chatgpt_handoff":
        if runtime["chatgpt_transmission"] == "denied":
            return "unavailable", "ChatGPT transmission was declined"
        return "viable", "the prepared prompt pack can be handed to the user"

    if backend in {"mixed", "deterministic"}:
        if runtime["local_renderer"] == "unknown":
            return "unknown", "the local renderer has not been checked"
        if runtime["local_renderer"] != "available":
            return "unavailable", "the local renderer is unavailable"
        return "viable", "the local renderer is available"

    return "unavailable", f"unsupported backend {backend}"


def ordered_candidates(runtime: dict[str, Any], local_fallback: str) -> list[str]:
    requested = runtime["requested_backend"]
    if requested != "auto":
        return [requested]
    preferred = runtime["preferred_backend"]
    ordered = [
        preferred,
        "chatgpt_computer_use",
        "built_in_imagegen",
        "manual_chatgpt_handoff",
        local_fallback,
    ]
    return list(dict.fromkeys(ordered))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--handoff", required=True, type=Path)
    parser.add_argument("--backend", choices=sorted(BACKENDS))
    parser.add_argument("--preferred-backend", choices=sorted(BACKENDS - {"auto"}))
    parser.add_argument("--computer-use", required=True, choices=("unknown", "available", "unavailable"))
    parser.add_argument(
        "--chatgpt-session",
        required=True,
        choices=("unknown", "authenticated", "login_required"),
    )
    parser.add_argument(
        "--built-in-imagegen",
        required=True,
        choices=("unknown", "healthy", "unhealthy", "unavailable"),
    )
    parser.add_argument("--local-renderer", required=True, choices=("unknown", "available", "unavailable"))
    parser.add_argument("--chatgpt-transmission", required=True, choices=("pending", "approved", "denied"))
    parser.add_argument("--local-fallback", choices=("mixed", "deterministic"), default="mixed")
    args = parser.parse_args()

    handoff = args.handoff.expanduser().resolve()
    state_path = handoff / "jobs.json"
    state = load_json(state_path)
    if int(state.get("schema_version", 1)) < 2:
        state["migrated_from_mode"] = state.get("mode")
        state["schema_version"] = 2
        state["mode"] = "adaptive_image_handoff"
    runtime = state.setdefault("generation_runtime", {})
    runtime.setdefault("requested_backend", "auto")
    runtime.setdefault("preferred_backend", "chatgpt_computer_use")
    if args.backend:
        runtime["requested_backend"] = args.backend
    if args.preferred_backend:
        runtime["preferred_backend"] = args.preferred_backend
    runtime.update(
        {
            "computer_use": args.computer_use,
            "chatgpt_session": args.chatgpt_session,
            "built_in_imagegen": args.built_in_imagegen,
            "local_renderer": args.local_renderer,
            "chatgpt_transmission": args.chatgpt_transmission,
        }
    )

    selected = None
    reason = None
    selection_status = "blocked"
    for candidate in ordered_candidates(runtime, args.local_fallback):
        status, candidate_reason = viability(candidate, runtime)
        if status == "viable":
            selected = candidate
            reason = candidate_reason
            selection_status = "selected"
            break
        if status == "unknown":
            reason = candidate_reason
            selection_status = "awaiting_capability_check"
            break

    if reason is None:
        reason = "no permitted generation backend is currently available"

    runtime["selected_backend"] = selected
    runtime["selection_status"] = selection_status
    runtime["selection_reason"] = reason
    runtime["resolved_at"] = utc_now()

    external = state.setdefault("external_handoff", {"destination": "ChatGPT"})
    external.setdefault("destination", "ChatGPT")
    external.setdefault("approved_prompt_files", [])
    external.setdefault("approved_reference_paths", [])
    if selected in {"chatgpt_computer_use", "manual_chatgpt_handoff"}:
        external["status"] = (
            "ready_to_send" if runtime["chatgpt_transmission"] == "approved" else "awaiting_confirmation"
        )
    elif selected is None:
        external["status"] = "declined" if runtime["chatgpt_transmission"] == "denied" else "not_started"
    elif runtime["chatgpt_transmission"] == "denied":
        external["status"] = "declined"
    else:
        external["status"] = "not_required"

    refresh_run_status(state)
    if selection_status == "awaiting_capability_check":
        state["run_status"] = "awaiting_capability_check"
    elif selection_status == "blocked":
        state["run_status"] = "backend_unavailable"
    state["updated_at"] = utc_now()
    save_json(state_path, state)

    print(selected or "blocked")
    print(reason)


if __name__ == "__main__":
    main()
