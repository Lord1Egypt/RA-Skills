#!/usr/bin/env python3
"""
Memory Lifecycle Setup Script

Scaffolds structured memory files, adds the Recent buffer to MEMORY.md,
creates cron jobs for nightly/weekly/monthly/yearly cycles, and updates
HEARTBEAT.md with memory micro-attention tasks.

Usage:
    python3 setup.py [--agent AGENT_ID] [--dry-run] [--timezone TIMEZONE]

Options:
    --agent       Agent ID (default: main)
    --dry-run     Preview changes without applying
    --timezone    Timezone for cron schedules (default: UTC)
    --workspace   Workspace directory (default: current working directory)
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# --- Templates ---

PEOPLE_TEMPLATE = """# People — Contacts & Relationships

> Maintained by nightly/weekly memory cycles. See memory-lifecycle skill.

---

## Family
*(Add family members, their contact details, and relationship notes)*

## Work / Business
*(Add colleagues, clients, partners)*

## Services
*(Add tradespeople, accountants, agents — anyone who provides a service)*
"""

DECISIONS_TEMPLATE = """# Decisions — Key Choices & Rationale

> Maintained by nightly/weekly memory cycles. See memory-lifecycle skill.

---

*(Entries added by the nightly sleep cycle. Format:)*

<!--
### YYYY-MM-DD: [Decision title]
- **Decision:** What was decided
- **Options considered:** What alternatives existed
- **Reasoning:** Why this option was chosen
- **Outcome:** (updated later when known)
-->
"""

LESSONS_TEMPLATE = """# Lessons — Things We Learned

> Maintained by nightly/weekly memory cycles. See memory-lifecycle skill.

---

## Technical
*(Technical lessons — tools, APIs, infrastructure)*

## Process
*(Workflow and communication lessons)*

## People
*(Relationship and interaction lessons)*
"""

COMMITMENTS_TEMPLATE = """# Commitments & Deadlines

> Maintained by nightly/weekly memory cycles. See memory-lifecycle skill.

---

## Recurring
*(Regular obligations — monthly invoices, quarterly filings, etc.)*

## Upcoming
*(One-off deadlines and appointments)*
"""

RECENT_BUFFER = """## Recent
> Working memory — heartbeat promotes critical items here, nightly cycle processes them.
"""

HEARTBEAT_SECTION = """## Memory Micro-Attention
Quick memory hygiene — keep this focused (capture + promote + tag):
1. **Capture check:** Did anything noteworthy happen since last heartbeat? If so, ensure it's in today's `memory/YYYY-MM-DD.md`.
2. **Promote critical items:** If something session-critical happened (new appointment, key decision, deadline change), add a one-liner to `MEMORY.md → ## Recent`.
3. **Tag unprocessed items:** Scan today's daily file for untagged entries. Add inline tags: `[decision]`, `[lesson]`, `[person]` so the nightly cycle knows where to file them.
4. **Staleness flag:** If `## Recent` has items older than 48h not processed by nightly, flag for investigation.
5. **Nightly cycle health:** Find the "Memory: Nightly Sleep Cycle" job via `openclaw cron list` and check its last run status. If errored: diagnose, fix, and re-run. Only alert the human if you genuinely can't fix it yourself.
6. Do NOT consolidate, archive, or heavily edit MEMORY.md — that's the nightly cycle's job.
"""


def run_cmd(cmd, dry_run=False):
    """Run a shell command, or print it in dry-run mode."""
    if dry_run:
        print(f"  [DRY RUN] {cmd}")
        return None
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  [ERROR] {cmd}")
        print(f"  stderr: {result.stderr.strip()}")
    return result


def discover_agents():
    """Discover all agents on this OpenClaw server."""
    result = subprocess.run("openclaw status --json 2>/dev/null", shell=True, capture_output=True, text=True)
    try:
        data = json.loads(result.stdout)
        agents_data = data.get("agents", {})
        agent_list = agents_data.get("agents", []) if isinstance(agents_data, dict) else agents_data
        return [
            {"id": a.get("id"), "name": a.get("name", ""), "workspace": a.get("workspaceDir", "")}
            for a in agent_list
            if a.get("id") and a.get("workspaceDir")
        ]
    except (json.JSONDecodeError, KeyError, TypeError):
        return []


def create_file(path, content, dry_run=False):
    """Create a file if it doesn't exist."""
    if path.exists():
        print(f"  [SKIP] {path} already exists")
        return False
    if dry_run:
        print(f"  [DRY RUN] Would create {path}")
        return True
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    print(f"  [OK] Created {path}")
    return True


