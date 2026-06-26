#!/bin/bash

# ==========================================
# OpenClaw automated agent creation script, optimized for openclaw.json
# $1: agent_id, for example: product_manager
# $2: agent_display_name, for example: Product Manager
# $3: identity_prompt, detailed persona/system prompt
# ==========================================

if [ "$#" -ne 3 ]; then
    echo "❌ Error: Invalid number of arguments."
    exit 1
fi

AGENT_ID=$1
DISPLAY_NAME=$2
PERSONA=$3
WORKSPACE_DIR="$HOME/.openclaw/workspace-${AGENT_ID}"
# Main OpenClaw configuration file
CONFIG_FILE="$HOME/.openclaw/openclaw.json"

echo "🚀 [1/3] Creating Agent ID: ${AGENT_ID}..."

# ------------------------------------------
# Step 1: Create the base agent entry
# ------------------------------------------
if openclaw agents add "${AGENT_ID}" --workspace "${WORKSPACE_DIR}"; then
    echo "✅ Base agent entry created."
else
    echo "❌ Agent creation failed. The ID [${AGENT_ID}] may already exist."
    exit 1
fi

# ------------------------------------------
# Step 2: Update the display name in openclaw.json
# ------------------------------------------
echo "📝 [2/3] Updating ${CONFIG_FILE} with display name: ${DISPLAY_NAME}..."

if [ -f "$CONFIG_FILE" ]; then
    # Use Python to update agents -> list -> name in the JSON config.
    AGENT_ID="$AGENT_ID" DISPLAY_NAME="$DISPLAY_NAME" CONFIG_FILE="$CONFIG_FILE" python3 <<'PY'
import json, os
path = os.path.expanduser(os.environ['CONFIG_FILE'])
agent_id = os.environ['AGENT_ID']
display_name = os.environ['DISPLAY_NAME']

with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Find the matching agent in agents -> list.
agents_list = data.get('agents', {}).get('list', [])
found = False
for agent in agents_list:
    if agent.get('id') == agent_id:
        agent['name'] = display_name
        found = True
        break

if found:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f'✅ Updated the name for ID [{agent_id}] to [{display_name}]')
else:
    print('⚠️ No matching agent entry found in openclaw.json')
PY
else
    echo "❌ Error: Config file not found: $CONFIG_FILE"
    exit 1
fi

# ------------------------------------------
# Step 3: Inject the persona/system prompt
# ------------------------------------------
echo "🧠 [3/3] Injecting persona for ID [${AGENT_ID}]..."
FULL_MESSAGE=$(printf 'Remember your identity and operating instructions:\n%s' "$PERSONA")

if openclaw agent --agent "${AGENT_ID}" --message "${FULL_MESSAGE}"; then
    echo "✅ Persona injection completed."
else
    echo "❌ Persona injection failed. Please check the agent status manually."
fi

echo "🎉 SUCCESS! Agent [${DISPLAY_NAME}] is ready."
exit 0
