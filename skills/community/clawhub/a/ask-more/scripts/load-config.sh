#!/usr/bin/env bash
# Load and validate ask-more config.
# Usage: bash scripts/load-config.sh <skill-dir>
# Outputs: config summary to stdout, or exits with error.

set -euo pipefail

SKILL_DIR="${1:-.}"
CONFIG_FILE="$SKILL_DIR/config.yaml"
EXAMPLE_FILE="$SKILL_DIR/config.example.yaml"

# --- Check config exists ---
if [[ ! -f "$CONFIG_FILE" ]]; then
  if [[ -f "$EXAMPLE_FILE" ]]; then
    echo "ERROR: config.yaml not found. Copy config.example.yaml to config.yaml and configure your models." >&2
    exit 1
  else
    echo "ERROR: No config files found in $SKILL_DIR" >&2
    exit 1
  fi
fi

# --- Parse with python for proper YAML handling ---
python3 -c "
import yaml, sys, json

with open('$CONFIG_FILE') as f:
    conf = yaml.safe_load(f)

if not conf:
    print('ERROR: config.yaml is empty or invalid', file=sys.stderr)
    sys.exit(1)

# Validate models
models = conf.get('models', [])
if not models or not isinstance(models, list):
    print('ERROR: No models configured in config.yaml. Add at least 2 models under the \"models:\" key.', file=sys.stderr)
    sys.exit(1)

# Filter out None/empty entries (from commented lines)
models = [m for m in models if m]

if len(models) < 2:
    print(f'ERROR: Need at least 2 models. Currently found: {len(models)}', file=sys.stderr)
    sys.exit(1)

# Validate presets if present
presets = conf.get('presets', {})
if presets and isinstance(presets, dict):
    for name, pool in presets.items():
        if not pool or not isinstance(pool, list) or len(pool) < 2:
            print(f'WARNING: Preset \"{name}\" has fewer than 2 models, it will not be usable.', file=sys.stderr)

# Check synthesis_model is not in the consultation pool
synthesis = conf.get('synthesis_model')
if synthesis and synthesis in models:
    print(f'WARNING: synthesis_model \"{synthesis}\" is also in the models pool. This may introduce bias.', file=sys.stderr)

# Output summary
print(f'Models configured: {len(models)}')
for m in models:
    print(f'  - {m}')

if presets:
    print(f'Presets: {list(presets.keys())}')

if synthesis:
    print(f'Synthesis model: {synthesis}')

min_models = conf.get('min_models', 2)
timeout = conf.get('timeout_seconds', 30)
mode = conf.get('context_mode', 'summary')
print(f'min_models: {min_models}')
print(f'timeout: {timeout}s')
print(f'context_mode: {mode}')
print(f'privacy_acknowledged: {conf.get(\"privacy_acknowledged\", False)}')
" 2>&1
