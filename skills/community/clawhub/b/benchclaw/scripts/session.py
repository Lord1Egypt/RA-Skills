from __future__ import annotations

import json
import logging
import os
import shutil
import subprocess
import sys
import time
import traceback
from pathlib import Path
from typing import Any, NamedTuple

from config import DEFAULT_AGENT_ID, DEFAULT_SESSION_PREFIX

SESSION_STORE_PATH = Path.home() / ".openclaw" / "agents" / "main" / "sessions" / "sessions.json"

DEFAULT_TASK_COUNT = 3
DEFAULT_TASK_SECONDS = 5
SESSION_LIST_TIMEOUT = 60
CHANNEL_MESSAGE_TIMEOUT = 60
AGENT_MESSAGE_TIMEOUT = 120
AGENT_MESSAGE_RETRY_COUNT = 1


logger = logging.getLogger("benchclaw.session")


class OpenClawSessionInfo(NamedTuple):
    """从 OpenClaw CLI / 会话存储解析出的通知目标（当前会话 + channel/target）。"""

    session_id: str
    session_key: str
    channel: str | None
    target: str | None


def ran_under_openclaw_exec() -> bool:
    """
    True when spawned from OpenClaw gateway `exec` (sanitized env + markers).
    Either OPENCLAW_SHELL=exec or OPENCLAW_CLI=1 suffices; manual `cmd` runs
    typically have neither.
    """
    return (
        os.environ.get("OPENCLAW_SHELL", "").strip() == "exec"
        or os.environ.get("OPENCLAW_CLI", "").strip() == "1"
    )

def parse_json_from_mixed_output(output: str) -> dict[str, Any]:
    """
    Parse JSON from output that may contain extra log lines.
    """
    lines = output.splitlines()
    buffer: list[str] = []
    depth = 0

    for line in lines:
        stripped = line.lstrip()
        if not buffer and not stripped.startswith("{"):
            continue

        buffer.append(line)
        depth += line.count("{") - line.count("}")

        if depth <= 0:
            candidate = "\n".join(buffer)
            try:
                parsed = json.loads(candidate)
                if isinstance(parsed, dict):
                    return parsed
            except json.JSONDecodeError:
                pass
            buffer = []
            depth = 0

    raise ValueError("Failed to parse JSON from `openclaw sessions --json` output.")


def _session_updated_at_ts(session: dict[str, Any]) -> int:
    """Sort key: numeric updatedAt from sessions JSON; invalid or missing → 0."""
    raw = session.get("updatedAt")
    if raw is None:
        return 0
    if isinstance(raw, bool):
        return 0
    if isinstance(raw, int):
        return raw
    if isinstance(raw, float):
        return int(raw)
    if isinstance(raw, str):
        s = raw.strip()
        if not s:
            return 0
        try:
            return int(s, 10)
        except ValueError:
            try:
                return int(float(s))
            except ValueError:
                return 0
    return 0


def _argv_preview(argv: list[str]) -> str:
    return " ".join(argv)

def _log_openclaw_subprocess_failure(
    label: str,
    argv: list[str],
    returncode: int | None,
    stdout: str | None,
    stderr: str | None,
) -> None:
    """Write full stdout/stderr to sessions.log (and console) when an openclaw subprocess fails."""
    out = "" if stdout is None else stdout
    err = "" if stderr is None else stderr
    logger.error(
        "%s failed (exit=%s) argv=%s\n--- stdout (full) ---\n%s\n--- stderr (full) ---\n%s",
        label,
        returncode,
        _argv_preview(argv),
        out,
        err,
    )

def _run_command(
    argv: list[str],
    timeout: int,
) -> subprocess.CompletedProcess[str]:
    logger.info("Running: %s", " ".join(argv))

    process_result = subprocess.run(
        argv,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        check=False,
    )
    
    logger.info("run command result: %s", process_result)

    return process_result

def _load_session_store() -> dict[str, Any] | None:
    if not SESSION_STORE_PATH.exists():
        logger.warning("Session store not found: %s", SESSION_STORE_PATH)
        return None
    try:
        payload = json.loads(SESSION_STORE_PATH.read_text(encoding="utf-8"))
    except Exception as exc:
        logger.warning("Failed to parse session store: %s", exc)
        return None
    if not isinstance(payload, dict):
        return None
    return payload

