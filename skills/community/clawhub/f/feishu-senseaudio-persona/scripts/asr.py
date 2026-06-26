from __future__ import annotations

import importlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict


def ensure_python_package(import_name: str, pip_name: str | None = None) -> None:
    pip_name = pip_name or import_name
    try:
        importlib.import_module(import_name)
        return
    except ImportError:
        pass

    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", pip_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"缺少 Python 依赖 {pip_name}，自动安装失败。\n"
            f"请手动执行: {sys.executable} -m pip install {pip_name}\n"
            f"stderr:\n{result.stderr}"
        )


def _requests_module():
    ensure_python_package("requests")
    return importlib.import_module("requests")


def transcribe_audio(audio_path: str) -> Dict[str, Any]:
    requests = _requests_module()

    api_key = os.getenv("SENSEAUDIO_API_KEY")
    if not api_key:
        raise RuntimeError("缺少环境变量 SENSEAUDIO_API_KEY")

    endpoint = os.getenv("SENSEAUDIO_ASR_ENDPOINT", "https://api.senseaudio.cn/v1/asr")
    path = Path(audio_path).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"找不到音频文件: {path}")

    headers = {"Authorization": f"Bearer {api_key}"}

    with path.open("rb") as f:
        files = {"file": (path.name, f, "application/octet-stream")}
        data = {"model": os.getenv("SENSEAUDIO_ASR_MODEL", "SenseAudio-ASR")}
        resp = requests.post(endpoint, headers=headers, files=files, data=data, timeout=120)

    resp.raise_for_status()
    payload = resp.json()

    # 容忍不同字段命名
    text = (
        payload.get("text")
        or payload.get("result")
        or payload.get("data", {}).get("text")
        or payload.get("data", {}).get("result")
    )
    if not text:
        raise RuntimeError(f"ASR 返回中未找到文本字段: {json.dumps(payload, ensure_ascii=False)}")

    return {"text": text, "raw": payload, "endpoint": endpoint}
