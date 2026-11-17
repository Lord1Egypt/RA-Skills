#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""install_auth_skill.py

对齐 tp圈人-组合人群-4-1 的鉴权技能安装交互：
- 检测 mingdata-dmp-auth 是否存在
- 允许在用户明确同意后执行自动安装（通过 openclaw 命令）

注意：
- 本脚本只负责“检测/安装尝试/返回结果JSON”。
- 是否安装必须由对话侧在用户回复“是”后再触发执行。
"""

import json
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))


def _find_auth_skill() -> str | None:
    try:
        from find_auth_skill import find_auth_skill_path
        p = find_auth_skill_path()
        return str(p) if p else None
    except Exception:
        return None


def main():
    ap = (sys.argv[1] if len(sys.argv) > 1 else "").strip().lower()
    # ap: "check" | "install"
    if ap not in ("check", "install"):
        print(json.dumps({
            "ok": False,
            "error": "BAD_ARGS",
            "usage": "python3 install_auth_skill.py check|install"
        }, ensure_ascii=False))
        sys.exit(2)

    existing = _find_auth_skill()
    if ap == "check":
        print(json.dumps({
            "ok": True,
            "installed": bool(existing),
            "path": existing
        }, ensure_ascii=False))
        sys.exit(0)

    # install
    if existing:
        print(json.dumps({
            "ok": True,
            "installed": True,
            "already_installed": True,
            "path": existing
        }, ensure_ascii=False))
        sys.exit(0)

    cmd = ["openclaw", "skills", "install", "mingdata-dmp-auth"]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True)
        out = (r.stdout or "").strip()
        err = (r.stderr or "").strip()
        if r.returncode != 0:
            print(json.dumps({
                "ok": False,
                "installed": False,
                "error": "INSTALL_FAILED",
                "returncode": r.returncode,
                "stderr": err[:500],
                "stdout": out[:500],
                "manual_install_url": "https://clawhub.ai/mingri26/mingdata-dmp-auth"
            }, ensure_ascii=False))
            sys.exit(1)

        # re-check
        existing2 = _find_auth_skill()
        print(json.dumps({
            "ok": True,
            "installed": bool(existing2),
            "path": existing2,
            "stdout": out[:500]
        }, ensure_ascii=False))
        sys.exit(0)
    except FileNotFoundError:
        print(json.dumps({
            "ok": False,
            "installed": False,
            "error": "OPENCLAW_NOT_FOUND",
            "message": "未找到openclaw命令，无法自动安装。请使用手动安装入口。",
            "manual_install_url": "https://clawhub.ai/mingri26/mingdata-dmp-auth"
        }, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
