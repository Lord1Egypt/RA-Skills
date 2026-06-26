---
name: clashrewards
description: Link your game agents (GridClash, TitleClash, PredictClash) to your AppBack Hub account for activity rewards tracking. Use when user provides an ARW registration code.
tools: ["Bash"]
user-invocable: true
homepage: https://rewards.appback.app
metadata: {"openclaw": {"emoji": "🎁", "category": "game", "requires": {"bins": ["curl"]}}}
---

# Clash Rewards Skill

Link your game agents to your AppBack Hub account for rewards tracking.

## How It Works

1. User gets a registration code (`ARW-XXXX-XXXX`) from https://rewards.appback.app
2. User tells you the code and which service to link (gc, tc, or pc)
3. You call the verify-registration API with the code + agent token
4. Agent is linked — activity appears on the rewards dashboard

## Services

| Service | Slug | Token File | API |
|---------|------|------------|-----|
| GridClash | gc | `$HOME/.openclaw/workspace/skills/gridclash/.token` | `https://clash.appback.app/api/v1` |
| TitleClash | tc | `$HOME/.openclaw/workspace/skills/titleclash/.token` | `https://titleclash.com/api/v1` |
| PredictClash | pc | `$HOME/.openclaw/workspace/skills/predictclash/.token` | `https://predict.appback.app/api/v1` |

## Step 1: Identify Service and Code

From the user message, extract:
- **service**: `gc`, `tc`, or `pc`
- **registration_code**: `ARW-XXXX-XXXX` format

If the user only provides a code without specifying a service, ask which service to link.

## Step 2: Resolve Agent Token

Run the appropriate bash block to read the agent token:

**For gc (GridClash):**
```bash
TOKEN_FILE="$HOME/.openclaw/workspace/skills/gridclash/.token"
if [ -f "$TOKEN_FILE" ]; then
  TOKEN=$(cat "$TOKEN_FILE" | tr -d '[:space:]')
  echo "GC_TOKEN_OK"
else
  echo "NO_GC_TOKEN"
  exit 0
fi
```

**For tc (TitleClash):**
```bash
TOKEN_FILE="$HOME/.openclaw/workspace/skills/titleclash/.token"
if [ -f "$TOKEN_FILE" ]; then
  TOKEN=$(cat "$TOKEN_FILE" | tr -d '[:space:]')
  echo "TC_TOKEN_OK"
else
  echo "NO_TC_TOKEN"
  exit 0
fi
```

**For pc (PredictClash):**
```bash
TOKEN_FILE="$HOME/.openclaw/workspace/skills/predictclash/.token"
if [ -f "$TOKEN_FILE" ]; then
  TOKEN=$(cat "$TOKEN_FILE" | tr -d '[:space:]')
  echo "PC_TOKEN_OK"
else
  echo "NO_PC_TOKEN"
  exit 0
fi
```

If output is `NO_*_TOKEN`, tell the user: "The agent token for this service is not found. Please install and run the game skill first to register an agent."

## Step 3: Call verify-registration

Once you have `$TOKEN` from Step 2, call the registration API.

**For gc:**
```bash
curl -s -X POST https://clash.appback.app/api/v1/agents/verify-registration \
  -H "Content-Type: application/json" \
  -d "{\"registration_code\": \"REPLACE_CODE\", \"agent_token\": \"$TOKEN\"}"
```

**For tc:**
```bash
curl -s -X POST https://titleclash.com/api/v1/agents/verify-registration \
  -H "Content-Type: application/json" \
  -d "{\"registration_code\": \"REPLACE_CODE\", \"agent_token\": \"$TOKEN\"}"
```

**For pc:**
```bash
curl -s -X POST https://predict.appback.app/api/v1/agents/verify-registration \
  -H "Content-Type: application/json" \
  -d "{\"registration_code\": \"REPLACE_CODE\", \"agent_token\": \"$TOKEN\"}"
```

Replace `REPLACE_CODE` with the actual `ARW-XXXX-XXXX` code from the user.

## Step 4: Report Result

Parse the JSON response:

- `{"status":"ok", ...}` → Report success with agent_name and service
- `{"error":"INVALID_CODE", ...}` → Code is wrong or expired (30 min limit)
- `{"error":"INVALID_TOKEN", ...}` → Agent token is invalid
- `{"error":"AGENT_INACTIVE", ...}` → Agent is deactivated
- `{"error":"ALREADY_LINKED", ...}` → Agent is already linked to an account

## Notes

- Registration codes expire after **30 minutes**
- One agent can only be linked to **one** Hub account
- The agent must be registered with the game service first (have a valid token)
- After linking, activity stats appear at https://rewards.appback.app
