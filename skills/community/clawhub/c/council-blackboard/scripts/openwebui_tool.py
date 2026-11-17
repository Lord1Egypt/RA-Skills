"""Open WebUI tool for visible, typed council conversations with OpenClaw."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

DEFAULT_WORKSPACE = Path.home() / ".openclaw" / "workspace"
WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", DEFAULT_WORKSPACE)).expanduser()
BOARDS = (WORKSPACE / "blackboards" / "councils").resolve()
BB = Path(
    os.environ.get(
        "COUNCIL_BLACKBOARD_SCRIPT",
        WORKSPACE / "skills" / "blackboard" / "scripts" / "blackboard.py",
    )
).expanduser()
COUNCIL = Path(
    os.environ.get(
        "COUNCIL_ROOM_SCRIPT",
        WORKSPACE / "skills" / "council-blackboard" / "scripts" / "council.py",
    )
).expanduser()
PYTHON = os.environ.get("COUNCIL_PYTHON", sys.executable)
ORNITH_MODEL_ID = os.environ.get("COUNCIL_ORNITH_WRITER", "ollama/local-model:latest")
OPENCLAW_MODEL = os.environ.get("COUNCIL_OPENCLAW_MODEL", "openai/gpt-5.6")
OPENCLAW_WRITER_PREFIX = os.environ.get("COUNCIL_OPENCLAW_WRITER_PREFIX", "openai/")
OPENCLAW_AGENT = os.environ.get("COUNCIL_OPENCLAW_AGENT", "main")
OPENCLAW_THINKING = os.environ.get("COUNCIL_OPENCLAW_THINKING", "off")


def _env_int(name: str, default: int, minimum: int, maximum: int) -> int:
    try:
        value = int(os.environ.get(name, str(default)))
    except ValueError:
        value = default
    return max(minimum, min(value, maximum))


ROUTE_LEASE_SECONDS = _env_int("COUNCIL_ROUTE_LEASE_SECONDS", 900, 60, 86400)
MAX_AWAIT_SECONDS = _env_int("COUNCIL_MAX_AWAIT_SECONDS", 20, 0, 60)
RESULT_COLLECTIONS = (
    "facts",
    "inferences",
    "evidence",
    "test_results",
    "failed_attempts",
    "open_questions",
)


def _normalise(value: str) -> str:
    return " ".join(str(value or "").split())


def _board(value: str) -> Path:
    path = Path(value).expanduser().resolve()
    if path.parent != BOARDS or path.suffix.lower() != ".json":
        raise ValueError("invalid council board path")
    if not path.is_file():
        raise FileNotFoundError(f"council board not found: {path}")
    return path


def _run(command: list[str], timeout: int = 120) -> str:
    try:
        process = subprocess.run(
            command,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        raise RuntimeError(f"command timed out after {timeout}s: {command[0]}") from error
    if process.returncode:
        detail = (process.stderr or process.stdout or "command failed")[-4000:]
        raise RuntimeError(detail.strip())
    return process.stdout


def _json_output(raw: str) -> dict[str, Any]:
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as error:
        raise RuntimeError(f"helper returned non-JSON output: {raw[-1200:]}") from error
    if not isinstance(value, dict):
        raise RuntimeError("helper returned a non-object JSON value")
    return value


def _bb(*args: str, timeout: int = 60) -> str:
    if not BB.is_file():
        raise FileNotFoundError(f"blackboard helper not found: {BB}")
    return _run([PYTHON, str(BB), *args], timeout)


def _bb_json(*args: str, timeout: int = 60) -> dict[str, Any]:
    return _json_output(_bb(*args, timeout=timeout))


def _summary(board: Path, limit: int = 6) -> dict[str, Any]:
    return _bb_json("summary", str(board), "--limit", str(max(1, min(limit, 20))))


def _route_status(board: Path, route_id: str) -> dict[str, Any]:
    return _bb_json(
        "route-status", str(board), "--route-id", route_id, "--json"
    )


def _route_results(board: Path, route_id: str) -> dict[str, Any]:
    return _bb_json("route-results", str(board), route_id)


def _parse_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _fallback_route_results(
    board: Path,
    route_id: str,
    route_created_at: str | None,
) -> list[dict[str, Any]]:
    """Correlate old/uncooperative agents without accepting stale old replies."""
    created = _parse_timestamp(route_created_at)
    if created is None:
        return []
    raw = _bb_json("show", str(board))
    output: list[dict[str, Any]] = []
    for collection in RESULT_COLLECTIONS:
        for entry in raw.get(collection, []):
            writer = (entry.get("written_by") or {}).get("model", "")
            timestamp = _parse_timestamp(entry.get("created_at"))
            tagged = (entry.get("metadata") or {}).get("route_id") == route_id or any(
                isinstance(item, dict) and item.get("route_id") == route_id
                for item in entry.get("provenance", [])
            )
            if tagged:
                continue
            if (
                str(writer).startswith(OPENCLAW_WRITER_PREFIX)
                and timestamp is not None
                and timestamp >= created
            ):
                output.append(
                    {
                        "collection": collection,
                        **entry,
                        "correlation": "writer_and_timestamp_fallback",
                    }
                )
    output.sort(key=lambda item: item.get("created_at", ""))
    return output


def _binary(name: str, env_name: str) -> str:
    configured = os.environ.get(env_name)
    if configured:
        return configured
    found = shutil.which(name)
    if not found:
        raise FileNotFoundError(f"required executable not found in PATH: {name}")
    return found


def _openclaw_prompt(board: Path, route_id: str, question: str) -> str:
    return (
        "You are the OpenClaw member of a visible council with the user and the Open WebUI model. "
        "Use the blackboard skill and do exactly one bounded job. Validate and read the board, "
        "answer the routed question, and append only genuinely useful typed contributions. "
        "Do not overwrite entries, create another route, change policy, or send anything externally.\n\n"
        f"Board: {board}\n"
        f"Route ID: {route_id}\n"
        f"Question: {question}\n\n"
        f"Every blackboard entry created for this answer MUST carry route_id {route_id}. "
        "When using blackboard.py add, pass --route-id with that exact UUID. Add receipts and "
        "confidence where appropriate. Do not resolve the route yourself; the visible council "
        "tool resolves it after it has collected the tagged entries. Return a concise council reply."
    )


def _launch_openclaw(
    board: Path,
    route_id: str,
    question: str,
    unit: str,
) -> None:
    systemd_run = _binary("systemd-run", "COUNCIL_SYSTEMD_RUN")
    openclaw = _binary("openclaw", "COUNCIL_OPENCLAW_BIN")
    session_suffix = f"{board.stem[-18:]}-{route_id[:8]}"
    command = [
        systemd_run,
        "--user",
        "--quiet",
        "--collect",
        "--no-block",
        "--service-type=exec",
        f"--unit={unit}",
        f"--property=RuntimeMaxSec={ROUTE_LEASE_SECONDS}",
        "--property=TimeoutStopSec=15",
        openclaw,
        "agent",
        "--agent",
        OPENCLAW_AGENT,
        "--session-key",
        f"agent:{OPENCLAW_AGENT}:council-{session_suffix}",
        "--model",
        OPENCLAW_MODEL,
        "--thinking",
        OPENCLAW_THINKING,
        "--message",
        _openclaw_prompt(board, route_id, question),
        "--json",
    ]
    _run(command, timeout=30)


def _systemd_unit_state(unit: str | None) -> dict[str, Any]:
    if not unit:
        return {"available": False, "reason": "no unit recorded"}
    systemctl = os.environ.get("COUNCIL_SYSTEMCTL") or shutil.which("systemctl")
    if not systemctl:
        return {"available": False, "reason": "systemctl not found"}
    process = subprocess.run(
        [
            systemctl,
            "--user",
            "show",
            unit,
            "--property=LoadState,ActiveState,SubState,Result,ExecMainStatus",
        ],
        text=True,
        capture_output=True,
        timeout=10,
        check=False,
    )
    if process.returncode:
        return {
            "available": False,
            "reason": (process.stderr or process.stdout or "systemctl failed")[-1000:],
        }
    state: dict[str, Any] = {"available": True, "unit": unit}
    for line in process.stdout.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            state[key] = value
    return state


def _unit_finished(state: dict[str, Any]) -> bool:
    return bool(
        state.get("available")
        and state.get("LoadState") != "not-found"
        and state.get("ActiveState") in {"inactive", "failed"}
    )


def _unit_failed(state: dict[str, Any]) -> bool:
    if not state.get("available"):
        return False
    if state.get("ActiveState") == "failed":
        return True
    result = str(state.get("Result", ""))
    exit_status = str(state.get("ExecMainStatus", ""))
    return result not in {"", "success"} or exit_status not in {"", "0"}


def _error(error: Exception, **extra: Any) -> str:
    return json.dumps(
        {"ok": False, "error": str(error), **extra},
        ensure_ascii=False,
    )


def _format_results(results: list[dict[str, Any]]) -> str:
    parts: list[str] = []
    for result in results[-12:]:
        parts.append(
            f"{result.get('collection', 'entry')}: {result.get('content', '')}"
        )
    return "\n".join(parts)


class Tools:
    # Open WebUI's automatic citation cards are not useful for local board paths.
    citation = False

    def start_council(self, topic: str, __user__: dict = None) -> str:
        """Create a fresh typed blackboard and a separate visible Open WebUI council room."""
        try:
            user_id = (__user__ or {}).get("id")
            if not user_id:
                raise ValueError("authenticated Open WebUI user required")
            if not COUNCIL.is_file():
                raise FileNotFoundError(f"council helper not found: {COUNCIL}")
            output = _run(
                [
                    PYTHON,
                    str(COUNCIL),
                    "room",
                    "--topic",
                    _normalise(topic),
                    "--user-id",
                    str(user_id),
                ],
                timeout=60,
            )
            data = _json_output(output)
            data["ok"] = True
            data["instruction"] = (
                "Open chat_url. Consultations are correlated by route_id; repeated calls will "
                "reuse the live route instead of launching duplicate OpenClaw turns."
            )
            return json.dumps(data, ensure_ascii=False)
        except Exception as error:
            return _error(error)

    def read_council(
        self,
        board_path: str,
        full: bool = False,
        recent_per_collection: int = 6,
    ) -> str:
        """Validate and read either a compact council summary or the full blackboard."""
        try:
            board = _board(board_path)
            if full:
                _bb("validate", str(board))
                return _bb("show", str(board))
            return _bb(
                "summary",
                str(board),
                "--limit",
                str(max(1, min(int(recent_per_collection or 6), 20))),
            )
        except Exception as error:
            return _error(error)

    def contribute(
        self,
        board_path: str,
        entry_type: str,
        content: str,
        confidence: float = 0.75,
        route_id: str = "",
    ) -> str:
        """Append one typed Ornith contribution, optionally correlated to a council route."""
        allowed = set(RESULT_COLLECTIONS)
        try:
            if entry_type not in allowed:
                raise ValueError(f"unsupported entry_type: {entry_type}")
            text = _normalise(content)
            if not text:
                raise ValueError("content must not be empty")
            board = _board(board_path)
            arguments = [
                "add",
                str(board),
                entry_type,
                "--content",
                text,
                "--model",
                ORNITH_MODEL_ID,
                "--agent",
                "open-webui",
                "--kind",
                "model_output",
                "--source",
                "Open WebUI council conversation",
                "--json",
            ]
            if entry_type in {"facts", "inferences"}:
                bounded = max(0.0, min(float(confidence), 1.0))
                arguments += ["--confidence", str(bounded)]
            if route_id:
                arguments += ["--route-id", route_id]
            data = _bb_json(*arguments)
            return json.dumps(data, ensure_ascii=False)
        except Exception as error:
            return _error(error)

    def consult_openclaw(
        self,
        board_path: str,
        question: str,
        ornith_position: str = "",
    ) -> str:
        """Route exactly one idempotent, leased council turn to OpenClaw."""
        try:
            board = _board(board_path)
            cleaned_question = _normalise(question)
            if not cleaned_question:
                raise ValueError("question must not be empty")

            summary = _summary(board)
            if summary.get("status") != "active":
                raise RuntimeError(f"board state is {summary.get('status')}")

            pending = summary.get("active_route") or None
            created_new_route = False
            if pending:
                pending_question = _normalise(
                    (pending.get("payload") or {}).get("instruction", "")
                )
                if pending_question != cleaned_question:
                    return json.dumps(
                        {
                            "ok": False,
                            "error": "board already has a different pending route",
                            "pending": pending,
                        },
                        ensure_ascii=False,
                    )
                route_id = str(pending["route_id"])
                route_data = _route_status(board, route_id)
                claim = route_data.get("claim") or {}
                if route_data.get("state") == "claimed" and route_data.get("claim_live"):
                    return json.dumps(
                        {
                            "ok": True,
                            "queued": True,
                            "idempotent": True,
                            "route_id": route_id,
                            "unit": claim.get("unit"),
                            "board": str(board),
                            "instruction": "Call await_openclaw with this route_id.",
                        },
                        ensure_ascii=False,
                    )
            else:
                try:
                    routed = _bb_json(
                        "route",
                        str(board),
                        "--capability",
                        "independent judgement and synthesis",
                        "--recommended-model",
                        OPENCLAW_MODEL,
                        "--instruction",
                        cleaned_question,
                        "--model",
                        ORNITH_MODEL_ID,
                        "--agent",
                        "open-webui",
                        "--json",
                    )
                    route_id = str(routed["route_id"])
                    created_new_route = True
                except RuntimeError:
                    # A concurrent caller may have created the same route between
                    # our summary read and route command. Re-read before failing.
                    refreshed = _summary(board)
                    pending = refreshed.get("active_route") or {}
                    if _normalise((pending.get("payload") or {}).get("instruction", "")) != cleaned_question:
                        raise
                    route_id = str(pending["route_id"])

            if created_new_route and _normalise(ornith_position):
                try:
                    _bb_json(
                        "add",
                        str(board),
                        "inferences",
                        "--content",
                        _normalise(ornith_position),
                        "--confidence",
                        "0.75",
                        "--model",
                        ORNITH_MODEL_ID,
                        "--agent",
                        "open-webui",
                        "--kind",
                        "model_output",
                        "--source",
                        "Open WebUI council position",
                        "--route-id",
                        route_id,
                        "--json",
                    )
                except Exception as error:
                    _bb_json(
                        "fail-route",
                        str(board),
                        route_id,
                        "--model",
                        ORNITH_MODEL_ID,
                        "--agent",
                        "open-webui",
                        "--error",
                        f"failed to record Ornith position: {error}",
                        "--json",
                    )
                    raise

            unit = f"openclaw-council-{route_id.replace('-', '')[:16]}"
            try:
                claim = _bb_json(
                    "claim-route",
                    str(board),
                    route_id,
                    "--model",
                    ORNITH_MODEL_ID,
                    "--agent",
                    "open-webui",
                    "--unit",
                    unit,
                    "--lease-seconds",
                    str(ROUTE_LEASE_SECONDS),
                    "--json",
                )
            except RuntimeError:
                current = _route_status(board, route_id)
                current_claim = current.get("claim") or {}
                if current.get("state") == "claimed" and current.get("claim_live"):
                    return json.dumps(
                        {
                            "ok": True,
                            "queued": True,
                            "idempotent": True,
                            "route_id": route_id,
                            "unit": current_claim.get("unit"),
                            "board": str(board),
                            "instruction": "Call await_openclaw with this route_id.",
                        },
                        ensure_ascii=False,
                    )
                raise

            try:
                _launch_openclaw(board, route_id, cleaned_question, unit)
            except Exception as error:
                _bb_json(
                    "fail-route",
                    str(board),
                    route_id,
                    "--model",
                    ORNITH_MODEL_ID,
                    "--agent",
                    "open-webui",
                    "--error",
                    f"launch failed: {error}",
                    "--json",
                )
                raise

            return json.dumps(
                {
                    "ok": True,
                    "queued": True,
                    "idempotent": False,
                    "route_id": route_id,
                    "unit": unit,
                    "lease_until": claim.get("lease_until"),
                    "board": str(board),
                    "instruction": "Call await_openclaw with this board and route_id to collect the contribution.",
                },
                ensure_ascii=False,
            )
        except Exception as error:
            return _error(error)

    def await_openclaw(
        self,
        board_path: str,
        route_id: str,
        timeout_seconds: int = 0,
    ) -> str:
        """Poll briefly for one specific route and resolve only its correlated contributions."""
        try:
            board = _board(board_path)
            wait_seconds = max(
                0,
                min(int(timeout_seconds or 0), MAX_AWAIT_SECONDS),
            )
            deadline = time.monotonic() + wait_seconds

            while True:
                status = _route_status(board, route_id)
                if not status.get("found"):
                    raise ValueError("route not found")

                tagged = _route_results(board, route_id).get("results", [])
                results = [
                    item
                    for item in tagged
                    if str((item.get("written_by") or {}).get("model", "")).startswith(
                        OPENCLAW_WRITER_PREFIX
                    )
                ]
                correlation = "route_id"
                if not results:
                    results = _fallback_route_results(
                        board,
                        route_id,
                        status.get("created_at"),
                    )
                    if results:
                        correlation = "writer_and_timestamp_fallback"

                if results:
                    result_ids = [
                        str(item["entry_id"])
                        for item in results
                        if item.get("entry_id")
                    ]
                    if status.get("state") in {"pending", "claimed"}:
                        arguments = [
                            "resolve-route",
                            str(board),
                            route_id,
                            "--model",
                            ORNITH_MODEL_ID,
                            "--agent",
                            "open-webui",
                            "--json",
                        ]
                        for entry_id in result_ids:
                            arguments += ["--result-entry", entry_id]
                        _bb_json(*arguments)
                    return json.dumps(
                        {
                            "ok": True,
                            "pending": False,
                            "route_id": route_id,
                            "correlation": correlation,
                            "openclaw_reply": _format_results(results),
                            "entries": results[-12:],
                            "board": str(board),
                        },
                        ensure_ascii=False,
                    )

                if status.get("state") == "failed":
                    resolution = status.get("resolution") or {}
                    raise RuntimeError(
                        f"OpenClaw route failed: {resolution.get('error') or 'unknown error'}"
                    )
                if status.get("state") == "resolved":
                    return json.dumps(
                        {
                            "ok": True,
                            "pending": False,
                            "route_id": route_id,
                            "openclaw_reply": "",
                            "warning": "route is resolved but has no correlated result entries",
                            "board": str(board),
                        },
                        ensure_ascii=False,
                    )

                claim = status.get("claim") or {}
                if status.get("state") == "claimed" and not status.get("claim_live"):
                    return json.dumps(
                        {
                            "ok": True,
                            "pending": True,
                            "route_id": route_id,
                            "state": "claim_expired",
                            "unit": claim.get("unit"),
                            "lease_until": claim.get("lease_until"),
                            "board": str(board),
                            "instruction": (
                                "The route lease expired without a result. Call consult_openclaw "
                                "again with the same question to reclaim and relaunch it."
                            ),
                        },
                        ensure_ascii=False,
                    )

                unit_state = _systemd_unit_state(claim.get("unit"))
                if _unit_finished(unit_state):
                    if _unit_failed(unit_state):
                        detail = (
                            f"systemd unit {claim.get('unit')} failed: "
                            f"result={unit_state.get('Result')} "
                            f"exit={unit_state.get('ExecMainStatus')}"
                        )
                    else:
                        detail = (
                            f"systemd unit {claim.get('unit')} completed without adding "
                            "a route-correlated contribution"
                        )
                    _bb_json(
                        "fail-route",
                        str(board),
                        route_id,
                        "--model",
                        ORNITH_MODEL_ID,
                        "--agent",
                        "open-webui",
                        "--error",
                        detail,
                        "--json",
                    )
                    raise RuntimeError(detail)

                if time.monotonic() >= deadline:
                    return json.dumps(
                        {
                            "ok": True,
                            "pending": True,
                            "route_id": route_id,
                            "state": status.get("state"),
                            "unit": claim.get("unit"),
                            "unit_state": unit_state,
                            "lease_until": claim.get("lease_until"),
                            "board": str(board),
                            "instruction": "Call await_openclaw again with the same route_id.",
                        },
                        ensure_ascii=False,
                    )
                time.sleep(0.75)
        except Exception as error:
            return _error(error, route_id=route_id)

    def cancel_openclaw(self, board_path: str, route_id: str, reason: str) -> str:
        """Stop a live council unit and explicitly fail its pending route."""
        try:
            board = _board(board_path)
            status = _route_status(board, route_id)
            if not status.get("found"):
                raise ValueError("route not found")
            if status.get("state") in {"resolved", "failed"}:
                return json.dumps(
                    {
                        "ok": True,
                        "route_id": route_id,
                        "state": status.get("state"),
                        "idempotent": True,
                    },
                    ensure_ascii=False,
                )
            unit = (status.get("claim") or {}).get("unit")
            systemctl = os.environ.get("COUNCIL_SYSTEMCTL") or shutil.which("systemctl")
            if unit and systemctl:
                subprocess.run(
                    [systemctl, "--user", "stop", unit],
                    text=True,
                    capture_output=True,
                    timeout=15,
                    check=False,
                )
            failed = _bb_json(
                "fail-route",
                str(board),
                route_id,
                "--model",
                ORNITH_MODEL_ID,
                "--agent",
                "open-webui",
                "--error",
                _normalise(reason) or "cancelled by council",
                "--json",
            )
            return json.dumps(failed, ensure_ascii=False)
        except Exception as error:
            return _error(error, route_id=route_id)

    def handover(
        self,
        board_path: str,
        outcome: str,
        unresolved: str,
        next_action: str,
    ) -> str:
        """Append a compact operational handover as an action, not as evidence."""
        try:
            board = _board(board_path)
            content = (
                f"Council handover — outcome: {_normalise(outcome)}; "
                f"unresolved: {_normalise(unresolved)}; "
                f"next action: {_normalise(next_action)}"
            )
            data = _bb_json(
                "add",
                str(board),
                "actions",
                "--content",
                content,
                "--target",
                f"council://{board.name}/handover",
                "--model",
                ORNITH_MODEL_ID,
                "--agent",
                "open-webui",
                "--kind",
                "model_output",
                "--source",
                "Open WebUI council handover",
                "--json",
            )
            data["handover"] = content
            return json.dumps(data, ensure_ascii=False)
        except Exception as error:
            return _error(error)

    def council_doctor(self) -> str:
        """Check configured helper paths and the Open WebUI database schema."""
        try:
            if not COUNCIL.is_file():
                raise FileNotFoundError(f"council helper not found: {COUNCIL}")
            return _run([PYTHON, str(COUNCIL), "doctor"], timeout=30)
        except Exception as error:
            return _error(error)
