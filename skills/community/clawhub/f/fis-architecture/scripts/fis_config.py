import os
from pathlib import Path

DEFAULT_SHARED_HUB_NAME = "fis-hub"


def get_skill_root() -> Path:
    return Path(__file__).parent.parent


def get_scripts_dir() -> Path:
    return Path(__file__).parent


def get_shared_hub_path(hub_name: str | None = None) -> Path:
    name = hub_name or DEFAULT_SHARED_HUB_NAME
    if "FIS_HUB_PATH" in os.environ:
        return Path(os.environ["FIS_HUB_PATH"])
    return Path.home() / ".openclaw" / name


def get_openclaw_base() -> Path:
    if "OPENCLAW_HOME" in os.environ:
        return Path(os.environ["OPENCLAW_HOME"])

    skill_root = get_skill_root()
    if "workspace" in str(skill_root):
        return skill_root.parent.parent.parent

    return Path.home() / ".openclaw"


def get_workspace_path(agent_id: str) -> Path:
    base = get_openclaw_base()

    workspace_map = {
        "researcher": "workspace-research",
        "engineer": "workspace-code",
        "writer": "workspace-writer",
        "main": "workspace",
        "cybermao": "workspace",
    }

    workspace_name = workspace_map.get(agent_id.lower(), f"workspace-{agent_id}")
    return base / workspace_name


def set_shared_hub_name(name: str):
    global DEFAULT_SHARED_HUB_NAME
    DEFAULT_SHARED_HUB_NAME = name


LEGACY_SHARED_HUB = get_openclaw_base() / "fis-hub"
