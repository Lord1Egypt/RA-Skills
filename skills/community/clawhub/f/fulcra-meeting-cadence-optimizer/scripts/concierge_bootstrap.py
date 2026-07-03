"""Put the shared concierge lib on sys.path.

Ships with every concierge skill so its scripts can import the shared modules
(concierge_cli, concierge_fulcra, fulcra_read, attio_client, ...).

Resolution order:
  1. ./lib next to this file   (vendored -- self-contained skill, e.g. a ClawHub install)
  2. <repo-root>/lib           (this mono-repo layout: skills/<name>/scripts/..)
  3. $FULCRA_CONCIERGE_HOME/lib
  4. ~/.fulcra-concierge/lib

    import concierge_bootstrap  # noqa: F401
    import concierge_cli
"""
from __future__ import annotations

import os
import sys
from pathlib import Path


def _candidates() -> list[Path]:
    here = Path(__file__).resolve()
    out: list[Path] = [here.parent / "lib"]
    try:
        out.append(here.parents[3] / "lib")  # repo root in the mono-repo layout
    except IndexError:
        pass
    env = os.environ.get("FULCRA_CONCIERGE_HOME")
    if env:
        out.append(Path(env) / "lib")
    out.append(Path.home() / ".fulcra-concierge" / "lib")
    return out


for _c in _candidates():
    if (_c / "concierge_cli.py").exists() and str(_c) not in sys.path:
        sys.path.insert(0, str(_c))
        break