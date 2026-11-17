"""Writers for the reproducibility/ folder of a dnasp run.

Written for the standalone dnasp package; dnasp.py loads this file by its path
(see _load_repro_writers), so it needs no package installed and cannot be
shadowed by another module of a similar name.

Every file is written as UTF-8 with LF line endings on all platforms, so the
bundle, and therefore its checksums, are byte-identical wherever a run happens.
"""

from __future__ import annotations

import hashlib
import stat
from pathlib import Path

BUNDLE_DIR = "reproducibility"
_BLOCK_SIZE = 1 << 20


def _bundle_dir(output_dir: Path | str) -> Path:
    folder = Path(output_dir) / BUNDLE_DIR
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def _write_lf(path: Path, text: str) -> Path:
    """Write text as UTF-8 bytes after converting CRLF and lone CR to LF."""
    path.write_bytes(text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8"))
    return path


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(_BLOCK_SIZE), b""):
            digest.update(block)
    return digest.hexdigest()


def write_commands_sh(output_dir: Path | str, command: str) -> Path:
    """Write reproducibility/commands.sh holding the replay command, marked executable."""
    script = _write_lf(_bundle_dir(output_dir) / "commands.sh", f"#!/usr/bin/env bash\n{command}\n")
    script.chmod(script.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return script


def write_environment_yml(output_dir: Path | str, env_name: str, pip_deps: list[str],
                          python_version: str) -> Path:
    """Write reproducibility/environment.yml: a conda environment with pinned pip packages."""
    lines = [
        f"name: {env_name}",
        "channels:",
        "  - conda-forge",
        "dependencies:",
        f"  - python={python_version}",
        "  - pip",
    ]
    if pip_deps:
        lines.append("  - pip:")
        lines.extend(f"      - {dep}" for dep in pip_deps)
    return _write_lf(_bundle_dir(output_dir) / "environment.yml", "\n".join(lines) + "\n")


def write_checksums(paths: list[Path], output_dir: Path | str,
                    anchor: Path | str | None = None) -> Path:
    """Write reproducibility/checksums.sha256 in `sha256sum -c` format.

    Each existing file gets one line, "<hex digest>  <label>". The label is the
    path relative to anchor with forward slashes, or the bare file name when no
    anchor is given or the file lies outside it. Missing files are skipped.
    """
    base = Path(anchor) if anchor is not None else None
    entries = []
    for item in map(Path, paths):
        if not item.is_file():
            continue
        label = item.name
        if base is not None:
            try:
                label = item.relative_to(base).as_posix()
            except ValueError:
                pass
        entries.append(f"{_sha256(item)}  {label}\n")
    return _write_lf(_bundle_dir(output_dir) / "checksums.sha256", "".join(entries))


def write_result_json(output_dir: Path | str, skill: str, version: str, summary: dict,
                      data: dict, input_checksum: str = "", datasets: dict | None = None,
                      status: str | None = None, ok: bool | None = None) -> Path:
    """Write the result.json envelope with the same keys as ClawBio's shared writer.

    Kept here so a standalone run produces the same structured file that the
    ClawBio runner reads (status, ok, skill, version, completed_at,
    input_checksum, datasets, summary, data).
    """
    import json
    from datetime import datetime, timezone
    envelope: dict = {}
    if status is not None:
        envelope["status"] = status
    if ok is not None:
        envelope["ok"] = ok
    envelope.update({
        "skill": skill,
        "version": version,
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "input_checksum": f"sha256:{input_checksum}" if input_checksum else "",
        "datasets": datasets or {},
        "summary": summary,
        "data": data,
    })
    return _write_lf(Path(output_dir) / "result.json", json.dumps(envelope, indent=2, default=str) + "\n")
