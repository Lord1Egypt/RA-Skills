#!/usr/bin/env python3
"""ACP bridge: query an OpenClaw agent from Hermes.

Generic version — all paths are discoverable via environment variables
or sensible defaults. No hardcoded role names.
"""

from __future__ import annotations

import argparse
from collections import deque
import fcntl
import json
import os
import pty
import re
import select
import shutil
import signal
import sys
import time
from pathlib import Path
from typing import Any


# ──────────────────────────────────────────────
#  Path discovery (env var → PATH → sensible fallback)
# ──────────────────────────────────────────────

def _resolve_openclaw_bin() -> Path:
    env = os.environ.get("OPENCLAW_BIN", "").strip()
    if env:
        return Path(env)
    found = shutil.which("openclaw")
    if found:
        return Path(found)
    # Sensible defaults
    for candidate in (
        Path("/opt/homebrew/bin/openclaw"),
        Path("/usr/local/bin/openclaw"),
        Path.home() / ".local/bin/openclaw",
    ):
        if candidate.exists():
            return candidate
    return Path("openclaw")  # best-effort


def _resolve_openclaw_home() -> Path:
    env = os.environ.get("OPENCLAW_HOME", "").strip()
    if env:
        return Path(env)
    return Path.home() / ".openclaw"


def _resolve_path_prefix() -> str:
    env = os.environ.get("OPENCLAW_PATH_PREFIX", "").strip()
    if env:
        return env
    openclaw_bin = _resolve_openclaw_bin()
    if openclaw_bin.parent != Path("."):
        return str(openclaw_bin.parent)
    return "/opt/homebrew/bin"


OPENCLAW_BIN = _resolve_openclaw_bin()
OPENCLAW_HOME = _resolve_openclaw_home()
SCRIPT_BIN = Path(shutil.which("script") or "/usr/bin/script")
PATH_PREFIX = _resolve_path_prefix()
LOCK_FILE = Path(os.environ.get("ACP_BRIDGE_LOCK_FILE", "/tmp/openclaw-acp-bridge.lock"))
DEFAULT_TIMEOUT = 120
DEFAULT_SESSION_NAME = "hermes-chair"
STARTUP_DELAY_SECONDS = 1.0
TRANSCRIPT_RECOVERY_WAIT_SECONDS = 20.0
TRANSCRIPT_RECOVERY_POLL_SECONDS = 1.0
TRANSCRIPT_RECOVERY_FILE_WINDOW_SECONDS = 120.0
TRANSCRIPT_RECOVERY_CANDIDATE_LIMIT = 8
INIT_REQUEST_ID = 0
LOAD_REQUEST_ID = 1
PROMPT_REQUEST_ID = 2

# ──────────────────────────────────────────────
#  Configurable role maps — fill these for your setup
# ──────────────────────────────────────────────

# Agent name aliases:  "my-nickname" → "actual-agent-id"
ALIASES: dict[str, str] = {
    # Example: "strategist" → "agent-1",
    #          "executor" → "agent-2",
}

# Per-agent prompt builders: agent_id → lambda(topic) → prompt
CHAIR_PROMPT_BUILDERS: dict[str, Any] = {
    # Example:
    # "agent-1": lambda topic: f"你是战略顾问。议题：{topic}。请直接给结论，补2条依据和1条风险边界。",
    # "agent-2": lambda topic: f"你是执行顾问。议题：{topic}。请直接给结论，补2条执行约束。",
}

CHAIR_PROMPT_PATTERNS: dict[str, Any] = {
    # Fill regex patterns matching your CHAIR_PROMPT_BUILDERS output
    # to enable automatic prompt normalization.
}


# ──────────────────────────────────────────────
#  Core logic (unchanged from original)
# ──────────────────────────────────────────────

def normalize_agent_id(value: str) -> str:
    normalized = value.strip()
    return ALIASES.get(normalized, normalized)


def build_session_key(agent_id: str, suffix: str, persistent: bool) -> str:
    if persistent:
        return f"agent:{agent_id}:main"
    return f"agent:{agent_id}:{suffix}"


def build_consult_prompt(agent_id: str, user_prompt: str) -> str:
    return (
        f"你现在以 OpenClaw agent {agent_id} 的身份，给 Hermes 主持人做一次内部只读征询。\n"
        "要求：只代表你自己发言；不要改文件、写记忆或触发外部动作；如果信息不足直接说明。\n"
        "你不是主持人，不要控场，不要安排轮次，不要说“第1轮完成/第2轮开始/下一棒/轮到X”。\n"
        f"议题：{user_prompt.strip()}\n"
    )


