#!/usr/bin/env bash
set -euo pipefail

# Memory Boost — Installer
# Installs the skill, sets up memory directory, and adds 5 cron jobs.

OPENCLAW_DIR="${OPENCLAW_DIR:-$HOME/.openclaw}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# --- Usage ---
usage() {
  echo "Usage: ./install.sh"
  echo ""
  echo "Options:"
  echo "  --openclaw PATH      OpenClaw home directory (default: ~/.openclaw)"
  echo "  --help               Show this help"
  exit 1
}

# --- Parse args ---
while [[ $# -gt 0 ]]; do
  case "$1" in
    --openclaw)  OPENCLAW_DIR="$2"; shift 2 ;;
    --help)      usage ;;
    *)           echo "Unknown option: $1"; usage ;;
  esac
done

# --- Validate ---
if [[ ! -d "$OPENCLAW_DIR" ]]; then
  echo "Error: OpenClaw directory not found at $OPENCLAW_DIR"
  echo "Set --openclaw to your OpenClaw home directory."
  exit 1
fi

# --- 1. Install the skill ---
SKILL_DIR="$OPENCLAW_DIR/skills/memory-boost"
mkdir -p "$SKILL_DIR/templates" "$SKILL_DIR/prompts" "$SKILL_DIR/examples"
cp "$SCRIPT_DIR/SKILL.md" "$SKILL_DIR/SKILL.md"

for file in templates/TEMPLATE.md templates/LOOP-STATE.md; do
  if [[ -f "$SCRIPT_DIR/$file" ]]; then
    cp "$SCRIPT_DIR/$file" "$SKILL_DIR/$file"
  fi
done
for file in prompts/*.md; do
  if [[ -f "$SCRIPT_DIR/$file" ]]; then
    cp "$SCRIPT_DIR/$file" "$SKILL_DIR/$file"
  fi
done
for file in examples/*.md; do
  if [[ -f "$SCRIPT_DIR/$file" ]]; then
    cp "$SCRIPT_DIR/$file" "$SKILL_DIR/$file"
  fi
done

echo "Installed skill to $SKILL_DIR/"

# --- 2. Set up memory directory ---
MEMORY_DIR="$OPENCLAW_DIR/memory"
TASKS_DIR="$MEMORY_DIR/tasks"
mkdir -p "$TASKS_DIR"

if [[ ! -f "$MEMORY_DIR/TEMPLATE.md" ]]; then
  cp "$SCRIPT_DIR/templates/TEMPLATE.md" "$MEMORY_DIR/TEMPLATE.md"
  echo "Copied TEMPLATE.md to $MEMORY_DIR/"
else
  echo "TEMPLATE.md already exists, skipping."
fi

if [[ ! -f "$MEMORY_DIR/LOOP-STATE.md" ]]; then
  cp "$SCRIPT_DIR/templates/LOOP-STATE.md" "$MEMORY_DIR/LOOP-STATE.md"
  echo "Copied LOOP-STATE.md to $MEMORY_DIR/"
else
  echo "LOOP-STATE.md already exists, skipping."
fi

if [[ ! -f "$MEMORY_DIR/TASK-INDEX.md" ]]; then
  cp "$SCRIPT_DIR/examples/TASK-INDEX.md" "$MEMORY_DIR/TASK-INDEX.md"
  echo "Copied TASK-INDEX.md to $MEMORY_DIR/"
else
  echo "TASK-INDEX.md already exists, skipping."
fi

# --- 3. Add cron jobs ---
WATCHDOG_PROMPT="$(cat "$SCRIPT_DIR/prompts/watchdog-prompt.md")"
REPLAYER_PROMPT="$(cat "$SCRIPT_DIR/prompts/replayer-prompt.md")"
ESCALATOR_PROMPT="$(cat "$SCRIPT_DIR/prompts/escalator-prompt.md")"
VALIDATOR_PROMPT="$(cat "$SCRIPT_DIR/prompts/validator-prompt.md")"
SMOKETEST_PROMPT="$(cat "$SCRIPT_DIR/prompts/smoke-test-prompt.md")"

if command -v openclaw &>/dev/null; then
  echo "Using OpenClaw CLI to add cron jobs..."

  add_job_if_missing() {
    local name="$1" cron="$2" prompt="$3"
    if openclaw cron list 2>/dev/null | grep -q "$name"; then
      echo "  Skipped (already exists): $name"
    else
      openclaw cron add \
        --name "$name" \
        --cron "$cron" \
        --session isolated \
        --message "$prompt" \
        --announce 2>/dev/null && echo "  Added job: $name" || echo "  Warning: failed to add $name via CLI"
    fi
  }

  add_job_if_missing "boost-watchdog"    "*/15 * * * *" "$WATCHDOG_PROMPT"
  add_job_if_missing "boost-replayer"    "*/30 * * * *" "$REPLAYER_PROMPT"
  add_job_if_missing "boost-escalator"   "0 * * * *"    "$ESCALATOR_PROMPT"
  add_job_if_missing "boost-validator"   "5 * * * *"    "$VALIDATOR_PROMPT"
  add_job_if_missing "boost-smoke-test"  "0 */6 * * *"  "$SMOKETEST_PROMPT"

