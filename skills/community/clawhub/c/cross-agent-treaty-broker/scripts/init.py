#!/usr/bin/env python3
"""Initialize the Cross-Agent Treaty Broker skill."""
import os
import json
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
TREATIES_DIR = os.path.join(DATA_DIR, "treaties")
LOGS_DIR = os.path.join(DATA_DIR, "logs")
ANCHORS_DIR = os.path.join(DATA_DIR, "anchors")


def init_skill():
    """Create the skill's data directories and initial registry."""
    for directory in [DATA_DIR, TREATIES_DIR, LOGS_DIR, ANCHORS_DIR]:
        os.makedirs(directory, exist_ok=True)

    # Initialize anchor registry
    registry = {
        "anchors": [],
        "created_at": datetime.utcnow().isoformat() + "Z"
    }

    registry_path = os.path.join(ANCHORS_DIR, "registry.json")
    with open(registry_path, "w") as f:
        json.dump(registry, f, indent=2)

    print(f"CATB initialized. Data directory: {DATA_DIR}")
    print(f"Treaties directory: {TREATIES_DIR}")
    print(f"Logs directory: {LOGS_DIR}")
    print(f"Anchors directory: {ANCHORS_DIR}")


if __name__ == "__main__":
    init_skill()