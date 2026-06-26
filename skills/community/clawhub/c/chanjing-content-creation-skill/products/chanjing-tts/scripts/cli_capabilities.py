from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "common"))

from base import capability_catalog, config_contract, run_skill_script, usage_contract  # noqa: E402

SKILL_NAME = "chanjing-tts"


def list():
    return capability_catalog(
        SKILL_NAME,
        manual="chanjing-tts-SKILL.md",
        operations=[
            {"name": "list_voices", "script": "list_voices.py"},
            {"name": "create_task", "script": "create_task.py"},
            {"name": "poll_task", "script": "poll_task.py"},
        ],
    )


def config():
    return config_contract(
        preconditions=["使用 UTF-8 文本"],
        required=["text", "audio_man"],
        optional=["speed", "pitch"],
    )


def usage():
    return usage_contract(
        examples=[
            "python skills/chanjing-content-creation-skill/products/chanjing-tts/scripts/list_voices.py --json",
            "python skills/chanjing-content-creation-skill/products/chanjing-tts/scripts/create_task.py --audio-man <id> --text '你好'",
            "python skills/chanjing-content-creation-skill/products/chanjing-tts/scripts/poll_task.py --task-id <id>",
        ],
        outputs=["voice list / task_id / audio_url"],
    )


def list_voices(json_output: bool = False):
    args = ["--json"] if json_output else []
    return run_skill_script(SKILL_NAME, "list_voices.py", args=args)


def create_task(audio_man: str, text: str, speed: float | None = None, pitch: float | None = None):
    args = ["--audio-man", audio_man, "--text", text]
    if speed is not None:
        args += ["--speed", str(speed)]
    if pitch is not None:
        args += ["--pitch", str(pitch)]
    return run_skill_script(SKILL_NAME, "create_task.py", args=args)


def poll_task(task_id: str):
    return run_skill_script(SKILL_NAME, "poll_task.py", args=["--task-id", task_id])

