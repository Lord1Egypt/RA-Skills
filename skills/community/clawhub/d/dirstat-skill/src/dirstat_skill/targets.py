from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ScanTarget:
    raw_path: str
    resolved_path: Path
    platform_name: str


def normalize_targets(
    requested_paths: list[str],
    auto_discover: bool,
    platform_name: str,
) -> list[ScanTarget]:
    if not requested_paths and not auto_discover:
        raise ValueError("No scan targets were provided")

    normalized: list[ScanTarget] = []
    for raw_path in requested_paths:
        normalized.append(
            ScanTarget(
                raw_path=raw_path,
                resolved_path=Path(raw_path),
                platform_name=platform_name,
            )
        )

    return normalized
