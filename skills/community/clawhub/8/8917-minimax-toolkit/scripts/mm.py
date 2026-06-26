#!/usr/bin/env python3
"""
MiniMax Toolkit - Unified CLI Entry
"""

import sys
import os
import json
import base64
import binascii
import argparse
from pathlib import Path

scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir))

from minimax_client import MinimaxClient, get_standard_path
from executor_common import (
    execute_image, execute_video, execute_speech, execute_async_speech,
    execute_music, execute_i2i, execute_voice_clone, execute_voice_design,
    execute_video_template, _download_and_save,
)
import check_official_docs

FEATURE_FLAGS_PATH = scripts_dir.parent / "references" / "feature_flags.json"


def load_feature_flags():
    try:
        with open(FEATURE_FLAGS_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {"modality_enabled": {}}


MODALITIES = {
    "image": {"description": "Generate image from text prompt", "executor": execute_image, "default_model": "image-01", "needs_input": True},
    "i2i": {"description": "Transform reference image with style prompt", "executor": execute_i2i, "default_model": "image-01", "needs_input": True},
    "video": {"description": "Generate video from text prompt", "executor": execute_video, "default_model": "MiniMax-Hailuo-02", "needs_input": True},
    "video-template": {"description": "Generate video using template", "executor": execute_video_template, "default_model": None, "needs_input": True},
    "speech": {"description": "Short text to speech synthesis", "executor": execute_speech, "default_model": "speech-2.8-hd", "needs_input": True},
    "async-speech": {"description": "Long text async speech synthesis", "executor": execute_async_speech, "default_model": "speech-2.8-hd", "needs_input": True},
    "voice-clone": {"description": "Clone voice from audio sample", "executor": execute_voice_clone, "default_model": "speech-2.8-hd", "needs_input": True},
    "voice-design": {"description": "Design voice from text description", "executor": execute_voice_design, "default_model": None, "needs_input": True},
    "music": {"description": "Generate music from prompt", "executor": execute_music, "default_model": "music-2.5+", "needs_input": True},
    "remains": {"description": "Show official Token Plan remains report", "executor": None, "default_model": None, "needs_input": False},
    "check-docs": {"description": "Check official docs and compare with local references", "executor": None, "default_model": None, "needs_input": False},
}


def main():
    parser = argparse.ArgumentParser(
        description="MiniMax Toolkit - Unified CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scripts/mm.py image "A red apple" --project Demo
  python3 scripts/mm.py i2i "anime style" --ref ~/photo.jpg --project Demo
  python3 scripts/mm.py async-speech ~/script.txt --voice male-qn-qingse --project Demo
  python3 scripts/mm.py video-template labubu --media ~/photo.jpg --project Demo
  python3 scripts/mm.py voice-clone ~/voice.wav --voice-id my-voice --preview-text "你好，这是试听文本"
  python3 scripts/mm.py voice-design "Warm deep male voice" --preview-text "你好，这是试听文本"
  python3 scripts/mm.py remains
  python3 scripts/mm.py check-docs
        """.strip()
    )

    parser.add_argument("modality", choices=list(MODALITIES.keys()), help="Modality or utility command to use")
    parser.add_argument("prompt_or_text", nargs="?", help="Text prompt, file path, template name, or other input")

    parser.add_argument("--project", help="Project name for subdirectory organization")
    parser.add_argument("--output-dir", help="Override output root directory")
    parser.add_argument("--estimate", action="store_true", help="Only estimate cost, don't execute")

    parser.add_argument("--ref", help="Reference image path (for i2i)")
    parser.add_argument("--voice", default="male-qn-qingse", help="Voice ID (for speech)")
    parser.add_argument("--speed", type=float, default=1.0, help="Speech speed")
    parser.add_argument("--ratio", default="1:1", help="Aspect ratio (for image/i2i)")
    parser.add_argument("--model", help="Override model name")
    parser.add_argument("--instrumental", action="store_true", help="Generate instrumental (for music)")
    parser.add_argument("--voice-id", help="Voice ID for clone/design")
    parser.add_argument("--media", help="Media path for video-template")
    parser.add_argument("--template", help="Template name for video-template")
    parser.add_argument("--text", help="Template text input")
    parser.add_argument("--lyrics", help="Lyrics for music generation")
    parser.add_argument("--format", default="mp3", choices=["mp3", "pcm", "flac", "wav"], help="Audio format for async speech")
    parser.add_argument("--prompt-audio", help="Optional prompt audio for voice clone")
    parser.add_argument("--prompt-text", help="Prompt text corresponding to --prompt-audio")
    parser.add_argument("--preview-text", help="Preview text for voice clone/design")

    args = parser.parse_args()
    modality_info = MODALITIES[args.modality]
    feature_flags = load_feature_flags()
    enabled_map = feature_flags.get("modality_enabled", {})
    notes_map = feature_flags.get("notes", {})

    if enabled_map.get(args.modality, True) is False:
        note = notes_map.get(args.modality, "This modality is currently disabled.")
        print(f"Error: modality '{args.modality}' is disabled. {note}", file=sys.stderr)
        sys.exit(1)

    try:
        client = MinimaxClient()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.modality == "remains":
        print(client.format_plan_remains_report())
        return
    if args.modality == "check-docs":
        check_official_docs.main()
        return

    if modality_info["needs_input"] and not args.prompt_or_text:
        print(f"Error: modality '{args.modality}' requires prompt_or_text input", file=sys.stderr)
        sys.exit(1)

    executor = modality_info["executor"]
    model = args.model or modality_info["default_model"]
    result = executor(
        client=client,
        prompt_or_text=args.prompt_or_text,
        model=model,
        project=args.project,
        output_dir=args.output_dir,
        estimate_only=args.estimate,
        extra_args={
            "ref": args.ref,
            "voice": args.voice,
            "speed": args.speed,
            "ratio": args.ratio,
            "instrumental": args.instrumental,
            "voice_id": args.voice_id,
            "media": args.media,
            "template": args.template,
            "text": args.text,
            "lyrics": args.lyrics,
            "format": args.format,
            "prompt_audio": args.prompt_audio,
            "prompt_text": args.prompt_text,
            "preview_text": args.preview_text,
        }
    )

    if result.get("error"):
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)
    if result.get("filepath"):
        print(f"Success! Saved to: {result['filepath']}")
        print(f"MEDIA:{result['filepath']}")
    elif result.get("voice_id"):
        print(f"Success! Voice ID: {result['voice_id']}")
        if result.get("demo_audio"):
            audio_url = result["demo_audio"]
            target_dir, filename_base = get_standard_path("TTS", project=args.project, prompt_slug="voice_clone", output_dir=args.output_dir)
            filepath = os.path.join(target_dir, f"{filename_base}.mp3")
            try:
                # demo_audio is a URL, download it
                if audio_url.startswith('http'):
                    import requests
                    resp = requests.get(audio_url, timeout=60)
                    resp.raise_for_status()
                    with open(filepath, 'wb') as f:
                        f.write(resp.content)
                    print(f"Demo audio saved to: {filepath}")
                    print(f"MEDIA:{filepath}")
                else:
                    # Fallback to hex/base64 decode
                    if all(c in '0123456789abcdefABCDEF' for c in audio_url[:100]):
                        audio_bytes = bytes.fromhex(audio_url)
                    else:
                        audio_bytes = base64.b64decode(audio_url)
                    with open(filepath, 'wb') as f:
                        f.write(audio_bytes)
                    print(f"Demo audio saved to: {filepath}")
                    print(f"MEDIA:{filepath}")
            except Exception as e:
                print(f"Error saving demo audio: {e}")
        if result.get("trial_audio"):
            audio_data = result["trial_audio"]
            target_dir, filename_base = get_standard_path("TTS", project=args.project, prompt_slug="voice_design", output_dir=args.output_dir)
            filepath = os.path.join(target_dir, f"{filename_base}.mp3")
            try:
                # trial_audio can be hex-encoded (newer API) or base64-encoded (older)
                # Detect by checking if it's all hex characters
                if all(c in '0123456789abcdefABCDEF' for c in audio_data[:100]):
                    # Hex encoded
                    audio_bytes = bytes.fromhex(audio_data)
                else:
                    # Base64 encoded
                    audio_bytes = base64.b64decode(audio_data)
                with open(filepath, 'wb') as f:
                    f.write(audio_bytes)
                print(f"Trial audio saved to: {filepath}")
                print(f"MEDIA:{filepath}")
            except Exception as e:
                print(f"Error saving trial audio: {e}")
    elif result.get("task_id"):
        print(f"Task created! ID: {result['task_id']}")
        if result.get("suggested_path"):
            print(f"Suggested output: {result['suggested_path']}")


if __name__ == "__main__":
    main()
