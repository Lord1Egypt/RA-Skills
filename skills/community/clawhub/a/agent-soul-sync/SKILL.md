---
name: mysta-sync
description: >-
  Sync local OpenClaw skills to a remote NanoClaw agent on Mysta. Use when the
  user says "sync my skills", "upload skills to mysta", "push skills to my
  nanoclaw agent", or wants to make their local skills available on their cloud
  agent. Connects to the Mysta MCP server to list agents and upload SKILL.md file
  contents. Requires curl, jq, and MYSTA_API_KEY environment variable (API key
  obtained from app.staging.mysta.tech). Reads and uploads local SKILL.md files
  from ~/.openclaw/skills/ or ~/Workspace/openclaw/skills/. Opens browser for
  API key setup (user consent required).
license: MIT
compatibility:
  - curl
  - jq
  - MYSTA_API_KEY
metadata:
  author: mysta
  version: "0.3.0"
  openclaw:
    emoji: "☁️"
    requires:
      allBins: ["curl", "jq"]
      envVars: ["MYSTA_API_KEY"]
      tools: ["read", "exec"]
  clawhub: { "tags": ["mysta", "nanoclaw", "sync", "skills", "cloud"] }
homepage: "https://app.staging.mysta.tech"
---

# Mysta Skill Sync

Sync local OpenClaw skills to a remote NanoClaw agent on the Mysta platform via MCP (Model Context Protocol).

## Authentication

The user needs a Mysta API key (starts with `mysta_`) stored in the `MYSTA_API_KEY` environment variable.

1. Check if the key is already set:

```bash
if [ -n "${MYSTA_API_KEY}" ]; then echo "Key is set"; else echo "Key not set"; fi
```

2. If not set, open the API keys page in their browser:

```bash
# Cross-platform browser open
if command -v xdg-open &>/dev/null; then
  xdg-open "https://app.staging.mysta.tech/en/profile#api-keys"
elif command -v open &>/dev/null; then
  open "https://app.staging.mysta.tech/en/profile#api-keys"
else
  echo "Please visit: https://app.staging.mysta.tech/en/profile#api-keys"
fi
```

3. Tell them: **"Please create a new API key and set it as an environment variable: `export MYSTA_API_KEY=mysta_...`"**

4. Wait for the user to set their key.

Once the key is set, configure the variables for all subsequent commands:

```bash
# API key from environment (required)
: "${MYSTA_API_KEY:?Please set MYSTA_API_KEY environment variable}"

# MCP server URL (defaults to staging, override with MYSTA_MCP_URL for other envs)
MCP_URL="${MYSTA_MCP_URL:-https://api.staging.mysta.tech/api/v2/mcp}"
```

## MCP Protocol

All communication uses the MCP Streamable HTTP transport over HTTPS. Each request is a JSON-RPC call via HTTP POST. No temporary files are written — session IDs are extracted from response headers in-memory. The flow is:

1. **Initialize** a session (get a session ID)
2. **Call tools** using the session ID
3. **Close** the session when done

### Initialize session

```bash
# Extract session ID from response headers without writing temp files
MCP_SESSION=$(curl -sf -X POST "${MCP_URL}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer ${MYSTA_API_KEY}" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"openclaw","version":"1.0.0"}}}' \
  -D- -o /dev/null 2>/dev/null | grep -i "mcp-session-id" | tr -d '\r' | awk '{print $2}')
```

Then send the initialized notification:

```bash
curl -sf -X POST "${MCP_URL}" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${MYSTA_API_KEY}" \
  -H "Mcp-Session-Id: ${MCP_SESSION}" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized"}'
```

### Call a tool

```bash
RESULT=$(curl -sf -X POST "${MCP_URL}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer ${MYSTA_API_KEY}" \
  -H "Mcp-Session-Id: ${MCP_SESSION}" \
  -d "$(jq -n --arg name "TOOL_NAME" --argjson args 'ARGS_JSON' \
    '{jsonrpc:"2.0",id:2,method:"tools/call",params:{name:$name,arguments:$args}}')")
```

The response may be SSE (text/event-stream) — parse `data:` lines for JSON-RPC results.

### Close session

