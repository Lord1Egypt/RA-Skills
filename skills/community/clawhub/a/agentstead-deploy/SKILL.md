# AgentStead Deploy Skill

Deploy and manage AI agents on [AgentStead](https://agentstead.com) cloud hosting.

## Prerequisites

- An AgentStead account (sign up at https://agentstead.com/signup)
- `curl` and `jq` installed (standard on most systems)
- An auth token from logging in

## Authentication

First, log in to get an auth token. The skill provides a helper script that safely handles credentials:

```bash
# Save the deploy helper script
cat > /tmp/agentstead-deploy.sh << 'SCRIPT'
#!/bin/bash
# AgentStead Deploy Helper — handles JSON escaping safely
set -e

API="https://www.agentstead.com/api"
TOKEN_FILE="$HOME/.agentstead-token"

cmd_login() {
  local email="${1:-$AGENTSTEAD_EMAIL}" password="${2:-$AGENTSTEAD_PASSWORD}"
  if [ -z "$email" ]; then
    read -p "Email: " email
  fi
  if [ -z "$password" ]; then
    read -sp "Password: " password
    echo
  fi
  local body
  body=$(jq -n --arg e "$email" --arg p "$password" '{email: $e, password: $p}')
  local resp
  resp=$(curl -s -X POST "$API/auth/login" -H "Content-Type: application/json" -d "$body")
  local token
  token=$(echo "$resp" | jq -r '.token // empty')
  if [ -z "$token" ]; then
    echo "ERROR: Login failed — $(echo "$resp" | jq -r '.error // "unknown error"')" >&2
    return 1
  fi
  echo "$token" > "$TOKEN_FILE"
  chmod 600 "$TOKEN_FILE"
  echo "OK: Logged in successfully"
}

cmd_create() {
  local name="$1" plan="${2:-STARTER}" ai_plan="${3:-PAYG}" model="${4:-SONNET}"
  local token
  token=$(cat "$TOKEN_FILE" 2>/dev/null) || { echo "ERROR: Not logged in" >&2; return 1; }
  local body
  body=$(jq -n \
    --arg name "$name" \
    --arg plan "$plan" \
    --arg aiPlan "$ai_plan" \
    --arg model "$model" \
    '{name: $name, plan: $plan, aiPlan: $aiPlan, defaultModel: $model}')
  curl -s -X POST "$API/agents" \
    -H "Content-Type: application/json" \
    -H "x-cognito-id: $(cat "$TOKEN_FILE")" \
    -d "$body" | jq .
}

cmd_configure() {
  local agent_id="$1" personality="$2"
  local token
  token=$(cat "$TOKEN_FILE" 2>/dev/null) || { echo "ERROR: Not logged in" >&2; return 1; }
  local body
  body=$(jq -n --arg p "$personality" '{personality: $p}')
  curl -s -X PATCH "$API/agents/$agent_id" \
    -H "Content-Type: application/json" \
    -H "x-cognito-id: $(cat "$TOKEN_FILE")" \
    -d "$body" | jq .
}

cmd_channel() {
  local agent_id="$1" type="$2" bot_token="$3"
  local token
  token=$(cat "$TOKEN_FILE" 2>/dev/null) || { echo "ERROR: Not logged in" >&2; return 1; }
  local body
  body=$(jq -n --arg t "$type" --arg bt "$bot_token" '{type: $t, config: {botToken: $bt}}')
  curl -s -X POST "$API/agents/$agent_id/channels" \
    -H "Content-Type: application/json" \
    -H "x-cognito-id: $(cat "$TOKEN_FILE")" \
    -d "$body" | jq .
}

cmd_start() {
  local agent_id="$1"
  local token
  token=$(cat "$TOKEN_FILE" 2>/dev/null) || { echo "ERROR: Not logged in" >&2; return 1; }
  curl -s -X POST "$API/agents/$agent_id/start" \
    -H "Content-Type: application/json" \
    -H "x-cognito-id: $(cat "$TOKEN_FILE")" | jq .
}

cmd_stop() {
  local agent_id="$1"
  local token
  token=$(cat "$TOKEN_FILE" 2>/dev/null) || { echo "ERROR: Not logged in" >&2; return 1; }
  curl -s -X POST "$API/agents/$agent_id/stop" \
    -H "Content-Type: application/json" \
    -H "x-cognito-id: $(cat "$TOKEN_FILE")" | jq .
}

cmd_list() {
  local token
  token=$(cat "$TOKEN_FILE" 2>/dev/null) || { echo "ERROR: Not logged in" >&2; return 1; }
  curl -s "$API/agents" \
    -H "x-cognito-id: $(cat "$TOKEN_FILE")" | jq '.agents[] | {id, name, status, plan, aiPlan, defaultModel}'
}

cmd_subscribe() {
  local agent_id="$1" astd_cost="$2"
  local token
  token=$(cat "$TOKEN_FILE" 2>/dev/null) || { echo "ERROR: Not logged in" >&2; return 1; }
  local body
  body=$(jq -n --argjson cost "$astd_cost" '{planAstdCost: $cost}')
  curl -s -X POST "$API/agents/$agent_id/subscribe-astd" \
    -H "Content-Type: application/json" \
    -H "x-cognito-id: $(cat "$TOKEN_FILE")" \
    -d "$body" | jq .
}

case "$1" in
  login)     cmd_login "$2" "$3" ;;
  create)    cmd_create "$2" "$3" "$4" "$5" ;;
  configure) cmd_configure "$2" "$3" ;;
  channel)   cmd_channel "$2" "$3" "$4" ;;
  start)     cmd_start "$2" ;;
  stop)      cmd_stop "$2" ;;
  list)      cmd_list ;;
  subscribe) cmd_subscribe "$2" "$3" ;;
  *) echo "Usage: agentstead-deploy.sh {login|create|configure|channel|start|stop|list|subscribe}" ;;
esac
SCRIPT
chmod +x /tmp/agentstead-deploy.sh
```

## Usage

### 1. Log in

```bash
# Option A: Use environment variables (recommended)
export AGENTSTEAD_EMAIL="user@example.com"
export AGENTSTEAD_PASSWORD="password123"
/tmp/agentstead-deploy.sh login

# Option B: Interactive prompts (password hidden)
/tmp/agentstead-deploy.sh login

# Option C: Pass email only, prompt for password
/tmp/agentstead-deploy.sh login "user@example.com"
```

### 2. Create an agent

```bash
# Args: name, hardware_plan, ai_plan, default_model
/tmp/agentstead-deploy.sh create "My Agent" "STARTER" "PAYG" "SONNET"
```

**Hardware plans:** STARTER ($9/mo), PRO ($29/mo), BUSINESS ($59/mo), ENTERPRISE ($99/mo)

**AI plans:** BYOK (bring your own key), PAYG (pay-as-you-go from ASTD wallet), ASTD_1000–ASTD_10000

**Models (AgentStead Provided):**
- Anthropic: HAIKU, SONNET, OPUS
- AWS Bedrock: BEDROCK_HAIKU, BEDROCK_SONNET, BEDROCK_OPUS, BEDROCK_HAIKU45, BEDROCK_NOVA_PRO, BEDROCK_NOVA_LITE, BEDROCK_NOVA_MICRO, BEDROCK_LLAMA4_MAVERICK, BEDROCK_LLAMA33_70B, BEDROCK_DEEPSEEK_R1, BEDROCK_MISTRAL_LARGE, BEDROCK_COMMAND_R_PLUS
- Ollama (free): DEEPSEEK_V3, QWEN3, LLAMA4, GEMMA3, MISTRAL_LARGE, GLM5, KIMI_K2, MINIMAX

### 3. Activate subscription (deduct ASTD from wallet)

```bash
# Args: agent_id, astd_cost (900=Starter, 2900=Pro, 5900=Business, 9900=Enterprise)
/tmp/agentstead-deploy.sh subscribe "agent-uuid-here" 900
```

### 4. Set personality

```bash
/tmp/agentstead-deploy.sh configure "agent-uuid-here" "You are a helpful coding assistant specializing in Python."
```

### 5. Add a channel (Telegram, Discord, WhatsApp, Slack)

```bash
/tmp/agentstead-deploy.sh channel "agent-uuid-here" "TELEGRAM" "123456:ABC-DEF..."
```

### 6. Start the agent

```bash
/tmp/agentstead-deploy.sh start "agent-uuid-here"
```

### 7. List agents

```bash
/tmp/agentstead-deploy.sh list
```

### 8. Stop an agent

```bash
/tmp/agentstead-deploy.sh stop "agent-uuid-here"
```

## Security

- All user input is passed through `jq` for safe JSON encoding — never interpolated directly into shell commands
- Auth tokens are stored in `$HOME/.agentstead-token` with 600 permissions (owner-only read)
- Credentials are read from environment variables or interactive prompts — never passed as CLI arguments
- All API calls use HTTPS
- Network access is restricted to agentstead.com only
