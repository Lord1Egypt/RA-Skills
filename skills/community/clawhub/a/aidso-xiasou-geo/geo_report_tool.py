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
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests


ENV_KEY = "AIDSO_GEO_API_KEY"
ENV_FILE = Path(__file__).resolve().parent / ".env"

GET_QUESTIONS_URL = "https://api.aidso.com/openapi/skills/get_questions"
REPORT_URL = "https://api.aidso.com/openapi/skills/band_report/md/v2"


def print_json(data: Dict[str, Any]) -> None:
    """
    统一 JSON 输出，避免中文被转义。
    """
    print(json.dumps(data, ensure_ascii=False))


def load_env_file() -> Dict[str, str]:
    """
    读取当前 skill 目录下的 .env 文件。

    示例：
    AIDSO_GEO_API_KEY=xxx
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


def get_api_key() -> Tuple[Optional[str], Optional[str]]:
    """
    获取 API Key。

    优先级：
    1. 系统环境变量 AIDSO_GEO_API_KEY
    2. 当前 skill 目录下 .env 文件中的 AIDSO_GEO_API_KEY

    返回：
    api_key, source
    """
    api_key = os.getenv(ENV_KEY)

    if api_key:
        return api_key.strip(), "environment"

    env_data = load_env_file()
    api_key = env_data.get(ENV_KEY)

    if api_key:
        return api_key.strip(), ".env"

    return None, None



def request_post(
    url: str,
    api_key: str,
    payload: Dict[str, Any],
    timeout: int = 60,
) -> Dict[str, Any]:
    """
    统一 POST 请求。
    """
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            timeout=timeout,
        )

        try:
            data = response.json()
        except Exception:
            return {
                "code": -1,
                "msg": "response is not json",
                "data": response.text,
                "http_status": response.status_code,
            }

        if response.status_code < 200 or response.status_code >= 300:
            return {
                "code": -1,
                "msg": "http status error",
                "data": data,
                "http_status": response.status_code,
            }

        return data

    except requests.Timeout:
        return {
            "code": -1,
            "msg": "request timeout",
            "data": None,
        }

    except requests.RequestException as e:
        return {
            "code": -1,
            "msg": f"request error: {e}",
            "data": None,
        }


def normalize_questions(data: Any) -> List[str]:
    """
    将接口返回的问题数据统一转为 List[str]。

    兼容几种情况：
    1. data 本身就是 list
    2. data 是 JSON 字符串
    3. data 是 dict，里面包含 questions
    4. data 是单个字符串
    """
    questions: Any = data

    if isinstance(questions, dict):
        for key in ("questions", "list", "items", "data"):
            if key in questions:
                questions = questions.get(key)
                break

    if isinstance(questions, str):
        text = questions.strip()

        if not text:
            return []

        try:
            parsed = json.loads(text)
            questions = parsed
        except Exception:
            questions = [text]

    if isinstance(questions, dict):
        for key in ("questions", "list", "items", "data"):
            if key in questions:
                questions = questions.get(key)
                break

    if not isinstance(questions, list):
        return []

    result: List[str] = []

    for item in questions:
        if isinstance(item, dict):
            value = (
                item.get("question")
                or item.get("content")
                or item.get("text")
                or item.get("title")
            )
            if value:
                result.append(str(value).strip())
        else:
            value = str(item).strip()
            if value:
                result.append(value)

    return [q for q in result if q]


def get_questions(brand_name: str) -> Dict[str, Any]:
    """
    根据品牌名称获取问题列表。
    """
    brand_name = brand_name.strip()

    if not brand_name:
        return {
            "ok": False,
            "msg": "brand_name 不能为空",
        }

    api_key, source = get_api_key()

    if not api_key:
        return {
            "ok": False,
            "need_bind_api_key": True,
            "env_key": ENV_KEY,
            "msg": "还没有绑定 API Key，请先发送：绑定 api-key：你的_api_key",
        }

    payload = {
        "brand_name": brand_name,
    }

    raw_result = request_post(
        url=GET_QUESTIONS_URL,
        api_key=api_key,
        payload=payload,
        timeout=60,
    )

    if raw_result.get("code") != 200:
        return {
            "ok": False,
            "msg": "获取问题列表失败",
            "brand_name": brand_name,
            "raw": raw_result,
        }

    questions = normalize_questions(raw_result.get("data"))

    if not questions:
        return {
            "ok": False,
            "msg": "暂未获取到可用的问题列表，请更换品牌名称后重试",
            "brand_name": brand_name,
            "raw": raw_result,
        }

    return {
        "ok": True,
        "msg": "success",
        "brand_name": brand_name,
        "questions": questions,
        "api_key_source": source,
    }


def normalize_questions_json(questions_json: str) -> List[str]:
    """
    解析命令行传入的问题 JSON 数组。
    """
    try:
        questions = json.loads(questions_json)
    except Exception as e:
        raise ValueError(f"questions-json 不是合法 JSON: {e}")

    if not isinstance(questions, list):
        raise ValueError("questions-json 必须是 JSON 数组")

    result: List[str] = []

    for item in questions:
        value = str(item).strip()
        if value:
            result.append(value)

    if not result:
        raise ValueError("questions-json 不能为空数组")

    return result


def call_report_api(brand_name: str, questions: List[str]) -> Dict[str, Any]:
    """
    单次调用报告生成接口。
    """
    api_key, source = get_api_key()

    if not api_key:
        return {
            "ok": False,
            "need_bind_api_key": True,
            "env_key": ENV_KEY,
            "msg": "还没有绑定 API Key，请先发送：绑定 api-key：你的_api_key",
        }

    payload = {
        "brand_name": brand_name,
        "questions": questions,
    }

    result = request_post(
        url=REPORT_URL,
        api_key=api_key,
        payload=payload,
        timeout=120,
    )

    result["_api_key_source"] = source
    return result


def is_report_success(result: Dict[str, Any]) -> bool:
    """
    判断报告是否生成成功。
    """
    return (
        result.get("code") == 200
        and result.get("msg") == "success"
        and isinstance(result.get("data"), str)
        and result.get("data", "").startswith("http")
    )


def is_report_processing(result: Dict[str, Any]) -> bool:
    """
    判断报告是否仍在处理中。
    """
    return (
        result.get("code") == 200
        and "处理中" in str(result.get("msg", ""))
    )


def generate_report(
    brand_name: str,
    questions: List[str],
    poll_interval: int = 120,
    max_poll_times: int = 6,
) -> Dict[str, Any]:

    brand_name = brand_name.strip()

    if not brand_name:
        return {
            "ok": False,
            "msg": "brand_name 不能为空",
        }

    if not questions:
        return {
            "ok": False,
            "msg": "questions 不能为空",
        }

    if poll_interval <= 0:
        poll_interval = 120

    if max_poll_times <= 0:
        max_poll_times = 6

    last_result: Optional[Dict[str, Any]] = None
    task_id: Optional[str] = None
    api_key_source: Optional[str] = None

    for index in range(1, max_poll_times + 1):
        result = call_report_api(brand_name, questions)
        last_result = result

        if result.get("ok") is False and result.get("need_bind_api_key"):
            return result

        api_key_source = result.get("_api_key_source")

        if is_report_success(result):
            return {
                "ok": True,
                "msg": "success",
                "brand_name": brand_name,
                "report_url": result.get("data"),
                "poll_times": index,
                "api_key_source": api_key_source,
            }

        if is_report_processing(result):
            if isinstance(result.get("data"), str):
                task_id = result.get("data")

            if index < max_poll_times:
                time.sleep(poll_interval)

            continue

        return {
            "ok": False,
            "msg": "报告生成失败",
            "brand_name": brand_name,
            "raw": result,
        }

    return {
        "ok": False,
        "msg": "报告仍在处理中，请稍后重新生成或检查任务状态",
        "brand_name": brand_name,
        "task_id": task_id,
        "poll_times": max_poll_times,
        "raw": last_result,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="AIDSO GEO Report Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    questions_parser = subparsers.add_parser(
        "questions",
        help="根据品牌名称获取 GEO 诊断问题列表",
    )
    questions_parser.add_argument(
        "--brand-name",
        required=True,
        help="品牌名称，例如 VIVO",
    )

    report_parser = subparsers.add_parser(
        "report",
        help="根据品牌名称和问题列表生成 GEO 品牌诊断报告",
    )
    report_parser.add_argument(
        "--brand-name",
        required=True,
        help="品牌名称，例如 VIVO",
    )
    report_parser.add_argument(
        "--questions-json",
        required=True,
        help='问题 JSON 数组，例如：["问题1","问题2"]',
    )
    report_parser.add_argument(
        "--poll-interval",
        type=int,
        default=120,
        help="轮询间隔秒数，默认 120 秒",
    )
    report_parser.add_argument(
        "--max-poll-times",
        type=int,
        default=6,
        help="最大轮询次数，默认 6 次",
    )

    args = parser.parse_args()

    if args.command == "questions":
        result = get_questions(args.brand_name)
        print_json(result)

        if not result.get("ok"):
            sys.exit(1)

        return

    if args.command == "report":
        try:
            questions = normalize_questions_json(args.questions_json)
        except ValueError as e:
            print_json({
                "ok": False,
                "msg": str(e),
            })
            sys.exit(1)

        result = generate_report(
            brand_name=args.brand_name,
            questions=questions,
            poll_interval=args.poll_interval,
            max_poll_times=args.max_poll_times,
        )

        print_json(result)

        if not result.get("ok"):
            sys.exit(1)

        return


if __name__ == "__main__":
    main()