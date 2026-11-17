from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest


def test_root_ci_fails_when_canonical_tests_are_absent(tmp_path: Path):
    repository_root = Path(__file__).resolve().parents[3]
    if not (repository_root / "scripts" / "run_ci_local.sh").exists():
        pytest.skip("repository CI script is not shipped with the installed skill")
    isolated_scripts = tmp_path / "scripts"
    isolated_scripts.mkdir()
    copied_ci = isolated_scripts / "run_ci_local.sh"
    shutil.copyfile(repository_root / "scripts" / "run_ci_local.sh", copied_ci)

    run = subprocess.run(
        ["sh", str(copied_ci)],
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )

    assert run.returncode == 2
    assert "no unit tests found" in run.stderr
