#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cad-file-reader Windows 安装入口（纯 Python，SkillHub 轻量包也可用）。

用法：
  python scripts/setup_win.py            # 安装（转发 scripts/setup.py）
  python scripts/setup_win.py --dry-run  # 只打印平台/依赖清单
功能：py -> python -> python3 探测 Python 3.10+；调 scripts/setup.py；
打印 winget/choco 可选后端指引；不改系统配置，全部依赖写 vendor/。
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
SETUP_PY = SKILL_DIR / "scripts" / "setup.py"

def ensure_utf8():
    sys.path.insert(0, str(SKILL_DIR / "scripts"))
    try:
        import pyboot
        pyboot.ensure_utf8_io()
    except Exception:
        pass

def find_python() -> str:
    pf = os.environ.get("ProgramFiles", r"C:\Program Files")
    cands = [os.environ.get("CAD_PYTHON", ""), "py", "python", "python3",
             str(Path(pf) / "PythonLauncher" / "py.exe")]
    for c in cands:
        if not c:
            continue
        try:
            r = subprocess.run(
                [c, "-c", "import sys;print(1 if sys.version_info>=(3,10) else 0)"],
                capture_output=True, text=True, timeout=30)
            if r.returncode == 0 and r.stdout.strip() == "1":
                return c
        except (OSError, subprocess.SubprocessError):
            continue
    return ""

def print_backend_guide():
    print("\n[可选外部后端指引 - 仅按需安装]")
    print("  1) DWG->DXF 转换：winget install ODA.ODAFileConverter")
    print("     或 choco install oda-file-converter；官方页")
    print("     https://www.opendesign.com/guestfiles/oda_file_converter")
    print("  2) PDF 转图片（矢量层读取）：winget install poppler.poppler")
    print("  3) 扫描/图片 OCR：winget install UB-Mannheim.TesseractOCR")
    print("     或 choco install tesseract（中文需勾选 chi_sim 语言包）")

def main() -> int:
    ensure_utf8()
    python = find_python()
    if not python:
        print("❌ 未找到 Python 3.10+，请从以下地址安装并勾选 Add to PATH：",
              file=sys.stderr)
        print("   https://www.python.org/downloads/windows/", file=sys.stderr)
        return 1
    if not SETUP_PY.is_file():
        print(f"❌ 找不到 {SETUP_PY}，下载包可能不完整。", file=sys.stderr)
        return 1
    cmd = [python, str(SETUP_PY)]
    if "--dry-run" in sys.argv:
        cmd.append("--dry-run")
    env = dict(os.environ)
    env["PYTHONUTF8"] = "1"
    r = subprocess.run(cmd, env=env)
    if r.returncode != 0:
        print(f"❌ scripts/setup.py 失败（错误码 {r.returncode}）。",
              file=sys.stderr)
        return r.returncode
    print_backend_guide()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
