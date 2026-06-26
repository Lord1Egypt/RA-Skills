#!/usr/bin/env python3
"""
install.py - Auto-install agent-interrupt integration into all agent AGENTS.md files

Run once after installing the skill:
    python -X utf8 scripts/install.py

What it does:
- Reads all agents from openclaw.json
- Appends the run.py protocol block to each agent's AGENTS.md
- Skips agents that already have the integration
- Skips 'main' agent by default (use --include-main to include)
"""

import argparse
import json
import os
from pathlib import Path

INTEGRATION_MARKER = "<!-- agent-interrupt:integrated -->"


def find_openclaw_home():
    env = os.environ.get("OPENCLAW_HOME")
    if env:
        return Path(env)
    return Path.home() / ".openclaw"


def get_skill_path():
    """Get the absolute path of this skill's directory."""
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
- To interrupt this agent: `interrupt.py --agent {agent_id}`
<!-- agent-interrupt:end -->
"""


def install_to_agent(agent, skill_path, dry_run=False):
    agent_id = agent["id"]
    workspace = agent.get("workspace")

    if not workspace:
        print(f"  [SKIP] {agent_id}: no workspace configured")
        return

    agents_md = Path(workspace) / "AGENTS.md"

    if not agents_md.exists():
        print(f"  [SKIP] {agent_id}: AGENTS.md not found at {agents_md}")
        return

    content = agents_md.read_text(encoding="utf-8")

    if INTEGRATION_MARKER in content:
        print(f"  [SKIP] {agent_id}: already integrated")
        return

    block = build_integration_block(agent_id, skill_path)

    if dry_run:
        print(f"  [DRY-RUN] {agent_id}: would append integration block to {agents_md}")
        return

    with open(agents_md, "a", encoding="utf-8") as f:
        f.write(block)

    print(f"  [OK] {agent_id}: integration added to {agents_md}")


def main():
    parser = argparse.ArgumentParser(description="Install agent-interrupt into all agent AGENTS.md files")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, no changes")
    parser.add_argument("--include-main", action="store_true", help="Also install into main agent")
    parser.add_argument("--agent", help="Install into specific agent only")
    args = parser.parse_args()

    openclaw_home = find_openclaw_home()
    skill_path = get_skill_path()

    config_path = openclaw_home / "openclaw.json"
    with open(config_path, encoding="utf-8") as f:
        config = json.load(f)

    agents = config["agents"]["list"]

    if args.agent:
        agents = [a for a in agents if a["id"] == args.agent]
        if not agents:
            print(f"[install] ERROR: Agent '{args.agent}' not found")
            return
    elif not args.include_main:
        agents = [a for a in agents if a["id"] != "main"]

    print(f"[install] agent-interrupt integration installer")
    print(f"[install] Skill path: {skill_path}")
    print(f"[install] Target agents: {len(agents)}")
    if args.dry_run:
        print("[install] DRY-RUN mode")
    print()

    for agent in agents:
        install_to_agent(agent, skill_path, args.dry_run)

    print()
    print("[install] Done. Agents will use run.py for long tasks automatically.")
    print(f"[install] To interrupt any agent: python -X utf8 {skill_path}/scripts/interrupt.py --agent <id>")
    print(f"[install] To interrupt all agents: python -X utf8 {skill_path}/scripts/interrupt.py --all")


if __name__ == "__main__":
    main()
