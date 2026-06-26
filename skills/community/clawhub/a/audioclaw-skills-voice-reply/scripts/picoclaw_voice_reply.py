#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
for parent in SCRIPT_DIR.parents:
    candidate = parent / "_shared" / "audioclaw_paths.py"
    if candidate.exists():
        candidate_dir = str(candidate.parent)
        if candidate_dir not in sys.path:
            sys.path.insert(0, candidate_dir)
        break

from audioclaw_paths import get_workspace_root

SWITCHBOARD_SCRIPT = SCRIPT_DIR / "openclaw_voice_switchboard.py"
FEISHU_AUDIO_SENDER = SCRIPT_DIR / "feishu_audio_sender.py"
DEFAULT_WORKSPACE = get_workspace_root()


def run_switchboard(args: list[str], env: dict) -> dict:
    command = [sys.executable, str(SWITCHBOARD_SCRIPT), *args]
    completed = subprocess.run(command, capture_output=True, text=True, env=env, check=False)
    if completed.returncode != 0:
        message = completed.stderr.strip() or completed.stdout.strip() or "switchboard failed"
        raise SystemExit(message)
    stdout = completed.stdout.strip()
    if not stdout:
        raise SystemExit("switchboard returned no manifest")
    return json.loads(stdout)


def run_feishu_audio_sender(args: list[str], env: dict) -> dict:
    command = [sys.executable, str(FEISHU_AUDIO_SENDER), *args]
    completed = subprocess.run(command, capture_output=True, text=True, env=env, check=False)
    if completed.returncode != 0:
        message = completed.stderr.strip() or completed.stdout.strip() or "feishu audio sender failed"
        raise SystemExit(message)
    stdout = completed.stdout.strip()
    if not stdout:
        raise SystemExit("feishu audio sender returned no result")
    return json.loads(stdout)


def main() -> int:
    parser = argparse.ArgumentParser(description="PicoClaw one-step voice reply wrapper for Feishu/Lark.")
    parser.add_argument("--text", required=True)
    parser.add_argument("--scene", default="assistant")
    parser.add_argument("--emotion", default="calm")
    parser.add_argument("--voice-id")
    parser.add_argument("--voice-family")
    parser.add_argument("--speed", type=float)
    parser.add_argument("--pitch", type=int)
    parser.add_argument("--volume", type=float)
    parser.add_argument("--preference-key")
    parser.add_argument("--reply-mode")
    parser.add_argument(
        "--workspace-root",
        default=(
            os.getenv("AUDIOCLAW_WORKSPACE")
            or os.getenv("PICOCLAW_WORKSPACE")
            or str(DEFAULT_WORKSPACE)
        ),
    )
    parser.add_argument("--delivery-profile", default="feishu_voice", choices=["default", "feishu_voice"])
    parser.add_argument("--api-key-env", default="SENSEAUDIO_API_KEY")
    parser.add_argument("--chat-id")
    parser.add_argument("--session-file")
    parser.add_argument("--config-path")
    parser.add_argument("--skip-direct-send", action="store_true")
    args = parser.parse_args()

    env = os.environ.copy()
    workspace_root = Path(args.workspace_root).expanduser()
    switchboard_args = [
        "--text", args.text,
        "--scene", args.scene,
        "--emotion", args.emotion,
        "--delivery-profile", args.delivery_profile,
        "--openclaw-workspace-root", str(workspace_root),
        "--api-key-env", args.api_key_env,
    ]
    optional_values = {
        "--voice-id": args.voice_id,
        "--voice-family": args.voice_family,
        "--speed": args.speed,
        "--pitch": args.pitch,
        "--volume": args.volume,
        "--preference-key": args.preference_key,
        "--reply-mode": args.reply_mode,
    }
    for flag, value in optional_values.items():
        if value is not None:
            switchboard_args.extend([flag, str(value)])

    manifest = run_switchboard(switchboard_args, env)
    media_ref = ((manifest.get("delivery") or {}).get("openclaw_media_reference") or "").strip()
    if not media_ref:
        raise SystemExit("switchboard did not return an OpenClaw media reference")

    audio_path = ((manifest.get("audio") or {}).get("path") or "")
    duration_ms = (((manifest.get("audio") or {}).get("extra_info") or {}).get("audio_length"))
    if args.skip_direct_send or args.delivery_profile != "feishu_voice":
        payload = {
            "mode": "send_file_audio",
            "send_file_tool_arguments": {
                "path": audio_path,
            },
            "audio_path": audio_path,
            "media_reference": media_ref,
            "trace_id": ((manifest.get("audio") or {}).get("trace_id") or ""),
            "resolved_voice_id": ((manifest.get("resolved") or {}).get("voice_id") or ""),
            "delivery_profile": ((manifest.get("delivery") or {}).get("delivery_profile") or ""),
            "instructions": [
                "Call the `send_file` tool with `send_file_tool_arguments.path`.",
                "Do not send the local path or the MEDIA reference as a text message.",
                "Do not call the `message` tool unless you need an extra caption after the file is sent.",
                "Treat `media_reference` as OpenClaw-compatible metadata only, not as the primary PicoClaw delivery path.",
            ],
            "manifest": manifest,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    sender_args = [
        "--audio-path", audio_path,
        "--workspace-root", str(workspace_root),
    ]
    if duration_ms:
        sender_args.extend(["--duration-ms", str(duration_ms)])
    if args.chat_id:
        sender_args.extend(["--chat-id", args.chat_id])
    if args.session_file:
        sender_args.extend(["--session-file", args.session_file])
    if args.config_path:
        sender_args.extend(["--config-path", args.config_path])

    send_result = run_feishu_audio_sender(sender_args, env)
    payload = {
        "mode": "feishu_audio_sent",
        "audio_path": audio_path,
        "media_reference": media_ref,
        "trace_id": ((manifest.get("audio") or {}).get("trace_id") or ""),
        "resolved_voice_id": ((manifest.get("resolved") or {}).get("voice_id") or ""),
        "delivery_profile": ((manifest.get("delivery") or {}).get("delivery_profile") or ""),
        "chat_id": send_result.get("chat_id") or "",
        "message_id": (((send_result.get("send") or {}).get("data") or {}).get("message_id") or ""),
        "instructions": [
            "The Feishu audio message is already sent.",
            "Do not call the `send_file` tool for this audio again.",
            "Do not send the MEDIA reference as text.",
            "Prefer no follow-up confirmation text after the audio.",
            "If the host runtime still requires one final assistant message, send one short natural Chinese line such as: 我已经用语音回复你了。",
        ],
        "send_result": send_result,
        "manifest": manifest,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