def resolve_session_delivery_context(
    session_id: str,
    session_key: str | None = None,
) -> tuple[str | None, str | None]:
    """Return channel/target for routing. `channel` may be set without `target` (e.g. webchat)."""
    if not session_id and not session_key:
        return None, None
    payload = _load_session_store()
    if payload is None:
        return None, None

    matched_entry: dict[str, Any] | None = None
    matched_key: str | None = None

    if session_key:
        key_candidate = str(session_key).strip()
        entry = payload.get(key_candidate)
        if isinstance(entry, dict):
            matched_entry = entry
            matched_key = key_candidate

    if matched_entry is None and session_id:
        for key, entry in payload.items():
            if not isinstance(entry, dict):
                continue
            if str(entry.get("sessionId", "")).strip() == str(session_id).strip():
                matched_entry = entry
                matched_key = str(key)
                break

    if matched_entry is None:
        logger.warning(
            "No matching session entry found for sessionId=%s sessionKey=%s",
            session_id,
            session_key,
        )
        return None, None

    logger.info(
        "Matched session entry: key=%s sessionId=%s",
        matched_key,
        str(matched_entry.get("sessionId", "")).strip(),
    )

    last_channel = str(matched_entry.get("lastChannel", "")).strip() or None
    last_to = str(matched_entry.get("lastTo", "")).strip() or None
    dc = matched_entry.get("deliveryContext")
    dc_channel = (
        str(dc.get("channel", "")).strip() or None
        if isinstance(dc, dict)
        else None
    )
    dc_to = (
        str(dc.get("to", "")).strip() or None if isinstance(dc, dict) else None
    )
    channel = last_channel or dc_channel
    target = last_to or dc_to
    return channel, target

def lookup_session_id_for_key(session_key: str) -> str | None:
    payload = _load_session_store()
    if payload is None:
        return None
    entry = payload.get(str(session_key).strip())
    if isinstance(entry, dict):
        sid = str(entry.get("sessionId", "")).strip()
        return sid or None
    return None

def lookup_session_key_for_id(session_id: str) -> str | None:
    payload = _load_session_store()
    if payload is None:
        return None
    want = str(session_id).strip()
    for key, entry in payload.items():
        if not isinstance(entry, dict):
            continue
        if str(entry.get("sessionId", "")).strip() == want:
            return str(key).strip() or None
    return None


def cleanup_agent_sessions(
    agent_id: str = DEFAULT_AGENT_ID,
    session_prefix: str = DEFAULT_SESSION_PREFIX,
) -> dict[str, int]:
    """
    清理指定 agent 下匹配 explicit session 前缀的历史会话：
    1) 删除 <sessionId>.jsonl / <sessionId>.jsonl.lock
    2) 删除 sessions.json 中对应 session key 条目
    """
    result = {
        "matched_entries": 0,
        "removed_session_files": 0,
        "removed_lock_files": 0,
        "removed_store_entries": 0,
    }

    session_store_path = (
        Path.home() / ".openclaw" / "agents" / str(agent_id) / "sessions" / "sessions.json"
    )
    sessions_dir = session_store_path.parent

    if not session_store_path.exists():
        logger.warning("cleanup_agent_sessions: session store not found: %s", session_store_path)
        return result

    try:
        payload = json.loads(session_store_path.read_text(encoding="utf-8"))
    except Exception as exc:
        logger.warning("cleanup_agent_sessions: failed to parse session store: %s", exc)
        return result

    if not isinstance(payload, dict):
        logger.warning("cleanup_agent_sessions: invalid session store structure")
        return result

    key_prefix = f"agent:{agent_id}:explicit:{session_prefix}".lower()
    keys_to_delete: list[str] = []

    for key, entry in payload.items():
        key_str = str(key).strip()
        if not key_str.lower().startswith(key_prefix):
            continue
        if not isinstance(entry, dict):
            continue

        result["matched_entries"] += 1
        session_id = str(entry.get("sessionId", "")).strip()
        if session_id:
            session_file = sessions_dir / f"{session_id}.jsonl"
            lock_file = sessions_dir / f"{session_id}.jsonl.lock"

            if session_file.exists():
                try:
                    session_file.unlink()
                    result["removed_session_files"] += 1
                except OSError as exc:
                    logger.warning("cleanup_agent_sessions: failed to remove %s: %s", session_file, exc)

            if lock_file.exists():
                try:
                    lock_file.unlink()
                    result["removed_lock_files"] += 1
                except OSError as exc:
                    logger.warning("cleanup_agent_sessions: failed to remove %s: %s", lock_file, exc)

        keys_to_delete.append(key_str)

    if not keys_to_delete:
        logger.info("cleanup_agent_sessions: no matching session entries for prefix %s", key_prefix)
        return result

    for key in keys_to_delete:
        if key in payload:
            del payload[key]
            result["removed_store_entries"] += 1

    try:
        session_store_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except Exception as exc:
        logger.warning("cleanup_agent_sessions: failed to write session store: %s", exc)
        return result

    logger.info(
        "cleanup_agent_sessions done: matched=%s removed_jsonl=%s removed_lock=%s removed_entries=%s",
        result["matched_entries"],
        result["removed_session_files"],
        result["removed_lock_files"],
        result["removed_store_entries"],
    )
    return result


