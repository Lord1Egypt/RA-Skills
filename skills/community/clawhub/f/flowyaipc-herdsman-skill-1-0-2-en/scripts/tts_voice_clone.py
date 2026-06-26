#!/usr/bin/env python3
"""
Voice cloning TTS synthesis script: clone voices using Herdsman qwen3-tts-voiceclone.
Clones voice based on reference audio and reference text, then synthesizes target script.

Usage:
    uv run python tts_voice_clone.py <ref_audio> <ref_text> <target_text> [--output <path>]

Parameters:
    ref_audio   - Reference audio WAV path (must be 16kHz/mono WAV)
    ref_text    - Original text corresponding to the reference audio
    target_text - Target text for synthesis
    --output    - Output audio path (optional, default ripple_tts_cloned.wav)

Dependencies:
    - Herdsman service running (http://127.0.0.1:8080)
    - qwen3-tts-voiceclone model started

Output:
    WAV format cloned voice file
"""

import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.error


def build_payload(ref_audio_path: str, ref_text: str, target_text: str) -> dict:
    """Build the qwen3-tts-voiceclone API request payload."""

    try:
        with open(ref_audio_path, "rb") as f:
            audio_bytes = f.read()
    except FileNotFoundError:
        print(f"Error: reference audio file not found -> {ref_audio_path}", file=sys.stderr)
        sys.exit(1)

    audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

    payload = {
        "model": "qwen3-tts-voiceclone",
        "input": target_text,
        "ref_audio": f"data:audio/wav;base64,{audio_b64}",
        "ref_text": ref_text,
        "language": "Chinese",
        "speed": 1.0,
        "stream": False
    }
    return payload


def call_tts_api(payload: dict, timeout: int = 180) -> dict:
    """Call the Herdsman OpenAI-compatible TTS endpoint."""

    url = "http://127.0.0.1:8080/v1/audio/speech"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer "
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"API request failed (HTTP {e.code}): {body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"API connection failed: {e.reason}\nEnsure Herdsman service is running at http://127.0.0.1:8080", file=sys.stderr)
        sys.exit(1)

    # Try JSON parsing (data URL mode)
    try:
        result = json.loads(raw.decode("utf-8"))
        return result
    except json.JSONDecodeError:
        pass

    # Return WAV binary directly (standard OpenAI TTS response)
    return {"_raw_wav": raw}


def save_audio(result: dict, output_path: str) -> str:
    """Extract and save audio from API response."""

    # Standard response: return WAV binary directly
    if "_raw_wav" in result:
        with open(output_path, "wb") as f:
            f.write(result["_raw_wav"])
        print(f"Cloned voice saved: {output_path} ({len(result['_raw_wav'])} bytes)")
        return output_path

    # data URL mode
    audio_b64 = result.get("audio_url", "")
    if not audio_b64:
        print(f"Error: no audio data found in response\n{json.dumps(result, indent=2, ensure_ascii=False)}", file=sys.stderr)
        sys.exit(1)

    if audio_b64.startswith("data:audio/wav;base64,"):
        audio_b64 = audio_b64[len("data:audio/wav;base64,"):]

    # Fix base64 padding
    padding = 4 - len(audio_b64) % 4
    if padding != 4:
        audio_b64 += "=" * padding

    audio_bytes = base64.b64decode(audio_b64)
    with open(output_path, "wb") as f:
        f.write(audio_bytes)

    print(f"Cloned voice saved: {output_path} ({len(audio_bytes)} bytes)")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Herdsman Voice Clone Synthesis Script")
    parser.add_argument("ref_audio", help="Reference audio WAV file path")
    parser.add_argument("ref_text", help="Original text of the reference audio")
    parser.add_argument("target_text", help="Target text to synthesize")
    parser.add_argument("--output", "-o", default="ripple_tts_cloned.wav", help="Output audio file path")
    parser.add_argument("--timeout", type=int, default=180, help="API timeout in seconds")

    args = parser.parse_args()

    # Validate reference audio
    if not os.path.isfile(args.ref_audio):
        print(f"Error: reference audio file not found -> {args.ref_audio}", file=sys.stderr)
        sys.exit(1)

    # Ensure output directory exists
    out_dir = os.path.dirname(args.output)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    # Build payload
    payload = build_payload(args.ref_audio, args.ref_text, args.target_text)

    print("Calling Herdsman voice clone API...")
    result = call_tts_api(payload, timeout=args.timeout)

    # Save result
    saved = save_audio(result, args.output)

    # Try to get duration info via ffprobe (if available)
    try:
        import subprocess
        probe = subprocess.run(
            ["ffprobe", "-v", "quiet", "-show_entries",
             "format=duration,bit_rate", "-of", "csv=p=0", saved],
            capture_output=True, text=True, timeout=10
        )
        if probe.returncode == 0 and probe.stdout.strip():
            parts = probe.stdout.strip().split(",")
            dur = parts[0]
            br = parts[1] if len(parts) > 1 else "?"
            print(f"Duration: {dur}s | Bitrate: {br} bps")
    except Exception:
        pass


if __name__ == "__main__":
    main()