#!/usr/bin/env bash
# check-models.sh — Check which models are eligible for a given project.
# Usage: bash check-models.sh [project-name]
# If no project is given, shows global model list with routing status.
#
# This script is designed to be called by sub-agents BEFORE selecting a model.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
DATA_DIR="${ORCHESTRATOR_DATA_DIR:-$(cd "$SKILL_DIR/../.." && pwd)/orchestrator-data}"
CONFIG_FILE="$DATA_DIR/dashboard-config.json"
MODELS_FILE="$DATA_DIR/models.json"
PROJECT="${1:-}"

if [ ! -f "$CONFIG_FILE" ]; then
  echo "ERROR: Config not found at $CONFIG_FILE"
  echo "Set ORCHESTRATOR_DATA_DIR or ensure orchestrator-data/ exists."
  exit 1
fi

if [ ! -f "$MODELS_FILE" ]; then
  echo "ERROR: models.json not found at $MODELS_FILE"
  exit 1
fi

# Export for Python
export CONFIG_FILE MODELS_FILE PROJECT

# Use python3 to parse JSON and apply filters
python3 << 'PYEOF'
import json, sys, os

config_file = os.environ.get("CONFIG_FILE", "")
models_file = os.environ.get("MODELS_FILE", "")
project = os.environ.get("PROJECT", "")

with open(config_file) as f:
    cfg = json.load(f)
with open(models_file) as f:
    data = json.load(f)

models = data.get("models", [])
free_only = cfg.get("free_only_mode", False)
disabled = cfg.get("disabled_models", [])
projects_cfg = cfg.get("projects", {})

# Apply global free-only
if free_only:
    models = [m for m in models if m.get("cost", {}).get("type", "") not in ("subscription", "payg", "pay_per_token")]

# Apply global disabled
if disabled:
    models = [m for m in models if m.get("id") not in disabled]

# Apply per-project filters
whitelist = []
proj_free = False
if project:
    proj_cfg = projects_cfg.get(project, {})
    whitelist = proj_cfg.get("model_allowlist", [])
    proj_free = proj_cfg.get("free_only", False)
    if whitelist:
        models = [m for m in models if m.get("id") in whitelist]
    if proj_free:
        models = [m for m in models if m.get("cost", {}).get("type", "") not in ("subscription", "payg", "pay_per_token")]

# Output
print(f"=== Model Routing Report ===")
print(f"Project: {project or '(global)'}")
print(f"Global free-only: {'ON' if free_only else 'OFF'}")
print(f"Global disabled: {len(disabled)} models")
if project:
    print(f"Project allowlist: {len(whitelist) if whitelist else 'not set (all eligible)'}")
    print(f"Project free-only: {'ON' if proj_free else 'OFF'}")
print(f"Eligible models: {len(models)}")
print("")

if not models:
    print("⚠️  NO ELIGIBLE MODELS — check your configuration!")
    sys.exit(1)

# Group by cost type
free_models = [m for m in models if m.get("cost", {}).get("type", "") not in ("subscription", "payg", "pay_per_token")]
paid_models = [m for m in models if m.get("cost", {}).get("type", "") in ("subscription", "payg", "pay_per_token")]

if free_models:
    print(f"--- Free ({len(free_models)}) ---")
    for m in sorted(free_models, key=lambda x: x.get("tier", 99)):
        tier = f"T{m.get('tier', '?')}" if m.get("tier") else "?"
        print(f"  {m['id']:50s} {tier}  {m.get('name', '')}")

if paid_models:
    print(f"\n--- Paid ({len(paid_models)}) ---")
    for m in sorted(paid_models, key=lambda x: x.get("tier", 99)):
        tier = f"T{m.get('tier', '?')}" if m.get("tier") else "?"
        cost = m.get("cost", {})
        cost_str = f"${cost.get('amount', '?')}/{cost.get('period', '?')}" if cost.get("amount") else cost.get("type", "?")
        print(f"  {m['id']:50s} {tier}  {cost_str}  {m.get('name', '')}")

print(f"\n✅ {len(models)} models available for routing")
PYEOF