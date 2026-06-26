#!/usr/bin/env python3
"""
colab_tts.py — Text-to-speech via F5-TTS on Google Colab GPU.

Uses a reference voice sample for zero-shot voice cloning.

Usage:
    # Generate speech
    python3 colab_tts.py speak "Hello Eric" --output hello.wav
    
    # Generate with specific reference
    python3 colab_tts.py speak "Hello" --ref-audio voice_sample.wav --ref-text "reference text"
    
    # Download voice samples from ElevenLabs
    python3 colab_tts.py fetch-voice --voice-id YOUR_VOICE_ID --api-key YOUR_API_KEY
"""

import argparse
import base64
import json
import os
import sys
import time

VENV_PYTHON = os.path.join(os.path.dirname(__file__), ".colab-venv", "bin", "python")
if os.path.exists(VENV_PYTHON) and sys.executable != VENV_PYTHON:
    os.execv(VENV_PYTHON, [VENV_PYTHON] + sys.argv)

import requests

VOICE_DIR = os.path.expanduser("~/.openclaw/private/ren-voice/")

# ─── ElevenLabs voice sample download ───────────────────────────────────────

def fetch_voice_samples(voice_id: str, api_key: str):
    """Download voice samples from ElevenLabs."""
    os.makedirs(VOICE_DIR, exist_ok=True)
    
    headers = {"xi-api-key": api_key}
    resp = requests.get(f"https://api.elevenlabs.io/v1/voices/{voice_id}", headers=headers)
    resp.raise_for_status()
    voice = resp.json()
    
    print(f"Voice: {voice.get('name', 'unknown')}")
    print(f"Category: {voice.get('category', 'unknown')}")
    
    samples = voice.get("samples", [])
    if not samples:
        print("No samples found. Generating a reference sample via TTS...")
        # Generate a reference clip using ElevenLabs itself
        gen_resp = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            headers={**headers, "Content-Type": "application/json"},
            json={
                "text": "Hello, I'm Ren. I'm a research assistant who helps with mathematics, coding, and all sorts of intellectual adventures. Nice to meet you.",
                "model_id": "eleven_multilingual_v3",
                "voice_settings": {"stability": 0.36, "similarity_boost": 0.82, "style": 0.42}
            }
        )
        gen_resp.raise_for_status()
        ref_path = os.path.join(VOICE_DIR, "ren_reference.mp3")
        with open(ref_path, "wb") as f:
            f.write(gen_resp.content)
        print(f"Generated reference: {ref_path} ({len(gen_resp.content)} bytes)")
        
        # Also save the reference text
        with open(os.path.join(VOICE_DIR, "ren_reference.txt"), "w") as f:
            f.write("Hello, I'm Ren. I'm a research assistant who helps with mathematics, coding, and all sorts of intellectual adventures. Nice to meet you.")
        return
    
    for i, sample in enumerate(samples):
        sample_id = sample.get("sample_id", f"sample_{i}")
        file_name = sample.get("file_name", f"sample_{i}.mp3")
        
        # Download sample audio
        dl_resp = requests.get(
            f"https://api.elevenlabs.io/v1/voices/{voice_id}/samples/{sample_id}/audio",
            headers=headers
        )
        dl_resp.raise_for_status()
        
        out_path = os.path.join(VOICE_DIR, file_name)
        with open(out_path, "wb") as f:
            f.write(dl_resp.content)
        print(f"  Downloaded: {out_path} ({len(dl_resp.content)} bytes)")


# ─── Colab TTS execution ────────────────────────────────────────────────────

F5_TTS_SETUP = """
import subprocess, sys, os

# Install F5-TTS if not present
try:
    import f5_tts
    print("F5-TTS already installed")
except ImportError:
    print("Installing F5-TTS...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "f5-tts[eval]"])
    print("F5-TTS installed")

import torch
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
"""

F5_TTS_GENERATE = """
import base64, json, os, sys, time

# Upload reference audio (base64-encoded)
ref_audio_b64 = {ref_audio_b64!r}
ref_text = {ref_text!r}
target_text = {target_text!r}

ref_path = "/tmp/ref_audio.wav"
with open(ref_path, "wb") as f:
    f.write(base64.b64decode(ref_audio_b64))
print(f"Reference audio: {{os.path.getsize(ref_path)}} bytes")

from f5_tts.api import F5TTS
import soundfile as sf

t0 = time.time()
tts = F5TTS(model_type="F5-TTS", ckpt_file="", vocab_file="")
print(f"Model loaded in {{time.time()-t0:.1f}}s")

t1 = time.time()
wav, sr, _ = tts.infer(
    ref_file=ref_path,
    ref_text=ref_text,
    gen_text=target_text,
)
gen_time = time.time() - t1
print(f"Generated in {{gen_time:.1f}}s, sample rate={{sr}}, samples={{len(wav)}}")

# Save and encode output
out_path = "/tmp/tts_output.wav"
sf.write(out_path, wav, sr)
with open(out_path, "rb") as f:
    audio_b64 = base64.b64encode(f.read()).decode()

duration = len(wav) / sr
print(f"Duration: {{duration:.1f}}s, RTF: {{gen_time/duration:.2f}}")
print("__AUDIO__" + audio_b64)
"""


