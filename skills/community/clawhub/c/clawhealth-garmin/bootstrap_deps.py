from __future__ import annotations

import os
import subprocess
import sys
import venv
from pathlib import Path


# For the ClawHub skill we no longer fetch source code. Instead we
# install the published `clawhealth` package into a local .venv so that
# the `clawhealth` CLI is available for `run_clawhealth.py`.

REQS = [
    "clawhealth>=0.1.1",
]


def _venv_python(base_dir: Path) -> Path:
    venv_dir = base_dir / ".venv"
    if os.name == "nt":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def _run(cmd: list[str]) -> None:
    proc = subprocess.run(cmd)
    if proc.returncode != 0:
        raise SystemExit(proc.returncode)


def main() -> int:
    base_dir = Path(__file__).resolve().parent
    venv_dir = base_dir / ".venv"
    vpy = _venv_python(base_dir)

    if not vpy.exists():
        print("[clawhealth-garmin] Creating venv at", venv_dir)
        venv.EnvBuilder(with_pip=True).create(venv_dir)

    print("[clawhealth-garmin] Installing/upgrading dependencies:", ", ".join(REQS))
    _run([str(vpy), "-m", "pip", "install", "--upgrade", *REQS])

    print("[clawhealth-garmin] OK: clawhealth installed in .venv.")
    print("[clawhealth-garmin] The skill entrypoint (run_clawhealth.py) will use the installed CLI.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
