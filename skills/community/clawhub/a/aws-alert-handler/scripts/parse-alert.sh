#!/usr/bin/env bash
# parse-alert.sh — unified entry point. Reads AWS alert JSON from stdin,
# auto-detects the format, unwraps SNS envelopes, and dispatches to the
# appropriate parser.
#
# Handles:
#   - Security Hub ASFF finding (single or {Findings:[...]} envelope)
#   - CloudWatch alarm state change (EventBridge or SNS-direct shape)
#   - Inspector v2 finding (EventBridge envelope, raw API finding, or
#     {findings:[...]} list response)
#   - Any of the above wrapped in an SNS {Type:"Notification",Message:"..."}
#     envelope — unwrapped automatically
#
# Dispatch order: most-specific-first. The format shapes are mutually
# exclusive (different required fields), so order is for clarity, not
# correctness.
#
# Exit codes:
#   0  — parsed successfully; stdout is normalized JSON
#   2  — input did not match any known format; stderr has guidance
#   3  — missing required tool (jq)
#   4  — SNS SubscriptionConfirmation (not an alert; caller should confirm)
#  10  — non-incident alarm skipped by the noise filter; stdout is the skip
#         sentinel JSON. Distinct from 0 so callers can distinguish skip
#         from success without parsing JSON.

set -euo pipefail

if ! command -v jq >/dev/null 2>&1; then
  echo "parse-alert.sh: jq is required but not installed" >&2
  exit 3
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
raw=$(cat)

# SNS envelope handling.
sns_type=$(echo "$raw" | jq -r '.Type // empty' 2>/dev/null || true)
case "$sns_type" in
  "SubscriptionConfirmation"|"UnsubscribeConfirmation")
    subscribe_url=$(echo "$raw" | jq -r '.SubscribeURL // empty')
    echo "parse-alert.sh: SNS $sns_type received, not an alert" >&2
    echo "parse-alert.sh: SubscribeURL=$subscribe_url" >&2
    echo "parse-alert.sh: GET that URL to confirm the subscription (or run aws sns confirm-subscription)" >&2
    exit 4
    ;;
  "Notification")
    inner=$(echo "$raw" | jq -r '.Message')
    if ! echo "$inner" | jq -e . >/dev/null 2>&1; then
      echo "parse-alert.sh: SNS Notification .Message is not valid JSON" >&2
      exit 2
    fi
    raw="$inner"
    ;;
esac

# Dispatch. Each branch hands stdin to a format-specific parser and
# propagates its exit code. The CloudWatch parser may emit a skip sentinel
# with exit 10 (via this wrapper's logic below).

parse_and_handle_skip() {
  # Runs the given parser with stdin, passes through its output, and
  # translates the "skip sentinel" case to exit 10.
  local parser="$1"
  local parsed
  parsed=$("$parser") || return $?
  echo "$parsed"
  if echo "$parsed" | jq -e '.skip == "non-incident-alarm"' >/dev/null 2>&1; then
    return 10
  fi
  return 0
}

# ASFF.
if echo "$raw" | jq -e '(.SchemaVersion == "2018-10-08") or (.Findings[0].SchemaVersion == "2018-10-08")' >/dev/null 2>&1; then
  echo "$raw" | parse_and_handle_skip "$SCRIPT_DIR/parse-asff.sh"
  exit $?
fi

# CloudWatch alarm — both shapes dispatch to the same parser.
if echo "$raw" | jq -e '."detail-type" == "CloudWatch Alarm State Change" or (.AlarmName and .NewStateValue)' >/dev/null 2>&1; then
  echo "$raw" | parse_and_handle_skip "$SCRIPT_DIR/parse-cloudwatch-alarm.sh"
  exit $?
fi

# Inspector v2 — three possible shapes (EventBridge envelope, raw finding,
# list-response), all handled by the Inspector parser internally.
if echo "$raw" | jq -e '
  ."detail-type" == "Inspector2 Finding"
  or (.findingArn and .severity and .type)
  or (.findings[0].findingArn and .findings[0].severity and .findings[0].type)
' >/dev/null 2>&1; then
  echo "$raw" | parse_and_handle_skip "$SCRIPT_DIR/parse-inspector2.sh"
  exit $?
fi

echo "parse-alert.sh: payload did not match any known alert shape" >&2
echo "parse-alert.sh: expected one of:" >&2
echo "  - Security Hub ASFF finding or {Findings:[...]} envelope" >&2
echo "  - CloudWatch Alarm State Change (EventBridge envelope or SNS-direct shape)" >&2
echo "  - Inspector v2 finding (EventBridge envelope, raw API finding, or {findings:[...]} list)" >&2
echo "  - SNS Notification envelope wrapping any of the above" >&2
exit 2