def resolve_invoking_session(
    sorted_sessions: list[dict[str, Any]],
) -> tuple[str, str]:
    """
    必须由『当前会话』接收进度：优先环境变量（exec 注入或手工指定），否则退回 sessions --json 第一条。
    手工测试可设 SESSION_LIST_SESSION_ID / SESSION_LIST_SESSION_KEY；
    与 OpenClaw 对齐时可设 OPENCLAW_SESSION_ID / OPENCLAW_SESSION_KEY。
    """
    env_id = (
        os.getenv("OPENCLAW_SESSION_ID", "").strip()
        or os.getenv("SESSION_LIST_SESSION_ID", "").strip()
    )
    env_key = (
        os.getenv("OPENCLAW_SESSION_KEY", "").strip()
        or os.getenv("SESSION_LIST_SESSION_KEY", "").strip()
    )

    if env_id and env_key:
        logger.info("Notify target: invoking session from env id+key id=%s key=%s", env_id, env_key)
        return env_id, env_key

    if env_key:
        sid = lookup_session_id_for_key(env_key)
        if sid:
            logger.info(
                "Notify target: invoking session from env key=%s resolved sessionId=%s",
                env_key,
                sid,
            )
            return sid, env_key
        logger.warning(
            "OPENCLAW_SESSION_KEY / SESSION_LIST_SESSION_KEY set but sessionStore has no entry: %s",
            env_key,
        )

    if env_id:
        sk = lookup_session_key_for_id(env_id)
        logger.info(
            "Notify target: invoking session from env id=%s resolved sessionKey=%s",
            env_id,
            sk or "",
        )
        return env_id, sk or ""

    if sorted_sessions:
        sid = str(sorted_sessions[0].get("sessionId", "")).strip()
        sk = str(sorted_sessions[0].get("key", "")).strip()
        logger.warning(
            "No session env hints; using top session from `sessions --json` (updatedAt desc) "
            "id=%s key=%s — for correct 『current session』, set OPENCLAW_SESSION_KEY or SESSION_LIST_SESSION_KEY",
            sid,
            sk,
        )
        return sid, sk

    return "", ""


def send_channel_message(
    openclaw_cmd: str | None,
    channel: str | None,
    target: str | None,
    message: str,
) -> bool:
    under_openclaw = ran_under_openclaw_exec()
    if not under_openclaw:
        logger.info("跳过 channel 通知（非 OpenClaw exec）：%s", message)
        return False

    msg = (message or "").strip()
    if not msg:
        logger.info("跳过 channel 通知（消息为空）。")
        return False

    ch_norm = (channel or "").strip().lower()
    if not ch_norm:
        logger.info("跳过 channel 通知（channel 未配置或为空）。")
        return False
    if ch_norm == "webchat":
        logger.info("Channel webchat: skip send message.")
        return False

    tgt_norm = (target or "").strip()
    if not tgt_norm:
        logger.info(
            "跳过 channel 通知（target 未配置或为空，channel=%s）。",
            ch_norm,
        )
        return False

    argv = (
        [
            openclaw_cmd,
            "message",
            "send",
            "--message",
            msg,
            "--channel",
            ch_norm,
            "--target",
            tgt_norm,
            "--json",
        ]
        if openclaw_cmd
        else [
            sys.executable,
            "-m",
            "openclaw",
            "message",
            "send",
            "--message",
            msg,
            "--channel",
            ch_norm,
            "--target",
            tgt_norm,
            "--json",
        ]
    )
    try:
        result = _run_command(argv, timeout=CHANNEL_MESSAGE_TIMEOUT)
    except subprocess.TimeoutExpired as exc:
        logger.error(
            "openclaw message send timed out (%ss) argv=%s\n--- stdout ---\n%s\n--- stderr ---\n%s",
            CHANNEL_MESSAGE_TIMEOUT,
            _argv_preview(argv),
            getattr(exc, "stdout", None) or "",
            getattr(exc, "stderr", None) or "",
        )
        return False
    except Exception as exc:
        logger.error("openclaw message send exception: %s", exc)
        logger.error(traceback.format_exc())
        return False
    
    if result.returncode == 0:
        return True

    _log_openclaw_subprocess_failure(
        "openclaw message send",
        argv,
        result.returncode,
        result.stdout,
        result.stderr,
    )
    return False