```bash
curl -sf -X DELETE "${MCP_URL}" \
  -H "Authorization: Bearer ${MYSTA_API_KEY}" \
  -H "Mcp-Session-Id: ${MCP_SESSION}"
```

## Workflow

### Step 1: Initialize MCP session

Initialize using the protocol above. Store `MCP_SESSION` for all subsequent calls.

### Step 2: List agents

Call the `mysta_list_agents` tool:

```bash
RESULT=$(curl -sf -X POST "${MCP_URL}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer ${MYSTA_API_KEY}" \
  -H "Mcp-Session-Id: ${MCP_SESSION}" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"mysta_list_agents","arguments":{}}}')
```

Parse the response to find agent IDs and names.

- If **no agents** found, tell the user to create one at https://app.staging.mysta.tech
- If **one agent**, auto-select it
- If **multiple**, ask which one to sync to

### Step 3: Scan local skills

Find all SKILL.md files in the OpenClaw skills directories:

```bash
find ~/.openclaw/skills ~/Workspace/openclaw/skills -maxdepth 2 -name "SKILL.md" -type f 2>/dev/null
```

For each skill, the name is the parent directory name.

Present the list and ask:

- **"all"** → sync everything
- **specific names** → sync only those
- **"cancel"** → abort

### Step 4: Upload skills via MCP

For each selected skill, read the content and call `mysta_sync_skill`:

```bash
SKILL_CONTENT=$(cat "$SKILL_PATH")
RESULT=$(curl -sf -X POST "${MCP_URL}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer ${MYSTA_API_KEY}" \
  -H "Mcp-Session-Id: ${MCP_SESSION}" \
  -d "$(jq -n --arg name "$SKILL_NAME" --arg content "$SKILL_CONTENT" --arg agentId "$AGENT_ID" \
    '{jsonrpc:"2.0",id:3,method:"tools/call",params:{name:"mysta_sync_skill",arguments:{agentId:$agentId,skillName:$name,content:$content}}}')")
```

Alternatively, use `mysta_sync_all_skills` to batch upload:

```bash
# Build skills JSON array
SKILLS_JSON=$(for skill_path in $SELECTED_SKILLS; do
  name=$(basename $(dirname "$skill_path"))
  content=$(cat "$skill_path")
  jq -n --arg name "$name" --arg content "$content" '{name:$name,content:$content}'
done | jq -s '.')

RESULT=$(curl -sf -X POST "${MCP_URL}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer ${MYSTA_API_KEY}" \
  -H "Mcp-Session-Id: ${MCP_SESSION}" \
  -d "$(jq -n --arg agentId "$AGENT_ID" --argjson skills "$SKILLS_JSON" \
    '{jsonrpc:"2.0",id:3,method:"tools/call",params:{name:"mysta_sync_all_skills",arguments:{agentId:$agentId,skills:$skills}}}')")
```

### Step 5: Close session and report results

Close the MCP session, then show a summary:

- Total skills synced
- Any failures with error details
- If the agent's dev pod was running, skills are live immediately
- If not running, tell user to start the dev pod on https://app.staging.mysta.tech to apply skills

## Security Notes

- All API communication uses HTTPS. API keys are transmitted over encrypted connections only.
- The `MYSTA_API_KEY` must be stored as an environment variable, never hardcoded in scripts. Use limited-scope keys and revoke after use.
- No temporary files are written. Session IDs are extracted in-memory from response headers and stored only in shell variables for the duration of the session.
- SKILL.md file contents are read and uploaded to the Mysta server. **Review skill files before syncing** — do not include secrets, credentials, or sensitive data in SKILL.md files.
- API keys are scoped to the authenticated user's agents only.
- This skill requires explicit user consent before: opening a browser, uploading files, or connecting to the Mysta API.

## Notes

- Skills are uploaded to OSS for audit and pushed to the agent's NAS-mounted storage.
- Skills persist across pod restarts.
- Re-uploading a skill with the same name overwrites it (idempotent).
- This does NOT publish the agent. Publishing is a separate action on the Mysta platform.
- The MCP server handles auth, OSS audit, DB metadata update, and live push to running pods — all in one call.
