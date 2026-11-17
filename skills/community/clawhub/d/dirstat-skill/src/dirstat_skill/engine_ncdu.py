from __future__ import annotations

from pathlib import Path
import shutil

from dirstat_skill.models import EngineInfo


def detect_ncdu(path_entries: list[str] | None = None) -> EngineInfo | None:
    path_value = None
    if path_entries is not None:
        path_value = ":".join(path_entries)
    resolved = shutil.which("ncdu", path=path_value)
    if resolved is None:
        return None
    return EngineInfo(binary="ncdu", resolved_path=Path(resolved))


def build_ncdu_export_command(
    binary: str,
    target: Path,
    output_path: Path,
    one_file_system: bool,
    exclude_patterns: list[str],
) -> list[str]:
    command = [binary, "-o", output_path.as_posix()]
    if one_file_system:
        command.append("-x")
    for pattern in exclude_patterns:
        command.extend(["--exclude", pattern])
    command.append(target.as_posix())
    return command

