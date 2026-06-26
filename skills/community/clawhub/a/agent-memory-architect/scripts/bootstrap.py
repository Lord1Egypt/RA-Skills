#!/usr/bin/env python3
"""Bootstrap agent memory directory structure and template files."""

import os
import sys
from pathlib import Path

# Default memory root
DEFAULT_ROOT = os.path.expanduser("~/agent-memory")

HOT_MD = """# HOT Memory — Always Loaded

## Preferences
<!-- User-confirmed rules. Never decay. -->
<!-- Format: - rule description (confirmed YYYY-MM-DD) -->

## Patterns
<!-- Observed 3+ times. Decay after 30 days unused. -->
<!-- Format: - pattern description (used Nx, last: YYYY-MM-DD) -->

## Recent
<!-- New corrections pending confirmation. Max 10. -->
<!-- Format: - correction (corrected YYYY-MM-DD, N/3) -->
"""

CORRECTIONS_LOG = """# Corrections Log (last 50)

<!-- Format:
[DATE] WHAT → WHY
  Type: preference|technical|workflow|communication
  Context: where this happened
  Count: N/3
  Status: pending|confirmed|archived
-->
"""

INDEX_MD = """# Memory Index

| Tier | File | Lines | Updated |
|------|------|-------|---------|
| HOT | hot.md | 0 | {date} |

Last compaction: never
"""

AGENT_TEMPLATE = """# HOT Memory — {name} Agent

## Confirmed Rules
<!-- Agent-specific confirmed rules -->

## Active Patterns
<!-- Agent-specific observed patterns -->

## Recent
<!-- New corrections for this agent -->
"""


def create_file(path: Path, content: str, overwrite: bool = False):
    """Create a file if it doesn't exist (or overwrite if forced)."""
    if path.exists() and not overwrite:
        print(f"  ⏭️  {path.name} already exists, skipping")
        return False
    path.write_text(content, encoding="utf-8")
    print(f"  ✅ Created {path.name}")
    return True


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(DEFAULT_ROOT)
    overwrite = "--force" in sys.argv

    from datetime import date
    today = date.today().isoformat()

    print(f"📦 Bootstrapping Agent Memory at: {root}")
    print()

    # Create directories
    dirs = ["projects", "domains", "agents", "archive"]
    for d in dirs:
        dir_path = root / d
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"  📁 {d}/")

    print()

    # Create template files
    create_file(root / "hot.md", HOT_MD, overwrite)
    create_file(root / "corrections.log", CORRECTIONS_LOG, overwrite)
    create_file(root / "index.md", INDEX_MD.format(date=today), overwrite)

    print()
    print("🎉 Agent Memory initialized!")
    print()
    print("Directory structure:")
    print(f"  {root}/")
    print(f"  ├── hot.md              # 🔥 HOT: Always loaded")
    print(f"  ├── corrections.log     # Recent corrections")
    print(f"  ├── index.md            # File manifest")
    print(f"  ├── projects/           # 🌡️ Per-project patterns")
    print(f"  ├── domains/            # 🌡️ Domain knowledge")
    print(f"  ├── agents/             # 🌡️ Per-agent HOT memory")
    print(f"  └── archive/            # ❄️ Decayed patterns")
    print()
    print("Next steps:")
    print("  1. Memory is now active — corrections are auto-detected")
    print("  2. Say 'memory stats' to check status anytime")
    print("  3. For multi-agent setup, create agents/*.md files")
    print()

    # Optional: create agent files if names provided
    agent_args = [a for a in sys.argv[1:] if not a.startswith("--") and a != str(root)]
    if "--agents" in sys.argv:
        idx = sys.argv.index("--agents")
        agent_names = sys.argv[idx + 1:]
        agent_names = [a for a in agent_names if not a.startswith("--")]
        if agent_names:
            print("Creating agent HOT files:")
            for name in agent_names:
                create_file(
                    root / "agents" / f"{name}.md",
                    AGENT_TEMPLATE.format(name=name.capitalize()),
                    overwrite,
                )
            print()


if __name__ == "__main__":
    main()
