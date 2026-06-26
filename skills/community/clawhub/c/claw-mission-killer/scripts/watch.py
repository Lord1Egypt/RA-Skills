#!/usr/bin/env python3
"""
watch.py - Auto-install agent-interrupt into newly created agents

Run periodically via cron to detect new agents and inject the integration.
Safe to run multiple times — skips agents already integrated.

Usage:
    python -X utf8 scripts/watch.py
"""

import json
import os
import sys
from pathlib import Path

INTEGRATION_MARKER = "<!-- agent-interrupt:integrated -->"
SKIP_AGENTS = {"main"}


def find_openclaw_home():
    env = os.environ.get("OPENCLAW_HOME")
    if env:
        return Path(env)
    return Path.home() / ".openclaw"


def get_skill_path():
    return Path(__file__).parent.parent.resolve()


def build_integration_block(agent_id, skill_path):
    run_py = skill_path / "scripts" / "run.py"
    return f"""
{INTEGRATION_MARKER}
## Long Task Protocol (agent-interrupt)

For all exec tasks expected to run longer than 10 seconds, use `run.py` instead of calling python directly.
This enables precise kill support via the agent-interrupt skill.

```bash
# Instead of: python your_script.py
python -X utf8 "{run_py}" --agent {agent_id} -- python your_script.py
```

- PID is automatically registered before execution
- Marker is automatically cleared when task finishes (even on crash)
- To interrupt this agent: interrupt.py --agent {agent_id}
<!-- agent-interrupt:end -->
"""


def main():
    openclaw_home = find_openclaw_home()
    skill_path = get_skill_path()

    config_path = openclaw_home / "openclaw.json"
    with open(config_path, encoding="utf-8") as f:
        config = json.load(f)

    agents = [a for a in config["agents"]["list"] if a["id"] not in SKIP_AGENTS]
    injected = []

    for agent in agents:
        agent_id = agent["id"]
        workspace = agent.get("workspace")
        if not workspace:
            continue

        agents_md = Path(workspace) / "AGENTS.md"
        if not agents_md.exists():
            continue

        content = agents_md.read_text(encoding="utf-8")
        if INTEGRATION_MARKER in content:
            continue

        # New agent found — inject
        block = build_integration_block(agent_id, skill_path)
        with open(agents_md, "a", encoding="utf-8") as f:
            f.write(block)
        injected.append(agent_id)
        print(f"[watch] Injected: {agent_id} ({agents_md})")

    if not injected:
        print("[watch] No new agents found, all up to date.")
    else:
        print(f"[watch] Injected {len(injected)} new agent(s): {', '.join(injected)}")


if __name__ == "__main__":
    main()
