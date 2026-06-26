#!/usr/bin/env bash
set -euo pipefail

VERSION="0.12.0"

# cost-waterfall.sh <path-to-jsonl>
# Outputs per-turn cost breakdown sorted by cost descending.
# Output is a JSON array.

usage() {
  cat <<EOF
Usage: cost-waterfall.sh [--help|--version] <path-to-jsonl>

Description:
  Outputs per-turn cost breakdown sorted by cost descending.

Options:
  --help      Show this help message and exit
  --version   Show version and exit

Example:
  cost-waterfall.sh session.jsonl | jq '.[0:5]'
EOF
}

check_deps() {
  for dep in jq awk; do
    if ! command -v "$dep" >/dev/null 2>&1; then
      echo "Error: required dependency '$dep' not found. Install it and retry." >&2
      exit 1
    fi
  done
}

if [ $# -ge 1 ]; then
  case "$1" in
    --help) usage; exit 0 ;;
    --version) echo "$VERSION"; exit 0 ;;
  esac
fi

check_deps

if [ $# -lt 1 ]; then
  echo "Usage: cost-waterfall.sh <path-to-jsonl>" >&2
  exit 1
fi

JSONL="$1"

if [ ! -f "$JSONL" ]; then
  echo "Error: file not found: $JSONL" >&2
  exit 1
fi

jq -s '
  [.[] | select(.type == "message")] as $messages |

  # For each turn, capture context about what preceded it (tool results)
  [$messages | to_entries[] |
    .key as $idx |
    .value as $msg |
    select($msg.message.role == "assistant" and $msg.message.usage != null and ($msg.message.usage.cost.total // 0) > 0) |

    # Identify tool used in this turn
    ([$msg.message.content[]? | select(.type == "toolCall") | .name] | first // null) as $tool |

    # Look at the preceding toolResult for cause identification
    ($messages[$idx - 1] // null) as $prev_msg |
    (if $prev_msg != null and $prev_msg.message.role == "toolResult"
     then
       ($prev_msg.message.content[]? | select(.type == "text") | .text | length) // 0
     else 0 end) as $prev_result_len |

    # Compute cause annotation
    ($msg.message.usage.inputTokens // 0) as $in_tokens |
    ($msg.message.usage.outputTokens // 0) as $out_tokens |
    ($msg.message.usage.cost.total // 0) as $cost |

    (if $prev_result_len > 4000 then
      "tool result (" + ($prev_result_len | tostring) + " chars / ~" + (($prev_result_len / 4 | floor) | tostring) + " tokens) in previous toolResult inflated context"
     elif $in_tokens > 80000 then
      "very large context (" + ($in_tokens | tostring) + " input tokens) — accumulated conversation or large tool outputs"
     elif $in_tokens > 50000 then
      "large context (" + ($in_tokens | tostring) + " input tokens) — consider compaction"
     elif $out_tokens > 2000 then
      "verbose output (" + ($out_tokens | tostring) + " output tokens)"
     elif $tool != null then
      "tool call: " + $tool
     else
      "standard turn"
     end) as $cause |

    {
      turn: ($idx + 1),
      role: $msg.message.role,
      cost: $cost,
      input_tokens: $in_tokens,
      output_tokens: $out_tokens,
      tool: $tool,
      cause: $cause,
      timestamp: $msg.timestamp
    }
  ] | sort_by(-.cost)
' "$JSONL"