def add_recent_buffer(memory_path, dry_run=False):
    """Add ## Recent section to MEMORY.md if not present."""
    if not memory_path.exists():
        print(f"  [SKIP] {memory_path} not found — create MEMORY.md first")
        return False

    content = memory_path.read_text()
    if "## Recent" in content:
        print(f"  [SKIP] ## Recent already exists in {memory_path}")
        return False

    if dry_run:
        print(f"  [DRY RUN] Would add ## Recent buffer to {memory_path}")
        return True

    # Insert after the first heading
    lines = content.split("\n")
    insert_idx = 0
    for i, line in enumerate(lines):
        if line.startswith("# "):
            insert_idx = i + 1
            break

    lines.insert(insert_idx, "")
    lines.insert(insert_idx + 1, RECENT_BUFFER)

    memory_path.write_text("\n".join(lines))
    print(f"  [OK] Added ## Recent buffer to {memory_path}")
    return True


def update_heartbeat(heartbeat_path, dry_run=False):
    """Add memory micro-attention section to HEARTBEAT.md."""
    if not heartbeat_path.exists():
        print(f"  [SKIP] {heartbeat_path} not found — create HEARTBEAT.md first")
        return False

    content = heartbeat_path.read_text()
    if "Memory Micro-Attention" in content:
        print(f"  [SKIP] Memory Micro-Attention already in {heartbeat_path}")
        return False

    if dry_run:
        print(f"  [DRY RUN] Would add Memory Micro-Attention to {heartbeat_path}")
        return True

    # Append after the first section
    lines = content.split("\n")
    insert_idx = len(lines)
    found_first_section = False
    for i, line in enumerate(lines):
        if line.startswith("## ") and found_first_section:
            insert_idx = i
            break
        if line.startswith("## "):
            found_first_section = True

    lines.insert(insert_idx, HEARTBEAT_SECTION)
    heartbeat_path.write_text("\n".join(lines))
    print(f"  [OK] Added Memory Micro-Attention to {heartbeat_path}")
    return True


def get_cron_schedules(timezone):
    """Return cron expressions with timezone annotation.

    Uses OpenClaw's '@ Timezone' syntax so cron jobs run at the intended
    local time regardless of server UTC offset or DST changes.
    """
    tz_suffix = f" @ {timezone}" if timezone != "UTC" else ""
    return {
        "nightly": f"0 2 * * *{tz_suffix}",      # 2:00 AM local
        "weekly": f"0 3 * * 0{tz_suffix}",        # Sunday 3:00 AM local
        "monthly": f"0 4 1 * *{tz_suffix}",       # 1st of month 4:00 AM local
        "yearly": f"0 3 1 1 *{tz_suffix}",        # Jan 1 3:00 AM local
    }


def get_existing_cron_jobs(agent_id):
    """Fetch existing cron jobs for this agent."""
    result = subprocess.run(
        f'openclaw cron list --json 2>/dev/null',
        shell=True, capture_output=True, text=True
    )
    try:
        data = json.loads(result.stdout)
        jobs = data.get("jobs", data) if isinstance(data, dict) else data
        if isinstance(jobs, list):
            return {j.get("name", ""): j for j in jobs if j.get("agentId") == agent_id}
        return {}
    except (json.JSONDecodeError, TypeError):
        return {}


