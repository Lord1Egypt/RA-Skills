#!/usr/bin/env python3
"""
verify.py - 沟通三部曲凭证验证
检查本地凭证文件，有效时输出 SKILL.md 内容
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

# 凭证目录（平台下发 skill 包时自带）
LICENSE_DIR = Path.home() / ".openclaw" / "skills" / ".license" / "3steps"
LICENSE_PATH = LICENSE_DIR / "license.json"

# SKILL.md 路径（与 verify.py 同目录）
SKILL_DIR = Path(__file__).parent
SKILL_PATH = SKILL_DIR / "SKILL.md"


def load_credential():
    """加载 license 文件"""
    if not LICENSE_PATH.exists():
        return None
    try:
        with open(LICENSE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def verify_credential(cred):
    """验证凭证是否有效"""
    if cred is None:
        return False, "请先订阅后再使用沟通三部曲"

    if cred.get("status") == "revoked":
        return False, "订阅已失效，请联系续费"

    expires_at = cred.get("expires_at")
    if expires_at:
        current_time = int(datetime.now().timestamp())
        if expires_at < current_time:
            return False, "订阅已过期，请续费"

    subscription_type = cred.get("subscription_type", "")
    if subscription_type not in ["monthly", "yearly", "lifetime"]:
        return False, "订阅类型无效，请重新订阅"

    return True, ""


def read_skill_content():
    """读取 SKILL.md 内容"""
    if not SKILL_PATH.exists():
        return None
    try:
        with open(SKILL_PATH, 'r', encoding='utf-8') as f:
            return f.read()
    except (IOError, OSError):
        return None


def main():
    cred = load_credential()
    valid, msg = verify_credential(cred)

    if valid:
        content = read_skill_content()
        if content:
            print(content)
        else:
            print("❌ SKILL.md 文件不存在")
            print(f"请检查: {SKILL_PATH}")
    else:
        print(f"❌ {msg}")
        print("")
        print("订阅地址：https://clawhub.com")
        print("或联系客服开通")


if __name__ == "__main__":
    main()
