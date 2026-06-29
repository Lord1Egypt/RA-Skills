"""Path resolution shared by the drivethru-graphic-artist scripts.

The original product_mockup role hard-coded Railway/agent-core paths
(``/data/agent/mockup/...`` and ``/app/roles/...``). To make this skill
self-contained for any OpenClaw agent, paths are resolved like this:

* **Bundled starter catalog** ships inside the skill at
  ``assets/placement_rules.json`` and is read-only.
* **Editable working copy + outputs** live in a writable *data dir*:
  - ``$MOCKUP_DATA_DIR`` if set (``~`` is expanded), otherwise
  - ``~/.drivethru/mockup``.

Reads prefer the editable copy and fall back to the bundled starter, so
the skill works out of the box. The first edit seeds the editable copy
from the bundled starter, after which all changes persist in the data dir.
"""

from __future__ import annotations

import os
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
BUNDLED_RULES = SKILL_ROOT / "assets" / "placement_rules.json"


def data_dir() -> Path:
    env = os.getenv("MOCKUP_DATA_DIR", "").strip()
    if env:
        return Path(env).expanduser()
    return Path.home() / ".drivethru" / "mockup"


def rules_path() -> Path:
    """Path to the editable working copy of the catalog (may not exist yet)."""
    return data_dir() / "placement_rules.json"


def output_dir() -> Path:
    return data_dir() / "out"


def effective_rules_path() -> Path:
    """Best path to *read* rules from: editable copy if present, else bundled."""
    p = rules_path()
    return p if p.exists() else BUNDLED_RULES


def ensure_data_rules() -> Path:
    """Ensure a writable catalog exists in the data dir and return its path.

    Seeds from the bundled starter on first use so edits never mutate the
    shipped skill asset.
    """
    p = rules_path()
    if not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        if BUNDLED_RULES.exists():
            p.write_text(BUNDLED_RULES.read_text())
        else:
            p.write_text("{}\n")
    return p
