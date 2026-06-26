#!/usr/bin/env python3
"""
douyin-transcribe-lz 环境自动配置

首次使用前运行此脚本，自动完成：
  1. 检测兼容的 Python 版本（需要 3.10~3.12，不兼容 3.13）
  2. 创建独立 venv
  3. 按正确顺序安装所有依赖（numpy<2 优先）
  4. 安装 Chromium 浏览器
  5. 验证所有包可正常 import
  6. 保存配置供后续使用

用法：
    python setup_env.py [--force] [--mirror {aliyun|pypi|tsinghua}]
"""

import os
import sys
import shutil
import subprocess
import platform
import json
import re
from pathlib import Path

# ── 配置 ──────────────────────────────────────────────────────────────────────

SKILL_DIR = Path(__file__).resolve().parent.parent  # douyin-transcribe-lz/
VENV_DIR = SKILL_DIR / "venv"
CONFIG_FILE = SKILL_DIR / ".env_config.json"

PYTHON_MIN = (3, 10)
PYTHON_RECOMMENDED = (3, 12)
PYTHON_INCOMPATIBLE = (3, 13)  # greenlet DLL 在 3.13 下加载失败

MIRRORS = {
    "aliyun": {"url": "https://mirrors.aliyun.com/pypi/simple/", "trusted": True},
    "pypi": {"url": "https://pypi.org/simple/", "trusted": False},
    "tsinghua": {"url": "https://pypi.tuna.tsinghua.edu.cn/simple/", "trusted": True},
}

# ── 工具函数 ──────────────────────────────────────────────────────────────────

def info(msg: str):
    print(f"\033[36m[INFO]\033[0m {msg}")

def success(msg: str):
    print(f"\033[32m[OK]\033[0m   {msg}")

def warn(msg: str):
    print(f"\033[33m[WARN]\033[0m {msg}")

def error(msg: str):
    print(f"\033[31m[ERR]\033[0m  {msg}")


def run_cmd(cmd: list, **kwargs) -> subprocess.CompletedProcess:
    """运行命令，捕获输出，失败时打印诊断信息。"""
    try:
        return subprocess.run(cmd, capture_output=True, text=True, **kwargs)
    except FileNotFoundError:
        error(f"命令未找到: {cmd[0]}")
        raise


