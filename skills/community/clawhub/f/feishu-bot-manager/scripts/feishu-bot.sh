#!/bin/bash
# Feishu Bot Manager - Complete CRUD for OpenClaw Feishu bots
# Usage: feishu-bot.sh <command> [options]
# Commands: add, delete, update, list, info

set -e

# Default values
DEFAULT_MODEL="bailian-coding-plan/glm-5"
OPENCLAW_CONFIG="$HOME/.openclaw/openclaw.json"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_error() { echo -e "${RED}❌ $1${NC}"; }
print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
print_warn() { echo -e "${YELLOW}⚠️  $1${NC}"; }

# Check prerequisites
check_prerequisites() {
  if [[ ! -f "$OPENCLAW_CONFIG" ]]; then
    print_error "OpenClaw config file not found at $OPENCLAW_CONFIG"
    exit 1
  fi
  
  if ! command -v jq &> /dev/null; then
    print_error "jq is required but not installed"
    exit 1
  fi
}

# Backup config
backup_config() {
  local BACKUP_TIME=$(TZ='Asia/Shanghai' date +%Y.%m%d.%H%M)
  local BACKUP_FILE="$OPENCLAW_CONFIG.bak.$BACKUP_TIME"
  cp "$OPENCLAW_CONFIG" "$BACKUP_FILE"
  print_info "Backup saved: $BACKUP_FILE"
}

# Check if bot exists
bot_exists() {
  local bot_id="$1"
  local existing=$(jq -r --arg bot_id "$bot_id" '.agents.list[]? | select(.id == $bot_id) | .id' "$OPENCLAW_CONFIG" 2>/dev/null)
  [[ -n "$existing" ]]
}

# ADD command
cmd_add() {
  local bot_id="" app_id="" app_secret="" model=""
  
  while [[ $# -gt 0 ]]; do
    case $1 in
      --botId) bot_id="$2"; shift 2 ;;
      --appId) app_id="$2"; shift 2 ;;
      --appSecret) app_secret="$2"; shift 2 ;;
      --model) model="$2"; shift 2 ;;
      *) shift ;;
    esac
  done
  
  if [[ -z "$bot_id" || -z "$app_id" || -z "$app_secret" ]]; then
    print_error "Missing required parameters"
    echo "Usage: feishu-bot.sh add --botId <id> --appId <id> --appSecret <secret> [--model <model>]"
    exit 1
  fi
  
  model="${model:-$DEFAULT_MODEL}"
  
  check_prerequisites
  
  # Check if bot already exists
  if bot_exists "$bot_id"; then
    print_error "Bot '$bot_id' already exists!"
    echo ""
    echo "Existing bots:"
    jq -r '.agents.list[]?.id' "$OPENCLAW_CONFIG" | sed 's/^/  - /'
    exit 1
  fi
  
  backup_config
  
  # Define paths
  local workspace_path="$HOME/.openclaw/workspace-$bot_id"
  local agent_dir="$HOME/.openclaw/agents/$bot_id/agent"
  
  # Create directories
  mkdir -p "$workspace_path" "$agent_dir"
  print_info "Created workspace: $workspace_path"
  print_info "Created agent dir: $agent_dir"
  
  # Modify config using jq
  local tmp_file=$(mktemp)
  jq --arg bot_id "$bot_id" \
     --arg workspace "$workspace_path" \
     --arg agent_dir "$agent_dir" \
     --arg model "$model" \
     --arg app_id "$app_id" \
     --arg app_secret "$app_secret" \
     '
     .agents.list += [{
       "id": $bot_id,
       "name": $bot_id,
       "workspace": $workspace,
       "agentDir": $agent_dir,
       "model": $model
     }] |
     .channels.feishu.accounts[$bot_id] = {
       "appId": $app_id,
       "appSecret": $app_secret,
       "groupPolicy": "open",
       "dmPolicy": "open",
       "allowFrom": ["*"],
       "connectionMode": "websocket"
     } |
     .bindings += [{
       "agentId": $bot_id,
       "match": {
         "channel": "feishu",
         "accountId": $bot_id
       }
     }]
     ' "$OPENCLAW_CONFIG" > "$tmp_file"
  
  mv "$tmp_file" "$OPENCLAW_CONFIG"
  
  print_success "Bot '$bot_id' added successfully!"
  echo ""
  echo "Summary:"
  echo "  - Bot ID: $bot_id"
  echo "  - Model: $model"
  echo "  - Workspace: $workspace_path"
  echo "  - Agent Dir: $agent_dir"
  echo ""
  print_warn "Run 'openclaw gateway restart' to apply changes"
}

