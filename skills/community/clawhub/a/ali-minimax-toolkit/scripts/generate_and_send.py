#!/usr/bin/env python3
"""
MiniMax Generate & Send — Generate multimedia content and send to Feishu.

Usage:
    python generate_and_send.py tts "Hello world" --voice female-shaonv --feishu-chat <chat_id>
    python generate_and_send.py music "soft piano" --instrumental --feishu-chat <chat_id>
    python generate_and_send.py image "A cute cat" --ratio 16:9 --feishu-chat <chat_id>
    python generate_and_send.py video "Dog running" --feishu-chat <chat_id>

After generation, prints the file path so the agent can send via feishu-media skill.
Set FEISHU_CHAT_ID env var to auto-print the feishu-media command.
"""

import argparse
import json
import os
import sys

# Add skill scripts dir to path so we can import minimax_api
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import minimax_api


def main():
    parser = argparse.ArgumentParser(description="Generate with MiniMax and prepare for Feishu send")
    parser.add_argument("type", choices=["tts", "music", "image", "i2i", "video"],
                        help="Generation type")
    parser.add_argument("prompt", help="Text prompt for generation")
    parser.add_argument("-o", "--output", default="", help="Output file path")
    parser.add_argument("--feishu-chat", default="", help="Feishu chat/group ID to send to")
    parser.add_argument("--caption", default="", help="Caption text for the message")

    # TTS args
    parser.add_argument("--voice", default="female-shaonv", help="TTS voice ID")
    parser.add_argument("--emotion", default="", help="TTS emotion")
    parser.add_argument("--tts-model", default="speech-2.8-hd", help="TTS model")

    # Music args
    parser.add_argument("--lyrics", default="", help="Music lyrics")
    parser.add_argument("--instrumental", action="store_true", help="Instrumental music")
    parser.add_argument("--music-model", default="music-2.5", help="Music model")

    # Image args
    parser.add_argument("--ratio", default="1:1", help="Image aspect ratio")
    parser.add_argument("--count", type=int, default=1, help="Number of images")
    parser.add_argument("--image-model", default="image-01", help="Image model")
    parser.add_argument("--optimize", action="store_true", help="Prompt optimizer")
    parser.add_argument("--ref-image", default="", help="Reference image for i2i")

    # Video args
    parser.add_argument("--mode", default="t2v", help="Video mode: t2v, i2v, sef, ref")
    parser.add_argument("--first-frame", default="", help="Video first frame")
    parser.add_argument("--subject", default="", help="Video subject reference")
    parser.add_argument("--video-model", default="MiniMax-Hailuo-2.3", help="Video model")
    parser.add_argument("--max-wait", type=int, default=600, help="Max wait for video")

    args = parser.parse_args()

    # Auto-generate output path
    if not args.output:
        out_dir = os.environ.get("MINIMAX_OUTPUT_DIR", "minimax-output")
        if args.type == "tts":
            ext, name = ".mp3", "tts"
        elif args.type == "music":
            ext, name = ".mp3", "music"
        elif args.type in ("image", "i2i"):
            ext, name = ".png", "image"
        elif args.type == "video":
            ext, name = ".mp4", "video"
        else:
            ext, name = ".bin", "output"
        import uuid
        short_id = uuid.uuid4().hex[:8]
        args.output = os.path.join(out_dir, "{}_{}".format(name, short_id) + ext)

    chat_id = args.feishu_chat or os.environ.get("FEISHU_CHAT_ID", "")

    try:
        result = None

        if args.type == "tts":
            result = minimax_api.generate_tts(
                args.prompt, output=args.output, voice_id=args.voice,
                emotion=args.emotion, model=args.tts_model,
            )

        elif args.type == "music":
            result = minimax_api.generate_music(
                args.prompt, output=args.output, lyrics=args.lyrics,
                instrumental=args.instrumental, model=args.music_model,
            )

        elif args.type == "image":
            result = minimax_api.generate_image(
                args.prompt, output=args.output, aspect_ratio=args.ratio,
                count=args.count, model=args.image_model,
                prompt_optimizer=args.optimize,
            )

        elif args.type == "i2i":
            if not args.ref_image:
                print("ERROR: --ref-image required for i2i mode", file=sys.stderr)
                sys.exit(1)
            result = minimax_api.image_to_image(
                args.prompt, args.ref_image, output=args.output,
                aspect_ratio=args.ratio, count=args.count,
            )

        elif args.type == "video":
            result = minimax_api.generate_video(
                args.prompt, output=args.output, mode=args.mode,
                first_frame=args.first_frame, subject_image=args.subject,
                model=args.video_model, max_wait=args.max_wait,
            )

        # Determine the actual file path(s) generated
        if isinstance(result, list):
            paths = [r.get("path", "") for r in result if r.get("path")]
        elif isinstance(result, dict):
            paths = [r for r in [result.get("path", "")] if r]
        elif isinstance(result, str):
            paths = [result]
        else:
            paths = []

        print("\n--- Generation Complete ---")
        for p in paths:
            print("File: {}".format(os.path.abspath(p)))

        if chat_id:
            print("\n--- Feishu Send ---")
            print("To send to Feishu chat '{}', use the feishu-media skill:".format(chat_id))
            for p in paths:
                print('  Send file "{}" to chat "{}"{}'.format(
                    p, chat_id,
                    ' with caption "{}"'.format(args.caption) if args.caption else "",
                ))
            # Also output machine-readable JSON for agent consumption
            print("\n__FEISHU_SEND__")
            send_info = {"chat_id": chat_id, "files": paths, "caption": args.caption}
            print(json.dumps(send_info))
        else:
            print("\nTip: Set --feishu-chat or FEISHU_CHAT_ID env var to auto-generate send commands.")

    except Exception as e:
        print("ERROR: {}".format(e), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