def normalize_chair_prompt(agent_id: str, prompt_text: str) -> tuple[str, bool]:
    pattern = CHAIR_PROMPT_PATTERNS.get(agent_id)
    builder = CHAIR_PROMPT_BUILDERS.get(agent_id)
    if pattern is None or builder is None:
        return prompt_text, False
    match = pattern.match(prompt_text.strip())
    if match is None:
        return prompt_text, False
    topic = match.group("topic").strip().rstrip("。.")
    if not topic:
        return prompt_text, False
    normalized = builder(topic)
    return normalized, normalized != prompt_text.strip()


def should_retry_empty(result: dict[str, Any]) -> bool:
    if result.get("ok"):
        return False
    output_text = str(result.get("output") or "").strip()
    if output_text:
        return False
    return str(result.get("stop_reason") or "") in {"", "end_turn", "endTurn", "stop"}


def build_retry_session_key(session_key: str, attempt: int, persistent: bool) -> str:
    if attempt <= 0 or persistent:
        return session_key
    return f"{session_key}-retry{attempt}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Query an OpenClaw agent from Hermes through ACP.",
    )
    parser.add_argument("--agent", required=True, help="OpenClaw agent id")
    parser.add_argument("--prompt", help="Prompt text to send")
    parser.add_argument("--prompt-file", type=Path, help="Read prompt text from a file")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--cwd", type=Path, default=OPENCLAW_HOME)
    parser.add_argument("--session-key", help="Override target session key")
    parser.add_argument("--persistent", action="store_true")
    parser.add_argument("--session-suffix", default=DEFAULT_SESSION_NAME)
    parser.add_argument("--consult-template", dest="consult_template", action="store_true")
    parser.add_argument("--raw-prompt", dest="consult_template", action="store_false")
    parser.add_argument("--normalize-chair-prompt", dest="normalize_chair_prompt", action="store_true")
    parser.add_argument("--no-normalize-chair-prompt", dest="normalize_chair_prompt", action="store_false")
    parser.add_argument("--retry-on-empty", type=int, default=None)
    parser.add_argument("--reset-session", dest="reset_session", action="store_true")
    parser.add_argument("--no-reset-session", dest="reset_session", action="store_false")
    parser.set_defaults(reset_session=None)
    parser.set_defaults(consult_template=True)
    parser.set_defaults(normalize_chair_prompt=True)
    return parser


def load_prompt(args: argparse.Namespace) -> str:
    if args.prompt and args.prompt_file:
        raise SystemExit("Use either --prompt or --prompt-file, not both.")
    if args.prompt_file:
        return args.prompt_file.read_text(encoding="utf-8")
    if args.prompt:
        return args.prompt
    raise SystemExit("One of --prompt or --prompt-file is required.")


def print_json(payload: dict[str, object]) -> None:
    sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def build_openclaw_command(session_key: str, reset_session: bool) -> list[str]:
    openclaw_bin = str(OPENCLAW_BIN if OPENCLAW_BIN.exists() else "openclaw")
    script_bin = str(SCRIPT_BIN if SCRIPT_BIN.exists() else "script")
    cmd = [script_bin, "-q", "/dev/null", openclaw_bin, "acp", "--session", session_key, "--no-prefix-cwd"]
    if reset_session:
        cmd.append("--reset-session")
    return cmd


def build_initialize_request() -> dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": INIT_REQUEST_ID,
        "method": "initialize",
        "params": {
            "protocolVersion": 1,
            "clientCapabilities": {
                "fs": {"readTextFile": True, "writeTextFile": True},
                "terminal": True,
            },
            "clientInfo": {"name": "openclaw-agent-query", "version": "0.2"},
        },
    }


def build_load_request(session_key: str, cwd: Path) -> dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": LOAD_REQUEST_ID,
        "method": "session/load",
        "params": {
            "sessionId": session_key,
            "cwd": str(cwd.resolve()),
            "mcpServers": [],
        },
    }


def build_prompt_request(session_key: str, prompt_text: str) -> dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": PROMPT_REQUEST_ID,
        "method": "session/prompt",
        "params": {
            "sessionId": session_key,
            "prompt": [{"type": "text", "text": prompt_text}],
        },
    }


