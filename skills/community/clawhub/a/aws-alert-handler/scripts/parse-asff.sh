#!/usr/bin/env bash
# parse-asff.sh — normalize a Security Hub ASFF finding from stdin to stdout.
#
# Accepts:
#   - Single ASFF finding:  {"SchemaVersion":"2018-10-08", ...}
#   - Findings envelope:    {"Findings":[{...}]}  — emits the first finding
#
# SNS envelope unwrapping is handled by parse-alert.sh upstream; this script
# assumes the inner payload is already unwrapped.
#
# Multiple findings caveat: when the envelope contains >1 finding, only the
# first is emitted. EventBridge rules that batch findings are unusual; the
# default configuration delivers one-at-a-time. If you expect batches, split
# them before invoking this parser.
#
# Exit: 0 on success, 2 on shape mismatch, 3 on missing required field.

set -euo pipefail

if ! command -v jq >/dev/null 2>&1; then
  echo "parse-asff.sh: jq is required but not installed" >&2
  exit 3
fi

raw=$(cat)

if ! echo "$raw" | jq -e '(.SchemaVersion == "2018-10-08") or (.Findings[0].SchemaVersion == "2018-10-08")' >/dev/null 2>&1; then
  echo "parse-asff.sh: input does not look like ASFF (missing SchemaVersion 2018-10-08)" >&2
  exit 2
fi

if echo "$raw" | jq -e 'has("Findings")' >/dev/null 2>&1; then
  n=$(echo "$raw" | jq -r '.Findings | length')
  if [ "$n" -gt 1 ]; then
    echo "parse-asff.sh: envelope contains $n findings; emitting first only (others preserved in raw)" >&2
  fi
  finding=$(echo "$raw" | jq -c '.Findings[0]')
else
  finding=$(echo "$raw" | jq -c '.')
fi

product_arn=$(echo "$finding" | jq -r '.ProductArn // ""')
source_subtype=$(case "$product_arn" in
  *"product/aws/inspector"*)         echo "inspector"         ;;
  *"product/aws/guardduty"*)         echo "guardduty"         ;;
  *"product/aws/macie"*)             echo "macie"             ;;
  *"product/aws/access-analyzer"*)   echo "access-analyzer"   ;;
  *"product/aws/config"*)            echo "config"            ;;
  *"product/aws/firewall-manager"*)  echo "firewall-manager"  ;;
  *"product/aws/health"*)            echo "health"            ;;
  *"product/aws/ssm-patch-manager"*) echo "ssm-patch"         ;;
  *)                                 echo "other"             ;;
esac)

severity=$(echo "$finding" | jq -r '
  if .Severity.Label then .Severity.Label
  elif .Severity.Normalized then
    (.Severity.Normalized | if . >= 90 then "CRITICAL"
      elif . >= 70 then "HIGH"
      elif . >= 40 then "MEDIUM"
      elif . >= 1 then "LOW"
      else "INFORMATIONAL" end)
  else "INFORMATIONAL"
  end')

account_id=$(echo "$finding" | jq -r '.AwsAccountId // empty')
if [ -z "$account_id" ]; then
  echo "parse-asff.sh: missing AwsAccountId" >&2
  exit 3
fi

region=$(echo "$finding" | jq -r '.Region // .Resources[0].Region // empty')
title=$(echo "$finding" | jq -r '.Title // "(no title)"')

# Summary: ASFF Description can be long (1k+ chars). Truncate to 500 to
# keep normalized output tidy; full text remains in `raw`.
full_description=$(echo "$finding" | jq -r '.Description // .Title // "(no description)"')
summary=$(printf '%s' "$full_description" | tr '\n' ' ' | tr -s ' ' | cut -c1-500)
[ -z "$summary" ] && summary="$full_description"

detected_at=$(echo "$finding" | jq -r '.CreatedAt // .UpdatedAt // empty')

# Console URL: prefer the finding's SourceUrl; otherwise construct a
# Security Hub console link from the finding id. The search-param URL
# format is current as of 2026-04; AWS may change the console URL shape.
finding_id=$(echo "$finding" | jq -r '.Id // ""')
source_url=$(echo "$finding" | jq -r '.SourceUrl // empty')
if [ -n "$source_url" ]; then
  console_url="$source_url"
elif [ -n "$finding_id" ] && [ -n "$region" ]; then
  encoded_id=$(printf '%s' "$finding_id" | jq -sRr @uri)
  console_url="https://console.aws.amazon.com/securityhub/home?region=${region}#/findings?search=Id%3D${encoded_id}"
else
  console_url=""
fi

# Resource IDs: all non-empty ones (ASFF typically has 1-few).
resource_ids=$(echo "$finding" | jq -c '[.Resources[]?.Id // empty] | map(select(. != ""))')

jq -n \
  --arg source "security-hub" \
  --arg source_subtype "$source_subtype" \
  --arg severity "$severity" \
  --arg title "$title" \
  --arg summary "$summary" \
  --arg account_id "$account_id" \
  --arg region "$region" \
  --argjson resource_ids "$resource_ids" \
  --arg state "ACTIVE" \
  --arg detected_at "$detected_at" \
  --arg console_url "$console_url" \
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
  }'
