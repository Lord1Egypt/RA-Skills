from __future__ import annotations


# --- UTF-8 stdout/stderr (Windows 中文输出防乱码) -----------------------------
def _configure_stream_encoding(stream):
    reconfigure = getattr(stream, "reconfigure", None)
    if callable(reconfigure):
        reconfigure(encoding="utf-8")

import sys as _sys
_configure_stream_encoding(_sys.stdout)
_configure_stream_encoding(_sys.stderr)
del _sys
# ----------------------------------------------------------------------------

from log_util import get_logger

log = get_logger("runtime")

import hashlib
import json
import subprocess
import sys
from pathlib import Path

MIN_PYTHON = (3, 10)
DEFAULT_MODEL_NAME = "DeepSeek-R1-Distill-Qwen-1.5B-int4-cw-ov"

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
VENV_DIR = SKILL_DIR / ".venv"
REQUIREMENTS_FILE = SKILL_DIR / "requirements.txt"
REQUIREMENTS_STAMP = VENV_DIR / ".requirements.sha256"
BIN_DIR = SKILL_DIR / "bin"
MODELS_DIR = SKILL_DIR / "models"
DEFAULT_MODEL_DIR = MODELS_DIR / DEFAULT_MODEL_NAME

# 跨平台路径：Windows 用 Scripts/python.exe，Unix 用 bin/python
_IS_WINDOWS = sys.platform == "win32"
if _IS_WINDOWS:
    VENV_PYTHON = VENV_DIR / "Scripts" / "python.exe"
    FFMPEG_PATH = BIN_DIR / "ffmpeg.exe"
    FFPROBE_PATH = BIN_DIR / "ffprobe.exe"
else:
    VENV_PYTHON = VENV_DIR / "bin" / "python"
    FFMPEG_PATH = BIN_DIR / "ffmpeg"
    FFPROBE_PATH = BIN_DIR / "ffprobe"


def min_python_display() -> str:
    return f"{MIN_PYTHON[0]}.{MIN_PYTHON[1]}"


def python_version_supported(version_info: tuple[int, int] | None = None) -> bool:
    if version_info is None:
        version_info = (sys.version_info.major, sys.version_info.minor)
    return version_info >= MIN_PYTHON


def assert_host_python_supported() -> None:
    if python_version_supported():
        return
    version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    raise RuntimeError(
        f"当前 Python 版本 {version} 不受支持，需要 Python >= {min_python_display()}。"
    )


def ensure_skill_venv() -> Path:
    assert_host_python_supported()
    if VENV_PYTHON.exists():
        return VENV_PYTHON

    VENV_DIR.parent.mkdir(parents=True, exist_ok=True)
    log.info(f"[venv] 创建统一虚拟环境：{VENV_DIR}")
    subprocess.run([sys.executable, "-m", "venv", str(VENV_DIR)], check=True)
    if not VENV_PYTHON.exists():
        raise RuntimeError(f"虚拟环境创建后未找到 Python：{VENV_PYTHON}")
    log.info(f"[venv] ✓ 虚拟环境已就绪：{VENV_PYTHON}")
    return VENV_PYTHON


def requirements_digest() -> str:
    if not REQUIREMENTS_FILE.exists():
        return ""
    return hashlib.sha256(REQUIREMENTS_FILE.read_bytes()).hexdigest()


def requirements_current() -> bool:
    if not VENV_PYTHON.exists() or not REQUIREMENTS_STAMP.exists():
        return False
    return REQUIREMENTS_STAMP.read_text(encoding="utf-8").strip() == requirements_digest()


def ensure_skill_requirements(force: bool = False) -> Path:
    venv_python = ensure_skill_venv()
    digest = requirements_digest()

    if not force and digest and requirements_current():
        log.info(f"[venv] 依赖已是最新：{REQUIREMENTS_FILE}")
        return venv_python

    if not REQUIREMENTS_FILE.exists():
        raise FileNotFoundError(f"requirements.txt 不存在：{REQUIREMENTS_FILE}")

    log.info(f"[venv] 安装依赖：{REQUIREMENTS_FILE}")
    subprocess.run([str(venv_python), "-m", "pip", "install", "--upgrade", "pip"], check=True)
    subprocess.run(
        [str(venv_python), "-m", "pip", "install", "-r", str(REQUIREMENTS_FILE)],
        check=True,
    )
    REQUIREMENTS_STAMP.write_text(digest, encoding="utf-8")
    log.info("[venv] ✓ requirements.txt 依赖安装完成")
    return venv_python


def running_in_skill_venv() -> bool:
    if not VENV_PYTHON.exists():
        return False
    try:
        current = Path(sys.executable).resolve()
        target = VENV_PYTHON.resolve()
    except OSError:
        return False
    return current == target


def maybe_reexec_in_skill_venv(script_path: Path) -> None:
    if running_in_skill_venv():
        return
    if not VENV_PYTHON.exists():
        return
    cmd = [str(VENV_PYTHON), str(script_path), *sys.argv[1:]]
    raise SystemExit(subprocess.call(cmd))


def runtime_summary() -> dict[str, str]:
    return {
        "skill_dir": str(SKILL_DIR),
        "venv_dir": str(VENV_DIR),
        "venv_python": str(VENV_PYTHON),
        "requirements_file": str(REQUIREMENTS_FILE),
        "ffmpeg": str(FFMPEG_PATH),
        "ffprobe": str(FFPROBE_PATH),
        "model_dir": str(DEFAULT_MODEL_DIR),
        "min_python": min_python_display(),
    }


def write_runtime_manifest(
    workspace_dir: Path,
    merge: dict | None = None,
) -> Path:
    """写出工作区 runtime_env.json。

    教学场景特化：merge 字段默认包含 ``compose_target_module``，用于指明
    下游教学课件生成阶段需要装配的模块名（例如 lesson_compose /
    slide_build 等）。其他键可由调用方追加。
    """
    manifest_path = workspace_dir / "runtime_env.json"
    payload: dict[str, object] = dict(
        runtime_summary() | {"workspace_dir": str(workspace_dir)}
    )
    payload.setdefault("compose_target_module", None)
    if merge:
        payload |= merge
    manifest_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return manifest_path