else
  echo "OpenClaw CLI not found. Merging jobs directly into jobs.json..."

  JOBS_FILE="$OPENCLAW_DIR/cron/jobs.json"
  mkdir -p "$OPENCLAW_DIR/cron"
  NOW="$(date -u +"%Y-%m-%dT%H:%M:%S.000000+00:00")"

  python3 - "$JOBS_FILE" "$NOW" \
    "$WATCHDOG_PROMPT" "$REPLAYER_PROMPT" "$ESCALATOR_PROMPT" \
    "$VALIDATOR_PROMPT" "$SMOKETEST_PROMPT" <<'PYEOF'
import json, sys, secrets, os

jobs_file = sys.argv[1]
now = sys.argv[2]

SKILL_NAME = "memory-boost"

prompts = {
    "boost-watchdog":    {"prompt": sys.argv[3], "cron": "*/15 * * * *"},
    "boost-replayer":    {"prompt": sys.argv[4], "cron": "*/30 * * * *"},
    "boost-escalator":   {"prompt": sys.argv[5], "cron": "0 * * * *"},
    "boost-validator":   {"prompt": sys.argv[6], "cron": "5 * * * *"},
    "boost-smoke-test":  {"prompt": sys.argv[7], "cron": "0 */6 * * *"},
}

if os.path.exists(jobs_file):
    with open(jobs_file) as f:
        data = json.load(f)
else:
    data = {"jobs": []}

existing_names = {j["name"] for j in data["jobs"]}
added = []
skipped = []

for name, info in prompts.items():
    if name in existing_names:
        skipped.append(name)
        continue
    job = {
        "id": secrets.token_hex(6),
        "name": name,
        "prompt": info["prompt"],
        "skills": [SKILL_NAME],
        "skill": SKILL_NAME,
        "model": None,
        "provider": None,
        "base_url": None,
        "schedule": {
            "kind": "cron",
            "expression": info["cron"],
            "display": info["cron"]
        },
        "schedule_display": info["cron"],
        "repeat": {"times": None, "completed": 0},
        "enabled": True,
        "state": "scheduled",
        "paused_at": None,
        "paused_reason": None,
        "created_at": now,
        "next_run_at": now,
        "last_run_at": None,
        "last_status": None,
        "last_error": None,
        "deliver": "origin",
        "origin": None,
    }
    data["jobs"].append(job)
    added.append(name)

with open(jobs_file, "w") as f:
    json.dump(data, f, indent=2)

for name in added:
    print(f"  Added job: {name}")
for name in skipped:
    print(f"  Skipped (already exists): {name}")
PYEOF
fi

echo ""
echo "Done. Installed:"
echo "  - Skill:      $SKILL_DIR/"
echo "  - Memory:     $MEMORY_DIR/"
echo "  - Cron jobs:  5 jobs configured"
echo ""
echo "Your agent will now automatically create task notes for every task."
echo "For long tasks, use /loop-start to arm the keep-alive loop."
echo "When done, /loop-stop to stop burning tokens."
