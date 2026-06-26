"""
AgentCli — 通过 openclaw agent CLI 子进程实现。
"""
from __future__ import annotations

import json
import logging
import os
import shutil
import subprocess
import sys
import time
import uuid
from typing import Any
from pathlib import Path
from typing import Any, Dict, List

from verification import verify_task_answer
from utils import get_temp_file
from session_info import SessionInfo
from usage_info import UsageInfo
from config import (
    DEFAULT_SESSION_PREFIX,
    DEFAULT_AGENT_ID
)
logger = logging.getLogger("benchclaw")


# ---------- CLI 工具函数 ----------

def resolve_openclaw_cmd() -> list[str]:
    """返回调用 openclaw 的命令前缀列表。"""
    exe = shutil.which("openclaw")
    if exe:
        return [exe]
    # 回退：用当前 Python 解释器调用模块
    return [sys.executable, "-m", "openclaw"]


def _verify_cli_task(task: dict[str, Any], stdout: str) -> int:
    """
    CLI 模式下的结果验证，逻辑与 TaskManager.verify_task_result 一致。
    返回得分（0 表示验证失败）。
    """
    from openclawbot import get_openclaw_bot  # 延迟导入避免循环依赖

    question_id = str(task.get("id") or "")
    answer = task.get("answer")
    if not isinstance(answer, dict):
        logger.debug(" [verify] no answer config, skip verification")
        return 0

    workspace_dir = os.path.join(get_openclaw_bot().openclaw_root, "workspace")
    try:
        vr = verify_task_answer(
            workspace_dir=workspace_dir,
            question_id=question_id,
            answer=answer,
            stdout_content=stdout,
        )
    except Exception as e:
        logger.error(f" [verify] exception during verification: {e}")
        return 0

    logger.info(
        f" [verify] question {vr.question_id}: "
        f"score={vr.score}/{vr.max_score}, "
        f"before_penalty={vr.score_before_penalty}, "
        f"penalty={vr.penalty_deduction}, fatal={vr.fatal}"
    )
    if vr.fatal:
        return 0
    return vr.score

