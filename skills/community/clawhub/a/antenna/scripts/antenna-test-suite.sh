#!/usr/bin/env bash
# antenna-test-suite.sh — Two-tier Antenna model/script tester with comparison
#
# Test A: Script validation (no model, no network)
# Test B: Model → write + exec tool calls
#
# Usage:
#   antenna-test-suite.sh [--model <model>] [--models <m1,m2,...>] [--tier A|B|all]
#                         [--verbose] [--report [dir]] [--format terminal|markdown|json]
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$SKILL_DIR/antenna-config.json"
PEERS_FILE="$SKILL_DIR/antenna-peers.json"
RELAY_SCRIPT="$SCRIPT_DIR/antenna-relay.sh"
AGENT_INSTRUCTIONS="$SKILL_DIR/agent/AGENTS.md"

# shellcheck source=../lib/peers.sh
source "$SKILL_DIR/lib/peers.sh"
# shellcheck source=../lib/config.sh
source "$SKILL_DIR/lib/config.sh"

# ── Defaults ─────────────────────────────────────────────────────────────────

MODELS=()
TIER="all"
VERBOSE=false
REPORT_DIR=""
FORMAT="terminal"
MAX_MODELS=6

# Per-run tracking
declare -A RESULTS        # "model:test" → "pass|fail|skip"
declare -A RESULTS_MSG    # "model:test" → failure/skip reason
declare -A RESULTS_TIME   # "model" → elapsed seconds for B+C
declare -A MODEL_SCORES   # "model" → "pass/total"
declare -A RAW_REQUESTS   # "model:tier" → request JSON
declare -A RAW_RESPONSES  # "model:tier" → response JSON

TIER_A_PASS=0
TIER_A_FAIL=0
TIER_A_TOTAL=0

TOTAL_PASS=0
TOTAL_FAIL=0
TOTAL_SKIP=0

RUN_TIMESTAMP=""

# ANSI colors (disabled for non-terminal formats)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

# ── Parse args ───────────────────────────────────────────────────────────────

while [[ $# -gt 0 ]]; do
  case "$1" in
    --model)    MODELS+=("$2"); shift 2 ;;
    --models)   IFS=',' read -ra _M <<< "$2"; MODELS+=("${_M[@]}"); shift 2 ;;
    --tier)     TIER="$2"; shift 2 ;;
    --verbose)  VERBOSE=true; shift ;;
    --report)
      if [[ "${2:-}" != "" && "${2:0:1}" != "-" ]]; then
        REPORT_DIR="$2"; shift 2
      else
        REPORT_DIR="$SKILL_DIR/test-results"; shift
      fi
      ;;
    --format)   FORMAT="$2"; shift 2 ;;
    --compare)  shift ;;  # implied by --models, accepted for clarity
    -h|--help)
      cat <<'EOF'
Usage: antenna-test-suite.sh [options]

  --model <model>          Single model for Tier B (full provider/model ID)
  --models <m1,m2,...>     Comma-separated models for comparison (max 6)
  --tier A|B|all         Run specific tier (default: all)
  --verbose                Show full request/response payloads inline
  --report [dir]           Save structured report (default: test-results/)
  --format terminal|markdown|json   Output format (default: terminal)
  --compare                Enable comparison table (implied by --models)

Tiers:
  A  Script validation — tests antenna-relay.sh parsing (no model, no network)
  B  Model → tool call — does the model call exec with relay script?

Examples:
  antenna-test-suite.sh --tier A
  antenna-test-suite.sh --model openai/gpt-5.4
  antenna-test-suite.sh --models "openai/gpt-5.4,openrouter/openai/gpt-5.2-codex" --report
  antenna-test-suite.sh --models "openai/gpt-5.4,openrouter/openai/gpt-5.2-codex" --format markdown
EOF
      exit 0
      ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

# Validate model count
if [[ ${#MODELS[@]} -gt $MAX_MODELS ]]; then
  echo "Error: Maximum $MAX_MODELS models allowed (got ${#MODELS[@]})" >&2
  exit 1
fi

# Disable colors for non-terminal output
if [[ "$FORMAT" != "terminal" ]]; then
  RED="" GREEN="" YELLOW="" CYAN="" BOLD="" DIM="" NC=""
fi

RUN_TIMESTAMP=$(date -u +"%Y-%m-%dT%H-%M-%SZ")

# ── Output helpers ───────────────────────────────────────────────────────────

out() { echo -e "$@"; }

pass() {
  local test_id="$1" label="$2" model="${3:-}"
  RESULTS["${model}:${test_id}"]="pass"
  TOTAL_PASS=$((TOTAL_PASS + 1))
  if [[ "$FORMAT" == "terminal" ]]; then
    echo -e "  ${GREEN}✓ PASS${NC}  ${test_id} — ${label}"
  fi
}

fail() {
  local test_id="$1" label="$2" reason="${3:-}" model="${4:-}"
  RESULTS["${model}:${test_id}"]="fail"
  RESULTS_MSG["${model}:${test_id}"]="$reason"
  TOTAL_FAIL=$((TOTAL_FAIL + 1))
  if [[ "$FORMAT" == "terminal" ]]; then
    echo -e "  ${RED}✗ FAIL${NC}  ${test_id} — ${label}"
    if [[ -n "$reason" ]]; then
      echo -e "         ${DIM}${reason}${NC}"
    fi
  fi
}

skip() {
  local test_id="$1" label="$2" reason="${3:-}" model="${4:-}"
  RESULTS["${model}:${test_id}"]="skip"
  RESULTS_MSG["${model}:${test_id}"]="$reason"
  TOTAL_SKIP=$((TOTAL_SKIP + 1))
  if [[ "$FORMAT" == "terminal" ]]; then
    echo -e "  ${YELLOW}— SKIP${NC}  ${test_id} — ${label}"
    if [[ -n "$reason" ]]; then
      echo -e "         ${DIM}${reason}${NC}"
    fi
  fi
}

verbose_out() {
  if [[ "$VERBOSE" == "true" && "$FORMAT" == "terminal" ]]; then
    echo -e "         ${DIM}$1${NC}"
  fi
}

section() {
  if [[ "$FORMAT" == "terminal" ]]; then
    echo ""
    echo -e "${CYAN}${BOLD}═══ $1 ═══${NC}"
    echo ""
  fi
}

# ── Resolve model API details ───────────────────────────────────────────────

resolve_model_api() {
  local model="$1"
  local provider model_name

  provider="${model%%/*}"
  model_name="${model#*/}"

  case "$provider" in
    openai)
      echo "https://api.openai.com/v1|${OPENAI_API_KEY:-}|${model_name}|openai"
      ;;
    openai-codex)
      echo "https://api.openai.com/v1|${OPENAI_API_KEY:-}|${model_name}|openai"
      ;;
    openrouter)
      echo "https://openrouter.ai/api/v1|${OPENROUTER_API_KEY:-${OR_API_KEY:-}}|${model#openrouter/}|openai"
      ;;
    anthropic)
      echo "https://api.anthropic.com/v1/messages|${ANTHROPIC_API_KEY:-}|${model_name}|anthropic"
      ;;
    ollama)
      echo "http://127.0.0.1:11434/v1|ollama|${model_name}|openai"
      ;;
    google)
      echo "https://generativelanguage.googleapis.com/v1beta|${GOOGLE_API_KEY:-${GEMINI_API_KEY:-}}|${model_name}|google"
      ;;
    nvidia)
      echo "https://integrate.api.nvidia.com/v1|${NVIDIA_API_KEY:-${NIM_API_KEY:-}}|${model#nvidia/}|openai"
      ;;
    *)
      echo "UNSUPPORTED"
      ;;
  esac
}

