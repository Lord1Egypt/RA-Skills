#!/usr/bin/env python3
"""Azure Speech TTS helper.

Supports plain text or SSML input, writes audio to a local file, and prints a
small JSON summary on success.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from urllib import error, request
from xml.sax.saxutils import escape

SKILL_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = SKILL_ROOT / "config.json"
DEFAULT_CONFIG = {
    "default_voice": "zh-CN-Yunqi:DragonHDOmniLatestNeural",
    "default_format": "mp3",
    "default_output_dir": "download",
    "default_timeout_seconds": 60,
}

TOKEN_URL_TEMPLATE = "https://{region}.api.cognitive.microsoft.com/sts/v1.0/issuetoken"
SYNTHESIS_URL_TEMPLATE = (
    "https://{region}.tts.speech.microsoft.com/cognitiveservices/v1"
)
DEFAULT_FORMAT = "audio-24khz-48kbitrate-mono-mp3"
FORMAT_ALIASES = {
    "mp3": DEFAULT_FORMAT,
    "wav": "riff-24khz-16bit-mono-pcm",
    "pcm": "raw-16khz-16bit-mono-pcm",
    "ogg": "ogg-24khz-16bit-mono-opus",
}
EXT_BY_FORMAT = {
    "audio-16khz-32kbitrate-mono-mp3": ".mp3",
    "audio-16khz-128kbitrate-mono-mp3": ".mp3",
    "audio-24khz-48kbitrate-mono-mp3": ".mp3",
    "audio-24khz-96kbitrate-mono-mp3": ".mp3",
    "riff-16khz-16bit-mono-pcm": ".wav",
    "riff-24khz-16bit-mono-pcm": ".wav",
    "raw-16khz-16bit-mono-pcm": ".pcm",
    "ogg-24khz-16bit-mono-opus": ".ogg",
}


@dataclass
class InputSpec:
    kind: str  # "text" or "ssml"
    content: str


def load_skill_config() -> dict[str, object]:
    config = dict(DEFAULT_CONFIG)
    if CONFIG_PATH.exists():
        try:
            loaded = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Invalid config.json: {exc}") from exc
        if not isinstance(loaded, dict):
            raise SystemExit("config.json must contain a JSON object.")
        for key, value in loaded.items():
            if value is not None:
                config[key] = value
    return config


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate audio with Azure Speech TTS.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--text", help="Plain text to synthesize.")
    group.add_argument("--text-file", help="Path to a UTF-8 text file.")
    group.add_argument("--ssml", help="Raw SSML payload to synthesize.")
    group.add_argument("--ssml-file", help="Path to a UTF-8 SSML file.")

    parser.add_argument("--voice", help="Azure voice name, e.g. zh-CN-Yunqi:DragonHDOmniLatestNeural.")
    parser.add_argument(
        "--language",
        help="SSML language tag for plain text mode. Defaults to the voice prefix.",
    )
    parser.add_argument(
        "--format",
        help="Azure output format or short alias (mp3, wav, pcm, ogg).",
    )
    parser.add_argument(
        "--style",
        help="Optional speaking style for supported neural voices (e.g. cheerful, sad, chat).",
    )
    parser.add_argument(
        "--style-degree",
        type=float,
        default=None,
        help="Optional style degree for expressive voices.",
    )
    parser.add_argument("--role", help="Optional style role, e.g. YoungAdultFemale.")
    parser.add_argument("--rate", help="Optional speaking rate, e.g. +10%% or 1.1.")
    parser.add_argument("--pitch", help="Optional pitch, e.g. +2st or -5%%.")
    parser.add_argument("--output", help="Exact output file path.")
    parser.add_argument(
        "--output-dir",
        help="Directory used when --output is not provided.",
    )
    parser.add_argument(
        "--filename",
        help="Filename used with --output-dir. Defaults to a timestamped name.",
    )
    parser.add_argument(
        "--save-ssml",
        help="Write the generated SSML to this path for debugging.",
    )
    parser.add_argument(
        "--key",
        default=os.getenv("AZURE_SPEECH_KEY"),
        help="Azure Speech subscription key. Defaults to AZURE_SPEECH_KEY.",
    )
    parser.add_argument(
        "--region",
        default=os.getenv("AZURE_SPEECH_REGION"),
        help="Azure Speech region, e.g. eastasia. Defaults to AZURE_SPEECH_REGION.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the generated SSML and exit without calling Azure.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        help="HTTP timeout in seconds.",
    )
    return parser.parse_args()


def read_text_value(path: str | None, direct: str | None) -> str | None:
    if direct is not None:
        return direct
    if path is None:
        return None
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def read_input(args: argparse.Namespace) -> InputSpec:
    if args.ssml is not None or args.ssml_file is not None:
        content = read_text_value(args.ssml_file, args.ssml)
        if not content or not content.strip():
            raise SystemExit("SSML input is empty.")
        return InputSpec(kind="ssml", content=content.strip())

    content = read_text_value(args.text_file, args.text)
    if content is None:
        if sys.stdin.isatty():
            raise SystemExit("Provide --text, --text-file, --ssml, --ssml-file, or pipe input.")
        content = sys.stdin.read()
    if not content or not content.strip():
        raise SystemExit("Text input is empty.")
    return InputSpec(kind="text", content=content.strip())


def normalize_format(fmt: str) -> str:
    return FORMAT_ALIASES.get(fmt.lower(), fmt)


def output_extension(fmt: str) -> str:
    fmt = normalize_format(fmt)
    return EXT_BY_FORMAT.get(fmt, Path(fmt).suffix or ".audio")


def infer_language(voice: str | None) -> str:
    if not voice:
        return "en-US"
    parts = voice.split("-")
    if len(parts) >= 2:
        return f"{parts[0]}-{parts[1]}"
    return "en-US"


def split_paragraphs(text: str) -> list[str]:
    paras = [p.strip() for p in text.replace("\r\n", "\n").replace("\r", "\n").split("\n\n")]
    return [p for p in paras if p]


def build_text_ssml(
    text: str,
    voice: str,
    language: str,
    rate: str | None,
    pitch: str | None,
    style: str | None,
    style_degree: float | None,
    role: str | None,
) -> str:
    voice_lang = language or infer_language(voice)
    body = []
    paragraphs = split_paragraphs(text)
    for paragraph in paragraphs:
        escaped = escape(" ".join(line.strip() for line in paragraph.splitlines()))
        body.append(f"<p>{escaped}</p>")

    inner = "".join(body)
    if rate or pitch:
        prosody_attrs = []
        if rate:
            prosody_attrs.append(f'rate="{escape(rate)}"')
        if pitch:
            prosody_attrs.append(f'pitch="{escape(pitch)}"')
        inner = f"<prosody {' '.join(prosody_attrs)}>{inner}</prosody>"
    if style:
        attrs = [f'style="{escape(style)}"']
        if style_degree is not None:
            attrs.append(f'styledegree="{style_degree}"')
        if role:
            attrs.append(f'role="{escape(role)}"')
        inner = f"<mstts:express-as {' '.join(attrs)}>{inner}</mstts:express-as>"
    elif role:
        inner = f'<mstts:express-as role="{escape(role)}">{inner}</mstts:express-as>'

    return (
        f"<speak version='1.0' xml:lang='{escape(voice_lang)}' "
        "xmlns='http://www.w3.org/2001/10/synthesis' "
        "xmlns:mstts='http://www.w3.org/2001/mstts'>"
        f"<voice name='{escape(voice)}'>{inner}</voice>"
        "</speak>"
    )


def maybe_wrap_ssml(ssml: str) -> str:
    stripped = ssml.strip()
    if not stripped.lower().startswith("<speak"):
        raise SystemExit("SSML input must include a <speak> root element.")
    return stripped


def fetch_token(region: str, key: str, timeout: int) -> str:
    url = TOKEN_URL_TEMPLATE.format(region=region)
    req = request.Request(
        url,
        method="POST",
        headers={"Ocp-Apim-Subscription-Key": key},
    )
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8")
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Token request failed: {exc.code} {exc.reason}: {body}") from exc


def synthesize(
    region: str,
    token: str,
    ssml: str,
    audio_format: str,
    timeout: int,
) -> bytes:
    url = SYNTHESIS_URL_TEMPLATE.format(region=region)
    req = request.Request(
        url,
        data=ssml.encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": audio_format,
            "User-Agent": "openclaw-azure-speech-tts",
        },
    )
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Synthesis failed: {exc.code} {exc.reason}: {body}") from exc


def default_output_path(
    output: str | None,
    output_dir: str,
    filename: str | None,
    fmt: str,
    voice: str,
) -> Path:
    if output:
        return Path(output).expanduser()
    out_dir = Path(output_dir).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_voice = "".join(c if c.isalnum() or c in {"-", "_"} else "-" for c in voice)
        filename = f"azure_speech_{safe_voice}_{timestamp}{output_extension(fmt)}"
    else:
        filename = filename if Path(filename).suffix else f"{filename}{output_extension(fmt)}"
    return out_dir / filename


def main() -> int:
    args = parse_args()
    config = load_skill_config()
    input_spec = read_input(args)

    voice = args.voice or os.getenv("AZURE_SPEECH_VOICE") or str(
        config.get("default_voice", DEFAULT_CONFIG["default_voice"])
    )
    audio_format = normalize_format(
        args.format
        or os.getenv("AZURE_SPEECH_FORMAT")
        or str(config.get("default_format", DEFAULT_CONFIG["default_format"]))
    )
    output_dir = args.output_dir or str(
        config.get("default_output_dir", DEFAULT_CONFIG["default_output_dir"])
    )
    timeout = args.timeout if args.timeout is not None else int(
        config.get("default_timeout_seconds", DEFAULT_CONFIG["default_timeout_seconds"])
    )
    language = args.language or str(config.get("default_language", "")) or infer_language(voice)

    ssml = (
        maybe_wrap_ssml(input_spec.content)
        if input_spec.kind == "ssml"
        else build_text_ssml(
            input_spec.content,
            voice,
            language,
            args.rate,
            args.pitch,
            args.style,
            args.style_degree,
            args.role,
        )
    )

    if args.save_ssml:
        Path(args.save_ssml).expanduser().parent.mkdir(parents=True, exist_ok=True)
        Path(args.save_ssml).expanduser().write_text(ssml, encoding="utf-8")

    if args.dry_run:
        print(ssml)
        return 0

    if not args.key:
        raise SystemExit("Missing Azure key. Set AZURE_SPEECH_KEY or pass --key.")
    if not args.region:
        raise SystemExit("Missing Azure region. Set AZURE_SPEECH_REGION or pass --region.")

    out_path = default_output_path(args.output, output_dir, args.filename, audio_format, voice)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    token = fetch_token(args.region, args.key, timeout)
    audio = synthesize(args.region, token, ssml, audio_format, timeout)
    out_path.write_bytes(audio)

    result = {
        "ok": True,
        "output_path": str(out_path),
        "format": audio_format,
        "voice": voice,
        "language": language,
        "bytes": len(audio),
    }
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
