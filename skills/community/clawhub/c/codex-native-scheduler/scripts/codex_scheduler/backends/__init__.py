"""Native scheduler backend selection."""

from __future__ import annotations

from pathlib import Path

from ..errors import BackendError
from ..util import platform_name
from .base import Backend
from .launchd import LaunchdBackend
from .systemd import SystemdBackend
from .windows import TaskSchedulerBackend


def backend_for(
    name: str,
    *,
    state_root: Path,
    execute=None,
) -> Backend:
    selected = platform_name() if name == "auto" else name
    classes = {
        "launchd": LaunchdBackend,
        "systemd": SystemdBackend,
        "task-scheduler": TaskSchedulerBackend,
    }
    backend_class = classes.get(selected)
    if backend_class is None:
        raise BackendError(f"unsupported scheduler backend: {selected}")
    return backend_class(state_root=state_root, execute=execute)

