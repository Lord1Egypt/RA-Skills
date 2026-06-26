#!/usr/bin/env python3
"""确定性 presence tick 入口。

cron 只负责调用本脚本。本脚本先在普通进程里执行 prepare；只有命中当前
day-schedule 事件时，才把已经生成好的合同交给稳定 companion session。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import time
import subprocess
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OPENCLAW_HOME = ROOT.parents[2]
SESSIONS_DIR = OPENCLAW_HOME / "agents" / "main" / "sessions"
COMPANION_RUN = ROOT / "scripts" / "companion_run.py"
DEFAULT_CONFIG = ROOT / "config.local.json"
DEFAULT_SESSION_KEY = "agent:main:companion-runtime"
DEFAULT_DISPATCH_LOCK = ROOT / "state" / "presence-dispatch.json"
DEFAULT_DISPATCH_LOG_DIR = ROOT / "state" / "presence-dispatch-logs"
DEFAULT_DISPATCH_TTL_SECONDS = 45 * 60
# If the dispatch lock status is still "agent_enqueued" after this many seconds,
# the agent session likely failed to start. The lock is treated as stale
# so the next tick can recover.
DEFAULT_DISPATCH_STALL_SECONDS = 300
DEFAULT_AGENT_START_WAIT_SECONDS = 8.0
DEFAULT_AGENT_START_POLL_SECONDS = 0.25
DEFAULT_AGENT_LAUNCH_ATTEMPTS = 3
DEFAULT_AGENT_LAUNCH_RETRY_DELAY_SECONDS = 4.0
DEFAULT_RECENT_MEDIA_WATCH_SECONDS = 900
DEFAULT_RECENT_MEDIA_POLL_SECONDS = 5.0
NODE_CA_OPTION_FLAGS = {"--use-system-ca", "--use-openssl-ca", "--use-bundled-ca"}
WRONG_MEDIA_ROUTE_MARKERS = (
    "internal-ui",
    "current webchat conversation",
    "current/original chat",
)
MEDIA_TASK_KINDS = {"image_generation", "video_generation", "music_generation", "audio_generation"}


def openclaw_child_env(base_env: dict[str, str] | None = None) -> dict[str, str]:
    """Build a stable environment for OpenClaw CLI children launched by cron."""
    env = dict(base_env or os.environ)
    env["NODE_USE_SYSTEM_CA"] = "0"
    raw_options = env.get("NODE_OPTIONS", "")
    try:
        node_options = shlex.split(raw_options)
    except ValueError:
        node_options = raw_options.split()
    node_options = [option for option in node_options if option not in NODE_CA_OPTION_FLAGS]
    node_options.append("--use-bundled-ca")
    env["NODE_OPTIONS"] = " ".join(node_options)
    return env


def openclaw_child_cwd() -> str:
    """Run OpenClaw CLI children from ~/.openclaw, not the workspace.

    Codex app-server `workspace-write` turns derive writable roots from `cwd`.
    When a gateway fallback runs embedded from the workspace, the resulting
    writable roots exclude `~/.openclaw/agents/.../sessions`, which breaks
    stable-session persistence with EPERM. Launching the CLI from the OpenClaw
    home keeps the session state tree inside the writable root.
    """
    return str(OPENCLAW_HOME)


def run_json(command: list[str]) -> dict:
    env = None
    cwd = None
    if Path(command[0]).name == "openclaw":
        env = openclaw_child_env()
        cwd = openclaw_child_cwd()
    result = subprocess.run(command, text=True, capture_output=True, check=False, env=env, cwd=cwd)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or f"command failed: {command}")
    stdout = result.stdout.strip()
    stderr = result.stderr.strip()
    raw_output = stdout or stderr
    try:
        return json.loads(raw_output)
    except json.JSONDecodeError as exc:
        fallback = extract_json_object(raw_output)
        if fallback:
            return fallback
        details = []
        if stdout:
            details.append(f"stdout={stdout[:500]}")
        if stderr:
            details.append(f"stderr={stderr[:500]}")
        raise RuntimeError("command did not return JSON: " + "; ".join(details)) from exc


def extract_json_object(text: str) -> dict:
    """Extract the first complete JSON object from CLI output with log prefixes."""
    if not text:
        return {}
    for start, char in enumerate(text):
        if char != "{":
            continue
        depth = 0
        in_string = False
        escape = False
        for index in range(start, len(text)):
            current = text[index]
            if in_string:
                if escape:
                    escape = False
                elif current == "\\":
                    escape = True
                elif current == '"':
                    in_string = False
                continue
            if current == '"':
                in_string = True
            elif current == "{":
                depth += 1
            elif current == "}":
                depth -= 1
                if depth == 0:
                    candidate = text[start : index + 1]
                    try:
                        parsed = json.loads(candidate)
                    except json.JSONDecodeError:
                        break
                    return parsed if isinstance(parsed, dict) else {}
    return {}


def load_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def save_json(path: Path, payload: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def tail_text(path: Path, max_chars: int = 1200) -> str:
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8", errors="replace")
    return text[-max_chars:]


def diagnostic_tail_text(path: Path, max_chars: int = 1200) -> str:
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8", errors="replace")
    marker_lines = [
        line
        for line in text.splitlines()
        if line.startswith("ERROR:")
        or "OAuth token refresh failed" in line
        or "SecItemCopyMatching" in line
        or line.startswith("Traceback ")
    ]
    if marker_lines:
        return "\n".join(marker_lines[-8:])[-max_chars:]
    return text[-max_chars:]


def log_file_name(run_id: str, now_epoch: int) -> str:
    safe_run_id = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in (run_id or "presence"))
    return f"{time.strftime('%Y%m%d-%H%M%S', time.localtime(now_epoch))}-{safe_run_id}.log"


def retryable_agent_launch_failure(error_text: str) -> bool:
    text = (error_text or "").lower()
    if not text:
        return False
    return any(
        needle in text
        for needle in (
            "gateway closed (1006",
            "gateway agent failed",
            "secitemcopymatching failed -50",
            "sessions.json.",
            "eperm: operation not permitted",
        )
    )


def prepare_command(config_path: Path) -> list[str]:
    return [
        sys.executable,
        str(COMPANION_RUN),
        "--stage",
        "prepare",
        "--config",
        str(config_path),
        "--no-record-pending",
    ]


def send_notification(contract: dict, dry_run: bool = False) -> dict:
    delivery = contract.get("delivery_contract", {}) if isinstance(contract.get("delivery_contract"), dict) else {}
    text = str(contract.get("notification_text") or "").strip()
    if not text:
        return {"status": "skip", "reason": "empty_notification_text"}
    result = send_text_with_delivery_contract(delivery, text, dry_run=dry_run)
    return {"status": "notification_sent", "delivery_result": result}


def parse_json_object_arg(value: str, label: str) -> dict:
    try:
        payload = json.loads(value or "{}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid {label}: {exc}") from exc
    if not isinstance(payload, dict):
        raise SystemExit(f"invalid {label}: expected JSON object")
    return payload


def media_send_command(delivery: dict, media: str, message: str = "") -> list[str]:
    channel = str(delivery.get("channel") or "").strip()
    target = str(delivery.get("target") or delivery.get("owner_target") or "").strip()
    account = str(delivery.get("account") or "").strip()
    media_ref = str(media or "").strip()
    if not channel:
        raise ValueError("delivery_contract.channel is required")
    if not target:
        raise ValueError("delivery_contract.target is required")
    if not media_ref:
        raise ValueError("media path or URL is required")
    command = [
        "openclaw",
        "message",
        "send",
        "--json",
        "--channel",
        channel,
        "--target",
        target,
        "--media",
        media_ref,
    ]
    if account:
        command.extend(["--account", account])
    if str(message or "").strip():
        command.extend(["--message", str(message).strip()])
    return command


def text_send_command(delivery: dict, text: str) -> list[str]:
    channel = str(delivery.get("channel") or "").strip()
    target = str(delivery.get("target") or delivery.get("owner_target") or "").strip()
    account = str(delivery.get("account") or "").strip()
    body = str(text or "").strip()
    if not channel:
        raise ValueError("delivery_contract.channel is required")
    if not target:
        raise ValueError("delivery_contract.target is required")
    if not body:
        raise ValueError("story text is required")
    command = [
        "openclaw",
        "message",
        "send",
        "--json",
        "--channel",
        channel,
        "--target",
        target,
        "--message",
        body,
    ]
    if account:
        command.extend(["--account", account])
    return command


def delivery_result_has_wrong_media_route(result: dict) -> bool:
    text = json.dumps(result, ensure_ascii=False).lower() if isinstance(result, dict) else str(result).lower()
    return any(marker in text for marker in WRONG_MEDIA_ROUTE_MARKERS)


MEDIA_PATH_RE = re.compile(r"(/[^\s\"']+\.(?:png|jpg|jpeg|webp|gif|mp4|mov|mp3|wav|m4a))", re.IGNORECASE)


def extract_media_paths_from_task(task: dict) -> list[str]:
    paths = []
    for key in ("terminalSummary", "progressSummary", "result", "output"):
        value = task.get(key)
        if not value:
            continue
        text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
        for match in MEDIA_PATH_RE.findall(text):
            cleaned = match.rstrip(".,;)")
            if cleaned not in paths:
                paths.append(cleaned)
    return paths


def parse_timestamp_ms(value) -> int:
    if isinstance(value, (int, float)):
        value = int(value)
        return value if value > 10_000_000_000 else value * 1000
    if isinstance(value, str):
        raw = value.strip()
        if not raw:
            return 0
        try:
            return int(datetime.fromisoformat(raw.replace("Z", "+00:00")).timestamp() * 1000)
        except ValueError:
            return 0
    return 0


def recent_session_jsonl_paths(started_after_ms: int = 0) -> list[Path]:
    if not SESSIONS_DIR.exists():
        return []
    candidates = []
    for path in SESSIONS_DIR.glob("*.jsonl"):
        try:
            stat = path.stat()
        except OSError:
            continue
        modified_ms = int(stat.st_mtime * 1000)
        if started_after_ms and modified_ms < started_after_ms:
            continue
        candidates.append((modified_ms, path))
    candidates.sort(key=lambda item: item[0], reverse=True)
    return [path for _, path in candidates]


def extract_media_paths_from_completion_session(task_id: str, *, started_after_ms: int = 0) -> list[str]:
    task_ref = str(task_id or "").strip()
    if not task_ref:
        return []
    paths = []
    task_markers = (
        task_ref,
        f"image_generate:{task_ref}",
        f"video_generate:{task_ref}",
        f"music_generate:{task_ref}",
        f"audio_generate:{task_ref}",
    )
    for path in recent_session_jsonl_paths(started_after_ms):
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for line in reversed(lines):
            if not any(marker in line for marker in task_markers):
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            message = row.get("message", {}) if isinstance(row, dict) else {}
            if not isinstance(message, dict) or message.get("role") != "user":
                continue
            content = message.get("content")
            if not isinstance(content, str) or "Attachments:" not in content:
                continue
            event_ts = parse_timestamp_ms(message.get("timestamp"))
            if started_after_ms and event_ts and event_ts < started_after_ms:
                continue
            for match in MEDIA_PATH_RE.findall(content):
                cleaned = match.rstrip(".,;)")
                if cleaned not in paths:
                    paths.append(cleaned)
            if paths:
                return paths
    return paths


def wait_for_media_task_and_send(
    task_id: str,
    delivery: dict,
    *,
    message: str = "",
    timeout_seconds: int = 420,
    poll_seconds: float = 5.0,
    dry_run: bool = False,
    started_after_ms: int = 0,
) -> dict:
    task_ref = str(task_id or "").strip()
    if not task_ref:
        raise ValueError("task id is required")
    deadline = time.time() + max(int(timeout_seconds), 1)
    last_task = {}
    while time.time() <= deadline:
        task = run_json(["openclaw", "tasks", "show", task_ref, "--json"])
        last_task = task
        status = str(task.get("status") or "")
        if status == "succeeded":
            media_paths = extract_media_paths_from_task(task)
            if not media_paths:
                media_paths = extract_media_paths_from_completion_session(
                    task_ref,
                    started_after_ms=int(started_after_ms),
                )
            if not media_paths:
                raise RuntimeError(f"media task succeeded but no media path was found: {task_ref}")
            send_result = send_media_with_delivery_contract(delivery, media_paths, message=message, dry_run=dry_run)
            return {
                "status": "media_task_sent",
                "task_id": task_ref,
                "media_paths": media_paths,
                "send_result": send_result,
            }
        if status in {"failed", "timed_out", "cancelled", "lost"}:
            return {
                "status": "media_task_failed",
                "task_id": task_ref,
                "task_status": status,
                "task": task,
            }
        time.sleep(max(float(poll_seconds), 0.5))
    return {
        "status": "media_task_timeout",
        "task_id": task_ref,
        "last_task_status": str(last_task.get("status") or ""),
        "last_task": last_task,
    }


def list_openclaw_tasks() -> list[dict]:
    payload = run_json(["openclaw", "tasks", "list", "--json"])
    tasks = payload.get("tasks", []) if isinstance(payload, dict) else []
    return [task for task in tasks if isinstance(task, dict)]


def is_media_task(task: dict) -> bool:
    task_kind = str(task.get("taskKind") or "").strip()
    source_id = str(task.get("sourceId") or "").strip()
    label = str(task.get("label") or "").strip().lower()
    return (
        task_kind in MEDIA_TASK_KINDS
        or source_id.startswith(("image_generate:", "video_generate:", "music_generate:", "audio_generate:"))
        or label in {"image generation", "video generation", "music generation", "audio generation"}
    )


def media_task_matches(task: dict, *, session_key: str, started_after_ms: int) -> bool:
    if not is_media_task(task):
        return False
    task_id = str(task.get("taskId") or "").strip()
    if not task_id:
        return False
    if session_key:
        session_fields = (
            str(task.get("requesterSessionKey") or ""),
            str(task.get("ownerKey") or ""),
            str(task.get("childSessionKey") or ""),
        )
        if session_key not in session_fields:
            return False
    created_at = int(task.get("createdAt") or task.get("startedAt") or 0)
    return bool(created_at and created_at >= int(started_after_ms))


def select_recent_media_task(tasks: list[dict], *, session_key: str, started_after_ms: int) -> dict:
    matches = [
        task
        for task in tasks
        if media_task_matches(task, session_key=session_key, started_after_ms=started_after_ms)
    ]
    matches.sort(key=lambda task: int(task.get("createdAt") or task.get("startedAt") or 0))
    return matches[0] if matches else {}


def wait_for_recent_media_task_and_send(
    delivery: dict,
    *,
    session_key: str,
    started_after_ms: int,
    message: str = "",
    timeout_seconds: int = DEFAULT_RECENT_MEDIA_WATCH_SECONDS,
    poll_seconds: float = DEFAULT_RECENT_MEDIA_POLL_SECONDS,
    dry_run: bool = False,
) -> dict:
    deadline = time.time() + max(int(timeout_seconds), 1)
    last_seen_status = ""
    while time.time() <= deadline:
        task = select_recent_media_task(
            list_openclaw_tasks(),
            session_key=session_key,
            started_after_ms=int(started_after_ms),
        )
        if not task:
            time.sleep(max(float(poll_seconds), 0.5))
            continue
        task_id = str(task.get("taskId") or "").strip()
        status = str(task.get("status") or "")
        last_seen_status = status
        if status == "succeeded":
            return wait_for_media_task_and_send(
                task_id,
                delivery,
                message=message,
                timeout_seconds=1,
                poll_seconds=0.5,
                dry_run=dry_run,
                started_after_ms=int(started_after_ms),
            )
        if status in {"failed", "timed_out", "cancelled", "lost"}:
            return {
                "status": "media_task_failed",
                "task_id": task_id,
                "task_status": status,
                "task": task,
            }
        time.sleep(max(float(poll_seconds), 0.5))
    return {
        "status": "recent_media_task_timeout",
        "session_key": session_key,
        "started_after_ms": int(started_after_ms),
        "last_seen_status": last_seen_status,
    }


def send_media_with_delivery_contract(delivery: dict, media_items: list[str], message: str = "", dry_run: bool = False) -> dict:
    """Send generated media through explicit delivery fields.

    This is the deterministic media-completion entrypoint. It intentionally
    bypasses the agent session's "current chat" context so async completions
    cannot fall back to webchat/internal-ui.
    """
    media_refs = [str(item).strip() for item in media_items if str(item or "").strip()]
    if not media_refs:
        return {"status": "skip", "reason": "empty_media"}
    results = []
    for media_ref in media_refs:
        command = media_send_command(delivery, media_ref, message=message)
        if dry_run:
            results.append({"media": media_ref, "command": command})
            continue
        first_result = run_json(command)
        if delivery_result_has_wrong_media_route(first_result):
            retry_result = run_json(command)
            results.append(
                {
                    "media": media_ref,
                    "status": "resent_after_wrong_route",
                    "wrong_route_detected": True,
                    "first_result": first_result,
                    "retry_result": retry_result,
                }
            )
            continue
        results.append({"media": media_ref, "status": "sent", "result": first_result})
    return {
        "status": "dry_run" if dry_run else "media_sent",
        "count": len(media_refs),
        "results": results,
    }


def send_text_with_delivery_contract(delivery: dict, text: str, dry_run: bool = False) -> dict:
    command = text_send_command(delivery, text)
    if dry_run:
        return {"status": "dry_run", "command": command}
    return run_json(command)


def run_state_commit(command: list[str], dry_run: bool = False) -> dict:
    if not isinstance(command, list) or not command:
        return {"status": "skip", "reason": "empty_state_commit_command"}
    if dry_run:
        return {"status": "dry_run", "command": command}
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or f"state commit failed: {command}")
    raw_output = (result.stdout or result.stderr or "").strip()
    if not raw_output:
        return {"status": "state_committed", "output": ""}
    try:
        parsed = json.loads(raw_output)
    except json.JSONDecodeError:
        return {"status": "state_committed", "output": raw_output[:500]}
    return parsed if isinstance(parsed, dict) else {"status": "state_committed", "output": raw_output[:500]}


def load_contract_from_dispatch_lock(lock_path: Path, run_id: str = "") -> dict:
    lock = load_json(lock_path, {})
    if not isinstance(lock, dict) or not lock:
        raise ValueError("dispatch lock is missing")
    if run_id and lock.get("run_id") and lock.get("run_id") != run_id:
        raise ValueError("dispatch lock run_id mismatch")
    contract = lock.get("contract")
    if not isinstance(contract, dict):
        raise ValueError("dispatch lock is missing contract")
    return contract


def send_story_from_dispatch_lock(lock_path: Path, run_id: str, story: str, dry_run: bool = False) -> dict:
    contract = load_contract_from_dispatch_lock(lock_path, run_id=run_id)
    delivery = contract.get("delivery_contract", {}) if isinstance(contract.get("delivery_contract"), dict) else {}
    state_commit = contract.get("state_commit", {}) if isinstance(contract.get("state_commit"), dict) else {}
    send_result = send_text_with_delivery_contract(delivery, story, dry_run=dry_run)
    commit_result = run_state_commit(state_commit.get("command", []), dry_run=dry_run)
    if not dry_run:
        update_dispatch_lock_status(lock_path, "text_sent", run_id=run_id)
    return {
        "status": "story_sent",
        "run_id": str(contract.get("run_id", "")),
        "event_key": extract_event_key(contract),
        "delivery_result": send_result,
        "state_commit_result": commit_result,
        "has_media": event_has_media(contract),
    }


def compact_contract(contract: dict) -> str:
    return json.dumps(contract, ensure_ascii=False, separators=(",", ":"))


def notification_payload(contract: dict) -> dict:
    delivery = contract.get("delivery_contract", {}) if isinstance(contract.get("delivery_contract"), dict) else {}
    text = str(contract.get("notification_text") or "").strip()
    return {
        "status": "notification_ready" if text else "skip",
        "reason": "" if text else "empty_notification_text",
        "notification_text": text,
        "delivery_contract": delivery,
    }


def extract_event_key(contract: dict) -> str:
    command = contract.get("state_commit", {}).get("command", [])
    if isinstance(command, list) and "--event-key" in command:
        index = command.index("--event-key")
        if index + 1 < len(command):
            return str(command[index + 1])
    event = contract.get("life_context", {}).get("event", {})
    today = contract.get("life_context", {}).get("today", {})
    if isinstance(event, dict):
        return "|".join(
            [
                str(today.get("date", "")) if isinstance(today, dict) else "",
                str(event.get("start_time", "")),
                str(event.get("title", "")),
            ]
        ).strip("|")
    return ""


def normalize_delivery_target_for_session_key(channel: str, target: str) -> str:
    normalized_channel = str(channel or "").strip()
    normalized_target = str(target or "").strip()
    if not normalized_channel or not normalized_target:
        return ""
    if normalized_channel == "openclaw-weixin":
        return normalized_target.lower()
    return normalized_target


def delivery_session_key(delivery: dict, agent: str = "main") -> str:
    if not isinstance(delivery, dict):
        return ""
    channel = str(delivery.get("channel") or "").strip()
    target = normalize_delivery_target_for_session_key(channel, str(delivery.get("target") or ""))
    agent_name = str(agent or "main").strip() or "main"
    if not channel or not target:
        return ""
    return f"agent:{agent_name}:{channel}:direct:{target}"


def dispatch_is_locked(path: Path, event_key: str, now_epoch: int, max_stall_seconds: int = DEFAULT_DISPATCH_STALL_SECONDS) -> dict:
    """Check dispatch lock.

    Returns the lock dict if active and not stale. A lock with status
    "agent_enqueued" that has not moved to "agent_started" within
    max_stall_seconds is considered stale (the agent session never
    actually started) and return {} to allow recovery.
    """
    lock = load_json(path, {})
    if not isinstance(lock, dict):
        return {}
    if lock.get("event_key") != event_key:
        return {}
    expires_at = int(lock.get("expires_at") or 0)
    if expires_at and expires_at > now_epoch:
        status = str(lock.get("status") or "")
        if status in {"agent_launch_failed", "agent_start_timeout"}:
            return {}
        started_at = int(lock.get("started_at") or 0)
        # If the agent never confirmed it started, and the lock is older
        # than the stall threshold, treat as expired so the next tick
        # can retry. This prevents a failed dispatch from blocking
        # until TTL expiry.
        if status in ("agent_enqueued", "") and started_at and (now_epoch - started_at) > max_stall_seconds:
            return {}
        return lock
    return {}


def write_dispatch_lock(path: Path, contract: dict, session_key: str, ttl_seconds: int, now_epoch: int):
    event_key = extract_event_key(contract)
    if not event_key:
        return
    save_json(
        path,
        {
            "event_key": event_key,
            "run_id": contract.get("run_id", ""),
            "session_key": session_key,
            "started_at": now_epoch,
            "expires_at": now_epoch + ttl_seconds,
            "status": "agent_enqueued",
            "dispatch_attempt": int(load_json(path, {}).get("dispatch_attempt", 0)) + 1,
            "contract": contract,
        },
    )


def build_agent_message(contract: dict, lock_path: str = "", lock_run_id: str = "") -> str:
    contract_json = compact_contract(contract)
    delivery = contract.get("delivery_contract", {}) if isinstance(contract.get("delivery_contract"), dict) else {}
    explicit_delivery_args = []
    channel = str(delivery.get("channel") or "").strip()
    target = str(delivery.get("target") or "").strip()
    account = str(delivery.get("account") or "").strip()
    if channel:
        explicit_delivery_args.append(f'channel="{channel}"')
    if target:
        explicit_delivery_args.append(f'target="{target}"')
    if account:
        explicit_delivery_args.append(f'accountId="{account}"')
    delivery_override_block = ""
    explicit_delivery_signature = ", ".join(explicit_delivery_args)
    if explicit_delivery_args:
        delivery_override_block = (
            "\n固定投递要求：\n"
            f"- 本轮真实投递目标来自 delivery_contract（{explicit_delivery_signature}）。\n"
            "- 文本主消息不要调用 `message(action=\"send\")`；必须调用固定 `--send-story` 入口，让 wrapper 用外部 OpenClaw CLI 按 delivery_contract 投递。\n"
            "- 不要依赖当前 stable session 的默认投递上下文；这个 session 自己可能挂在 webchat/internal-ui，不是用户真正收到消息的聊天。\n"
            "- 后续媒体 completion 回到这个 stable session 时，发送附件也继续沿用同一组显式 delivery_contract 字段。\n"
        )
    story_lock_path = lock_path or "<dispatch-lock>"
    story_run_id = lock_run_id or str(contract.get("run_id", "")) or "<run-id>"
    send_story_entrypoint = (
        f'python3 "{Path(__file__).resolve()}" --send-story '
        f'--dispatch-lock "{story_lock_path}" --run-id "{story_run_id}" --story-stdin <<\'PRESENCE_STORY\'\n'
        "<你刚写好的完整 presence story 正文>\n"
        "PRESENCE_STORY"
    )
    media_delivery_entrypoint = (
        f'python3 "{Path(__file__).resolve()}" --send-media '
        f"--delivery-contract-json {shlex.quote(json.dumps(delivery, ensure_ascii=False, separators=(',', ':')))} "
        "--media '<generated-media-path-or-url>'"
    )
    media_delegate_rule = (
        "- wrapper 已经为本轮媒体事件启动后台 recent-media watcher；media_contract.tool_name 返回 `Background task started ... (<task-id>)` 后，不要再自己运行 watcher，也不要等待 completion turn 发附件；直接回复 NO_REPLY。\n"
        "- 如果你是在后续媒体 completion turn 中看到生成媒体路径或 URL，不要调用 `message(action=\"send\", attachments=...)`，也不要使用 current/original chat、webchat 或 internal-ui；默认回复 NO_REPLY，让 wrapper watcher 负责投递。\n"
        "- 只有人工排障明确要求你补发时，才允许每个媒体文件调用下面的固定入口发送：\n"
        f"  `{media_delivery_entrypoint}`\n"
        "- 固定发送入口会按 delivery_contract 显式调用 `openclaw message send --channel/--target/--account/--media`，并在返回结果出现 internal-ui/current webchat 标记时用同一合同自动重发一次。\n"
    )
    lock_update_line = (
        f'\n0. （开始处理前，先直接运行 `python3 "{Path(__file__).resolve()}" --dispatch-lock "{lock_path}" --run-id "{lock_run_id}" --update-dispatch-lock-status agent_started`，把 dispatch lock 更新成 `agent_started`，不需要再走 `openclaw shell`。）'
        if lock_path and lock_run_id
        else ""
    )
    return f"""这是本轮 companion-presence wrapper 已经 fresh prepare 后得到的唯一有效合同。{lock_update_line}{delivery_override_block}