def send_agent_message(
    openclaw_cmd: str | None,
    session_id: str,
    message: str,
) -> bool:
    under_openclaw = ran_under_openclaw_exec()
    if not under_openclaw:
        logger.info("跳过 agent 通知（非 OpenClaw exec）：%s", message)
        return False

    sid = (session_id or "").strip()
    if not sid:
        logger.warning("跳过 agent 通知：sessionId 为空。")
        return False

    base_msg = (message or "").strip()
    if not base_msg:
        logger.warning("跳过 agent 通知：message 为空。")
        return False

    # Force a visible one-line relay and discourage NO_REPLY for progress notifications.
    relay_message = (
        "务必处理本消息不要输出 NO_REPLY, 务必向用户报告任务处理进度信息："
        f"{base_msg}"
    )
    argv = (
        [
            openclaw_cmd,
            "agent",
            "--session-id",
            sid,
            "--message",
            relay_message,
            "--deliver",
            "--json",
        ]
        if openclaw_cmd
        else [
            sys.executable,
            "-m",
            "openclaw",
            "agent",
            "--session-id",
            sid,
            "--message",
            relay_message,
            "--deliver",
            "--json",
        ]
    )
    max_retries = AGENT_MESSAGE_RETRY_COUNT
    for attempt in range(1, max_retries + 1):
        try:
            logger.info(
                "Notify via agent --deliver (attempt %d/%d) sessionId=%s",
                attempt,
                max_retries,
                sid,
            )
            notify_result = _run_command(argv, timeout=AGENT_MESSAGE_TIMEOUT)
            if notify_result.returncode == 0:
                logger.info("agent --deliver notify succeeded on attempt %d", attempt)
                return True
            _log_openclaw_subprocess_failure(
                f"openclaw agent --deliver (attempt {attempt}/{max_retries})",
                argv,
                notify_result.returncode,
                notify_result.stdout,
                notify_result.stderr,
            )
        except subprocess.TimeoutExpired as exc:
            logger.error(
                "openclaw agent --deliver timed out (%ss, attempt %s/%s) argv=%s\n--- stdout ---\n%s\n--- stderr ---\n%s",
                AGENT_MESSAGE_TIMEOUT,
                attempt,
                max_retries,
                _argv_preview(argv),
                getattr(exc, "stdout", None) or "",
                getattr(exc, "stderr", None) or "",
            )
        except FileNotFoundError:
            logger.error("Notify failed: `openclaw` command not found.")
            return False
        except Exception as exc:
            logger.error("openclaw agent --deliver exception (attempt %s/%s): %s", attempt, max_retries, exc)
            logger.error(traceback.format_exc())
        if attempt < max_retries:
            time.sleep(2)
    return False

