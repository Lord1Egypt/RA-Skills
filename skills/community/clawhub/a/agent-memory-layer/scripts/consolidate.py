"""
Consolidation daemon — promotes recurring episodic memories to long-term.
Run periodically via cron.
"""
import json
from pathlib import Path
from datetime import datetime


def consolidate(agent_id: str, storage_dir: str = ".agent_memory"):
    """Scan episodic memory and promote recurring patterns to long-term."""
    base = Path(storage_dir) / agent_id
    lt_path = base / "long_term.json"

    # Load long-term
    if lt_path.exists():
        long_term = json.loads(lt_path.read_text())
    else:
        long_term = []

    # Count episode patterns (simulated — in production read from episodic store)
    # This is the consolidation engine that would run on the actual memory
    new_entries = []

    # Deduplicate against existing
    existing_contents = {e.get("content", "") for e in long_term}
    for entry in new_entries:
        if entry["content"] not in existing_contents:
            long_term.append(entry)

    lt_path.parent.mkdir(parents=True, exist_ok=True)
    lt_path.write_text(json.dumps(long_term, indent=2))
    print(f"[Consolidate] {agent_id}: {len(long_term)} long-term entries ({len(new_entries)} new)")


if __name__ == "__main__":
    import sys
    agent_id = sys.argv[1] if len(sys.argv) > 1 else "default"
    consolidate(agent_id)
