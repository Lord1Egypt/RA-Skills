#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""setup_credentials.py

明日DMP API凭证配置脚本。
保存 Access Key / Secret Key / base_url 到本地配置文件 ~/.mingdata_dmp_credentials
（与批量打通圈包/批量圈包/人群投放等技能共用同一凭证文件）。

用法：
    python3 setup_credentials.py <ACCESS_KEY> <SECRET_KEY> [BASE_URL]

默认 BASE_URL: https://open.mingdata.com（生产环境）
"""

import json
import os
import sys
from pathlib import Path

CRED_FILE = Path.home() / ".mingdata_dmp_credentials"
DEFAULT_BASE_URL = "https://open.mingdata.com"


def main():
    if len(sys.argv) < 3:
        print("用法: python3 setup_credentials.py <ACCESS_KEY> <SECRET_KEY> [BASE_URL]")
        print(f"  BASE_URL 默认: {DEFAULT_BASE_URL}（生产环境）")
        print(f"  测试环境: https://dmp-dev.mingdata.com")
        sys.exit(1)

    access_key = sys.argv[1].strip()
    secret_key = sys.argv[2].strip()
    base_url = sys.argv[3].strip() if len(sys.argv) > 3 else DEFAULT_BASE_URL

    if not access_key or not secret_key:
        print("[ERROR] AK/SK 不能为空")
        sys.exit(1)

    credentials = {
        "access_key": access_key,
        "secret_key": secret_key,
        "base_url": base_url,
    }

    try:
        CRED_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CRED_FILE, "w", encoding="utf-8") as f:
            json.dump(credentials, f, indent=2, ensure_ascii=False)
        os.chmod(CRED_FILE, 0o600)
        print(f"[SUCCESS] 凭证已保存到 {CRED_FILE}")
        print(f"  base_url: {base_url}")
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] 保存凭证失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
