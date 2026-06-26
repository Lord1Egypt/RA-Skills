#!/usr/bin/env python3
"""Shared helpers for the AutoDL training operator skill."""

from __future__ import annotations

import argparse
import base64
import json
import os
import posixpath
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

DEFAULT_CONFIG: Dict[str, Any] = {
    "port": 22,
    "strict_host_key_checking": "accept-new",
    "project_path": "/root/autodl-tmp/your-project",
    "allowed_project_roots": ["/root/autodl-tmp"],
    "conda_sh_path": "/root/miniconda3/etc/profile.d/conda.sh",
    "venv_path": "venv",
    "env_activate": "",
    "resume_argument_template": "--resume-from {checkpoint}",
    "log_path": "logs/train.log",
    "log_candidates": ["logs/train.log", "outputs/latest.log", "nohup.out"],
    "status_log_tail": 40,
    "summary_log_tail": 400,
    "resource_warn_disk_pct": 85,
    "resource_warn_memory_pct": 90,
    "resource_warn_gpu_memory_pct": 90,
    "resource_low_gpu_util_pct": 30,
    "extra_ssh_options": [],
}

ENV_MAP = {
    "host": "AUTOCLAW_TRAIN_HOST",
    "port": "AUTOCLAW_TRAIN_PORT",
    "username": "AUTOCLAW_TRAIN_USERNAME",
    "ssh_key_path": "AUTOCLAW_TRAIN_SSH_KEY_PATH",
    "ssh_password": "AUTOCLAW_TRAIN_SSH_PASSWORD",
    "strict_host_key_checking": "AUTOCLAW_TRAIN_STRICT_HOST_KEY_CHECKING",
    "project_path": "AUTOCLAW_TRAIN_PROJECT_PATH",
    "allowed_project_roots": "AUTOCLAW_TRAIN_ALLOWED_PROJECT_ROOTS",
    "env_name": "AUTOCLAW_TRAIN_ENV_NAME",
    "conda_sh_path": "AUTOCLAW_TRAIN_CONDA_SH_PATH",
    "venv_path": "AUTOCLAW_TRAIN_VENV_PATH",
    "env_activate": "AUTOCLAW_TRAIN_ENV_ACTIVATE",
    "train_command": "AUTOCLAW_TRAIN_TRAIN_COMMAND",
    "resume_argument_template": "AUTOCLAW_TRAIN_RESUME_ARGUMENT_TEMPLATE",
    "process_match": "AUTOCLAW_TRAIN_PROCESS_MATCH",
    "log_path": "AUTOCLAW_TRAIN_LOG_PATH",
    "log_candidates": "AUTOCLAW_TRAIN_LOG_CANDIDATES",
    "status_log_tail": "AUTOCLAW_TRAIN_STATUS_LOG_TAIL",
    "summary_log_tail": "AUTOCLAW_TRAIN_SUMMARY_LOG_TAIL",
    "resource_warn_disk_pct": "AUTOCLAW_TRAIN_RESOURCE_WARN_DISK_PCT",
    "resource_warn_memory_pct": "AUTOCLAW_TRAIN_RESOURCE_WARN_MEMORY_PCT",
    "resource_warn_gpu_memory_pct": "AUTOCLAW_TRAIN_RESOURCE_WARN_GPU_MEMORY_PCT",
    "resource_low_gpu_util_pct": "AUTOCLAW_TRAIN_RESOURCE_LOW_GPU_UTIL_PCT",
}

DANGEROUS_COMMAND_FRAGMENTS = [
    "rm -rf",
    "reboot",
    "shutdown",
    "poweroff",
    "mkfs",
    "kill -9 -1",
    ":(){",
    "dd if=",
]


class SkillError(RuntimeError):
    """Raised when configuration or remote execution fails."""


class ConfigArgumentParser(argparse.ArgumentParser):
    """Argument parser with shared config overrides."""

    def __init__(self, description: str) -> None:
        super().__init__(description=description)
        self.add_argument("--config", help="Path to a JSON config file.")
        self.add_argument("--env-file", help="Path to a .env file.")
        self.add_argument("--host")
        self.add_argument("--port", type=int)
        self.add_argument("--username")
        self.add_argument("--ssh-key-path")
        self.add_argument("--strict-host-key-checking")
        self.add_argument("--project-path")
        self.add_argument(
            "--allowed-project-root",
            action="append",
            dest="allowed_project_roots",
            help="Allowed remote project root. Can be set more than once.",
        )
        self.add_argument("--env-name")
        self.add_argument("--conda-sh-path")
        self.add_argument("--venv-path")
        self.add_argument("--env-activate")
        self.add_argument("--train-command")
        self.add_argument("--resume-argument-template")
        self.add_argument("--process-match")
        self.add_argument("--log-path")
        self.add_argument(
            "--log-candidate",
            action="append",
            dest="log_candidates",
            help="Additional log candidate path. Can be set more than once.",
        )
        self.add_argument("--status-log-tail", type=int)
        self.add_argument("--summary-log-tail", type=int)
        self.add_argument("--json", action="store_true", help="Print machine-readable JSON only.")


