#!/usr/bin/env python3
"""Dependency installation script.

Supports pip installation.

[INPUT]: None
[OUTPUT]: Install dependencies required by awiki-did and run local database
          upgrade checks after installation, including listener stop/restart
          coordination for explicit upgrade flows
[POS]: Project root, provides pip installation and post-install local database
       upgrade orchestration

[PROTOCOL]:
1. Update this header when logic changes
2. Check the folder's CLAUDE.md after updating
"""

import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


def run_command(cmd: list[str], check: bool = True) -> bool:
    """Run a command."""
    try:
        result = subprocess.run(cmd, check=check, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {' '.join(cmd)}")
        if e.stderr:
            print(e.stderr)
        return False
    except FileNotFoundError:
        return False


def find_installer() -> tuple[str, list[str]]:
    """Find an available package installer."""
    script_dir = Path(__file__).parent
    requirements = str(script_dir / "requirements.txt")
    current_python_pip = [
        sys.executable,
        "-m",
        "pip",
        "install",
        "-r",
        requirements,
    ]

    # Prefer the current Python interpreter's pip to avoid cross-environment installs.
    # If pip is missing but ensurepip is available, stay on the current interpreter
    # and let main() bootstrap pip before installation.
    if (
        importlib.util.find_spec("pip") is not None
        or importlib.util.find_spec("ensurepip") is not None
    ):
        return "current-python-pip", current_python_pip

    # Fallback to a bare pip only when the current interpreter cannot provide pip.
    if shutil.which("pip"):
        return "pip", ["pip", "install", "-r", requirements]

    return "current-python-pip", current_python_pip


def bootstrap_current_python_pip() -> bool:
    """Bootstrap pip for the current Python interpreter when possible."""
    if importlib.util.find_spec("ensurepip") is None:
        return False
    print("\nCurrent Python has no pip module. Bootstrapping with ensurepip...\n")
    return run_command([sys.executable, "-m", "ensurepip", "--upgrade"])


def run_local_database_upgrade() -> tuple[bool, dict[str, Any] | None]:
    """Check whether the local database requires migration and upgrade it if needed."""
    script_dir = Path(__file__).parent
    scripts_dir = script_dir / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))

    try:
        from database_migration import ensure_local_database_ready_for_upgrade
    except Exception as exc:  # noqa: BLE001
        print("Failed to load local database migration helper.")
        print(f"Error: {exc}")
        return False, None

    try:
        result = ensure_local_database_ready_for_upgrade()
    except Exception as exc:  # noqa: BLE001
        print("Local database upgrade check failed.")
        print(f"Error: {exc}")
        return False, None

    status = result.get("status")
    db_path = result.get("db_path")
    before_version = result.get("before_version")
    after_version = result.get("after_version")
    backup_path = result.get("backup_path")

    print("\nLocal database upgrade check:")
    print(f"  status: {status}")
    if db_path:
        print(f"  db_path: {db_path}")
    if before_version is not None:
        print(f"  before_version: {before_version}")
    if after_version is not None:
        print(f"  after_version: {after_version}")
    if backup_path:
        print(f"  backup_path: {backup_path}")
    listener_service = result.get("listener_service")
    if isinstance(listener_service, dict):
        print("  listener_service:")
        for key in (
            "was_running",
            "stopped",
            "restarted",
            "error",
            "status_error",
            "stop_error",
            "restart_error",
        ):
            if key in listener_service:
                print(f"    {key}: {listener_service[key]}")

    return status in {"not_found", "not_needed", "ready", "migrated"}, result


def main() -> int:
    """Main function."""
    print("=" * 50)
    print("awiki-did Skill Dependency Installation")
    print("=" * 50)

    installer_name, cmd = find_installer()
    print(f"\nUsing {installer_name} to install dependencies...")
    print(f"Running: {' '.join(cmd)}\n")

    if installer_name == "current-python-pip" and importlib.util.find_spec("pip") is None:
        if not bootstrap_current_python_pip():
            print("\nDependency installation failed. Unable to prepare pip for the current Python.")
            print("Please install pip for this Python interpreter and retry, or run manually:")
            print(f"  {sys.executable} -m pip install -r requirements.txt")
            return 1

    if not run_command(cmd):
        print("\nDependency installation failed. Please install manually:")
        print(f"  {sys.executable} -m pip install -r requirements.txt")
        return 1

    ok, _result = run_local_database_upgrade()
    if not ok:
        print("\nDependencies were installed, but the local database upgrade check failed.")
        print("Please run manually:")
        print("  python scripts/migrate_local_database.py")
        print("or:")
        print("  python scripts/check_status.py --upgrade-only")
        return 1

    print("\nDependencies installed successfully!")
    print("\nReady to use:")
    print("  python scripts/setup_identity.py --name MyAgent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
