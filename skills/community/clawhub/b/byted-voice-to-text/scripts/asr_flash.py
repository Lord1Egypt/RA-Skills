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
Byted-Voice-to-Text (ASR) using Volcengine BigModel ASR API.
Ref: https://www.volcengine.com/docs/6561/1354870
鉴权: 新版控制台 API Key 方案 https://www.volcengine.com/docs/6561/2119699
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import tempfile
import time
import uuid

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

from api_key import get_speech_api_key

ASR_ENDPOINT = os.getenv(
    "MODEL_SPEECH_ASR_API_BASE",
    "https://openspeech.bytedance.com/api/v3/auc/bigmodel/recognize/flash",
)
ASR_RESOURCE_ID = os.getenv("MODEL_SPEECH_ASR_RESOURCE_ID", "volc.bigasr.auc_turbo")


def log(msg: str) -> None:
    print(f"[byted-voice-to-text] {msg}", file=sys.stderr)


def fail(msg: str) -> None:
    full = f"[byted-voice-to-text ERROR] {msg}"
    print(full, file=sys.stderr)
    print(full)
    sys.exit(1)


try:
    import requests
except ImportError:
    fail("requests 库未安装，请执行 pip install requests")


# ============================================================
# 飞书语音文件下载
# ============================================================
def download_feishu_audio(file_key: str, tenant_token: str) -> str:
    """
    通过飞书 file_key 下载语音文件到临时目录，返回本地文件路径。

    飞书语音消息格式：
      - message_type: "audio"
      - content: {"file_key": "file_v2_xxxx"}
      - 音频编码: Opus in OGG 容器

    调用飞书「下载文件」接口:
      GET https://open.feishu.cn/open-apis/im/v1/files/{file_key}
    """
    download_url = f"https://open.feishu.cn/open-apis/im/v1/files/{file_key}"
    headers = {
        "Authorization": f"Bearer {tenant_token}",
        "Content-Type": "application/json; charset=utf-8",
    }

    log(f"正在从飞书下载语音文件: file_key={file_key}")
    resp = requests.get(download_url, headers=headers, timeout=30)

    if resp.status_code != 200:
        fail(
            f"飞书文件下载失败: HTTP {resp.status_code}, "
            f"响应: {resp.text[:500]}"
        )

    tmp_file = tempfile.NamedTemporaryFile(suffix=".ogg", delete=False)
    tmp_file.write(resp.content)
    tmp_file.close()

    file_size = len(resp.content)
    log(f"语音文件已下载: {tmp_file.name} ({file_size} bytes)")
    return tmp_file.name


# ============================================================
# 火山引擎 ASR 识别
# ============================================================
def file_to_base64(file_path: str) -> str:
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def _build_headers(appid: str | None = None, token: str | None = None) -> dict:
    """构建请求头。支持新版控制台(X-Api-Key)和旧版(X-Api-App-Key + X-Api-Access-Key)。"""
    app_id = appid or os.getenv("MODEL_SPEECH_APP_ID", "").strip()
    api_key = token or get_speech_api_key().strip()

    if not api_key:
        raise PermissionError(
            "MODEL_SPEECH_API_KEY 需在环境变量中配置。"
            "见 https://www.volcengine.com/docs/6561/2119699"
        )

    headers = {
        "X-Api-Resource-Id": ASR_RESOURCE_ID,
        "X-Api-Request-Id": str(uuid.uuid4()),
        "X-Api-Sequence": "-1",
    }

    if app_id:
        headers["X-Api-App-Key"] = app_id
        headers["X-Api-Access-Key"] = api_key
    else:
        headers["X-Api-Key"] = api_key

    return headers


