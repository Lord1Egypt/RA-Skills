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
Byted-Text-to-Speech (TTS) using Volcengine Doubao Speech API.
Ref: https://www.volcengine.com/docs/6561/1598757 (HTTP Chunked/SSE 单向流式-V3)
鉴权: 新版控制台 API Key 方案 https://console.volcengine.com/speech/new/setting/apikeys
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
import uuid
from pathlib import Path
from typing import Optional

import httpx

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

from api_key import get_speech_api_key

TTS_API_BASE = os.getenv("MODEL_SPEECH_API_BASE", "openspeech.bytedance.com")
TTS_ENDPOINT = f"https://{TTS_API_BASE}/api/v3/tts/unidirectional/sse"
TTS_RESOURCE_ID = os.getenv("MODEL_SPEECH_TTS_RESOURCE_ID", "seed-tts-2.0")
DEFAULT_SPEAKER = "zh_female_vv_uranus_bigtts"
DEFAULT_FORMAT = "mp3"
DEFAULT_SAMPLE_RATE = 24000
VALID_FORMATS = ("mp3", "pcm", "ogg_opus")
VALID_SAMPLE_RATES = (8000, 16000, 22050, 24000, 32000, 44100, 48000)


def _build_headers() -> dict:
    """构建请求头。使用新版控制台 X-Api-Key 鉴权。"""
    headers = {
        "Content-Type": "application/json",
        "X-Api-Resource-Id": TTS_RESOURCE_ID,
        "X-Api-Request-Id": str(uuid.uuid4()),
    }
    api_key = get_speech_api_key().strip()

    if not api_key:
        raise PermissionError(
            "MODEL_SPEECH_API_KEY 需在环境变量中配置。"
            "见 https://console.volcengine.com/speech/new/setting/apikeys"
        )

    headers["X-Api-Key"] = api_key

    return headers


def _build_body(
    text: str,
    speaker: str,
    audio_format: str,
    sample_rate: int,
    speech_rate: int,
    pitch_rate: int,
    loudness_rate: int = 0,
    bit_rate: Optional[int] = None,
    enable_latex: bool = False,
    filter_markdown: bool = False,
) -> dict:
    """构建 V3 SSE 请求 body。"""
    audio_params: dict = {
        "format": audio_format,
        "speech_rate": speech_rate,
        "loudness_rate": loudness_rate,
    }
    if audio_format in ("mp3", "ogg_opus"):
        audio_params["bit_rate"] = bit_rate if bit_rate is not None else 64000
    additions_dict: dict = {
        "post_process": {"pitch": pitch_rate},
        "disable_markdown_filter": True,
        "enable_latex_tn": True,
        "latex_parser": "v2",
    }
    if filter_markdown:
        additions_dict["disable_markdown_filter"] = False
    if not enable_latex:
        additions_dict["enable_latex_tn"] = False
    return {
        "user": {"uid": "skill_tts_user"},
        "req_params": {
            "text": text,
            "speaker": speaker,
            "sample_rate": sample_rate,
            "audio_params": audio_params,
            "additions": json.dumps(additions_dict),
        },
    }