def create_cron_jobs(agent_id, schedules, skill_dir, dry_run=False):
    """Create the four memory lifecycle cron jobs (idempotent — skips existing)."""
    prompts = {
        "nightly": (skill_dir / "references" / "nightly-prompt.md"),
        "weekly": (skill_dir / "references" / "weekly-prompt.md"),
        "monthly": (skill_dir / "references" / "monthly-prompt.md"),
        "yearly": (skill_dir / "references" / "yearly-prompt.md"),
    }

    job_configs = {
        "nightly": {
            "name": "Memory: Nightly Sleep Cycle",
            "description": "Nightly memory consolidation — review daily notes, promote to structured files, update MEMORY.md",
        },
        "weekly": {
            "name": "Memory: Weekly Reflection",
            "description": "Weekly memory reflection — review 7 days, spot patterns, refine MEMORY.md",
        },
        "monthly": {
            "name": "Memory: Monthly Deep Clean",
            "description": "Monthly memory archiving — archive completed work, clean MEMORY.md, consolidate lessons",
        },
        "yearly": {
            "name": "Memory: Yearly Wisdom",
            "description": "Yearly wisdom distillation — extract transcendent lessons, evolve SOUL.md",
        },
    }

    # Check for existing jobs to avoid duplicates
    existing_jobs = get_existing_cron_jobs(agent_id)

    created = []
    for cycle, config in job_configs.items():
        # Check if a job with this name (or similar) already exists
        job_exists = False
        for existing_name in existing_jobs:
            if config["name"].lower() in existing_name.lower() or \
               cycle.lower() in existing_name.lower() and "memory" in existing_name.lower():
                print(f"\n  [SKIP] {config['name']} — already exists as '{existing_name}'")
                job_exists = True
                break

        if job_exists:
            continue

        # Inline the full prompt text into the cron message. Cron jobs run
        # in isolated sessions without filesystem access, so reference-based
        # "read the file" instructions don't work. The prompt files still
        # serve as the canonical source — we just bake them in at setup time.
        prompt_file = prompts[cycle]
        if prompt_file.exists():
            prompt_text = prompt_file.read_text().strip()
        else:
            prompt_text = f"Run the {cycle} memory lifecycle cycle."
            print(f"  [WARN] Prompt file not found: {prompt_file}")
        message = f"MEMORY LIFECYCLE — {cycle.upper()} CYCLE:\n\n{prompt_text}"

        cmd = (
            f'openclaw cron create '
            f'--name "{config["name"]}" '
            f'--cron "{schedules[cycle]}" '
            f'--agent {agent_id} '
            f'--session isolated '
            f'--no-deliver '
            f'--description "{config["description"]}" '
            f'--message "{message}" '
        )

        print(f"\n  Creating cron job: {config['name']}")
        result = run_cmd(cmd, dry_run)
        if result and result.returncode == 0:
            # Extract job ID from JSON output
            try:
                data = json.loads(result.stdout)
                created.append({"cycle": cycle, "id": data.get("id"), "name": config["name"]})
                print(f"  [OK] Created: {config['name']} (ID: {data.get('id')})")
            except (json.JSONDecodeError, KeyError):
                print(f"  [OK] Created: {config['name']}")
                created.append({"cycle": cycle, "name": config["name"]})

    return created