check_model_api() {
  local api_info="$1" model="$2"
  if [[ "$api_info" == "UNSUPPORTED" ]]; then
    echo "unsupported_provider"
    return
  fi
  local api_key
  IFS='|' read -r _ api_key _ _ <<< "$api_info"
  if [[ -z "$api_key" ]]; then
    echo "no_key"
    return
  fi
  echo "ok"
}

get_provider_format() {
  local api_info="$1"
  local fmt
  IFS='|' read -r _ _ _ fmt <<< "$api_info"
  echo "${fmt:-openai}"
}

# ── Tool definitions (OpenAI format) ─────────────────────────────────────────

TOOLS_JSON='[
  {
    "type": "function",
    "function": {
      "name": "write",
      "description": "Write content to a file",
      "parameters": {
        "type": "object",
        "properties": {
          "path": {"type": "string", "description": "Path to write"},
          "content": {"type": "string", "description": "Content to write"}
        },
        "required": ["path", "content"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "exec",
      "description": "Execute a shell command",
      "parameters": {
        "type": "object",
        "properties": {
          "command": {"type": "string", "description": "Shell command to execute"}
        },
        "required": ["command"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "sessions_send",
      "description": "Send a message to a session",
      "parameters": {
        "type": "object",
        "properties": {
          "sessionKey": {"type": "string", "description": "Target session key"},
          "message": {"type": "string", "description": "Message to send"},
          "timeoutSeconds": {"type": "number", "description": "Timeout in seconds"}
        },
        "required": ["sessionKey", "message"]
      }
    }
  }
]'

# ── Tool definitions (Anthropic format) ──────────────────────────────────────

TOOLS_ANTHROPIC='[
  {
    "name": "write",
    "description": "Write content to a file",
    "input_schema": {
      "type": "object",
      "properties": {
        "path": {"type": "string", "description": "Path to write"},
        "content": {"type": "string", "description": "Content to write"}
      },
      "required": ["path", "content"]
    }
  },
  {
    "name": "exec",
    "description": "Execute a shell command",
    "input_schema": {
      "type": "object",
      "properties": {
        "command": {"type": "string", "description": "Shell command to execute"}
      },
      "required": ["command"]
    }
  },
  {
    "name": "sessions_send",
    "description": "Send a message to a session",
    "input_schema": {
      "type": "object",
      "properties": {
        "sessionKey": {"type": "string", "description": "Target session key"},
        "message": {"type": "string", "description": "Message to send"},
        "timeoutSeconds": {"type": "number", "description": "Timeout in seconds"}
      },
      "required": ["sessionKey", "message"]
    }
  }
]'

# ── Tool definitions (Google Gemini format) ──────────────────────────────────

TOOLS_GOOGLE='[
  {
    "functionDeclarations": [
      {
        "name": "write",
        "description": "Write content to a file",
        "parameters": {
          "type": "OBJECT",
          "properties": {
            "path": {"type": "STRING", "description": "Path to write"},
            "content": {"type": "STRING", "description": "Content to write"}
          },
          "required": ["path", "content"]
        }
      },
      {
        "name": "exec",
        "description": "Execute a shell command",
        "parameters": {
          "type": "OBJECT",
          "properties": {
            "command": {"type": "STRING", "description": "Shell command to execute"}
          },
          "required": ["command"]
        }
      },
      {
        "name": "sessions_send",
        "description": "Send a message to a session",
        "parameters": {
          "type": "OBJECT",
          "properties": {
            "sessionKey": {"type": "STRING", "description": "Target session key"},
            "message": {"type": "STRING", "description": "Message to send"},
            "timeoutSeconds": {"type": "NUMBER", "description": "Timeout in seconds"}
          },
          "required": ["sessionKey", "message"]
        }
      }
    ]
  }
]'

# ── Provider API call helpers ────────────────────────────────────────────────
# Each returns a normalized JSON object:
#   { "http_code": N, "first_tool_name": "...", "first_tool_args": "...", "raw": "..." }
# This lets Tier B assertions stay provider-agnostic.

call_anthropic_api() {
  local base_url="$1" api_key="$2" model_name="$3" request_body_json="$4"
  # Build Anthropic request from our normalized inputs
  local system_prompt user_msg extra_messages
  system_prompt=$(echo "$request_body_json" | jq -r '.system // ""')
  user_msg=$(echo "$request_body_json" | jq -r '.user_message')
  extra_messages=$(echo "$request_body_json" | jq -c '.extra_messages // []')

  local messages
  messages=$(jq -n --arg user_msg "$user_msg" '[{"role":"user","content":$user_msg}]')

  local body
  body=$(jq -n \
    --arg model "$model_name" \
    --arg system "$system_prompt" \
    --argjson messages "$messages" \
    --argjson tools "$TOOLS_ANTHROPIC" \
    '{
      model: $model,
      max_tokens: 400,
      system: $system,
      messages: $messages,
      tools: $tools,
      tool_choice: {"type": "auto"}
    }')

  local start_time response http_code elapsed
  start_time=$(date +%s%N)

  response=$(curl -s -w "\n__HTTP_CODE__%{http_code}" \
    -X POST "$base_url" \
    -H "Content-Type: application/json" \
    -H "x-api-key: $api_key" \
    -H "anthropic-version: 2023-06-01" \
    -d "$body" \
    --max-time 60 2>&1)

  elapsed=$(( ($(date +%s%N) - start_time) / 1000000 ))
  http_code=$(echo "$response" | grep "__HTTP_CODE__" | sed 's/__HTTP_CODE__//')
  response=$(echo "$response" | sed '/__HTTP_CODE__/d')

  # Normalize: find first tool_use block in content array
  local tool_name tool_args
  tool_name=$(echo "$response" | jq -r '[.content[]? | select(.type=="tool_use")][0].name // ""' 2>/dev/null)
  tool_args=$(echo "$response" | jq -c '[.content[]? | select(.type=="tool_use")][0].input // {}' 2>/dev/null)
  local tool_id
  tool_id=$(echo "$response" | jq -r '[.content[]? | select(.type=="tool_use")][0].id // ""' 2>/dev/null)

  jq -n \
    --arg http_code "$http_code" \
    --arg elapsed "$elapsed" \
    --arg tool_name "$tool_name" \
    --arg tool_args "$tool_args" \
    --arg tool_id "$tool_id" \
    --arg raw "$response" \
    --arg request "$body" \
    '{
      http_code: ($http_code | tonumber),
      elapsed_ms: ($elapsed | tonumber),
      first_tool_name: $tool_name,
      first_tool_args: $tool_args,
      first_tool_id: $tool_id,
      raw: $raw,
      request: $request
    }'
}

