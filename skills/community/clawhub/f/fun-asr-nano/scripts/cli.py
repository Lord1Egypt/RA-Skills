#!/usr/bin/env python3
#
# Copyright (c)  2025  zengyw
#
"""
Decode audio files using Fun-ASR-nano models with sherpa-onnx Python API.

This script demonstrates how to use Fun-ASR-nano models for offline speech recognition.

Usage:
    python offline-funasr-nano-decode-files.py \
        [--num-threads=4] \
        [--provider=cpu] \
        audio1.wav audio2.wav ...
"""

import argparse
import os
import sys
from pathlib import Path

import soundfile as sf
from modelscope import snapshot_download

try:
    import sherpa_onnx
except ImportError:
    print("Please install sherpa-onnx: pip install sherpa-onnx")
    sys.exit(1)


def get_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=__doc__,
    )

    parser.add_argument(
        "--system-prompt",
        type=str,
        default="You are a helpful assistant.",
        help="System prompt for FunASR-nano",
    )

    parser.add_argument(
        "--user-prompt",
        type=str,
        default="语音转写:",
        help="User prompt template for FunASR-nano",
    )

    parser.add_argument(
        "--max-new-tokens",
        type=int,
        default=512,
        help="Maximum number of new tokens to generate",
    )

    parser.add_argument(
        "--temperature",
        type=float,
        default=1e-6,
        help="Sampling temperature",
    )

    parser.add_argument(
        "--top-p",
        type=float,
        default=0.8,
        help="Top-p (nucleus) sampling threshold",
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed",
    )

    parser.add_argument(
        "--language",
        type=str,
        default="",
        help="Language for transcription (empty string means None)",
    )

    parser.add_argument(
        "--itn",
        action="store_true",
        default=True,
        help="Whether to apply inverse text normalization (default: True)",
    )

    parser.add_argument(
        "--no-itn",
        dest="itn",
        action="store_false",
        help="Disable inverse text normalization",
    )

    parser.add_argument(
        "--hotwords",
        type=str,
        default="",
        help="Hotwords (comma-separated, e.g., 'Sherpa,FunASR')",
    )

    parser.add_argument(
        "--num-threads",
        type=int,
        default=2,
        help="Number of threads for neural network computation",
    )

    parser.add_argument(
        "--provider",
        type=str,
        default="cpu",
        choices=["cpu", "cuda"],
        help="Provider: cpu or cuda",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="True to print model information while loading",
    )

    parser.add_argument(
        "sound_files",
        type=str,
        nargs="+",
        help="The input sound file(s) to decode. "
        "Each file must be of single channel, 16-bit PCM encoded wav file. "
        "Its sample rate can be arbitrary and does not need to be 16kHz.",
    )

    return parser.parse_args()


def create_recognizer(args) -> sherpa_onnx.OfflineRecognizer:
    model_dir = snapshot_download("pengzhendong/Fun-ASR-Nano-int8")
    return sherpa_onnx.OfflineRecognizer.from_funasr_nano(
        encoder_adaptor=os.path.join(model_dir, "encoder_adaptor.int8.onnx"),
        llm=os.path.join(model_dir, "llm.int8.onnx"),
        embedding=os.path.join(model_dir, "embedding.int8.onnx"),
        tokenizer=os.path.join(model_dir, "Qwen3-0.6B"),
        num_threads=args.num_threads,
        provider=args.provider,
        debug=args.debug,
        system_prompt=args.system_prompt,
        user_prompt=args.user_prompt,
        max_new_tokens=args.max_new_tokens,
        temperature=args.temperature,
        top_p=args.top_p,
        seed=args.seed,
        language=args.language,
        itn=args.itn,
        hotwords=args.hotwords,
    )


def decode_file(
    recognizer: sherpa_onnx.OfflineRecognizer,
    filename: str,
):
    """Decode a single audio file."""
    audio, sample_rate = sf.read(filename, dtype="float32", always_2d=True)
    audio = audio[:, 0]  # only use the first channel

    stream = recognizer.create_stream()
    stream.accept_waveform(sample_rate, audio)
    recognizer.decode_stream(stream)
    result = stream.result
    return result


def main():
    args = get_args()
    recognizer = create_recognizer(args)

    for sound_file in args.sound_files:
        if not Path(sound_file).exists():
            print(f"Error: File not found: {sound_file}", file=sys.stderr)
            continue

        result = decode_file(recognizer, sound_file)
        print(f"Text: {result.text}")
        if result.timestamps:
            print(f"Timestamps: {[round(t, 2) for t in result.timestamps]}")


if __name__ == "__main__":
    main()
