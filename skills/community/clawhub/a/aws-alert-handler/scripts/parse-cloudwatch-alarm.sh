#!/usr/bin/env bash
# parse-cloudwatch-alarm.sh — normalize a CloudWatch alarm event.
#
# Accepts two shapes on stdin:
#   (a) EventBridge envelope: {"source":"aws.cloudwatch","detail-type":"CloudWatch Alarm State Change","detail":{...}}
#   (b) SNS direct:          {"AlarmName":"...","NewStateValue":"ALARM",...}
#
# SNS envelope unwrapping is handled by parse-alert.sh upstream; this script
# assumes the inner payload is already unwrapped.
#
# Severity:
#   CloudWatch alarms do not carry severity inline. This parser emits
#   INFORMATIONAL by default. For explicit severity, tag the alarm with a
#   `severity` tag externally (not readable from the event payload; requires
#   a separate enrichment step the skill intentionally does not perform).
#
# Noise filter:
#   Exits 0 with a skip sentinel for known non-incident alarm patterns.
#   The skill should drop these without invoking triage.
#
# Exit: 0 on success (or skip sentinel), 2 on shape mismatch, 3 on missing jq.

set -euo pipefail

if ! command -v jq >/dev/null 2>&1; then
  echo "parse-cloudwatch-alarm.sh: jq is required but not installed" >&2
  exit 3
fi

raw=$(cat)

# Detect shape.
if echo "$raw" | jq -e '."detail-type" == "CloudWatch Alarm State Change"' >/dev/null 2>&1; then
  shape="eventbridge"
elif echo "$raw" | jq -e '.AlarmName and .NewStateValue' >/dev/null 2>&1; then
  shape="sns-direct"
else
  echo "parse-cloudwatch-alarm.sh: input does not look like a CloudWatch alarm event" >&2
  exit 2
fi

# Region-name → region-code map for SNS-direct shape (uses friendly names).
region_code_from_friendly() {
  case "$1" in
    "US East (N. Virginia)")          echo "us-east-1"       ;;
    "US East (Ohio)")                 echo "us-east-2"       ;;
    "US West (N. California)")        echo "us-west-1"       ;;
    "US West (Oregon)")               echo "us-west-2"       ;;
    "Africa (Cape Town)")             echo "af-south-1"      ;;
    "Asia Pacific (Hong Kong)")       echo "ap-east-1"       ;;
    "Asia Pacific (Hyderabad)")       echo "ap-south-2"      ;;
    "Asia Pacific (Jakarta)")         echo "ap-southeast-3"  ;;
    "Asia Pacific (Malaysia)")        echo "ap-southeast-5"  ;;
    "Asia Pacific (Melbourne)")       echo "ap-southeast-4"  ;;
    "Asia Pacific (Mumbai)")          echo "ap-south-1"      ;;
    "Asia Pacific (Osaka)")           echo "ap-northeast-3"  ;;
    "Asia Pacific (Seoul)")           echo "ap-northeast-2"  ;;
    "Asia Pacific (Singapore)")       echo "ap-southeast-1"  ;;
    "Asia Pacific (Sydney)")          echo "ap-southeast-2"  ;;
    "Asia Pacific (Thailand)")        echo "ap-southeast-7"  ;;
    "Asia Pacific (Tokyo)")           echo "ap-northeast-1"  ;;
    "Canada (Central)")               echo "ca-central-1"    ;;
    "Canada West (Calgary)")          echo "ca-west-1"       ;;
    "China (Beijing)")                echo "cn-north-1"      ;;
    "China (Ningxia)")                echo "cn-northwest-1"  ;;
    "Europe (Frankfurt)"|"EU (Frankfurt)")     echo "eu-central-1" ;;
    "Europe (Ireland)"|"EU (Ireland)")         echo "eu-west-1"    ;;
    "Europe (London)"|"EU (London)")           echo "eu-west-2"    ;;
    "Europe (Milan)"|"EU (Milan)")             echo "eu-south-1"   ;;
    "Europe (Paris)"|"EU (Paris)")             echo "eu-west-3"    ;;
    "Europe (Spain)")                          echo "eu-south-2"   ;;
    "Europe (Stockholm)"|"EU (Stockholm)")     echo "eu-north-1"   ;;
    "Europe (Zurich)")                         echo "eu-central-2" ;;
    "Israel (Tel Aviv)")              echo "il-central-1"    ;;
    "Mexico (Central)")               echo "mx-central-1"    ;;
    "Middle East (Bahrain)")          echo "me-south-1"      ;;
    "Middle East (UAE)")              echo "me-central-1"    ;;
    "South America (Sao Paulo)")      echo "sa-east-1"       ;;
    "AWS GovCloud (US-East)")         echo "us-gov-east-1"   ;;
    "AWS GovCloud (US-West)")         echo "us-gov-west-1"   ;;
    *)                                echo "$1"              ;;
  esac
}

