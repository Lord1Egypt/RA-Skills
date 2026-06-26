"""路径与运行时目录解析（无业务逻辑）。

负责回答四个问题：
  1) skill 根目录在哪？        -> WORKSPACE_ROOT
  2) config.json 读哪个？      -> resolve_config_path_for_read()
  3) 任务输出落到哪？          -> resolve_output_root()
  4) 续跑 / 批量状态文件在哪？ -> resolve_runtime_state_file() / resolve_batch_runs_dir()

优先级一律是「环境变量 > skill 自带默认」。环境变量见 HOME_ENV / STATE_DIR_ENV / OUTPUT_DIR_ENV。
本文件不依赖任何其它脚本模块，是整个 skill 的最底层。
"""
from __future__ import annotations

import os
import tempfile
from pathlib import Path


APP_NAME = "bizyair"
SCRIPT_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = SCRIPT_DIR.parent

HOME_ENV = "BIZYAIR_HOME"
STATE_DIR_ENV = "BIZYAIR_STATE_DIR"
OUTPUT_DIR_ENV = "BIZYAIR_OUTPUT_DIR"

WORKSPACE_RUNTIME_ROOT = WORKSPACE_ROOT / ".tmp" / APP_NAME
WORKSPACE_OUTPUT_ROOT = WORKSPACE_RUNTIME_ROOT / "outputs"


def _expand_path(value: str) -> Path:
    return Path(os.path.expandvars(os.path.expanduser(str(value)))).resolve()


def display_path(path: str | Path) -> str:
    raw = str(path)
    home = str(Path.home())
    if raw == home:
        return "~"
    if raw.startswith(home + os.sep):
        return "~" + raw[len(home):]
    return raw


def preferred_config_path() -> Path:
    return (WORKSPACE_ROOT / "config.json").resolve()


def resolve_config_path_for_read() -> Path:
    return preferred_config_path()


def config_display_path() -> str:
    return display_path(preferred_config_path())


def resolve_runtime_root() -> Path:
    state_override = os.environ.get(STATE_DIR_ENV, "").strip()
    if state_override:
        return _expand_path(state_override)

    home_override = os.environ.get(HOME_ENV, "").strip()
    if home_override:
        return _expand_path(home_override)

    return WORKSPACE_RUNTIME_ROOT.resolve()


def resolve_runtime_state_file() -> Path:
    return (resolve_runtime_root() / "runtime_state.json").resolve()


def resolve_batch_runs_dir() -> Path:
    return (resolve_runtime_root() / "batch_runs").resolve()


def resolve_output_root() -> Path:
    output_override = os.environ.get(OUTPUT_DIR_ENV, "").strip()
    if output_override:
        return _expand_path(output_override)

    home_override = os.environ.get(HOME_ENV, "").strip()
    if home_override:
        return (_expand_path(home_override) / "outputs").resolve()

    return WORKSPACE_OUTPUT_ROOT.resolve()


def load_config_json() -> dict:
    config_path = resolve_config_path_for_read()
    try:
        if config_path.exists():
            parsed = json_load(config_path)
            if isinstance(parsed, dict):
                return parsed
    except Exception:
        pass
    return {}


def json_load(path: Path) -> object:
    import json

    return json.loads(path.read_text(encoding="utf-8"))