def extract_text_chunk(value: Any) -> str | None:
    if isinstance(value, str):
        return value if value else None
    if not isinstance(value, dict):
        return None
    content_type = value.get("type")
    if isinstance(content_type, str) and content_type and content_type != "text":
        return None
    text = value.get("text")
    return text if isinstance(text, str) and text else None


def parse_prompt_stream_event(payload: dict[str, Any]) -> dict[str, Any] | None:
    event_type = payload.get("type")
    if event_type == "text":
        text = extract_text_chunk(payload.get("content")) or extract_text_chunk(payload.get("text"))
        return {"kind": "text", "text": text} if text else None
    if event_type == "done":
        stop = payload.get("stopReason")
        return {
            "kind": "done",
            "stop_reason": stop if isinstance(stop, str) and stop else None,
        }
    if event_type == "error":
        message = payload.get("message")
        return {
            "kind": "error",
            "message": message if isinstance(message, str) and message else "acp runtime error",
        }

    update_payload = payload
    params = payload.get("params")
    if isinstance(params, dict):
        update = params.get("update")
        if isinstance(update, dict):
            update_payload = update

    session_update = update_payload.get("sessionUpdate")
    if session_update == "agent_message_chunk":
        text = extract_text_chunk(update_payload.get("content")) or extract_text_chunk(update_payload.get("text"))
        return {"kind": "text", "text": text} if text else None
    return None


def extract_message_text(content: Any) -> str | None:
    items = content if isinstance(content, list) else [content]
    texts: list[str] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        if item.get("type") != "text":
            continue
        text = item.get("text")
        if isinstance(text, str) and text:
            texts.append(text)
    combined = "".join(texts).strip()
    return combined or None


def find_transcript_recovery_candidates(agent_id: str, cwd: Path, started_at: float) -> list[Path]:
    sessions_dir = cwd.resolve() / "agents" / agent_id / "sessions"
    if not sessions_dir.is_dir():
        return []
    candidates: list[Path] = []
    min_mtime = started_at - TRANSCRIPT_RECOVERY_FILE_WINDOW_SECONDS
    for path in sessions_dir.glob("*.jsonl"):
        try:
            if path.stat().st_mtime < min_mtime:
                continue
        except OSError:
            continue
        candidates.append(path)
    candidates.sort(key=lambda item: item.stat().st_mtime, reverse=True)
    return candidates[:TRANSCRIPT_RECOVERY_CANDIDATE_LIMIT]


def recover_output_from_transcript_once(
    *,
    agent_id: str,
    prompt_text: str,
    cwd: Path,
    started_at: float,
) -> str | None:
    prompt_snippet = prompt_text.strip()
    if not prompt_snippet:
        return None
    for path in find_transcript_recovery_candidates(agent_id=agent_id, cwd=cwd, started_at=started_at):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        matched_prompt = False
        for line in lines:
            try:
                payload = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(payload, dict):
                continue
            message_wrapper = payload.get("message")
            if not isinstance(message_wrapper, dict):
                continue
            role = message_wrapper.get("role")
            if role == "user":
                text = extract_message_text(message_wrapper.get("content"))
                if text and prompt_snippet in text:
                    matched_prompt = True
                continue
            if role == "assistant" and matched_prompt:
                text = extract_message_text(message_wrapper.get("content"))
                if text:
                    return text
    return None


def recover_output_from_transcript(
    *,
    agent_id: str,
    prompt_text: str,
    cwd: Path,
    started_at: float,
    wait_seconds: float = TRANSCRIPT_RECOVERY_WAIT_SECONDS,
) -> str | None:
    deadline = time.time() + max(0.0, wait_seconds)
    while True:
        recovered = recover_output_from_transcript_once(
            agent_id=agent_id,
            prompt_text=prompt_text,
            cwd=cwd,
            started_at=started_at,
        )
        if recovered:
            return recovered
        if time.time() >= deadline:
            return None
        time.sleep(TRANSCRIPT_RECOVERY_POLL_SECONDS)


def send_json_line(fd: int, payload: dict[str, Any], echoed_requests: deque[str]) -> None:
    line = json.dumps(payload, ensure_ascii=False) + "\n"
    echoed_requests.append(line.rstrip("\n"))
    os.write(fd, line.encode("utf-8"))


