from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "common"))

from base import capability_catalog, config_contract, run_skill_script, usage_contract  # noqa: E402

SKILL_NAME = "chanjing-text-to-digital-person"


def list():
    return capability_catalog(
        SKILL_NAME,
        manual="chanjing-text-to-digital-person-SKILL.md",
        operations=[
            {"name": "create_photo_task", "script": "create_photo_task.py"},
            {"name": "poll_photo_task", "script": "poll_photo_task.py"},
            {"name": "create_motion_task", "script": "create_motion_task.py"},
            {"name": "poll_motion_task", "script": "poll_motion_task.py"},
            {"name": "create_lora_task", "script": "create_lora_task.py"},
            {"name": "poll_lora_task", "script": "poll_lora_task.py"},
        ],
    )


def config():
    return config_contract(
        preconditions=[],
        required=["photo prompt fields 或 lora photo urls"],
        optional=["motion params", "download_result"],
    )


def usage():
    return usage_contract(
        examples=[
            "python skills/chanjing-content-creation-skill/products/chanjing-text-to-digital-person/scripts/create_photo_task.py --age 'Young adult' --gender Female --number-of-images 1",
            "python skills/chanjing-content-creation-skill/products/chanjing-text-to-digital-person/scripts/poll_photo_task.py --unique-id <photo_id>",
            "python skills/chanjing-content-creation-skill/products/chanjing-text-to-digital-person/scripts/create_motion_task.py --photo-unique-id <photo_id> --photo-path <url>",
        ],
        outputs=["photo_unique_id / motion_unique_id / image_url / video_url"],
    )


def create_photo_task(args: list[str]):
    return run_skill_script(SKILL_NAME, "create_photo_task.py", args=args)


def poll_photo_task(unique_id: str):
    return run_skill_script(SKILL_NAME, "poll_photo_task.py", args=["--unique-id", unique_id])


def create_motion_task(args: list[str]):
    return run_skill_script(SKILL_NAME, "create_motion_task.py", args=args)


def poll_motion_task(unique_id: str):
    return run_skill_script(SKILL_NAME, "poll_motion_task.py", args=["--unique-id", unique_id])

