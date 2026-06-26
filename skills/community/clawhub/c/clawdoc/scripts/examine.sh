#!/usr/bin/env bash
set -euo pipefail

VERSION="0.12.0"

# examine.sh <path-to-jsonl>
# Reads one JSONL session file, outputs a JSON summary to stdout.

usage() {
  cat <<EOF
Usage: examine.sh [--help|--version] <path-to-jsonl>

Description:
  Reads one JSONL session file, outputs a JSON summary to stdout.

Options:
  --help      Show this help message and exit
  --version   Show version and exit

Example:
  examine.sh ~/.openclaw/agents/main/sessions/abc123.jsonl
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
  echo "Usage: examine.sh <path-to-jsonl>" >&2
  exit 1
fi

JSONL="$1"

if [ ! -f "$JSONL" ]; then
  echo "Error: file not found: $JSONL" >&2
  exit 1
fi

jq -s '
  # Extract session metadata from first line
  (.[0] | select(.type == "session")) as $meta |

  # All message lines
  [.[] | select(.type == "message")] as $messages |

  # Assistant messages with usage
  [$messages[] | select(.message.role == "assistant" and .message.usage != null)] as $assistant_msgs |

  # Total cost
  ($assistant_msgs | map(.message.usage.cost.total // 0) | add // 0) as $total_cost |

  # Total input tokens
  ($assistant_msgs | map(.message.usage.inputTokens // 0) | add // 0) as $total_input |

  # Total output tokens
  ($assistant_msgs | map(.message.usage.outputTokens // 0) | add // 0) as $total_output |

  # Peak input tokens
  ($assistant_msgs | map(.message.usage.inputTokens // 0) | max // 0) as $peak_input |

  # Context limit (from usage contextTokens if present, else 128000)
  ($assistant_msgs | map(.message.usage.contextTokens // 0) | max // 0) as $ctx_raw |
  (if $ctx_raw > 0 then $ctx_raw else 128000 end) as $context_limit |

  # Turn count (all message lines)
  ($messages | length) as $turns |

  # Timestamps for duration
  ([.[] | select(.timestamp != null) | .timestamp] | first) as $first_ts |
  ([.[] | select(.timestamp != null) | .timestamp] | last) as $last_ts |

  # Duration in seconds (strip milliseconds for strptime)
  (try
    (($last_ts | gsub("\\.[0-9]+Z$"; "Z") | strptime("%Y-%m-%dT%H:%M:%SZ") | mktime) -
     ($first_ts | gsub("\\.[0-9]+Z$"; "Z") | strptime("%Y-%m-%dT%H:%M:%SZ") | mktime))
   catch 0) as $duration |

  # Tool call counts by tool name
  ([.[] | select(.type == "message") | .message.content[]? | select(.type == "toolCall") | .name]
   | group_by(.) | map({(.[0]): length}) | add // {}) as $tool_calls |

  # Error count in toolResult messages
  ([.[] | select(.type == "message" and .message.role == "toolResult")
    | .message.content[]? | select(.type == "text") | .text
    | test("(?i)(error|fail|denied|timeout|not found|missing|exception)")]
   | map(select(.)) | length) as $error_count |

  # Turns timeline
  ([$messages[] | . as $line |
    {
      timestamp: $line.timestamp,
      role: $line.message.role,
      input_tokens: ($line.message.usage.inputTokens // 0),
      output_tokens: ($line.message.usage.outputTokens // 0),
      cost: ($line.message.usage.cost.total // 0),
      tool: ([$line.message.content[]? | select(.type == "toolCall") | .name] | first // null)
    }
  ] | to_entries | map(.value + {turn: (.key + 1)})) as $timeline |

  {
    sessionId: ($meta.sessionId // "unknown"),
    agentId: ($meta.agentId // "unknown"),
    model: ($meta.model // "unknown"),
    sessionKey: ($meta.sessionKey // ""),
    turns: $turns,
    duration_seconds: $duration,
    total_cost: $total_cost,
    total_input_tokens: $total_input,
    total_output_tokens: $total_output,
    peak_input_tokens: $peak_input,
    context_limit: $context_limit,
    tool_calls: $tool_calls,
    error_count: $error_count,
    turns_timeline: $timeline
  }
' "$JSONL"
