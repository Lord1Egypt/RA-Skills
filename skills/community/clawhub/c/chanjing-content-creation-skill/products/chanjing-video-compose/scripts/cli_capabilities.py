from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "common"))

from base import capability_catalog, config_contract, run_skill_script, usage_contract  # noqa: E402

SKILL_NAME = "chanjing-video-compose"


def list():
    return capability_catalog(
        SKILL_NAME,
        manual="chanjing-video-compose-SKILL.md",
        operations=[
            {"name": "list_figures", "script": "list_figures.py"},
            {"name": "list_tag_dict", "script": "list_tag_dict.py"},
            {"name": "upload_file", "script": "upload_file.py"},
            {"name": "create_task", "script": "create_task.py"},
            {"name": "poll_task", "script": "poll_task.py"},
            {"name": "download_result", "script": "download_result.py"},
        ],
    )


def config():
    return config_contract(
        preconditions=["创建任务前明确字幕 show/hide"],
        required=["source", "person_id"],
        optional=["figure_type", "audio_man_id", "audio_file_id", "subtitle"],
    )


def usage():
    return usage_contract(
        examples=[
            "python skills/chanjing-content-creation-skill/products/chanjing-video-compose/scripts/list_tag_dict.py --business-type 1 --json",
            "python skills/chanjing-content-creation-skill/products/chanjing-video-compose/scripts/list_figures.py --source common --fetch-all --page-size 80 --json",
            "python skills/chanjing-content-creation-skill/products/chanjing-video-compose/scripts/list_figures.py --source common --tag-ids 23,41 --fetch-all --page-size 80 --json",
            "python skills/chanjing-content-creation-skill/products/chanjing-video-compose/scripts/create_task.py --person-id <id> --audio-man <voice_id> --subtitle hide --text '你好'",
            "python skills/chanjing-content-creation-skill/products/chanjing-video-compose/scripts/poll_task.py --id <video_id>",
        ],
        outputs=["figure list / video_id / video_url"],
    )


def list_figures(source: str, json_output: bool = False, page_size: int | None = None, max_pages: int | None = None):
    args = ["--source", source]
    if page_size is not None:
        args += ["--page-size", str(page_size)]
    if max_pages is not None:
        args += ["--max-pages", str(max_pages)]
    if json_output:
        args.append("--json")
    return run_skill_script(SKILL_NAME, "list_figures.py", args=args)


def create_task(args: list[str]):
    return run_skill_script(SKILL_NAME, "create_task.py", args=args)


def poll_task(video_id: str):
    return run_skill_script(SKILL_NAME, "poll_task.py", args=["--id", video_id])

