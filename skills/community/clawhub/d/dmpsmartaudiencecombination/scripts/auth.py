#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""auth.py

统一凭证加载模块（零依赖）。
凭证查找优先级：
1. 命令行参数（--ak/--sk/--base-url）
2. 环境变量（DMP_AK / DMP_SK / DMP_BASE_URL）
3. 配置文件 ~/.mingdata_dmp_credentials（JSON格式，与批量打通/批量圈包技能共用）

配置文件格式：
{
  "access_key": "xxx",
  "secret_key": "xxx",
  "base_url": "https://open.mingdata.com"
}
"""

import json
import os
import sys
from pathlib import Path
from typing import Optional, Tuple

CRED_FILE = Path.home() / ".mingdata_dmp_credentials"
DEFAULT_BASE_URL = "https://open.mingdata.com"


def load_credentials(ak: Optional[str] = None, sk: Optional[str] = None,
                     base_url: Optional[str] = None) -> Tuple[str, str, str]:
    """按优先级加载AK/SK/BaseURL，返回(ak, sk, base_url)。
    任何一项找不到则抛出 RuntimeError，并提示配置方法。
    """
    # 1. 命令行参数
    ak = ak or os.environ.get("DMP_AK")
    sk = sk or os.environ.get("DMP_SK")
    base_url = base_url or os.environ.get("DMP_BASE_URL")

    # 2. 配置文件
    if (not ak or not sk) and CRED_FILE.exists():
        try:
            with open(CRED_FILE, "r", encoding="utf-8") as f:
                creds = json.load(f)
            ak = ak or creds.get("access_key")
            sk = sk or creds.get("secret_key")
            base_url = base_url or creds.get("base_url")
        except Exception as e:
            raise RuntimeError(f"凭证文件 {CRED_FILE} 读取失败: {e}") from e

    # 3. base_url 默认值
    base_url = base_url or DEFAULT_BASE_URL

    if not ak or not sk:
        raise RuntimeError(
            f"未找到DMP API凭证。\n"
            f"请使用以下任一方式配置：\n"
            f"  1) 运行配置脚本：python3 {Path(__file__).parent / 'setup_credentials.py'} <AK> <SK>\n"
            f"  2) 设置环境变量：export DMP_AK=xxx DMP_SK=xxx\n"
            f"  3) 手动创建 {CRED_FILE}，格式：{{\"access_key\":\"xxx\",\"secret_key\":\"xxx\",\"base_url\":\"{DEFAULT_BASE_URL}\"}}\n"
            f"\n凭证申请请参考 references/凭证获取指南.md"
        )

    return ak, sk, base_url


def add_auth_args(parser):
    """给argparse添加通用鉴权参数（均为可选，因为会自动从配置文件加载）"""
    parser.add_argument("--ak", default=None, help="Access Key（可选，默认从 ~/.mingdata_dmp_credentials 读取）")
    parser.add_argument("--sk", default=None, help="Secret Key（可选，默认从凭证文件读取）")
    parser.add_argument("--base-url", default=None, help="API base_url（可选，默认生产环境）")
