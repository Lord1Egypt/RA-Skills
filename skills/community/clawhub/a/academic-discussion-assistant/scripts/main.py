#!/usr/bin/env python3
"""
Meeting Assistant skill CLI.

职责：
- 调用 SenseAudio ASR 完成带说话人分离的会议转写
- 整理可直接交给 LLM 的结构化会议文本
- 调用 SenseAudio TTS 将摘要内容合成为语音

说明：
- 摘要本身由上层 Agent 按 references/summary_prompt.md 执行
- 本脚本负责稳定的 API 调用、文件输出和中间产物组织
"""

from __future__ import annotations

import argparse
import datetime as dt
import importlib
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


def ensure_python_package(import_name: str, pip_name: Optional[str] = None) -> None:
    pip_name = pip_name or import_name
    try:
        importlib.import_module(import_name)
        return
    except ImportError:
        print(f"缺少 {pip_name}，正在自动安装...", file=sys.stderr)

    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", pip_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"自动安装 {pip_name} 失败，请手动执行: {sys.executable} -m pip install {pip_name}\n"
            f"{result.stderr.strip()}"
        )

    try:
        importlib.import_module(import_name)
    except ImportError as exc:
        raise RuntimeError(f"已安装 {pip_name}，但仍无法导入 {import_name}。") from exc


ensure_python_package("requests")
import requests


DEFAULT_API_BASE = "https://api.senseaudio.cn"
ASR_API_PATH = "/v1/audio/transcriptions"
TTS_API_PATH = "/v1/t2a_v2"

DEFAULT_ASR_MODEL = "sense-asr-pro"
DEFAULT_TTS_MODEL = "SenseAudio-TTS-1.0"
DEFAULT_TTS_VOICE = "male_0004_a"
DEFAULT_OUTPUT_FORMAT = "mp3"
DEFAULT_SAMPLE_RATE = 32000
DEFAULT_BITRATE = 128000
DEFAULT_CHANNEL = 1
DEFAULT_SPEED = 1.0
DEFAULT_VOL = 1.0
DEFAULT_PITCH = 0
DEFAULT_MAX_SPEAKERS = 3
MAX_AUDIO_SIZE_MB = 10
OUTPUT_DIR = Path("./outputs")


class APIError(Exception):
    pass


@dataclass
class TranscriptionResult:
    output_dir: Path
    json_path: Path
    transcript_txt_path: Path
    diarized_txt_path: Path
    llm_input_path: Path
    response_json: Dict[str, Any]


@dataclass
class TTSResult:
    output_path: Path
    meta_path: Optional[Path]
    response_json: Dict[str, Any]