def json_dump(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True)


def print_json(data: Any) -> None:
    print(json_dump(data))


def print_error(message: str, *, json_mode: bool = False, details: Optional[Dict[str, Any]] = None) -> None:
    payload = {"ok": False, "error": message}
    if details:
        payload.update(details)
    if json_mode:
        print_json(payload)
    else:
        print(f"ERROR: {message}", file=sys.stderr)
        if details:
            print_json(details)


def load_env_file(path: Optional[str]) -> Dict[str, str]:
    if not path:
        return {}
    env_path = Path(path).expanduser()
    if not env_path.is_file():
        raise SkillError(f"env file not found: {env_path}")
    data: Dict[str, str] = {}
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def load_config(args: argparse.Namespace) -> Dict[str, Any]:
    config: Dict[str, Any] = dict(DEFAULT_CONFIG)

    if args.config:
        config_path = Path(args.config).expanduser()
        if not config_path.is_file():
            raise SkillError(f"config file not found: {config_path}")
        with config_path.open("r", encoding="utf-8") as handle:
            file_data = json.load(handle)
        config.update(file_data)

    env_data = os.environ.copy()
    env_data.update(load_env_file(getattr(args, "env_file", None)))
    for key, env_name in ENV_MAP.items():
        value = env_data.get(env_name)
        if value is None or value == "":
            continue
        if key in {"port", "status_log_tail", "summary_log_tail", "resource_warn_disk_pct", "resource_warn_memory_pct", "resource_warn_gpu_memory_pct", "resource_low_gpu_util_pct"}:
            config[key] = int(value)
        elif key in {"log_candidates", "allowed_project_roots"}:
            config[key] = [item.strip() for item in value.split(",") if item.strip()]
        else:
            config[key] = value

    cli_overrides = {
        "host": args.host,
        "port": args.port,
        "username": args.username,
        "ssh_key_path": args.ssh_key_path,
        "strict_host_key_checking": args.strict_host_key_checking,
        "project_path": args.project_path,
        "allowed_project_roots": args.allowed_project_roots,
        "env_name": args.env_name,
        "conda_sh_path": args.conda_sh_path,
        "venv_path": args.venv_path,
        "env_activate": args.env_activate,
        "train_command": args.train_command,
        "resume_argument_template": args.resume_argument_template,
        "process_match": args.process_match,
        "log_path": args.log_path,
        "log_candidates": args.log_candidates,
        "status_log_tail": args.status_log_tail,
        "summary_log_tail": args.summary_log_tail,
    }
    for key, value in cli_overrides.items():
        if value is not None:
            config[key] = value

    normalize_config(config)
    return config


def normalize_config(config: Dict[str, Any]) -> None:
    if isinstance(config.get("allowed_project_roots"), str):
        config["allowed_project_roots"] = [config["allowed_project_roots"]]
    if not config.get("allowed_project_roots"):
        project_path = config.get("project_path", DEFAULT_CONFIG["project_path"])
        config["allowed_project_roots"] = [posixpath.dirname(project_path.rstrip("/")) or "/"]

    if isinstance(config.get("log_candidates"), str):
        config["log_candidates"] = [item.strip() for item in config["log_candidates"].split(",") if item.strip()]
    if config.get("log_path"):
        candidates = [config["log_path"]]
        for item in config.get("log_candidates", []):
            if item not in candidates:
                candidates.append(item)
        config["log_candidates"] = candidates

    if config.get("ssh_key_path"):
        config["ssh_key_path"] = os.path.expanduser(config["ssh_key_path"])


def validate_required_config(config: Dict[str, Any], *, require_train_command: bool = False) -> None:
    required = ["host", "username", "project_path"]
    if require_train_command:
        required.append("train_command")
    missing = [key for key in required if not config.get(key)]
    if missing:
        raise SkillError("missing required config keys: " + ", ".join(sorted(missing)))

    project_path = str(config["project_path"])
    if not project_path.startswith("/"):
        raise SkillError("project_path must be an absolute path")
    if project_path in {"/", "/root", "/home"}:
        raise SkillError("project_path is too broad; use the exact project directory")
    if ".." in project_path.split("/"):
        raise SkillError("project_path must not contain '..'")

    allowed_roots = config.get("allowed_project_roots") or []
    if not any(project_path == root or project_path.startswith(root.rstrip("/") + "/") for root in allowed_roots):
        raise SkillError("project_path must stay inside allowed_project_roots")

    if require_train_command:
        lowered = str(config["train_command"]).lower()
        for fragment in DANGEROUS_COMMAND_FRAGMENTS:
            if fragment in lowered:
                raise SkillError(f"refusing to run dangerous train command fragment: {fragment}")