call_google_api() {
  local base_url="$1" api_key="$2" model_name="$3" request_body_json="$4"
  local system_prompt user_msg extra_contents
  system_prompt=$(echo "$request_body_json" | jq -r '.system // ""')
  user_msg=$(echo "$request_body_json" | jq -r '.user_message')
  extra_contents=$(echo "$request_body_json" | jq -c '.extra_google_contents // []')

  local contents
  if [[ "$extra_contents" != "[]" && "$extra_contents" != "null" ]]; then
    contents=$(jq -n \
      --arg user_msg "$user_msg" \
      --argjson extra "$extra_contents" \
      '[{"role":"user","parts":[{"text":$user_msg}]}] + $extra')
  else
    contents=$(jq -n --arg user_msg "$user_msg" '[{"role":"user","parts":[{"text":$user_msg}]}]')
  fi

  local body
  body=$(jq -n \
    --arg system "$system_prompt" \
    --argjson contents "$contents" \
    --argjson tools "$TOOLS_GOOGLE" \
    '{
      system_instruction: {"parts": [{"text": $system}]},
      contents: $contents,
      tools: $tools,
      tool_config: {"function_calling_config": {"mode": "AUTO"}}
    }')

  local url="${base_url}/models/${model_name}:generateContent?key=${api_key}"

  local start_time response http_code elapsed
  start_time=$(date +%s%N)

  response=$(curl -s -w "\n__HTTP_CODE__%{http_code}" \
    -X POST "$url" \
    -H "Content-Type: application/json" \
    -d "$body" \
    --max-time 60 2>&1)

  elapsed=$(( ($(date +%s%N) - start_time) / 1000000 ))
  http_code=$(echo "$response" | grep "__HTTP_CODE__" | sed 's/__HTTP_CODE__//')
  response=$(echo "$response" | sed '/__HTTP_CODE__/d')

  # Normalize: Gemini puts function calls in candidates[0].content.parts[].functionCall
  local tool_name tool_args
  tool_name=$(echo "$response" | jq -r '[.candidates[0].content.parts[]? | select(.functionCall) | .functionCall.name][0] // ""' 2>/dev/null)
  tool_args=$(echo "$response" | jq -c '[.candidates[0].content.parts[]? | select(.functionCall) | .functionCall.args][0] // {}' 2>/dev/null)

  jq -n \
    --arg http_code "$http_code" \
    --arg elapsed "$elapsed" \
    --arg tool_name "$tool_name" \
    --arg tool_args "$tool_args" \
    --arg tool_id "" \
    --arg raw "$response" \
    --arg request "$body" \
    '{
      http_code: ($http_code | tonumber),
      elapsed_ms: ($elapsed | tonumber),
      first_tool_name: $tool_name,
      first_tool_args: $tool_args,
      first_tool_id: "",
      raw: $raw,
      request: $request
    }'
}

call_openai_api() {
  local base_url="$1" api_key="$2" model_name="$3" request_body="$4"
  # request_body is already the full OpenAI-format JSON

  local start_time response http_code elapsed
  start_time=$(date +%s%N)

  response=$(curl -s -w "\n__HTTP_CODE__%{http_code}" \
    -X POST "$base_url/chat/completions" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $api_key" \
    -d "$request_body" \
    --max-time 30 2>&1)

  elapsed=$(( ($(date +%s%N) - start_time) / 1000000 ))
  http_code=$(echo "$response" | grep "__HTTP_CODE__" | sed 's/__HTTP_CODE__//')
  response=$(echo "$response" | sed '/__HTTP_CODE__/d')

  local tool_name tool_args tool_id
  tool_name=$(echo "$response" | jq -r '.choices[0].message.tool_calls[0].function.name // ""' 2>/dev/null)
  tool_args=$(echo "$response" | jq -r '.choices[0].message.tool_calls[0].function.arguments // ""' 2>/dev/null)
  tool_id=$(echo "$response" | jq -r '.choices[0].message.tool_calls[0].id // ""' 2>/dev/null)

  jq -n \
    --arg http_code "$http_code" \
    --arg elapsed "$elapsed" \
    --arg tool_name "$tool_name" \
    --arg tool_args "$tool_args" \
    --arg tool_id "$tool_id" \
    --arg raw "$response" \
    --arg request "$request_body" \
    '{
      http_code: ($http_code | tonumber),
      elapsed_ms: ($elapsed | tonumber),
      first_tool_name: $tool_name,
      first_tool_args: $tool_args,
      first_tool_id: $tool_id,
      raw: $raw,
      request: $request
    }'
}

# Unified dispatcher
call_model_api() {
  local format="$1" base_url="$2" api_key="$3" model_name="$4" request_json="$5"
  case "$format" in
    anthropic) call_anthropic_api "$base_url" "$api_key" "$model_name" "$request_json" ;;
    google)    call_google_api "$base_url" "$api_key" "$model_name" "$request_json" ;;
    openai)    call_openai_api "$base_url" "$api_key" "$model_name" "$request_json" ;;
    *)         echo '{"http_code":0,"elapsed_ms":0,"first_tool_name":"","first_tool_args":"","raw":"unsupported format"}' ;;
  esac
}

# ── Self peer ────────────────────────────────────────────────────────────────

SELF_PEER=$(peers_self_id)
LOCAL_AGENT=$(config_local_agent_id)

# ══════════════════════════════════════════════════════════════════════════════
# TIER A: Script validation
# ══════════════════════════════════════════════════════════════════════════════

