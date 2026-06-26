# -*- coding: utf-8 -*-
# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd. and/or its affiliates.
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

"""
asr_standard.py — 火山引擎 BigModel ASR 标准版（录音文件识别）。

异步 submit + poll 模式，支持 ≤5 小时音频。
参考: auc_http_demo.py (submit_task → query_task → result)
鉴权: 新版控制台 API Key 方案 https://www.volcengine.com/docs/6561/2119699

用法:
  # URL 识别（最常用）
  python3 asr_standard.py --url "https://example.com/audio.mp3"

  # 本地文件识别
  python3 asr_standard.py --file "/path/to/long_audio.wav"

  # 仅提交任务（不轮询）
  python3 asr_standard.py --url "https://..." --no-poll

  # 查询已有任务
  python3 asr_standard.py --query-task-id <TASK_ID> --query-logid <X_TT_LOGID>
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
import uuid

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

from api_key import get_speech_api_key

# ============================================================
# 端点与资源 ID 配置
# ============================================================
ASR_STANDARD_SUBMIT_URL = os.getenv(
    "MODEL_SPEECH_ASR_STANDARD_SUBMIT_URL",
    "https://openspeech.bytedance.com/api/v3/auc/bigmodel/submit",
)
ASR_STANDARD_QUERY_URL = os.getenv(
    "MODEL_SPEECH_ASR_STANDARD_QUERY_URL",
    "https://openspeech.bytedance.com/api/v3/auc/bigmodel/query",
)
ASR_STANDARD_RESOURCE_ID = os.getenv(
    "MODEL_SPEECH_ASR_STANDARD_RESOURCE_ID", "volc.bigasr.auc"
)

# 轮询参数
DEFAULT_POLL_INTERVAL = 3       # 秒
DEFAULT_POLL_MAX_TIME = 10800   # 3 小时

# 标准版最大支持时长
STANDARD_MAX_SECONDS = 5 * 60 * 60  # 5 小时


def log(msg: str) -> None:
    print(f"[byted-asr-standard] {msg}", file=sys.stderr)


def fail_json(error_code: str, message: str, **extra) -> None:
    """输出 JSON 格式的错误并退出。"""
    payload = {"error": error_code, "message": message}
    payload.update(extra)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    sys.exit(1)


try:
    import requests
except ImportError:
    fail_json("MISSING_DEPENDENCY", "requests 库未安装，请执行 pip install requests")


# ============================================================
# 鉴权 Header 构建
# ============================================================
def _build_headers(appid: str | None = None, token: str | None = None) -> dict:
    """
    构建标准版请求头。

    鉴权方式（与极速版 asr_flash.go 保持一致）:
      - 新版控制台: X-Api-Key
      - 旧版: X-Api-App-Key + X-Api-Access-Key
    """
    app_id = appid or os.getenv("MODEL_SPEECH_APP_ID", "").strip()
    api_key = token or get_speech_api_key().strip()

    if not api_key:
        fail_json(
            "CREDENTIALS_NOT_CONFIGURED",
            "MODEL_SPEECH_API_KEY 需在环境变量中配置。"
            "见 https://www.volcengine.com/docs/6561/2119699",
            missing_credentials=["MODEL_SPEECH_API_KEY"],
        )

    headers = {
        "X-Api-Resource-Id": ASR_STANDARD_RESOURCE_ID,
        "X-Api-Request-Id": str(uuid.uuid4()),
        "X-Api-Sequence": "-1",
    }

    if app_id:
        headers["X-Api-App-Key"] = app_id
        headers["X-Api-Access-Key"] = api_key
    else:
        headers["X-Api-Key"] = api_key

    return headers


# ============================================================
# 文件 → Base64
# ============================================================
def file_to_base64(file_path: str) -> str:
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


# ============================================================
# Submit Task
# ============================================================
def submit_task(
    audio_url: str | None = None,
    file_path: str | None = None,
    appid: str | None = None,
    token: str | None = None,
    language: str | None = None,
) -> dict:
    """
    向火山标准版提交识别任务。

    Args:
        audio_url: 音频 URL（与 file_path 二选一）。
        file_path: 本地文件路径（会 base64 上传）。
        appid: App ID (可选)。
        token: API Key (可选)。
        language: 语言代码 (可选)。

    Returns:
        {"task_id": str, "x_tt_logid": str}
    """
    headers = _build_headers(appid=appid, token=token)
    task_id = headers["X-Api-Request-Id"]

    audio_payload: dict = {}
    if audio_url:
        audio_payload["url"] = audio_url
    elif file_path:
        if not os.path.isfile(file_path):
            fail_json("FILE_NOT_FOUND", f"音频文件不存在: {file_path}")
        if os.path.getsize(file_path) == 0:
            fail_json("FILE_EMPTY", f"音频文件为空: {file_path}")
        audio_payload["data"] = file_to_base64(file_path)
    else:
        fail_json("NO_INPUT", "必须提供 --url 或 --file")

    if language:
        audio_payload["language"] = language

    request_body = {
        "user": {"uid": headers.get("X-Api-App-Key", "skill_asr_user")},
        "audio": audio_payload,
        "request": {
            "model_name": "bigmodel",
            "enable_itn": True,
            "enable_punc": True,
            "show_utterances": True,
        },
    }

    log(f"正在提交标准版识别任务: task_id={task_id}")
    try:
        resp = requests.post(
            ASR_STANDARD_SUBMIT_URL,
            data=json.dumps(request_body),
            headers=headers,
            timeout=60,
        )
    except requests.RequestException as e:
        fail_json("NETWORK_ERROR", f"提交请求网络异常: {e}")

    resp_status = resp.headers.get("X-Api-Status-Code", "")
    x_tt_logid = resp.headers.get("X-Tt-Logid", "")

    if resp_status != "20000000":
        msg = resp.headers.get("X-Api-Message", "未知错误")
        fail_json(
            "SUBMIT_FAILED",
            f"标准版任务提交失败: code={resp_status}, msg={msg}",
            task_id=task_id,
            logid=x_tt_logid,
        )

    log(f"任务已提交: task_id={task_id}, logid={x_tt_logid}")
    return {"task_id": task_id, "x_tt_logid": x_tt_logid}


# ============================================================
# Query Task
# ============================================================
def query_task(
    task_id: str,
    x_tt_logid: str,
    appid: str | None = None,
    token: str | None = None,
) -> dict:
    """
    查询标准版识别任务状态。

    Returns:
        {"status_code": str, "message": str, "logid": str, "body": dict}
    """
    headers = _build_headers(appid=appid, token=token)
    headers["X-Api-Request-Id"] = task_id
    headers["X-Tt-Logid"] = x_tt_logid

    try:
        resp = requests.post(
            ASR_STANDARD_QUERY_URL,
            data=json.dumps({}),
            headers=headers,
            timeout=30,
        )
    except requests.RequestException as e:
        return {
            "status_code": "NETWORK_ERROR",
            "message": str(e),
            "logid": "",
            "body": {},
        }

    return {
        "status_code": resp.headers.get("X-Api-Status-Code", ""),
        "message": resp.headers.get("X-Api-Message", ""),
        "logid": resp.headers.get("X-Tt-Logid", ""),
        "body": resp.json() if resp.text.strip() else {},
    }


# ============================================================
# Poll until done
# ============================================================
def poll_until_done(
    task_id: str,
    x_tt_logid: str,
    appid: str | None = None,
    token: str | None = None,
    poll_interval: int = DEFAULT_POLL_INTERVAL,
    poll_max_time: int = DEFAULT_POLL_MAX_TIME,
) -> dict:
    """
    轮询标准版识别任务直到完成或超时。

    Returns:
        ASR 结果 JSON (dict)。
    """
    start = time.time()
    while True:
        elapsed = time.time() - start
        if elapsed > poll_max_time:
            fail_json(
                "POLL_TIMEOUT",
                f"标准版识别任务超时: task_id={task_id}, "
                f"已等待 {int(elapsed)} 秒（上限 {poll_max_time} 秒）",
                task_id=task_id,
            )

        qr = query_task(task_id, x_tt_logid, appid=appid, token=token)
        code = qr["status_code"]

        if code == "20000000":
            log(f"识别完成: task_id={task_id}")
            return qr["body"]
        elif code in ("20000001", "20000002"):
            log(
                f"任务进行中: code={code}, "
                f"已等待 {int(elapsed)}s, {poll_interval}s 后重试..."
            )
            time.sleep(poll_interval)
        else:
            fail_json(
                "TASK_FAILED",
                f"标准版识别失败: code={code}, msg={qr['message']}",
                task_id=task_id,
                logid=qr["logid"],
            )


# ============================================================
# 文本提取 (统一格式)
# ============================================================
def extract_text(result: dict) -> str:
    """
    从火山 ASR 标准版响应 JSON 中提取纯文本。

    兼容多种返回格式:
      - result.text
      - result.utterances[].text
      - utterances[].text (顶层)
      - result[] (列表形式)
    """
    text_parts: list[str] = []

    if "result" in result:
        res = result["result"]
        if isinstance(res, list):
            for item in res:
                if isinstance(item, dict) and "text" in item:
                    text_parts.append(item["text"])
        elif isinstance(res, dict):
            if "text" in res:
                text_parts.append(res["text"])
            elif "utterances" in res:
                for utt in res["utterances"]:
                    if "text" in utt:
                        text_parts.append(utt["text"])

    if not text_parts and "utterances" in result:
        for utt in result["utterances"]:
            if "text" in utt:
                text_parts.append(utt["text"])

    return "".join(text_parts)


# ============================================================
# CLI 主流程
# ============================================================
def main() -> None:
    parser = argparse.ArgumentParser(
        description="火山引擎 BigModel ASR 标准版（录音文件识别，异步 submit+poll）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
示例:
  # URL 识别
  python3 asr_standard.py --url "https://example.com/audio.mp3"

  # 本地文件识别
  python3 asr_standard.py --file "/path/to/long_audio.wav"

  # 仅提交，不轮询
  python3 asr_standard.py --url "https://..." --no-poll

  # 查询已有任务
  python3 asr_standard.py --query-task-id <ID> --query-logid <LOGID>
        """,
    )

    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument("--url", help="音频文件的 URL 地址")
    input_group.add_argument("--file", help="本地音频文件路径")

    parser.add_argument(
        "--appid",
        help="火山引擎 ASR App ID (也可通过环境变量 MODEL_SPEECH_APP_ID 设置)",
    )
    parser.add_argument(
        "--token",
        help="火山引擎 ASR API Key (也可通过环境变量 MODEL_SPEECH_API_KEY 设置)",
    )
    parser.add_argument(
        "--language",
        help="语言代码，如 zh-CN, ja-JP, en-US (可选，不传则自动识别)",
    )
    parser.add_argument(
        "--no-poll",
        action="store_true",
        help="仅提交任务，不轮询结果（返回 task_id 供后续查询）",
    )
    parser.add_argument(
        "--poll-interval",
        type=int,
        default=DEFAULT_POLL_INTERVAL,
        help=f"轮询间隔秒数 (默认: {DEFAULT_POLL_INTERVAL})",
    )
    parser.add_argument(
        "--poll-max-time",
        type=int,
        default=DEFAULT_POLL_MAX_TIME,
        help=f"最大轮询时间秒数 (默认: {DEFAULT_POLL_MAX_TIME})",
    )

    # 查询子功能
    parser.add_argument(
        "--query-task-id",
        help="查询已有任务的 task_id（与 --query-logid 配合使用）",
    )
    parser.add_argument(
        "--query-logid",
        default="",
        help="查询时传入的 X-Tt-Logid（可选）",
    )

    args = parser.parse_args()

    # 模式 1: 查询已有任务
    if args.query_task_id:
        log(f"查询任务: task_id={args.query_task_id}")
        result = poll_until_done(
            task_id=args.query_task_id,
            x_tt_logid=args.query_logid,
            appid=args.appid,
            token=args.token,
            poll_interval=args.poll_interval,
            poll_max_time=args.poll_max_time,
        )
        text = extract_text(result)
        if text:
            print(text)
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # 模式 2: 提交新任务
    if not args.url and not args.file:
        fail_json("NO_INPUT", "必须提供 --url 或 --file（或 --query-task-id 查询已有任务）")

    submit_result = submit_task(
        audio_url=args.url,
        file_path=args.file,
        appid=args.appid,
        token=args.token,
        language=args.language,
    )

    task_id = submit_result["task_id"]
    x_tt_logid = submit_result["x_tt_logid"]

    if args.no_poll:
        print(json.dumps({
            "task_id": task_id,
            "x_tt_logid": x_tt_logid,
            "status": "submitted",
            "message": "任务已提交，使用以下命令查询结果:",
            "query_command": (
                f"python3 asr_standard.py "
                f"--query-task-id {task_id} --query-logid {x_tt_logid}"
            ),
        }, ensure_ascii=False, indent=2))
        return

    # 轮询直到完成
    result = poll_until_done(
        task_id=task_id,
        x_tt_logid=x_tt_logid,
        appid=args.appid,
        token=args.token,
        poll_interval=args.poll_interval,
        poll_max_time=args.poll_max_time,
    )
    text = extract_text(result)
    if text:
        log(f"识别成功，文本长度: {len(text)} 字符")
        print(text)
    else:
        log("警告: 未提取到文本，输出原始 JSON")
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