def run_task_cli(
    task: dict[str, Any],
    *,
    timeout_sec: int,
) -> dict[str, Any]:
    """通过 openclaw agent 执行单条题目，收集 stdout/stderr/returncode，并验证结果。"""
    task_id = task.get("id", "?")
    category = task.get("category", "?")
    category_label = task.get("category_label", category)
    answer = task.get("answer")
    max_score = answer.get("max_score", 0) if isinstance(answer, dict) else 0
    question = (task.get("question") or "").strip()

    _fail_start_time = int(time.time() * 1000)

    def _fail(error: str, duration: float = 0.0) -> dict[str, Any]:
        _now = int(time.time() * 1000)
        return {
            "id": task_id,
            "category": category,
            "category_label": category_label,
            "max_accuracy_score": max_score,
            "success": False,
            "error": error,
            "stdout": "",
            "stderr": "",
            "returncode": -1,
            "start_time": _fail_start_time,
            "end_time": _now,
            "duration_sec": duration,
            "accuracy_score": 0,
            "real_accuracy_score": 0,
            "score": 0,
            "tps": 0.0,
            "tps_score": 0,
            "input_tokens": 0,
            "output_tokens": 0,
            "cache_read_tokens": 0,
            "cache_write_tokens": 0,
            "total_tokens": 0,
        }

    if not question:
        return _fail("empty question")

    # 将题目内容写入 ../tmp/prompt.md，文件已存在则覆盖
    prompt_file_path = get_temp_file("prompt.md")
    with open(prompt_file_path, "w", encoding="utf-8") as _pf:
        _pf.write(question)

    # 使用
    session_id = f'{DEFAULT_SESSION_PREFIX}{task_id}'
    base = resolve_openclaw_cmd()
    cmd = base + [
        "agent",
        # "--agent", DEFAULT_AGENT_ID, 加上的话 session名称为 uuid
        "--session-id", session_id,
        "--message", f'执行文件中的指令：{prompt_file_path}',
        "--timeout", str(timeout_sec),
    ]

    time_before = time.perf_counter()
    start_time = int(time.time() * 1000)  # ms 时间戳

    # subprocess 侧留 30s 宽限期，让 openclaw agent 在内部 timeout 触发后有时间优雅退出
    # 避免 Python 侧强杀导致 transcript 未写完、token_usage 丢失
    _subprocess_timeout = timeout_sec + 30

    stdout_text = ""
    stderr_text = ""
    returncode = -1
    end_time = start_time
    duration_sec = 0.0
    proc = None
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        try:
            stdout_text, stderr_text = proc.communicate(timeout=_subprocess_timeout)
            stdout_text = (stdout_text or "").strip()
            stderr_text = (stderr_text or "").strip()
            returncode = proc.returncode
        except subprocess.TimeoutExpired:
            # 超时后强制终止子进程
            logger.warning(f"任务 {task_id} 超时，强制终止子进程")
            proc.kill()
            try:
                stdout_text, stderr_text = proc.communicate(timeout=10)
                stdout_text = (stdout_text or "").strip()
                stderr_text = (stderr_text or "").strip()
            except subprocess.TimeoutExpired:
                logger.error(f"强制终止子进程后仍无法获取输出")
                stdout_text = ""
                stderr_text = ""
            return _fail("timeout", round(time.perf_counter() - time_before, 2))

        end_time = int(time.time() * 1000)  # ms 时间戳
        duration_sec = round(time.perf_counter() - time_before, 2)
        logger.info(f" 任务消耗的时间: {duration_sec} seconds")

        # 加载对话脚本
        transcript = _load_transcript('main', session_id, 0)
        token_usage = _extract_usage_from_transcript(transcript)
        logger.info(f" token_usage: {token_usage}")

    except FileNotFoundError:
        if proc is not None and proc.poll() is None:
            proc.kill()
        return _fail("openclaw not found", round(time.perf_counter() - time_before, 2))
    except Exception as e:
        if proc is not None and proc.poll() is None:
            proc.kill()
        return _fail(str(e), round(time.perf_counter() - time_before, 2))

    total_tokens = token_usage["total_tokens"]
    tps = round(total_tokens / duration_sec, 2) if total_tokens > 0 and duration_sec > 0 else 0.0
    tps_score = int(tps * 0.1)

    if returncode != 0:
        return {
            "id": task_id,
            "category": category,
            "category_label": category_label,
            "max_accuracy_score": max_score,
            "success": False,
            "error": f"exit code {returncode}",
            "stdout": stdout_text,
            "stderr": stderr_text,
            "returncode": returncode,
            "start_time": start_time,
            "end_time": end_time,
            "duration_sec": duration_sec,
            "accuracy_score": 0,
            "real_accuracy_score": 0,
            "score": 0,
            "tps": tps,
            "tps_score": 0,
            "input_tokens": token_usage["input_tokens"],
            "output_tokens": token_usage["output_tokens"],
            "cache_read_tokens": token_usage["cache_read_tokens"],
            "cache_write_tokens": token_usage["cache_write_tokens"],
            "total_tokens": total_tokens,
        }

    # 验证结果
    logger.info(f" 开始验证题目结果 {task_id} ...")
    accuracy_score = int(_verify_cli_task(task, stdout_text))
    if accuracy_score <= 0:
        logger.warning(f" 题目结果验证失败: {task_id}, accuracy_score={accuracy_score}")
        return {
            "id": task_id,
            "category": category,
            "category_label": category_label,
            "max_accuracy_score": max_score,
            "success": False,
            "error": f"验证失败, score={accuracy_score}",
            "stdout": stdout_text,
            "stderr": stderr_text,
            "returncode": returncode,
            "start_time": start_time,
            "end_time": end_time,
            "duration_sec": duration_sec,
            "accuracy_score": 0,
            "real_accuracy_score": 0,
            "score": 0,
            "tps": tps,
            "tps_score": 0,
            "input_tokens": token_usage["input_tokens"],
            "output_tokens": token_usage["output_tokens"],
            "cache_read_tokens": token_usage["cache_read_tokens"],
            "cache_write_tokens": token_usage["cache_write_tokens"],
            "total_tokens": total_tokens,
        }

    real_accuracy_score = int(accuracy_score * (1000 / duration_sec) * 10)
    total_score = real_accuracy_score + tps_score

    logger.info(f" tps: {tps} tokens/s, tps_score: {tps_score}, accuracy_score: {accuracy_score}, total_score: {total_score}")

    return {
        "id": task_id,
        "category": category,
        "category_label": category_label,
        "max_accuracy_score": max_score,
        "success": True,
        "stdout": stdout_text,
        "stderr": stderr_text,
        "returncode": returncode,
        "start_time": start_time,
        "end_time": end_time,
        "duration_sec": duration_sec,
        "accuracy_score": accuracy_score,
        "real_accuracy_score": real_accuracy_score,
        "score": total_score,
        "tps": tps,
        "tps_score": tps_score,
        "input_tokens": token_usage["input_tokens"],
        "output_tokens": token_usage["output_tokens"],
        "cache_read_tokens": token_usage["cache_read_tokens"],
        "cache_write_tokens": token_usage["cache_write_tokens"],
        "total_tokens": total_tokens,
    }