# DELETE command
cmd_delete() {
  local bot_id=""
  
  while [[ $# -gt 0 ]]; do
    case $1 in
      --botId) bot_id="$2"; shift 2 ;;
      *) shift ;;
    esac
  done
  
  if [[ -z "$bot_id" ]]; then
    print_error "Missing botId parameter"
    echo "Usage: feishu-bot.sh delete --botId <id>"
    exit 1
  fi
  
  check_prerequisites
  
  # Check if bot exists
  if ! bot_exists "$bot_id"; then
    print_error "Bot '$bot_id' not found!"
    exit 1
  fi
  
  backup_config
  
  # Define paths
  local workspace_path="$HOME/.openclaw/workspace-$bot_id"
  local agent_dir="$HOME/.openclaw/agents/$bot_id"
  
  # Modify config using jq
  local tmp_file=$(mktemp)
  jq --arg bot_id "$bot_id" '
    .agents.list = [.agents.list[]? | select(.id != $bot_id)] |
    .channels.feishu.accounts = del(.channels.feishu.accounts[$bot_id]) |
    .bindings = [.bindings[]? | select(.agentId != $bot_id)]
  ' "$OPENCLAW_CONFIG" > "$tmp_file"
  
  mv "$tmp_file" "$OPENCLAW_CONFIG"
  
  # Remove directories (ask first)
  if [[ -d "$workspace_path" || -d "$agent_dir" ]]; then
    echo ""
    read -p "Delete workspace and agent directories? [y/N] " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
      rm -rf "$workspace_path" "$agent_dir"
      print_info "Deleted: $workspace_path"
      print_info "Deleted: $agent_dir"
    fi
  fi
  
  print_success "Bot '$bot_id' deleted successfully!"
  print_warn "Run 'openclaw gateway restart' to apply changes"
}

# UPDATE command
cmd_update() {
  local bot_id="" model="" app_id="" app_secret=""
  
  while [[ $# -gt 0 ]]; do
    case $1 in
      --botId) bot_id="$2"; shift 2 ;;
      --model) model="$2"; shift 2 ;;
      --appId) app_id="$2"; shift 2 ;;
      --appSecret) app_secret="$2"; shift 2 ;;
      *) shift ;;
    esac
  done
  
  if [[ -z "$bot_id" ]]; then
    print_error "Missing botId parameter"
    echo "Usage: feishu-bot.sh update --botId <id> [--model <model>] [--appId <id>] [--appSecret <secret>]"
    exit 1
  fi
  
  if [[ -z "$model" && -z "$app_id" && -z "$app_secret" ]]; then
    print_error "At least one of --model, --appId, --appSecret is required"
    exit 1
  fi
  
  check_prerequisites
  
  # Check if bot exists
  if ! bot_exists "$bot_id"; then
    print_error "Bot '$bot_id' not found!"
    exit 1
  fi
  
  backup_config
  
  # Build jq update commands
  local jq_cmd="."
  
  if [[ -n "$model" ]]; then
    jq_cmd="$jq_cmd | .agents.list = [.agents.list[]? | if .id == \$bot_id then .model = \$model else . end]"
  fi
  
  if [[ -n "$app_id" ]]; then
    jq_cmd="$jq_cmd | .channels.feishu.accounts[\$bot_id].appId = \$app_id"
  fi
  
  if [[ -n "$app_secret" ]]; then
    jq_cmd="$jq_cmd | .channels.feishu.accounts[\$bot_id].appSecret = \$app_secret"
  fi
  
  local tmp_file=$(mktemp)
  jq --arg bot_id "$bot_id" \
     --arg model "$model" \
     --arg app_id "$app_id" \
     --arg app_secret "$app_secret" \
     "$jq_cmd" "$OPENCLAW_CONFIG" > "$tmp_file"
  
  mv "$tmp_file" "$OPENCLAW_CONFIG"
  
  print_success "Bot '$bot_id' updated successfully!"
  
  if [[ -n "$model" ]]; then echo "  - Model: $model"; fi
  if [[ -n "$app_id" ]]; then echo "  - App ID: $app_id"; fi
  if [[ -n "$app_secret" ]]; then echo "  - App Secret: (updated)"; fi
  
  print_warn "Run 'openclaw gateway restart' to apply changes"
}

