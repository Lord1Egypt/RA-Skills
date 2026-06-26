#!/usr/bin/env python3
"""配置状态检查命令 — CLI 入口（无 service 层，逻辑足够简单）"""

COMMAND_NAME = "check"
COMMAND_DESC = "检查配置状态"

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from pathlib import Path
from _auth import get_ak_from_env
from _output import print_output
from _const import SKILL_NAME

def check_status() -> dict:
    lines = []
    ok = True

    # 1. AK（由 OpenClaw 注入到环境变量）
    ak_id, _ = get_ak_from_env()
    if ak_id:
        masked = f"{ak_id[:4]}****{ak_id[-4:]}" if len(ak_id) >= 8 else "****"
        lines.append(f"✅ AK 已配置: {masked}")
        ak_ok = True
    else:
        lines.append("❌ AK 未配置 — 运行: `cli.py configure YOUR_AK`")
        ak_ok = False
        ok = False

    status_icon = "✅ 一切正常" if ok else "⚠️  有问题需处理"
    markdown = ("##" + SKILL_NAME + "状态检查\n\n"
                + "\n".join(f"- {l}" for l in lines)
                + f"\n\n**{status_icon}**")

    return {
        "success": ok,
        "markdown": markdown,
        "data": {
            "ak_configured": ak_ok
        },
    }


def main():
    result = check_status()
    print_output(result["success"], result["markdown"], result["data"])


if __name__ == "__main__":
    main()
