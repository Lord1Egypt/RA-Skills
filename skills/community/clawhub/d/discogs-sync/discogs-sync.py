"""Entry-point script for running discogs-sync without pip install.

Dependencies must be installed beforehand (see SKILL.md), either into the
current interpreter or into a venv at ~/.discogs-sync/venv:

    python3 -m venv ~/.discogs-sync/venv
    ~/.discogs-sync/venv/bin/pip install -r requirements.txt

This script never installs packages or launches other processes. If a
required package is missing it prints install instructions and exits.
"""

import os
import site
import sys

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_VENV_DIR = os.path.join(os.path.expanduser("~"), ".discogs-sync", "venv")

if sys.platform == "win32":
    _VENV_SITE = os.path.join(_VENV_DIR, "Lib", "site-packages")
else:
    _VENV_SITE = os.path.join(
        _VENV_DIR, "lib", f"python{sys.version_info.major}.{sys.version_info.minor}", "site-packages"
    )

if os.path.isdir(_VENV_SITE):
    site.addsitedir(_VENV_SITE)

_missing = []
try:
    import discogs_client  # noqa: F401
except ImportError:
    _missing.append("python3-discogs-client")
try:
    import click  # noqa: F401
except ImportError:
    _missing.append("click")
try:
    import rich  # noqa: F401
except ImportError:
    _missing.append("rich")

if _missing:
    print(
        f"Error: missing required packages: {', '.join(_missing)}\n"
        f"Install them once with:\n"
        f"  python3 -m venv {_VENV_DIR}\n"
        f"  {_VENV_DIR}/bin/pip install -r {os.path.join(_SCRIPT_DIR, 'requirements.txt')}",
        file=sys.stderr,
    )
    sys.exit(2)

sys.path.insert(0, os.path.join(_SCRIPT_DIR, "src"))

from discogs_sync.cli import main

main()