硬规则：
1. 不要再运行 prepare，不要沿用旧 skip、旧 tool result、旧媒体 completion 或旧上下文判断。
2. 如果合同 status 不是 ok，只回复 NO_REPLY。
3. status=ok 时，只使用合同里的 life_context、delivery_contract、media_contract、state_commit 和 delivery_tracking。
4. 先写一段 companion 第一人称当前事件故事：符合人设，完整具体，有情绪和心理活动，不少于 160 个中文字符；有 user_interaction 时自然保留。不要在用户可见文本里出现脚本、JSON、cron、工具、模型、路由、状态值、步骤名、诊断或本机路径。
5. 必须从当前事件提取 2-4 个公开、非敏感关键词联网搜索，最多补 1-2 个小细节；不要搜索 owner 身份、私人关系、账号、频道、会话、本机路径、密钥、配置或状态。
6. 禁止调用 message(action="send") 投递文本。写好正文后，调用固定入口发送正文：
```bash
{send_story_entrypoint}
```
这个入口会按 delivery_contract 显式投递文本，成功后由脚本执行 state_commit.command；如果入口失败，不要提交状态，也不要继续媒体生成。
7. 如果 media_contract.kind != "event_media"，固定入口成功后只回复 NO_REPLY；不要自己运行 state_commit.command。
8. 如果 media_contract.kind == "event_media"，固定入口成功后再调用 media_contract.tool_name，参数使用 life_context.event.media_info。wrapper 已经启动后台 recent-media watcher 等待本次媒体任务完成并按 delivery_contract 发送媒体；你不要自己运行 watcher，也不要等媒体 completion turn 自己发。后续媒体 completion 回到本稳定 session 时，不运行 prepare、不写第二段、不再运行 state_commit.command，只回复 NO_REPLY。
9. 固定媒体入口：
{media_delegate_rule}10. 文本主消息和媒体 completion 都不允许直接用 message tool 投递；文本必须调用固定 `--send-story` 入口，媒体必须交给 wrapper watcher 或固定媒体入口。

