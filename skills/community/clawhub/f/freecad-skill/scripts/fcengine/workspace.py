"""Workspace path confinement (pure Python).

Every file the engine reads or writes must resolve inside the workspace
root. Symlinks are resolved before the check.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, List

from . import errors


def resolve(root: Path, rel: str) -> Path:
    """Resolve ``rel`` against ``root`` and refuse anything outside it."""
    if not isinstance(rel, str) or not rel.strip():
        raise errors.SkillError(errors.PATH_NOT_ALLOWED, "Empty path")
    if "\x00" in rel:
        raise errors.SkillError(errors.PATH_NOT_ALLOWED, "Invalid path")
    if os.sep == "/" and "\\" in rel:
        rel = rel.replace("\\", "/")  # Windows-style separators from an agent on Linux/macOS
    root_real = Path(os.path.realpath(root))
    candidate = Path(rel)
    if not candidate.is_absolute():
        candidate = root_real / candidate
    real = Path(os.path.realpath(candidate))
    try:
        real.relative_to(root_real)
    except ValueError:
        raise errors.SkillError(
            errors.PATH_NOT_ALLOWED,
            f"Path '{rel}' is outside the workspace",
            hint=f"Use a path relative to the workspace root ({root_real}).",
        ) from None
    return real


def relative(root: Path, path: Path) -> str:
    return Path(os.path.realpath(path)).relative_to(Path(os.path.realpath(root))).as_posix()


def request_inputs(request: Any) -> List[str]:
    """Workspace files a request reads besides its document: imported files and font files.

    The launcher needs them when it runs FreeCAD on a staged copy of the workspace (snap confinement)."""
    steps = request.get("steps") if isinstance(request, dict) else None
    if not isinstance(steps, list) and isinstance(request, dict) and isinstance(request.get("op"), str):
        steps = [request]
    out: List[str] = []
    for s in steps or []:
        if not isinstance(s, dict):
            continue
        refs = []
        if s.get("op") == "import":
            refs.append(s.get("file"))
        elif s.get("op") == "text":
            refs.append(s.get("font"))
        elif s.get("op") == "set" and isinstance(s.get("properties"), dict):
            refs.append(s["properties"].get("font"))
        for ref in refs:
            if isinstance(ref, str) and ref.strip() and ref != "default" and ref not in out:
                out.append(ref)
    return out