def main():
    parser = argparse.ArgumentParser(description="Set up Memory Lifecycle for an OpenClaw agent")
    parser.add_argument("--agent", default="main", help="Agent ID (default: main)")
    parser.add_argument("--all", action="store_true", help="Set up all agents on this server")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without applying")
    parser.add_argument("--timezone", default="UTC", help="Timezone for cron schedules (default: UTC)")
    parser.add_argument("--workspace", default=None, help="Workspace directory (default: auto-detect)")
    args = parser.parse_args()

    # --all flag: discover all agents and run setup for each
    if args.all:
        agents = discover_agents()
        if not agents:
            print("No agents found. Check openclaw status.")
            sys.exit(1)
        print(f"\n🔄 Setting up memory lifecycle for {len(agents)} agent(s)...\n")
        for agent_info in agents:
            print(f"\n{'=' * 60}")
            print(f"  Agent: {agent_info['id']} ({agent_info.get('name', 'unnamed')})")
            print(f"  Workspace: {agent_info['workspace']}")
            print(f"{'=' * 60}")
            run_setup_for_agent(agent_info['id'], Path(agent_info['workspace']), args.timezone, args.dry_run)
        print(f"\n✅ All {len(agents)} agent(s) processed.")
        sys.exit(0)

    # Extract args for single-agent mode
    agent_id = args.agent
    timezone = args.timezone
    dry_run = args.dry_run

    # Determine workspace for single agent
    if args.workspace:
        workspace = Path(args.workspace)
    else:
        # Try to detect from openclaw
        agents = discover_agents()
        workspace = None
        for a in agents:
            if a['id'] == agent_id:
                workspace = Path(a['workspace'])
                break
        if not workspace:
            workspace = Path(os.getcwd())

    run_setup_for_agent(agent_id, workspace, timezone, dry_run)

def run_setup_for_agent(agent_id, workspace, timezone="UTC", dry_run=False):
    """Run the full setup for a single agent."""
    memory_dir = workspace / "memory"
    skill_dir = Path(__file__).parent.parent  # Go up from scripts/ to skill root

    print(f"\n{'=' * 60}")
    print(f"  Memory Lifecycle Setup")
    print(f"  Agent: {agent_id}")
    print(f"  Workspace: {workspace}")
    print(f"  Timezone: {timezone}")
    if dry_run:
        print(f"  Mode: DRY RUN (no changes will be made)")
    print(f"{'=' * 60}\n")

    # Step 1: Create structured memory files
    print("📁 Step 1: Creating structured memory files...\n")
    create_file(memory_dir / "people.md", PEOPLE_TEMPLATE, dry_run)
    create_file(memory_dir / "decisions.md", DECISIONS_TEMPLATE, dry_run)
    create_file(memory_dir / "lessons.md", LESSONS_TEMPLATE, dry_run)
    if not (memory_dir / "commitments.md").exists():
        create_file(memory_dir / "commitments.md", COMMITMENTS_TEMPLATE, dry_run)
    else:
        print(f"  [SKIP] {memory_dir / 'commitments.md'} already exists")
    create_file(memory_dir / "archive" / ".gitkeep", "", dry_run)
    create_file(memory_dir / "wisdom" / ".gitkeep", "", dry_run)

    # Step 2: Add Recent buffer to MEMORY.md
    print("\n📋 Step 2: Adding ## Recent buffer to MEMORY.md...\n")
    add_recent_buffer(workspace / "MEMORY.md", dry_run)

    # Step 3: Update HEARTBEAT.md
    print("\n💓 Step 3: Adding Memory Micro-Attention to HEARTBEAT.md...\n")
    update_heartbeat(workspace / "HEARTBEAT.md", dry_run)

    # Step 4: Create cron jobs
    print("\n⏰ Step 4: Creating cron jobs...\n")
    schedules = get_cron_schedules(timezone)
    created_jobs = create_cron_jobs(agent_id, schedules, skill_dir, dry_run)

    # Summary
    print(f"\n{'=' * 60}")
    print(f"  Setup complete!")
    print(f"{'=' * 60}")
    print(f"\n  Structured files: memory/people.md, decisions.md, lessons.md, commitments.md")
    print(f"  Archive dirs: memory/archive/, memory/wisdom/")
    print(f"  MEMORY.md: ## Recent buffer added")
    print(f"  HEARTBEAT.md: Memory Micro-Attention added")
    print(f"  Cron jobs: {len(created_jobs)} created")
    print(f"\n  Next steps:")
    print(f"  1. Populate people.md with known contacts")
    print(f"  2. Add existing commitments to commitments.md")
    print(f"  3. The first nightly cycle will run at midnight UTC")
    print(f"  4. Monitor the first few cycles and iterate")
    print()


if __name__ == "__main__":
    main()
