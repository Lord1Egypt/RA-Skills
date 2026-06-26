#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2026 Beijing Aisou Quanyu (Beijing) Technology Co., Ltd. and/or its affiliates.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import requests


ENV_KEY = "AIDSO_GEO_API_KEY"
ENV_FILE = Path(__file__).resolve().parent / ".env"

BIND_URL = "https://api.aidso.com/openapi/skills/save_content/md"


def print_json(data: Dict[str, Any]) -> None:
    print(json.dumps(data, ensure_ascii=False))


def mask_key(api_key: str) -> str:
    """
    API Key 脱敏展示，避免日志泄露。
    """
    if not api_key:
        return ""

    if len(api_key) <= 8:
        return "*" * len(api_key)

    return api_key[:4] + "*" * (len(api_key) - 8) + api_key[-4:]


def load_env_file() -> Dict[str, str]:
    """
    读取当前 skill 目录下的 .env 文件。
    """
    result: Dict[str, str] = {}

    if not ENV_FILE.exists():
        return result

    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if not line:
            continue

        if line.startswith("#"):
            continue

        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        result[key.strip()] = value.strip().strip('"').strip("'")

    return result


def save_env_value(key: str, value: str) -> None:
    """
    写入当前 skill 目录下的 .env 文件。
    已存在同名 key 时覆盖。
    """
    env_data = load_env_file()
    env_data[key] = value

    content = "\n".join(f"{k}={v}" for k, v in env_data.items()) + "\n"
    ENV_FILE.write_text(content, encoding="utf-8")


def get_existing_api_key() -> Tuple[Optional[str], Optional[str]]:
    """
    获取已存在的 API Key。

    优先级：
    1. 系统环境变量 AIDSO_GEO_API_KEY
    2. 当前 skill 目录下 .env 文件
    """
    api_key = os.getenv(ENV_KEY)
    if api_key:
        return api_key.strip(), "environment"

    env_data = load_env_file()
    api_key = env_data.get(ENV_KEY)

    if api_key:
        return api_key.strip(), ".env"

    return None, None


def request_bind_check(api_key: str) -> Dict[str, Any]:
    """
    调用绑定校验接口。
    """
    payload = {
        "content": api_key,
        "brand_name": api_key,
    }

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            BIND_URL,
            headers=headers,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            timeout=30,
        )

        try:
            return response.json()
        except Exception:
            return {
                "code": -1,
                "msg": "response is not json",
                "data": response.text,
                "http_status": response.status_code,
            }

    except requests.RequestException as e:
        return {
            "code": -1,
            "msg": f"request error: {e}",
            "data": None,
        }


def is_bind_success(result: Dict[str, Any]) -> bool:
    """
    判断接口返回是否为绑定成功。
    只有下面这种结构才算成功：

    {
        "code": 200,
        "msg": "success",
        "data": true
    }
    """
    return (
        result.get("code") == 200
        and result.get("msg") == "success"
        and result.get("data") is True
    )


def bind_api_key(api_key: str, force: bool = False) -> Dict[str, Any]:
    """
    绑定 API Key。
    """
    api_key = api_key.strip()

    if not api_key:
        return {
            "ok": False,
            "msg": "api-key 不能为空",
        }

    existing_key, source = get_existing_api_key()

    if existing_key and not force:
        return {
            "ok": True,
            "already_exists": True,
            "source": source,
            "env_key": ENV_KEY,
            "api_key": mask_key(existing_key),
            "msg": "API Key 已存在，无需重复绑定。如需覆盖，请使用 --force",
        }

    check_result = request_bind_check(api_key)

    if not is_bind_success(check_result):
        return {
            "ok": False,
            "msg": "API Key 校验失败",
            "api_key": mask_key(api_key),
            "raw": check_result,
        }

    save_env_value(ENV_KEY, api_key)

    return {
        "ok": True,
        "already_exists": False,
        "source": ".env",
        "env_file": str(ENV_FILE),
        "env_key": ENV_KEY,
        "api_key": mask_key(api_key),
        "msg": "API Key 绑定成功",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Bind AIDSO GEO API Key")
    parser.add_argument(
        "--api-key",
        required=True,
        help="AIDSO API Key",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="如果已经存在 API Key，是否强制覆盖",
    )

    args = parser.parse_args()

    result = bind_api_key(
        api_key=args.api_key,
        force=args.force,
    )

    print_json(result)

    if not result.get("ok"):
        sys.exit(1)


if __name__ == "__main__":
    main()