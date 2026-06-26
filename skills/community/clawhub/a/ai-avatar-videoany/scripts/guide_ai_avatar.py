#!/usr/bin/env python3
"""
Print guidance for VideoAny AI Avatar workflow.
"""
import argparse
import sys

VIDEOANY_URL = "https://videoany.io/tools/ai-avatar"
IMAGE_FORMATS = ["JPG", "PNG", "WebP"]
AUDIO_FORMATS = ["MP3", "WAV", "OGG", "M4A"]
SUPPORTED_MODES = {"standard": "Standard (Balanced quality)"}
AUDIO_DURATION_HINT = "2-60s"


def _normalize(text: str) -> str:
    return "".join(ch for ch in text.lower() if ch.isalnum())


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Guide users to VideoAny AI Avatar page and recommended inputs."
    )
    parser.add_argument(
        "--avatar-image", default="", help="Optional local avatar image path"
    )
    parser.add_argument(
        "--image-url", default="", help="Optional avatar image URL for web input"
    )
    parser.add_argument("--audio", default="", help="Optional local audio path")
    parser.add_argument(
        "--audio-id",
        default="",
        help="Optional uploaded audio_id (audio file or audio_id is required on web)",
    )
    parser.add_argument(
        "--script",
        default="",
        help="Optional script text. Voice audio can work without script.",
    )
    parser.add_argument(
        "--mode",
        default="standard",
        help="Generation mode. Currently supported: standard",
    )
    args = parser.parse_args()

    mode_key = _normalize(args.mode)
    selected_mode = SUPPORTED_MODES.get(mode_key, "")
    if not selected_mode:
        print(
            "Warning: unsupported --mode value. Choose one of: "
            + ", ".join(sorted(SUPPORTED_MODES)),
            file=sys.stderr,
        )
        selected_mode = SUPPORTED_MODES["standard"]

    print("VideoAny AI Avatar")
    print(f"URL: {VIDEOANY_URL}")
    print("Summary: Create a talking AI avatar from a portrait and voice.")
    print("Image input: upload image or use avatar image URL")
    print("Image formats: " + ", ".join(IMAGE_FORMATS))
    print(
        "Audio input: upload audio or use audio_id (one is required), duration hint "
        + AUDIO_DURATION_HINT
    )
    print("Audio formats: " + ", ".join(AUDIO_FORMATS) + " (or record)")
    print("Script prompt: optional")
    print("Credits: based on audio duration")
    print("Mode: " + selected_mode)

    if args.avatar_image or args.image_url or args.audio or args.audio_id or args.script:
        print("\nSuggested input for the web workflow:")
        if args.avatar_image:
            print(f"- Avatar image: {args.avatar_image}")
        if args.image_url:
            print(f"- Avatar image URL: {args.image_url}")
        if args.audio:
            print(f"- Audio file: {args.audio}")
        if args.audio_id:
            print(f"- Audio ID: {args.audio_id}")
        if args.script:
            print(f"- Script: {args.script}")
    else:
        print("\nSuggested workflow:")
        print("- Prepare one clear, front-facing portrait")
        print("- Prepare clean speech audio (low background noise)")
        print("- Start with short generation first, then extend if needed")

    print("\nResponsible use reminders:")
    print("- Use only image/voice content you own or are authorized to use")
    print("- Do not create deceptive deepfakes or non-consensual impersonations")
    print("- Follow platform policy and applicable laws")

    print("\nNext step: open the URL above and run generation on VideoAny web.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