# Extract fields based on shape.
if [ "$shape" = "eventbridge" ]; then
  alarm_name=$(echo "$raw" | jq -r '.detail.alarmName // ""')
  state=$(echo "$raw" | jq -r '.detail.state.value // "ALARM"')
  reason=$(echo "$raw" | jq -r '.detail.state.reason // ""')
  account_id=$(echo "$raw" | jq -r '.account // ""')
  region=$(echo "$raw" | jq -r '.region // ""')
  detected_at=$(echo "$raw" | jq -r '.time // .detail.state.timestamp // ""')
  resource_ids=$(echo "$raw" | jq -c '.resources // []')
else
  alarm_name=$(echo "$raw" | jq -r '.AlarmName // ""')
  state=$(echo "$raw" | jq -r '.NewStateValue // "ALARM"')
  reason=$(echo "$raw" | jq -r '.NewStateReason // ""')
  account_id=$(echo "$raw" | jq -r '.AWSAccountId // ""')
  region_raw=$(echo "$raw" | jq -r '.Region // ""')
  region=$(region_code_from_friendly "$region_raw")
  detected_at=$(echo "$raw" | jq -r '.StateChangeTime // ""')
  if [ -n "$account_id" ] && [ -n "$region" ] && [ -n "$alarm_name" ]; then
    resource_ids=$(jq -cn --arg arn "arn:aws:cloudwatch:${region}:${account_id}:alarm:${alarm_name}" '[$arn]')
  else
    resource_ids="[]"
  fi
fi

# Noise filter: skip known non-incident alarm patterns.
# These fire routinely on normal workload behavior and should not trigger
# incident triage. Patterns are conservative — add new ones as identified.
skip_reason=""
case "$alarm_name" in
  TargetTracking-*-AlarmHigh-*|TargetTracking-*-AlarmLow-*)
    skip_reason="ecs-target-tracking-autoscaling" ;;
  awseb-*-AWSEBCloudwatchAlarmHigh-*|awseb-*-AWSEBCloudwatchAlarmLow-*)
    skip_reason="elastic-beanstalk-default-alarm" ;;
  AutoScaling-*-AlarmHigh-*|AutoScaling-*-AlarmLow-*)
    skip_reason="ec2-autoscaling-policy" ;;
  CloudWatchSynthetics-*)
    # Canaries run on a schedule and emit state changes frequently.
    # Canary failures are usually monitored via the Synthetics dashboard
    # or a separate alerting path rather than routed into incident triage.
    skip_reason="synthetics-canary-state-change" ;;
esac

if [ -n "$skip_reason" ]; then
  jq -n \
    --arg alarm_name "$alarm_name" \
    --arg reason "$skip_reason" \
    '{
      skip: "non-incident-alarm",
      reason: $reason,
      alarm_name: $alarm_name,
      note: "Routine autoscaling or operational-machinery alarm. Skill should not invoke incident-triage for this event."
    }'
  exit 0
fi

# Severity: default INFORMATIONAL. Explicit severity must come from tags,
# which are not in the event payload. Upstream enrichment can override.
severity="INFORMATIONAL"

title="CloudWatch alarm: ${alarm_name} → ${state}"
summary="${reason:-(no reason provided)}"

# Console URL.
if [ -n "$region" ] && [ -n "$alarm_name" ]; then
  encoded_name=$(printf '%s' "$alarm_name" | jq -sRr @uri)
  console_url="https://console.aws.amazon.com/cloudwatch/home?region=${region}#alarmsV2:alarm/${encoded_name}"
else
  console_url=""
fi

jq -n \
  --arg source "cloudwatch-alarm" \
  --arg source_subtype "" \
  --arg severity "$severity" \
  --arg title "$title" \
  --arg summary "$summary" \
  --arg account_id "$account_id" \
  --arg region "$region" \
  --argjson resource_ids "$resource_ids" \
  --arg state "$state" \
  --arg detected_at "$detected_at" \
  --arg console_url "$console_url" \
  --argjson raw "$(echo "$raw" | jq -c .)" \
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