合同：
{contract_json}
"""


def build_handoff_payload(contract: dict, *, session_key: str, lock_path: Path) -> dict:
    return {
        "status": "handoff_ready",
        "run_id": str(contract.get("run_id", "")),
        "event_key": extract_event_key(contract),
        "session_key": session_key,
        "dispatch_lock": str(lock_path),
        "agent_message": build_agent_message(
            contract,
            lock_path=str(lock_path),
            lock_run_id=str(contract.get("run_id", "")),
        ),
        "has_media": contract.get("media_contract", {}).get("kind") == "event_media",
    }


def maybe_launch_handoff_media_watcher(
    args,
    contract: dict,
    *,
    lock_path: Path,
    log_dir: Path,
    started_after_ms: int,
) -> dict:
    """Start the deterministic media watcher for handoff-only flow when needed.

    The live isolated cron now uses `--handoff-only` and `sessions_send` instead
    of the older shell-launched stable session path. The watcher must still be
    started by the wrapper; otherwise the stable session sends text, launches the
    async image task, replies NO_REPLY, and nobody explicitly delivers the media
    to the real owner channel.
    """
    if not event_has_media(contract):
        return {}
    try:
        return launch_recent_media_watcher(
            args,
            contract,
            lock_path=lock_path,
            log_dir=log_dir,
            started_after_ms=started_after_ms,
        )
    except Exception as exc:  # pragma: no cover - defensive diagnostics only
        return {"media_watcher_launch_error": str(exc)}


def update_dispatch_lock_status(lock_path: Path, status: str, run_id: str = "") -> bool:
    """Update the status field of the dispatch lock.

    Called by the agent session to confirm it started processing.
    Returns True if the lock was updated, False if lock missing or run_id mismatch.
    """
    lock = load_json(lock_path, {})
    if not isinstance(lock, dict) or not lock:
        return False
    if run_id and lock.get("run_id") and lock.get("run_id") != run_id:
        return False
    lock["status"] = status
    lock["last_status_at"] = int(time.time())
    save_json(lock_path, lock)
    return True


def finalize_dispatch_lock(
    lock_path: Path,
    *,
    status: str,
    run_id: str = "",
    launch_log: Path | None = None,
    process_id: int | None = None,
    exit_code: int | None = None,
    error: str = "",
) -> bool:
    """Record launch metadata or failure details on the dispatch lock."""
    lock = load_json(lock_path, {})
    if not isinstance(lock, dict) or not lock:
        return False
    if run_id and lock.get("run_id") and lock.get("run_id") != run_id:
        return False
    lock["status"] = status
    lock["last_status_at"] = int(time.time())
    if launch_log:
        lock["launch_log"] = str(launch_log)
    if process_id is not None:
        lock["agent_pid"] = int(process_id)
    if exit_code is not None:
        lock["exit_code"] = int(exit_code)
    if error:
        lock["error"] = error[:500]
    save_json(lock_path, lock)
    return True


def wait_for_agent_start(
    lock_path: Path,
    run_id: str,
    process: subprocess.Popen,
    *,
    wait_seconds: float,
    poll_seconds: float,
    launch_log: Path,
) -> dict:
    """Wait briefly for either an agent_started ack or an early process exit."""
    deadline = time.time() + max(wait_seconds, 0.0)
    while time.time() < deadline:
        lock = load_json(lock_path, {})
        if isinstance(lock, dict) and lock.get("run_id") == run_id and lock.get("status") == "agent_started":
            finalize_dispatch_lock(
                lock_path,
                status="agent_started",
                run_id=run_id,
                launch_log=launch_log,
                process_id=process.pid,
            )
            return {
                "status": "agent_started",
                "run_id": run_id,
                "agent_pid": process.pid,
                "dispatch_lock": str(lock_path),
                "launch_log": str(launch_log),
            }
        exit_code = process.poll()
        if exit_code is not None:
            stderr_tail = diagnostic_tail_text(launch_log)
            finalize_dispatch_lock(
                lock_path,
                status="agent_launch_failed",
                run_id=run_id,
                launch_log=launch_log,
                process_id=process.pid,
                exit_code=exit_code,
                error=stderr_tail,
            )
            return {
                "status": "agent_launch_failed",
                "run_id": run_id,
                "agent_pid": process.pid,
                "exit_code": exit_code,
                "dispatch_lock": str(lock_path),
                "launch_log": str(launch_log),
                "error_tail": stderr_tail,
            }
        time.sleep(max(poll_seconds, 0.05))

    finalize_dispatch_lock(
        lock_path,
        status="agent_enqueued",
        run_id=run_id,
        launch_log=launch_log,
        process_id=process.pid,
    )
    return {
        "status": "agent_enqueued",
        "run_id": run_id,
        "agent_pid": process.pid,
        "dispatch_lock": str(lock_path),
        "launch_log": str(launch_log),
        "waited_seconds": wait_seconds,
    }


def event_has_media(contract: dict) -> bool:
    media = contract.get("media_contract", {}) if isinstance(contract.get("media_contract"), dict) else {}
    return media.get("kind") == "event_media"


def record_media_watcher_launch(lock_path: Path, run_id: str, *, process_id: int, log_path: Path, started_after_ms: int) -> bool:
    lock = load_json(lock_path, {})
    if not isinstance(lock, dict) or not lock:
        return False
    if run_id and lock.get("run_id") and lock.get("run_id") != run_id:
        return False
    lock["media_watcher_pid"] = int(process_id)
    lock["media_watcher_log"] = str(log_path)
    lock["media_watcher_started_after_ms"] = int(started_after_ms)
    lock["last_status_at"] = int(time.time())
    save_json(lock_path, lock)
    return True


def launch_recent_media_watcher(
    args,
    contract: dict,
    *,
    lock_path: Path,
    log_dir: Path,
    started_after_ms: int,
) -> dict:
    delivery = contract.get("delivery_contract", {}) if isinstance(contract.get("delivery_contract"), dict) else {}
    command = [
        sys.executable,
        str(Path(__file__).resolve()),
        "--watch-recent-media-task",
        "--session-key",
        args.session_key,
        "--started-after-ms",
        str(int(started_after_ms)),
        "--delivery-contract-json",
        json.dumps(delivery, ensure_ascii=False, separators=(",", ":")),
        "--watch-timeout-seconds",
        str(args.recent_media_watch_seconds),
        "--watch-poll-seconds",
        str(args.recent_media_poll_seconds),
        "--dispatch-lock",
        str(lock_path),
        "--run-id",
        str(contract.get("run_id", "")),
    ]
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / log_file_name(f"{contract.get('run_id', 'presence')}-media-watcher", int(time.time()))
    with log_path.open("a", encoding="utf-8") as log_handle:
        log_handle.write(f"# media watcher {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))}\n")
        log_handle.write("command: " + json.dumps(command, ensure_ascii=False) + "\n")
        log_handle.flush()
        process = subprocess.Popen(
            command,
            stdout=log_handle,
            stderr=subprocess.STDOUT,
            start_new_session=True,
            text=True,
            env=openclaw_child_env(),
            cwd=openclaw_child_cwd(),
        )
    record_media_watcher_launch(
        lock_path,
        str(contract.get("run_id", "")),
        process_id=process.pid,
        log_path=log_path,
        started_after_ms=started_after_ms,
    )
    return {
        "media_watcher_pid": process.pid,
        "media_watcher_log": str(log_path),
        "media_watcher_started_after_ms": int(started_after_ms),
    }


def agent_command(args, message: str) -> list[str]:
    command = [
        "openclaw",
        "agent",
        "--session-key",
        args.session_key,
        "--message",
        message,
        "--timeout",
        str(args.agent_timeout_seconds),
        "--json",
    ]
    if args.agent:
        command.extend(["--agent", args.agent])
    if args.model:
        command.extend(["--model", args.model])
    if args.thinking:
        command.extend(["--thinking", args.thinking])
    return command


def parse_args():
    parser = argparse.ArgumentParser(description="Run one deterministic companion presence tick.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--session-key", default=DEFAULT_SESSION_KEY)
    parser.add_argument("--agent", default="main")
    parser.add_argument("--model", default="")
    parser.add_argument("--thinking", default="medium")
    parser.add_argument("--agent-timeout-seconds", type=int, default=600)
    parser.add_argument("--dispatch-lock", default=str(DEFAULT_DISPATCH_LOCK))
    parser.add_argument("--dispatch-log-dir", default=str(DEFAULT_DISPATCH_LOG_DIR))
    parser.add_argument("--dispatch-ttl-seconds", type=int, default=DEFAULT_DISPATCH_TTL_SECONDS)
    parser.add_argument("--dispatch-stall-seconds", type=int, default=DEFAULT_DISPATCH_STALL_SECONDS,
                        help="Grace period before a stuck 'agent_enqueued' lock is treated as stale.")
    parser.add_argument("--agent-start-wait-seconds", type=float, default=DEFAULT_AGENT_START_WAIT_SECONDS,
                        help="How long to wait for the stable agent to confirm startup before returning.")
    parser.add_argument("--agent-start-poll-seconds", type=float, default=DEFAULT_AGENT_START_POLL_SECONDS,
                        help="Polling interval while waiting for agent_started or early process exit.")
    parser.add_argument("--agent-launch-attempts", type=int, default=DEFAULT_AGENT_LAUNCH_ATTEMPTS,
                        help="How many times to retry launching the stable agent on transient startup failures.")
    parser.add_argument("--agent-launch-retry-delay-seconds", type=float, default=DEFAULT_AGENT_LAUNCH_RETRY_DELAY_SECONDS,
                        help="Delay between retryable stable-agent launch failures.")
    parser.add_argument("--update-dispatch-lock-status", default="",
                        help="Internal helper mode: update the dispatch lock and exit.")
    parser.add_argument("--run-id", default="", help="Run id for dispatch lock helper mode.")
    parser.add_argument(
        "--handoff-only",
        action="store_true",
        help="Prepare and return a stable-session handoff payload instead of launching `openclaw agent` from shell.",
    )
    parser.add_argument(
        "--send-story",
        action="store_true",
        help="Internal helper mode: send the generated presence story and commit state through the dispatch contract.",
    )
    parser.add_argument("--story", default="", help="Presence story text for --send-story.")
    parser.add_argument(
        "--story-stdin",
        action="store_true",
        help="Read presence story text for --send-story from stdin.",
    )
    parser.add_argument(
        "--send-media",
        action="store_true",
        help="Internal helper mode: send generated media through an explicit delivery contract.",
    )
    parser.add_argument("--delivery-contract-json", default="", help="JSON delivery contract for --send-media.")
    parser.add_argument("--media", action="append", default=[], help="Media path or URL for --send-media. Repeatable.")
    parser.add_argument("--message", default="", help="Optional caption for --send-media.")
    parser.add_argument(
        "--watch-media-task",
        action="store_true",
        help="Internal helper mode: wait for a media task, then send generated media with an explicit delivery contract.",
    )
    parser.add_argument("--task-id", default="", help="OpenClaw media task id for --watch-media-task.")
    parser.add_argument(
        "--watch-recent-media-task",
        action="store_true",
        help="Internal helper mode: find the next media task created by the stable session, then send it explicitly.",
    )
    parser.add_argument("--started-after-ms", type=int, default=0,
                        help="Only match recent media tasks created at or after this millisecond timestamp.")
    parser.add_argument("--watch-timeout-seconds", type=int, default=420)
    parser.add_argument("--watch-poll-seconds", type=float, default=5.0)
    parser.add_argument("--recent-media-watch-seconds", type=int, default=DEFAULT_RECENT_MEDIA_WATCH_SECONDS)
    parser.add_argument("--recent-media-poll-seconds", type=float, default=DEFAULT_RECENT_MEDIA_POLL_SECONDS)
    parser.add_argument("--dry-run", action="store_true", help="Run prepare but do not call OpenClaw delivery or agent.")
    return parser.parse_args()


def main():
    args = parse_args()
    config_path = Path(args.config).expanduser().resolve()
    lock_path = Path(args.dispatch_lock).expanduser().resolve()
    if args.update_dispatch_lock_status:
        updated = update_dispatch_lock_status(lock_path, args.update_dispatch_lock_status, run_id=args.run_id)
        print(
            json.dumps(
                {
                    "status": "dispatch_lock_updated" if updated else "dispatch_lock_update_skipped",
                    "dispatch_lock": str(lock_path),
                    "run_id": args.run_id,
                    "lock_status": args.update_dispatch_lock_status,
                },
                ensure_ascii=False,
            )
        )
        return
    if args.send_story:
        story = sys.stdin.read() if args.story_stdin else args.story
        try:
            result = send_story_from_dispatch_lock(
                lock_path,
                args.run_id,
                story,
                dry_run=args.dry_run,
            )
        except (ValueError, RuntimeError) as exc:
            raise SystemExit(str(exc)) from exc
        print(json.dumps(result, ensure_ascii=False))
        return
    if args.send_media:
        delivery = parse_json_object_arg(args.delivery_contract_json, "--delivery-contract-json")
        try:
            result = send_media_with_delivery_contract(
                delivery,
                args.media,
                message=args.message,
                dry_run=args.dry_run,
            )
        except ValueError as exc:
            raise SystemExit(str(exc)) from exc
        print(json.dumps(result, ensure_ascii=False))
        return
    if args.watch_media_task:
        delivery = parse_json_object_arg(args.delivery_contract_json, "--delivery-contract-json")
        try:
            result = wait_for_media_task_and_send(
                args.task_id,
                delivery,
                message=args.message,
                timeout_seconds=args.watch_timeout_seconds,
                poll_seconds=args.watch_poll_seconds,
                dry_run=args.dry_run,
            )
        except ValueError as exc:
            raise SystemExit(str(exc)) from exc
        print(json.dumps(result, ensure_ascii=False))
        return
    if args.watch_recent_media_task:
        delivery = parse_json_object_arg(args.delivery_contract_json, "--delivery-contract-json")
        result = wait_for_recent_media_task_and_send(
            delivery,
            session_key=args.session_key,
            started_after_ms=args.started_after_ms,
            message=args.message,
            timeout_seconds=args.watch_timeout_seconds,
            poll_seconds=args.watch_poll_seconds,
            dry_run=args.dry_run,
        )
        status = str(result.get("status") or "")
        if args.run_id and status:
            if status == "media_task_sent":
                update_dispatch_lock_status(lock_path, "media_sent", run_id=args.run_id)
            elif status in {"media_task_failed", "recent_media_task_timeout"}:
                update_dispatch_lock_status(lock_path, status, run_id=args.run_id)
        print(json.dumps(result, ensure_ascii=False))
        return
    contract = run_json(prepare_command(config_path))
    status = str(contract.get("status") or "")
    if status == "skip":
        print(json.dumps({"status": "skip", "reason": contract.get("reason", "")}, ensure_ascii=False))
        return
    if status == "notify_owner":
        if args.handoff_only:
            print(json.dumps(notification_payload(contract), ensure_ascii=False))
            return
        result = send_notification(contract, dry_run=args.dry_run)
        print(json.dumps({"status": result["status"], "prepare_status": status}, ensure_ascii=False))
        return
    if status != "ok":
        print(json.dumps({"status": "skip", "reason": f"prepare_status_{status or 'empty'}"}, ensure_ascii=False))
        return

    event_key = extract_event_key(contract)
    now_epoch = int(time.time())
    lock = dispatch_is_locked(lock_path, event_key, now_epoch, args.dispatch_stall_seconds) if event_key else {}
    if lock and not args.dry_run:
        started_at = int(lock.get("started_at") or 0)
        stalled_sec = now_epoch - started_at if started_at else 0
        print(
            json.dumps(
                {
                    "status": "skip",
                    "reason": "dispatch_in_flight",
                    "run_id": lock.get("run_id", ""),
                    "event_key": event_key,
                    "expires_at": lock.get("expires_at", 0),
                    "lock_status": lock.get("status", ""),
                    "stalled_seconds": stalled_sec,
                },
                ensure_ascii=False,
            )
        )
        return
    if args.handoff_only:
        if args.dry_run:
            payload = build_handoff_payload(contract, session_key=args.session_key, lock_path=lock_path)
            payload["status"] = "would_handoff_session"
            del payload["agent_message"]
            print(json.dumps(payload, ensure_ascii=False))
            return
        write_dispatch_lock(lock_path, contract, args.session_key, args.dispatch_ttl_seconds, now_epoch)
        payload = build_handoff_payload(contract, session_key=args.session_key, lock_path=lock_path)
        log_dir = Path(args.dispatch_log_dir).expanduser().resolve()
        log_dir.mkdir(parents=True, exist_ok=True)
        payload.update(
            maybe_launch_handoff_media_watcher(
                args,
                contract,
                lock_path=lock_path,
                log_dir=log_dir,
                started_after_ms=now_epoch * 1000,
            )
        )
        print(json.dumps(payload, ensure_ascii=False))
        return
    message = build_agent_message(contract, lock_path=str(lock_path), lock_run_id=str(contract.get("run_id", "")))
    command = agent_command(args, message)
    if args.dry_run:
        print(
            json.dumps(
                {
                    "status": "would_start_agent",
                    "run_id": contract.get("run_id", ""),
                    "session_key": args.session_key,
                    "has_media": contract.get("media_contract", {}).get("kind") == "event_media",
                    "command": command[:4] + ["..."],
                },
                ensure_ascii=False,
            )
        )
        return
    write_dispatch_lock(lock_path, contract, args.session_key, args.dispatch_ttl_seconds, now_epoch)
    log_dir = Path(args.dispatch_log_dir).expanduser().resolve()
    log_dir.mkdir(parents=True, exist_ok=True)
    launch_log = log_dir / log_file_name(str(contract.get("run_id", "")), now_epoch)
    attempts = max(int(args.agent_launch_attempts), 1)
    retry_delay = max(float(args.agent_launch_retry_delay_seconds), 0.0)
    result = None
    attempts_used = 0
    for attempt in range(1, attempts + 1):
        attempts_used = attempt
        with launch_log.open("a", encoding="utf-8") as log_handle:
            log_handle.write(f"# launch {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))} attempt={attempt}/{attempts}\n")
            log_handle.write("command: " + json.dumps(command, ensure_ascii=False) + "\n")
            log_handle.flush()
            process = subprocess.Popen(
                command,
                stdout=log_handle,
                stderr=subprocess.STDOUT,
                start_new_session=True,
                text=True,
                env=openclaw_child_env(),
                cwd=openclaw_child_cwd(),
            )

        result = wait_for_agent_start(
            lock_path,
            str(contract.get("run_id", "")),
            process,
            wait_seconds=args.agent_start_wait_seconds,
            poll_seconds=args.agent_start_poll_seconds,
            launch_log=launch_log,
        )
        if result.get("status") != "agent_launch_failed":
            break
        if attempt >= attempts:
            break
        error_tail = str(result.get("error_tail") or "")
        if not retryable_agent_launch_failure(error_tail):
            break
        with launch_log.open("a", encoding="utf-8") as log_handle:
            log_handle.write(
                f"# retrying after transient launch failure attempt={attempt}/{attempts} delay={retry_delay}s\n"
            )
        time.sleep(retry_delay)

    if result is None:
        result = {
            "status": "agent_launch_failed",
            "run_id": str(contract.get("run_id", "")),
            "dispatch_lock": str(lock_path),
            "launch_log": str(launch_log),
            "error_tail": "launch loop did not produce a result",
        }
    result["launch_attempts"] = attempts_used
    result["session_key"] = args.session_key
    result["event_key"] = event_key
    if result.get("status") != "agent_launch_failed" and event_has_media(contract):
        watcher = launch_recent_media_watcher(
            args,
            contract,
            lock_path=lock_path,
            log_dir=log_dir,
            started_after_ms=now_epoch * 1000,
        )
        result.update(watcher)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
