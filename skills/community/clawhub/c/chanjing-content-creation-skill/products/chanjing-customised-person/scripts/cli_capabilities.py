from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "common"))

from base import capability_catalog, config_contract, run_skill_script, usage_contract  # noqa: E402

SKILL_NAME = "chanjing-customised-person"


def list():
    return capability_catalog(
        SKILL_NAME,
        manual="chanjing-customised-person-SKILL.md",
        operations=[
            {"name": "upload_file", "script": "upload_file.py"},
            {"name": "create_person", "script": "create_person.py"},
            {"name": "list_persons", "script": "list_persons.py"},
            {"name": "get_person", "script": "get_person.py"},
            {"name": "poll_person", "script": "poll_person.py"},
            {"name": "delete_person", "script": "delete_person.py"},
        ],
    )


def config():
    return config_contract(
        preconditions=[],
        required=["file_id", "name"],
        optional=["train_type", "id"],
    )


def usage():
    return usage_contract(
        examples=[
            "python skills/chanjing-content-creation-skill/products/chanjing-customised-person/scripts/upload_file.py --file ./source.mp4",
            "python skills/chanjing-content-creation-skill/products/chanjing-customised-person/scripts/create_person.py --name '演示数字人' --file-id <file_id> --train-type figure",
            "python skills/chanjing-content-creation-skill/products/chanjing-customised-person/scripts/poll_person.py --id <person_id>",
        ],
        outputs=["file_id / person_id / preview_url"],
    )


def upload_file(file_path: str):
    return run_skill_script(SKILL_NAME, "upload_file.py", args=["--file", file_path])


def create_person(args: list[str]):
    return run_skill_script(SKILL_NAME, "create_person.py", args=args)


def get_person(person_id: str):
    return run_skill_script(SKILL_NAME, "get_person.py", args=["--id", person_id])


def poll_person(person_id: str):
    return run_skill_script(SKILL_NAME, "poll_person.py", args=["--id", person_id])

