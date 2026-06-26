#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict

import requests

DEFAULT_BASE_URL = "https://api.senseaudio.cn"
DEFAULT_MODEL = "sense-asr-pro"
TRANSCRIBE_PATH = "/v1/audio/transcriptions"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Transcribe one audio file with SenseASR and print plain text")
    parser.add_argument("--file", required=True, help="Path to the local audio file")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--language", default="en")
    parser.add_argument("--target-language")
    return parser


def getenv_required(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"缺少配置：{name}")
    return value


def should_enable_punctuation(model: str) -> bool:
    return model in {"sense-asr", "sense-asr-pro"}


def should_enable_itn(model: str) -> bool:
    return model != "sense-asr-deepthink"


def parse_json_response(resp: requests.Response) -> Dict[str, Any]:
    try:
        return resp.json()
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"服务返回了非 JSON 内容: status={resp.status_code}") from exc


def main() -> None:
    args = build_parser().parse_args()
    api_key = getenv_required("SENSEAUDIO_API_KEY")
    base_url = os.environ.get("SENSEAUDIO_BASE_URL", DEFAULT_BASE_URL).rstrip("/")

    if args.model == "sense-asr-deepthink" and args.language:
        raise RuntimeError("sense-asr-deepthink 不支持 language 参数")

    if not os.path.isfile(args.file):
        raise RuntimeError(f"找不到音频文件: {args.file}")

    data = {
        "model": args.model,
        "response_format": "json",
    }
    if args.language:
        data["language"] = args.language
    if args.target_language:
        data["target_language"] = args.target_language
    if should_enable_itn(args.model):
        data["enable_itn"] = "true"
    if should_enable_punctuation(args.model):
        data["enable_punctuation"] = "true"

    headers = {"Authorization": f"Bearer {api_key}"}

    with open(args.file, "rb") as fh:
        files = {"file": (os.path.basename(args.file), fh)}
        resp = requests.post(
            f"{base_url}{TRANSCRIBE_PATH}",
            headers=headers,
            data=data,
            files=files,
            timeout=120,
        )

    body = parse_json_response(resp)
    if not resp.ok:
        message = body.get("message") or body.get("error") or body
        raise RuntimeError(f"语音识别失败: status={resp.status_code}, message={message}")

    text = str(body.get("text") or "").strip()
    if not text:
        raise RuntimeError("语音识别返回为空")
    print(text)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
