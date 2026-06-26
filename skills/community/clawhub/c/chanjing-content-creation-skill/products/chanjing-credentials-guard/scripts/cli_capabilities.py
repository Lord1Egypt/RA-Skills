from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "common"))

from base import capability_catalog, config_contract, run_skill_script, usage_contract  # noqa: E402

SKILL_NAME = "chanjing-credentials-guard"


def list():
    return capability_catalog(
        SKILL_NAME,
        manual="chanjing-credentials-guard-SKILL.md",
        operations=[
            {"name": "open_login_page", "script": "open_login_page.py"},
            {"name": "status", "script": "chanjing_config.py --status"},
            {"name": "set_credentials", "script": "chanjing_config.py --app-id ... --sk ..."},
            {"name": "run_print_access_token_script", "script": "chanjing_get_token.py"},
        ],
    )


def config():
    return config_contract(
        preconditions=["在任何蝉镜 API 调用前先运行本 skill"],
        required=[],
        optional=["app_id", "sk"],
    )


def usage():
    return usage_contract(
        examples=[
            "python skills/chanjing-content-creation-skill/products/chanjing-credentials-guard/scripts/chanjing_config.py --status",
            "python skills/chanjing-content-creation-skill/products/chanjing-credentials-guard/scripts/open_login_page.py",
        ],
        outputs=["status JSON / access_token / 用户配置提示"],
    )


def status():
    return run_skill_script(SKILL_NAME, "chanjing_config.py", args=["--status"])


def set_credentials(app_id: str, sk: str):
    return run_skill_script(
        SKILL_NAME, "chanjing_config.py", args=["--app-id", app_id, "--sk", sk]
    )


def open_login_page():
    return run_skill_script(SKILL_NAME, "open_login_page.py")


def run_print_access_token_script():
    return run_skill_script(SKILL_NAME, "chanjing_get_token.py")

