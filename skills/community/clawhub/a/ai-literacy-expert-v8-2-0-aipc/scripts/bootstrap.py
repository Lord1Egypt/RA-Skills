"""
bootstrap.py - 统一准备阶段：.venv / requirements / ffmpeg / 文本推理模型

对应 video-editing-skills-main/scripts/bootstrap.py，但模型阶段调用
setup_text_model.py（DeepSeek-R1-1.5B）而非 setup_ov_model.py（Qwen2.5-VL-7B）。

执行顺序：
    1. ensure_skill_requirements  (venv + pip install)
    2. ensure_ffmpeg               (下载 ffmpeg/ffprobe 到 bin/)
    3. ensure_model                (下载 + 校验文本推理模型到 models/)
    4. runtime_summary()           (返回所有路径字典)

用法：
    python bootstrap.py                          # 全量准备（首次）
    python bootstrap.py --skip-model             # 跳过模型（调试用）
    python bootstrap.py --force-model            # 强制重下模型
    python bootstrap.py --json                   # JSON 输出
"""
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

import argparse
import json
import subprocess
import sys
from pathlib import Path

from skill_runtime import (
    DEFAULT_MODEL_DIR,
    SCRIPT_DIR,
    ensure_skill_requirements,
    runtime_summary,
)


def run_script_with_venv(
    venv_python: Path,
    script_name: str,
    script_args: list[str] | None = None,
    capture_output: bool = False,
) -> subprocess.CompletedProcess[str]:
    if script_args is None:
        script_args = []
    cmd = [str(venv_python), str(SCRIPT_DIR / script_name), *script_args]
    return subprocess.run(
        cmd,
        check=False,
        capture_output=capture_output,
        text=True,
    )


def ensure_ffmpeg(venv_python: Path, force: bool = False) -> None:
    args: list[str] = []
    if force:
        args.append("--force")
    result = run_script_with_venv(venv_python, "setup_resources.py", args)
    if result.returncode != 0:
        raise RuntimeError("ffmpeg / ffprobe 准备失败")


def ensure_model(venv_python: Path, force: bool = False) -> None:
    if not force:
        check = run_script_with_venv(
            venv_python,
            "setup_text_model.py",
            ["--check-only"],
            capture_output=True,
        )
        if check.returncode == 0:
            if check.stdout:
                log.info(check.stdout.strip())
            return
        if check.stdout:
            log.info(check.stdout.strip())
        if check.stderr:
            log.error(check.stderr.strip())

    args: list[str] = []
    if force:
        args.append("--force")
    result = run_script_with_venv(venv_python, "setup_text_model.py", args)
    if result.returncode != 0:
        raise RuntimeError(f"模型准备失败：{DEFAULT_MODEL_DIR}")


def bootstrap_environment(
    force_requirements: bool = False,
    force_ffmpeg: bool = False,
    force_model: bool = False,
    skip_ffmpeg: bool = False,
    skip_model: bool = False,
) -> dict[str, str]:
    venv_python = ensure_skill_requirements(force=force_requirements)
    if not skip_ffmpeg:
        ensure_ffmpeg(venv_python, force=force_ffmpeg)
    if not skip_model:
        ensure_model(venv_python, force=force_model)
    return runtime_summary()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="统一准备阶段 bootstrap：.venv、requirements、ffmpeg、文本推理模型"
    )
    parser.add_argument(
        "--force-requirements",
        action="store_true",
        help="强制重新安装 requirements.txt",
    )
    parser.add_argument(
        "--force-ffmpeg",
        action="store_true",
        help="强制重新下载 ffmpeg / ffprobe",
    )
    parser.add_argument(
        "--force-model",
        action="store_true",
        help="强制重新下载 OpenVINO 文本推理模型",
    )
    parser.add_argument(
        "--skip-ffmpeg",
        action="store_true",
        help="跳过 ffmpeg / ffprobe 准备",
    )
    parser.add_argument(
        "--skip-model",
        action="store_true",
        help="跳过模型准备",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="以 JSON 输出准备结果",
    )
    return parser.parse_args()


def main() -> int:
    log = get_logger("bootstrap")
    args = parse_args()
    try:
        summary = bootstrap_environment(
            force_requirements=args.force_requirements,
            force_ffmpeg=args.force_ffmpeg,
            force_model=args.force_model,
            skip_ffmpeg=args.skip_ffmpeg,
            skip_model=args.skip_model,
        )
    except Exception as exc:
        log.error(f"[bootstrap] ✗ 失败：{exc}")
        return 1

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        log.info("[bootstrap] ✓ 准备完成")
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