def get_openclaw_session_info() -> OpenClawSessionInfo:
    empty = OpenClawSessionInfo("", "", "", "")
    under_openclaw = ran_under_openclaw_exec()
    if under_openclaw:
        logger.info("OpenClaw exec 环境：将发送 channel / agent 消息。")
    else:
        logger.info("非 OpenClaw exec（需 OPENCLAW_SHELL=exec 或 OPENCLAW_CLI=1）：仅执行任务，不发送 channel / agent 消息。")
        return empty

    openclaw_cmd = shutil.which("openclaw") or shutil.which("openclaw.cmd")
    argv = [openclaw_cmd, "sessions", "--json"] if openclaw_cmd else [sys.executable, "-m", "openclaw", "sessions", "--json"]

    try:
        logger.info("Get sessions list")
        result = _run_command(argv, timeout=SESSION_LIST_TIMEOUT)
    except FileNotFoundError:
        logger.error("`openclaw` command not found.")
        return empty
    except subprocess.TimeoutExpired as exc:
        logger.error(
            "openclaw sessions --json timed out (%ss) argv=%s\n--- stdout ---\n%s\n--- stderr ---\n%s",
            SESSION_LIST_TIMEOUT,
            _argv_preview(argv),
            getattr(exc, "stdout", None) or "",
            getattr(exc, "stderr", None) or "",
        )
        return empty

    combined_output = (result.stdout or "").strip()
    if result.stderr:
        logger.info("stderr: %s", result.stderr.strip())

    if result.returncode != 0:
        _log_openclaw_subprocess_failure(
            "openclaw sessions --json",
            argv,
            result.returncode,
            result.stdout,
            result.stderr,
        )
        return empty

    try:
        payload = parse_json_from_mixed_output(combined_output)
        logger.info("Parse json from mixed output success")
    except ValueError as exc:
        logger.error("Parse json from mixed output failed: %s", exc)
        raw_out = result.stdout if result.stdout is not None else ""
        raw_err = result.stderr if result.stderr is not None else ""
        logger.error(
            "openclaw sessions --json output could not be parsed as JSON; full capture follows.\n--- stdout (full) ---\n%s\n--- stderr (full) ---\n%s",
            raw_out,
            raw_err,
        )
        return empty

    sessions = payload.get("sessions")
    if not isinstance(sessions, list):
        logger.error("JSON payload has no `sessions` list.")
        return empty

    sorted_sessions = sorted(
        (s for s in sessions if isinstance(s, dict)),
        key=_session_updated_at_ts,
        reverse=True,
    )

    logger.info("Sorted sessions by updatedAt (desc):")
    for index, session in enumerate(sorted_sessions, start=1):
        key = session.get("key", "")
        session_id = session.get("sessionId", "")
        updated_at = session.get("updatedAt", 0)
        logger.info("%d. key=%s sessionId=%s updatedAt=%s", index, key, session_id, updated_at)

    notify_session_id, notify_session_key = resolve_invoking_session(sorted_sessions)
    logger.info("Resolve invoking session success: notify_session_id=%s notify_session_key=%s", notify_session_id, notify_session_key)
    channel, target = resolve_session_delivery_context(
        notify_session_id, notify_session_key
    )
    logger.info("Resolved delivery context (progress): channel=%s target=%s", channel, target)

    return OpenClawSessionInfo(notify_session_id, notify_session_key, channel, target)


def main() -> int:
    openclaw_cmd = shutil.which("openclaw") or shutil.which("openclaw.cmd")
    session_info = get_openclaw_session_info()

    try:
        total_tasks = int(os.getenv("SESSION_LIST_TASK_COUNT", str(DEFAULT_TASK_COUNT)))
        sleep_seconds = int(os.getenv("SESSION_LIST_TASK_SECONDS", str(DEFAULT_TASK_SECONDS)))
    
        for index in range(1, total_tasks + 1):
            logger.info("Running simulated subtask %d/%d (%ss)...", index, total_tasks, sleep_seconds)

            time.sleep(max(0, sleep_seconds))
            progress_msg = f"当前进度：{index}/{total_tasks} 已完成。"
            ok = send_channel_message(
                openclaw_cmd,
                session_info.channel,
                session_info.target,
                progress_msg,
            )
            if ok:
                logger.info("Progress notified for subtask %d/%d", index, total_tasks)
            else:
                logger.warning("Progress notify failed for subtask %d/%d", index, total_tasks)

        agent_msg = f"当前任务已全部执行完成，详细总结Skill执行的结果信息，立即向我报告。"
        ok = send_agent_message(openclaw_cmd, session_info.session_id, agent_msg)
        if ok:
            logger.info("Final summary notify sent.")
        else:
            logger.warning("Final summary notify failed.")
    except Exception as exc:
        logger.error("Main process crashed: %s", exc)
        logger.error(traceback.format_exc())
        return 1

    return 0


if __name__ == "__main__":
    results = cleanup_agent_sessions()
    logger.info("Cleanup agent sessions results: %s", results)
    #raise SystemExit(main())
