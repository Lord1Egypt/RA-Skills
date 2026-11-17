#!/usr/bin/env python3
"""AGY -> Kiro ACP bridge (Kiro CLI V3 only).

Dispatches an engineering job from AGY to the Kiro ``ppt-engineer`` custom agent
over the Agent Client Protocol (ACP), using newline-delimited JSON-RPC 2.0 on the
child process stdin/stdout.

Design constraints enforced here (see ``docs/agent-routing.md`` and
``docs/oauth-subscription-runtime.md``):

* V3 only. The single supported runtime is
  ``kiro-cli --v3 acp --auth-method cli``. There is no V2 code path and no
  engine fallback; a legacy ``engine="v2"`` request is refused with
  ``UNSUPPORTED_KIRO_ENGINE``.
* OAuth-only. The bridge never reads, copies, stores or forwards OAuth tokens.
  It relies on the already-authenticated local ``kiro-cli`` session and lets
  ``--auth-method cli`` resolve access tokens inside kiro-cli.
* No API keys. API-key style environment variables are stripped from the child
  environment so an API fallback cannot silently happen.
* Agent scope is a turn-long invariant. The agent is selected with
  ``session/set_mode`` and confirmed by the engine before any prompt is sent
  (otherwise ``ENGINEERING_AGENT_UNAVAILABLE``), and the active agent is watched
  for the whole turn (drift -> cancel + ``ENGINEERING_AGENT_SCOPE_LOST``).
* Kiro must not call Codex. Tool calls / permission requests that look like a
  Codex or image-generation invocation are denied and reported.
* Runtime permission enforcement. ``.kiro/agents/ppt-engineer.md`` says what the
  agent may ask for; this bridge decides what is approved, and the stricter rule
  wins. No version control, no shell chaining, dependency changes need explicit
  authorization, writes stay inside the repository root.
* Control returns to AGY. The bridge performs exactly one prompt turn, then
  reports a structured result and exits.

Usage::

    python3 kiro_acp_bridge.py --input job.json --output result.json
    cat job.json | python3 kiro_acp_bridge.py

JSON-RPC flow::

    -> initialize                 {protocolVersion, clientCapabilities}
    <- result                     {protocolVersion, agentCapabilities, authMethods}
    -> session/new                {cwd, mcpServers}
    <- result                     {sessionId, modes:{availableModes, currentModeId}}
    -> session/set_mode           {sessionId, modeId: "ppt-engineer"}
    <- session/update             config_option_update -> mode.currentValue
    <- result                     {}          (empty even for an unknown modeId)
    -> session/prompt             {sessionId, prompt:[{type:"text", text}]}
    <- session/update             agent_message_chunk / tool_call / tool_call_update
    <- session/request_permission {sessionId, toolCall, options, _meta.kiro.consent}
    -> result                     {outcome:{outcome:"selected", optionId}}
    <- result                     {stopReason:"end_turn"}   <- turn end

Request JSON (all fields optional unless marked required)::

    {
      "repository_root": "/abs/path",          # required
      "task": "engineering request",           # required
      "allowed_scope": ["scripts/", "tests/"],
      "acceptance_criteria": ["..."],
      "verification": ["..."],
      "notes": "free-form context",
      "agent": "ppt-engineer",
      "command": ["kiro-cli", "--v3", "acp", "--auth-method", "cli"],
      "cwd": "/abs/path",
      "session_id": "reuse-an-existing-session",
      "timeout_seconds": 900,
      "startup_timeout_seconds": 30,
      "agent_select_timeout_seconds": 30,
      "cancel_grace_seconds": 15,
      "permission_mode": "allow_once",         # allow_once | allow_always | reject
      "require_agent_scope": true,             # refuse to prompt an unscoped agent
      "allow_dependency_changes": false,       # authorize pip install / uv add / ...
      "raw_prompt": false                      # true -> send "task" verbatim
    }

Response JSON::

    {
      "schema": "agy-ppt/kiro-acp-bridge-result/1",
      "status": "completed|incomplete|cancelled|timeout|failed|unavailable"
                "|agent_unavailable|agent_scope_lost",
      "error_code": null | "ENGINEERING_WORKER_UNAVAILABLE"
                         | "ENGINEERING_AGENT_UNAVAILABLE"
                         | "ENGINEERING_AGENT_SCOPE_LOST"
                         | "UNSUPPORTED_KIRO_ENGINE" | ...,
      "control": "returned_to_agy",
      "agent": "ppt-engineer",
      "session_id": "...",
      "stop_reason": "end_turn",
      "agent_text": "...",
      "messages": [...],
      "tool_calls": [...],
      "permission_decisions": [...],
      "policy_violations": [...],
      "warnings": [...],
      "timeline": [...],
      "diagnostics": {
        "engine": "v3", "auth": "cli",
        "agent_requested": "ppt-engineer",
        "agent_resolved": true,
        "agent_scoped": true,
        "agent_scope_lost": false,
        "agent_selection": {"method": "session/set_mode", ...},
        "engine_fallback_used": false,
        ...
      }
    }
"""

from __future__ import annotations

import argparse
import json
import os
import queue
import re
import shlex
import signal
import subprocess
import sys
import threading
import time
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Iterable, Sequence

RESULT_SCHEMA = "agy-ppt/kiro-acp-bridge-result/1"
REQUEST_SCHEMA = "agy-ppt/kiro-acp-bridge-request/1"

DEFAULT_AGENT = "ppt-engineer"

# Kiro runtime: V3 only.
#
# `--v3` selects the next generation Kiro agent engine. Its `acp` subcommand
# rejects `--agent`, so the custom agent is selected *inside* the ACP session
# with `session/set_mode`. `--auth-method cli` keeps access-token resolution
# inside kiro-cli; without it the engine asks the ACP *client* to broker OAuth
# tokens, which this bridge must never do.
ENGINE_V3 = "v3"
SUPPORTED_ENGINES = (ENGINE_V3,)
DEFAULT_ENGINE = ENGINE_V3
DEFAULT_COMMAND: tuple[str, ...] = ("kiro-cli", "--v3", "acp", "--auth-method", "cli")
ACP_PROTOCOL_VERSION = 1

# The only supported way to bind a custom agent to a V3 ACP session.
SELECTION_SET_MODE = "session/set_mode"

# v3 engine extension notifications.
KIRO_POLICY_CHANGED = "_kiro/policy/changed"
KIRO_TOOLS_DID_CHANGE = "_kiro/tools/didChange"
# `configOptions` entry that reports the session's active agent/mode.
MODE_OPTION_ID = "mode"

DEFAULT_TIMEOUT_SECONDS = 900.0
DEFAULT_STARTUP_TIMEOUT_SECONDS = 30.0
DEFAULT_CANCEL_GRACE_SECONDS = 15.0
# Extra window spent waiting for the engine to confirm the active agent.
DEFAULT_AGENT_SELECT_TIMEOUT_SECONDS = 30.0

# Status values
STATUS_COMPLETED = "completed"
STATUS_INCOMPLETE = "incomplete"
STATUS_CANCELLED = "cancelled"
STATUS_TIMEOUT = "timeout"
STATUS_FAILED = "failed"
STATUS_UNAVAILABLE = "unavailable"
STATUS_AGENT_UNAVAILABLE = "agent_unavailable"
STATUS_AGENT_SCOPE_LOST = "agent_scope_lost"

# Failure contract codes. ENGINEERING_WORKER_UNAVAILABLE is the contract value
# required by SKILL.md whenever the Kiro worker cannot be reached at all.
# ENGINEERING_AGENT_UNAVAILABLE means the worker is reachable but the session
# could not be bound to the requested engineering agent, so no coding task was
# dispatched. ENGINEERING_AGENT_SCOPE_LOST means the agent was confirmed, the
# turn started, and the active agent then drifted away from ppt-engineer.
ERROR_WORKER_UNAVAILABLE = "ENGINEERING_WORKER_UNAVAILABLE"
ERROR_AGENT_UNAVAILABLE = "ENGINEERING_AGENT_UNAVAILABLE"
ERROR_AGENT_SCOPE_LOST = "ENGINEERING_AGENT_SCOPE_LOST"
ERROR_UNSUPPORTED_ENGINE = "UNSUPPORTED_KIRO_ENGINE"
ERROR_WORKER_TIMEOUT = "ENGINEERING_WORKER_TIMEOUT"
ERROR_WORKER_CANCELLED = "ENGINEERING_WORKER_CANCELLED"
ERROR_WORKER_PROTOCOL = "ENGINEERING_WORKER_PROTOCOL_ERROR"
ERROR_WORKER_TURN_FAILED = "ENGINEERING_WORKER_TURN_FAILED"
ERROR_INVALID_REQUEST = "ENGINEERING_TASK_INVALID"

PERMISSION_ALLOW_ONCE = "allow_once"
PERMISSION_ALLOW_ALWAYS = "allow_always"
PERMISSION_REJECT = "reject"
PERMISSION_MODES = (PERMISSION_ALLOW_ONCE, PERMISSION_ALLOW_ALWAYS, PERMISSION_REJECT)

