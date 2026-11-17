#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""跨平台安装器（cad-file-reader）。

用途
----
- 检测 Python（3.10+）与当前平台；
- 默认用 ``pip --target vendor`` 到技能目录的 ``vendor/`` 安装
  ezdwg / ezdxf / fonttools / pyparsing / numpy（不污染系统环境）；
- 安装后做一次 import 校验；
- 保留既有 ``CAD_FILE_READER_REPO`` 回退：macOS/Linux 上配置了该环境
  变量时优先交给 ``scripts/install_vendor.sh``（GitHub Release 校验下载），
  失败回退公共 PyPI；Windows 未实现 Release 下载，直接公共 PyPI 并给出提示；
- ``--dry-run`` 只打印平台检测与依赖清单，不做任何安装/写文件。

三平台说明
----------
- macOS / Linux：setup.py 纯 Python，支持 ``python3 scripts/setup.py``。
- Windows：先用 ``setup_windows.ps1`` 找到 ``py``/``python`` 再调用本脚本。
- 不修改系统级配置；全部写进技能目录下的 vendor/.env。
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = SKILL_DIR / "scripts"
VENDOR_DIR = SKILL_DIR / "vendor"
MIN_PY = (3, 10)
PIP_PACKAGES = [
    "ezdwg==0.12.6",
    "ezdxf==1.4.4",
    "fonttools",
    "pyparsing",
    "numpy",
]
CORE_PACKAGES = ("ezdwg", "ezdxf", "fontTools")  # import 校验必查


def find_python_interpreter() -> str:
    """找 Python：CAD_PYTHON > codex runtime > PATH python3/py。"""
    sys.path.insert(0, str(SCRIPTS_DIR))
    try:
        import pyboot
        found = pyboot.find_python()
    except Exception:
        found = None

    cache = Path.home() / ".cache" / "codex-runtimes"
    candidates: list[str] = [os.environ.get("CAD_PYTHON", "")]
    if cache.is_dir():
        candidates += sorted(str(p) for p in cache.glob("*/dependencies/python/bin/python3"))
    if found:
        candidates.append(found)
    for c in candidates:
        if c and Path(c).is_file() and os.access(c, os.X_OK):
            return c
    return sys.executable or "python"


def _import_check(dest: Path, interpreter: str) -> bool:
    code = (
        "import importlib.util as u\n"
        "mods = ['ezdwg','ezdxf','fontTools','pyparsing','numpy']\n"
        "ok = all(u.find_spec(m) is not None for m in mods)\n"
        "print('import_ok=' + str(ok))\n"
    )
    env = dict(os.environ)
    env["PYTHONPATH"] = str(dest) + os.pathsep + env.get("PYTHONPATH", "")
    env["PYTHONUTF8"] = "1"
    proc = subprocess.run([interpreter, "-c", code], env=env, capture_output=True, text=True, timeout=120)
    return "import_ok=True" in proc.stdout


def _vendor_ok(dest: Path) -> bool:
    if not dest.is_dir():
        return False
    return all((dest / pkg).is_dir() for pkg in CORE_PACKAGES)


def _pip_install(dest: Path, interpreter: str, quiet: bool = False) -> bool:
    dest.mkdir(parents=True, exist_ok=True)
    cmd = [interpreter, "-m", "pip", "install", "--disable-pip-version-check",
           "--no-input", "--target", str(dest)] + PIP_PACKAGES
    if not quiet:
        print("运行：", " ".join(cmd))
    try:
        subprocess.run(cmd, check=True, timeout=1200)
    except (subprocess.CalledProcessError, OSError) as exc:
        print(f"❌ pip 安装失败：{exc}", file=sys.stderr)
        return False
    return True