# LIST command
cmd_list() {
  check_prerequisites
  
  echo "Feishu Bots:"
  echo ""
  
  local count=$(jq '[.agents.list[]? | select(.id != "main")] | length' "$OPENCLAW_CONFIG")
  
  if [[ "$count" -eq 0 ]]; then
    print_info "No Feishu bots configured"
    return
  fi
  
  jq -r '.agents.list[]? | select(.id != "main") | "  \(.id) - Model: \(.model)"' "$OPENCLAW_CONFIG"
  echo ""
  echo "Total: $count bot(s)"
}

# INFO command
cmd_info() {
  local bot_id=""
  
  while [[ $# -gt 0 ]]; do
    case $1 in
      --botId) bot_id="$2"; shift 2 ;;
      *) shift ;;
    esac
  done
  
  if [[ -z "$bot_id" ]]; then
    print_error "Missing botId parameter"
    echo "Usage: feishu-bot.sh info --botId <id>"
    exit 1
  fi
  
  check_prerequisites
  
  if ! bot_exists "$bot_id"; then
    print_error "Bot '$bot_id' not found!"
    exit 1
  fi
  
  echo "Bot: $bot_id"
  echo ""
  
  echo "Agent Config:"
  jq -r --arg bot_id "$bot_id" '.agents.list[]? | select(.id == $bot_id) | "  Model: \(.model)\n  Workspace: \(.workspace)\n  Agent Dir: \(.agentDir)"' "$OPENCLAW_CONFIG"
  
  echo ""
  echo "Feishu Account:"
  jq -r --arg bot_id "$bot_id" '.channels.feishu.accounts[$bot_id] | "  App ID: \(.appId)\n  Group Policy: \(.groupPolicy)\n  DM Policy: \(.dmPolicy)\n  Connection: \(.connectionMode)"' "$OPENCLAW_CONFIG"
}

# Main command dispatcher
case "$1" in
  add) shift; cmd_add "$@" ;;
  delete) shift; cmd_delete "$@" ;;
  update) shift; cmd_update "$@" ;;
  list) shift; cmd_list "$@" ;;
  info) shift; cmd_info "$@" ;;
  *)
    echo "Feishu Bot Manager"
    echo ""
    echo "Usage: feishu-bot.sh <command> [options]"
    echo ""
    echo "Commands:"
    echo "  add     Add a new Feishu bot"
    echo "  delete  Delete a Feishu bot"
    echo "  update  Update a Feishu bot"
    echo "  list    List all Feishu bots"
    echo "  info    Show bot details"
    echo ""
    echo "Examples:"
    echo "  feishu-bot.sh add --botId mybot --appId cli_xxx --appSecret xxx"
    echo "  feishu-bot.sh update --botId mybot --model kimi-k2.5"
    echo "  feishu-bot.sh delete --botId mybot"
    echo "  feishu-bot.sh list"
    echo "  feishu-bot.sh info --botId mybot"
    exit 1
    ;;
esac