#!/usr/bin/env python3
"""
腾讯云 API 密钥统一加载模块（复用自 tencentcloud-ocr/env_loader.py）。

环境变量读取优先级（从高到低）：
1. 系统环境变量（os.environ）
2. .env 文件 —— 从脚本所在目录逐级向上查找，找到的第一个生效

用法：
    from env_loader import validate_env
    secret_id, secret_key = validate_env()
"""

import os
import sys

REQUIRED_SECRET_ID = "TENCENTCLOUD_SECRET_ID"
REQUIRED_SECRET_KEY = "TENCENTCLOUD_SECRET_KEY"


def _find_env_file() -> str:
    """从脚本所在目录逐级向上查找 .env 文件，最多向上 5 级。"""
    try:
        current = os.path.dirname(os.path.abspath(__file__))
        for _ in range(5):
            env_path = os.path.join(current, ".env")
            if os.path.isfile(env_path):
                return env_path
            parent = os.path.dirname(current)
            if parent == current:
                break
            current = parent
    except Exception:
        pass
    return ""


def _parse_env_file(path: str) -> dict:
    """解析 .env 文件，返回键值对字典。异常安全。"""
    result = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip()
                if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
                    value = value[1:-1]
                if key:
                    result[key] = value
    except Exception:
        pass
    return result


def _ensure_env_loaded() -> None:
    """将 .env 文件中的变量加载到 os.environ（不覆盖已有系统环境变量）。幂等。"""
    env_path = _find_env_file()
    if not env_path:
        return
    for key, value in _parse_env_file(env_path).items():
        if not os.environ.get(key):
            os.environ[key] = value


def validate_env() -> tuple:
    """校验并返回腾讯云 API 密钥。缺失时打印指引并 sys.exit(1)。返回 (secret_id, secret_key)。"""
    _ensure_env_loaded()

    secret_id = os.environ.get(REQUIRED_SECRET_ID)
    secret_key = os.environ.get(REQUIRED_SECRET_KEY)

    if not secret_id or not secret_key:
        missing = []
        if not secret_id:
            missing.append(REQUIRED_SECRET_ID)
        if not secret_key:
            missing.append(REQUIRED_SECRET_KEY)
        print(
            "错误: 缺少腾讯云 API 密钥\n"
            f"缺失变量: {', '.join(missing)}\n"
            "\n"
            "请通过以下任一方式提供：\n"
            "  方式1 - 在项目根目录创建 .env 文件：\n"
            "    TENCENTCLOUD_SECRET_ID=你的SecretId\n"
            "    TENCENTCLOUD_SECRET_KEY=你的SecretKey\n"
            "  方式2 - 在终端设置环境变量：\n"
            "    export TENCENTCLOUD_SECRET_ID='你的SecretId'\n"
            "    export TENCENTCLOUD_SECRET_KEY='你的SecretKey'\n"
            "密钥获取: https://console.cloud.tencent.com/cam/capi",
            file=sys.stderr,
        )
        sys.exit(1)

    return secret_id, secret_key