def text_to_speech(
    text: str,
    output_path: Optional[str] = None,
    speaker: str = DEFAULT_SPEAKER,
    audio_format: str = DEFAULT_FORMAT,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    speech_rate: int = 0,
    pitch_rate: int = 0,
    loudness_rate: int = 0,
    bit_rate: Optional[int] = None,
    enable_latex: bool = False,
    filter_markdown: bool = False,
    timeout: float = 60.0,
) -> dict:
    """
    调用火山引擎豆包语音合成 API，将文本转为语音并保存为文件。

    Returns:
        包含 status, local_path, format, error 的字典
    """
    if not text or not text.strip():
        return {
            "status": "error",
            "local_path": None,
            "format": audio_format,
            "error": "text is empty",
        }
    if audio_format not in VALID_FORMATS:
        return {
            "status": "error",
            "local_path": None,
            "format": audio_format,
            "error": f"format must be one of {VALID_FORMATS}",
        }
    if sample_rate not in VALID_SAMPLE_RATES:
        return {
            "status": "error",
            "local_path": None,
            "format": audio_format,
            "error": f"sample_rate must be one of {VALID_SAMPLE_RATES}",
        }

    if output_path is None:
        ts = int(time.time())
        output_path = f"tts_output_{ts}.{audio_format}"

    output_path = os.path.abspath(output_path)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    headers = _build_headers()
    body = _build_body(
        text=text.strip(),
        speaker=speaker,
        audio_format=audio_format,
        sample_rate=sample_rate,
        speech_rate=speech_rate,
        pitch_rate=pitch_rate,
        loudness_rate=loudness_rate,
        bit_rate=bit_rate,
        enable_latex=enable_latex,
        filter_markdown=filter_markdown,
    )

    try:
        with httpx.Client(timeout=timeout) as client:
            with client.stream("POST", TTS_ENDPOINT, headers=headers, json=body) as resp:
                resp.raise_for_status()

                audio_chunks = []
                for line in resp.iter_lines():
                    if not line.startswith("data:"):
                        continue
                    try:
                        d = json.loads(line[5:].strip())
                        code = d.get("code", 0)
                        if code not in (0, 20000000):
                            return {
                                "status": "error",
                                "local_path": None,
                                "format": audio_format,
                                "error": f"API error code={code}: {d.get('message', '')}",
                            }
                        if d.get("data"):
                            audio_chunks.append(base64.b64decode(d["data"]))
                    except (json.JSONDecodeError, KeyError):
                        continue

        if not audio_chunks:
            return {
                "status": "error",
                "local_path": None,
                "format": audio_format,
                "error": "No audio data returned.",
            }

        with open(output_path, "wb") as f:
            for chunk in audio_chunks:
                f.write(chunk)

        return {
            "status": "success",
            "local_path": output_path,
            "format": audio_format,
            "error": None,
        }
    except Exception as e:
        try:
            if os.path.exists(output_path):
                os.remove(output_path)
        except OSError:
            pass
        return {
            "status": "error",
            "local_path": None,
            "format": audio_format,
            "error": str(e),
        }


def main():
    parser = argparse.ArgumentParser(
        description="Byted-Text-to-Speech using Volcengine Doubao Speech (TTS)"
    )
    parser.add_argument(
        "--text", "-t", required=True, help="Text to synthesize"
    )
    parser.add_argument(
        "--output", "-o", default=None, help="Output audio file path"
    )
    parser.add_argument(
        "--speaker", "-s", default=DEFAULT_SPEAKER, help="Speaker ID"
    )
    parser.add_argument(
        "--format", "-f", choices=VALID_FORMATS, default=DEFAULT_FORMAT,
        help="Audio format",
    )
    parser.add_argument(
        "--sample-rate", type=int, default=DEFAULT_SAMPLE_RATE,
        choices=VALID_SAMPLE_RATES, help="Sample rate",
    )
    parser.add_argument(
        "--speech-rate", type=int, default=0,
        help="Speech rate [-50, 100]",
    )
    parser.add_argument(
        "--pitch-rate", type=int, default=0,
        help="Pitch rate [-12, 12]",
    )
    parser.add_argument(
        "--loudness-rate", type=int, default=0,
        help="Loudness rate [-50, 100]. 100=2x volume, -50=0.5x volume",
    )
    parser.add_argument(
        "--bit-rate", type=int, default=None,
        help="Bit rate (e.g. 64000, 128000). Applies to mp3 and ogg_opus formats, default 64000.",
    )
    parser.add_argument(
        "--enable-latex", action="store_true", default=False,
        help="Enable LaTeX formula reading (uses latex_parser v2)",
    )
    parser.add_argument(
        "--filter-markdown", action="store_true", default=False,
        help="Filter markdown syntax (e.g. **hello** reads as 'hello')",
    )
    parser.add_argument(
        "--timeout", type=float, default=60.0, help="Request timeout (seconds)",
    )
    args = parser.parse_args()

    try:
        result = text_to_speech(
            text=args.text,
            output_path=args.output,
            speaker=args.speaker,
            audio_format=args.format,
            sample_rate=args.sample_rate,
            speech_rate=args.speech_rate,
            pitch_rate=args.pitch_rate,
            loudness_rate=args.loudness_rate,
            bit_rate=args.bit_rate,
            enable_latex=args.enable_latex,
            filter_markdown=args.filter_markdown,
            timeout=args.timeout,
        )
    except PermissionError as e:
        print(json.dumps({
            "status": "error",
            "local_path": None,
            "format": getattr(args, "format", DEFAULT_FORMAT),
            "error": str(e),
        }, indent=2, ensure_ascii=False))
        sys.exit(1)

    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("status") == "success" else 1)


if __name__ == "__main__":
    main()