def shell_quote(value: str) -> str:
    return shlex.quote(value)


def build_ssh_command(config: Dict[str, Any], *, inline_script: Optional[str] = None) -> List[str]:
    target = f"{config['username']}@{config['host']}"
    uses_password = bool(config.get("ssh_password"))
    command = [
        "ssh",
        "-p",
        str(config.get("port", 22)),
        "-o",
        f"StrictHostKeyChecking={config.get('strict_host_key_checking', 'accept-new')}",
        "-o",
        f"BatchMode={'no' if uses_password else 'yes'}",
    ]
    ssh_key_path = config.get("ssh_key_path")
    if ssh_key_path:
        command.extend(["-i", ssh_key_path])
    if uses_password:
        command.extend([
            "-o",
            "PreferredAuthentications=publickey,password,keyboard-interactive",
            "-o",
            "KbdInteractiveAuthentication=yes",
        ])
    for option in config.get("extra_ssh_options", []):
        command.extend(["-o", option])
    if inline_script is None:
        command.extend([target, "bash", "-s", "--"])
    else:
        encoded_script = base64.b64encode(inline_script.encode("utf-8")).decode("ascii")
        remote_command = f"printf %s {shell_quote(encoded_script)} | base64 -d | bash -s --"
        command.extend([target, remote_command])
    return command


def _make_askpass_script() -> str:
    handle = tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, prefix="autoclaw-askpass-", suffix=".sh")
    try:
        handle.write("#!/bin/sh\nprintf '%s\\n' \"$AUTOCLAW_TRAIN_SSH_PASSWORD\"\n")
        handle.flush()
    finally:
        handle.close()
    os.chmod(handle.name, 0o700)
    return handle.name