def find_python() -> str | None:
    """在 PATH 中查找兼容的 Python 解释器。"""
    candidates = []

    # Windows 常见路径
    if sys.platform == "win32":
        candidates = [
            "python3.12", "python3.11", "python3.10",
            "python312", "python311", "python310",
            "python3", "python",
        ]
        # 也尝试 Program Files 下的常见路径
        program_files = [
            os.environ.get("ProgramFiles", "C:\\Program Files"),
            os.environ.get("LOCALAPPDATA", ""),
        ]
        for pf in program_files:
            if not pf:
                continue
            for ver in ["312", "311", "310"]:
                path = os.path.join(pf, "Python", f"Python{ver[:1]}.{ver[1:]}", "python.exe")
                if os.path.exists(path):
                    candidates.insert(0, path)
    else:
        candidates = [
            "python3.12", "python3.11", "python3.10",
            "python3", "python",
        ]
        # macOS: Homebrew (Intel + Apple Silicon)
        for ver in ["3.12", "3.11", "3.10"]:
            for prefix in ["/usr/local/bin", "/opt/homebrew/bin"]:
                path = os.path.join(prefix, f"python{ver}")
                if os.path.exists(path):
                    candidates.insert(0, path)
        # Linux: common alt-install paths
        for ver in ["3.12", "3.11", "3.10"]:
            path = f"/usr/bin/python{ver}"
            if os.path.exists(path):
                candidates.insert(0, path)

    for cmd in candidates:
        if sys.platform == "win32" and os.path.exists(os.path.expandvars(cmd)):
            return cmd
        try:
            result = subprocess.run([cmd, "--version"], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return cmd
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue

    return None


def check_python_version(python_path: str) -> tuple[bool, str]:
    """检查 Python 版本兼容性。返回 (是否兼容, 版本描述)。"""
    try:
        result = subprocess.run(
            [python_path, "-c", "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')"],
            capture_output=True, text=True, timeout=10
        )
        ver_str = result.stdout.strip()
        parts = ver_str.split(".")
        major, minor = int(parts[0]), int(parts[1])

        if (major, minor) >= PYTHON_INCOMPATIBLE:
            return False, f"{ver_str} (不兼容: Python 3.13+ 的 greenlet DLL 无法加载)"
        if (major, minor) < PYTHON_MIN:
            return False, f"{ver_str} (不兼容: 需要 Python >= {PYTHON_MIN[0]}.{PYTHON_MIN[1]})"
        return True, ver_str
    except Exception as e:
        return False, f"无法检测: {e}"


def get_pip_install_cmd(python_path: str, mirror: str) -> list:
    """构造 pip install 命令，选择合适的镜像源。"""
    mirror_cfg = MIRRORS.get(mirror, MIRRORS["aliyun"])
    cmd = [python_path, "-m", "pip", "install", "-i", mirror_cfg["url"]]
    if mirror_cfg["trusted"]:
        host = mirror_cfg["url"].split("://")[1].split("/")[0]
        cmd.extend(["--trusted-host", host])
    return cmd


def save_config(python_path: str, mirror: str):
    """保存环境配置到 JSON 文件。"""
    config = {
        "venv_python": python_path,
        "venv_dir": str(VENV_DIR.resolve()),
        "mirror": mirror,
        "created_at": __import__("datetime").datetime.now().isoformat(),
        "platform": platform.platform(),
        "python_version": sys.version.split()[0],
    }
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    info(f"配置已保存: {CONFIG_FILE}")


def load_config() -> dict | None:
    """读取保存的环境配置。"""
    if not CONFIG_FILE.exists():
        return None
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


# ── 主流程 ────────────────────────────────────────────────────────────────────

def main():
    force = "--force" in sys.argv
    mirror = "aliyun"
    for arg in sys.argv[1:]:
        if arg.startswith("--mirror="):
            mirror = arg.split("=", 1)[1]

    print("=" * 60)
    print("  douyin-transcribe-lz 环境配置工具")
    print("=" * 60)
    print()

    # 1. 查找兼容的 Python
    info("检测 Python 环境...")

    # 检查是否已有保存的配置
    existing = load_config()
    if existing and not force:
        venv_python = existing.get("venv_python", "")
        if os.path.exists(venv_python):
            info(f"发现已有配置: {venv_python}")
            info("如需重建，请使用 --force 参数")
            return

    # 优先使用当前运行的 Python（如果兼容）
    current_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    info(f"当前执行 Python: {sys.executable} ({current_ver})")

    if (sys.version_info.major, sys.version_info.minor) >= PYTHON_INCOMPATIBLE:
        warn(f"当前 Python {current_ver} 不兼容，正在查找其他版本...")
        base_python = find_python()
        if not base_python:
            error("未找到兼容的 Python (需要 3.10~3.12)")
            error("请安装 Python 3.12: https://www.python.org/downloads/")
            sys.exit(1)
        info(f"使用找到的 Python: {base_python}")
    else:
        base_python = sys.executable
        info(f"使用当前 Python: {base_python}")

    # 验证版本
    compat, ver_info = check_python_version(base_python)
    if not compat:
        error(f"Python 版本不兼容: {ver_info}")
        sys.exit(1)
    success(f"Python 版本兼容: {ver_info}")

    # 2. 创建 venv
    print()
    info("创建虚拟环境...")
    if VENV_DIR.exists() and not force:
        info(f"venv 已存在: {VENV_DIR}")
        info("跳过创建，如需重建请使用 --force")
    else:
        if VENV_DIR.exists():
            shutil.rmtree(VENV_DIR)
            info(f"已删除旧的 venv: {VENV_DIR}")

        result = subprocess.run(
            [base_python, "-m", "venv", str(VENV_DIR)],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            error(f"创建 venv 失败:\n{result.stderr}")
            sys.exit(1)
        success(f"venv 已创建: {VENV_DIR}")

    # 确定 venv 内 Python 路径
    if sys.platform == "win32":
        venv_python = str(VENV_DIR / "Scripts" / "python.exe")
    else:
        venv_python = str(VENV_DIR / "bin" / "python")

    # 3. 安装依赖（按正确顺序）
    print()
    info(f"安装依赖包 (镜像: {mirror})...")

    # 先升级 pip + setuptools
    info("升级 pip 和 setuptools...")
    subprocess.run(
        venv_python.split() + ["-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel",
         "-i", MIRRORS[mirror]["url"]] +
        (["--trusted-host", MIRRORS[mirror]["url"].split("://")[1].split("/")[0]]
         if MIRRORS[mirror]["trusted"] else []),
        check=False
    )

    install_base = get_pip_install_cmd(venv_python, mirror)

    # 顺序安装，每步检查
    packages_ordered = [
        # Step A: numpy < 2 必须先装（numpy>=2 在 Python 3.12 下会崩溃）
        ("numpy (锁定版本 < 2)", ['numpy<2']),
        # Step B: 基础工具
        ("requests, imageio[ffmpeg]", ["requests", 'imageio[ffmpeg]']),
        # Step C: Playwright 浏览器控制
        ("playwright", ["playwright"]),
        # Step D: Whisper + torch（最大，最后装）
        ("openai-whisper (含 torch ~800MB)", ["openai-whisper"]),
    ]

    all_ok = True
    for step_name, pkgs in packages_ordered:
        info(f"安装 {step_name}...")
        cmd = install_base + pkgs
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            # 提取关键错误信息
            err_lines = result.stderr.strip().split("\n")
            err_summary = "\n".join(err_lines[-5:]) if err_lines else "Unknown error"
            error(f"{step_name} 安装失败:\n{err_summary}")
            all_ok = False
            break
        else:
            # 验证是否真的装上了
            success(f"{step_name} 安装完成")

    if not all_ok:
        error("\n部分依赖安装失败，请检查网络连接或更换镜像源")
        error("用法: python setup_env.py --mirror=pypi")
        sys.exit(1)

    print()
    success("所有依赖包安装完成")

    # 4. 安装 Chromium
    print()
    info("安装 Chromium 浏览器...")
    chromium_result = subprocess.run(
        [venv_python, "-m", "playwright", "install", "chromium"],
        capture_output=True, text=True
    )
    if chromium_result.returncode != 0:
        warn(f"Chromium 安装可能失败:\n{chromium_result.stderr[-300:]}")
        warn("不影响使用，但首次运行视频捕获时会自动下载")
    else:
        success("Chromium 安装完成")

    # 5. 验证所有包
    print()
    info("验证所有包是否可正常导入...")
    verify_script = """
import sys
errors = []

try:
    import torch
except Exception as e:
    errors.append(f"torch: {e}")

try:
    import whisper
except Exception as e:
    errors.append(f"whisper: {e}")

try:
    import playwright
except Exception as e:
    errors.append(f"playwright: {e}")

try:
    import requests
except Exception as e:
    errors.append(f"requests: {e}")

try:
    import imageio_ffmpeg
except Exception as e:
    errors.append(f"imageio_ffmpeg: {e}")

if errors:
    print("FAIL:", "; ".join(errors))
    sys.exit(1)
else:
    print("OK: all imports successful")
    print(f"torch: {torch.__version__}")
    print(f"whisper: {getattr(whisper, '__version__', 'installed')}")
    print(f"playwright: {getattr(playwright, '__version__', 'installed')}")
    print(f"requests: {requests.__version__}")
    print(f"ffmpeg: {imageio_ffmpeg.get_ffmpeg_exe()}")
"""

    verify_result = subprocess.run(
        [venv_python, "-c", verify_script],
        capture_output=True, text=True, timeout=30
    )

    if verify_result.returncode != 0:
        error(f"导入验证失败:\n{verify_result.stdout}\n{verify_result.stderr}")
        error("\n可能的原因:")
        error("  - VC++ Redistributable 未安装 (torch 需要)")
        error("    下载: https://aka.ms/vs/17/release/vc_redist.x64.exe")
        error("  - numpy 版本冲突，尝试: pip install 'numpy<2' --force-reinstall")
        sys.exit(1)

    print(verify_result.stdout)
    success("所有依赖验证通过！")

    # 6. 保存配置
    print()
    save_config(venv_python, mirror)

    # 7. 打印使用说明
    print()
    print("=" * 60)
    print("  [OK] 环境配置完成!")
    print("=" * 60)
    print()
    print(f"  Python 环境: {venv_python}")
    print(f"  Skill 目录:  {SKILL_DIR}")
    print()
    print("  使用方式（在 WorkBuddy 中）：")
    print('    1. 提供抖音短链接，说 "使用 douyin-transcribe 提取视频文本"')
    print(f"    2. agent 会自动使用此环境运行脚本")
    print()
    print("  手动运行:")
    print(f"    {venv_python} scripts/fetch_douyin_video.py <短链接>")
    print()


if __name__ == "__main__":
    main()