def terminate_child(pid: int, fd: int) -> None:
    try:
        os.close(fd)
    except OSError:
        pass
    for signum in (signal.SIGTERM, signal.SIGKILL):
        try:
            waited_pid, _status = os.waitpid(pid, os.WNOHANG)
        except ChildProcessError:
            return
        if waited_pid == pid:
            return
        try:
            os.kill(pid, signum)
        except ProcessLookupError:
            return
        deadline = time.monotonic() + (1.0 if signum == signal.SIGTERM else 0.2)
        while time.monotonic() < deadline:
            try:
                waited_pid, _status = os.waitpid(pid, os.WNOHANG)
            except ChildProcessError:
                return
            if waited_pid == pid:
                return
            time.sleep(0.05)


def acquire_bridge_lock() -> int:
    lock_fd = os.open(str(LOCK_FILE), os.O_CREAT | os.O_RDWR, 0o600)
    fcntl.flock(lock_fd, fcntl.LOCK_EX)
    return lock_fd


def spawn_acp_bridge(session_key: str, reset_session: bool) -> tuple[int, int]:
    pid, fd = pty.fork()
    if pid == 0:
        try:
            command = build_openclaw_command(session_key, reset_session)
            env = os.environ.copy()
            env["PATH"] = f"{PATH_PREFIX}:{env.get('PATH', '')}".rstrip(":")
            os.execvpe(command[0], command, env)
        except Exception as exc:
            sys.stderr.write(f"failed to exec openclaw acp bridge: {exc}\n")
            sys.stderr.flush()
            os._exit(1)
    return pid, fd


def run_query(
    *,
    agent_id: str,
    session_key: str,
    prompt_text: str,
    timeout: int,
    cwd: Path,
    reset_session: bool,
) -> dict[str, Any]:
    lock_fd = acquire_bridge_lock()
    pid, fd = spawn_acp_bridge(session_key=session_key, reset_session=reset_session)
    echoed_requests: deque[str] = deque()
    logs: list[str] = []
    json_events: list[str] = []
    chunks: list[str] = []
    stop_reason: str | None = None
    phase = "init"
    buffer = ""
    deadline = time.monotonic() + timeout
    started_at = time.time()

    try:
        time.sleep(STARTUP_DELAY_SECONDS)
        send_json_line(fd, build_initialize_request(), echoed_requests)
        while time.monotonic() < deadline:
            remaining = max(0.0, deadline - time.monotonic())
            ready, _, _ = select.select([fd], [], [], min(0.5, remaining))
            if not ready:
                continue
            try:
                data = os.read(fd, 4096)
            except OSError as exc:
                return {
                    "ok": False,
                    "returncode": 1,
                    "output": "".join(chunks).strip(),
                    "stop_reason": stop_reason,
                    "stderr": f"ACP bridge read failed: {exc}",
                }
            if not data:
                break
            buffer += data.decode("utf-8", errors="replace")
            while "\n" in buffer:
                raw_line, buffer = buffer.split("\n", 1)
                line = raw_line.rstrip("\r")
                if not line:
                    continue
                if echoed_requests and echoed_requests[0] == line:
                    echoed_requests.popleft()
                    continue
                try:
                    payload = json.loads(line)
                except json.JSONDecodeError:
                    logs.append(line)
                    continue
                if not isinstance(payload, dict):
                    continue
                json_events.append(line)
                error = payload.get("error")
                if isinstance(error, dict):
                    message = error.get("message")
                    return {
                        "ok": False,
                        "returncode": 1,
                        "output": "".join(chunks).strip(),
                        "stop_reason": stop_reason,
                        "stderr": str(message) if message else line,
                    }
                stream_event = parse_prompt_stream_event(payload)
                if stream_event:
                    kind = stream_event.get("kind")
                    if kind == "text":
                        text = stream_event.get("text")
                        if isinstance(text, str) and text:
                            chunks.append(text)
                        continue
                    if kind == "done":
                        stop = stream_event.get("stop_reason")
                        stop_reason = stop if isinstance(stop, str) and stop else None
                        output_text = "".join(chunks).strip()
                        if not output_text:
                            recovered_output = recover_output_from_transcript(
                                agent_id=agent_id,
                                prompt_text=prompt_text,
                                cwd=cwd,
                                started_at=started_at,
                            )
                            if recovered_output:
                                output_text = recovered_output
                        return {
                            "ok": bool(output_text),
                            "returncode": 0 if output_text else 1,
                            "output": output_text,
                            "stop_reason": stop_reason,
                            "stderr": "\n".join((logs + json_events)[-20:]).strip(),
                        }
                    if kind == "error":
                        message = stream_event.get("message")
                        return {
                            "ok": False,
                            "returncode": 1,
                            "output": "".join(chunks).strip(),
                            "stop_reason": stop_reason,
                            "stderr": str(message) if message else line,
                        }
                result = payload.get("result")
                request_id = payload.get("id")
                if request_id == INIT_REQUEST_ID and isinstance(result, dict) and phase == "init":
                    send_json_line(fd, build_load_request(session_key=session_key, cwd=cwd), echoed_requests)
                    phase = "load"
                    continue
                if request_id == LOAD_REQUEST_ID and isinstance(result, dict) and phase == "load":
                    send_json_line(fd, build_prompt_request(session_key=session_key, prompt_text=prompt_text), echoed_requests)
                    phase = "prompt"
                    continue
                if request_id == PROMPT_REQUEST_ID and isinstance(result, dict) and phase == "prompt":
                    stop = result.get("stopReason")
                    stop_reason = stop if isinstance(stop, str) and stop else None
                    output_text = "".join(chunks).strip()
                    if not output_text:
                        recovered_output = recover_output_from_transcript(
                            agent_id=agent_id,
                            prompt_text=prompt_text,
                            cwd=cwd,
                            started_at=started_at,
                        )
                        if recovered_output:
                            output_text = recovered_output
                    return {
                        "ok": bool(output_text),
                        "returncode": 0 if output_text else 1,
                        "output": output_text,
                        "stop_reason": stop_reason,
                        "stderr": "\n".join((logs + json_events)[-20:]).strip(),
                    }
        output_text = "".join(chunks).strip()
        return {
            "ok": False,
            "returncode": 3,
            "output": output_text,
            "stop_reason": stop_reason,
            "stderr": "\n".join((logs + json_events)[-20:]).strip(),
        }
    finally:
        terminate_child(pid, fd)
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
        finally:
            os.close(lock_fd)


