#!/usr/bin/env python3
"""
douyin-transcribe-lz 环境验证工具

检查所有依赖是否正确安装，逐项报告状态。
支持 --fix 模式自动修复检测到的问题。

用法：
    python verify_env.py          # 仅检测
    python verify_env.py --fix    # 自动修复
    python verify_env.py --json   # JSON 输出（供程序调用）
"""

import os
import sys
import json
import subprocess
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
VENV_DIR = SKILL_DIR / "venv"
CONFIG_FILE = SKILL_DIR / ".env_config.json"

# ── 辅助 ──────────────────────────────────────────────────────────────────────

def find_venv_python() -> str | None:
    """查找 venv Python 路径。"""
    # 1. 读取保存的配置
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, encoding="utf-8") as f:
                cfg = json.load(f)
            path = cfg.get("venv_python", "")
            if path and os.path.exists(path):
                return path
        except Exception:
            pass

    # 2. 按平台规则查找
    if sys.platform == "win32":
        py = VENV_DIR / "Scripts" / "python.exe"
    else:
        py = VENV_DIR / "bin" / "python"

    if py.exists():
        return str(py)

    return None


def run_python(script: str, timeout: int = 30) -> tuple[int, str, str]:
    """运行 Python 代码片段。"""
    python = find_venv_python()
    if not python:
        return -1, "", "venv Python not found"
    try:
        r = subprocess.run(
            [python, "-c", script],
            capture_output=True, text=True, timeout=timeout
        )
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except Exception as e:
        return -1, "", str(e)


def check_import(pkg: str, attr: str | None = None) -> dict:
    """检查单个包是否可导入，返回状态字典。"""
    if attr:
        script = f"import {pkg}; print({attr})"
    else:
        script = f"import {pkg}; print('OK')"

    code, out, err = run_python(script, timeout=15)
    return {
        "name": pkg,
        "ok": code == 0,
        "detail": out if code == 0 else (err[:200] if err else "import failed"),
    }


def check_chromium() -> dict:
    """检查 Chromium 浏览器是否安装。"""
    # playwright 通常安装到用户目录
    import platform
    if platform.system() == "Windows":
        base = os.path.expandvars("%USERPROFILE%\\AppData\\Local\\ms-playwright")
    elif platform.system() == "Darwin":
        base = os.path.expanduser("~/Library/Caches/ms-playwright")
    else:
        base = os.path.expanduser("~/.cache/ms-playwright")

    if not os.path.exists(base):
        return {"name": "chromium", "ok": False, "detail": f"未安装 (目录不存在: {base})"}

    # 查找任意 chromium-* 目录
    for item in os.listdir(base):
        if item.startswith("chromium-"):
            if platform.system() == "Windows":
                chrome_exe = os.path.join(base, item, "chrome-win64", "chrome.exe")
            elif platform.system() == "Darwin":
                chrome_exe = os.path.join(base, item, "chrome-mac", "Chromium.app", "Contents", "MacOS", "Chromium")
            else:
                chrome_exe = os.path.join(base, item, "chrome-linux64", "chrome")
            if os.path.exists(chrome_exe):
                return {"name": "chromium", "ok": True, "detail": item}
    return {"name": "chromium", "ok": False, "detail": "目录存在但无 chrome 可执行文件"}


def check_whisper_cache() -> dict:
    """检查 Whisper 模型缓存是否存在且完整。"""
    cache_dir = os.path.expanduser("~/.cache/whisper")
    if not os.path.exists(cache_dir):
        return {"name": "whisper-cache", "ok": False, "detail": "未下载 (目录不存在)"}

    models = [f for f in os.listdir(cache_dir) if f.endswith(".pt")]
    if not models:
        return {"name": "whisper-cache", "ok": False, "detail": "未下载 (无模型文件)"}

    # 检查文件大小是否合理 (medium.pt 约 1.42GB，< 500MB 肯定损坏)
    ok = []
    suspect = []
    for m in models:
        size = os.path.getsize(os.path.join(cache_dir, m))
        if m == "medium.pt" and size < 500_000_000:
            suspect.append(f"{m} ({size/1024/1024:.0f}MB, 疑似损坏)")
        else:
            ok.append(f"{m} ({size/1024/1024:.0f}MB)")

    if suspect:
        return {"name": "whisper-cache", "ok": False, "detail": f"损坏: {', '.join(suspect)}"}
    return {"name": "whisper-cache", "ok": True, "detail": ", ".join(ok)}