def speak(text: str, ref_audio_path: str, ref_text: str, output_path: str, gpu: str = "T4"):
    """Generate speech on Colab using F5-TTS."""
    from colab_run import ColabRuntime, get_session, format_outputs
    
    # Read and encode reference audio
    with open(ref_audio_path, "rb") as f:
        ref_audio_b64 = base64.b64encode(f.read()).decode()
    
    session = get_session()
    rt = ColabRuntime(session, gpu=gpu)
    
    print("Assigning GPU VM...", file=sys.stderr)
    info = rt.assign()
    print(f"Assigned: {info.get('endpoint', '?')} (accelerator={info.get('accelerator', '?')})", file=sys.stderr)
    
    print("Connecting to kernel...", file=sys.stderr)
    rt.connect_kernel()
    
    # Step 1: Install F5-TTS
    print("Installing F5-TTS...", file=sys.stderr)
    result = rt.execute(F5_TTS_SETUP)
    print(format_outputs(result), file=sys.stderr)
    
    # Step 2: Generate speech
    print(f"Generating speech: '{text[:50]}...'", file=sys.stderr)
    code = F5_TTS_GENERATE.format(
        ref_audio_b64=ref_audio_b64,
        ref_text=ref_text,
        target_text=text,
    )
    result = rt.execute(code)
    output = format_outputs(result)
    
    # Extract audio
    if "__AUDIO__" in output:
        audio_b64 = output.split("__AUDIO__")[1].strip()
        audio_bytes = base64.b64decode(audio_b64)
        with open(output_path, "wb") as f:
            f.write(audio_bytes)
        print(f"Saved: {output_path} ({len(audio_bytes)} bytes)", file=sys.stderr)
        # Print info lines (before __AUDIO__)
        for line in output.split("__AUDIO__")[0].strip().split("\n"):
            if line.strip():
                print(line)
    else:
        print(output)
        print("ERROR: No audio output found", file=sys.stderr)
    
    rt.stop()


# ─── CLI ─────────────────────────────────────────────────────────────────────

def cmd_fetch_voice(args):
    fetch_voice_samples(args.voice_id, args.api_key)


def cmd_speak(args):
    ref_audio = args.ref_audio
    ref_text = args.ref_text
    
    # Default to saved reference
    if not ref_audio:
        ref_audio = os.path.join(VOICE_DIR, "ren_reference.mp3")
        if not os.path.exists(ref_audio):
            print(f"No reference audio found at {ref_audio}", file=sys.stderr)
            print("Run: python3 colab_tts.py fetch-voice --voice-id ... --api-key ...", file=sys.stderr)
            sys.exit(1)
    
    if not ref_text:
        ref_text_path = os.path.join(VOICE_DIR, "ren_reference.txt")
        if os.path.exists(ref_text_path):
            with open(ref_text_path) as f:
                ref_text = f.read().strip()
        else:
            ref_text = ""
    
    output = args.output or "/tmp/tts_output.wav"
    speak(args.text, ref_audio, ref_text, output, gpu=args.gpu or "T4")


def main():
    parser = argparse.ArgumentParser(description="TTS via F5-TTS on Colab")
    sub = parser.add_subparsers(dest="command")
    
    p_fetch = sub.add_parser("fetch-voice", help="Download voice samples from ElevenLabs")
    p_fetch.add_argument("--voice-id", required=True)
    p_fetch.add_argument("--api-key", required=True)
    p_fetch.set_defaults(func=cmd_fetch_voice)
    
    p_speak = sub.add_parser("speak", help="Generate speech")
    p_speak.add_argument("text", help="Text to speak")
    p_speak.add_argument("--ref-audio", help="Reference audio file")
    p_speak.add_argument("--ref-text", help="Reference audio transcript")
    p_speak.add_argument("--output", "-o", help="Output wav file")
    p_speak.add_argument("--gpu", default="T4", help="GPU type (T4, L4, A100)")
    p_speak.set_defaults(func=cmd_speak)
    
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)
    args.func(args)


if __name__ == "__main__":
    main()
