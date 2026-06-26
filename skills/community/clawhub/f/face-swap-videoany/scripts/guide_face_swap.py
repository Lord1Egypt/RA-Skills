#!/usr/bin/env python3
"""
Print guidance for VideoAny Face Swap workflow.
"""
import argparse
import sys

VIDEOANY_URL = "https://videoany.io/face-swap"
MODEL = "Half Moon AI"
VIDEO_FORMATS = ["MP4", "MOV", "WebM"]
FACE_FORMATS = ["JPG", "PNG", "WEBP"]
ASPECT_RATIOS = {"16:9", "1:1", "9:16"}
QUALITY_MODES = {"standard": "Standard"}
DURATION_OPTIONS = {"3", "5", "10"}


def _normalize(text: str) -> str:
    return "".join(ch for ch in text.lower() if ch.isalnum())


def _resolve_quality(mode: str) -> str:
    if not mode:
        return QUALITY_MODES["standard"]
    key = _normalize(mode)
    for short, full in QUALITY_MODES.items():
        if key in {_normalize(short), _normalize(full)}:
            return full
    print(
        "Warning: unsupported --quality value. Choose one of: "
        + ", ".join(sorted(QUALITY_MODES)),
        file=sys.stderr,
    )
    return QUALITY_MODES["standard"]


def _resolve_aspect_ratio(ratio: str) -> str:
    if not ratio:
        return "16:9"
    if ratio in ASPECT_RATIOS:
        return ratio
    print(
        "Warning: unsupported --aspect-ratio value. Choose one of: "
        + ", ".join(sorted(ASPECT_RATIOS)),
        file=sys.stderr,
    )
    return "16:9"


def _resolve_duration(duration: str) -> str:
    if not duration:
        return "5"
    if duration in DURATION_OPTIONS:
        return duration
    print(
        "Warning: unsupported --duration value. Choose one of: "
        + ", ".join(sorted(DURATION_OPTIONS)),
        file=sys.stderr,
    )
    return "5"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Guide users to VideoAny Face Swap page and recommended inputs."
    )
    parser.add_argument("--video", default="", help="Optional local source video path")
    parser.add_argument("--video-url", default="", help="Optional source video URL")
    parser.add_argument(
        "--face-image", default="", help="Optional local source face image path"
    )
    parser.add_argument("--face-url", default="", help="Optional source face image URL")
    parser.add_argument(
        "--aspect-ratio",
        default="16:9",
        help="Aspect ratio: 16:9, 1:1, 9:16",
    )
    parser.add_argument(
        "--duration",
        default="5",
        help="Duration option in seconds: 3, 5, 10",
    )
    parser.add_argument(
        "--quality",
        default="standard",
        help="Quality mode. Currently supported: standard",
    )
    parser.add_argument("--notes", default="", help="Optional face swap notes")
    args = parser.parse_args()

    selected_aspect_ratio = _resolve_aspect_ratio(args.aspect_ratio)
    selected_duration = _resolve_duration(args.duration)
    selected_quality = _resolve_quality(args.quality)

    print("VideoAny Face Swap")
    print(f"URL: {VIDEOANY_URL}")
    print("Summary: Create AI face swap videos from source video + face image.")
    print("Model: " + MODEL)
    print("Video formats: " + ", ".join(VIDEO_FORMATS))
    print("Face image formats: " + ", ".join(FACE_FORMATS))
    print("Aspect ratios: " + ", ".join(sorted(ASPECT_RATIOS)))
    print("Duration options: 3s, 5s, 10s (minimum length hint: 3s)")
    print("Quality mode: " + selected_quality)
    print("Credits: scale with video duration")
    print("Selected aspect ratio: " + selected_aspect_ratio)
    print("Selected duration: " + selected_duration + "s")

    if args.video or args.video_url or args.face_image or args.face_url or args.notes:
        print("\nSuggested input for the web workflow:")
        if args.video:
            print(f"- Source video: {args.video}")
        if args.video_url:
            print(f"- Source video URL: {args.video_url}")
        if args.face_image:
            print(f"- Face image: {args.face_image}")
        if args.face_url:
            print(f"- Face image URL: {args.face_url}")
        if args.notes:
            print(f"- Notes: {args.notes}")
    else:
        print("\nSuggested workflow:")
        print("- Upload a clear source clip with a visible front-facing face")
        print("- Use a well-lit face image with similar angle/expression")
        print("- Start with short clips to validate realism before longer runs")
        print("- If artifacts appear, try a different face image and simpler scenes")

    print("\nResponsible use reminders:")
    print("- Use only media you own or are explicitly authorized to edit")
    print("- Do not produce deceptive impersonation or non-consensual deepfakes")
    print("- Follow content policy and applicable laws")

    print("\nNext step: open the URL above and run generation on VideoAny web.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