def main() -> int:
    args = build_parser().parse_args()
    agent_id = normalize_agent_id(args.agent)
    prompt_text = load_prompt(args).strip()
    session_key = args.session_key or build_session_key(
        agent_id=agent_id,
        suffix=args.session_suffix,
        persistent=args.persistent,
    )
    reset_session = (not args.persistent) if args.reset_session is None else args.reset_session
    effective_prompt = build_consult_prompt(agent_id, prompt_text) if args.consult_template else prompt_text
    effective_prompt, prompt_normalized = normalize_chair_prompt(agent_id, effective_prompt) if args.normalize_chair_prompt else (effective_prompt, False)
    retry_on_empty = args.retry_on_empty if args.retry_on_empty is not None else (1 if prompt_normalized else 0)

    attempt_index = 0
    attempts_made = 0
    result: dict[str, Any] | None = None
    while attempt_index <= retry_on_empty:
        attempt_session_key = build_retry_session_key(session_key, attempt_index, args.persistent)
        result = run_query(
            agent_id=agent_id,
            session_key=attempt_session_key,
            prompt_text=effective_prompt,
            timeout=args.timeout,
            cwd=args.cwd,
            reset_session=reset_session,
        )
        attempts_made += 1
        if not should_retry_empty(result):
            session_key = attempt_session_key
            break
        session_key = attempt_session_key
        attempt_index += 1
    assert result is not None

    payload = {
        "ok": result["ok"],
        "agent_id": agent_id,
        "session_key": session_key,
        "reset_session": reset_session,
        "attempts": attempts_made,
        "prompt_normalized": prompt_normalized,
        "returncode": result["returncode"],
        "output": result["output"],
        "stop_reason": result["stop_reason"],
        "stderr": result["stderr"],
    }

    if args.format == "json":
        print_json(payload)
        return 0 if payload["ok"] else 1

    if payload["ok"]:
        output_text = str(payload["output"])
        sys.stdout.write(output_text + ("\n" if not output_text.endswith("\n") else ""))
        return 0

    message = str(payload["stderr"] or payload["output"] or f"ACP query failed for agent `{agent_id}`.")
    sys.stderr.write(message + ("\n" if not message.endswith("\n") else ""))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