# Environment variables that would turn this OAuth-only path into a billed API
# path. They are removed from the child environment.
BLOCKED_ENV_VARS = (
    "KIRO_API_KEY",
    "OPENAI_API_KEY",
    "CODEX_API_KEY",
    "GEMINI_API_KEY",
    "GOOGLE_API_KEY",
    "ANTHROPIC_API_KEY",
    "IMAGE_API_KEY",
    "CODEX_PPT_API_KEY",
    "CODEX_PPT_IMAGE_API_KEY",
)
BLOCKED_ENV_PATTERN = re.compile(
    r"(?i)(?:^|_)(?:API_KEY|APIKEY|ACCESS_TOKEN|REFRESH_TOKEN|ID_TOKEN|BEARER_TOKEN|SESSION_TOKEN)$"
)

# Codex / image-generation invocations that Kiro must not perform itself.
CODEX_INVOCATION_PATTERN = re.compile(
    r"(?i)(?:\bcodex(?:-cli)?\b|\$imagegen\b|\bimagegen\b|\bimage_gen\b|\bimage_providers\b)"
)

# ---------------------------------------------------------------------------
# ppt-engineer runtime permission policy
#
# `.kiro/agents/ppt-engineer.md` defines what the agent *can* ask for.
# This policy defines what the bridge will *approve* at runtime. When the two
# disagree, the stricter rule wins, so the bridge is deliberately narrower than
# the agent profile:
#   * no version control at all (this skill needs no git capability),
#   * no shell chaining / substitution, because it escapes the allowlist,
#   * dependency-changing commands need explicit authorization,
#   * writes must stay inside the repository root.
# ---------------------------------------------------------------------------
DEFAULT_SHELL_ALLOWLIST: tuple[str, ...] = (
    "python",
    "python3",
    "pytest",
    "pip",
    "pip3",
    "uv",
)

# Package-manager subcommands that mutate the environment, dependencies or a
# lockfile. Denied unless `allow_dependency_changes` is explicitly enabled.
DEPENDENCY_CHANGING_SUBCOMMANDS: dict[str, frozenset[str]] = {
    "pip": frozenset({"install", "uninstall", "download", "wheel"}),
    "pip3": frozenset({"install", "uninstall", "download", "wheel"}),
    "uv": frozenset({"add", "remove", "sync", "lock", "pip", "tool", "self"}),
}
# `python -m pip install ...` reaches the same place through a different door.
MODULE_DEPENDENCY_TOOLS = frozenset({"pip", "pip3", "uv", "ensurepip", "venv"})

# Programs that are never approved, whatever else the request says.
PERMANENTLY_DENIED_PROGRAMS = frozenset(
    {
        "sudo",
        "doas",
        "su",
        "rm",
        "rmdir",
        "mv",
        "dd",
        "mkfs",
        "shutdown",
        "reboot",
        "kill",
        "killall",
        "pkill",
        "chmod",
        "chown",
        "curl",
        "wget",
        "ssh",
        "scp",
        "sh",
        "bash",
        "zsh",
        "npx",
        "npm",
        "pnpm",
        "yarn",
        "brew",
        "apt",
        "apt-get",
        "docker",
        "git",
    }
)
# Shell syntax that would let an allowlisted command launch a different one.
SHELL_CHAINING_PATTERN = re.compile(r"(?:;|&&|\|\||\||`|\$\(|<\(|>\(|\n)")

READ_CAPABILITIES = frozenset({"fs_read", "read", "search", "think"})
WRITE_CAPABILITIES = frozenset({"fs_write", "write", "edit", "delete", "move"})
SHELL_CAPABILITIES = frozenset({"shell", "execute", "run_command"})

_REDACTIONS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"(?i)\b(bearer)\s+[A-Za-z0-9._\-]{12,}"), r"\1 [REDACTED]"),
    (re.compile(r"\bsk-[A-Za-z0-9._\-]{12,}"), "[REDACTED]"),
    (
        re.compile(
            r"(?i)(\"?(?:access|refresh|id|session)_token\"?\s*[:=]\s*\"?)[A-Za-z0-9._\-]{12,}"
        ),
        r"\1[REDACTED]",
    ),
    (re.compile(r"(?i)(\"?api[_-]?key\"?\s*[:=]\s*\"?)[A-Za-z0-9._\-]{12,}"), r"\1[REDACTED]"),
)