class SenseAudioClient:
    def __init__(self, api_key: Optional[str] = None, api_base: Optional[str] = None):
        self.api_key = (api_key or os.getenv("SENSEAUDIO_API_KEY", "")).strip()
        self.api_base = (api_base or os.getenv("SENSEAUDIO_API_BASE", DEFAULT_API_BASE)).rstrip("/")

    @property
    def configured(self) -> bool:
        return bool(self.api_key)

    @property
    def headers_json(self) -> Dict[str, str]:
        if not self.api_key:
            raise APIError(missing_key_message())
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    @property
    def headers_auth_only(self) -> Dict[str, str]:
        if not self.api_key:
            raise APIError(missing_key_message())
        return {"Authorization": f"Bearer {self.api_key}"}

    def auth_check(self) -> Dict[str, Any]:
        if not self.configured:
            raise APIError(missing_key_message())
        return {
            "configured": self.configured,
            "api_base": self.api_base,
            "message": "已检测到 `SENSEAUDIO_API_KEY`。当前 auth-check 仅做本地配置检查，避免伪造测试音频触发服务端 500。",
        }

    def transcribe(
        self,
        *,
        audio_path: Path,
        language: Optional[str],
        max_speakers: int,
        enable_sentiment: bool,
        output_dir: Optional[Path] = None,
    ) -> TranscriptionResult:
        if not audio_path.exists():
            raise APIError(f"音频文件不存在: {audio_path}")
        if audio_path.stat().st_size > MAX_AUDIO_SIZE_MB * 1024 * 1024:
            raise APIError(
                f"音频文件大于 {MAX_AUDIO_SIZE_MB}MB，当前官方建议单文件不超过 {MAX_AUDIO_SIZE_MB}MB。"
                " 请先切片后再调用。"
            )

        data: List[tuple[str, str]] = [
            ("model", DEFAULT_ASR_MODEL),
            ("response_format", "verbose_json"),
            ("enable_speaker_diarization", "true"),
            ("max_speakers", str(max_speakers)),
            ("enable_itn", "true"),
            ("enable_punctuation", "true"),
            ("enable_sentiment", "true" if enable_sentiment else "false"),
            ("timestamp_granularities[]", "segment"),
            ("timestamp_granularities[]", "word"),
        ]
        if language:
            data.append(("language", language))

        with audio_path.open("rb") as audio_file:
            files = {"file": (audio_path.name, audio_file, guess_mime_type(audio_path))}
            response = requests.post(
                f"{self.api_base}{ASR_API_PATH}",
                headers=self.headers_auth_only,
                data=data,
                files=files,
                timeout=600,
            )

        parsed = handle_json_response(response)
        out_dir = prepare_transcription_dir(audio_path, output_dir)
        json_path = out_dir / "asr_verbose.json"
        transcript_txt_path = out_dir / "transcript_raw.txt"
        diarized_txt_path = out_dir / "transcript_diarized.txt"
        llm_input_path = out_dir / "llm_meeting_input.txt"

        json_path.write_text(json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8")
        transcript_txt_path.write_text((parsed.get("text") or "").strip() + "\n", encoding="utf-8")

        diarized_text = build_diarized_transcript(parsed)
        diarized_txt_path.write_text(diarized_text, encoding="utf-8")

        llm_input = build_llm_input(audio_path, parsed, diarized_text)
        llm_input_path.write_text(llm_input, encoding="utf-8")

        return TranscriptionResult(
            output_dir=out_dir,
            json_path=json_path,
            transcript_txt_path=transcript_txt_path,
            diarized_txt_path=diarized_txt_path,
            llm_input_path=llm_input_path,
            response_json=parsed,
        )

    def synthesize(
        self,
        *,
        text: str,
        output: Path,
        voice_id: str,
        output_format: str,
        sample_rate: int,
        bitrate: int,
        channel: int,
        speed: float,
        vol: float,
        pitch: int,
        save_meta: bool,
    ) -> TTSResult:
        validate_tts_params(
            text=text,
            output_format=output_format,
            sample_rate=sample_rate,
            bitrate=bitrate,
            channel=channel,
            speed=speed,
            vol=vol,
            pitch=pitch,
        )
        payload = {
            "model": DEFAULT_TTS_MODEL,
            "text": text,
            "stream": False,
            "voice_setting": {
                "voice_id": voice_id,
                "speed": speed,
                "vol": vol,
                "pitch": pitch,
            },
            "audio_setting": {
                "format": output_format,
                "sample_rate": sample_rate,
                "bitrate": bitrate,
                "channel": channel,
            },
        }
        try:
            response = requests.post(
                f"{self.api_base}{TTS_API_PATH}",
                headers=self.headers_json,
                json=payload,
                timeout=300,
            )
        except requests.exceptions.RequestException as exc:
            raise APIError(f"TTS 请求失败: {exc}") from exc

        parsed = handle_json_response(response)
        audio_hex = ((parsed.get("data") or {}).get("audio") or "").strip()
        if not audio_hex:
            raise APIError("TTS 返回成功但 `data.audio` 为空。")

        try:
            audio_bytes = bytes.fromhex(audio_hex)
        except ValueError as exc:
            raise APIError("TTS 返回的 `data.audio` 不是合法 hex。") from exc

        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(audio_bytes)

        meta_path = None
        if save_meta:
            meta_path = output.with_suffix(output.suffix + ".json")
            meta_path.write_text(json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8")

        return TTSResult(output_path=output, meta_path=meta_path, response_json=parsed)


def missing_key_message() -> str:
    return (
        "未检测到 `SENSEAUDIO_API_KEY`。\n"
        "请先配置：\n"
        'export SENSEAUDIO_API_KEY="YOUR_API_KEY"\n'
        'export SENSEAUDIO_API_BASE="https://api.senseaudio.cn"'
    )


def guess_mime_type(path: Path) -> str:
    ext = path.suffix.lower()
    mapping = {
        ".wav": "audio/wav",
        ".mp3": "audio/mpeg",
        ".m4a": "audio/mp4",
        ".mp4": "video/mp4",
        ".ogg": "audio/ogg",
        ".aac": "audio/aac",
        ".flac": "audio/flac",
    }
    return mapping.get(ext, "application/octet-stream")


def handle_json_response(response: requests.Response) -> Dict[str, Any]:
    if response.status_code in (401, 403):
        raise APIError("认证失败：`SENSEAUDIO_API_KEY` 无效、过期或无权限。")
    if response.status_code == 429:
        raise APIError("请求频率过高，接口返回 HTTP 429。")
    if response.status_code >= 400:
        raise APIError(f"HTTP {response.status_code}: {response.text[:500]}")

    try:
        parsed = response.json()
    except ValueError as exc:
        raise APIError(f"接口返回了非 JSON 内容: {response.text[:300]}") from exc

    if isinstance(parsed, dict) and parsed.get("code") and parsed.get("message"):
        raise APIError(f"{parsed['code']}: {parsed['message']}")
    base_resp = parsed.get("base_resp")
    if isinstance(base_resp, dict) and base_resp.get("status_code", 0) not in (0, None):
        raise APIError(f"{base_resp.get('status_code')}: {base_resp.get('status_msg')}")
    return parsed


def format_seconds(seconds: Optional[float]) -> str:
    if seconds is None:
        return "unknown"
    total_ms = int(round(seconds * 1000))
    minutes, ms_remainder = divmod(total_ms, 60_000)
    secs, ms = divmod(ms_remainder, 1000)
    return f"{minutes:02d}:{secs:02d}.{ms:03d}"


def speaker_alias_map(segments: List[Dict[str, Any]]) -> Dict[str, str]:
    aliases: Dict[str, str] = {}
    ordered = []
    for segment in segments:
        speaker = (segment.get("speaker") or "speaker_unknown").strip()
        if speaker not in aliases:
            ordered.append(speaker)
            aliases[speaker] = f"发言人{len(ordered)}"
    return aliases


def build_diarized_transcript(parsed: Dict[str, Any]) -> str:
    segments = parsed.get("segments") or []
    if not segments:
        return (parsed.get("text") or "").strip() + "\n"

    aliases = speaker_alias_map(segments)
    lines = []
    for segment in segments:
        start = format_seconds(segment.get("start"))
        end = format_seconds(segment.get("end"))
        speaker = aliases.get((segment.get("speaker") or "").strip(), "发言人")
        sentiment = segment.get("sentiment")
        text = (segment.get("text") or "").strip()
        suffix = f" [{sentiment}]" if sentiment else ""
        lines.append(f"[{start} - {end}] {speaker}{suffix}: {text}")
    return "\n".join(lines) + "\n"


def build_llm_input(audio_path: Path, parsed: Dict[str, Any], diarized_text: str) -> str:
    segments = parsed.get("segments") or []
    speaker_count = len({(item.get('speaker') or '').strip() for item in segments if item.get("speaker")})
    duration_seconds = parsed.get("duration")
    if duration_seconds is None:
        audio_info = parsed.get("audio_info") or {}
        duration_ms = audio_info.get("duration")
        if duration_ms is not None:
            duration_seconds = float(duration_ms) / 1000.0

    lines = [
        "# Academic Discussion Transcription Package",
        "",
        f"- Source file: {audio_path.name}",
        f"- ASR model: {DEFAULT_ASR_MODEL}",
        f"- Duration: {format_seconds(duration_seconds)}",
        f"- Speaker count detected: {speaker_count or 'unknown'}",
        "- Expected scene: research group meeting / advisor-student paper discussion / technical revision discussion",
        "- Role hint: prioritize identifying teacher/advisor and student/speaker roles when the context is clear",
        "",
        "## Full transcript",
        (parsed.get("text") or "").strip(),
        "",
        "## Speaker diarization transcript",
        diarized_text.strip(),
        "",
        "## Extraction guidance",
        "请把这段内容视为研究生组会、导师与学生讨论论文修改、或小规模技术讨论来处理。",
        "请优先识别老师/导师与学生/汇报者，并明确区分双方角色；若无法稳定判断，再保留发言人标签。",
        "请优先提炼老师提出的判断、修改意见、要求、标准和结论，再整理学生的提问、确认和后续执行动作。",
        "请特别关注：论文写作问题、技术逻辑问题、创新点表述、实验指标、修改要求、截止时间、待办事项、风险与未决问题。",
        "如果某项信息未明确提及，请标注“未明确提及”，不要编造。",
    ]
    return "\n".join(lines) + "\n"


def prepare_transcription_dir(audio_path: Path, output_dir: Optional[Path]) -> Path:
    if output_dir is not None:
        result = output_dir
    else:
        stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        result = OUTPUT_DIR / f"{audio_path.stem}-{stamp}"
    result.mkdir(parents=True, exist_ok=True)
    return result


def prepare_tts_output(output: Optional[str], output_format: str, source_dir: Optional[Path]) -> Path:
    if output:
        path = Path(output).expanduser()
        if not path.is_absolute():
            path = Path.cwd() / path
    else:
        base_dir = source_dir or OUTPUT_DIR
        base_dir.mkdir(parents=True, exist_ok=True)
        stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        path = base_dir / f"meeting-summary-{stamp}.{output_format}"

    if path.suffix.lower() != f".{output_format}":
        path = path.with_suffix(f".{output_format}")
    return path


def build_media_reference(path: Path) -> Optional[str]:
    try:
        relative = path.resolve().relative_to(Path.cwd().resolve())
    except ValueError:
        return None
    return f"MEDIA:./{relative.as_posix()}"


def validate_tts_params(
    *,
    text: str,
    output_format: str,
    sample_rate: int,
    bitrate: int,
    channel: int,
    speed: float,
    vol: float,
    pitch: int,
) -> None:
    if not text.strip():
        raise APIError("TTS 文本不能为空。")
    if len(text) > 10000:
        raise APIError("TTS 文本超过 10000 字符，请先压缩摘要或分段合成。")
    if output_format not in {"mp3", "wav", "pcm", "flac"}:
        raise APIError("`format` 必须是 mp3/wav/pcm/flac 之一。")
    if sample_rate not in {8000, 16000, 22050, 24000, 32000, 44100}:
        raise APIError("`sample_rate` 不在官方支持范围内。")
    if bitrate not in {32000, 64000, 128000, 256000}:
        raise APIError("`bitrate` 不在官方支持范围内。")
    if channel not in {1, 2}:
        raise APIError("`channel` 只能是 1 或 2。")
    if not 0.5 <= speed <= 2.0:
        raise APIError("`speed` 必须在 0.5 到 2.0 之间。")
    if not 0 <= vol <= 10:
        raise APIError("`vol` 必须在 0 到 10 之间。")
    if not -12 <= pitch <= 12:
        raise APIError("`pitch` 必须在 -12 到 12 之间。")


def print_json(data: Dict[str, Any]) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_auth_check(args: argparse.Namespace) -> int:
    client = SenseAudioClient(api_key=args.api_key, api_base=args.api_base)
    result = client.auth_check()
    print_json(result)
    return 0


def cmd_transcribe(args: argparse.Namespace) -> int:
    client = SenseAudioClient(api_key=args.api_key, api_base=args.api_base)
    result = client.transcribe(
        audio_path=Path(args.audio).expanduser(),
        language=args.language,
        max_speakers=args.max_speakers,
        enable_sentiment=not args.disable_sentiment,
        output_dir=Path(args.output_dir).expanduser() if args.output_dir else None,
    )
    print_json(
        {
            "output_dir": str(result.output_dir),
            "asr_verbose_json": str(result.json_path),
            "transcript_raw_txt": str(result.transcript_txt_path),
            "transcript_diarized_txt": str(result.diarized_txt_path),
            "llm_input_txt": str(result.llm_input_path),
            "speaker_segments": len(result.response_json.get("segments") or []),
        }
    )
    return 0


def cmd_tts(args: argparse.Namespace) -> int:
    client = SenseAudioClient(api_key=args.api_key, api_base=args.api_base)
    output_path = prepare_tts_output(args.output, args.format, None)
    result = client.synthesize(
        text=load_text_arg(args),
        output=output_path,
        voice_id=args.voice_id,
        output_format=args.format,
        sample_rate=args.sample_rate,
        bitrate=args.bitrate,
        channel=args.channel,
        speed=args.speed,
        vol=args.vol,
        pitch=args.pitch,
        save_meta=args.save_meta,
    )
    payload = {
        "audio_output": str(result.output_path),
        "meta_output": str(result.meta_path) if result.meta_path else None,
    }
    media_ref = build_media_reference(result.output_path)
    if media_ref:
        payload["media_ref"] = media_ref
    print_json(payload)
    if media_ref:
        print(media_ref)
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    client = SenseAudioClient(api_key=args.api_key, api_base=args.api_base)
    transcription = client.transcribe(
        audio_path=Path(args.audio).expanduser(),
        language=args.language,
        max_speakers=args.max_speakers,
        enable_sentiment=not args.disable_sentiment,
        output_dir=Path(args.output_dir).expanduser() if args.output_dir else None,
    )

    summary_text = load_text_arg(args)
    output_path = prepare_tts_output(args.output, args.format, transcription.output_dir)
    tts_result = client.synthesize(
        text=summary_text,
        output=output_path,
        voice_id=args.voice_id,
        output_format=args.format,
        sample_rate=args.sample_rate,
        bitrate=args.bitrate,
        channel=args.channel,
        speed=args.speed,
        vol=args.vol,
        pitch=args.pitch,
        save_meta=args.save_meta,
    )
    payload = {
        "output_dir": str(transcription.output_dir),
        "transcript_raw_txt": str(transcription.transcript_txt_path),
        "transcript_diarized_txt": str(transcription.diarized_txt_path),
        "llm_input_txt": str(transcription.llm_input_path),
        "summary_audio": str(tts_result.output_path),
        "summary_tts_meta": str(tts_result.meta_path) if tts_result.meta_path else None,
    }
    media_ref = build_media_reference(tts_result.output_path)
    if media_ref:
        payload["media_ref"] = media_ref
    print_json(payload)
    if media_ref:
        print(media_ref)
    return 0


def load_text_arg(args: argparse.Namespace) -> str:
    if getattr(args, "text", None):
        return args.text
    if getattr(args, "text_file", None):
        return Path(args.text_file).expanduser().read_text(encoding="utf-8").strip()
    raise APIError("需要通过 `--text` 或 `--text-file` 提供摘要文本。")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Meeting Assistant skill CLI")
    parser.add_argument("--api-key", help="覆盖环境变量中的 SENSEAUDIO_API_KEY")
    parser.add_argument("--api-base", help="覆盖环境变量中的 SENSEAUDIO_API_BASE")

    subparsers = parser.add_subparsers(dest="command", required=True)

    auth_check = subparsers.add_parser("auth-check", help="检查 SenseAudio API Key 是否可用")
    auth_check.set_defaults(func=cmd_auth_check)

    transcribe = subparsers.add_parser("transcribe", help="将会议录音转写为文本")
    transcribe.add_argument("--audio", required=True, help="本地会议录音路径")
    transcribe.add_argument("--language", default="zh", help="音频语言，默认 zh")
    transcribe.add_argument("--max-speakers", type=int, default=DEFAULT_MAX_SPEAKERS)
    transcribe.add_argument("--disable-sentiment", action="store_true")
    transcribe.add_argument("--output-dir", help="输出目录，默认自动创建")
    transcribe.set_defaults(func=cmd_transcribe)

    tts = subparsers.add_parser("tts", help="将摘要文本合成为语音")
    add_tts_args(tts)
    tts.set_defaults(func=cmd_tts)

    run_all = subparsers.add_parser("run", help="执行 ASR + 输出摘要语音")
    run_all.add_argument("--audio", required=True, help="本地会议录音路径")
    run_all.add_argument("--language", default="zh", help="音频语言，默认 zh")
    run_all.add_argument("--max-speakers", type=int, default=DEFAULT_MAX_SPEAKERS)
    run_all.add_argument("--disable-sentiment", action="store_true")
    run_all.add_argument("--output-dir", help="输出目录，默认自动创建")
    add_tts_args(run_all)
    run_all.set_defaults(func=cmd_run)

    return parser


def add_tts_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--text", help="直接提供待合成文本")
    parser.add_argument("--text-file", help="从文本文件读取待合成内容")
    parser.add_argument("--output", help="输出音频路径")
    parser.add_argument("--voice-id", default=DEFAULT_TTS_VOICE)
    parser.add_argument("--format", default=DEFAULT_OUTPUT_FORMAT, choices=["mp3", "wav", "pcm", "flac"])
    parser.add_argument("--sample-rate", type=int, default=DEFAULT_SAMPLE_RATE)
    parser.add_argument("--bitrate", type=int, default=DEFAULT_BITRATE)
    parser.add_argument("--channel", type=int, default=DEFAULT_CHANNEL)
    parser.add_argument("--speed", type=float, default=DEFAULT_SPEED)
    parser.add_argument("--vol", type=float, default=DEFAULT_VOL)
    parser.add_argument("--pitch", type=int, default=DEFAULT_PITCH)
    parser.add_argument("--save-meta", action="store_true")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except APIError as exc:
        print(f"错误: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("已取消。", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
