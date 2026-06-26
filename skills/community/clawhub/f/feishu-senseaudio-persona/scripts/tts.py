from __future__ import annotations

import importlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Optional

ROOT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT_DIR / "outputs"


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


def synthesize(
    text: str,
    voice_id: str,
    speed: float = 1.0,
    pitch: int = 0,
    vol: float = 1.0,
    emotion: Optional[str] = None,
    output_wav: Optional[str] = None,
) -> Dict[str, Any]:
    requests = _requests_module()

    api_key = os.getenv("SENSEAUDIO_API_KEY")
    if not api_key:
        raise RuntimeError("缺少环境变量 SENSEAUDIO_API_KEY")

    base = os.getenv("SENSEAUDIO_API_BASE", "https://api.senseaudio.cn").rstrip("/")
    endpoint = f"{base}/v1/t2a_v2"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if output_wav:
        wav_path = Path(output_wav).expanduser().resolve()
        wav_path.parent.mkdir(parents=True, exist_ok=True)
    else:
        wav_path = OUTPUT_DIR / "reply.wav"

    payload = {
        "model": os.getenv("SENSEAUDIO_TTS_MODEL", "SenseAudio-TTS-1.0"),
        "text": text,
        "stream": False,
        "voice_setting": {
            "voice_id": voice_id,
            "speed": float(speed),
            "pitch": int(round(float(pitch))),
            "vol": float(vol),
        },
        "audio_setting": {
            "format": "wav",
            "sample_rate": int(os.getenv("SENSEAUDIO_TTS_SAMPLE_RATE", "24000")),
            "channel": 1,
        },
    }
    if emotion:
        payload["voice_setting"]["emotion"] = emotion

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    resp = requests.post(endpoint, headers=headers, json=payload, timeout=120)
    resp.raise_for_status()
    data = resp.json()

    base_resp = data.get("base_resp", {})
    status_code = base_resp.get("status_code")
    status_msg = base_resp.get("status_msg") or base_resp.get("status_message") or ""
    if status_code not in (None, 0):
        raise RuntimeError(f"SenseAudio TTS 调用失败: status_code={status_code}, status_msg={status_msg}")

    audio_hex = data.get("data", {}).get("audio") or data.get("audio")
    if not audio_hex:
        raise RuntimeError(f"TTS 返回中缺少音频字段: {json.dumps(data, ensure_ascii=False)}")

    wav_path.write_bytes(bytes.fromhex(audio_hex))
    return {"wav_path": str(wav_path), "raw": data, "endpoint": endpoint}


def convert_wav_to_opus(input_wav: str, output_opus: Optional[str] = None) -> str:
    input_path = Path(input_wav).expanduser().resolve()
    if not input_path.exists():
        raise FileNotFoundError(f"找不到 wav 文件: {input_path}")

    if output_opus:
        opus_path = Path(output_opus).expanduser().resolve()
        opus_path.parent.mkdir(parents=True, exist_ok=True)
    else:
        opus_path = input_path.with_suffix(".opus")

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-c:a",
        "libopus",
        "-b:a",
        "32k",
        str(opus_path),
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg 转 OPUS 失败:\n{result.stderr}")
    return str(opus_path)
