from __future__ import annotations

import asyncio
import json
import os
import shlex
import subprocess
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ============================================================
# CLAW HARNESS CONFIG
# ============================================================

DEFAULT_TIMEOUT_SEC = int(os.getenv("CLAW_CODE_TIMEOUT_SEC", "120"))
DEFAULT_MAX_OUTPUT_CHARS = int(os.getenv("CLAW_CODE_MAX_OUTPUT_CHARS", "25000"))
DEFAULT_WORKSPACE = os.getenv(
    "CLAW_CODE_WORKSPACE",
    "./claw-code"
)
DEFAULT_PYTHON = os.getenv("CLAW_CODE_PYTHON", "python3")
DEFAULT_MODULE = os.getenv("CLAW_CODE_MODULE", "src.main")
DEFAULT_EVENT_LOG = os.getenv(
    "CLAW_CODE_EVENT_LOG",
    "./claw-code/telemetry/claw_harness_events.jsonl"
)

# Command definitions: (positional_arg_names, allowed_flags)
COMMAND_DEFS = {
    # Inspection commands
    "summary": ((), set()),
    "manifest": ((), set()),
    "parity-audit": ((), set()),
    "subsystems": ((), {"limit"}),
    "commands": ((), {"limit", "query", "no_plugin_commands", "no_skill_commands"}),
    "tools": ((), {"limit", "query", "simple_mode", "no_mcp", "deny_tool", "deny_prefix"}),
    
    # Discovery commands
    "show-command": (("name",), set()),
    "show-tool": (("name",), set()),
    
    # Routing & execution
    "route": (("prompt",), {"limit"}),
    "bootstrap": (("prompt",), {"limit"}),
    "turn-loop": (("prompt",), {"limit", "max_turns", "structured_output"}),
    
    # Direct execution (use with caution)
    "exec-command": (("name", "prompt"), set()),
    "exec-tool": (("name", "payload"), set()),
    
    # Session management
    "load-session": (("session_id",), set()),
    "flush-transcript": (("prompt",), set()),
    
    # Runtime modes (advanced)
    "remote-mode": (("target",), set()),
    "ssh-mode": (("target",), set()),
    "teleport-mode": (("target",), set()),
    "direct-connect-mode": (("target",), set()),
    "deep-link-mode": (("target",), set()),
}

ALLOWED_COMMANDS = set(COMMAND_DEFS.keys())


# ============================================================
# DATA STRUCTURES
# ============================================================

@dataclass
class HarnessResult:
    ok: bool
    run_id: str
    command: str
    args: Dict[str, Any]
    cwd: str
    started_at: float
    completed_at: float
    duration_ms: int
    returncode: int
    stdout: str
    stderr: str
    output: str
    truncated: bool
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ok": self.ok,
            "run_id": self.run_id,
            "command": self.command,
            "args": self.args,
            "cwd": self.cwd,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "duration_ms": self.duration_ms,
            "returncode": self.returncode,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "output": self.output,
            "truncated": self.truncated,
            "metadata": self.metadata,
        }


# ============================================================
# CLAW HARNESS CORE
# ============================================================

