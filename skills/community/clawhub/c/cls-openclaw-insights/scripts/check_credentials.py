#!/usr/bin/env python3
"""
凭证检查脚本 - 检查 TCCLI 安装状态和临时密钥是否可用

检查项目：
1. TCCLI 是否已安装
2. TCCLI 凭证是否存在
3. 凭证格式是否正确（包含必需字段）
4. 临时密钥是否已过期

仅输出配置状态，不会输出任何密钥内容，避免泄漏风险。

退出码：
  0 - 凭证已配置且有效
  1 - TCCLI 未安装
  2 - 凭证文件不存在（需要执行 tccli auth login）
  3 - 凭证文件格式错误或缺少必需字段
  4 - 临时密钥已过期（需要重新执行 tccli auth login）
"""

import os
import sys
import json
import time
import shutil
from datetime import datetime


TCCLI_CREDENTIAL_PATH = os.path.expanduser("~/.tccli/default.credential")


def check_tccli_installed() -> bool:
    """检查 TCCLI 是否已安装"""
    return shutil.which("tccli") is not None


def check_credentials():
    """检查 TCCLI 安装状态和凭证配置，输出状态摘要"""

    # 1. 检查 TCCLI 是否安装
    if not check_tccli_installed():
        print("❌ TCCLI 未安装")
        print("")
        print("请先安装 TCCLI:")
        print("  pip install tccli")
        print("")
        print("安装后执行授权登录:")
        print("  tccli auth login")
        return 1

    print("✅ TCCLI 已安装")

    # 2. 检查凭证文件是否存在
    if not os.path.exists(TCCLI_CREDENTIAL_PATH):
        print("❌ TCCLI 凭证不存在")
        print("")
        print("请执行授权登录获取临时密钥:")
        print("  tccli auth login")
        return 2

    # 3. 读取并验证凭证文件
    try:
        with open(TCCLI_CREDENTIAL_PATH, "r", encoding="utf-8") as f:
            cred_data = json.load(f)
    except json.JSONDecodeError:
        print("❌ TCCLI 凭证格式错误")
        print("")
        print("请重新执行授权登录:")
        print("  tccli auth login")
        return 3
    except PermissionError:
        print("❌ 无权限读取 TCCLI 凭证")
        return 3

    # 检查必需字段
    secret_id = cred_data.get("secretId", "").strip()
    secret_key = cred_data.get("secretKey", "").strip()
    token = cred_data.get("token", "").strip()
    cred_type = cred_data.get("type", "unknown")

    if not secret_id or not secret_key:
        print(f"❌ 凭证文件中缺少 secretId 或 secretKey")
        print("")
        print("请重新执行授权登录:")
        print("  tccli auth login")
        return 3

    # 4. 检查密钥过期时间
    expires_at = cred_data.get("expiresAt")
    if expires_at and isinstance(expires_at, (int, float)):
        now = time.time()
        if now > expires_at:
            expire_time_str = datetime.fromtimestamp(expires_at).strftime("%Y-%m-%d %H:%M:%S")
            print(f"❌ 临时密钥已过期（过期时间: {expire_time_str}）")
            print("")
            print("请重新执行授权登录:")
            print("  tccli auth login")
            return 4

        # 计算剩余有效时间
        remaining = expires_at - now
        hours = int(remaining // 3600)
        minutes = int((remaining % 3600) // 60)
        expire_time_str = datetime.fromtimestamp(expires_at).strftime("%Y-%m-%d %H:%M:%S")
        remaining_str = f"{hours}小时{minutes}分钟" if hours > 0 else f"{minutes}分钟"

        print("✅ 腾讯云临时密钥已配置且有效")
        print(f"   凭证类型:       {cred_type}")
        print(f"   SecretId:       已设置")
        print(f"   SecretKey:      已设置")
        print(f"   Token:          {'已设置' if token else '未设置'}")
        print(f"   过期时间:       {expire_time_str}")
        print(f"   剩余有效时间:   {remaining_str}")
    else:
        # 没有过期时间信息，可能是永久密钥
        print("✅ 腾讯云 API 密钥已配置")
        print(f"   凭证类型:       {cred_type}")
        print(f"   SecretId:       已设置")
        print(f"   SecretKey:      已设置")
        print(f"   Token:          {'已设置' if token else '未设置'}")

    return 0


if __name__ == "__main__":
    sys.exit(check_credentials())
