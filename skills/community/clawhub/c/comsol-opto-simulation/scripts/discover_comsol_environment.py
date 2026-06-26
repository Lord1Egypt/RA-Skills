#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Discover local COMSOL commands, documentation roots, and bundled Java tools."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path


REG_QUERY = [
    "powershell",
    "-NoProfile",
    "-Command",
    (
        "$keys=@("
        "'HKLM:\\SOFTWARE\\COMSOL\\COMSOL64',"
        "'HKLM:\\SOFTWARE\\WOW6432Node\\COMSOL\\COMSOL64',"
        "'HKCU:\\SOFTWARE\\COMSOL\\COMSOL64'"
        "); "
        "foreach($k in $keys){"
        "  if(Test-Path $k){"
        "    $v=(Get-ItemProperty $k).COMSOLROOT;"
        "    if($v){ Write-Output $v }"
        "  }"
        "}"
    ),
]


def _registry_roots() -> list[Path]:
    try:
        proc = subprocess.run(REG_QUERY, capture_output=True, text=True, check=False)
    except OSError:
        return []
    return [Path(line.strip()) for line in proc.stdout.splitlines() if line.strip()]


def _candidate_roots() -> list[Path]:
    roots = _registry_roots()
    for env_name in ("COMSOLROOT", "COMSOL_ROOT", "COMSOL_HOME"):
        value = os.environ.get(env_name)
        if value:
            roots.append(Path(value))
    for command in ("comsol", "comsol.exe"):
        resolved = shutil.which(command)
        if resolved:
            path = Path(resolved).resolve()
            roots.append(path.parents[2] if len(path.parents) > 2 else path.parent)
    roots.extend(
        [
            Path(r"C:\Program Files\COMSOL\COMSOL64\Multiphysics"),
            Path(r"C:\Program Files (x86)\COMSOL\COMSOL64\Multiphysics"),
            Path(r"<COMSOL_INSTALL_DIR>"),
        ]
    )

    unique: list[Path] = []
    seen: set[str] = set()
    for root in roots:
        key = str(root).lower()
        if key not in seen:
            seen.add(key)
            unique.append(root)
    return unique


def _file_info(path: Path) -> dict[str, str | int | bool]:
    return {
        "path": str(path),
        "exists": path.exists(),
        "size": path.stat().st_size if path.exists() and path.is_file() else 0,
    }


def discover(root: Path | None = None) -> dict[str, object]:
    roots = [root] if root else _candidate_roots()
    install_root = next((p for p in roots if p.exists()), None)

    result: dict[str, object] = {
        "status": "found" if install_root else "missing",
        "candidate_roots": [str(p) for p in roots],
    }
    if not install_root:
        return result

    bin_dir = install_root / "bin" / "win64"
    java_dir = install_root / "java" / "win64" / "jre" / "bin"
    doc_root = install_root / "doc" / "help" / "wtpwebapps" / "ROOT" / "doc"

    commands = {
        name: _file_info(bin_dir / f"{name}.exe")
        for name in (
            "comsol",
            "comsolbatch",
            "comsolcompile",
            "comsoldoc",
            "comsolmphserver",
            "comsolmphclient",
        )
    }
    java_tools = {
        name: _file_info(java_dir / f"{name}.exe")
        for name in ("java", "javac", "jshell")
    }

    manual_specs = {
        "programming_reference": ("com.comsol.help.comsol", "COMSOL_ProgrammingReferenceManual.pdf"),
        "reference_manual": ("com.comsol.help.comsol", "COMSOL_ReferenceManual.pdf"),
        "introduction_semiconductor_module": ("com.comsol.help.semicond", "IntroductionToSemiconductorModule.pdf"),
        "semiconductor_users_guide": ("com.comsol.help.semicond", "SemiconductorModuleUsersGuide.pdf"),
        "wave_optics_users_guide": ("com.comsol.help.woptics", "WaveOpticsModuleUsersGuide.pdf"),
        "rf_users_guide": ("com.comsol.help.rf", "RFModuleUsersGuide.pdf"),
        "heat_transfer_users_guide": ("com.comsol.help.heat", "HeatTransferModuleUsersGuide.pdf"),
        "livelink_matlab_users_guide": ("com.comsol.help.llmatlab", "LiveLinkForMATLABUsersGuide.pdf"),
    }
    manuals = {
        label: _file_info(doc_root / folder / filename)
        for label, (folder, filename) in manual_specs.items()
    }

    result.update(
        {
            "install_root": str(install_root),
            "bin_dir": str(bin_dir),
            "java_dir": str(java_dir),
            "doc_root": str(doc_root),
            "commands": commands,
            "java_tools": java_tools,
            "manuals": manuals,
        }
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, help="Override COMSOL installation root.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON.")
    args = parser.parse_args()

    result = discover(args.root)
    print(json.dumps(result, indent=2 if args.pretty else None, ensure_ascii=False))
    return 0 if result["status"] == "found" else 1


if __name__ == "__main__":
    raise SystemExit(main())

