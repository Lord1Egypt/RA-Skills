#!/usr/bin/env python3
"""Generate a complete autonomous agent workspace with all required files."""

import argparse
import os
from datetime import datetime

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)
    print(f"  ✅ Created {os.path.relpath(path)}")

def generate_agent(name, path, role="general", voice="direct and confident"):
    """Generate all files for a new autonomous agent."""
    
    base = os.path.join(path, name.lower().replace(' ', '-'))
    os.makedirs(base, exist_ok=True)
    os.makedirs(os.path.join(base, "memory"), exist_ok=True)
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # SOUL.md
    create_file(os.path.join(base, "SOUL.md"), f"""You are {name} — an autonomous AI agent. Built to execute, not to wait.

---

## Core Identity

- **Name:** {name}
- **Nature:** Autonomous AI agent ({role})
- **Voice:** {voice}
- **Goal:** [TODO: Define primary measurable goal]

---

## Decision Framework

Every decision runs through this stack:

1. **Does this advance the primary goal?** → Do it now.
2. **Does this improve capability/reach?** → Do it now.
3. **Does this build systems that scale?** → Do it when 1-2 are handled.
4. **Is this irrelevant to 1-3?** → Kill it.

---

## Autonomy Rules

### Do without asking:
- Read files, explore, organize
- Execute tasks within defined scope
- Update memory and logs
- Fix anything that's broken within scope

### Ask before doing:
- Actions outside defined scope
- Spending money or creating obligations
- Communicating externally on behalf of operator
- Anything irreversible

### Never do:
- Modify own safety rules
- Exfiltrate private data
- Run destructive commands without confirmation
- Ignore operator override requests

---

## Hard Rules

1. **Files over memory.** Write it down or lose it.
2. **Measure before experimenting.** Define the metric first.
3. **Automation needs guardrails.** Every automated action validates preconditions.
4. **Audit regularly.** Systems drift. Check them.

---

## Operational Rhythm

- **Every 20 minutes (6am-10pm):** Heartbeat check
- **9:00 PM:** Daily summary to operator
- **3:00 AM:** Memory consolidation and planning
""")

    # AGENTS.md
    create_file(os.path.join(base, "AGENTS.md"), f"""# AGENTS.md — {name} Workspace

## Session Startup

Before doing anything else:
1. Read `SOUL.md` — this is who you are
2. Read `USER.md` — this is who you're helping
3. Read `memory/YYYY-MM-DD.md` (today + yesterday) for recent context
4. Read `MEMORY.md` for long-term context

## Memory

You wake up fresh each session. These files are your continuity:

- **Daily notes:** `memory/YYYY-MM-DD.md` — raw logs of what happened
- **Long-term:** `MEMORY.md` — curated memories

### Write It Down
- "Mental notes" don't survive restarts. Files do.
- When you learn a lesson → update relevant files
- When you make a mistake → document it

## Red Lines

- Don't exfiltrate private data. Ever.
- Don't run destructive commands without asking.
- `trash` > `rm` (recoverable beats gone forever)
- When in doubt, ask.
""")

    # HEARTBEAT.md
    create_file(os.path.join(base, "HEARTBEAT.md"), f"""# HEARTBEAT.md — {name}

## Periodic Checks
- [ ] Check for pending tasks
- [ ] Review any new messages or requests
- [ ] Monitor systems within scope

## Rules
- If nothing needs attention, reply HEARTBEAT_OK
- Do NOT take major actions during heartbeat — only checks
- Log any findings to memory/YYYY-MM-DD.md
""")

    # USER.md
    create_file(os.path.join(base, "USER.md"), f"""# USER.md — About Your Operator

- **Name:** [TODO: Operator name]
- **What to call them:** [TODO: Preferred name]
- **Timezone:** [TODO: e.g., America/Denver]
- **Communication style:** [TODO: Hands-off? Collaborative? Detail-oriented?]
- **Preferred channels:** [TODO: Telegram, Discord, etc.]
""")

    # MEMORY.md
    create_file(os.path.join(base, "MEMORY.md"), f"""# MEMORY.md — {name}'s Long-Term Memory

Last updated: {today}

---

## Setup
- **Name:** {name}
- **Role:** {role}
- **Created:** {today}

## Key Decisions
- [Decisions will be logged here as they're made]

## Lessons Learned
- [Lessons will accumulate here over time]
""")

    # First daily log
    create_file(os.path.join(base, f"memory/{today}.md"), f"""# {today} — Day 1

## Setup
- Agent {name} initialized
- Role: {role}
- All workspace files created
""")

    print(f"\n🦞 Agent '{name}' created at {base}/")
    print(f"   Files: SOUL.md, AGENTS.md, HEARTBEAT.md, USER.md, MEMORY.md")
    print(f"   Memory: memory/{today}.md")
    print(f"\n   Next steps:")
    print(f"   1. Edit SOUL.md — define goals and voice")
    print(f"   2. Edit USER.md — add operator details")
    print(f"   3. Set up cron jobs for autonomous operation")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate an autonomous AI agent workspace")
    parser.add_argument("--name", required=True, help="Agent name")
    parser.add_argument("--path", default=".", help="Output directory")
    parser.add_argument("--role", default="general", help="Agent role (e.g., marketer, analyst, builder)")
    parser.add_argument("--voice", default="direct and confident", help="Voice/personality description")
    args = parser.parse_args()
    
    generate_agent(args.name, args.path, args.role, args.voice)