def run_remote_script(
    config: Dict[str, Any],
    script: str,
    *,
    timeout: Optional[int] = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    ssh_password = config.get("ssh_password")
    command = build_ssh_command(config, inline_script=script if ssh_password else None)
    env = os.environ.copy()
    askpass_script: Optional[str] = None
    if ssh_password:
        askpass_script = _make_askpass_script()
        env["AUTOCLAW_TRAIN_SSH_PASSWORD"] = str(ssh_password)
        env["SSH_ASKPASS"] = askpass_script
        env["SSH_ASKPASS_REQUIRE"] = "force"
        env.setdefault("DISPLAY", "autoclaw:0")

    try:
        result = subprocess.run(
            command,
            input=None if ssh_password else script,
            text=True,
            capture_output=True,
            timeout=timeout,
            env=env,
        )
    finally:
        if askpass_script:
            try:
                os.unlink(askpass_script)
            except FileNotFoundError:
                pass
    if check and result.returncode != 0:
        stderr = result.stderr.strip() or result.stdout.strip()
        raise SkillError(f"ssh exited with code {result.returncode}: {stderr}")
    return result


def remote_path(config: Dict[str, Any], path_value: str) -> str:
    if path_value.startswith("/"):
        return path_value
    return posixpath.normpath(posixpath.join(config["project_path"], path_value))


def build_guard_block(config: Dict[str, Any]) -> str:
    allowed_roots = config.get("allowed_project_roots") or []
    roots_literal = " ".join(shell_quote(root) for root in allowed_roots)
    project_path_literal = shell_quote(config["project_path"])
    return f"""
set -euo pipefail
PROJECT_PATH={project_path_literal}
export PROJECT_PATH
ALLOWED_ROOTS=({roots_literal})
ALLOW_MATCH=0
for root in "${{ALLOWED_ROOTS[@]}}"; do
  case "$PROJECT_PATH" in
    "$root"|"$root"/*) ALLOW_MATCH=1 ;;
  esac
done
if [ "$ALLOW_MATCH" -ne 1 ]; then
  echo "Refusing to work outside allowed_project_roots" >&2
  exit 2
fi
if [ ! -d "$PROJECT_PATH" ]; then
  echo "Project directory does not exist: $PROJECT_PATH" >&2
  exit 3
fi
cd "$PROJECT_PATH"
""".strip()


def build_activation_block(config: Dict[str, Any]) -> str:
    env_activate = config.get("env_activate") or ""
    env_name = config.get("env_name") or ""
    conda_sh_path = config.get("conda_sh_path") or DEFAULT_CONFIG["conda_sh_path"]
    venv_path = config.get("venv_path") or ""
    venv_activate = posixpath.join(venv_path, "bin", "activate") if venv_path else ""
    return f"""
activate_training_env() {{
  if [ -n {shell_quote(env_activate)} ]; then
    eval {shell_quote(env_activate)} && return 0
  fi
  if [ -n {shell_quote(env_name)} ]; then
    if command -v conda >/dev/null 2>&1; then
      BASE_PATH="$(conda info --base 2>/dev/null || true)"
      if [ -n "$BASE_PATH" ] && [ -f "$BASE_PATH/etc/profile.d/conda.sh" ]; then
        . "$BASE_PATH/etc/profile.d/conda.sh" && conda activate {shell_quote(env_name)} && return 0
      fi
      conda activate {shell_quote(env_name)} >/dev/null 2>&1 && return 0 || true
    fi
    if [ -f {shell_quote(conda_sh_path)} ]; then
      . {shell_quote(conda_sh_path)} && conda activate {shell_quote(env_name)} && return 0
    fi
  fi
  if [ -n {shell_quote(venv_activate)} ] && [ -f {shell_quote(venv_activate)} ]; then
    . {shell_quote(venv_activate)} && return 0
  fi
  return 1
}}
if ! activate_training_env; then
  echo "WARN: environment activation failed; continuing with current shell" >&2
fi
""".strip()


def build_process_match(config: Dict[str, Any]) -> str:
    explicit = (config.get("process_match") or "").strip()
    if explicit:
        return explicit
    command = str(config.get("train_command") or "").strip()
    return " ".join(command.split()[:6])


def resolve_log_candidates(config: Dict[str, Any]) -> List[str]:
    seen: List[str] = []
    for item in config.get("log_candidates", []) or []:
        if item and item not in seen:
            seen.append(item)
    return seen


def select_remote_log_file(config: Dict[str, Any]) -> Optional[str]:
    candidates = resolve_log_candidates(config)
    if not candidates:
        return None
    candidate_lines = "\n".join(f"CANDIDATES+=({shell_quote(item)})" for item in candidates)
    script = f"""
{build_guard_block(config)}
CANDIDATES=()
{candidate_lines}
best_path=""
best_ts=0
for raw in "${{CANDIDATES[@]}}"; do
  if [ "${{raw#/}}" != "$raw" ]; then
    candidate="$raw"
  else
    candidate="$PROJECT_PATH/$raw"
  fi
  if [ -f "$candidate" ]; then
    ts=$(stat -c '%Y' "$candidate" 2>/dev/null || echo 0)
    if [ "$ts" -ge "$best_ts" ]; then
      best_ts="$ts"
      best_path="$candidate"
    fi
  fi
done
if [ -n "$best_path" ]; then
  printf '%s\n' "$best_path"
fi
""".strip()
    result = run_remote_script(config, script, check=False)
    path = result.stdout.strip()
    return path or None


def read_remote_file_tail(config: Dict[str, Any], path_value: str, *, tail_lines: int) -> Dict[str, Any]:
    script = f"""
{build_guard_block(config)}
LOG_PATH={shell_quote(path_value)}
if [ ! -f "$LOG_PATH" ]; then
  echo "LOG_NOT_FOUND=$LOG_PATH"
  exit 4
fi
printf 'LOG_PATH=%s\n' "$LOG_PATH"
printf 'LOG_MTIME=%s\n' "$(stat -c '%y' "$LOG_PATH" 2>/dev/null || true)"
printf 'LOG_SIZE=%s\n' "$(stat -c '%s' "$LOG_PATH" 2>/dev/null || echo 0)"
echo '__LOG_START__'
tail -n {int(tail_lines)} "$LOG_PATH" || true
echo '__LOG_END__'
""".strip()
    result = run_remote_script(config, script, check=False)
    if result.returncode not in {0, 4}:
        raise SkillError(result.stderr.strip() or result.stdout.strip() or "failed to read log")
    output = result.stdout.splitlines()
    info: Dict[str, Any] = {"path": None, "mtime": None, "size": None, "text": "", "found": result.returncode == 0}
    in_log = False
    log_lines: List[str] = []
    for line in output:
        if line == "__LOG_START__":
            in_log = True
            continue
        if line == "__LOG_END__":
            in_log = False
            continue
        if in_log:
            log_lines.append(line)
            continue
        if line.startswith("LOG_PATH="):
            info["path"] = line.split("=", 1)[1]
        elif line.startswith("LOG_MTIME="):
            info["mtime"] = line.split("=", 1)[1]
        elif line.startswith("LOG_SIZE="):
            info["size"] = int(line.split("=", 1)[1] or 0)
    info["text"] = "\n".join(log_lines)
    return info


def format_command_list(command: Iterable[str]) -> str:
    return " ".join(shell_quote(part) for part in command)