def _release_repo_fallback(dest: Path) -> bool:
    """CAD_FILE_READER_REPO 回退（macOS/Linux 复用 install_vendor.sh）。"""
    repo = os.environ.get("CAD_FILE_READER_REPO", "").strip()
    if not repo:
        return False
    if os.name == "nt":
        print("⚠️  Windows 暂不实现 GitHub Release 完整包下载，改走公共 PyPI（可由官方下载页手动补齐 vendor）。")
        return False
    install_sh = SCRIPTS_DIR / "install_vendor.sh"
    if not install_sh.is_file():
        return False
    print(f"检测到 CAD_FILE_READER_REPO={repo} → 优先用 install_vendor.sh（Release 校验下载）。")
    try:
        subprocess.run(["bash", str(install_sh)], check=True, timeout=1800)
        return _vendor_ok(dest)
    except (subprocess.CalledProcessError, OSError) as exc:
        print(f"⚠️  Release 回退失败（{exc}），回退公共 PyPI。")
        return False


def _py_version(interpreter: str) -> str:
    try:
        proc = subprocess.run([interpreter, "-c",
                               "import sys; print(sys.version.split()[0])"],
                              capture_output=True, text=True, timeout=30)
        return proc.stdout.strip() or "?"
    except (OSError, subprocess.SubprocessError):
        return "?"


def dry_run():
    interpreter = find_python_interpreter()
    print(f"platform.os = {os.name}")
    print(f"python = {interpreter}")
    print(f"python.version = {_py_version(interpreter)}")
    print(f"vendor_dir = {VENDOR_DIR}")
    print(f"vendor_present = {_vendor_ok(VENDOR_DIR)}")
    print(f"CAD_FILE_READER_REPO = {os.environ.get('CAD_FILE_READER_REPO', '') or '(未设置)'}")
    print("packages = " + ", ".join(PIP_PACKAGES))
    print("mode = pip --target vendor（REPO 配置后优先 install_vendor.sh 回退）")


def main() -> int:
    import pyboot
    pyboot.ensure_utf8_io()
    ap = argparse.ArgumentParser(description="cad-file-reader 跨平台安装器")
    ap.add_argument("--dry-run", action="store_true", help="只打印平台检测与依赖清单")
    ap.add_argument("--force", action="store_true", help="强制重装 vendor")
    ap.add_argument("--quiet", action="store_true", help="减少输出")
    args = ap.parse_args()

    if args.dry_run:
        dry_run()
        return 0

    interpreter = find_python_interpreter()
    proc = subprocess.run(
        [interpreter, "-c", "import sys; print(1 if sys.version_info>=(3,10) else 0)"],
        capture_output=True, text=True, timeout=30)
    if proc.stdout.strip() != "1":
        print(f"❌ 需要 Python 3.10+（当前使用 {interpreter} {proc.stdout.strip() or proc.stderr.strip()}）。", file=sys.stderr)
        return 1

    needs_install = not _vendor_ok(VENDOR_DIR) or args.force
    if not needs_install:
        if not args.quiet:
            print("vendor 已存在且完整，跳过安装（强制重装：--force 或 CAD_FORCE_INSTALL=1）。")
    else:
        if not args.quiet:
            print("1/3 准备 vendor …")
        if not _release_repo_fallback(VENDOR_DIR):
            if _pip_install(VENDOR_DIR, interpreter, args.quiet)\
               and _import_check(VENDOR_DIR, interpreter):
                if not args.quiet:
                    print(f"vendor 已安装到 {VENDOR_DIR}（公共 PyPI）。")
            else:
                print("❌ vendor 安装后 import 校验未通过，请手动检查。", file=sys.stderr)
                return 1
        elif not args.quiet:
            print("vendor 已由 GitHub Release 完整包补齐。")

    env_file = SKILL_DIR / ".env"
    if not env_file.exists() or "PYTHONPATH=" not in env_file.read_text(encoding="utf-8", errors="ignore"):
        env_file.write_text(
            f"# 由 scripts/setup.py 生成；供未走 run_cad 自举的手工调用使用\n"
            f'PYTHONPATH="{VENDOR_DIR}"\n',
            encoding="utf-8")
        if not args.quiet:
            print(f"2/3 已生成 {env_file}")

    if not args.quiet:
        print("3/3 Python import 校验：", "通过 ✓" if _import_check(VENDOR_DIR, interpreter) else "需复核")
        print("✅ 安装完成。示例：scripts/demo.sh（macOS/Linux）、scripts/demo.cmd（Windows）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