def recognize(
    audio_url: str | None = None,
    file_path: str | None = None,
    appid: str | None = None,
    token: str | None = None,
    language: str | None = None,
) -> str:
    """调用火山引擎 BigModel ASR Flash 接口，返回识别文本。"""
    headers = _build_headers(appid=appid, token=token)

    audio_data: dict = {}
    if audio_url:
        audio_data["url"] = audio_url
    elif file_path:
        audio_data["data"] = file_to_base64(file_path)
    else:
        raise ValueError("必须提供 audio_url 或 file_path")

    if language:
        audio_data["language"] = language

    payload = {
        "user": {"uid": headers.get("X-Api-App-Key", "skill_asr_user")},
        "audio": audio_data,
        "request": {
            "model_name": "bigmodel",
            "enable_itn": True,
            "enable_punc": True,
        },
    }

    log("正在调用火山引擎 ASR...")
    resp = requests.post(ASR_ENDPOINT, json=payload, headers=headers, timeout=60)

    status_code = resp.headers.get("X-Api-Status-Code", "")
    if status_code != "20000000":
        msg = resp.headers.get("X-Api-Message", "未知错误")
        logid = resp.headers.get("X-Tt-Logid", "N/A")
        fail(f"ASR 请求失败: code={status_code}, msg={msg}, logid={logid}")

    result = resp.json()
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

    if not text_parts:
        fail(f"无法从响应中提取文本，原始响应: {json.dumps(result, ensure_ascii=False)}")

    text = "".join(text_parts)
    log(f"识别成功，文本长度: {len(text)} 字符")
    return text


# ============================================================
# 主流程
# ============================================================
def main() -> None:
    parser = argparse.ArgumentParser(
        description="语音转文字工具（火山引擎 BigModel ASR）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:

  # 方式1: 直接传音频 URL
  python asr_flash.py --url "https://example.com/audio.mp3"

  # 方式2: 传本地音频文件
  python asr_flash.py --file "/path/to/audio.ogg"

  # 方式3: 传飞书语音消息的 file_key
  python asr_flash.py --file-key "file_v2_xxxx" --feishu-token "t-g104xxx"

飞书语音消息处理流程:
  收到 audio 消息 → 提取 content.file_key → 本脚本下载+识别 → 返回文字
        """,
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", help="音频文件的 URL 地址")
    group.add_argument("--file", help="本地音频文件路径")
    group.add_argument("--file-key", help="飞书语音消息的 file_key")

    parser.add_argument(
        "--feishu-token",
        help="飞书 tenant_access_token (也可通过环境变量 FEISHU_TENANT_TOKEN 设置)",
    )
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

    args = parser.parse_args()

    log(f"启动参数: file={args.file}, url={args.url}, file_key={args.file_key}")
    log(
        f"环境变量: MODEL_SPEECH_APP_ID={'已设置' if os.environ.get('MODEL_SPEECH_APP_ID') else '未设置'}, "
        f"MODEL_SPEECH_API_KEY={'已设置' if os.environ.get('MODEL_SPEECH_API_KEY') else '未设置'}, "
        f"FEISHU_TENANT_TOKEN={'已设置' if os.environ.get('FEISHU_TENANT_TOKEN') else '未设置'}"
    )

    if args.file:
        if not os.path.exists(args.file):
            fail(f"音频文件不存在: {args.file}")
        file_size = os.path.getsize(args.file)
        log(f"音频文件: {args.file} ({file_size} bytes)")
        if file_size == 0:
            fail(f"音频文件为空: {args.file}")

    local_file = None
    try:
        if args.file_key:
            feishu_token = args.feishu_token or os.environ.get(
                "FEISHU_TENANT_TOKEN", ""
            )
            if not feishu_token:
                fail(
                    "使用 --file-key 时需要飞书 token。"
                    "请通过 --feishu-token 参数或环境变量 FEISHU_TENANT_TOKEN 提供"
                )
            local_file = download_feishu_audio(args.file_key, feishu_token)

        text = recognize(
            audio_url=args.url,
            file_path=args.file or local_file,
            appid=args.appid,
            token=args.token,
            language=args.language,
        )

        print(text)

    except PermissionError as e:
        fail(str(e))
    except SystemExit:
        raise
    except Exception as e:
        fail(str(e))
    finally:
        if local_file and os.path.exists(local_file):
            os.unlink(local_file)


if __name__ == "__main__":
    main()
