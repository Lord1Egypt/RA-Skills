from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path

from dirstat_skill.targets import ScanTarget


@dataclass(frozen=True)
class WindowsExportResult:
    engine_name: str
    output_path: Path


def _scan_path(root: Path, swallow_root_errors: bool) -> tuple[list[dict[str, object]], int]:
    nodes: list[dict[str, object]] = []
    total_size = 0
    try:
        with os.scandir(root) as entries:
            for entry in entries:
                entry_path = Path(entry.path)
                try:
                    if entry.is_dir(follow_symlinks=False):
                        if _is_windows_junction(entry):
                            continue
                        child_nodes, child_total_size = _scan_path(
                            entry_path,
                            swallow_root_errors=True,
                        )
                        nodes.append(
                            {
                                "path": str(entry_path),
                                "name": entry.name,
                                "is_dir": True,
                                "size": 0,
                                "dsize": child_total_size,
                            }
                        )
                        nodes.extend(child_nodes)
                        total_size += child_total_size
                    else:
                        file_size = entry.stat(follow_symlinks=False).st_size
                        nodes.append(
                            {
                                "path": str(entry_path),
                                "name": entry.name,
                                "is_dir": False,
                                "size": file_size,
                                "dsize": file_size,
                            }
                        )
                        total_size += file_size
                except OSError:
                    continue
    except OSError:
        if swallow_root_errors:
            return nodes, total_size
        raise
    return nodes, total_size


def _is_windows_junction(entry: os.DirEntry[str]) -> bool:
    is_junction = getattr(entry, "is_junction", None)
    if not callable(is_junction):
        return False
    try:
        return bool(is_junction())
    except OSError:
        return False


def build_windows_export(target: Path, output_path: Path) -> WindowsExportResult:
    return build_windows_export_for_targets(
        targets=[ScanTarget(raw_path=str(target), resolved_path=target, platform_name="windows")],
        output_path=output_path,
    )


def build_windows_export_for_targets(
    targets: list[ScanTarget],
    output_path: Path,
) -> WindowsExportResult:
    nodes: list[dict[str, object]] = []
    roots: list[str] = []
    for target in targets:
        if not target.resolved_path.exists():
            raise FileNotFoundError(f"Scan target does not exist: {target.raw_path}")
        if not target.resolved_path.is_dir():
            raise NotADirectoryError(f"Scan target is not a directory: {target.raw_path}")
        child_nodes, child_total_size = _scan_path(
            target.resolved_path,
            swallow_root_errors=False,
        )
        roots.append(str(target.resolved_path))
        nodes.append(
            {
                "path": str(target.resolved_path),
                "name": target.resolved_path.name or str(target.resolved_path),
                "is_dir": True,
                "size": 0,
                "dsize": child_total_size,
            }
        )
        nodes.extend(child_nodes)

    payload = {
        "engine": "windows-native",
        "root": roots[0] if len(roots) == 1 else None,
        "roots": roots,
        "nodes": nodes,
    }
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return WindowsExportResult(engine_name="windows-native", output_path=output_path)

