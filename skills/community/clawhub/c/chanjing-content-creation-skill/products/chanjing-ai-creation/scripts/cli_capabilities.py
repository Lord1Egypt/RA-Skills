from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "common"))

from base import capability_catalog, config_contract, run_skill_script, usage_contract  # noqa: E402

SKILL_NAME = "chanjing-ai-creation"


def list():
    return capability_catalog(
        SKILL_NAME,
        manual="chanjing-ai-creation-SKILL.md",
        operations=[
            {"name": "submit_task", "script": "submit_task.py"},
            {"name": "get_task", "script": "get_task.py"},
            {"name": "list_tasks", "script": "list_tasks.py"},
            {"name": "poll_task", "script": "poll_task.py"},
            {"name": "download_result", "script": "download_result.py"},
        ],
    )


def config():
    return config_contract(
        preconditions=[],
        required=["creation_type", "model_code"],
        optional=["prompt", "ref_img_url", "body_file", "body_json"],
    )


def usage():
    return usage_contract(
        examples=[
            "python skills/chanjing-content-creation-skill/products/chanjing-ai-creation/scripts/submit_task.py --creation-type 3 --model-code doubao-seedream-3.0-t2i --prompt '赛博朋克城市夜景'",
            "python skills/chanjing-content-creation-skill/products/chanjing-ai-creation/scripts/poll_task.py --unique-id <task_id>",
        ],
        outputs=["unique_id / task detail / output_url"],
    )


def submit_task(args: list[str]):
    return run_skill_script(SKILL_NAME, "submit_task.py", args=args)


def get_task(unique_id: str):
    return run_skill_script(SKILL_NAME, "get_task.py", args=["--unique-id", unique_id])


def list_tasks(args: list[str] | None = None):
    return run_skill_script(SKILL_NAME, "list_tasks.py", args=args or [])


def poll_task(unique_id: str):
    return run_skill_script(SKILL_NAME, "poll_task.py", args=["--unique-id", unique_id])

