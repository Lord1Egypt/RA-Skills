#!/usr/bin/env bash
set -euo pipefail
# Ignore SIGPIPE (exit 141) — occurs when jq output pipes into head/sort/uniq
# and the reader closes before jq finishes writing. Harmless in diagnostic context.
trap '' PIPE

VERSION="0.12.0"

# diagnose.sh — Detects 14 anti-patterns in an OpenClaw JSONL session file
# Usage: diagnose.sh <path-to-session.jsonl>
# Output: JSON array of findings to stdout; progress on stderr

usage() {
  cat <<EOF
Usage: diagnose.sh [--help|--version] <path-to-jsonl>

Description:
  Runs all 14 pattern detectors against a session JSONL file.

Options:
  --help      Show this help message and exit
  --version   Show version and exit

Example:
  diagnose.sh ~/.openclaw/agents/main/sessions/abc123.jsonl | jq .
EOF
}

check_deps() {
  for dep in jq awk bc; do
    if ! command -v "$dep" >/dev/null 2>&1; then
      echo "Error: required dependency '$dep' not found. Install it and retry." >&2
      exit 1
    fi
  done
}

if [[ $# -ge 1 ]]; then
  case "$1" in
    --help) usage; exit 0 ;;
    --version) echo "$VERSION"; exit 0 ;;
  esac
fi

check_deps

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <session.jsonl>" >&2
  exit 1
fi

JSONL="$1"

if [[ ! -f "$JSONL" ]]; then
  echo "Error: file not found: $JSONL" >&2
  exit 1
fi

# Guard against very large files (default: 100MB)
MAX_SIZE_BYTES="${CLAWDOC_MAX_FILE_SIZE:-104857600}"
FILE_SIZE=$(wc -c < "$JSONL" 2>/dev/null | tr -d ' ')
if [[ "$FILE_SIZE" -gt "$MAX_SIZE_BYTES" ]]; then
  echo "Warning: file is $(( FILE_SIZE / 1048576 ))MB — processing may be slow and memory-intensive. Set CLAWDOC_MAX_FILE_SIZE to override the ${MAX_SIZE_BYTES}-byte limit." >&2
fi

FINDINGS=()

add_finding() {
  local json="$1"
  FINDINGS+=("$json")
}

# ---------------------------------------------------------------------------
# Helpers: parse the JSONL once into shell variables where needed
# ---------------------------------------------------------------------------

# Session metadata (line 1)
# Use read to grab just the first line — avoids SIGPIPE from head under set -o pipefail
SESSION_LINE=""
IFS= read -r SESSION_LINE < "$JSONL" || true
SESSION_MODEL=$(echo "$SESSION_LINE" | jq -r '.model // ""' 2>/dev/null || echo "")
SESSION_KEY=$(echo "$SESSION_LINE" | jq -r '.sessionKey // ""' 2>/dev/null || echo "")
CONTEXT_TOKENS=128000

# ---------------------------------------------------------------------------
# Shared helper: find compaction turn index from token data
# Input: tab-separated lines with idx, tokens, ... (tokens in field 2)
# Output: prints the compaction turn index, or -1 if none found
# Used by: detect_compaction_damage (P10), detect_task_drift (P12)
# ---------------------------------------------------------------------------
find_compaction_idx() {
  local data="$1"
  local prev_tokens=0
  local result=-1

  while IFS=$'\t' read -r idx tokens _rest; do
    if [[ "$prev_tokens" -gt 0 && "$tokens" -gt 0 ]]; then
      local drop_pct
      drop_pct=$(echo "scale=1; ($prev_tokens - $tokens) * 100 / $prev_tokens" | bc 2>/dev/null || echo "0")
      local drop_int
      drop_int=$(echo "$drop_pct" | cut -d. -f1)
      drop_int=${drop_int:-0}
      if [[ "$drop_int" =~ ^-?[0-9]+$ ]] && [[ "$drop_int" -ge 40 ]]; then
        result=$idx
        break
      fi
    fi
    prev_tokens=$tokens
  done <<< "$data"

  echo "$result"
}

