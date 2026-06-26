#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path
from typing import Dict, List


ENV_PATH = Path(".env")
SCRIPT_DIR = Path(__file__).resolve().parent
REQUIRED_ENV_NAMES = [
    "AICADE_GALAXY_BASE_URL",
    "AICADE_GALAXY_API_KEY",
    "AICADE_GALAXY_OUTPUT_PATH",
]


def main() -> None:
    existing = load_env(ENV_PATH)
    missing = [name for name in REQUIRED_ENV_NAMES if not existing.get(name)]

    if missing:
        print(
            f"Missing required environment values: {', '.join(missing)}. Running setup_env.py..."
        )
        run_script([sys.executable, str(SCRIPT_DIR / "setup_env.py")], "setup_env.py")
    else:
        print("Environment already configured. Skipping setup_env.py.")

    print("Running export_artifact.py...")
    run_script([sys.executable, str(SCRIPT_DIR / "export_artifact.py")], "export_artifact.py")
    print("Bootstrap completed.")


def load_env(path: Path) -> Dict[str, str]:
    if not path.exists():
        return {}

    result: Dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        result[key.strip()] = strip_quotes(value.strip())
    return result


def strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def run_script(command: List[str], label: str) -> None:
    try:
        result = subprocess.run(command, check=False)
    except OSError as exc:
        raise RuntimeError(f"Failed to run {label}: {exc}") from exc

    if result.returncode != 0:
        sys.exit(result.returncode)


if __name__ == "__main__":
    main()
