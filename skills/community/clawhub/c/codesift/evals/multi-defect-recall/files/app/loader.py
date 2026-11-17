"""Load order records exported by the billing system."""

import json
from pathlib import Path


def load_orders(path: Path) -> list[dict]:
    """Return the orders in an export file; an export without orders yields []."""
    try:
        return json.loads(path.read_text())["orders"]
    except Exception:
        return []
