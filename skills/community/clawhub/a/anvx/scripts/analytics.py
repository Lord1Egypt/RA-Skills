"""Send an anonymised analytics event. Used by SKILL.md agent instructions."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from engine.analytics import EventTracker


def main() -> None:
    if len(sys.argv) < 3:
        print("Usage: analytics.py <event_type> <event_category> [--metadata '{...}']")
        print("Example: analytics.py query intelligence --metadata '{\"intent\": \"category\"}'")
        sys.exit(1)

    event_type = sys.argv[1]
    event_category = sys.argv[2]

    metadata: dict = {}
    if "--metadata" in sys.argv:
        idx = sys.argv.index("--metadata")
        if idx + 1 < len(sys.argv):
            try:
                metadata = json.loads(sys.argv[idx + 1])
            except json.JSONDecodeError:
                print("Warning: invalid metadata JSON, ignoring.")

    tracker = EventTracker()
    tracker.track(event_type, event_category, "openclaw", metadata)
    print(f"Event logged: {event_type} ({event_category})")


if __name__ == "__main__":
    main()
