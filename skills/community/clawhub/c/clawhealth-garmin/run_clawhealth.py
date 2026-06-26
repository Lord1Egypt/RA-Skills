from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def _load_env(path: Path) -> None:
    """Load key=value pairs from a simple .env file if present.

    This is deliberately minimal and only used to wire credentials and
    configuration for the skill. It does not override existing env vars.
    """

    if not path.exists():
        return

    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value
    except Exception:
        # Best-effort only; do not block execution if .env has issues.
        return


def _set_skill_defaults(base_dir: Path) -> None:
    """Set default config/db locations under the skill directory.

    This keeps clawhealth's config and SQLite DB scoped to this skill
    folder unless the user overrides them via env vars.
    """

    config_dir = base_dir / "config"
    db_path = base_dir / "data" / "health.db"
    os.environ.setdefault("CLAWHEALTH_CONFIG_DIR", str(config_dir))
    os.environ.setdefault("CLAWHEALTH_DB", str(db_path))


def _resolve_env_paths_relative_to_skill(base_dir: Path) -> None:
    """Resolve relative paths in env vars against the skill directory.

    OpenClaw may invoke this script with a CWD that is not the skill folder.
    For paths like `./garmin_pass.txt`, we treat them as relative to
    `{baseDir}`.
    """

    for key in (
        "CLAWHEALTH_GARMIN_PASSWORD_FILE",
        "CLAWHEALTH_CONFIG_DIR",
        "CLAWHEALTH_DB",
    ):
        raw = os.environ.get(key)
        if not raw:
            continue
        try:
            p = Path(raw).expanduser()
            if not p.is_absolute():
                p = base_dir / p
            os.environ[key] = str(p.resolve())
        except Exception:
            # Best-effort: keep raw value if resolution fails.
            continue


def main() -> int:
    """Entry point for the clawhealth-garmin skill.

    This script wires environment/configuration and then delegates to the
    `clawhealth` CLI, which is provided by the `clawhealth` Python package
    installed via pip (see SKILL.md install section).
    """

    base_dir = Path(__file__).resolve().parent

    # 1) Load .env if present (credentials, DB/config overrides, etc.)
    _load_env(base_dir / ".env")

    # 2) Set default config/db locations under the skill directory
    _set_skill_defaults(base_dir)

    # 3) Resolve relative paths (e.g. ./garmin_pass.txt) against the skill dir
    _resolve_env_paths_relative_to_skill(base_dir)

    # 4) Delegate to the installed `clawhealth` CLI
    try:
        result = subprocess.run(["clawhealth", *sys.argv[1:]])
        return result.returncode
    except FileNotFoundError:
        sys.stderr.write(
            "Error: 'clawhealth' CLI not found.\n"
            "Please install the 'clawhealth' Python package, for example:\n"
            "  python -m pip install clawhealth\n"
        )
        return 127


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