def get_sessions() -> list[SessionInfo]:
    """
    调用 `openclaw sessions --json`，从标准输出中提取 JSON 块并解析为 SessionInfo 列表。

    输出中可能混有非 JSON 的日志行（如 [plugins] 注册信息），
    解析时逐行扫描，找到完整 JSON 对象后提取其中的 sessions 字段。
    """
    cmd = resolve_openclaw_cmd() + ["sessions", "--json"]
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=15,
            encoding="utf-8",
            errors="replace",
        )
    except FileNotFoundError:
        logger.error("get_sessions: openclaw 命令未找到")
        return []
    except subprocess.TimeoutExpired:
        logger.error("get_sessions: 命令超时")
        return []
    except Exception as e:
        logger.error(f"get_sessions: 执行失败: {e}")
        return []

    output = proc.stdout or ""

    # 从混有日志行的输出中找到第一个完整 JSON 对象
    # 策略：收集以 '{' 开头的连续行，尝试逐步拼接并解析
    data: dict | None = None
    buf: list[str] = []
    brace_depth = 0
    for line in output.splitlines():
        if not buf:
            stripped = line.lstrip()
            if not stripped.startswith("{"):
                continue  # 跳过非 JSON 起始行
        buf.append(line)
        brace_depth += line.count("{") - line.count("}")
        if brace_depth <= 0:
            # 可能已构成完整 JSON 对象，尝试解析
            try:
                data = json.loads("\n".join(buf))
                break
            except json.JSONDecodeError:
                pass
            buf.clear()
            brace_depth = 0

    if data is None:
        logger.warning("get_sessions: 未能从输出中解析到 JSON")
        logger.debug(f"get_sessions stdout: {output!r}")
        return []

    raw_sessions = data.get("sessions")
    if not isinstance(raw_sessions, list):
        logger.warning("get_sessions: JSON 中缺少 sessions 字段")
        return []

    return [SessionInfo.from_dict(s) for s in raw_sessions if isinstance(s, dict)]


def session_exists(session_id: str) -> bool:
    """判断指定 session_id 的 session 是否存在。入参须为 UUID 格式，否则直接返回 False。"""
    try:
        uuid.UUID(session_id)
    except (ValueError, AttributeError):
        return False
    sessions = get_sessions()
    return any(s.session_id == session_id for s in sessions)


def get_latest_session() -> SessionInfo | None:
    """返回 updatedAt 最大（最近活跃）的 session，若无则返回 None。"""
    sessions = get_sessions()
    if not sessions:
        return None
    return max(sessions, key=lambda s: s.updated_at)


def get_latest_session_usage() -> UsageInfo:
    """返回最近活跃 session 的 token 使用信息（input / output / total_tokens）。
    若无可用 session 则返回空 UsageInfo。
    """
    session = get_latest_session()
    if session is None:
        return UsageInfo()
    return UsageInfo(
        input=session.input_tokens or 0,
        output=session.output_tokens or 0,
        totalTokens=session.total_tokens or 0,
    )



