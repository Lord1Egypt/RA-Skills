#!/usr/bin/env python3
"""
builtin-tools 公共层
跨平台命令执行 + JSON 协议 + 路径处理
纯 Python 标准库，零外部依赖
"""

import subprocess
import sys
import os
import json
import re
from pathlib import Path


# ─── Exit Codes ───────────────────────────────────────────
EXIT_OK = 0
EXIT_PARAM_ERROR = 1
EXIT_EXEC_ERROR = 2
EXIT_UNSUPPORTED_OS = 3


# ─── JSON Protocol ────────────────────────────────────────
def parse_input():
    """从命令行参数或 stdin 读取 JSON 输入"""
    if len(sys.argv) > 1:
        raw = " ".join(sys.argv[1:])
    elif not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
    else:
        return None
    if not raw:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        output_error(f"JSON 解析失败: {e}", EXIT_PARAM_ERROR)


def output_ok(data=None, message="ok"):
    """输出成功结果"""
    result = {"status": "ok", "data": data, "message": message}
    print(json.dumps(result, ensure_ascii=False, default=str))


def output_error(message, code=EXIT_EXEC_ERROR):
    """输出错误结果并退出"""
    result = {"status": "error", "code": code, "message": message}
    print(json.dumps(result, ensure_ascii=False), file=sys.stderr)
    sys.exit(code)


def get_param(params, key, default=None, required=False):
    """安全获取参数"""
    if params is None:
        if required:
            output_error(f"缺少必要参数: {key}", EXIT_PARAM_ERROR)
        return default
    value = params.get(key, default)
    if required and value is None:
        output_error(f"缺少必要参数: {key}", EXIT_PARAM_ERROR)
    return value


# ─── Shell Execution ──────────────────────────────────────
def run_shell(script, timeout=60):
    """
    跨平台命令执行，自动选择 Shell
    Returns: (stdout, stderr, returncode)
    """
    if not script or not script.strip():
        return "", "空命令", 1

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    if sys.platform == "win32":
        encoding_setup = (
            "[Console]::InputEncoding = [Console]::OutputEncoding = "
            "[System.Text.Encoding]::UTF8; "
            "$OutputEncoding = [System.Text.Encoding]::UTF8; "
        )
        full_script = encoding_setup + script
        cmd = ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", full_script]
    else:
        full_script = script
        cmd = ["/bin/sh", "-c", full_script]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            env=env,
        )
        stdout = (result.stdout or "").strip()
        stderr = (result.stderr or "").strip()
        return stdout, stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", f"命令超时 ({timeout}s)", 1
    except FileNotFoundError:
        return "", "Shell 未找到", 3
    except Exception as e:
        return "", str(e), 2


# ─── Path Utilities ───────────────────────────────────────
def resolve_path(path, must_exist=False, base=None):
    """解析路径为绝对路径"""
    if not path:
        output_error("路径不能为空", EXIT_PARAM_ERROR)
    p = Path(path)
    if not p.is_absolute():
        p = (Path(base) if base else Path.cwd()) / p
    p = p.resolve()
    if must_exist and not p.exists():
        output_error(f"路径不存在: {p}", EXIT_EXEC_ERROR)
    return p


def home_dir():
    """用户主目录"""
    return Path.home()


def memory_dir(base=None):
    """记忆目录（跨平台）"""
    if base:
        return resolve_path(base)
    return home_dir() / ".workbuddy" / "memory"


# ─── File Utilities (内部使用) ────────────────────────────
def read_text_file(path, encoding="utf-8"):
    """读取文本文件"""
    p = resolve_path(str(path), must_exist=True)
    try:
        return p.read_text(encoding=encoding, errors="replace")
    except Exception as e:
        output_error(f"读取文件失败: {e}", EXIT_EXEC_ERROR)


def write_text_file(path, content, encoding="utf-8", mkdirs=False):
    """写入文本文件"""
    p = resolve_path(str(path))
    if mkdirs:
        p.parent.mkdir(parents=True, exist_ok=True)
    try:
        p.write_text(content, encoding=encoding)
        return p.stat().st_size
    except Exception as e:
        output_error(f"写入文件失败: {e}", EXIT_EXEC_ERROR)


def ensure_dir(path):
    """确保目录存在"""
    p = resolve_path(str(path))
    p.mkdir(parents=True, exist_ok=True)
    return p
