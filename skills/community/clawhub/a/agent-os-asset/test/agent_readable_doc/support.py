from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
from types import ModuleType


def find_skill_root() -> Path:
    """Find the nested child Skill without depending on a fixed parent depth."""
    for parent in Path(__file__).resolve().parents:
        candidate = parent / "skills" / "agent-readable-doc"
        if (candidate / "SKILL.md").is_file():
            return candidate
    raise RuntimeError("Unable to locate skills/agent-readable-doc from the test tree")


SKILL_ROOT = find_skill_root()


def load_skill_script(script_name: str, module_name: str | None = None) -> ModuleType:
    path = SKILL_ROOT / "scripts" / script_name
    name = module_name or f"agent_readable_doc_{path.stem}"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module
