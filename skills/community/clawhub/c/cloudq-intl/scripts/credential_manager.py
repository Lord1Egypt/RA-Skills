#!/usr/bin/env python3
"""凭证管理（国际站：仅 AK/SK 环境变量）

国际站凭证只从环境变量读取 AK/SK。若检测到本地 credential.json
（如其他版本残留），输出忽略提示后照常使用环境变量（防止残留文件遮蔽 AK/SK）。

凭证文件与配置目录仅由 cleanup.py 清理时使用（load/clear 接口保留）。
"""

import json
import os
import sys
from pathlib import Path
from typing import Optional

CONFIG_DIR = Path.home() / ".tencent-cloudq"
CREDENTIAL_FILE = CONFIG_DIR / "credential.json"


class CredentialNotFoundError(Exception):
    """未找到可用凭证（环境变量 AK/SK 未配置）"""


def load_credential() -> Optional[dict]:
    """读取本地凭证文件（仅供残留诊断与 cleanup 清理；国际站运行时不使用）"""
    if not CREDENTIAL_FILE.exists():
        return None
    try:
        data = json.loads(CREDENTIAL_FILE.read_text(encoding="utf-8"))
        if data.get("type") not in ("oauth", "connector"):
            return None
        return data
    except (json.JSONDecodeError, IOError):
        return None


def clear_credential():
    """清除凭证文件（cleanup.py 使用，清理其他版本残留）"""
    if CREDENTIAL_FILE.exists():
        CREDENTIAL_FILE.unlink()


def get_credential() -> dict:
    """获取凭证：国际站仅 AK/SK 环境变量（本地文件凭证一律忽略）

    Returns:
        {"secretId": "...", "secretKey": "...", "token": "...", "source": "env"}

    Raises:
        CredentialNotFoundError: 环境变量未配置
    """
    # 残留文件诊断：中文版等历史凭证不参与鉴权，仅提示
    if load_credential() is not None:
        sys.stderr.write(
            "[cloudq-intl] ignoring local credential file — "
            "the international site supports AK/SK only\n")

    env_id = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
    env_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")
    if env_id and env_key:
        return {
            "secretId": env_id,
            "secretKey": env_key,
            "token": os.environ.get("TENCENTCLOUD_TOKEN", ""),
            "source": "env",
        }
    raise CredentialNotFoundError("NEED_AUTH")