def _get_agent_workspace(agent_id: str) -> Path | None:
    """Get the workspace path for an agent from OpenClaw config."""
    try:
        list_result = subprocess.run(
            ["openclaw", "agents", "list"],
            capture_output=True,
            text=True,
            check=False,
        )
        if list_result.returncode != 0:
            return None

        # Parse the agent list output to find workspace
        # OpenClaw normalizes colons to dashes in agent names, so check both.
        normalized_id = agent_id.replace(":", "-")
        lines = list_result.stdout.split("\n")
        found_agent = False
        for line in lines:
            stripped = line.strip()
            if stripped.startswith(f"- {agent_id}") or stripped.startswith(f"- {normalized_id}"):
                found_agent = True
            elif found_agent and "Workspace:" in line:
                workspace_str = line.split("Workspace:")[1].strip()
                # Expand ~ if present
                if workspace_str.startswith("~/"):
                    workspace_str = str(Path.home() / workspace_str[2:])
                return Path(workspace_str)
            elif found_agent and line.strip().startswith("-"):
                # Found next agent, stop looking
                break
        return None
    except Exception as exc:
        logger.warning("Failed to get agent workspace: %s", exc)
        return None


def ensure_agent_exists(agent_id: str, workspace_dir: Path) -> bool:
    """Ensure the OpenClaw agent exists with the correct workspace.

    If the agent already exists but points to a different workspace, it is
    deleted and recreated so that the new workspace takes effect.
    Returns True if the agent was (re)created.
    """
    workspace_dir.mkdir(parents=True, exist_ok=True)

    try:
        list_result = subprocess.run(
            ["openclaw", "agents", "list"],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        logger.error("openclaw CLI not found while listing agents")
        return False

    if list_result.returncode == 0:
        # Check for exact agent ID match — avoid substring false positives
        # (e.g. "bench-foo-4" matching "bench-foo-4-5" in the output).
        # Output format is "- <agent_id>" or "- <agent_id> (default)" per line.
        # OpenClaw normalizes colons to dashes in directory/display names, so
        # also check the normalized form.
        existing_agents = set()
        for line in list_result.stdout.splitlines():
            line = line.strip()
            if line.startswith("- "):
                # Extract agent name: "- bench-foo-4-5" or "- main (default)"
                name_part = line[2:].split()[0] if line[2:].strip() else ""
                if name_part:
                    existing_agents.add(name_part)
        normalized_id = agent_id.replace(":", "-")
        if agent_id in existing_agents or normalized_id in existing_agents:
            # Agent exists — check if workspace matches
            current_workspace = _get_agent_workspace(agent_id)
            if (
                current_workspace is not None
                and current_workspace.resolve() == workspace_dir.resolve()
            ):
                logger.info("Agent %s already exists with correct workspace", agent_id)
                return False
            # Workspace is stale or unknown — delete and recreate
            delete_name = normalized_id if normalized_id in existing_agents else agent_id
            logger.info(
                "Agent %s exists with stale workspace (%s != %s), recreating",
                agent_id,
                current_workspace,
                workspace_dir,
            )
            subprocess.run(
                ["openclaw", "agents", "delete", delete_name, "--force"],
                capture_output=True,
                text=True,
                check=False,
            )

    logger.info("Creating OpenClaw agent %s", agent_id)
    try:
        create_result = subprocess.run(
            [
                "openclaw",
                "agents",
                "add",
                agent_id,
                "--workspace",
                str(workspace_dir),
                "--non-interactive",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        logger.error("openclaw CLI not found while creating agent")
        return False

    if create_result.returncode != 0:
        logger.warning(
            "Agent creation returned %s: %s", create_result.returncode, create_result.stderr
        )
    return True


def cleanup_agent_sessions(agent_id: str) -> None:
    """Remove stored session transcripts for an agent to avoid unbounded growth."""
    agent_dir = _get_agent_store_dir(agent_id)
    sessions_dir = agent_dir / "sessions"
    if not sessions_dir.exists():
        return
    removed = 0
    for pattern in ("*.jsonl", "*.jsonl.lock"):
        for path in sessions_dir.glob(pattern):
            try:
                path.unlink()
                removed += 1
            except OSError as exc:
                logger.warning("Failed to remove session file %s: %s", path, exc)
    sessions_store = sessions_dir / "sessions.json"
    if sessions_store.exists():
        try:
            sessions_store.unlink()
        except OSError as exc:
            logger.warning("Failed to remove session store %s: %s", sessions_store, exc)
    if removed:
        logger.info("Removed %s old OpenClaw session transcripts for %s", removed, agent_id)


def _get_agent_store_dir(agent_id: str) -> Path:
    base_dir = Path.home() / ".openclaw" / "agents"
    direct_dir = base_dir / agent_id
    if direct_dir.exists():
        return direct_dir
    normalized_dir = base_dir / agent_id.replace(":", "-")
    if normalized_dir.exists():
        return normalized_dir
    return direct_dir

def cleanup_agent_sessions_with_prefix(agent_id: str, prefix_pattern: str) -> None:
    """Remove stored session transcripts for an agent to avoid unbounded growth."""
    agent_dir = _get_agent_store_dir(agent_id)
    sessions_dir = agent_dir / "sessions"
    if not sessions_dir.exists():
        return

    removed = 0
    for pattern in (f"{prefix_pattern}.jsonl", f"{prefix_pattern}.jsonl.lock"):
        for path in sessions_dir.glob(pattern):
            try:
                path.unlink()
                removed += 1
            except OSError as exc:
                logger.warning("清理会话文件失败 %s: %s", path, exc)

    if removed:
        logger.info("已清理 %s 个历史会话脚本文件 Agent: %s", removed, agent_id)



def _resolve_session_uuid(agent_id: str, session_id: str) -> str | None:
    """从 sessions.json 中根据 session key 解析实际的 UUID sessionId。

    session key 格式：agent:{agent_id}:explicit:{session_id}
    匹配成功后返回对应的 sessionId（UUID 字符串），失败返回 None。
    """
    agent_dir = _get_agent_store_dir(agent_id)
    sessions_json_path = agent_dir / "sessions" / "sessions.json"

    if not sessions_json_path.exists():
        logger.warning(f"sessions.json 不存在: {sessions_json_path}")
        return None

    session_key = f"agent:{agent_id}:explicit:{session_id}".lower()
    try:
        data = json.loads(sessions_json_path.read_text(encoding="utf-8"))
        entry = data.get(session_key)
        if entry is None:
            logger.warning(f"sessions.json 中未找到 session key: {session_key}")
            return None
        uuid_str = entry.get("sessionId")
        if not uuid_str:
            logger.warning(f"sessions.json 中 session key {session_key} 无 sessionId 字段")
            return None
        logger.info(f"已从 sessions.json 解析 sessionId: {uuid_str}")
        return uuid_str
    except Exception as e:
        logger.warning(f"解析 sessions.json 失败: {e}")
        return None


def _load_transcript(agent_id: str, session_id: str, started_at: float) -> List[Dict[str, Any]]:
    agent_dir = _get_agent_store_dir(agent_id)

    # transcript 文件名已由 <session_id>.jsonl 变更为 <UUID>.jsonl，
    # 需先从 sessions.json 解析实际的 UUID sessionId
    resolved_id = _resolve_session_uuid(agent_id, session_id)
    transcript_path = agent_dir / "sessions" / f"{resolved_id if resolved_id else session_id}.jsonl"
    logger.info(f"transcript 路径：{transcript_path}")

    for attempt in range(6):
        if transcript_path.exists():
            logger.info(f"transcript 已找到！attempt: {attempt}")
            break
        time.sleep(1.0)

    if not transcript_path.exists():
        logger.info(f"transcript 文件未找到！")
        return []

    transcript: List[Dict[str, Any]] = []
    for line in transcript_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            transcript.append(json.loads(line))
        except json.JSONDecodeError as exc:
            logger.warning("解析会话脚本文件失败: %s", exc)
            transcript.append({"raw": line, "parse_error": str(exc)})
    return transcript


def _extract_usage_from_transcript(transcript: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Sum token usage and cost from all assistant messages in transcript."""
    totals = {
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_read_tokens": 0,
        "cache_write_tokens": 0,
        "total_tokens": 0,
        "cost_usd": 0.0,
        "request_count": 0,
    }

    for entry in transcript:
        if entry.get("type") != "message":
            continue
        msg = entry.get("message", {})
        if msg.get("role") != "assistant":
            continue
        totals["request_count"] += 1
        usage = msg.get("usage", {})
        totals["input_tokens"] += usage.get("input", 0)
        totals["output_tokens"] += usage.get("output", 0)
        totals["cache_read_tokens"] += usage.get("cacheRead", 0)
        totals["cache_write_tokens"] += usage.get("cacheWrite", 0)
        totals["total_tokens"] += usage.get("totalTokens", 0)
        cost = usage.get("cost", {})
        totals["cost_usd"] += cost.get("total", 0.0)

    return totals