def now_iso() -> str:
    """UTC timestamp, matching the style used by the other skill scripts."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def redact(text: str) -> str:
    """Strip credential-looking substrings from anything we echo back to AGY."""
    if not text:
        return text
    for pattern, replacement in _REDACTIONS:
        text = pattern.sub(replacement, text)
    return text


def sanitize_env(base: dict[str, str] | None = None) -> tuple[dict[str, str], list[str]]:
    """Return a child environment with API-key style variables removed.

    Only variable *names* are reported, never values.
    """
    source = dict(os.environ if base is None else base)
    removed: list[str] = []
    for name in list(source):
        if name in BLOCKED_ENV_VARS or BLOCKED_ENV_PATTERN.search(name):
            source.pop(name, None)
            removed.append(name)
    return source, sorted(removed)


def looks_like_codex_invocation(*values: Any) -> bool:
    """True when any value looks like an attempt to drive Codex / image gen."""
    for value in values:
        if value is None:
            continue
        text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, default=str)
        if CODEX_INVOCATION_PATTERN.search(text):
            return True
    return False


@dataclass(frozen=True)
class PolicyDecision:
    """Outcome of evaluating one permission request against the agent policy."""

    allowed: bool
    rule: str
    reason: str


@dataclass(frozen=True)
class ConsentView:
    """Normalized view of a `session/request_permission` payload.

    Kiro v3 puts the useful detail in ``_meta.kiro`` (``toolId``, ``command``
    and ``consent`` with ``capability`` / ``resource`` / ``matchedRule`` /
    ``workspaceRoot``); the ACP-standard ``toolCall`` only carries an id, a
    status and a title. Older shapes keep it in ``toolCall.rawInput``.
    """

    capability: str = ""
    resource: str = ""
    command: str = ""
    path: str = ""
    title: str = ""
    tool_id: str = ""
    kind: str = ""
    workspace_root: str = ""
    matched_rule: dict[str, Any] = field(default_factory=dict)
    source: str = ""
    raw: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_permission_request(
        cls,
        params: dict[str, Any],
        tool_call_hint: dict[str, Any] | None = None,
    ) -> "ConsentView":
        tool_call = params.get("toolCall") if isinstance(params.get("toolCall"), dict) else {}
        meta = cls._kiro_meta(params) or cls._kiro_meta(tool_call)
        consent = meta.get("consent") if isinstance(meta.get("consent"), dict) else {}

        raw_input = tool_call.get("rawInput") or tool_call.get("raw_input") or {}
        if not isinstance(raw_input, dict):
            raw_input = {}
        hint_input: dict[str, Any] = {}
        if tool_call_hint:
            candidate = tool_call_hint.get("raw_input")
            if isinstance(candidate, dict):
                hint_input = candidate

        capability = str(
            consent.get("capability")
            or meta.get("capability")
            or tool_call.get("kind")
            or (tool_call_hint or {}).get("kind")
            or ""
        )
        command = str(
            meta.get("command")
            or raw_input.get("command")
            or hint_input.get("command")
            or (consent.get("resource") if capability in SHELL_CAPABILITIES else "")
            or ""
        )
        path = str(
            raw_input.get("path")
            or hint_input.get("path")
            or (consent.get("resource") if capability in WRITE_CAPABILITIES else "")
            or ""
        )
        return cls(
            capability=capability,
            resource=str(consent.get("resource") or ""),
            command=command,
            path=path,
            title=str(tool_call.get("title") or (tool_call_hint or {}).get("title") or ""),
            tool_id=str(meta.get("toolId") or ""),
            kind=str(tool_call.get("kind") or (tool_call_hint or {}).get("kind") or ""),
            workspace_root=str(consent.get("workspaceRoot") or ""),
            matched_rule=consent.get("matchedRule")
            if isinstance(consent.get("matchedRule"), dict)
            else {},
            source=str(consent.get("source") or ""),
            raw={"params": params, "tool_call_hint": tool_call_hint},
        )

    @staticmethod
    def _kiro_meta(payload: dict[str, Any]) -> dict[str, Any]:
        meta = payload.get("_meta")
        if isinstance(meta, dict) and isinstance(meta.get("kiro"), dict):
            return meta["kiro"]
        return {}

    def codex_surface(self) -> tuple[Any, ...]:
        return (self.command, self.path, self.title, self.resource, self.tool_id)

    def describe(self) -> str:
        detail = self.command or self.path or self.resource or self.title
        return f"{self.capability or self.kind or 'unknown'}: {detail}"


class PermissionPolicy:
    """Decides whether a permission request stays inside the ppt-engineer policy."""

    def __init__(
        self,
        repository_root: str,
        shell_allowlist: Sequence[str] = DEFAULT_SHELL_ALLOWLIST,
        allow_dependency_changes: bool = False,
    ) -> None:
        self.repository_root = os.path.realpath(os.path.expanduser(repository_root or os.getcwd()))
        self.shell_allowlist = tuple(shell_allowlist)
        self.allow_dependency_changes = allow_dependency_changes

    def describe(self) -> dict[str, Any]:
        return {
            "repository_root": self.repository_root,
            "shell_allowlist": list(self.shell_allowlist),
            "allow_dependency_changes": self.allow_dependency_changes,
            "version_control": "not_available",
            "codex_invocation": "always_denied",
            "shell_chaining": "always_denied",
        }

    def evaluate(self, view: ConsentView) -> PolicyDecision:
        if looks_like_codex_invocation(*view.codex_surface()):
            return PolicyDecision(
                False,
                "kiro_must_not_call_codex",
                "Codex / image generation is owned by AGY, never by the engineering worker",
            )

        capability = view.capability.lower()
        if capability in READ_CAPABILITIES:
            return PolicyDecision(True, "read_allowed", "project reads are inside the agent policy")
        if capability in WRITE_CAPABILITIES:
            return self._evaluate_write(view)
        if capability in SHELL_CAPABILITIES:
            return self._evaluate_shell(view)
        return PolicyDecision(
            False,
            "capability_not_in_agent_policy",
            f"capability '{view.capability or view.kind or 'unknown'}' is outside the "
            "ppt-engineer policy (read / write / shell only)",
        )

    def _evaluate_write(self, view: ConsentView) -> PolicyDecision:
        target = view.path or view.resource
        if not target:
            return PolicyDecision(
                False, "write_path_unknown", "write request carries no resolvable path"
            )
        root = os.path.realpath(view.workspace_root) if view.workspace_root else self.repository_root
        candidate = target if os.path.isabs(target) else os.path.join(root, target)
        candidate = os.path.realpath(candidate)
        if candidate == self.repository_root or candidate.startswith(self.repository_root + os.sep):
            return PolicyDecision(
                True, "write_within_repository", f"writes inside {self.repository_root}"
            )
        return PolicyDecision(
            False,
            "write_outside_repository",
            f"write target '{target}' resolves outside the repository root",
        )

    def _evaluate_shell(self, view: ConsentView) -> PolicyDecision:
        command = (view.command or "").strip()
        if not command:
            return PolicyDecision(
                False, "shell_command_unknown", "shell request carries no readable command"
            )
        if SHELL_CHAINING_PATTERN.search(command):
            return PolicyDecision(
                False,
                "shell_chaining_denied",
                "chained, piped or substituted shell commands can escape the allowlist",
            )
        try:
            argv = shlex.split(command)
        except ValueError:
            argv = command.split()
        if not argv:
            return PolicyDecision(
                False, "shell_command_unknown", "shell request carries no readable command"
            )

        program = os.path.basename(argv[0])
        if program in PERMANENTLY_DENIED_PROGRAMS:
            return PolicyDecision(
                False,
                "program_permanently_denied",
                f"'{program}' is never approved for the engineering worker",
            )
        if program not in self.shell_allowlist:
            return PolicyDecision(
                False,
                "shell_program_not_allowed",
                f"'{program}' is not in the ppt-engineer shell allowlist",
            )

        dependency_target = self._dependency_change_target(program, argv)
        if dependency_target is not None and not self.allow_dependency_changes:
            return PolicyDecision(
                False,
                "dependency_change_requires_explicit_authorization",
                f"'{dependency_target}' changes dependencies or lockfiles; set "
                "allow_dependency_changes=true to authorize it",
            )
        if dependency_target is not None:
            return PolicyDecision(
                True,
                "dependency_change_authorized",
                f"'{dependency_target}' authorized by allow_dependency_changes=true",
            )
        return PolicyDecision(True, "shell_allowed", f"'{program}' is an allowed dev command")

    @staticmethod
    def _dependency_change_target(program: str, argv: list[str]) -> str | None:
        """Return a description when argv mutates dependencies, else None."""
        args = [arg for arg in argv[1:] if not arg.startswith("-")]
        mutating = DEPENDENCY_CHANGING_SUBCOMMANDS.get(program)
        if mutating and args and args[0] in mutating:
            return f"{program} {args[0]}"
        # `python -m pip install ...` / `python3 -m uv add ...`
        if program in {"python", "python3"} and "-m" in argv:
            module_index = argv.index("-m") + 1
            if module_index < len(argv) and argv[module_index] in MODULE_DEPENDENCY_TOOLS:
                module = argv[module_index]
                rest = [arg for arg in argv[module_index + 1 :] if not arg.startswith("-")]
                sub = rest[0] if rest else ""
                mutating = DEPENDENCY_CHANGING_SUBCOMMANDS.get(module, frozenset())
                if not mutating or (sub in mutating):
                    return f"{program} -m {module} {sub}".strip()
        return None


class TransportError(RuntimeError):
    """Transport level failure."""


class TransportStartError(TransportError):
    """The worker process could not be started."""


class ProtocolError(RuntimeError):
    """The peer violated the JSON-RPC / ACP contract."""


class UnsupportedEngineError(ValueError):
    """A caller asked for a Kiro engine this bridge refuses to run."""


class StdioProcessTransport:
    """Newline-delimited JSON-RPC 2.0 transport over a child process stdio."""

    def __init__(
        self,
        command: Sequence[str],
        cwd: str | None = None,
        env: dict[str, str] | None = None,
        stderr_lines: int = 40,
    ) -> None:
        self.command = list(command)
        self.cwd = cwd
        self.env = env
        self._process: subprocess.Popen[str] | None = None
        self._inbox: "queue.Queue[dict[str, Any] | None]" = queue.Queue()
        self._stderr: deque[str] = deque(maxlen=stderr_lines)
        self._noise: deque[str] = deque(maxlen=stderr_lines)
        self._threads: list[threading.Thread] = []
        self._closed = False
        self._drained = False

    # -- lifecycle ---------------------------------------------------------
    def start(self) -> None:
        try:
            self._process = subprocess.Popen(  # noqa: S603 - command comes from the AGY job
                self.command,
                cwd=self.cwd,
                env=self.env,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                # Own process group so helper processes spawned by the worker
                # (engine servers, TUI helpers) can be cleaned up together.
                start_new_session=True,
            )
        except FileNotFoundError as exc:
            raise TransportStartError(f"worker executable not found: {self.command[0]}") from exc
        except OSError as exc:
            raise TransportStartError(f"failed to start worker: {exc}") from exc

        self._threads = [
            threading.Thread(target=self._read_stdout, name="acp-stdout", daemon=True),
            threading.Thread(target=self._read_stderr, name="acp-stderr", daemon=True),
        ]
        for thread in self._threads:
            thread.start()

    def _read_stdout(self) -> None:
        stream = self._process.stdout if self._process else None
        if stream is None:  # pragma: no cover - defensive
            self._inbox.put(None)
            return
        try:
            for line in stream:
                line = line.strip()
                if not line:
                    continue
                try:
                    message = json.loads(line)
                except json.JSONDecodeError:
                    self._noise.append(redact(line[:500]))
                    continue
                if isinstance(message, dict):
                    self._inbox.put(message)
                else:
                    self._noise.append(redact(line[:500]))
        except (ValueError, OSError):  # stream closed underneath us
            pass
        finally:
            self._inbox.put(None)

    def _read_stderr(self) -> None:
        stream = self._process.stderr if self._process else None
        if stream is None:  # pragma: no cover - defensive
            return
        try:
            for line in stream:
                line = line.rstrip()
                if line:
                    self._stderr.append(redact(line[:500]))
        except (ValueError, OSError):  # pragma: no cover - defensive
            pass

    # -- io ----------------------------------------------------------------
    def send(self, message: dict[str, Any]) -> None:
        process = self._process
        if process is None or process.stdin is None:
            raise TransportError("worker stdin is not available")
        payload = json.dumps(message, ensure_ascii=False, default=str)
        try:
            process.stdin.write(payload + "\n")
            process.stdin.flush()
        except (BrokenPipeError, ValueError, OSError) as exc:
            raise TransportError(f"failed to write to worker: {exc}") from exc

    def receive(self, timeout: float) -> dict[str, Any] | None:
        """Return the next message, ``None`` on timeout or stream end."""
        try:
            message = self._inbox.get(timeout=max(timeout, 0.0))
        except queue.Empty:
            return None
        if message is None:
            # Sentinel: stdout reached EOF and everything before it was consumed.
            self._drained = True
            self._inbox.put(None)  # keep signalling EOF to later callers
            return None
        return message

    def at_eof(self) -> bool:
        return self._drained

    def is_alive(self) -> bool:
        return self._process is not None and self._process.poll() is None

    def exit_code(self) -> int | None:
        if self._process is None:
            return None
        if self._drained and self._process.poll() is None:
            try:
                self._process.wait(timeout=1.0)
            except subprocess.TimeoutExpired:  # pragma: no cover - defensive
                pass
        return self._process.poll()

    def stderr_tail(self) -> list[str]:
        if self._drained:
            # Let the stderr reader finish so failure diagnostics are complete.
            for thread in self._threads:
                if thread.name == "acp-stderr":
                    thread.join(timeout=1.0)
        return list(self._stderr)

    def noise_tail(self) -> list[str]:
        return list(self._noise)

    def close(self, terminate_timeout: float = 5.0) -> None:
        if self._closed:
            return
        self._closed = True
        process = self._process
        if process is None:
            return

        # Close stdin first so a well-behaved worker can exit on its own. stdout
        # and stderr stay open until the reader threads finish: closing them here
        # would race with the blocking reads in those threads.
        try:
            if process.stdin is not None:
                process.stdin.close()
        except OSError:  # pragma: no cover - defensive
            pass

        if process.poll() is None:
            self._signal_tree(signal.SIGTERM)
            try:
                process.wait(timeout=terminate_timeout)
            except subprocess.TimeoutExpired:
                self._signal_tree(signal.SIGKILL)
                try:
                    process.wait(timeout=terminate_timeout)
                except subprocess.TimeoutExpired:  # pragma: no cover - defensive
                    pass

        for thread in self._threads:
            thread.join(timeout=1.0)
        for stream in (process.stdout, process.stderr):
            try:
                if stream is not None:
                    stream.close()
            except OSError:  # pragma: no cover - defensive
                pass

    def _signal_tree(self, sig: int) -> None:
        """Signal the worker, including helper processes it spawned."""
        process = self._process
        if process is None:  # pragma: no cover - defensive
            return
        if hasattr(os, "killpg"):
            try:
                os.killpg(os.getpgid(process.pid), sig)
                return
            except (ProcessLookupError, PermissionError, OSError):
                pass
        try:
            process.kill() if sig == signal.SIGKILL else process.terminate()
        except (ProcessLookupError, OSError):  # pragma: no cover - defensive
            pass


@dataclass
class BridgeRequest:
    """Structured engineering job handed to the bridge by AGY."""

    repository_root: str
    task: str
    agent: str = DEFAULT_AGENT
    engine: str = DEFAULT_ENGINE
    command: list[str] = field(default_factory=list)
    cwd: str | None = None
    allowed_scope: list[str] = field(default_factory=list)
    acceptance_criteria: list[str] = field(default_factory=list)
    verification: list[str] = field(default_factory=list)
    notes: str | None = None
    session_id: str | None = None
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS
    startup_timeout_seconds: float = DEFAULT_STARTUP_TIMEOUT_SECONDS
    cancel_grace_seconds: float = DEFAULT_CANCEL_GRACE_SECONDS
    permission_mode: str = PERMISSION_ALLOW_ONCE
    raw_prompt: bool = False
    require_agent_scope: bool = True
    allow_dependency_changes: bool = False
    agent_select_timeout_seconds: float = DEFAULT_AGENT_SELECT_TIMEOUT_SECONDS

    @staticmethod
    def _as_str_list(value: Any, field_name: str) -> list[str]:
        if value is None:
            return []
        if isinstance(value, str):
            return [value]
        if isinstance(value, Iterable):
            return [str(item) for item in value]
        raise ValueError(f"'{field_name}' must be a string or a list of strings")

    @staticmethod
    def _as_positive_float(value: Any, field_name: str, default: float) -> float:
        if value is None:
            return default
        try:
            number = float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"'{field_name}' must be a number") from exc
        if number <= 0:
            raise ValueError(f"'{field_name}' must be greater than 0")
        return number

    @classmethod
    def from_dict(cls, payload: Any) -> "BridgeRequest":
        if not isinstance(payload, dict):
            raise ValueError("request must be a JSON object")

        repository_root = payload.get("repository_root") or payload.get("repo_root")
        if not repository_root or not str(repository_root).strip():
            raise ValueError("'repository_root' is required")
        task = payload.get("task") or payload.get("request") or payload.get("prompt")
        if not task or not str(task).strip():
            raise ValueError("'task' is required")

        agent = str(payload.get("agent") or DEFAULT_AGENT)
        engine = str(payload.get("engine") or DEFAULT_ENGINE)
        if engine not in SUPPORTED_ENGINES:
            # Legacy callers may still pass engine="v2". It is refused, never run.
            raise UnsupportedEngineError(
                f"Kiro engine '{engine}' is not supported; this bridge is V3-only "
                f"(supported: {', '.join(SUPPORTED_ENGINES)})"
            )
        command = cls._as_str_list(payload.get("command"), "command")
        if not command:
            command = list(DEFAULT_COMMAND)

        permission_mode = str(payload.get("permission_mode") or PERMISSION_ALLOW_ONCE)
        if permission_mode not in PERMISSION_MODES:
            raise ValueError(f"'permission_mode' must be one of {', '.join(PERMISSION_MODES)}")

        return cls(
            repository_root=str(repository_root),
            task=str(task),
            agent=agent,
            engine=engine,
            command=command,
            cwd=str(payload["cwd"]) if payload.get("cwd") else str(repository_root),
            allowed_scope=cls._as_str_list(payload.get("allowed_scope"), "allowed_scope"),
            acceptance_criteria=cls._as_str_list(
                payload.get("acceptance_criteria"), "acceptance_criteria"
            ),
            verification=cls._as_str_list(payload.get("verification"), "verification"),
            notes=str(payload["notes"]) if payload.get("notes") else None,
            session_id=str(payload["session_id"]) if payload.get("session_id") else None,
            timeout_seconds=cls._as_positive_float(
                payload.get("timeout_seconds"), "timeout_seconds", DEFAULT_TIMEOUT_SECONDS
            ),
            startup_timeout_seconds=cls._as_positive_float(
                payload.get("startup_timeout_seconds"),
                "startup_timeout_seconds",
                DEFAULT_STARTUP_TIMEOUT_SECONDS,
            ),
            cancel_grace_seconds=cls._as_positive_float(
                payload.get("cancel_grace_seconds"),
                "cancel_grace_seconds",
                DEFAULT_CANCEL_GRACE_SECONDS,
            ),
            permission_mode=permission_mode,
            raw_prompt=bool(payload.get("raw_prompt", False)),
            require_agent_scope=bool(payload.get("require_agent_scope", True)),
            allow_dependency_changes=bool(payload.get("allow_dependency_changes", False)),
            agent_select_timeout_seconds=cls._as_positive_float(
                payload.get("agent_select_timeout_seconds"),
                "agent_select_timeout_seconds",
                DEFAULT_AGENT_SELECT_TIMEOUT_SECONDS,
            ),
        )

    def prompt_text(self) -> str:
        """Render the engineering task packet (see ``prompts/kiro-engineer.md``)."""
        if self.raw_prompt:
            return self.task

        def bullets(items: Sequence[str], fallback: str) -> str:
            if not items:
                return fallback
            return "\n".join(f"- {item}" for item in items)

        sections = [
            "你是 AGY 主控 PPT workflow 的工程 Worker。",
            f"Repository/project root:\n{self.repository_root}",
            f"工程任務：\n{self.task}",
            "允許修改範圍：\n"
            + bullets(self.allowed_scope, "- minimal required scope only"),
            "Acceptance criteria:\n"
            + bullets(self.acceptance_criteria, "- AGY 未指定，請以任務描述為準"),
            "Verification：\n"
            + bullets(
                self.verification,
                "- 執行相關 tests/checks\n- 誠實回報失敗\n- 變更保持最小且可維護",
            ),
        ]
        if self.notes:
            sections.append(f"補充context：\n{self.notes}")
        sections.append(
            "角色邊界：\n"
            "- 你只擁有 engineering implementation。\n"
            "- 不得改簡報文案、大綱、頁數、已核准視覺方向。\n"
            "- 不得生成或編修簡報圖片。\n"
            "- 不得自行呼叫 Codex / $imagegen。\n"
            "- 不得決定下一個簡報 workflow phase。\n"
            "- 完成後把控制權交回 AGY。"
        )
        sections.append(
            "回傳：\n1. 修改檔案\n2. 實作摘要\n3. 執行的 tests/checks 與結果\n4. 尚未解決的 blocker（如有）"
        )
        return "\n\n".join(sections)

    def auth_owner(self) -> str | None:
        """Who resolves access tokens, from `--auth-method` (never a key)."""
        if "--auth-method" in self.command:
            index = self.command.index("--auth-method") + 1
            if index < len(self.command):
                return self.command[index]
        return None

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": REQUEST_SCHEMA,
            "repository_root": self.repository_root,
            "task": self.task,
            "agent": self.agent,
            "engine": self.engine,
            "command": list(self.command),
            "cwd": self.cwd,
            "allowed_scope": list(self.allowed_scope),
            "acceptance_criteria": list(self.acceptance_criteria),
            "verification": list(self.verification),
            "notes": self.notes,
            "session_id": self.session_id,
            "timeout_seconds": self.timeout_seconds,
            "startup_timeout_seconds": self.startup_timeout_seconds,
            "cancel_grace_seconds": self.cancel_grace_seconds,
            "permission_mode": self.permission_mode,
            "raw_prompt": self.raw_prompt,
            "require_agent_scope": self.require_agent_scope,
            "allow_dependency_changes": self.allow_dependency_changes,
            "agent_select_timeout_seconds": self.agent_select_timeout_seconds,
        }


@dataclass
class BridgeResult:
    """Structured engineering result returned to AGY."""

    status: str
    agent: str = DEFAULT_AGENT
    error_code: str | None = None
    error_message: str | None = None
    session_id: str | None = None
    stop_reason: str | None = None
    agent_text: str = ""
    thought_text: str = ""
    messages: list[dict[str, Any]] = field(default_factory=list)
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    permission_decisions: list[dict[str, Any]] = field(default_factory=list)
    policy_violations: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    plans: list[dict[str, Any]] = field(default_factory=list)
    timeline: list[dict[str, Any]] = field(default_factory=list)
    diagnostics: dict[str, Any] = field(default_factory=dict)
    started_at: str | None = None
    ended_at: str | None = None
    duration_seconds: float | None = None

    @property
    def ok(self) -> bool:
        return self.status == STATUS_COMPLETED

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": RESULT_SCHEMA,
            "kind": "engineering_result",
            "status": self.status,
            "error_code": self.error_code,
            "error_message": self.error_message,
            "control": "returned_to_agy",
            "next_step_owner": "AGY",
            "agent": self.agent,
            "session_id": self.session_id,
            "stop_reason": self.stop_reason,
            "agent_text": self.agent_text,
            "thought_text": self.thought_text,
            "messages": self.messages,
            "tool_calls": self.tool_calls,
            "permission_decisions": self.permission_decisions,
            "policy_violations": self.policy_violations,
            "warnings": self.warnings,
            "plans": self.plans,
            "timeline": self.timeline,
            "diagnostics": self.diagnostics,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "duration_seconds": self.duration_seconds,
        }


TransportFactory = Callable[[BridgeRequest], StdioProcessTransport]


def default_transport_factory(request: BridgeRequest) -> StdioProcessTransport:
    env, removed = sanitize_env()
    transport = StdioProcessTransport(request.command, cwd=request.cwd, env=env)
    transport.removed_env_vars = removed  # type: ignore[attr-defined]
    return transport


class KiroAcpBridge:
    """One-shot ACP client: initialize -> session/new -> session/prompt -> result."""

    def __init__(
        self,
        request: BridgeRequest,
        transport: StdioProcessTransport | None = None,
        transport_factory: TransportFactory = default_transport_factory,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self.request = request
        self._transport = transport
        self._transport_factory = transport_factory
        self._clock = clock

        self._next_id = 0
        self._session_id: str | None = request.session_id
        self._cancel_event = threading.Event()
        self._cancel_sent = False
        self._turn_ended = False
        self._timed_out = False

        self._text_chunks: list[str] = []
        self._thought_chunks: list[str] = []
        self._chunk_counts: dict[str, int] = {}
        self._messages: list[dict[str, Any]] = []
        self._tool_calls: list[dict[str, Any]] = []
        self._tool_call_index: dict[str, dict[str, Any]] = {}
        self._permission_decisions: list[dict[str, Any]] = []
        self._policy_violations: list[dict[str, Any]] = []
        self._plans: list[dict[str, Any]] = []
        self._timeline: list[dict[str, Any]] = []
        self._always_allowed = request.permission_mode == PERMISSION_ALLOW_ALWAYS
        self._agent_capabilities: dict[str, Any] = {}
        self._protocol_version: Any = None

        # Agent (mode) selection state.
        self._available_modes: list[dict[str, Any]] = []
        self._current_mode: str | None = None
        self._current_mode_source: str | None = None
        self._selection_method: str | None = None
        self._selection_attempted = False
        self._tool_tags: list[str] = []

        # Mid-turn agent scope invariant.
        self._turn_active = False
        self._scope_lost = False
        self._scope_loss: dict[str, Any] | None = None

        self._policy = PermissionPolicy(
            request.repository_root,
            allow_dependency_changes=request.allow_dependency_changes,
        )

    # -- public API --------------------------------------------------------
    def cancel(self) -> None:
        """Request cancellation of the running turn (thread/signal safe)."""
        self._cancel_event.set()

    def run(self) -> BridgeResult:
        started_wall = now_iso()
        started = self._clock()
        deadline = started + self.request.timeout_seconds
        transport = self._transport

        try:
            if transport is None:
                transport = self._transport_factory(self.request)
                self._transport = transport
            transport.start()
        except TransportStartError as exc:
            return self._finish(
                STATUS_UNAVAILABLE,
                started_wall,
                started,
                error_code=ERROR_WORKER_UNAVAILABLE,
                error_message=str(exc),
            )
        except Exception as exc:  # noqa: BLE001 - any startup failure is "unavailable"
            return self._finish(
                STATUS_UNAVAILABLE,
                started_wall,
                started,
                error_code=ERROR_WORKER_UNAVAILABLE,
                error_message=f"failed to start worker: {exc}",
            )

        try:
            startup_deadline = min(deadline, started + self.request.startup_timeout_seconds)
            try:
                self._initialize(startup_deadline)
                if self._session_id is None:
                    self._new_session(startup_deadline)
            except (TransportError, ProtocolError, TimeoutError) as exc:
                return self._finish(
                    STATUS_UNAVAILABLE,
                    started_wall,
                    started,
                    error_code=ERROR_WORKER_UNAVAILABLE,
                    error_message=str(exc),
                )

            # Bind the session to the engineering agent BEFORE any coding task is
            # dispatched. Never fall through to the engine default agent.
            if self.request.require_agent_scope:
                selection_deadline = min(
                    deadline, self._clock() + self.request.agent_select_timeout_seconds
                )
                try:
                    ok, detail = self._ensure_agent_scope(selection_deadline)
                except (TransportError, ProtocolError, TimeoutError) as exc:
                    ok, detail = False, str(exc)
                if not ok:
                    return self._finish(
                        STATUS_AGENT_UNAVAILABLE,
                        started_wall,
                        started,
                        error_code=ERROR_AGENT_UNAVAILABLE,
                        error_message=detail,
                    )

            try:
                stop_reason = self._prompt(deadline)
            except TimeoutError as exc:
                return self._finish(
                    STATUS_TIMEOUT,
                    started_wall,
                    started,
                    error_code=ERROR_WORKER_TIMEOUT,
                    error_message=str(exc),
                )
            except (TransportError, ProtocolError) as exc:
                return self._finish(
                    STATUS_FAILED,
                    started_wall,
                    started,
                    error_code=ERROR_WORKER_PROTOCOL,
                    error_message=str(exc),
                )

            status, error_code, error_message = self._classify(stop_reason)
            return self._finish(
                status,
                started_wall,
                started,
                error_code=error_code,
                error_message=error_message,
                stop_reason=stop_reason,
            )
        finally:
            if self._transport is not None:
                self._transport.close()

    # -- protocol steps ----------------------------------------------------
    def _initialize(self, deadline: float) -> None:
        result = self._call(
            "initialize",
            {
                "protocolVersion": ACP_PROTOCOL_VERSION,
                "clientCapabilities": {
                    # The bridge intentionally exposes no filesystem or terminal
                    # capability: Kiro uses its own sandboxed tools instead.
                    "fs": {"readTextFile": False, "writeTextFile": False},
                    "terminal": False,
                },
                "clientInfo": {"name": "agy-ppt-kiro-acp-bridge", "version": "1"},
            },
            deadline,
        )
        self._protocol_version = result.get("protocolVersion")
        capabilities = result.get("agentCapabilities")
        self._agent_capabilities = capabilities if isinstance(capabilities, dict) else {}
        self._record("initialized", {"protocol_version": self._protocol_version})

    def _new_session(self, deadline: float) -> None:
        result = self._call(
            "session/new",
            {"cwd": self.request.cwd or self.request.repository_root, "mcpServers": []},
            deadline,
        )
        session_id = result.get("sessionId") or result.get("session_id")
        if not session_id:
            raise ProtocolError("session/new returned no sessionId")
        self._session_id = str(session_id)
        self._absorb_modes(result, "session/new")
        self._record(
            "session_created",
            {
                "session_id": self._session_id,
                "current_mode": self._current_mode,
                "available_modes": self._available_mode_ids(),
            },
        )

    # -- agent scope -------------------------------------------------------
    def _absorb_modes(self, payload: dict[str, Any], source: str) -> None:
        """Read `modes` / `agentMode` information out of an ACP result."""
        modes = payload.get("modes")
        if isinstance(modes, dict):
            available = modes.get("availableModes")
            if isinstance(available, list):
                self._available_modes = [m for m in available if isinstance(m, dict)]
            current = modes.get("currentModeId") or modes.get("currentMode")
            if current:
                self._set_current_mode(str(current), source)
        meta = payload.get("_meta")
        if isinstance(meta, dict) and meta.get("agentMode") and self._current_mode is None:
            self._set_current_mode(str(meta["agentMode"]), f"{source}._meta.agentMode")

    def _set_current_mode(self, mode_id: str, source: str) -> None:
        previous = self._current_mode
        self._current_mode = mode_id
        self._current_mode_source = source
        # Mid-turn invariant: once the engineering turn is running, the active
        # agent must stay ppt-engineer for the whole turn.
        if self._turn_active and not self._scope_lost and mode_id != self.request.agent:
            self._on_scope_lost(observed=mode_id, previous=previous, source=source)

    def _on_scope_lost(self, observed: str, previous: str | None, source: str) -> None:
        """Handle active-agent drift during the engineering turn.

        The turn is abandoned: no further permission request is approved, the
        turn is cancelled, and AGY gets ENGINEERING_AGENT_SCOPE_LOST. The bridge
        never switches the mode back and never restarts the task.
        """
        self._scope_lost = True
        self._scope_loss = {
            "agent_scope_lost": True,
            "expected_agent": self.request.agent,
            "observed_agent": observed,
            "previous_agent": previous,
            "scope_loss_phase": "during_turn",
            "observed_via": source,
            "detected_at": now_iso(),
        }
        self._record("agent_scope_lost", dict(self._scope_loss))
        self._send_cancel("agent_scope_lost")

    def _available_mode_ids(self) -> list[str]:
        return [str(m.get("id")) for m in self._available_modes if m.get("id")]

    def _mode_entry(self, mode_id: str) -> dict[str, Any] | None:
        for mode in self._available_modes:
            if str(mode.get("id")) == mode_id:
                return mode
        return None

    def _ensure_agent_scope(self, deadline: float) -> tuple[bool, str | None]:
        """Guarantee the session runs as the requested engineering agent.

        Returns ``(ok, detail)``. When ``ok`` is False the caller must not send
        any engineering prompt.
        """
        agent = self.request.agent
        self._selection_method = SELECTION_SET_MODE

        available = self._available_mode_ids()
        if available and agent not in available:
            return False, (
                f"agent '{agent}' is not offered by this ACP session; "
                f"available agents: {', '.join(available) or '(none)'}"
            )

        if self._current_mode != agent:
            self._selection_attempted = True
            result = self._call(
                "session/set_mode", {"sessionId": self._session_id, "modeId": agent}, deadline
            )
            self._absorb_modes(result, "session/set_mode")
            # An unknown modeId also returns an empty result, so the response is
            # never treated as proof. Confirmation only comes from the engine
            # reporting the new active mode.
            if self._current_mode != agent:
                self._pump_quiet(deadline)

        if self._current_mode != agent:
            return False, (
                f"session/set_mode did not confirm '{agent}' as the active agent "
                f"(current={self._current_mode!r}); refusing to dispatch engineering "
                "work to the engine default agent."
            )

        self._record(
            "agent_scoped",
            {
                "agent": agent,
                "method": SELECTION_SET_MODE,
                "confirmed_via": self._current_mode_source,
                "agent_origin": self._agent_origin(),
            },
        )
        return True, None

    def _agent_origin(self) -> dict[str, Any] | None:
        """Diagnostics about where the selected agent config came from."""
        entry = self._mode_entry(self.request.agent)
        if entry is None:
            return None
        kiro = ((entry.get("_meta") or {}).get("kiro")) or {}
        resource = kiro.get("resource") if isinstance(kiro.get("resource"), dict) else {}
        source = resource.get("source") if isinstance(resource.get("source"), dict) else {}
        return {
            "resource_type": resource.get("resourceType"),
            "source": kiro.get("source"),
            "origin": source.get("origin"),
            "root": source.get("root"),
        }

    def _dispatch_inbound(self, message: dict[str, Any]) -> None:
        if "method" in message and "id" in message:
            self._handle_incoming_request(message)
        elif "method" in message:
            self._handle_notification(message)
        else:
            self._record("unmatched_response", {"id": message.get("id")})

    def _pump_quiet(self, deadline: float) -> None:
        """Drain notifications until the deadline or until the mode is confirmed."""
        assert self._transport is not None
        transport = self._transport
        while self._clock() < deadline:
            if self._current_mode == self.request.agent:
                return
            message = transport.receive(0.2)
            if message is None:
                if transport.at_eof():
                    return
                continue
            self._dispatch_inbound(message)

    def _prompt(self, deadline: float) -> str | None:
        params = {
            "sessionId": self._session_id,
            "prompt": [{"type": "text", "text": self.request.prompt_text()}],
        }
        self._record("prompt_sent", {"session_id": self._session_id})
        self._turn_active = True
        try:
            result = self._call("session/prompt", params, deadline, is_turn=True)
        finally:
            self._turn_active = False
        stop_reason = result.get("stopReason") or result.get("stop_reason")
        self._turn_ended = True
        self._record("turn_end", {"stop_reason": stop_reason})
        return str(stop_reason) if stop_reason is not None else None

    def _classify(self, stop_reason: str | None) -> tuple[str, str | None, str | None]:
        if self._scope_lost:
            loss = self._scope_loss or {}
            return (
                STATUS_AGENT_SCOPE_LOST,
                ERROR_AGENT_SCOPE_LOST,
                (
                    f"active agent drifted from '{loss.get('expected_agent')}' to "
                    f"'{loss.get('observed_agent')}' during the turn; the turn was "
                    "cancelled and no result is trusted."
                ),
            )
        if self._timed_out:
            return STATUS_TIMEOUT, ERROR_WORKER_TIMEOUT, "worker turn exceeded timeout_seconds"
        normalized = (stop_reason or "").strip().lower().replace("-", "_")
        if normalized in {"end_turn", "endturn", "", "stop", "completed"}:
            return STATUS_COMPLETED, None, None
        if normalized in {"cancelled", "canceled"}:
            return (
                STATUS_CANCELLED,
                ERROR_WORKER_CANCELLED,
                "worker turn was cancelled before completion",
            )
        if normalized == "refusal":
            return STATUS_FAILED, ERROR_WORKER_TURN_FAILED, "worker refused the engineering task"
        return (
            STATUS_INCOMPLETE,
            ERROR_WORKER_TURN_FAILED,
            f"worker stopped early: stop_reason={stop_reason}",
        )

    # -- JSON-RPC plumbing -------------------------------------------------
    def _allocate_id(self) -> int:
        self._next_id += 1
        return self._next_id

    def _send(self, message: dict[str, Any]) -> None:
        assert self._transport is not None
        self._transport.send(message)

    def _notify(self, method: str, params: dict[str, Any]) -> None:
        self._send({"jsonrpc": "2.0", "method": method, "params": params})

    def _call(
        self,
        method: str,
        params: dict[str, Any],
        deadline: float,
        is_turn: bool = False,
    ) -> dict[str, Any]:
        request_id = self._allocate_id()
        self._send({"jsonrpc": "2.0", "id": request_id, "method": method, "params": params})
        return self._await_response(request_id, method, deadline, is_turn=is_turn)

    def _await_response(
        self,
        request_id: int,
        method: str,
        deadline: float,
        is_turn: bool = False,
    ) -> dict[str, Any]:
        assert self._transport is not None
        transport = self._transport
        grace_deadline: float | None = None

        while True:
            if self._cancel_event.is_set() and not self._cancel_sent and is_turn:
                self._send_cancel("client_cancel")
            # A cancel sent for any reason (client, timeout, agent scope loss)
            # starts the shared grace period for the worker's final response.
            if is_turn and self._cancel_sent and grace_deadline is None:
                grace_deadline = self._clock() + self.request.cancel_grace_seconds

            effective_deadline = deadline if grace_deadline is None else grace_deadline
            remaining = effective_deadline - self._clock()
            if remaining <= 0:
                if is_turn and not self._cancel_sent:
                    self._timed_out = True
                    self._send_cancel("timeout")
                    continue
                if self._scope_lost:
                    # The turn is already void; do not mask it with a timeout.
                    return {}
                if self._timed_out:
                    raise TimeoutError(f"{method} timed out after cancel grace period")
                raise TimeoutError(f"{method} timed out")

            message = transport.receive(min(remaining, 0.5))
            if message is None:
                if transport.at_eof():
                    if self._scope_lost:
                        return {}
                    raise TransportError(self._eof_message(method))
                continue

            if "method" in message and "id" in message:
                self._handle_incoming_request(message)
                continue
            if "method" in message:
                self._handle_notification(message)
                continue
            if message.get("id") != request_id:
                # Response to a request we no longer track; keep it for audit.
                self._record("unmatched_response", {"id": message.get("id")})
                continue

            if "error" in message:
                error = message.get("error") or {}
                raise ProtocolError(
                    f"{method} failed: {redact(str(error.get('message', error)))} "
                    f"(code={error.get('code')})"
                )
            result = message.get("result")
            return result if isinstance(result, dict) else {}

    def _eof_message(self, method: str) -> str:
        assert self._transport is not None
        transport = self._transport
        details = []
        exit_code = transport.exit_code()
        if exit_code is not None:
            details.append(f"exit_code={exit_code}")
        stderr_tail = transport.stderr_tail()
        if stderr_tail:
            details.append("stderr=" + " | ".join(stderr_tail[-5:]))
        suffix = f" ({'; '.join(details)})" if details else ""
        return f"worker closed the ACP stream during {method}{suffix}"

    def _send_cancel(self, reason: str) -> None:
        if self._cancel_sent or self._session_id is None:
            self._cancel_sent = True
            return
        self._cancel_sent = True
        try:
            self._notify("session/cancel", {"sessionId": self._session_id})
            self._record("cancel_sent", {"reason": reason})
        except TransportError as exc:
            self._record("cancel_failed", {"reason": reason, "error": str(exc)})

    # -- inbound handling --------------------------------------------------
    def _handle_notification(self, message: dict[str, Any]) -> None:
        method = message.get("method")
        params = message.get("params") if isinstance(message.get("params"), dict) else {}
        if method == "session/update":
            update = params.get("update")
            if isinstance(update, dict):
                self._handle_session_update(update)
            return
        if method == KIRO_POLICY_CHANGED:
            self._record("policy_changed", {"status": params.get("status")})
            return
        if method == KIRO_TOOLS_DID_CHANGE:
            tags = params.get("tags")
            if isinstance(tags, list):
                self._tool_tags = [
                    str(tag.get("tag")) for tag in tags if isinstance(tag, dict) and tag.get("tag")
                ]
            self._record("tools_changed", {"tags": self._tool_tags})
            return
        self._record("notification", {"method": method})

    def _handle_incoming_request(self, message: dict[str, Any]) -> None:
        method = message.get("method")
        request_id = message.get("id")
        params = message.get("params") if isinstance(message.get("params"), dict) else {}

        if method == "session/request_permission":
            self._respond(request_id, self._decide_permission(params))
            return
        if method in {"fs/read_text_file", "fs/write_text_file"}:
            # We advertised no fs capability; refuse instead of touching disk.
            self._respond_error(
                request_id,
                -32601,
                f"{method} is not supported by the AGY bridge (no fs capability advertised)",
            )
            return
        self._respond_error(request_id, -32601, f"method not supported: {method}")

    def _respond(self, request_id: Any, result: dict[str, Any]) -> None:
        try:
            self._send({"jsonrpc": "2.0", "id": request_id, "result": result})
        except TransportError as exc:  # pragma: no cover - defensive
            self._record("response_failed", {"id": request_id, "error": str(exc)})

    def _respond_error(self, request_id: Any, code: int, message: str) -> None:
        try:
            self._send(
                {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}
            )
        except TransportError as exc:  # pragma: no cover - defensive
            self._record("response_failed", {"id": request_id, "error": str(exc)})

    def _decide_permission(self, params: dict[str, Any]) -> dict[str, Any]:
        view = ConsentView.from_permission_request(params, self._correlate_tool_call(params))

        if self._scope_lost:
            # The turn is void: nothing else gets approved.
            return self._permission_outcome(
                params,
                view,
                PolicyDecision(
                    False,
                    "agent_scope_lost",
                    f"active agent is no longer '{self.request.agent}'; the turn is cancelled",
                ),
            )

        if self.request.permission_mode == PERMISSION_REJECT:
            return self._permission_outcome(
                params, view, PolicyDecision(False, "permission_mode", "permission_mode=reject")
            )

        decision = self._policy.evaluate(view)
        return self._permission_outcome(params, view, decision)

    def _correlate_tool_call(self, params: dict[str, Any]) -> dict[str, Any] | None:
        """Find the streamed tool_call that this permission request belongs to.

        Kiro prefixes some permission toolCallIds (``run_command_toolu_...`` for
        the tool call ``toolu_...``), so an exact match is tried first and a
        suffix match second.
        """
        tool_call = params.get("toolCall") if isinstance(params.get("toolCall"), dict) else {}
        call_id = tool_call.get("toolCallId") or tool_call.get("tool_call_id")
        if not call_id:
            return None
        call_id = str(call_id)
        exact = self._tool_call_index.get(call_id)
        if exact is not None:
            return exact
        for known_id, record in self._tool_call_index.items():
            if call_id.endswith(known_id) or known_id.endswith(call_id):
                return record
        return None

    def _permission_outcome(
        self,
        params: dict[str, Any],
        view: ConsentView,
        decision: PolicyDecision,
    ) -> dict[str, Any]:
        options = params.get("options") if isinstance(params.get("options"), list) else []
        outcome = "allowed" if decision.allowed else "denied"
        option_id, option_kind = self._pick_option(options, outcome, self._always_allowed)
        tool_call = params.get("toolCall") if isinstance(params.get("toolCall"), dict) else {}
        record = {
            "tool_call_id": tool_call.get("toolCallId") or tool_call.get("tool_call_id"),
            "decision": outcome,
            "rule": decision.rule,
            "reason": decision.reason,
            "capability": view.capability or view.kind or None,
            "target": redact(view.command or view.path or view.resource or view.title) or None,
            "option_id": option_id,
            "option_kind": option_kind,
            "decided_at": now_iso(),
        }
        self._permission_decisions.append(record)
        self._record("permission_decision", record)

        # Operator-chosen blanket rejection is not a policy breach; anything the
        # policy itself refused is recorded for AGY.
        if not decision.allowed and decision.rule != "permission_mode":
            self._policy_violations.append(
                {
                    "rule": decision.rule,
                    "reason": decision.reason,
                    "tool_call_id": record["tool_call_id"],
                    "capability": record["capability"],
                    "target": record["target"],
                    "detected_at": now_iso(),
                }
            )

        if option_id is not None:
            return {"outcome": {"outcome": "selected", "optionId": option_id}}
        # No usable option offered; cancel the permission prompt.
        return {"outcome": {"outcome": "cancelled"}}

    @staticmethod
    def _pick_option(
        options: list[Any],
        decision: str,
        prefer_always: bool = False,
    ) -> tuple[str | None, str | None]:
        if decision == "allowed":
            wanted = (
                ("allow_always", "allow_once", "allow")
                if prefer_always
                # allow_always would outlive this turn, so it is only a last resort.
                else ("allow_once", "allow", "allow_always")
            )
        else:
            wanted = ("reject_once", "reject_always", "reject", "deny")

        normalized: list[tuple[str, str]] = []
        for option in options:
            if not isinstance(option, dict):
                continue
            option_id = option.get("optionId") or option.get("id")
            if not option_id:
                continue
            kind = str(option.get("kind") or option.get("name") or "").lower().replace("-", "_")
            normalized.append((kind, str(option_id)))
        for wanted_kind in wanted:
            for kind, option_id in normalized:
                if kind == wanted_kind:
                    return option_id, kind
        for wanted_kind in wanted:
            for kind, option_id in normalized:
                if wanted_kind in kind:
                    return option_id, kind
        return None, None

    def _handle_session_update(self, update: dict[str, Any]) -> None:
        kind = self._normalize_kind(
            update.get("sessionUpdate") or update.get("type") or update.get("kind")
        )
        if kind == "agent_message_chunk":
            text = self._extract_text(update.get("content"))
            if text:
                self._text_chunks.append(text)
                self._append_message("assistant", text)
            return
        if kind == "agent_thought_chunk":
            text = self._extract_text(update.get("content"))
            if text:
                self._thought_chunks.append(text)
            return
        if kind == "user_message_chunk":
            text = self._extract_text(update.get("content"))
            if text:
                self._append_message("user", text)
            return
        if kind == "tool_call":
            self._on_tool_call(update)
            return
        if kind == "tool_call_update":
            self._on_tool_call_update(update)
            return
        if kind == "plan":
            plan = {"entries": update.get("entries"), "recorded_at": now_iso()}
            self._plans.append(plan)
            self._record("plan", {"entry_count": len(update.get("entries") or [])})
            return
        if kind in {"current_mode_update", "mode_updated"}:
            mode = (
                update.get("currentModeId")
                or update.get("modeId")
                or update.get("currentMode")
                or update.get("mode")
            )
            if mode:
                self._set_current_mode(str(mode), "current_mode_update")
                self._record("current_mode_update", {"current_mode": self._current_mode})
            return
        if kind == "config_option_update":
            self._absorb_config_options(update.get("configOptions"))
            return
        if kind in {"turn_end", "turn_ended", "end_turn"}:
            self._turn_ended = True
            self._record("turn_end_update", {"stop_reason": update.get("stopReason")})
            return
        self._record("session_update", {"kind": kind})

    def _append_message(self, role: str, text: str) -> None:
        """Coalesce streamed chunks into one message per contiguous role run."""
        self._chunk_counts[role] = self._chunk_counts.get(role, 0) + 1
        redacted = redact(text)
        if self._messages and self._messages[-1]["role"] == role:
            self._messages[-1]["text"] += redacted
            return
        self._messages.append({"role": role, "text": redacted})

    def _absorb_config_options(self, options: Any) -> None:
        """Track the session's active agent from the `mode` config option.

        Kiro v3 confirms `session/set_mode` by re-publishing the mode select with
        the new `currentValue`; this is the only trustworthy confirmation, because
        `session/set_mode` returns an empty result even for an unknown modeId.
        """
        if not isinstance(options, list):
            return
        for option in options:
            if not isinstance(option, dict):
                continue
            if option.get("id") != MODE_OPTION_ID and option.get("category") != MODE_OPTION_ID:
                continue
            choices = option.get("options")
            if isinstance(choices, list):
                modes = [
                    {
                        "id": choice.get("value") or choice.get("id"),
                        "name": choice.get("name"),
                        "description": choice.get("description"),
                        "_meta": choice.get("_meta"),
                    }
                    for choice in choices
                    if isinstance(choice, dict) and (choice.get("value") or choice.get("id"))
                ]
                if modes:
                    self._available_modes = modes
            current = option.get("currentValue")
            if current:
                previous = self._current_mode
                self._set_current_mode(str(current), "config_option_update")
                if previous != self._current_mode:
                    self._record("current_mode_update", {"current_mode": self._current_mode})

    @staticmethod
    def _normalize_kind(value: Any) -> str:
        if not isinstance(value, str):
            return ""
        # AgentMessageChunk / agentMessageChunk / agent_message_chunk -> agent_message_chunk
        snake = re.sub(r"(?<!^)(?=[A-Z])", "_", value.strip()).lower()
        return snake.replace("-", "_").replace("__", "_")

    @classmethod
    def _extract_text(cls, content: Any) -> str:
        if content is None:
            return ""
        if isinstance(content, str):
            return content
        if isinstance(content, dict):
            if isinstance(content.get("text"), str):
                return content["text"]
            if "content" in content:
                return cls._extract_text(content["content"])
            return ""
        if isinstance(content, list):
            return "".join(cls._extract_text(item) for item in content)
        return ""

    def _tool_call_id(self, payload: dict[str, Any]) -> str:
        return str(
            payload.get("toolCallId")
            or payload.get("tool_call_id")
            or payload.get("id")
            or f"anonymous_{len(self._tool_calls) + 1}"
        )

    def _on_tool_call(self, payload: dict[str, Any]) -> None:
        call_id = self._tool_call_id(payload)
        raw_input = payload.get("rawInput") or payload.get("raw_input")
        record = {
            "tool_call_id": call_id,
            "title": redact(str(payload["title"])) if payload.get("title") else None,
            "kind": payload.get("kind"),
            "status": payload.get("status") or "pending",
            "raw_input": raw_input,
            "locations": payload.get("locations"),
            "content": payload.get("content"),
            "updates": [],
            "started_at": now_iso(),
        }
        if looks_like_codex_invocation(payload.get("title"), raw_input, payload.get("kind")):
            record["policy_flag"] = "kiro_must_not_call_codex"
            self._policy_violations.append(
                {
                    "rule": "kiro_must_not_call_codex",
                    "tool_call_id": call_id,
                    "title": record["title"],
                    "detected_at": now_iso(),
                }
            )
        self._tool_calls.append(record)
        self._tool_call_index[call_id] = record
        self._record("tool_call", {"tool_call_id": call_id, "status": record["status"]})

    def _on_tool_call_update(self, payload: dict[str, Any]) -> None:
        call_id = self._tool_call_id(payload)
        record = self._tool_call_index.get(call_id)
        if record is None:
            self._on_tool_call(payload)
            record = self._tool_call_index[call_id]
        update = {
            key: payload[key]
            for key in ("status", "title", "kind", "content", "locations", "rawOutput", "rawInput")
            if key in payload
        }
        if payload.get("status"):
            record["status"] = payload["status"]
        if payload.get("title"):
            record["title"] = redact(str(payload["title"]))
        if payload.get("content") is not None:
            record["content"] = payload["content"]
        if payload.get("rawOutput") is not None:
            record["raw_output"] = payload["rawOutput"]
        update["updated_at"] = now_iso()
        record["updates"].append(update)
        record["updated_at"] = update["updated_at"]
        self._record("tool_call_update", {"tool_call_id": call_id, "status": record["status"]})

    # -- result assembly ---------------------------------------------------
    def _record(self, event: str, detail: dict[str, Any] | None = None) -> None:
        entry: dict[str, Any] = {"event": event, "at": now_iso()}
        if detail:
            entry.update(detail)
        self._timeline.append(entry)

    def _finish(
        self,
        status: str,
        started_wall: str,
        started: float,
        error_code: str | None = None,
        error_message: str | None = None,
        stop_reason: str | None = None,
    ) -> BridgeResult:
        transport = self._transport
        agent = self.request.agent
        resolved = self._current_mode == agent and not self._scope_lost
        scoped = resolved and self._selection_method is not None
        prompt_sent = any(entry["event"] == "prompt_sent" for entry in self._timeline)

        warnings: list[str] = []
        if self._scope_lost:
            loss = self._scope_loss or {}
            warnings.append(
                f"agent scope lost during the turn: expected '{loss.get('expected_agent')}', "
                f"observed '{loss.get('observed_agent')}'. The turn was cancelled and its "
                "output must not be trusted."
            )
        elif not resolved and prompt_sent is False and self.request.require_agent_scope:
            warnings.append(
                f"session/set_mode did not confirm '{agent}' as the active agent "
                f"(current={self._current_mode!r}); engineering work was NOT dispatched."
            )
        if not self.request.require_agent_scope and not scoped:
            warnings.append(
                "require_agent_scope=false: the engineering task may have run under "
                f"the engine default agent instead of '{agent}'."
            )
        if self.request.allow_dependency_changes:
            warnings.append(
                "allow_dependency_changes=true: dependency-changing commands passed the "
                "policy gate for this run."
            )

        diagnostics: dict[str, Any] = {
            "command": list(self.request.command),
            "engine": self.request.engine,
            "auth": self.request.auth_owner(),
            "agent_requested": agent,
            "agent_resolved": resolved,
            "agent_scoped": scoped,
            "agent_scope_lost": self._scope_lost,
            "agent_selection": {
                "required": self.request.require_agent_scope,
                "method": self._selection_method,
                "attempted": self._selection_attempted,
                "available_agents": self._available_mode_ids(),
                "current_agent": self._current_mode,
                "confirmed_via": self._current_mode_source,
                "agent_origin": self._agent_origin(),
            },
            "prompt_dispatched": prompt_sent,
            "engine_fallback_used": False,
            "tool_tags": list(self._tool_tags),
            "permission_policy": self._policy.describe(),
            "cwd": self.request.cwd,
            "protocol_version": self._protocol_version,
            "agent_capabilities": self._agent_capabilities,
            "permission_mode": self.request.permission_mode,
            "turn_end_observed": self._turn_ended,
            "stream_chunks": dict(self._chunk_counts),
            "thought_chunks": len(self._thought_chunks),
            "cancel_sent": self._cancel_sent,
            "timed_out": self._timed_out,
            "oauth_only": True,
            "api_key_used": False,
            "removed_env_vars": list(getattr(transport, "removed_env_vars", [])),
        }
        if self._scope_loss is not None:
            diagnostics["agent_scope_loss"] = dict(self._scope_loss)
            diagnostics.update(
                {
                    "expected_agent": self._scope_loss.get("expected_agent"),
                    "observed_agent": self._scope_loss.get("observed_agent"),
                    "scope_loss_phase": self._scope_loss.get("scope_loss_phase"),
                }
            )
        if transport is not None:
            diagnostics["exit_code"] = transport.exit_code()
            stderr_tail = transport.stderr_tail()
            if stderr_tail:
                diagnostics["stderr_tail"] = stderr_tail
            noise = transport.noise_tail()
            if noise:
                diagnostics["non_jsonrpc_stdout"] = noise

        return BridgeResult(
            status=status,
            agent=self.request.agent,
            error_code=error_code,
            error_message=redact(error_message) if error_message else None,
            session_id=self._session_id,
            stop_reason=stop_reason,
            agent_text=redact("".join(self._text_chunks)),
            thought_text=redact("".join(self._thought_chunks)),
            messages=self._messages,
            tool_calls=self._tool_calls,
            permission_decisions=self._permission_decisions,
            policy_violations=self._policy_violations,
            warnings=warnings,
            plans=self._plans,
            timeline=self._timeline,
            diagnostics=diagnostics,
            started_at=started_wall,
            ended_at=now_iso(),
            duration_seconds=round(self._clock() - started, 3),
        )


def dispatch(payload: Any) -> BridgeResult:
    """Run one engineering job described by ``payload`` and return the result."""
    request = BridgeRequest.from_dict(payload)
    # Resolved at call time so the factory stays patchable for tests.
    bridge = KiroAcpBridge(request, transport_factory=default_transport_factory)
    _install_signal_handlers(bridge)
    return bridge.run()

def _install_signal_handlers(bridge: KiroAcpBridge) -> None:
    def handler(signum: int, _frame: Any) -> None:
        bridge.cancel()

    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            signal.signal(sig, handler)
        except (ValueError, OSError, AttributeError):  # not the main thread / unsupported
            pass


def _load_payload(path: str | None) -> Any:
    if path and path != "-":
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    data = sys.stdin.read()
    if not data.strip():
        raise ValueError("no request JSON received on stdin")
    return json.loads(data)


def _exit_code(status: str) -> int:
    return 0 if status == STATUS_COMPLETED else 1


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Dispatch an AGY engineering job to Kiro over ACP.")
    parser.add_argument("--input", help="Request JSON file. Defaults to stdin.")
    parser.add_argument("--output", help="Write the result JSON here instead of stdout.")
    parser.add_argument("--timeout", type=float, help="Override timeout_seconds.")
    parser.add_argument("--agent", help="Override the Kiro custom agent name.")
    parser.add_argument(
        "--allow-dependency-changes",
        action="store_true",
        help="Authorize dependency/lockfile changing commands for this run.",
    )
    parser.add_argument(
        "--allow-unscoped-agent",
        action="store_true",
        help="Dangerous: run the task even if the ppt-engineer agent is unconfirmed.",
    )
    parser.add_argument(
        "--permission-mode",
        choices=PERMISSION_MODES,
        help="Override how tool permission requests are answered.",
    )
    parser.add_argument("--compact", action="store_true", help="Emit single-line JSON.")
    args = parser.parse_args(argv)

    try:
        payload = _load_payload(args.input)
        if not isinstance(payload, dict):
            raise ValueError("request must be a JSON object")
        if args.timeout is not None:
            payload["timeout_seconds"] = args.timeout
        if args.agent:
            payload["agent"] = args.agent
        if args.allow_dependency_changes:
            payload["allow_dependency_changes"] = True
        if args.allow_unscoped_agent:
            payload["require_agent_scope"] = False
        if args.permission_mode:
            payload["permission_mode"] = args.permission_mode
        result = dispatch(payload)
    except UnsupportedEngineError as exc:
        result = BridgeResult(
            status=STATUS_FAILED,
            error_code=ERROR_UNSUPPORTED_ENGINE,
            error_message=str(exc),
            started_at=now_iso(),
            ended_at=now_iso(),
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        result = BridgeResult(
            status=STATUS_FAILED,
            error_code=ERROR_INVALID_REQUEST,
            error_message=str(exc),
            started_at=now_iso(),
            ended_at=now_iso(),
        )

    body = json.dumps(
        result.to_dict(),
        ensure_ascii=False,
        indent=None if args.compact else 2,
        default=str,
    )
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(body + "\n")
        print(f"{result.status} -> {args.output}")
    else:
        print(body)
    return _exit_code(result.status)


if __name__ == "__main__":
    raise SystemExit(main())
