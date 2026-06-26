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

import json
import os
from pathlib import Path


ENV_KEY = "AIDSO_GEO_API_KEY"
ENV_FILE = Path(__file__).resolve().parent / ".env"


def print_json(data: dict):
    print(json.dumps(data, ensure_ascii=False))


def load_env_file() -> dict:
    """
    读取当前 skill 目录下的 .env 文件
    """
    result = {}

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


def main():
    """
    检查 API Key 是否存在。
    优先级：
    1. 系统环境变量 AIDSO_GEO_API_KEY
    2. 当前 skill 目录下 .env 文件中的 AIDSO_GEO_API_KEY
    """

    # 1. 优先检查系统环境变量
    api_key = os.getenv(ENV_KEY)

    if api_key:
        print_json({
            "ok": True,
            "source": "environment",
            "env_key": ENV_KEY,
            "msg": "API Key exists"
        })
        return

    # 2. 检查当前 skill 目录下的 .env
    env_data = load_env_file()
    api_key = env_data.get(ENV_KEY)

    if api_key:
        print_json({
            "ok": True,
            "source": ".env",
            "env_key": ENV_KEY,
            "msg": "API Key exists"
        })
        return

    # 3. 不存在，提示需要绑定
    print_json({
        "ok": False,
        "need_bind_api_key": True,
        "env_key": ENV_KEY,
        "msg": "还没有绑定 API Key，请先发送：绑定 api-key：你的_api_key"
    })


if __name__ == "__main__":
    main()




