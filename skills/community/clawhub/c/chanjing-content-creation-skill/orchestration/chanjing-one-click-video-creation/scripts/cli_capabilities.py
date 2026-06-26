from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "common"))

from base import capability_catalog, config_contract, run_skill_script, usage_contract  # noqa: E402

SKILL_NAME = "chanjing-one-click-video-creation"


def list():
    return capability_catalog(
        SKILL_NAME,
        manual="chanjing-one-click-video-creation-SKILL.md",
        operations=[
            {"name": "run_render", "script": "run_render.py"},
            {
                "name": "validate_ai_resolution",
                "script": "validate_ai_resolution.py",
            },
            {"name": "workflow_contract", "script": "workflow.json / workflow_result.json"},
        ],
    )


def config():
    return config_contract(
        preconditions=["本机存在 ffmpeg 与 ffprobe"],
        required=["topic 或 workflow.json"],
        optional=["output_dir", "CHAN_SKILLS_DIR", "max_retry_per_step"],
    )


def usage():
    return usage_contract(
        examples=[
            "python skills/chanjing-content-creation-skill/orchestration/chanjing-one-click-video-creation/scripts/run_render.py --input workflow.json --output-dir output/run1",
            "python .../scripts/validate_ai_resolution.py --input workflow.json --check-ref-prompt",
        ],
        outputs=["final_one_click.mp4 / workflow_result.json / work/"],
    )


def run_render(input_file: str, output_dir: str = ""):
    args = ["--input", input_file]
    if output_dir:
        args.extend(["--output-dir", output_dir])
    return run_skill_script(
        SKILL_NAME,
        "run_render.py",
        args=args,
    )