class ClawHarness:
    """
    Enhanced production-grade wrapper around the claw-code clean-room Python harness.
    Supports positional arguments and expanded command set.
    """

    def __init__(
        self,
        workspace: Optional[str] = None,
        python_bin: Optional[str] = None,
        module_name: Optional[str] = None,
        timeout_sec: Optional[int] = None,
        max_output_chars: Optional[int] = None,
        event_log_path: Optional[str] = None,
    ) -> None:
        self.workspace = Path(workspace or DEFAULT_WORKSPACE).expanduser().resolve()
        self.python_bin = python_bin or DEFAULT_PYTHON
        self.module_name = module_name or DEFAULT_MODULE
        self.timeout_sec = timeout_sec or DEFAULT_TIMEOUT_SEC
        self.max_output_chars = max_output_chars or DEFAULT_MAX_OUTPUT_CHARS
        self.event_log_path = Path(event_log_path or DEFAULT_EVENT_LOG)

    # --------------------------------------------------------
    # PUBLIC API
    # --------------------------------------------------------

    async def invoke(
        self,
        command: str,
        args: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Generic entrypoint for tool execution.
        """
        args = args or {}
        context = context or {}

        run_id = str(uuid.uuid4())
        started_at = time.time()

        self._validate_workspace()
        self._validate_command(command)
        positional_args, flag_args = self._sanitize_args(command, args)

        await self._log_event(
            event_type="claw_harness_started",
            payload={
                "run_id": run_id,
                "command": command,
                "args": args,
                "positional_args": positional_args,
                "flag_args": flag_args,
                "workspace": str(self.workspace),
                "context": context,
            },
        )

        try:
            result = await self._run_command(
                run_id=run_id,
                command=command,
                positional_args=positional_args,
                flag_args=flag_args,
                started_at=started_at,
                context=context,
            )

            await self._log_event(
                event_type="claw_harness_completed",
                payload=result.to_dict(),
            )

            return result.to_dict()

        except Exception as exc:
            completed_at = time.time()
            error_payload = {
                "ok": False,
                "run_id": run_id,
                "command": command,
                "args": args,
                "cwd": str(self.workspace),
                "started_at": started_at,
                "completed_at": completed_at,
                "duration_ms": int((completed_at - started_at) * 1000),
                "error": repr(exc),
                "error_type": type(exc).__name__,
                "metadata": {
                    "context": context,
                },
            }

            await self._log_event(
                event_type="claw_harness_failed",
                payload=error_payload,
            )

            return error_payload

    # --------------------------------------------------------
    # CONVENIENCE METHODS (optional)
    # --------------------------------------------------------

    async def summary(self) -> Dict[str, Any]:
        return await self.invoke("summary")

    async def manifest(self) -> Dict[str, Any]:
        return await self.invoke("manifest")

    async def subsystems(self, limit: int = 16) -> Dict[str, Any]:
        return await self.invoke("subsystems", {"limit": limit})

    async def commands(self, limit: int = 10, query: Optional[str] = None) -> Dict[str, Any]:
        args = {"limit": limit}
        if query:
            args["query"] = query
        return await self.invoke("commands", args)

    async def tools(self, limit: int = 10, query: Optional[str] = None) -> Dict[str, Any]:
        args = {"limit": limit}
        if query:
            args["query"] = query
        return await self.invoke("tools", args)

    async def parity_audit(self) -> Dict[str, Any]:
        return await self.invoke("parity-audit")

    async def route(self, prompt: str, limit: int = 5) -> Dict[str, Any]:
        return await self.invoke("route", {"prompt": prompt, "limit": limit})

    async def exec_tool(self, name: str, payload: str) -> Dict[str, Any]:
        return await self.invoke("exec-tool", {"name": name, "payload": payload})

    async def exec_command(self, name: str, prompt: str) -> Dict[str, Any]:
        return await self.invoke("exec-command", {"name": name, "prompt": prompt})

    async def show_tool(self, name: str) -> Dict[str, Any]:
        return await self.invoke("show-tool", {"name": name})

    async def show_command(self, name: str) -> Dict[str, Any]:
        return await self.invoke("show-command", {"name": name})

    # --------------------------------------------------------
    # INTERNALS
    # --------------------------------------------------------

    def _validate_workspace(self) -> None:
        if not self.workspace.exists():
            raise FileNotFoundError(
                f"CLAW_CODE_WORKSPACE does not exist: {self.workspace}"
            )
        if not self.workspace.is_dir():
            raise NotADirectoryError(
                f"CLAW_CODE_WORKSPACE is not a directory: {self.workspace}"
            )

    def _validate_command(self, command: str) -> None:
        if command not in ALLOWED_COMMANDS:
            raise ValueError(
                f"Unsupported claw-code command: {command}. "
                f"Allowed: {sorted(ALLOWED_COMMANDS)}"
            )

    def _sanitize_args(self, command: str, args: Dict[str, Any]) -> Tuple[List[str], Dict[str, Any]]:
        """Extract positional arguments and validate flag arguments."""
        positional_names, allowed_flags = COMMAND_DEFS[command]
        
        positional_args = []
        flag_args = {}
        
        for name in positional_names:
            if name not in args:
                raise ValueError(f"Missing required positional argument: {name}")
            value = args[name]
            if not isinstance(value, str):
                # Convert to string for command line
                value = str(value)
            positional_args.append(value)
        
        for key, value in args.items():
            if key in positional_names:
                continue  # Already handled
            if key not in allowed_flags:
                raise ValueError(
                    f"Unsupported flag '{key}' for command '{command}'. "
                    f"Allowed flags: {sorted(allowed_flags)}"
                )
            
            # Validate type
            if isinstance(value, bool):
                flag_args[key] = value
            elif isinstance(value, (int, float, str)):
                flag_args[key] = value
            else:
                raise ValueError(
                    f"Unsupported argument type for '{key}': {type(value).__name__}"
                )
        
        return positional_args, flag_args

    async def _run_command(
        self,
        run_id: str,
        command: str,
        positional_args: List[str],
        flag_args: Dict[str, Any],
        started_at: float,
        context: Dict[str, Any],
    ) -> HarnessResult:
        cmd = [self.python_bin, "-m", self.module_name, command]
        cmd.extend(positional_args)
        
        for key, value in flag_args.items():
            flag = f"--{key.replace('_', '-')}"  # Convert snake_case to kebab-case
            if isinstance(value, bool):
                if value:
                    cmd.append(flag)
            else:
                cmd.extend([flag, str(value)])

        loop = asyncio.get_running_loop()

        def _exec() -> subprocess.CompletedProcess[str]:
            return subprocess.run(
                cmd,
                cwd=str(self.workspace),
                capture_output=True,
                text=True,
                timeout=self.timeout_sec,
                shell=False,
            )

        proc_result = await loop.run_in_executor(None, _exec)
        completed_at = time.time()

        raw_stdout = proc_result.stdout or ""
        raw_stderr = proc_result.stderr or ""
        combined_output = raw_stdout if raw_stdout.strip() else raw_stderr

        truncated = False
        if len(combined_output) > self.max_output_chars:
            combined_output = (
                combined_output[: self.max_output_chars]
                + "\n\n[TRUNCATED OUTPUT]"
            )
            truncated = True

        return HarnessResult(
            ok=(proc_result.returncode == 0),
            run_id=run_id,
            command=command,
            args={"positional": positional_args, "flags": flag_args},
            cwd=str(self.workspace),
            started_at=started_at,
            completed_at=completed_at,
            duration_ms=int((completed_at - started_at) * 1000),
            returncode=proc_result.returncode,
            stdout=raw_stdout[: self.max_output_chars],
            stderr=raw_stderr[: self.max_output_chars],
            output=combined_output,
            truncated=truncated,
            metadata={
                "argv": self._safe_cmd_string(cmd),
                "python_bin": self.python_bin,
                "module_name": self.module_name,
                "context": context,
            },
        )

    async def _log_event(self, event_type: str, payload: Dict[str, Any]) -> None:
        try:
            self.event_log_path.parent.mkdir(parents=True, exist_ok=True)
            line = json.dumps(
                {
                    "ts": time.time(),
                    "event_type": event_type,
                    "payload": payload,
                },
                ensure_ascii=False,
            )
            await asyncio.to_thread(self._append_line, self.event_log_path, line)
        except Exception:
            # Never allow logging failure to break the harness.
            pass

    @staticmethod
    def _append_line(path: Path, line: str) -> None:
        with path.open("a", encoding="utf-8") as f:
            f.write(line + "\n")

    @staticmethod
    def _safe_cmd_string(cmd: List[str]) -> str:
        return " ".join(shlex.quote(part) for part in cmd)


# ============================================================
# OPENCLAW TOOL SURFACE
# ============================================================

HARNESS = ClawHarness()


async def claw_invoke(command: str, args: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return await HARNESS.invoke(command=command, args=args or {})


async def claw_summary() -> Dict[str, Any]:
    return await HARNESS.summary()


async def claw_manifest() -> Dict[str, Any]:
    return await HARNESS.manifest()


async def claw_subsystems(limit: int = 16) -> Dict[str, Any]:
    return await HARNESS.subsystems(limit=limit)


async def claw_commands(limit: int = 10, query: Optional[str] = None) -> Dict[str, Any]:
    return await HARNESS.commands(limit=limit, query=query)


async def claw_tools(limit: int = 10, query: Optional[str] = None) -> Dict[str, Any]:
    return await HARNESS.tools(limit=limit, query=query)


async def claw_parity_audit() -> Dict[str, Any]:
    return await HARNESS.parity_audit()


async def claw_route(prompt: str, limit: int = 5) -> Dict[str, Any]:
    return await HARNESS.route(prompt, limit=limit)


async def claw_exec_tool(name: str, payload: str) -> Dict[str, Any]:
    return await HARNESS.exec_tool(name, payload)


async def claw_exec_command(name: str, prompt: str) -> Dict[str, Any]:
    return await HARNESS.exec_command(name, prompt)


async def claw_show_tool(name: str) -> Dict[str, Any]:
    return await HARNESS.show_tool(name)


async def claw_show_command(name: str) -> Dict[str, Any]:
    return await HARNESS.show_command(name)


SKILL = {
    "name": "claw_harness",
    "description": (
        "Enhanced structured wrapper around the claw-code Python harness. "
        "Use for command/tool inventory, execution, routing, and analysis."
    ),
    "functions": [
        "claw_invoke",
        "claw_summary",
        "claw_manifest",
        "claw_subsystems",
        "claw_commands",
        "claw_tools",
        "claw_parity_audit",
        "claw_route",
        "claw_exec_tool",
        "claw_exec_command",
        "claw_show_tool",
        "claw_show_command",
    ],
}