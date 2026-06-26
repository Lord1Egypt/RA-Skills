from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "common"))

from base import capability_catalog, config_contract, run_skill_script, usage_contract  # noqa: E402

SKILL_NAME = "chanjing-avatar"


def list():
    return capability_catalog(
        SKILL_NAME,
        manual="chanjing-avatar-SKILL.md",
        operations=[
            {"name": "get_upload_url", "script": "get_upload_url.py"},
            {"name": "upload_file", "script": "upload_file.py"},
            {"name": "create_task", "script": "create_task.py"},
            {"name": "poll_task", "script": "poll_task.py"},
            {"name": "create_video", "script": "create_video.py"},
            {"name": "poll_video", "script": "poll_video.py"},
        ],
    )


def config():
    return config_contract(
        preconditions=[],
        required=["video_file_id OR person_id", "audio_type"],
        optional=[
            "text",
            "audio_man_id",
            "audio_man",
            "audio_file_id",
            "wav_url",
            "screen_width",
            "screen_height",
            "model",
            "callback",
            "speed",
            "pitch",
            "bg_color",
            "bg_src_url",
            "subtitle_show",
            "figure_type",
            "drive_mode",
            "add_compliance_watermark",
            "resolution_rate",
        ],
    )


def usage():
    return usage_contract(
        examples=[
            "python scripts/upload_file.py --service lip_sync_video --file ./my_video.mp4",
            "python scripts/create_task.py --video-file-id <id> --text '你好' --audio-man-id <voice_id> --model 1",
            "python scripts/poll_task.py --id <task_id>",
            "python scripts/create_video.py --person-id <id> --person-x 0 --person-y 480 --person-width 1080 --person-height 1440 --text '你好' --audio-man <voice_id> --model 2 --bg-color '#EDEDED'",
            "python scripts/poll_video.py --id <video_id>",
        ],
        outputs=["file_id / task_id / video_id / video_url"],
    )


def upload_file(service: str, file_path: str):
    return run_skill_script(SKILL_NAME, "upload_file.py", args=["--service", service, "--file", file_path])


def create_task(args: list[str]):
    return run_skill_script(SKILL_NAME, "create_task.py", args=args)


def poll_task(task_id: str):
    return run_skill_script(SKILL_NAME, "poll_task.py", args=["--id", task_id])


def create_video(args: list[str]):
    return run_skill_script(SKILL_NAME, "create_video.py", args=args)


def poll_video(video_id: str):
    return run_skill_script(SKILL_NAME, "poll_video.py", args=["--id", video_id])

