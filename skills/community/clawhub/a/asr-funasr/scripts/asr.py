#!/usr/bin/env python3
"""ASR — Speech-to-Text. Supports FunASR SenseVoice (Chinese-focused) and OpenAI Whisper (multilingual)."""

import argparse
import os
import re
import sys

# Ensure ffmpeg is available (use imageio-ffmpeg bundled binary if system ffmpeg missing)
try:
    import imageio_ffmpeg
    _ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    os.environ.setdefault("PATH", "")
    if _ffmpeg and not any(os.access(os.path.join(p, "ffmpeg"), os.X_OK) for p in os.environ.get("PATH", "").split(os.pathsep) if p):
        os.environ["PATH"] = os.path.dirname(_ffmpeg) + os.pathsep + os.environ.get("PATH", "")
except ImportError:
    pass

# Use comfyui-venv for dependencies
sys.path.insert(0, '/home/vincent/comfyui-venv/lib/python3.12/site-packages')


def clean_sensevoice_text(raw_text):
    """Remove SenseVoice special tokens like <|zh|><|HAPPY|><|Speech|><|woitn|>"""
    # Remove all <|...|> tokens
    text = re.sub(r'<\|[^|]*\|>', '', raw_text).strip()
    return text


def transcribe_funasr(input_file, language=None, output_file=None):
    """Transcribe using FunASR SenseVoice-Small (best for Chinese)."""
    try:
        from funasr import AutoModel
    except ImportError:
        print("❌ funasr not installed. Run: pip install funasr modelscope", file=sys.stderr)
        sys.exit(1)

    print(f"🎤 Loading FunASR SenseVoice-Small...")
    model = AutoModel(
        model='iic/SenseVoiceSmall',
        trust_remote_code=True,
        device='cuda:0',
    )

    print(f"📂 Input: {input_file}")

    kwargs = {}
    if language:
        kwargs['language'] = language
        print(f"🌐 Language: {language}")
    else:
        print(f"🌐 Language: auto-detect")

    print(f"⏳ Transcribing with SenseVoice...")
    result = model.generate(input=input_file, **kwargs)

    # Parse result
    raw_text = result[0]['text'] if result else ""
    clean = clean_sensevoice_text(raw_text)

    # Extract detected language from special tokens
    lang_match = re.search(r'<\|(\w+)\|>', raw_text)
    detected_lang = lang_match.group(1) if lang_match else "unknown"

    print(f"\n{'='*60}")
    print(f"Engine: FunASR SenseVoice-Small")
    print(f"Language detected: {detected_lang}")
    print(f"{'='*60}")
    print(clean)
    print(f"{'='*60}")

    if output_file:
        os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(clean)
        print(f"✅ Transcript saved: {output_file}")

    return clean


def transcribe_whisper(input_file, model_size="base", language=None, task="transcribe", output_file=None):
    """Transcribe using OpenAI Whisper (best for multilingual)."""
    try:
        import whisper
    except ImportError:
        print("❌ whisper not installed. Run: pip install openai-whisper", file=sys.stderr)
        sys.exit(1)

    print(f"🎤 Loading Whisper {model_size} model...")
    model = whisper.load_model(model_size)
    print(f"📂 Input: {input_file}")

    options = {"task": task}
    if language:
        options["language"] = language
        print(f"🌐 Language: {language}")
    else:
        print(f"🌐 Language: auto-detect")

    print(f"⏳ Transcribing with Whisper...")
    result = model.transcribe(input_file, **options)

    text = result["text"].strip()
    detected_lang = result.get("language", "unknown")

    print(f"\n{'='*60}")
    print(f"Engine: OpenAI Whisper ({model_size})")
    print(f"Language detected: {detected_lang}")
    print(f"Segments: {len(result.get('segments', []))}")
    print(f"{'='*60}")
    print(text)
    print(f"{'='*60}")

    if output_file:
        os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"✅ Transcript saved: {output_file}")

    return text


def main():
    parser = argparse.ArgumentParser(
        description="Speech-to-Text — FunASR SenseVoice (Chinese) + OpenAI Whisper (multilingual)")
    parser.add_argument("--input", required=True, help="Input audio file (mp3, wav, m4a, etc.)")
    parser.add_argument("--engine", default="funasr",
                        choices=["funasr", "whisper"],
                        help="ASR engine: funasr (SenseVoice, best Chinese) or whisper (multilingual)")
    parser.add_argument("--model", default=None,
                        help="Whisper model size: tiny, base, small, medium, large (whisper only, default: base)")
    parser.add_argument("--language", default=None,
                        help="Language code: zh, en, ja, ko, etc. — auto if omitted")
    parser.add_argument("--task", default="transcribe",
                        choices=["transcribe", "translate"],
                        help="transcribe or translate (whisper only)")
    parser.add_argument("--output", default=None, help="Write transcript to file")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"❌ File not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    if args.engine == "funasr":
        transcribe_funasr(args.input, args.language, args.output)
    else:
        model_size = args.model or "base"
        transcribe_whisper(args.input, model_size, args.language, args.task, args.output)


if __name__ == "__main__":
    main()