# ── 主流程 ────────────────────────────────────────────────────────────────────

def main():
    json_mode = "--json" in sys.argv
    fix_mode = "--fix" in sys.argv

    if not json_mode:
        print("=" * 50)
        print("  douyin-transcribe-lz env check")
        print("=" * 50)
        print()

    # 查找 venv Python
    python_path = find_venv_python()
    if not python_path:
        msg = "venv not found, run scripts/setup_env.py first"
        if json_mode:
            json.dump({"status": "fail", "reason": msg, "checks": []}, sys.stdout, indent=2)
            sys.exit(1)
        # --fix 模式：venv 不存在时自动运行 setup_env.py
        if fix_mode:
            print(f"  [FAIL] {msg}")
            print("  --fix: auto-running setup_env.py ...")
            setup_script = SKILL_DIR / "scripts" / "setup_env.py"
            result = subprocess.run(
                [sys.executable, str(setup_script), "--force"],
                capture_output=False,
                timeout=600,
            )
            print()
            if result.returncode == 0:
                print("  [SUCCESS] Setup completed. Re-run verify to confirm.")
            else:
                print("  [FAIL] Setup failed with exit code", result.returncode)
            sys.exit(result.returncode)
        else:
            print(f"\033[31m[FAIL]\033[0m {msg}")
            sys.exit(1)

    if not json_mode:
        print(f"  Python: {python_path}")
        print()

    # 逐项检查
    checks = []

    # 核心包
    packages = [
        ("torch", "torch.__version__"),
        ("whisper", None),
        ("playwright", None),
        ("requests", "requests.__version__"),
        ("imageio_ffmpeg", "imageio_ffmpeg.get_ffmpeg_exe()"),
    ]

    all_ok = True
    for pkg, attr in packages:
        result = check_import(pkg, attr)
        checks.append(result)
        if not result["ok"]:
            all_ok = False
        if not json_mode:
            icon = "[OK]" if result["ok"] else "[FAIL]"
            print(f"  {icon} {pkg:20s} {result['detail']}")

    # Chromium
    chromium = check_chromium()
    checks.append(chromium)
    if not chromium["ok"]:
        all_ok = False
    if not json_mode:
        icon = "[OK]" if chromium["ok"] else "[FAIL]"
        print(f"  {icon} {'chromium':20s} {chromium['detail']}")

    # Whisper 缓存
    cache = check_whisper_cache()
    checks.append(cache)
    # 缓存不存在不视为硬错误（首次运行会自动下载）
    if not json_mode:
        icon = "[OK]" if cache["ok"] else "[N/A]"
        print(f"  {icon} {'whisper-cache':20s} {cache['detail']}")

    # 汇总
    if json_mode:
        output = {
            "status": "pass" if all_ok else "fail",
            "python": python_path,
            "checks": checks,
        }
        json.dump(output, sys.stdout, indent=2, ensure_ascii=False)
        sys.exit(0 if all_ok else 1)

    # 人机可读模式
    print()
    if all_ok:
        print("  [SUCCESS] Environment ready!")
        sys.exit(0)

    # 存在问题
    print("  [FAILURE] Issues found, see [FAIL] marks above")
    print()
    print("  Fix suggestions:")
    for c in checks:
        if not c["ok"]:
            print(f"    - {c['name']}: {c['detail']}")

    # --fix 模式：自动运行 setup_env.py --force
    if fix_mode:
        print()
        print("  --fix: auto-running setup_env.py --force ...")
        setup_script = SKILL_DIR / "scripts" / "setup_env.py"
        if not setup_script.exists():
            print("  [FAIL] setup_env.py not found at", setup_script)
            sys.exit(1)
        # setup_env.py 内部会自己查找 python，用当前 python 运行即可
        result = subprocess.run(
            [sys.executable, str(setup_script), "--force"],
            capture_output=False,
            timeout=600,
        )
        print()
        if result.returncode == 0:
            print("  [SUCCESS] Auto-fix completed. Re-run verify to confirm.")
        else:
            print("  [FAIL] Auto-fix failed with exit code", result.returncode)
        sys.exit(result.returncode)
    else:
        print()
        print("  Auto-fix: python scripts/setup_env.py --force")
        print("           or: python scripts/verify_env.py --fix")
        sys.exit(1)


if __name__ == "__main__":
    main()
