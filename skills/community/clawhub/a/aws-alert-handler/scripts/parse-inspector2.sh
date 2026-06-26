#!/usr/bin/env bash
# parse-inspector2.sh — normalize an Amazon Inspector v2 finding.
#
# Accepts three shapes on stdin:
#   (a) EventBridge envelope: {"source":"aws.inspector2","detail-type":"Inspector2 Finding",
#                               "region":"...", "time":"...", "detail":{...}}
#   (b) Single finding (raw API format): {"findingArn":"...","severity":"HIGH",...}
#   (c) API list response: {"findings":[{...},...]} — first finding emitted (with a stderr
#                           warning when the batch has >1 finding)
#
# SNS envelope unwrapping is handled by parse-alert.sh upstream.
#
# Output: normalized JSON per the skill's shape. Includes `inspector_score`
# (CVSS-derived 0.0-10.0) as an extra field when present — useful for
# threshold-based downstream routing beyond the categorical severity label.
#
# Exit: 0 on success, 2 on shape mismatch, 3 on missing jq or required field.

set -euo pipefail

if ! command -v jq >/dev/null 2>&1; then
  echo "parse-inspector2.sh: jq is required but not installed" >&2
  exit 3
fi

raw=$(cat)

# Capture outer EventBridge context before unwrapping (may fall back to resource-local values later).
outer_region=$(echo "$raw" | jq -r 'select(."detail-type" == "Inspector2 Finding") | .region // empty' 2>/dev/null || true)
outer_time=$(echo "$raw" | jq -r 'select(."detail-type" == "Inspector2 Finding") | .time // empty' 2>/dev/null || true)

# Unwrap EventBridge envelope; handle list-response with a warning when batched.
if echo "$raw" | jq -e '."detail-type" == "Inspector2 Finding"' >/dev/null 2>&1; then
  finding=$(echo "$raw" | jq -c '.detail')
elif echo "$raw" | jq -e 'has("findings")' >/dev/null 2>&1; then
  n=$(echo "$raw" | jq -r '.findings | length')
  if [ "$n" -gt 1 ]; then
    echo "parse-inspector2.sh: list response has $n findings; emitting first only (others preserved in raw)" >&2
  fi
  finding=$(echo "$raw" | jq -c '.findings[0]')
else
  finding=$(echo "$raw" | jq -c '.')
fi

# Validate.
if ! echo "$finding" | jq -e 'has("findingArn") and has("severity") and has("type")' >/dev/null 2>&1; then
  echo "parse-inspector2.sh: input does not look like an Inspector v2 finding (missing findingArn/severity/type)" >&2
  exit 2
fi

# Severity: Inspector labels are already CRITICAL/HIGH/MEDIUM/LOW/INFORMATIONAL.
# UNTRIAGED → INFORMATIONAL (not a real signal until scored).
raw_severity=$(echo "$finding" | jq -r '.severity // "INFORMATIONAL"')
case "$raw_severity" in
  CRITICAL|HIGH|MEDIUM|LOW|INFORMATIONAL) severity="$raw_severity" ;;
  UNTRIAGED) severity="INFORMATIONAL" ;;
  *)         severity="INFORMATIONAL" ;;
esac

# Source subtype: lowercase the Inspector type directly (no redundant prefix;
# `source` already carries "inspector2").
finding_type=$(echo "$finding" | jq -r '.type // ""')
source_subtype=$(printf '%s' "$finding_type" | tr '[:upper:]_' '[:lower:]-')
[ -z "$source_subtype" ] && source_subtype="unknown"

account_id=$(echo "$finding" | jq -r '.awsAccountId // empty')
if [ -z "$account_id" ]; then
  echo "parse-inspector2.sh: missing awsAccountId" >&2
  exit 3
fi

title=$(echo "$finding" | jq -r '.title // "(no title)"')

# Summary: description can be multi-paragraph. Take first 500 chars after
# collapsing whitespace — portable across awk implementations.
full_description=$(echo "$finding" | jq -r '.description // .title // "(no description)"')
summary=$(printf '%s' "$full_description" | tr '\n' ' ' | tr -s ' ' | cut -c1-500)
[ -z "$summary" ] && summary="$full_description"

# Region: prefer finding's first resource, fall back to EventBridge outer region.
region=$(echo "$finding" | jq -r '.resources[0].region // empty')
[ -z "$region" ] && region="$outer_region"

# Resource IDs: all of them.
resource_ids=$(echo "$finding" | jq -c '[.resources[]?.id // empty] | map(select(. != ""))')

# State: ACTIVE / SUPPRESSED / CLOSED in the Inspector world.
inspector_status=$(echo "$finding" | jq -r '.status // "ACTIVE"')
case "$inspector_status" in
  ACTIVE)              state="ACTIVE"   ;;
  SUPPRESSED|CLOSED)   state="RESOLVED" ;;
  *)                   state="$inspector_status" ;;
esac

# Detected at: prefer finding's firstObservedAt, fall back to EventBridge time.
detected_at=$(echo "$finding" | jq -r '.firstObservedAt // .updatedAt // empty')
[ -z "$detected_at" ] && detected_at="$outer_time"

# Inspector score (CVSS-derived); optional field, emit as `inspector_score`.
inspector_score=$(echo "$finding" | jq -r '.inspectorScore // empty')

# Console URL. The search-param URL format here is current as of 2026-04;
# AWS may change it — fall back to the generic findings list if we can't
# construct a deep link.
finding_arn=$(echo "$finding" | jq -r '.findingArn // ""')
if [ -n "$region" ] && [ -n "$finding_arn" ]; then
  encoded_arn=$(printf '%s' "$finding_arn" | jq -sRr @uri)
  console_url="https://console.aws.amazon.com/inspector/v2/home?region=${region}#/findings/all?search=%7B%22findingArn%22%3A%5B%22${encoded_arn}%22%5D%7D"
elif [ -n "$region" ]; then
  console_url="https://console.aws.amazon.com/inspector/v2/home?region=${region}#/findings/all"
else
  console_url="https://console.aws.amazon.com/inspector/v2/home"
fi

jq -n \
  --arg source "inspector2" \
  --arg source_subtype "$source_subtype" \
  --arg severity "$severity" \
  --arg title "$title" \
  --arg summary "$summary" \
  --arg account_id "$account_id" \
  --arg region "$region" \
  --argjson resource_ids "$resource_ids" \
  --arg state "$state" \
  --arg detected_at "$detected_at" \
  --arg console_url "$console_url" \
  --arg inspector_score "$inspector_score" \
  --argjson raw "$finding" \
  '{
    source: $source,
    source_subtype: $source_subtype,
    severity: $severity,
    title: $title,
    summary: $summary,
    account_id: $account_id,
    region: $region,
    resource_ids: $resource_ids,
    state: $state,
    detected_at: $detected_at,
    console_url: $console_url,
    raw: $raw
  } + (if $inspector_score != "" then {inspector_score: ($inspector_score | tonumber)} else {} end)'
