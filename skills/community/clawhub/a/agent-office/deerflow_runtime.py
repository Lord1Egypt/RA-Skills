#!/usr/bin/env python3
"""Helpers for managing the shared embedded DeerFlow runtime."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

DEERFLOW_REPO_URL = os.environ.get(
    "AGENT_OFFICE_DEERFLOW_REPO_URL",
    "https://github.com/bytedance/deer-flow.git",
)
DEFAULT_MODEL = os.environ.get("AGENT_OFFICE_DEERFLOW_MODEL", "gpt-5.4")
DEFAULT_REASONING_EFFORT = os.environ.get(
    "AGENT_OFFICE_DEERFLOW_REASONING_EFFORT",
    "medium",
)
DEFAULT_RECURSION_LIMIT = int(
    os.environ.get("AGENT_OFFICE_DEERFLOW_RECURSION_LIMIT", "48")
)
DEFAULT_TASK_TIMEOUT = int(os.environ.get("AGENT_OFFICE_DEERFLOW_TIMEOUT", "600"))


def office_dir() -> Path:
    return Path(os.environ.get("HERMES_OFFICE_DIR", Path.home() / ".hermes" / "office"))


def runtime_root(base_dir: Path | None = None) -> Path:
    return (base_dir or office_dir()) / "deerflow-runtime" / "deer-flow"


def runtime_backend_dir(base_dir: Path | None = None) -> Path:
    return runtime_root(base_dir) / "backend"


def runtime_python(base_dir: Path | None = None) -> Path:
    return runtime_backend_dir(base_dir) / ".venv" / "bin" / "python"


def runtime_homes_root(base_dir: Path | None = None) -> Path:
    return (base_dir or office_dir()) / "deerflow-runtime" / "homes"


def worker_home(worker_id: str, base_dir: Path | None = None) -> Path:
    return runtime_homes_root(base_dir) / worker_id


def runtime_update_on_add() -> bool:
    return os.environ.get("AGENT_OFFICE_DEERFLOW_UPDATE_ON_ADD", "").lower() in {
        "1",
        "true",
        "yes",
    }


def missing_prerequisites() -> list[str]:
    missing = []
    for executable in ("git", "uv"):
        if not shutil.which(executable):
            missing.append(executable)
    return missing


def _run_checked(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    result = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        timeout=600,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "unknown error").strip()
        raise RuntimeError(f"{' '.join(cmd)} failed: {detail[:500]}")
    return result


def ensure_deerflow_runtime(update: bool = False) -> dict[str, str]:
    base_dir = office_dir()
    shared_root = base_dir / "deerflow-runtime"
    root = runtime_root(base_dir)
    backend_dir = runtime_backend_dir(base_dir)
    python_bin = runtime_python(base_dir)
    shared_root.mkdir(parents=True, exist_ok=True)

    missing = missing_prerequisites()
    if missing:
        raise RuntimeError(
            "DeerFlow 自动安装缺少依赖: " + ", ".join(missing)
        )

    if not root.exists():
        _run_checked(["git", "clone", "--depth=1", DEERFLOW_REPO_URL, str(root)])
    elif update:
        _run_checked(["git", "-C", str(root), "pull", "--ff-only"])

    if not backend_dir.exists():
        raise RuntimeError(f"DeerFlow backend 目录缺失: {backend_dir}")

    if update or not python_bin.exists():
        _run_checked(["uv", "sync"], cwd=backend_dir)

    return {
        "runtime_root": str(root),
        "runtime_backend_dir": str(backend_dir),
        "runtime_python": str(python_bin),
    }


def _yaml_string(value: str) -> str:
    return json.dumps(str(value), ensure_ascii=False)


def _optional_mounts() -> list[tuple[Path, str, bool]]:
    mounts: list[tuple[Path, str, bool]] = []
    extra_mounts = os.environ.get("AGENT_OFFICE_DEERFLOW_EXTRA_MOUNTS", "").strip()
    if not extra_mounts:
        return mounts
    for index, raw in enumerate(extra_mounts.split(os.pathsep), 1):
        if not raw.strip():
            continue
        path = Path(os.path.expanduser(raw.strip())).resolve()
        if path.exists():
            mounts.append((path, f"/mnt/extra-{index}", False))
    return mounts


def ensure_worker_home(
    worker_id: str,
    worker_name: str,
    role: str,
    model: str = DEFAULT_MODEL,
    base_dir: Path | None = None,
) -> Path:
    home_dir = worker_home(worker_id, base_dir)
    agent_dir = home_dir / "agents" / worker_id
    agent_dir.mkdir(parents=True, exist_ok=True)
    (home_dir / "threads").mkdir(exist_ok=True)
    (home_dir / "artifacts").mkdir(exist_ok=True)

    (agent_dir / "config.yaml").write_text(
        "\n".join(
            [
                f"name: {worker_id}",
                f"description: Agent Office DeerFlow team for {worker_name}",
                f"model: {model}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (agent_dir / "SOUL.md").write_text(
        "\n".join(
            [
                f"你是 {worker_name}（{worker_id}），是 Agent Office 自动创建的 DeerFlow 2.0 团队型员工。",
                "",
                f"- 主要职责：{role}",
                "- 默认承接复杂、多步、需要内部拆分的任务。",
                "- 优先把任务当作团队任务处理，而不是单人直答。",
                "- 可以读取共享办公室上下文，但不要假装没有发生的内部协作。",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return home_dir


def write_worker_runtime_config(
    worker_dir: Path,
    workspace_dir: str,
    worker_id: str,
    worker_name: str,
    role: str,
    model: str = DEFAULT_MODEL,
    reasoning_effort: str = DEFAULT_REASONING_EFFORT,
) -> Path:
    resolved_worker_dir = worker_dir.resolve()
    resolved_workspace = Path(os.path.expanduser(workspace_dir)).resolve()
    mounts: list[tuple[Path, str, bool]] = [
        (resolved_workspace, "/mnt/workspace", False),
        # Expose only the current worker's local files, not the whole office.
        (resolved_worker_dir, "/mnt/worker", True),
        * _optional_mounts(),
    ]

    mount_lines: list[str] = []
    seen_mounts: set[tuple[str, str]] = set()
    for path, container_path, read_only in mounts:
        key = (str(path), container_path)
        if key in seen_mounts or not path.exists():
            continue
        seen_mounts.add(key)
        mount_lines.extend(
            [
                f"    - host_path: {_yaml_string(path)}",
                f"      container_path: {_yaml_string(container_path)}",
                f"      read_only: {'true' if read_only else 'false'}",
            ]
        )

    config_lines = [
        "config_version: 6",
        "log_level: info",
        "",
        "models:",
        f"  - name: {_yaml_string(model)}",
        f"    display_name: {_yaml_string(f'{worker_name} · {model} (Codex CLI)')}",
        "    use: deerflow.models.openai_codex_provider:CodexChatModel",
        f"    model: {_yaml_string(model)}",
        f"    reasoning_effort: {_yaml_string(reasoning_effort)}",
        "    supports_thinking: true",
        "    supports_reasoning_effort: true",
        "",
        "tool_groups:",
        "  - name: web",
        "  - name: file:read",
        "  - name: file:write",
        "  - name: bash",
        "",
        "tools:",
        "  - name: web_search",
        "    group: web",
        "    use: deerflow.community.ddg_search.tools:web_search_tool",
        "    max_results: 5",
        "  - name: web_fetch",
        "    group: web",
        "    use: deerflow.community.jina_ai.tools:web_fetch_tool",
        "    timeout: 10",
        "  - name: image_search",
        "    group: web",
        "    use: deerflow.community.image_search.tools:image_search_tool",
        "    max_results: 5",
        "  - name: ls",
        "    group: file:read",
        "    use: deerflow.sandbox.tools:ls_tool",
        "  - name: read_file",
        "    group: file:read",
        "    use: deerflow.sandbox.tools:read_file_tool",
        "  - name: glob",
        "    group: file:read",
        "    use: deerflow.sandbox.tools:glob_tool",
        "    max_results: 200",
        "  - name: grep",
        "    group: file:read",
        "    use: deerflow.sandbox.tools:grep_tool",
        "    max_results: 100",
        "  - name: write_file",
        "    group: file:write",
        "    use: deerflow.sandbox.tools:write_file_tool",
        "  - name: str_replace",
        "    group: file:write",
        "    use: deerflow.sandbox.tools:str_replace_tool",
        "  - name: bash",
        "    group: bash",
        "    use: deerflow.sandbox.tools:bash_tool",
        "",
        "sandbox:",
        "  use: deerflow.sandbox.local:LocalSandboxProvider",
        "  allow_host_bash: true",
        "  mounts:",
        *mount_lines,
        "  bash_output_max_chars: 20000",
        "  read_file_output_max_chars: 50000",
        "  ls_output_max_chars: 20000",
        "",
        "skills:",
        "  container_path: /mnt/skills",
        "",
        "memory:",
        "  enabled: true",
        "  storage_path: memory.json",
        "  debounce_seconds: 5",
        "  model_name: null",
        "  max_facts: 80",
        "  fact_confidence_threshold: 0.7",
        "  injection_enabled: true",
        "  max_injection_tokens: 2000",
        "",
        "title:",
        "  enabled: true",
        "  max_words: 6",
        "  max_chars: 60",
        "  model_name: null",
        "",
        "summarization:",
        "  enabled: true",
        "  model_name: null",
        "  trigger:",
        "    - type: tokens",
        "      value: 15564",
        "  keep:",
        "    type: messages",
        "    value: 10",
        "  trim_tokens_to_summarize: 15564",
        "  summary_prompt: null",
        "",
    ]
    config_path = worker_dir / "deerflow_config.yaml"
    config_path.write_text("\n".join(config_lines), encoding="utf-8")
    return config_path