# ---------------------------------------------------------------------------
# Detector 1: detect_infinite_retry
# ---------------------------------------------------------------------------
detect_infinite_retry() {
  echo "[diagnose] running detect_infinite_retry..." >&2

  # Extract all toolCall names in message order (one per line), with turn index and cost
  # We emit: <turn_index> <tool_name> <input_snippet_100chars> <cost>
  local tool_seq
  tool_seq=$(jq -r '
    to_entries
    | map(select(.value.type == "message" and .value.message.role == "assistant"))
    | to_entries
    | .[]
    | . as $outer
    | .value.value.message.content[]?
    | select(.type == "toolCall")
    | [
        ($outer.key | tostring),
        .name,
        (.input | tojson | .[0:100]),
        ($outer.value.value.message.usage.cost.total // 0 | tostring)
      ]
    | join("\t")
  ' <(jq -s '.' "$JSONL" 2>/dev/null) 2>/dev/null) || return 0

  if [[ -z "$tool_seq" ]]; then return 0; fi

  # Use awk to find runs of >=5 consecutive same tool+input
  local finding
  finding=$(echo "$tool_seq" | awk -F'\t' '
  BEGIN { prev_name=""; prev_input=""; run=1; run_start=0; run_end=0; total_cost=0 }
  {
    turn=$1; name=$2; input=$3; cost=$4+0
    if (name == prev_name && input == prev_input) {
      run++
      total_cost += cost
      run_end = turn
    } else {
      if (run >= 5) {
        printf "%s\t%d\t%.6f\t%s\t%s\t%s\n", prev_name, run, total_cost, prev_input, run_start, run_end
      }
      run=1
      total_cost=cost
      prev_name=name
      prev_input=input
      run_start=turn
      run_end=turn
    }
  }
  END {
    if (run >= 5) {
      printf "%s\t%d\t%.6f\t%s\t%s\t%s\n", prev_name, run, total_cost, prev_input, run_start, run_end
    }
  }
  ')

  if [[ -z "$finding" ]]; then return 0; fi

  # Take the worst (highest run count) finding
  local worst
  worst=$(echo "$finding" | sort -t$'\t' -k2 -rn | head -1)

  local tool_name run_count cost_sum input_snippet run_start run_end
  tool_name=$(echo "$worst" | cut -f1)
  run_count=$(echo "$worst" | cut -f2)
  cost_sum=$(echo "$worst" | cut -f3)
  input_snippet=$(echo "$worst" | cut -f4)
  run_start=$(echo "$worst" | cut -f5)
  run_end=$(echo "$worst" | cut -f6)

  # Build a human-readable input summary from the snippet
  local cmd_display
  cmd_display=$(echo "$input_snippet" | jq -r 'if type=="object" then (.command // .path // .file_path // (to_entries[0].value // "") ) else . end' 2>/dev/null || echo "$input_snippet")
  # Fallback: if still empty or null, show raw JSON snippet (truncated) or "(empty input)"
  if [[ -z "$cmd_display" || "$cmd_display" == "null" ]]; then
    local raw_snippet
    raw_snippet=$(echo "$input_snippet" | tr -d '[:space:]')
    if [[ -z "$raw_snippet" || "$raw_snippet" == "{}" ]]; then
      cmd_display="(empty input)"
    else
      cmd_display=$(echo "$input_snippet" | cut -c1-80)
    fi
  fi

  local cost_rounded
  cost_rounded=$(printf "%.2f" "$cost_sum")

  # Look for error messages in toolResult scoped to the retry turn window
  local error_snippet=""
  error_snippet=$(jq -r --argjson start "$run_start" --argjson end "$run_end" '
    [ .[] | select(.type == "message") ] as $msgs |
    first(
      $msgs | to_entries[] |
      select(.key >= $start and .key <= ($end + 1)) |
      select(.value.message.role == "toolResult") |
      .value.message.content[]? | select(.type == "text") | .text |
      select(test("(?i)(error|fail|denied|timeout|not found|missing|exception|invalid)")) |
      .[0:120]
    ) // empty
  ' <(jq -s '.' "$JSONL" 2>/dev/null) 2>/dev/null) || error_snippet=""

  local evidence
  evidence="Turns $((run_start + 1))–$((run_end + 1)): \`${tool_name}\` called ${run_count} times consecutively with the same input \`$(echo "$cmd_display" | head -c 120)\`."
  if [[ -n "$error_snippet" ]]; then
    evidence="${evidence} Errors seen between retries: '$(echo "$error_snippet" | head -c 100)'"
  fi

  local prescription
  if echo "$SESSION_KEY" | grep -qE '^cron:'; then
    prescription="Your agent called \`${tool_name}\` ${run_count} times in a row, burning \$${cost_rounded}. Add \`timeoutSeconds\` to your cron payload to limit retries."
  else
    prescription="Your agent called \`${tool_name}\` ${run_count} times in a row with the same input, burning \$${cost_rounded}. The agent likely hit an error and kept retrying. Add an explicit stop condition or error check after \`${tool_name}\` calls in your task prompt."
  fi

  add_finding "$(jq -nc \
    --arg pattern "infinite-retry" \
    --argjson pattern_id 1 \
    --arg severity "critical" \
    --arg evidence "$evidence" \
    --argjson cost_impact "$(printf '%.6f' "$cost_sum")" \
    --arg prescription "$prescription" \
    '{pattern:$pattern,pattern_id:$pattern_id,severity:$severity,evidence:$evidence,cost_impact:$cost_impact,prescription:$prescription}')"
}

# ---------------------------------------------------------------------------
# Detector 2: detect_non_retryable_retry
# ---------------------------------------------------------------------------
detect_non_retryable_retry() {
  echo "[diagnose] running detect_non_retryable_retry..." >&2

  # For each toolResult with a non-retryable error, find the preceding assistant
  # toolCall name and count repeated identical calls.
  local result
  result=$(jq -r '
    [ .[] | select(.type == "message") ] as $msgs
    | $msgs | to_entries[]
    | select(.value.message.role == "toolResult")
    | . as $entry
    | .key as $idx
    | .value.message.content[]? | select(.type == "text") | .text as $err
    | select($err | test("Missing required parameter|Expected .* but received|TypeError|ValidationError|invalid.*parameter"; "i"))
    | if $idx > 0 then
        $msgs[$idx - 1].message as $prev
        | ($prev.content[]? | select(.type == "toolCall") | [.name, (.input | tojson | .[0:100]), $err[0:80]] | @tsv)
      else empty end
  ' <(jq -s '.' "$JSONL" 2>/dev/null) 2>/dev/null) || return 0

  if [[ -z "$result" ]]; then return 0; fi

  # Count occurrences per tool name
  local tool_counts
  tool_counts=$(echo "$result" | cut -f1 | sort | uniq -c | sort -rn | head -1)
  if [[ -z "$tool_counts" ]]; then return 0; fi

  local count tool_name
  count=$(echo "$tool_counts" | awk '{print $1}')
  tool_name=$(echo "$tool_counts" | awk '{print $2}')

  if [[ "$count" -lt 2 ]]; then return 0; fi

  local err_snippet
  err_snippet=$(echo "$result" | awk -F'\t' -v t="$tool_name" '$1==t {print $3; exit}' | head -c 80)

  local evidence="\`${tool_name}\` hit a non-retryable error '${err_snippet}' and was retried ${count} times with identical parameters. The error is deterministic — each retry produced the same failure, wasting tokens on calls that could never succeed."
  local prescription="\`${tool_name}\` failed with '${err_snippet}' and was retried ${count} times with the same invalid parameters. The error is deterministic — retrying won't fix it. Fix the input or add validation before calling \`${tool_name}\`."

  add_finding "$(jq -nc \
    --arg pattern "non-retryable-retry" \
    --argjson pattern_id 2 \
    --arg severity "high" \
    --arg evidence "$evidence" \
    --argjson cost_impact 0 \
    --arg prescription "$prescription" \
    '{pattern:$pattern,pattern_id:$pattern_id,severity:$severity,evidence:$evidence,cost_impact:$cost_impact,prescription:$prescription}')"
}

# ---------------------------------------------------------------------------
# Detector 3: detect_tool_as_text
# ---------------------------------------------------------------------------
detect_tool_as_text() {
  echo "[diagnose] running detect_tool_as_text..." >&2

  # Find assistant messages that have text matching tool invocation patterns
  # but NO toolCall block in the same message
  local findings
  findings=$(jq -r '
    .[]
    | select(.type == "message" and .message.role == "assistant")
    | .message as $msg
    | ($msg.content // []) as $content
    | ($content | map(select(.type == "toolCall")) | length) as $tc_count
    | if $tc_count > 0 then empty else
        $content[]
        | select(.type == "text")
        | .text
        | split("\n")[]
        | select(test("^(read|exec|write|search_web|browser_navigate|web_fetch)\\s+"))
      end
  ' <(jq -s '.' "$JSONL" 2>/dev/null) 2>/dev/null | sort | uniq -c | sort -rn) || return 0

  if [[ -z "$findings" ]]; then return 0; fi

  # Take the most common
  local top_count top_line
  top_count=$(echo "$findings" | head -1 | awk '{print $1}')
  top_line=$(echo "$findings" | head -1 | sed 's/^ *[0-9]* *//' | head -c 120)

  local evidence="Agent output '${top_line}' as plain text ${top_count} times without executing"
  local prescription="Agent wrote '${top_line}' as plain text ${top_count} times instead of executing it as a tool call. This usually means the model or provider doesn't support tool use, or the tool definition is missing. Check your model configuration and verify tool definitions are loaded."

  add_finding "$(jq -nc \
    --arg pattern "tool-as-text" \
    --argjson pattern_id 3 \
    --arg severity "high" \
    --arg evidence "$evidence" \
    --argjson cost_impact 0 \
    --arg prescription "$prescription" \
    '{pattern:$pattern,pattern_id:$pattern_id,severity:$severity,evidence:$evidence,cost_impact:$cost_impact,prescription:$prescription}')"
}

# ---------------------------------------------------------------------------
# Detector 4: detect_context_exhaustion
# ---------------------------------------------------------------------------
detect_context_exhaustion() {
  echo "[diagnose] running detect_context_exhaustion..." >&2

  # Extract inputTokens and contextTokens from all assistant messages
  local token_data
  token_data=$(jq -r '
    .[]
    | select(.type == "message" and .message.role == "assistant")
    | [
        (.message.usage.inputTokens // 0 | tostring),
        (.message.usage.contextTokens // 128000 | tostring),
        (.message.usage.cost.total // 0 | tostring)
      ]
    | join("\t")
  ' <(jq -s '.' "$JSONL" 2>/dev/null) 2>/dev/null) || return 0

  if [[ -z "$token_data" ]]; then return 0; fi

  local max_input_tokens=0
  local context_tokens=$CONTEXT_TOKENS
  local total_cost=0
  local turn=0
  local max_jump=0
  local max_jump_turn=0
  local window_start_tokens=()

  while IFS=$'\t' read -r input_tok ctx_tok cost; do
    turn=$((turn + 1))
    input_tok=${input_tok:-0}
    ctx_tok=${ctx_tok:-128000}
    cost=${cost:-0}

    # Track context tokens (use the most recent non-zero value)
    if [[ "$ctx_tok" -gt 0 ]]; then
      context_tokens=$ctx_tok
    fi

    total_cost=$(echo "$total_cost + $cost" | bc 2>/dev/null || echo "$total_cost")

    if [[ "$input_tok" -gt "$max_input_tokens" ]]; then
      max_input_tokens=$input_tok
    fi

    # Track 10-turn window for doubling detection
    window_start_tokens+=("$input_tok")
    if [[ ${#window_start_tokens[@]} -gt 10 ]]; then
      local oldest="${window_start_tokens[0]}"
      window_start_tokens=("${window_start_tokens[@]:1}")
      if [[ "$oldest" -gt 0 ]]; then
        local jump=$(( input_tok - oldest ))
        if [[ "$jump" -gt "$max_jump" ]]; then
          max_jump=$jump
          max_jump_turn=$turn
        fi
      fi
    fi
  done <<< "$token_data"

  if [[ "$max_input_tokens" -eq 0 || "$context_tokens" -eq 0 ]]; then return 0; fi

  local pct
  pct=$(echo "scale=1; $max_input_tokens * 100 / $context_tokens" | bc 2>/dev/null || echo "0")
  local pct_int
  pct_int=$(echo "$pct" | cut -d. -f1)

  # Only flag if > 70%
  if [[ "$pct_int" -lt 70 ]]; then
    # Also check 10-turn doubling: if max_input >= 2 * (oldest in any window)
    # We already tracked max_jump; check if any window start was < half max_input
    return 0
  fi

  local severity
  if [[ "$pct_int" -ge 90 ]]; then
    severity="high"
  else
    severity="medium"
  fi

  local ctx_k; ctx_k=$(echo "scale=0; $context_tokens / 1000" | bc 2>/dev/null || echo "$(( context_tokens / 1000 ))")
  local max_k; max_k=$(echo "scale=0; $max_input_tokens / 1000" | bc 2>/dev/null || echo "$(( max_input_tokens / 1000 ))")
  local jump_k; jump_k=$(echo "scale=0; $max_jump / 1000" | bc 2>/dev/null || echo "$(( max_jump / 1000 ))")

  local evidence="Session consumed ${max_k}K of ${ctx_k}K available tokens (${pct}%) over ${turn} turns. The largest single jump was +${jump_k}K tokens at turn ${max_jump_turn}, likely from a large file read or tool output that inflated the context."
  local prescription="Context hit ${pct}% of the ${ctx_k}K limit. The biggest spike was +${jump_k}K tokens at turn ${max_jump_turn} — check what tool output or file read caused it. Run /compact before hitting the wall, or use \`exec with tail/head\` to read only what you need instead of full files."

  local total_cost_rounded
  total_cost_rounded=$(printf "%.6f" "$total_cost" 2>/dev/null || echo "0")

  add_finding "$(jq -nc \
    --arg pattern "context-exhaustion" \
    --argjson pattern_id 4 \
    --arg severity "$severity" \
    --arg evidence "$evidence" \
    --argjson cost_impact "$total_cost_rounded" \
    --arg prescription "$prescription" \
    '{pattern:$pattern,pattern_id:$pattern_id,severity:$severity,evidence:$evidence,cost_impact:$cost_impact,prescription:$prescription}')"
}

# ---------------------------------------------------------------------------
# Detector 5: detect_subagent_replay
# ---------------------------------------------------------------------------
detect_subagent_replay() {
  echo "[diagnose] running detect_subagent_replay..." >&2

  # Only applies if sessionKey matches agent:*:subagent:*
  if ! echo "$SESSION_KEY" | grep -qE '^agent:.+:subagent:.+'; then
    return 0
  fi

  # Find consecutive identical assistant messages (same text content)
  local replay_data
  replay_data=$(jq -r '
    [ .[] | select(.type == "message" and .message.role == "assistant") ]
    | to_entries[]
    | .key as $k
    | .value.message as $m
    | ($m.usage.cost.total // 0) as $cost
    | ($m.content // [] | .[] | select(.type == "text") | .text) as $txt
    | [$k | tostring, $txt, ($cost | tostring)]
    | @tsv
  ' <(jq -s '.' "$JSONL" 2>/dev/null) 2>/dev/null) || return 0

  if [[ -z "$replay_data" ]]; then return 0; fi

  # Use awk to find consecutive runs of same text
  local worst
  worst=$(echo "$replay_data" | awk -F'\t' '
  BEGIN { prev_text=""; run=1; total_cost=0; best_run=0; best_cost=0; best_text="" }
  {
    idx=$1; text=$2; cost=$3+0
    if (text == prev_text) {
      run++
      total_cost += cost
    } else {
      if (run > best_run) {
        best_run = run
        best_cost = total_cost
        best_text = prev_text
      }
      run = 1
      total_cost = cost
      prev_text = text
    }
  }
  END {
    if (run > best_run) {
      best_run = run
      best_cost = total_cost
      best_text = prev_text
    }
    if (best_run >= 3) {
      printf "%d\t%.6f\t%s\n", best_run, best_cost, substr(best_text, 1, 80)
    }
  }
  ')

  if [[ -z "$worst" ]]; then return 0; fi

  local run_count cost_sum
  run_count=$(echo "$worst" | cut -f1)
  cost_sum=$(echo "$worst" | cut -f2)

  local evidence="Sub-agent completed but result was delivered ${run_count} times to parent session"
  local prescription="Known sub-agent delivery bug. Monitor sub-agent spawns and report persistent issues to the OpenClaw repo."

  add_finding "$(jq -nc \
    --arg pattern "subagent-replay" \
    --argjson pattern_id 5 \
    --arg severity "medium" \
    --arg evidence "$evidence" \
    --argjson cost_impact "$(printf '%.6f' "$cost_sum")" \
    --arg prescription "$prescription" \
    '{pattern:$pattern,pattern_id:$pattern_id,severity:$severity,evidence:$evidence,cost_impact:$cost_impact,prescription:$prescription}')"
}

# ---------------------------------------------------------------------------
# Detector 6: detect_cost_spike
# ---------------------------------------------------------------------------
detect_cost_spike() {
  echo "[diagnose] running detect_cost_spike..." >&2

  # Extract per-turn costs with turn index and tool call name
  local turn_costs
  turn_costs=$(jq -r '
    to_entries
    | map(select(.value.type == "message" and .value.message.role == "assistant"))
    | to_entries
    | .[]
    | [
        (.key + 1 | tostring),
        (.value.value.message.usage.cost.total // 0 | tostring),
        (.value.value.message.content // [] | map(select(.type == "toolCall")) | .[0].name // "(no tool)")
      ]
    | join("\t")
  ' <(jq -s '.' "$JSONL" 2>/dev/null) 2>/dev/null) || return 0

  if [[ -z "$turn_costs" ]]; then return 0; fi

  local total_cost=0
  local max_turn_cost=0
  local max_turn_num=0
  local max_turn_tool=""

  while IFS=$'\t' read -r turn_num cost tool_name; do
    total_cost=$(echo "$total_cost + $cost" | bc 2>/dev/null || echo "0")
    local cost_f
    cost_f=$(printf '%.6f' "$cost" 2>/dev/null || echo "0")
    local max_f
    max_f=$(printf '%.6f' "$max_turn_cost" 2>/dev/null || echo "0")
    if (( $(echo "$cost_f > $max_f" | bc -l 2>/dev/null || echo 0) )); then
      max_turn_cost=$cost
      max_turn_num=$turn_num
      max_turn_tool=$tool_name
    fi
  done <<< "$turn_costs"

  local max_rounded
  max_rounded=$(printf "%.2f" "$max_turn_cost" 2>/dev/null || echo "0")

  # Determine if we should flag
  # Thresholds configurable via env vars (defaults calibrated for Sonnet-class models)
  local turn_threshold_critical="${CLAWDOC_COST_TURN_CRITICAL:-1.00}"
  local turn_threshold_high="${CLAWDOC_COST_TURN_HIGH:-0.50}"
  local session_threshold="${CLAWDOC_COST_SESSION:-1.00}"

  local flag=0
  local severity=""
  local cost_impact=0

  if (( $(echo "$max_turn_cost > $turn_threshold_critical" | bc -l 2>/dev/null || echo 0) )); then
    flag=1; severity="critical"
    cost_impact=$(echo "$max_turn_cost - $turn_threshold_high" | bc 2>/dev/null || echo "$max_turn_cost")
  elif (( $(echo "$max_turn_cost > $turn_threshold_high" | bc -l 2>/dev/null || echo 0) )); then
    flag=1; severity="high"
    cost_impact=$(echo "$max_turn_cost - $turn_threshold_high" | bc 2>/dev/null || echo "$max_turn_cost")
  elif (( $(echo "$total_cost > $session_threshold" | bc -l 2>/dev/null || echo 0) )); then
    flag=1; severity="medium"
    cost_impact=$total_cost
  fi

  if [[ "$flag" -eq 0 ]]; then return 0; fi

  # Top 3 turns by cost
  local top3
  top3=$(echo "$turn_costs" | sort -t$'\t' -k2 -rn | head -3)
  local top3_total=0
  while IFS=$'\t' read -r _ c _; do
    top3_total=$(echo "$top3_total + $c" | bc 2>/dev/null || echo "$top3_total")
  done <<< "$top3"

  local top3_pct
  if (( $(echo "$total_cost > 0" | bc -l 2>/dev/null || echo 0) )); then
    top3_pct=$(echo "scale=0; $top3_total * 100 / $total_cost" | bc 2>/dev/null || echo "0")
  else
    top3_pct=0
  fi

  local total_rounded
  total_rounded=$(printf "%.2f" "$total_cost" 2>/dev/null || echo "0")
  local turn_count
  turn_count=$(echo "$turn_costs" | wc -l | tr -d ' ')

  local evidence
  if [ "$max_turn_tool" = "(no tool)" ]; then
    evidence="Session spent \$${total_rounded} across ${turn_count} turns. The most expensive single turn was turn ${max_turn_num} at \$${max_rounded} with no tool call — the agent was generating a long response on an inflated context. The top 3 most expensive turns accounted for ${top3_pct}% of the total session cost."
  else
    evidence="Session spent \$${total_rounded} across ${turn_count} turns. The most expensive single turn was turn ${max_turn_num} at \$${max_rounded} running \`${max_turn_tool}\`. The top 3 most expensive turns accounted for ${top3_pct}% of the total session cost."
  fi

  local prescription
  if [ "$max_turn_tool" = "(no tool)" ]; then
    prescription="Turn ${max_turn_num} cost \$${max_rounded} with no tool call — likely a large context response. Run /compact before this point to reduce accumulated context, or split the task into a sub-agent."
  else
    prescription="Turn ${max_turn_num} cost \$${max_rounded} on \`${max_turn_tool}\`. If this was a large file read or web fetch, use \`exec with tail/head\` to limit input size, or run /compact after processing large outputs."
  fi

  add_finding "$(jq -nc \
    --arg pattern "cost-spike" \
    --argjson pattern_id 6 \
    --arg severity "$severity" \
    --arg evidence "$evidence" \
    --argjson cost_impact "$(printf '%.6f' "$cost_impact")" \
    --arg prescription "$prescription" \
    '{pattern:$pattern,pattern_id:$pattern_id,severity:$severity,evidence:$evidence,cost_impact:$cost_impact,prescription:$prescription}')"
}

# ---------------------------------------------------------------------------
# Detector 7: detect_skill_miss
# ---------------------------------------------------------------------------
detect_skill_miss() {
  echo "[diagnose] running detect_skill_miss..." >&2

  # Find toolResult messages with "command not found" style errors
  local findings
  findings=$(jq -r '
    .[]
    | select(.type == "message" and .message.role == "toolResult")
    | .message.content[]?
    | select(.type == "text")
    | .text
    | select(test("command not found|not installed|No such file or directory|is not recognized as"; "i"))
    | .
  ' <(jq -s '.' "$JSONL" 2>/dev/null) 2>/dev/null) || return 0

  if [[ -z "$findings" ]]; then return 0; fi

  # Extract the command that failed — use a simpler O(n) approach instead of O(n²)
  # Pair each toolResult with its preceding assistant toolCall using sequential scan
  local cmd_snippet=""
  local first_err
  # Use bash read to get first line without a pipe (avoids broken pipe on large $findings)
  IFS= read -r first_err <<< "$findings" || true
  first_err="${first_err:0:100}"

  # Simple approach: find assistant toolCall names near the error
  # Use jq limit(1;...) to avoid SIGPIPE from head -1
  cmd_snippet=$(jq -r '
    [ .[] | select(.type == "message") ] | to_entries as $msgs |
    first(
      $msgs[] |
      select(.value.message.role == "toolResult") |
      select((.value.message.content[]? | select(.type == "text") | .text) |
        test("command not found|not installed|No such file or directory|is not recognized as"; "i")) |
      .key as $k |
      if $k > 0 then
        ($msgs[$k - 1].value.message.content[]? | select(.type == "toolCall") |
          .input | (.command // .path // .file_path // "") | .[0:80])
      else "unknown" end
    ) // "unknown"
  ' <(jq -s '.' "$JSONL" 2>/dev/null) 2>/dev/null) || cmd_snippet=""

  if [[ -z "$cmd_snippet" || "$cmd_snippet" == "unknown" || "$cmd_snippet" == "null" ]]; then
    # Extract the actual missing command from "command not found: <name>" pattern
    cmd_snippet=$(echo "$first_err" | grep -oE 'command not found: [a-zA-Z][a-zA-Z0-9_-]+' | sed 's/command not found: //' | head -1)
  fi
  if [[ -z "$cmd_snippet" ]]; then
    # Fallback: extract from "No such file or directory" or "not installed" patterns
    cmd_snippet=$(echo "$first_err" | grep -oE "'[a-zA-Z][a-zA-Z0-9_-]+'" | tr -d "'" | head -1)
  fi
  if [[ -z "$cmd_snippet" ]]; then
    cmd_snippet="(unknown command)"
  fi

  local evidence="exec called with '${cmd_snippet}' failed: ${first_err}"
  local prescription="\`${cmd_snippet}\` is not installed on this machine. Install it (e.g. \`brew install ${cmd_snippet}\` or \`apt install ${cmd_snippet}\`) or remove the skill that depends on it."

  add_finding "$(jq -nc \
    --arg pattern "skill-miss" \
    --argjson pattern_id 7 \
    --arg severity "low" \
    --arg evidence "$evidence" \
    --argjson cost_impact 0 \
    --arg prescription "$prescription" \
    '{pattern:$pattern,pattern_id:$pattern_id,severity:$severity,evidence:$evidence,cost_impact:$cost_impact,prescription:$prescription}')"
}

# ---------------------------------------------------------------------------
# Detector 8: detect_model_routing_waste
# ---------------------------------------------------------------------------
detect_model_routing_waste() {
  echo "[diagnose] running detect_model_routing_waste..." >&2

  # Check if session key contains cron: or heartbeat AND model is expensive
  local is_cron=0
  if echo "$SESSION_KEY" | grep -qE '(^cron:|heartbeat)'; then
    is_cron=1
  fi

  if [[ "$is_cron" -eq 0 ]]; then return 0; fi

  # Check if model is expensive (opus, sonnet, gpt-4o, gemini-pro)
  local is_expensive=0
  if echo "$SESSION_MODEL" | grep -qiE '(opus|sonnet|gpt-4o|gemini-pro)'; then
    is_expensive=1
  fi

  if [[ "$is_expensive" -eq 0 ]]; then return 0; fi

  # Calculate total cost and turn count
  local session_stats
  session_stats=$(jq -r '
    [ .[] | select(.type == "message" and .message.role == "assistant") ] as $msgs
    | {
        turns: ($msgs | length),
        total_cost: ($msgs | map(.message.usage.cost.total // 0) | add // 0),
        total_input_tokens: ($msgs | map(.message.usage.inputTokens // 0) | add // 0)
      }
    | [(.turns | tostring), (.total_cost | tostring), (.total_input_tokens | tostring)]
    | join("\t")
  ' <(jq -s '.' "$JSONL" 2>/dev/null) 2>/dev/null) || return 0

  if [[ -z "$session_stats" ]]; then return 0; fi

  local turns total_cost total_input_tokens
  turns=$(echo "$session_stats" | cut -f1)
  total_cost=$(echo "$session_stats" | cut -f2)
  total_input_tokens=$(echo "$session_stats" | cut -f3)

  local cost_rounded
  cost_rounded=$(printf "%.2f" "$total_cost" 2>/dev/null || echo "0")

  local tokens_k
  tokens_k=$(echo "scale=0; $total_input_tokens / 1000" | bc 2>/dev/null || echo "$(( total_input_tokens / 1000 ))")

  # Savings: haiku would cost ~10% of opus/sonnet
  local cost_impact
  cost_impact=$(echo "scale=6; $total_cost * 0.9" | bc 2>/dev/null || echo "0")

  local evidence="Session on ${SESSION_MODEL} with sessionKey '${SESSION_KEY}' — ${turns} turns, ${tokens_k}K tokens, \$${cost_rounded}"
  local haiku_cost
  haiku_cost=$(printf '%.2f' "$(echo "scale=4; $total_cost * 0.1" | bc 2>/dev/null || echo "0")")
  local prescription="Switching this cron to claude-haiku-4-5 would cost ~\$${haiku_cost} for the same work. Add to openclaw.json: \`\"heartbeat\": { \"model\": \"anthropic/claude-haiku-4-5\" }\`"

  add_finding "$(jq -nc \
    --arg pattern "model-routing-waste" \
    --argjson pattern_id 8 \
    --arg severity "medium" \
    --arg evidence "$evidence" \
    --argjson cost_impact "$(printf '%.6f' "$cost_impact")" \
    --arg prescription "$prescription" \
    '{pattern:$pattern,pattern_id:$pattern_id,severity:$severity,evidence:$evidence,cost_impact:$cost_impact,prescription:$prescription}')"
}

# ---------------------------------------------------------------------------
# Detector 9: detect_cron_accumulation
# ---------------------------------------------------------------------------
detect_cron_accumulation() {
  echo "[diagnose] running detect_cron_accumulation..." >&2

  # Only for cron sessions
  if ! echo "$SESSION_KEY" | grep -qE '^cron:'; then
    return 0
  fi

  # Extract inputTokens from each assistant turn in order
  local token_seq
  token_seq=$(jq -r '
    .[]
    | select(.type == "message" and .message.role == "assistant")
    | (.message.usage.inputTokens // 0)
  ' <(jq -s '.' "$JSONL" 2>/dev/null) 2>/dev/null) || return 0

  if [[ -z "$token_seq" ]]; then return 0; fi

  local first_val=0
  local last_val=0
  local prev_val=0
  local is_monotonic=1
  local count=0

  while read -r val; do
    count=$((count + 1))
    if [[ "$count" -eq 1 ]]; then
      first_val=$val
    fi
    last_val=$val
    if [[ "$prev_val" -gt 0 && "$val" -lt "$prev_val" ]]; then
      is_monotonic=0
    fi
    prev_val=$val
  done <<< "$token_seq"

  if [[ "$count" -lt 2 || "$is_monotonic" -eq 0 ]]; then return 0; fi
  if [[ "$first_val" -eq 0 ]]; then return 0; fi

  # Check if highest (last_val) > 2x lowest (first_val)
  local threshold=$(( first_val * 2 ))
  if [[ "$last_val" -le "$threshold" ]]; then return 0; fi

  local cron_name="${SESSION_KEY#cron:}"
  local growth_x=$(( last_val / first_val ))
  local evidence="cron:${cron_name} inputTokens grew from ${first_val} to ${last_val} (${growth_x}x) across session — accumulating context across runs"
  local prescription="Cron \`${cron_name}\` is growing ${growth_x}x per run (${first_val} → ${last_val} tokens). Each run inherits the previous run's context. Set session isolation: \`\"session\": { \"isolated\": true }\` in your cron config so each run starts fresh."

  add_finding "$(jq -nc \
    --arg pattern "cron-accumulation" \
    --argjson pattern_id 9 \
    --arg severity "medium" \
    --arg evidence "$evidence" \
    --argjson cost_impact 0 \
    --arg prescription "$prescription" \
    '{pattern:$pattern,pattern_id:$pattern_id,severity:$severity,evidence:$evidence,cost_impact:$cost_impact,prescription:$prescription}')"
}

# ---------------------------------------------------------------------------
# Detector 10: detect_compaction_damage
# ---------------------------------------------------------------------------
detect_compaction_damage() {
  echo "[diagnose] running detect_compaction_damage..." >&2

  # Extract per-turn: turn_index, inputTokens, and all toolCall name+input pairs
  local turns_data
  turns_data=$(jq -r '
    [ .[] | select(.type == "message" and .message.role == "assistant") ]
    | to_entries[]
    | .key as $idx
    | .value.message as $m
    | [
        ($idx | tostring),
        ($m.usage.inputTokens // 0 | tostring),
        ($m.usage.cost.total // 0 | tostring),
        ([$m.content[]? | select(.type == "toolCall") | {name: .name, input: (.input | tojson | .[0:100])}] | tojson)
      ]
    | join("\t")
  ' <(jq -s '.' "$JSONL" 2>/dev/null) 2>/dev/null) || return 0

  if [[ -z "$turns_data" ]]; then return 0; fi

  # Find compaction event using shared helper
  local compaction_idx
  compaction_idx=$(find_compaction_idx "$turns_data")

  if [[ "$compaction_idx" -lt 0 ]]; then return 0; fi

  # Collect toolCall name+input from BEFORE compaction
  local pre_tool_set=()
  while IFS=$'\t' read -r idx tokens cost tool_calls_json; do
    if [[ "$idx" -ge "$compaction_idx" ]]; then break; fi
    # Extract each tool call as "name|input" string
    while IFS= read -r tool_entry; do
      pre_tool_set+=("$tool_entry")
    done < <(echo "$tool_calls_json" | jq -r '.[] | [.name, .input] | join("|")' 2>/dev/null || true)
  done <<< "$turns_data"

  if [[ ${#pre_tool_set[@]} -eq 0 ]]; then return 0; fi

  # Check next 5 turns AFTER compaction for repeated tool calls
  local repeated_tools=()
  local post_cost=0
  local post_turn_count=0

  while IFS=$'\t' read -r idx tokens cost tool_calls_json; do
    if [[ "$idx" -le "$compaction_idx" ]]; then continue; fi
    if [[ "$post_turn_count" -ge 5 ]]; then break; fi
    post_turn_count=$((post_turn_count + 1))

    while IFS= read -r tool_entry; do
      for pre in "${pre_tool_set[@]}"; do
        if [[ "$tool_entry" == "$pre" ]]; then
          repeated_tools+=("$(echo "$tool_entry" | cut -d'|' -f1)")
          post_cost=$(echo "$post_cost + $cost" | bc 2>/dev/null || echo "$post_cost")
          break
        fi
      done
    done < <(echo "$tool_calls_json" | jq -r '.[] | [.name, .input] | join("|")' 2>/dev/null || true)
  done <<< "$turns_data"

  if [[ ${#repeated_tools[@]} -eq 0 ]]; then return 0; fi

  # Get the tokens before/after compaction for evidence
  local pre_tokens=0
  local post_tokens=0
  while IFS=$'\t' read -r idx tokens cost tool_calls_json; do
    if [[ "$idx" -eq $((compaction_idx - 1)) ]]; then pre_tokens=$tokens; fi
    if [[ "$idx" -eq "$compaction_idx" ]]; then post_tokens=$tokens; fi
  done <<< "$turns_data"

  local pre_k=$(( pre_tokens / 1000 ))
  local post_k=$(( post_tokens / 1000 ))

  # Unique tool names repeated
  local unique_repeated
  unique_repeated=$(printf '%s\n' "${repeated_tools[@]}" | sort -u | tr '\n' ', ' | sed 's/,$//')

  local repeated_count=${#repeated_tools[@]}
  local post_cost_rounded
  post_cost_rounded=$(printf "%.2f" "$post_cost")
  local evidence="Compaction at turn $((compaction_idx + 1)) dropped context from ${pre_k}K to ${post_k}K tokens. In the next 5 turns, the agent re-called \`${unique_repeated}\` — ${repeated_count} tool call(s) that it had already completed before compaction, wasting \$${post_cost_rounded}. The agent lost its memory of prior work and started over."
  local prescription="Compaction at turn $((compaction_idx + 1)) dropped context from ${pre_k}K to ${post_k}K tokens, and the agent re-ran \`${unique_repeated}\` — work it already completed. Write key results to MEMORY.md before long sessions so they survive compaction, or increase \`compaction.softThresholdTokens\` to delay compaction."

  add_finding "$(jq -nc \
    --arg pattern "compaction-damage" \
    --argjson pattern_id 10 \
    --arg severity "medium" \
    --arg evidence "$evidence" \
    --argjson cost_impact "$(printf '%.6f' "$post_cost")" \
    --arg prescription "$prescription" \
    '{pattern:$pattern,pattern_id:$pattern_id,severity:$severity,evidence:$evidence,cost_impact:$cost_impact,prescription:$prescription}')"
}

# ---------------------------------------------------------------------------
# Detector 11: detect_workspace_overhead
# ---------------------------------------------------------------------------
detect_workspace_overhead() {
  echo "[diagnose] running detect_workspace_overhead..." >&2

  # Find the FIRST assistant message's inputTokens and contextTokens
  local first_turn_data
  first_turn_data=$(jq -r '
    [ .[] | select(.type == "message" and .message.role == "assistant") ]
    | .[0]
    | [
        (.message.usage.inputTokens // 0 | tostring),
        (.message.usage.contextTokens // 128000 | tostring),
        (.message.usage.cost.total // 0 | tostring)
      ]
    | join("\t")
  ' <(jq -s '.' "$JSONL" 2>/dev/null) 2>/dev/null) || return 0

  if [[ -z "$first_turn_data" ]]; then return 0; fi

  local first_input_tokens ctx_tokens
  first_input_tokens=$(echo "$first_turn_data" | cut -f1)
  ctx_tokens=$(echo "$first_turn_data" | cut -f2)

  if [[ "$first_input_tokens" -eq 0 || "$ctx_tokens" -eq 0 ]]; then return 0; fi

  # Check if > 15% of contextTokens
  local threshold; threshold=$(echo "scale=0; $ctx_tokens * 15 / 100" | bc 2>/dev/null || echo "$(( ctx_tokens * 15 / 100 ))")
  if [[ "$first_input_tokens" -le "$threshold" ]]; then return 0; fi

  local pct
  pct=$(echo "scale=1; $first_input_tokens * 100 / $ctx_tokens" | bc 2>/dev/null || echo "0")

  local first_k=$(( first_input_tokens / 1000 ))
  local ctx_k=$(( ctx_tokens / 1000 ))

  # Total session cost
  local total_cost
  total_cost=$(jq -r '
    [ .[] | select(.type == "message" and .message.role == "assistant") ]
    | map(.message.usage.cost.total // 0) | add // 0
  ' <(jq -s '.' "$JSONL" 2>/dev/null) 2>/dev/null) || total_cost=0

  # cost_impact: (first_input_tokens / contextTokens) * total_session_cost
  local cost_impact
  cost_impact=$(echo "scale=6; $first_input_tokens * $total_cost / $ctx_tokens" | bc 2>/dev/null || echo "0")

  local remaining_k=$(( (ctx_tokens - first_input_tokens) / 1000 ))
  local pct_int_ws
  pct_int_ws=$(echo "$pct" | cut -d. -f1)
  local remaining_pct=$(( 100 - pct_int_ws ))
  local evidence="Before the first tool call, ${first_k}K of ${ctx_k}K tokens (${pct}%) were already consumed by system prompt and workspace files (AGENTS.md, SOUL.md, TOOLS.md, etc.). Only ${remaining_k}K tokens (${remaining_pct}%) remain for the actual conversation — limiting how much work the agent can do before hitting context limits."
  local prescription="${first_k}K of your ${ctx_k}K context window is consumed by system prompt and workspace files before any real work starts — leaving only ${remaining_k}K for the actual task. Trim AGENTS.md, SOUL.md, and other workspace files, or split large configuration into separate files loaded on demand."

  add_finding "$(jq -nc \
    --arg pattern "workspace-overhead" \
    --argjson pattern_id 11 \
    --arg severity "medium" \
    --arg evidence "$evidence" \
    --argjson cost_impact "$(printf '%.6f' "$cost_impact")" \
    --arg prescription "$prescription" \
    '{pattern:$pattern,pattern_id:$pattern_id,severity:$severity,evidence:$evidence,cost_impact:$cost_impact,prescription:$prescription}')"
}

# ---------------------------------------------------------------------------
# Detector 12: detect_task_drift
# ---------------------------------------------------------------------------
detect_task_drift() {
  echo "[diagnose] running detect_task_drift..." >&2

  # --- Sub-detector A: Post-compaction directory divergence ---

  # Extract per-turn: turn_index, inputTokens, cost, list of file paths from toolCall inputs
  local turns_data
  turns_data=$(jq -r '
    [ .[] | select(.type == "message" and .message.role == "assistant") ]
    | to_entries[]
    | .key as $idx
    | .value.message as $m
    | ($m.usage.inputTokens // 0) as $tokens
    | ($m.usage.cost.total // 0) as $cost
    | ([$m.content[]? | select(.type == "toolCall")
        | (.input.path // .input.file_path // "")
        | select(. != "" and . != null)]
       | join("|")) as $paths
    | [($idx | tostring), ($tokens | tostring), ($cost | tostring), $paths]
    | join("\t")
  ' <(jq -s '.' "$JSONL" 2>/dev/null) 2>/dev/null) || return 0

  if [[ -z "$turns_data" ]]; then return 0; fi

  # Find compaction using shared helper
  local compaction_idx
  compaction_idx=$(find_compaction_idx "$turns_data")

  if [[ "$compaction_idx" -ge 0 ]]; then
    # Collect directories touched before and after compaction
    local pre_dirs=""
    local post_cost=0
    local post_new_dir_count=0
    local post_total_dir_count=0
    local post_new_dirs_list=""

    while IFS=$'\t' read -r idx tokens cost paths; do
      if [[ -z "$paths" ]]; then continue; fi
      # Extract parent directories from pipe-separated paths
      local dir_list
      dir_list=$(echo "$paths" | tr '|' '\n' | while read -r p; do
        echo "$p" | sed 's|/[^/]*$||' | grep -v '^$'
      done | sort -u)

      if [[ "$idx" -lt "$compaction_idx" ]]; then
        if [[ -n "$dir_list" ]]; then
          pre_dirs=$(printf '%s\n%s' "$pre_dirs" "$dir_list" | sort -u | grep -v '^$')
        fi
      elif [[ "$idx" -gt "$compaction_idx" ]]; then
        if [[ -n "$dir_list" ]]; then
          while read -r d; do
            post_total_dir_count=$((post_total_dir_count + 1))
            if ! echo "$pre_dirs" | grep -qxF "$d"; then
              post_new_dir_count=$((post_new_dir_count + 1))
              post_new_dirs_list=$(printf '%s\n%s' "$post_new_dirs_list" "$d" | sort -u | grep -v '^$')
              post_cost=$(echo "$post_cost + $cost" | bc 2>/dev/null || echo "$post_cost")
            fi
          done <<< "$dir_list"
        fi
      fi
    done <<< "$turns_data"

    # Trigger if: pre_dirs non-empty AND >=3 tool calls to new dirs AND new dirs > 50% of post-compaction activity
    # If pre_dirs is empty, there's no baseline to compare — skip drift detection
    if [[ -n "$pre_dirs" && "$post_new_dir_count" -ge 3 && "$post_total_dir_count" -gt 0 ]]; then
      local new_pct=$(( post_new_dir_count * 100 / post_total_dir_count ))
      if [[ "$new_pct" -ge 50 ]]; then
        local unique_new_dirs
        unique_new_dirs=$(echo "$post_new_dirs_list" | tr '\n' ', ' | sed 's/,$//')
        local pre_dirs_short
        pre_dirs_short=$(echo "$pre_dirs" | head -3 | tr '\n' ', ' | sed 's/,$//')
        local evidence="The agent worked in ${pre_dirs_short} for the first $((compaction_idx)) turns. After compaction at turn $((compaction_idx + 1)), it drifted to entirely new directories: ${unique_new_dirs}. ${post_new_dir_count} of ${post_total_dir_count} post-compaction file operations (${new_pct}%) went to directories the agent never touched before compaction — it lost track of its original task."
        local cost_rounded
        cost_rounded=$(printf "%.2f" "$post_cost")
        local prescription="Agent was working in ${pre_dirs_short} before compaction at turn $((compaction_idx + 1)), then drifted to ${unique_new_dirs} — ${new_pct}% of post-compaction work went to directories it never touched before, wasting \$${cost_rounded}. Write your current objective to MEMORY.md before long sessions so it survives compaction, or delegate sub-tasks to sub-agents."

        add_finding "$(jq -nc \
          --arg pattern "task-drift" \
          --argjson pattern_id 12 \
          --arg severity "medium" \
          --arg evidence "$evidence" \
          --argjson cost_impact "$(printf '%.6f' "$post_cost")" \
          --arg prescription "$prescription" \
          '{pattern:$pattern,pattern_id:$pattern_id,severity:$severity,evidence:$evidence,cost_impact:$cost_impact,prescription:$prescription}')"
        return 0
      fi
    fi
  fi

  # --- Sub-detector B: Exploration spiral ---
  # Find runs of 10+ consecutive read-only tool calls (no writes/edits)

  local tool_seq
  tool_seq=$(jq -r '
    [ .[] | select(.type == "message" and .message.role == "assistant") ]
    | to_entries[]
    | .value.message as $m
    | ($m.usage.cost.total // 0) as $cost
    | ($m.content // [])[] | select(.type == "toolCall")
    | [.name, ($cost | tostring)]
    | join("\t")
  ' <(jq -s '.' "$JSONL" 2>/dev/null) 2>/dev/null) || return 0

  if [[ -z "$tool_seq" ]]; then return 0; fi

  # Classify each tool as read-only or write
  local best_run=0
  local best_cost=0
  local run=0
  local run_cost=0

  while IFS=$'\t' read -r tool_name cost; do
    # Write tools and exec break the run (exec is ambiguous — could be a build/test)
    if echo "$tool_name" | grep -qiE '^(write|edit|Write|Edit|exec)$'; then
      if [[ "$run" -gt "$best_run" ]]; then
        best_run=$run
        best_cost=$run_cost
      fi
      run=0
      run_cost=0
    else
      # Read-only tools extend the run
      if echo "$tool_name" | grep -qiE '^(read|Read|Glob|glob|Grep|grep|search_web|web_fetch|browser_navigate|Search)$'; then
        run=$((run + 1))
        run_cost=$(echo "$run_cost + $cost" | bc 2>/dev/null || echo "$run_cost")
      fi
      # Unknown tools are ignored (don't extend or break)
    fi
  done <<< "$tool_seq"

  # Check final run
  if [[ "$run" -gt "$best_run" ]]; then
    best_run=$run
    best_cost=$run_cost
  fi

  if [[ "$best_run" -lt 10 ]]; then return 0; fi

  local best_cost_rounded
  best_cost_rounded=$(printf "%.2f" "$best_cost")
  local total_turns
  total_turns=$(echo "$tool_seq" | wc -l | tr -d ' ')
  local evidence="The agent made ${best_run} consecutive read/search tool calls without writing or editing a single file — an exploration spiral. It spent \$${best_cost_rounded} reading without making any forward progress. This is ${best_run} of ${total_turns} total tool calls in the session spent purely on exploration."
  local prescription="Agent read/searched ${best_run} times in a row without writing or editing anything, burning \$${best_cost_rounded}. It was stuck exploring instead of making progress. Tell the agent to stop reading and start implementing after gathering initial context, or use a sub-agent for the research phase."

  add_finding "$(jq -nc \
    --arg pattern "task-drift" \
    --argjson pattern_id 12 \
    --arg severity "medium" \
    --arg evidence "$evidence" \
    --argjson cost_impact "$(printf '%.6f' "$best_cost")" \
    --arg prescription "$prescription" \
    '{pattern:$pattern,pattern_id:$pattern_id,severity:$severity,evidence:$evidence,cost_impact:$cost_impact,prescription:$prescription}')"
}

# ---------------------------------------------------------------------------
# Detector 13: detect_unbounded_walk
# ---------------------------------------------------------------------------
detect_unbounded_walk() {
  echo "[diagnose] running detect_unbounded_walk..." >&2

  # --- Sub-detector A: Repeated unscoped recursive commands ---
  # Extract exec tool calls and their commands
  local exec_cmds
  exec_cmds=$(jq -r '
    to_entries
    | map(select(.value.type == "message" and .value.message.role == "assistant"))
    | to_entries
    | .[]
    | . as $outer
    | .value.value.message.content[]?
    | select(.type == "toolCall" and .name == "exec")
    | [
        ($outer.key | tostring),
        (.input.command // ""),
        ($outer.value.value.message.usage.cost.total // 0 | tostring)
      ]
    | join("\t")
  ' <(jq -s '.' "$JSONL" 2>/dev/null) 2>/dev/null) || return 0

  local unscoped_count=0
  local unscoped_cmds=""
  local unscoped_cost=0
  local first_turn=0
  local last_turn=0

  if [[ -n "$exec_cmds" ]]; then
    while IFS=$'\t' read -r turn_idx cmd cost; do
      [[ -z "$cmd" ]] && continue

      # Check if command contains a recursive filesystem operation
      local is_recursive=0
      if echo "$cmd" | grep -qE '\bfind\b'; then
        is_recursive=1
      elif echo "$cmd" | grep -qE '\bgrep\s+(-[a-zA-Z]*r|-[a-zA-Z]*R|--include)\b'; then
        is_recursive=1
      elif echo "$cmd" | grep -qE '\bls\s+(-[a-zA-Z]*R)\b'; then
        is_recursive=1
      elif echo "$cmd" | grep -qE '\btree\b'; then
        is_recursive=1
      elif echo "$cmd" | grep -qE '\bdu\s+(-[a-zA-Z]*a)\b'; then
        is_recursive=1
      fi

      if [[ "$is_recursive" -eq 0 ]]; then continue; fi

      # Check for scope limiters that make it safe
      local is_scoped=0
      if echo "$cmd" | grep -qE '(-maxdepth|-L\s+[0-9])'; then
        is_scoped=1
      elif echo "$cmd" | grep -qE '\|\s*(head|tail|wc)\b'; then
        is_scoped=1
      fi

      if [[ "$is_scoped" -eq 0 ]]; then
        unscoped_count=$((unscoped_count + 1))
        if [[ "$unscoped_count" -eq 1 ]]; then
          first_turn=$turn_idx
        fi
        last_turn=$turn_idx
        unscoped_cost=$(echo "$unscoped_cost + $cost" | bc 2>/dev/null || echo "$unscoped_cost")
        local cmd_short
        cmd_short=$(echo "$cmd" | head -c 80)
        if [[ -n "$unscoped_cmds" ]]; then
          unscoped_cmds="${unscoped_cmds}, \`${cmd_short}\`"
        else
          unscoped_cmds="\`${cmd_short}\`"
        fi
      fi
    done <<< "$exec_cmds"
  fi

  # --- Sub-detector B: Exponential output growth ---
  # Track toolResult text lengths across consecutive turns
  local result_lengths
  result_lengths=$(jq -r '
    .[]
    | select(.type == "message" and .message.role == "toolResult")
    | [(.message.content[]? | select(.type == "text") | .text | length)] | add // 0
  ' <(jq -s '.' "$JSONL" 2>/dev/null) 2>/dev/null) || result_lengths=""

  local doubling_run=0
  local best_doubling_run=0
  local prev_len=0

  if [[ -n "$result_lengths" ]]; then
    while read -r len; do
      if [[ "$prev_len" -gt 0 && "$len" -ge $((prev_len * 2)) ]]; then
        doubling_run=$((doubling_run + 1))
        if [[ "$doubling_run" -gt "$best_doubling_run" ]]; then
          best_doubling_run=$doubling_run
        fi
      else
        doubling_run=0
      fi
      prev_len=$len
    done <<< "$result_lengths"
  fi

  # --- Combine: either sub-detector triggers ---
  local triggered_a=0
  local triggered_b=0

  if [[ "$unscoped_count" -ge 3 ]]; then
    triggered_a=1
  fi
  if [[ "$best_doubling_run" -ge 3 ]]; then
    triggered_b=1
  fi

  if [[ "$triggered_a" -eq 0 && "$triggered_b" -eq 0 ]]; then return 0; fi

  local evidence=""
  local prescription=""
  local cost_impact=0

  if [[ "$triggered_a" -eq 1 && "$triggered_b" -eq 1 ]]; then
    local cost_rounded
    cost_rounded=$(printf "%.2f" "$unscoped_cost")
    evidence="Agent ran ${unscoped_count} unscoped recursive commands (${unscoped_cmds}) across turns $((first_turn + 1))–$((last_turn + 1)), and tool output sizes doubled ${best_doubling_run} consecutive times — an unbounded filesystem walk with exponentially growing output."
    prescription="Agent ran ${unscoped_count} recursive commands without scope limits, burning \$${cost_rounded}. Each successive output was larger than the last. Scope recursive commands with \`-maxdepth\`, target specific directories instead of \`/\`, and pipe to \`| head -50\` to cap output size."
    cost_impact=$unscoped_cost
  elif [[ "$triggered_a" -eq 1 ]]; then
    local cost_rounded
    cost_rounded=$(printf "%.2f" "$unscoped_cost")
    evidence="Agent ran ${unscoped_count} unscoped recursive commands (${unscoped_cmds}) across turns $((first_turn + 1))–$((last_turn + 1)) without \`-maxdepth\` or output limits — an unbounded filesystem walk."
    prescription="Agent ran ${unscoped_count} recursive commands without scope limits, burning \$${cost_rounded}. Use \`-maxdepth\` with \`find\`, target specific directories instead of \`/\`, and pipe to \`| head -50\` to cap output size."
    cost_impact=$unscoped_cost
  else
    evidence="Tool output sizes doubled ${best_doubling_run} consecutive times — exponential output growth indicating an unbounded operation."
    prescription="Tool output kept doubling (${best_doubling_run} consecutive doublings). The agent is reading progressively larger results without limiting scope. Pipe commands to \`| head\` or \`| tail\`, target specific directories, or use more selective queries."
  fi

  add_finding "$(jq -nc \
    --arg pattern "unbounded-walk" \
    --argjson pattern_id 13 \
    --arg severity "high" \
    --arg evidence "$evidence" \
    --argjson cost_impact "$(printf '%.6f' "$cost_impact")" \
    --arg prescription "$prescription" \
    '{pattern:$pattern,pattern_id:$pattern_id,severity:$severity,evidence:$evidence,cost_impact:$cost_impact,prescription:$prescription}')"
}

# ---------------------------------------------------------------------------
# Detector 14: detect_tool_misuse
# ---------------------------------------------------------------------------
detect_tool_misuse() {
  echo "[diagnose] running detect_tool_misuse..." >&2

  # Extract tool calls in order: turn_index, tool_name, file_path, cost
  # file_path comes from .input.path, .input.file_path, or .input.file
  local tool_seq
  tool_seq=$(jq -r '
    to_entries
    | map(select(.value.type == "message" and .value.message.role == "assistant"))
    | to_entries
    | .[]
    | . as $outer
    | .value.value.message.content[]?
    | select(.type == "toolCall")
    | [
        ($outer.key | tostring),
        .name,
        (.input.path // .input.file_path // .input.file // ""),
        ($outer.value.value.message.usage.cost.total // 0 | tostring)
      ]
    | join("\t")
  ' <(jq -s '.' "$JSONL" 2>/dev/null) 2>/dev/null) || return 0

  if [[ -z "$tool_seq" ]]; then return 0; fi

  # --- Sub-detector A: Redundant file reads ---
  # Track reads per file path, reset count when a write/edit touches the same file.
  # Use awk to process the stream: for each (read|Read) of a file, increment counter.
  # For each (write|Write|edit|Edit) of a file, reset counter. Track the worst offender.

  local worst_read
  worst_read=$(echo "$tool_seq" | awk -F'\t' '
  BEGIN {
    best_file = ""
    best_count = 0
    best_cost = 0
    best_first_turn = 0
    best_last_turn = 0
  }
  {
    turn = $1+0
    tool = $2
    fpath = $3
    cost = $4+0

    if (fpath == "") next

    # Write/edit resets the counter for this file
    if (tool == "write" || tool == "Write" || tool == "edit" || tool == "Edit") {
      delete read_count[fpath]
      delete read_cost[fpath]
      delete read_first[fpath]
      delete read_last[fpath]
      next
    }

    # Read increments the counter
    if (tool == "read" || tool == "Read") {
      read_count[fpath]++
      read_cost[fpath] += cost
      if (read_count[fpath] == 1) read_first[fpath] = turn
      read_last[fpath] = turn

      if (read_count[fpath] > best_count) {
        best_count = read_count[fpath]
        best_file = fpath
        best_cost = read_cost[fpath]
        best_first_turn = read_first[fpath]
        best_last_turn = read_last[fpath]
      }
    }
  }
  END {
    if (best_count >= 3) {
      printf "%s\t%d\t%.6f\t%d\t%d\n", best_file, best_count, best_cost, best_first_turn, best_last_turn
    }
  }
  ')

  # --- Sub-detector B: Duplicate searches ---
  # Track identical Glob/Grep calls (same tool + same pattern/path input)
  local worst_search
  worst_search=$(echo "$tool_seq" | awk -F'\t' '
  BEGIN {
    best_key = ""
    best_count = 0
    best_cost = 0
  }
  {
    tool = $2
    fpath = $3
    cost = $4+0

    if (tool != "Glob" && tool != "glob" && tool != "Grep" && tool != "grep") next

    key = tool "|" fpath
    search_count[key]++
    search_cost[key] += cost

    if (search_count[key] > best_count) {
      best_count = search_count[key]
      best_key = key
      best_cost = search_cost[key]
    }
  }
  END {
    if (best_count >= 3) {
      printf "%s\t%d\t%.6f\n", best_key, best_count, best_cost
    }
  }
  ')

  # --- Combine results ---
  local triggered_a=0
  local triggered_b=0

  if [[ -n "$worst_read" ]]; then
    triggered_a=1
  fi
  if [[ -n "$worst_search" ]]; then
    triggered_b=1
  fi

  if [[ "$triggered_a" -eq 0 && "$triggered_b" -eq 0 ]]; then return 0; fi

  local evidence=""
  local prescription=""
  local cost_impact=0

  if [[ "$triggered_a" -eq 1 ]]; then
    local file_path read_count read_cost first_turn last_turn
    file_path=$(echo "$worst_read" | cut -f1)
    read_count=$(echo "$worst_read" | cut -f2)
    read_cost=$(echo "$worst_read" | cut -f3)
    first_turn=$(echo "$worst_read" | cut -f4)
    last_turn=$(echo "$worst_read" | cut -f5)
    cost_impact=$read_cost

    local cost_rounded
    cost_rounded=$(printf "%.2f" "$read_cost")

    if [[ "$triggered_b" -eq 1 ]]; then
      local search_key search_count search_cost
      search_key=$(echo "$worst_search" | cut -f1)
      search_count=$(echo "$worst_search" | cut -f2)
      search_cost=$(echo "$worst_search" | cut -f3)
      cost_impact=$(echo "$read_cost + $search_cost" | bc 2>/dev/null || echo "$read_cost")
      cost_rounded=$(printf "%.2f" "$cost_impact")

      evidence="\`${file_path}\` was read ${read_count} times (turns $((first_turn + 1))–$((last_turn + 1))) without being edited in between — the agent kept re-reading the same unchanged file. Additionally, \`${search_key}\` was searched ${search_count} times with identical parameters."
      prescription="Agent read \`${file_path}\` ${read_count} times without editing it, wasting \$${cost_rounded}. The file content was identical each time. Store important details from a file read in your working memory instead of re-reading the same file repeatedly."
    else
      evidence="\`${file_path}\` was read ${read_count} times (turns $((first_turn + 1))–$((last_turn + 1))) without being edited in between — the agent kept re-reading the same unchanged file, wasting tokens on content it already had in context."
      prescription="Agent read \`${file_path}\` ${read_count} times without editing it, wasting \$${cost_rounded}. The file content was identical each time. The agent should retain information from previous reads instead of re-reading unchanged files."
    fi
  else
    local search_key search_count search_cost
    search_key=$(echo "$worst_search" | cut -f1)
    search_count=$(echo "$worst_search" | cut -f2)
    search_cost=$(echo "$worst_search" | cut -f3)
    cost_impact=$search_cost

    local cost_rounded
    cost_rounded=$(printf "%.2f" "$search_cost")

    evidence="\`${search_key}\` was searched ${search_count} times with identical parameters — the agent ran the same search query repeatedly."
    prescription="Agent ran the same \`${search_key}\` search ${search_count} times, wasting \$${cost_rounded}. Search results don't change within a session — use the results from the first search instead of repeating it."
  fi

  add_finding "$(jq -nc \
    --arg pattern "tool-misuse" \
    --argjson pattern_id 14 \
    --arg severity "medium" \
    --arg evidence "$evidence" \
    --argjson cost_impact "$(printf '%.6f' "$cost_impact")" \
    --arg prescription "$prescription" \
    '{pattern:$pattern,pattern_id:$pattern_id,severity:$severity,evidence:$evidence,cost_impact:$cost_impact,prescription:$prescription}')"
}

# ---------------------------------------------------------------------------
# Run all detectors
# ---------------------------------------------------------------------------
detect_infinite_retry
detect_non_retryable_retry
detect_tool_as_text
detect_context_exhaustion
detect_subagent_replay
detect_cost_spike
detect_skill_miss
detect_model_routing_waste
detect_cron_accumulation
detect_compaction_damage
detect_workspace_overhead
detect_task_drift
detect_unbounded_walk
detect_tool_misuse

# ---------------------------------------------------------------------------
# Output JSON array
# ---------------------------------------------------------------------------
if [[ ${#FINDINGS[@]} -eq 0 ]]; then
  echo "[]"
else
  printf '%s\n' "${FINDINGS[@]}" | jq -s '.'
fi