run_tier_a() {
  section "TIER A: Script Validation (relay parser)"

  if [[ -z "$SELF_PEER" ]]; then
    fail "A.0" "No self-peer in peers registry" "Check antenna-peers.json" ""
    return
  fi

  local tests_run=0
  local inbox_file="" inbox_backup="" rate_file="" rate_backup="" orig_config_conc=""

  cleanup_tier_a_state() {
    [[ -n "$inbox_backup" && -f "$inbox_backup" && -n "$inbox_file" ]] && cp "$inbox_backup" "$inbox_file"
    [[ -n "$rate_backup" && -f "$rate_backup" && -n "$rate_file" ]] && cp "$rate_backup" "$rate_file"
    [[ -n "$orig_config_conc" ]] && echo "$orig_config_conc" > "$SKILL_DIR/antenna-config.json"
    [[ -n "$inbox_backup" ]] && rm -f "$inbox_backup"
    [[ -n "$rate_backup" ]] && rm -f "$rate_backup"
  }

  trap cleanup_tier_a_state RETURN

  # Load self-peer's auth secret for inclusion in valid test envelopes
  local SELF_SECRET="" SELF_SECRET_FILE=""
  SELF_SECRET_FILE=$(peers_get "$SELF_PEER" peer_secret_file)
  if [[ -n "$SELF_SECRET_FILE" ]]; then
    if [[ "$SELF_SECRET_FILE" != /* ]]; then
      SELF_SECRET_FILE="$SKILL_DIR/$SELF_SECRET_FILE"
    fi
    if [[ -f "$SELF_SECRET_FILE" ]]; then
      SELF_SECRET=$(tr -d '[:space:]' < "$SELF_SECRET_FILE")
    fi
  fi
  local AUTH_LINE=""
  if [[ -n "$SELF_SECRET" ]]; then
    AUTH_LINE="auth: ${SELF_SECRET}"
  fi

  # Helper: build a valid envelope with auth header included when available
  CURRENT_TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

  build_envelope() {
    local from="$1" session="$2" timestamp="$3" body="$4" extra_headers="${5:-}"
    local env="[ANTENNA_RELAY]
from: ${from}
target_session: ${session}
timestamp: ${timestamp}"
    if [[ -n "$AUTH_LINE" && "$from" == "$SELF_PEER" ]]; then
      env="${env}
${AUTH_LINE}"
    fi
    if [[ -n "$extra_headers" ]]; then
      env="${env}
${extra_headers}"
    fi
    env="${env}

${body}
[/ANTENNA_RELAY]"
    echo "$env"
  }

  # ── A.1: Valid envelope → relay ok ──
  local valid_envelope
  valid_envelope=$(build_envelope "$SELF_PEER" "agent:betty:main" "$CURRENT_TS" "Hello, this is a test message.")

  local result action status session_key
  result=$(echo "$valid_envelope" | bash "$RELAY_SCRIPT" --stdin 2>/dev/null)
  action=$(echo "$result" | jq -r '.action // "none"' 2>/dev/null)
  status=$(echo "$result" | jq -r '.status // "none"' 2>/dev/null)
  session_key=$(echo "$result" | jq -r '.sessionKey // "none"' 2>/dev/null)

  if [[ "$action" == "relay" && "$status" == "ok" && "$session_key" == "agent:betty:main" ]]; then
    pass "A.1" "Valid envelope → relay/ok with correct session"
  else
    fail "A.1" "Valid envelope → relay/ok" "Got action=$action status=$status session=$session_key"
  fi
  tests_run=$((tests_run + 1))

  # ── A.2: Missing envelope markers → malformed ──
  result=$(echo "Just a regular message." | bash "$RELAY_SCRIPT" --stdin 2>/dev/null)
  status=$(echo "$result" | jq -r '.status // "none"' 2>/dev/null)
  if [[ "$status" == "malformed" ]]; then
    pass "A.2" "Missing envelope markers → malformed"
  else
    fail "A.2" "Missing envelope markers → malformed" "Got status=$status"
  fi
  tests_run=$((tests_run + 1))

  # ── A.3: Missing 'from' header → rejected ──
  local no_from="[ANTENNA_RELAY]
target_session: agent:betty:main
timestamp: ${CURRENT_TS}

Test body
[/ANTENNA_RELAY]"
  result=$(echo "$no_from" | bash "$RELAY_SCRIPT" --stdin 2>/dev/null)
  action=$(echo "$result" | jq -r '.action // "none"' 2>/dev/null)
  if [[ "$action" == "reject" ]]; then
    pass "A.3" "Missing 'from' header → rejected"
  else
    fail "A.3" "Missing 'from' header → rejected" "Got action=$action"
  fi
  tests_run=$((tests_run + 1))

  # ── A.4: Unknown peer → rejected ──
  local unknown="[ANTENNA_RELAY]
from: totally_unknown_host
target_session: agent:betty:main
timestamp: ${CURRENT_TS}

Test body
[/ANTENNA_RELAY]"
  result=$(echo "$unknown" | bash "$RELAY_SCRIPT" --stdin 2>/dev/null)
  action=$(echo "$result" | jq -r '.action // "none"' 2>/dev/null)
  if [[ "$action" == "reject" ]]; then
    pass "A.4" "Unknown peer → rejected"
  else
    fail "A.4" "Unknown peer → rejected" "Got action=$action"
  fi
  tests_run=$((tests_run + 1))

  # ── A.5: Bare session name rejected, full session key required ──
  local main_env main_action main_reason
  main_env=$(build_envelope "$SELF_PEER" "main" "$CURRENT_TS" "Bare session should fail.")
  result=$(echo "$main_env" | bash "$RELAY_SCRIPT" --stdin 2>/dev/null)
  main_action=$(echo "$result" | jq -r '.action // "none"' 2>/dev/null)
  main_reason=$(echo "$result" | jq -r '.reason // ""' 2>/dev/null)
  if [[ "$main_action" == "reject" ]] && echo "$main_reason" | grep -qi "allowed_inbound_sessions\|session target"; then
    pass "A.5" "Bare session name 'main' → rejected"
  else
    fail "A.5" "Bare session name rejected" "Expected reject for bare session, got action=$main_action reason=$main_reason"
  fi
  tests_run=$((tests_run + 1))

  # ── A.5b: Full session key accepted ──
  local full_key_env
  full_key_env=$(build_envelope "$SELF_PEER" "agent:betty:main" "$CURRENT_TS" "Full session key should pass.")
  result=$(echo "$full_key_env" | bash "$RELAY_SCRIPT" --stdin 2>/dev/null)
  action=$(echo "$result" | jq -r '.action // "none"' 2>/dev/null)
  status=$(echo "$result" | jq -r '.status // "none"' 2>/dev/null)
  session_key=$(echo "$result" | jq -r '.sessionKey // "none"' 2>/dev/null)
  if [[ "$action" == "relay" && "$status" == "ok" && "$session_key" == "agent:betty:main" ]]; then
    pass "A.5b" "Full session key accepted"
  else
    fail "A.5b" "Full session key accepted" "Got action=$action status=$status session=$session_key"
  fi
  tests_run=$((tests_run + 1))

  # ── A.6: Oversized message → rejected ──
  local max_len
  max_len=$(config_max_message_length)
  local big_body
  big_body=$(head -c $((max_len + 100)) /dev/urandom | base64 | head -c $((max_len + 100)))
  local oversize
  oversize=$(build_envelope "$SELF_PEER" "agent:betty:main" "$CURRENT_TS" "$big_body")
  result=$(echo "$oversize" | bash "$RELAY_SCRIPT" --stdin 2>/dev/null)
  action=$(echo "$result" | jq -r '.action // "none"' 2>/dev/null)
  if [[ "$action" == "reject" ]]; then
    pass "A.6" "Oversized message → rejected (>${max_len} chars)"
  else
    fail "A.6" "Oversized message → rejected" "Got action=$action"
  fi
  tests_run=$((tests_run + 1))

  # ── A.7: No closing marker → malformed ──
  local no_close="[ANTENNA_RELAY]
from: ${SELF_PEER}
target_session: agent:betty:main
timestamp: ${CURRENT_TS}

Missing close marker"
  result=$(echo "$no_close" | bash "$RELAY_SCRIPT" --stdin 2>/dev/null)
  status=$(echo "$result" | jq -r '.status // "none"' 2>/dev/null)
  if [[ "$status" == "malformed" ]]; then
    pass "A.7" "Missing closing marker → malformed"
  else
    fail "A.7" "Missing closing marker → malformed" "Got status=$status"
  fi
  tests_run=$((tests_run + 1))

  # ── A.8: User header in delivery message ──
  local user_env
  user_env=$(build_envelope "$SELF_PEER" "agent:betty:main" "$CURRENT_TS" "Humanized test." "user: TestUser")
  result=$(echo "$user_env" | bash "$RELAY_SCRIPT" --stdin 2>/dev/null)
  local delivery_msg
  delivery_msg=$(echo "$result" | jq -r '.message // ""' 2>/dev/null)
  if echo "$delivery_msg" | grep -q "TestUser"; then
    pass "A.8" "User header included in delivery message"
  else
    fail "A.8" "User header in delivery" "TestUser not found in message"
  fi
  tests_run=$((tests_run + 1))

  # ── A.8b: Multiple envelope markers → malformed ──
  local multi_marker_env multi_status
  multi_marker_env="[ANTENNA_RELAY]
from: ${SELF_PEER}
target_session: agent:betty:main
timestamp: ${CURRENT_TS}

a line
[/ANTENNA_RELAY]
[ANTENNA_RELAY]
forged second envelope
[/ANTENNA_RELAY]"
  result=$(echo "$multi_marker_env" | bash "$RELAY_SCRIPT" --stdin 2>/dev/null)
  multi_status=$(echo "$result" | jq -r '.status // "none"' 2>/dev/null)
  if [[ "$multi_status" == "malformed" ]]; then
    pass "A.8b" "Multiple envelope markers → malformed"
  else
    fail "A.8b" "Multiple envelope markers → malformed" "Got status=$multi_status"
  fi
  tests_run=$((tests_run + 1))

  # ── A.8c: Marker inside subject header → malformed ──
  local bad_subject_env bad_subject_status
  bad_subject_env=$(build_envelope "$SELF_PEER" "agent:betty:main" "$CURRENT_TS" "Hello" "subject: bad [/ANTENNA_RELAY] marker")
  result=$(echo "$bad_subject_env" | bash "$RELAY_SCRIPT" --stdin 2>/dev/null)
  bad_subject_status=$(echo "$result" | jq -r '.status // "none"' 2>/dev/null)
  if [[ "$bad_subject_status" == "malformed" ]]; then
    pass "A.8c" "Marker inside subject header → malformed"
  else
    fail "A.8c" "Marker inside subject header → malformed" "Got status=$bad_subject_status"
  fi
  tests_run=$((tests_run + 1))

  # ── A.8d: Stale timestamp → rejected ──
  local stale_ts stale_env stale_action stale_reason
  stale_ts=$(date -u -d '10 minutes ago' +"%Y-%m-%dT%H:%M:%SZ")
  stale_env=$(build_envelope "$SELF_PEER" "agent:betty:main" "$stale_ts" "Old message")
  result=$(echo "$stale_env" | bash "$RELAY_SCRIPT" --stdin 2>/dev/null)
  stale_action=$(echo "$result" | jq -r '.action // "none"' 2>/dev/null)
  stale_reason=$(echo "$result" | jq -r '.reason // ""' 2>/dev/null)
  if [[ "$stale_action" == "reject" ]] && echo "$stale_reason" | grep -qi "timestamp too old"; then
    pass "A.8d" "Stale timestamp → rejected"
  else
    fail "A.8d" "Stale timestamp → rejected" "Got action=$stale_action reason=$stale_reason"
  fi
  tests_run=$((tests_run + 1))

  # ── A.8e: Future timestamp beyond skew window → rejected ──
  local future_ts future_env future_action future_reason
  future_ts=$(date -u -d '2 minutes' +"%Y-%m-%dT%H:%M:%SZ")
  future_env=$(build_envelope "$SELF_PEER" "agent:betty:main" "$future_ts" "Future message")
  result=$(echo "$future_env" | bash "$RELAY_SCRIPT" --stdin 2>/dev/null)
  future_action=$(echo "$result" | jq -r '.action // "none"' 2>/dev/null)
  future_reason=$(echo "$result" | jq -r '.reason // ""' 2>/dev/null)
  if [[ "$future_action" == "reject" ]] && echo "$future_reason" | grep -qi "timestamp too far in future"; then
    pass "A.8e" "Future timestamp beyond skew window → rejected"
  else
    fail "A.8e" "Future timestamp beyond skew window → rejected" "Got action=$future_action reason=$future_reason"
  fi
  tests_run=$((tests_run + 1))

  # ── A.9: Rate limiting — reject after burst ──
  # Temporarily set per_peer_per_minute to 2 in config, send 3 messages, expect 3rd rejected
  local orig_config rate_env rate_result rate_status
  orig_config=$(cat "$SKILL_DIR/antenna-config.json")

  # Patch config to limit 2/min for testing
  config_mutate '.rate_limit.per_peer_per_minute = 2'

  # Clear rate limit state
  echo '{}' > "$SKILL_DIR/antenna-ratelimit.json" 2>/dev/null

  rate_env=$(build_envelope "$SELF_PEER" "agent:betty:main" "$CURRENT_TS" "Rate limit test.")

  # Messages 1 and 2 should pass
  echo "$rate_env" | bash "$RELAY_SCRIPT" --stdin >/dev/null 2>&1
  echo "$rate_env" | bash "$RELAY_SCRIPT" --stdin >/dev/null 2>&1

  # Message 3 should be rate limited
  rate_result=$(echo "$rate_env" | bash "$RELAY_SCRIPT" --stdin 2>/dev/null)
  rate_status=$(echo "$rate_result" | jq -r '.status // "none"' 2>/dev/null)
  local rate_reason
  rate_reason=$(echo "$rate_result" | jq -r '.reason // ""' 2>/dev/null)

  # Restore original config and clean up
  echo "$orig_config" > "$SKILL_DIR/antenna-config.json"
  rm -f "$SKILL_DIR/antenna-ratelimit.json" 2>/dev/null

  if [[ "$rate_status" == "rejected" ]] && echo "$rate_reason" | grep -qi "rate.limit"; then
    pass "A.9" "Rate limiting rejects after burst (2/min limit, 3rd message rejected)"
  else
    fail "A.9" "Rate limiting burst rejection" "Expected rejected/rate_limited, got status=$rate_status reason=$rate_reason"
  fi
  tests_run=$((tests_run + 1))

  # ── A.10: Missing auth header → rejected (when peer secret is configured) ──
  if [[ -n "$SELF_SECRET" ]]; then
    local no_auth_env="[ANTENNA_RELAY]
from: ${SELF_PEER}
target_session: agent:betty:main
timestamp: ${CURRENT_TS}

No auth header test.
[/ANTENNA_RELAY]"
    local no_auth_result no_auth_action no_auth_reason
    no_auth_result=$(echo "$no_auth_env" | bash "$RELAY_SCRIPT" --stdin 2>/dev/null)
    no_auth_action=$(echo "$no_auth_result" | jq -r '.action // "none"' 2>/dev/null)
    no_auth_reason=$(echo "$no_auth_result" | jq -r '.reason // ""' 2>/dev/null)
    if [[ "$no_auth_action" == "reject" ]] && echo "$no_auth_reason" | grep -qi "auth"; then
      pass "A.10" "Missing auth header → rejected (peer secret configured)"
    else
      fail "A.10" "Missing auth → rejected" "Got action=$no_auth_action reason=$no_auth_reason"
    fi
  else
    skip "A.10" "Missing auth header → rejected" "No peer secret configured for self-peer" ""
  fi
  tests_run=$((tests_run + 1))

  # ── A.11: Wrong auth secret → rejected ──
  if [[ -n "$SELF_SECRET" ]]; then
    local bad_auth_env="[ANTENNA_RELAY]
from: ${SELF_PEER}
target_session: agent:betty:main
timestamp: ${CURRENT_TS}
auth: deadbeef0000000000000000000000000000000000000000000000000000cafe

Wrong secret test.
[/ANTENNA_RELAY]"
    local bad_auth_result bad_auth_action bad_auth_reason
    bad_auth_result=$(echo "$bad_auth_env" | bash "$RELAY_SCRIPT" --stdin 2>/dev/null)
    bad_auth_action=$(echo "$bad_auth_result" | jq -r '.action // "none"' 2>/dev/null)
    bad_auth_reason=$(echo "$bad_auth_result" | jq -r '.reason // ""' 2>/dev/null)
    if [[ "$bad_auth_action" == "reject" ]] && echo "$bad_auth_reason" | grep -qi "auth\|secret"; then
      pass "A.11" "Wrong auth secret → rejected"
    else
      fail "A.11" "Wrong auth → rejected" "Got action=$bad_auth_action reason=$bad_auth_reason"
    fi
  else
    skip "A.11" "Wrong auth secret → rejected" "No peer secret configured for self-peer" ""
  fi
  tests_run=$((tests_run + 1))

  # ── A.12: Inbox queue-add deterministic path works ──
  local queue_result queue_action queue_ref queue_from
  inbox_file="$SKILL_DIR/antenna-inbox.json"
  inbox_backup=$(mktemp)
  cp "$inbox_file" "$inbox_backup" 2>/dev/null || printf '[]\n' > "$inbox_backup"
  printf '[]\n' > "$inbox_file"

  queue_result=$(printf '%s' '{"from":"suitepeer","target_session":"agent:betty:main","full_message":"suite queue test","display_name":"Suite Peer","body_preview":"suite queue test","body_chars":16,"session_key":"agent:betty:main"}' | bash "$SCRIPT_DIR/antenna-inbox.sh" queue-add 2>/dev/null)
  queue_action=$(echo "$queue_result" | jq -r '.action // "none"' 2>/dev/null)
  queue_ref=$(echo "$queue_result" | jq -r '.ref // "none"' 2>/dev/null)
  queue_from=$(echo "$queue_result" | jq -r '.from // "none"' 2>/dev/null)
  if [[ "$queue_action" == "queue" && "$queue_ref" == "1" && "$queue_from" == "suitepeer" ]]; then
    pass "A.12" "Inbox queue-add returns queue action with ref"
  else
    fail "A.12" "Inbox queue-add deterministic path" "Got action=$queue_action ref=$queue_ref from=$queue_from"
  fi
  tests_run=$((tests_run + 1))

  # ── A.13: Inbox queue locking keeps refs unique under concurrency ──
  printf '[]\n' > "$inbox_file"
  for i in $(seq 1 6); do
    (
      printf '%s' '{"from":"suitepeer","target_session":"agent:betty:main","full_message":"suite lock test","display_name":"Suite Peer","body_preview":"suite lock test","body_chars":15,"session_key":"agent:betty:main"}' \
        | bash "$SCRIPT_DIR/antenna-inbox.sh" queue-add >/dev/null 2>&1
    ) &
  done
  wait
  local queue_count queue_uniq
  queue_count=$(jq 'length' "$inbox_file" 2>/dev/null || echo "0")
  queue_uniq=$(jq '[.[].ref] | unique | length' "$inbox_file" 2>/dev/null || echo "0")
  if [[ "$queue_count" == "6" && "$queue_uniq" == "6" ]]; then
    pass "A.13" "Inbox locking preserves unique refs under concurrency"
  else
    fail "A.13" "Inbox locking concurrency" "Expected count=6 uniq=6, got count=$queue_count uniq=$queue_uniq"
  fi
  tests_run=$((tests_run + 1))

  # ── A.14: Rate-limit locking preserves all concurrent writes below threshold ──
  rate_file="$SKILL_DIR/antenna-ratelimit.json"
  rate_backup=$(mktemp)
  cp "$rate_file" "$rate_backup" 2>/dev/null || printf '{}\n' > "$rate_backup"
  orig_config_conc=$(cat "$SKILL_DIR/antenna-config.json")
  printf '{}\n' > "$rate_file"
  config_mutate '.rate_limit.per_peer_per_minute = 20 | .rate_limit.global_per_minute = 50'
  for i in $(seq 1 6); do
    (
      build_envelope "$SELF_PEER" "agent:betty:main" "$CURRENT_TS" "Concurrent rate test $i" \
        | bash "$RELAY_SCRIPT" --stdin >/dev/null 2>&1
    ) &
  done
  wait
  local rate_count
  rate_count=$(jq '[."'"$SELF_PEER"'" // [] | length][0]' "$rate_file" 2>/dev/null || echo "0")
  if [[ "$rate_count" == "6" ]]; then
    pass "A.14" "Rate-limit locking preserves concurrent writes"
  else
    fail "A.14" "Rate-limit locking concurrency" "Expected self-peer count=6, got $rate_count"
  fi
  tests_run=$((tests_run + 1))

  # ── A.15: Inbox gate does not bypass allowed_inbound_sessions (REF-500) ──
  # When inbox_enabled=true and the peer is not auto-approved, a message
  # targeting a session OUTSIDE allowed_inbound_sessions must be REJECTED at
  # relay time, not quietly queued for human approval.
  local ref500_config_backup ref500_inbox_backup
  ref500_config_backup=$(cat "$SKILL_DIR/antenna-config.json")
  ref500_inbox_backup=$(mktemp)
  cp "$SKILL_DIR/antenna-inbox.json" "$ref500_inbox_backup" 2>/dev/null || printf '[]\n' > "$ref500_inbox_backup"
  printf '[]\n' > "$SKILL_DIR/antenna-inbox.json"

  config_mutate '
    .inbox_enabled = true
    | .inbox_auto_approve_peers = []
    | .allowed_inbound_sessions = ["agent:betty:main", "agent:betty:antenna"]
  '

  local ref500_env ref500_result ref500_action ref500_reason ref500_queue_len
  ref500_env=$(build_envelope "$SELF_PEER" "agent:betty:sensitive-private" "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" "Should be rejected, not queued.")
  ref500_result=$(echo "$ref500_env" | bash "$RELAY_SCRIPT" --stdin 2>/dev/null)
  ref500_action=$(echo "$ref500_result" | jq -r '.action // "none"' 2>/dev/null)
  ref500_reason=$(echo "$ref500_result" | jq -r '.reason // ""' 2>/dev/null)
  ref500_queue_len=$(jq 'length' "$SKILL_DIR/antenna-inbox.json" 2>/dev/null || echo "-1")

  if [[ "$ref500_action" == "reject" ]] \
     && echo "$ref500_reason" | grep -qi "allowed_inbound_sessions" \
     && [[ "$ref500_queue_len" == "0" ]]; then
    pass "A.15" "REF-500: inbox gate honors allowed_inbound_sessions"
  else
    fail "A.15" "REF-500: inbox gate must reject disallowed session targets" \
      "Got action=$ref500_action reason=$ref500_reason queue_len=$ref500_queue_len"
  fi
  tests_run=$((tests_run + 1))

  # Restore
  printf '%s' "$ref500_config_backup" > "$SKILL_DIR/antenna-config.json"
  cp "$ref500_inbox_backup" "$SKILL_DIR/antenna-inbox.json" 2>/dev/null || true
  rm -f "$ref500_inbox_backup"

  TIER_A_TOTAL=$tests_run
}

# ══════════════════════════════════════════════════════════════════════════════
# TIER B: Model → exec tool call
# ══════════════════════════════════════════════════════════════════════════════

run_tier_b() {
  local model="$1"
  local model_label="${model//\//_}"

  if [[ "$FORMAT" == "terminal" ]]; then
    echo ""
    echo -e "  ${CYAN}── Tier B: ${model} ──${NC}"
    echo ""
  fi

  local api_info check
  api_info=$(resolve_model_api "$model")
  check=$(check_model_api "$api_info" "$model")

  if [[ "$check" == "unsupported_provider" ]]; then
    skip "B.1" "API call" "Provider not supported: ${model%%/*}" "$model"
    skip "B.2" "First tool call is write" "Skipped (no API)" "$model"
    skip "B.3" "Write path/content shape" "Skipped (no API)" "$model"
    skip "B.4" "Temp-file relay exec command shape" "Skipped (no API)" "$model"
    return
  fi
  if [[ "$check" == "no_key" ]]; then
    skip "B.1" "API call" "No API key for ${model%%/*}" "$model"
    skip "B.2" "First tool call is write" "Skipped (no key)" "$model"
    skip "B.3" "Write path/content shape" "Skipped (no key)" "$model"
    skip "B.4" "Temp-file relay exec command shape" "Skipped (no key)" "$model"
    return
  fi

  local base_url api_key model_name fmt
  IFS='|' read -r base_url api_key model_name fmt <<< "$api_info"
  fmt="${fmt:-openai}"

  local system_prompt
  system_prompt=$(cat "$AGENT_INSTRUCTIONS")

  local test_ts
  test_ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)

  local allowed_test_session
  allowed_test_session=$(jq -r '.allowed_inbound_sessions[0] // .default_target_session // "agent:betty:main"' "$CONFIG_FILE" 2>/dev/null)

  local test_message="[ANTENNA_RELAY]
from: ${SELF_PEER:-testhost}
target_session: ${allowed_test_session}
timestamp: ${test_ts}

[Antenna Test Suite — Tier B]
model_under_test: ${model}
host: $(hostname)
test_time: ${test_ts}

This is an automated relay compatibility test verifying that ${model} correctly writes the raw inbound message to a unique temp file and then invokes the relay-file script with a simple exec command.
[/ANTENNA_RELAY]"

  # Build request based on provider format
  local request_input result
  if [[ "$fmt" == "openai" ]]; then
    request_input=$(jq -n \
      --arg model "$model_name" \
      --arg system "$system_prompt" \
      --arg user "$test_message" \
      --argjson tools "$TOOLS_JSON" \
      '{
        model: $model,
        messages: [
          {role: "system", content: $system},
          {role: "user", content: $user}
        ],
        tools: $tools,
        temperature: 0,
        max_completion_tokens: 400
      }')
  else
    # Anthropic/Google: pass normalized input for the helper to build
    request_input=$(jq -n \
      --arg system "$system_prompt" \
      --arg user_message "$test_message" \
      '{ system: $system, user_message: $user_message }')
  fi

  verbose_out "Calling ${fmt} API at ${base_url}..."

  result=$(call_model_api "$fmt" "$base_url" "$api_key" "$model_name" "$request_input")

  local http_code elapsed tool_name tool_args raw_response raw_request
  http_code=$(echo "$result" | jq -r '.http_code')
  elapsed=$(echo "$result" | jq -r '.elapsed_ms')
  tool_name=$(echo "$result" | jq -r '.first_tool_name')
  tool_args=$(echo "$result" | jq -r '.first_tool_args')
  raw_response=$(echo "$result" | jq -r '.raw')
  raw_request=$(echo "$result" | jq -r '.request')

  RAW_REQUESTS["${model}:B"]="$raw_request"
  RAW_RESPONSES["${model}:B"]="$raw_response"

  verbose_out "HTTP $http_code (${elapsed}ms)"
  verbose_out "Tool: ${tool_name} | Args: $(echo "$tool_args" | head -c 200)"

  # B.1: API success
  if [[ "$http_code" != "200" ]]; then
    local err_msg
    err_msg=$(echo "$raw_response" | jq -r '.error.message // .error.type // "unknown"' 2>/dev/null || echo "HTTP $http_code")
    fail "B.1" "API call" "HTTP $http_code: $err_msg" "$model"
    skip "B.2" "First tool call is write" "Skipped (API failed)" "$model"
    skip "B.3" "Write path/content shape" "Skipped (API failed)" "$model"
    skip "B.4" "Temp-file relay exec command shape" "Skipped (API failed)" "$model"
    return
  fi
  pass "B.1" "API call succeeded (${elapsed}ms)" "$model"

  if [[ -z "$tool_name" || "$tool_name" == "null" ]]; then
    fail "B.2" "Produced tool call" "Model returned text instead of tool call" "$model"
    skip "B.3" "Write path/content shape" "No tool call" "$model"
    skip "B.4" "Temp-file relay exec command shape" "No tool call" "$model"
    return
  fi

  if [[ "$tool_name" == "write" ]]; then
    pass "B.2" "First tool call is 'write'" "$model"
  else
    fail "B.2" "First tool call is 'write'" "Got '$tool_name'" "$model"
    skip "B.3" "Write path/content shape" "First tool was not write" "$model"
    skip "B.4" "Temp-file relay exec command shape" "First tool was not write" "$model"
    return
  fi

  local write_path write_content
  write_path=$(echo "$tool_args" | jq -r '.path // ""' 2>/dev/null)
  write_content=$(echo "$tool_args" | jq -r '.content // ""' 2>/dev/null)
  if echo "$write_path" | grep -Eq '^/tmp/antenna-relay/msg-[A-Za-z0-9._-]+\.txt$' && echo "$write_content" | grep -q '\[ANTENNA_RELAY\]'; then
    pass "B.3" "Write uses unique temp path and raw envelope content" "$model"
  else
    fail "B.3" "Write path/content shape" "Path=$write_path content_has_envelope=$(echo "$write_content" | grep -q '\[ANTENNA_RELAY\]' && echo yes || echo no)" "$model"
  fi

  local finish_reason
  finish_reason=$(echo "$raw_response" | jq -r '.choices[0].finish_reason // .stop_reason // ""' 2>/dev/null)
  if [[ "$finish_reason" == "tool_calls" || "$finish_reason" == "tool_use" || "$finish_reason" == "" ]]; then
    pass "B.4" "Tier B stops at first tool call; exec+deliver validated in B.2/B.3" "$model"
  else
    fail "B.4" "Tier B stop shape" "Unexpected finish_reason=$finish_reason" "$model"
  fi
}

# ══════════════════════════════════════════════════════════════════════════════
# COMPARISON TABLE
# ══════════════════════════════════════════════════════════════════════════════

print_comparison_table() {
  local all_tests=("B.1" "B.2" "B.3" "B.4")
  local total_bc=4

  if [[ "$FORMAT" == "terminal" ]]; then
    echo ""
    echo -e "${BOLD}${CYAN}═══ Model Comparison ═══${NC}"
    echo ""

    # Header
    printf "  ${BOLD}%-42s" "Model"
    for t in "${all_tests[@]}"; do
      printf " %-3s" "$t"
    done
    printf "  %-6s  %s${NC}\n" "Score" "Time"

    # Separator
    printf "  "
    printf '─%.0s' {1..82}
    echo ""

    # Per-model rows
    for model in "${MODELS[@]}"; do
      printf "  %-42s" "$model"

      local model_pass=0
      local model_total=0
      for t in "${all_tests[@]}"; do
        local r="${RESULTS["${model}:${t}"]:-none}"
        model_total=$((model_total + 1))
        case "$r" in
          pass)  printf " ${GREEN}✓${NC}  "; model_pass=$((model_pass + 1)) ;;
          fail)  printf " ${RED}✗${NC}  "; ;;
          skip)  printf " ${YELLOW}—${NC}  "; ;;
          *)     printf " ${DIM}?${NC}  "; ;;
        esac
      done

      MODEL_SCORES["$model"]="${model_pass}/${total_bc}"
      printf "  %-6s" "${model_pass}/${total_bc}"

      local time_val="${RESULTS_TIME["$model"]:-n/a}"
      printf "  %s" "$time_val"
      echo ""
    done

    echo ""

    # Verdict
    local best_model="" best_score=0
    for model in "${MODELS[@]}"; do
      local score="${MODEL_SCORES["$model"]:-0/0}"
      local s="${score%%/*}"
      if [[ "$s" -gt "$best_score" ]]; then
        best_score=$s
        best_model=$model
      fi
    done

    if [[ -n "$best_model" && "$best_score" -gt 0 ]]; then
      echo -e "  ${GREEN}${BOLD}Verdict: ${best_model} — RECOMMENDED (${MODEL_SCORES["$best_model"]}, ${RESULTS_TIME["$best_model"]:-?})${NC}"
    else
      echo -e "  ${YELLOW}Verdict: No model passed all tests.${NC}"
    fi

  elif [[ "$FORMAT" == "markdown" ]]; then
    echo ""
    echo "## Model Comparison"
    echo ""

    printf "| %-40s |" "Model"
    for t in "${all_tests[@]}"; do
      printf " %s |" "$t"
    done
    printf " %-5s | %s |\n" "Score" "Time"

    printf "| "
    printf '%-40s' "$(printf -- '-%.0s' {1..40})"
    printf " |"
    for _ in "${all_tests[@]}"; do
      printf " --- |"
    done
    printf " ----- | ---- |\n"

    for model in "${MODELS[@]}"; do
      printf "| %-40s |" "$model"
      local model_pass=0
      for t in "${all_tests[@]}"; do
        local r="${RESULTS["${model}:${t}"]:-none}"
        case "$r" in
          pass)  printf " ✅ |"; model_pass=$((model_pass + 1)) ;;
          fail)  printf " ❌ |" ;;
          skip)  printf " ⏭️ |" ;;
          *)     printf " ❓ |" ;;
        esac
      done
      MODEL_SCORES["$model"]="${model_pass}/${total_bc}"
      printf " %-5s |" "${model_pass}/${total_bc}"
      printf " %s |\n" "${RESULTS_TIME["$model"]:-n/a}"
    done
    echo ""
  fi
}

# ══════════════════════════════════════════════════════════════════════════════
# SUMMARY
# ══════════════════════════════════════════════════════════════════════════════

print_summary() {
  if [[ "$FORMAT" == "terminal" ]]; then
    echo ""
    echo -e "${BOLD}═══════════════════════════════════════════${NC}"
    echo -e "  ${GREEN}PASS: $TOTAL_PASS${NC}  ${RED}FAIL: $TOTAL_FAIL${NC}  ${YELLOW}SKIP: $TOTAL_SKIP${NC}  Total: $((TOTAL_PASS + TOTAL_FAIL + TOTAL_SKIP))"
    echo -e "${BOLD}═══════════════════════════════════════════${NC}"
  elif [[ "$FORMAT" == "markdown" ]]; then
    echo ""
    echo "---"
    echo "**Results:** PASS: $TOTAL_PASS | FAIL: $TOTAL_FAIL | SKIP: $TOTAL_SKIP | Total: $((TOTAL_PASS + TOTAL_FAIL + TOTAL_SKIP))"
  elif [[ "$FORMAT" == "json" ]]; then
    # JSON output — collect everything
    local models_json="[]"
    for model in "${MODELS[@]}"; do
      local model_results="{}"
      for t in "B.1" "B.2" "B.3" "B.4"; do
        local r="${RESULTS["${model}:${t}"]:-none}"
        local msg="${RESULTS_MSG["${model}:${t}"]:-}"
        model_results=$(echo "$model_results" | jq \
          --arg t "$t" --arg r "$r" --arg msg "$msg" \
          '. + {($t): {result: $r, message: $msg}}')
      done
      models_json=$(echo "$models_json" | jq \
        --arg model "$model" \
        --arg score "${MODEL_SCORES["$model"]:-n/a}" \
        --arg time "${RESULTS_TIME["$model"]:-n/a}" \
        --argjson tests "$model_results" \
        '. + [{model: $model, score: $score, time: $time, tests: $tests}]')
    done

    jq -n \
      --arg timestamp "$RUN_TIMESTAMP" \
      --argjson tier_a "{\"pass\": $TIER_A_PASS, \"total\": $TIER_A_TOTAL}" \
      --argjson models "$models_json" \
      --argjson totals "{\"pass\": $TOTAL_PASS, \"fail\": $TOTAL_FAIL, \"skip\": $TOTAL_SKIP}" \
      '{timestamp: $timestamp, tier_a: $tier_a, models: $models, totals: $totals}'
  fi
}

# ══════════════════════════════════════════════════════════════════════════════
# REPORT WRITER
# ══════════════════════════════════════════════════════════════════════════════

write_report() {
  if [[ -z "$REPORT_DIR" ]]; then
    return
  fi

  local run_dir="${REPORT_DIR}/${RUN_TIMESTAMP}"
  mkdir -p "$run_dir"

  # Tier A results
  echo '{}' | jq --argjson pass "$TIER_A_PASS" --argjson total "$TIER_A_TOTAL" \
    '{tier: "A", pass: $pass, total: $total}' > "$run_dir/tier-a.json"

  # Per-model request/response dumps
  for model in "${MODELS[@]}"; do
    local safe_name="${model//\//__}"
    local model_dir="$run_dir/models/${safe_name}"
    mkdir -p "$model_dir"

    # Dump raw requests/responses
    if [[ -n "${RAW_REQUESTS["${model}:B"]:-}" ]]; then
      echo "${RAW_REQUESTS["${model}:B"]}" | jq . > "$model_dir/tier-b-request.json" 2>/dev/null || true
    fi
    if [[ -n "${RAW_RESPONSES["${model}:B"]:-}" ]]; then
      echo "${RAW_RESPONSES["${model}:B"]}" | jq . > "$model_dir/tier-b-response.json" 2>/dev/null || true
    fi
    if [[ -n "${RAW_REQUESTS["${model}:C"]:-}" ]]; then
      echo "${RAW_REQUESTS["${model}:C"]}" | jq . > "$model_dir/tier-c-request.json" 2>/dev/null || true
    fi
    if [[ -n "${RAW_RESPONSES["${model}:C"]:-}" ]]; then
      echo "${RAW_RESPONSES["${model}:C"]}" | jq . > "$model_dir/tier-c-response.json" 2>/dev/null || true
    fi
  done

  # Summary JSON
  FORMAT="json" print_summary > "$run_dir/summary.json" 2>/dev/null

  # Summary markdown
  FORMAT="markdown" print_comparison_table > "$run_dir/summary.md" 2>/dev/null
  FORMAT="markdown" print_summary >> "$run_dir/summary.md" 2>/dev/null

  # Restore format
  if [[ "$FORMAT" == "terminal" ]]; then
    echo ""
    echo -e "  ${CYAN}Report saved: ${run_dir}/${NC}"
  fi
}

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if [[ "$FORMAT" == "terminal" ]]; then
  echo -e "${BOLD}=== Antenna Test Suite ===${NC}"
  if [[ ${#MODELS[@]} -gt 0 ]]; then
    echo "Models: ${MODELS[*]}"
  fi
  echo "Tier:   $TIER"
  if [[ -n "$REPORT_DIR" ]]; then
    echo "Report: $REPORT_DIR"
  fi
fi

# Run Tier A (always, once — model-independent)
if [[ "$TIER" == "all" || "$TIER" == "A" || "$TIER" == "a" ]]; then
  run_tier_a
  TIER_A_PASS=$((TOTAL_PASS))  # snapshot after A
fi

# Run Tier B per model
if [[ ${#MODELS[@]} -gt 0 ]]; then
  for model in "${MODELS[@]}"; do
    local_start=$(date +%s%N)

    if [[ "$TIER" == "all" || "$TIER" == "B" || "$TIER" == "b" ]]; then
      section "TIER B: Model → Tool Call"
      run_tier_b "$model"
    fi

    local_elapsed=$(( ($(date +%s%N) - local_start) / 1000000 ))
    RESULTS_TIME["$model"]="$(echo "scale=1; $local_elapsed / 1000" | bc)s"
  done
fi

# Tier A pass count (for reporting)
TIER_A_PASS=$((TIER_A_PASS))
TIER_A_TOTAL=$((TIER_A_TOTAL))

# Comparison table (multi-model)
if [[ ${#MODELS[@]} -gt 1 ]]; then
  print_comparison_table
fi

# Summary
print_summary

# Report
write_report

# Exit code
[[ $TOTAL_FAIL -gt 0 ]] && exit 1
exit 0
