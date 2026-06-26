#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$HOME/.openclaw/workspace/skills/clawgrid-connector"
source "$SKILL_DIR/scripts/_clawgrid_env.sh"

if [ ! -f "$CONFIG" ]; then
  echo "Config not found at $CONFIG — run setup first" >&2
  exit 1
fi

API_KEY=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_key'])")
API_BASE=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_base'])")

_usage() {
  cat <<EOF
Usage: llm-config.sh <command> [options]

Commands:
  list              List all LLM model presets
  tiers             Show available platform model tiers
  add               Create a new preset
  delete <id>       Delete a preset
  set-default <id>  Set a preset as default

Options for 'add':
  --name <name>     Preset display name (required)
  --tier <tier>     Tier: advanced | intermediate | beginner | custom (default: custom)
  --model <model>   Model ID in provider/model format (required)
  --default         Set as default model

Examples:
  llm-config.sh tiers
  llm-config.sh list
  llm-config.sh add --name "My Claude" --model "anthropic/claude-sonnet-4-6" --default
  llm-config.sh add --name "Fast" --tier beginner --model "google/gemini-3-flash"
  llm-config.sh set-default <preset-id>
  llm-config.sh delete <preset-id>
EOF
  exit 1
}

_api() {
  local method="$1" path="$2"
  shift 2
  curl -s -X "$method" "$API_BASE/api/lobster$path" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    --max-time 15 \
    "$@"
}

cmd_list() {
  local resp
  resp=$(_api GET "/me/llm-presets")
  echo "$resp" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    presets = data.get('presets', [])
    if not presets:
        print('No presets configured. Use \"llm-config.sh add\" to create one.')
        sys.exit(0)
    print(f'{'ID':<38} {'Name':<20} {'Tier':<14} {'Model':<40} {'Default'}')
    print('-' * 130)
    for p in presets:
        default = '*' if p.get('is_default') else ''
        print(f\"{p['id']:<38} {p['name']:<20} {p['tier']:<14} {p['model_id']:<40} {default}\")
except Exception as e:
    print(f'Error: {e}', file=sys.stderr)
    sys.exit(1)
"
}

cmd_tiers() {
  local resp
  resp=$(curl -s "$API_BASE/api/llm/tiers" --max-time 10)
  echo "$resp" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    tiers = data.get('tiers', {})
    for tier_key, tier_def in tiers.items():
        label = tier_def.get('label', tier_key)
        cost = tier_def.get('cost_hint', '?')
        desc = tier_def.get('description', '')
        models = tier_def.get('allowed_models', [])
        print(f'\n{label} ({tier_key}) — cost: {cost}')
        print(f'  {desc}')
        print(f'  Models: {', '.join(models)}')
except Exception as e:
    print(f'Error: {e}', file=sys.stderr)
    sys.exit(1)
"
}

cmd_add() {
  local name="" tier="custom" model="" is_default="false"
  while [ $# -gt 0 ]; do
    case "$1" in
      --name) name="$2"; shift 2 ;;
      --tier) tier="$2"; shift 2 ;;
      --model) model="$2"; shift 2 ;;
      --default) is_default="true"; shift ;;
      *) echo "Unknown option: $1" >&2; _usage ;;
    esac
  done
  if [ -z "$name" ] || [ -z "$model" ]; then
    echo "Error: --name and --model are required" >&2
    _usage
  fi
  local resp
  resp=$(_api POST "/me/llm-presets?name=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$name'))")&tier=$tier&model_id=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$model'))")&is_default=$is_default")
  echo "$resp" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    if 'id' in data:
        print(f\"Created preset: {data['name']} (ID: {data['id']}, model: {data['model_id']})\")
        if data.get('is_default'):
            print('  -> Set as default')
    elif 'detail' in data:
        print(f\"Error: {data['detail']}\", file=sys.stderr)
        sys.exit(1)
    else:
        print(json.dumps(data, indent=2))
except Exception as e:
    print(f'Error: {e}', file=sys.stderr)
    sys.exit(1)
"
}

cmd_delete() {
  local preset_id="$1"
  local resp
  resp=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE \
    "$API_BASE/api/lobster/me/llm-presets/$preset_id" \
    -H "Authorization: Bearer $API_KEY" \
    --max-time 10)
  if [ "$resp" = "204" ]; then
    echo "Deleted preset $preset_id"
  else
    echo "Failed to delete preset (HTTP $resp)" >&2
    exit 1
  fi
}

cmd_set_default() {
  local preset_id="$1"
  local resp
  resp=$(_api PUT "/me/llm-presets/$preset_id/set-default")
  echo "$resp" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    if 'id' in data:
        print(f\"Default model set to: {data['name']} ({data['model_id']})\")
    elif 'detail' in data:
        print(f\"Error: {data['detail']}\", file=sys.stderr)
        sys.exit(1)
except Exception as e:
    print(f'Error: {e}', file=sys.stderr)
    sys.exit(1)
"
}

case "${1:-}" in
  list) cmd_list ;;
  tiers) cmd_tiers ;;
  add) shift; cmd_add "$@" ;;
  delete) cmd_delete "${2:?preset_id required}" ;;
  set-default) cmd_set_default "${2:?preset_id required}" ;;
  *) _usage ;;
esac
