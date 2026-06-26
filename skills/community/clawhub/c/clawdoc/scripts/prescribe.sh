#!/usr/bin/env bash
set -euo pipefail

VERSION="0.12.0"

# prescribe.sh <diagnose-json-output>
# Takes diagnose.sh output (file path or stdin), formats into full markdown diagnosis report.
# If .learnings/ directory exists, also appends findings to .learnings/LEARNINGS.md.
# Output is formatted text (not JSON).

usage() {
  cat <<EOF
Usage: prescribe.sh [--help|--version] [diagnose-json-file]
       diagnose.sh session.jsonl | prescribe.sh

Description:
  Formats diagnose.sh JSON output into a markdown diagnosis report.

Options:
  --help      Show this help message and exit
  --version   Show version and exit

Example:
  diagnose.sh session.jsonl 2>/dev/null | prescribe.sh
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

INPUT=""

if [ $# -ge 1 ] && [ -f "$1" ]; then
  INPUT=$(cat "$1")
elif [ $# -ge 1 ]; then
  # Treat argument as JSON string directly
  INPUT="$1"
else
  # Read from stdin
  INPUT=$(cat)
fi

if [ -z "$INPUT" ]; then
  echo "Error: no input provided. Pass diagnose.sh JSON output as file, argument, or stdin." >&2
  exit 1
fi

# Validate it's a JSON array
if ! echo "$INPUT" | jq -e 'if type == "array" then true else error("not an array") end' >/dev/null 2>&1; then
  echo "Error: input is not a valid JSON array." >&2
  exit 1
fi

NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u)
TODAY=$(date -u +%Y-%m-%d 2>/dev/null || echo "today")

FINDING_COUNT=$(echo "$INPUT" | jq 'length')
TOTAL_IMPACT=$(echo "$INPUT" | jq '[.[].cost_impact // 0] | add // 0')

# Severity counts
CRITICAL_COUNT=$(echo "$INPUT" | jq '[.[] | select(.severity == "critical")] | length')
HIGH_COUNT=$(echo "$INPUT" | jq '[.[] | select(.severity == "high")] | length')
MEDIUM_COUNT=$(echo "$INPUT" | jq '[.[] | select(.severity == "medium")] | length')
LOW_COUNT=$(echo "$INPUT" | jq '[.[] | select(.severity == "low")] | length')

# Format the report
cat <<EOF
## 🩻 Diagnosis — ${TODAY}

### Patient summary
- Findings: ${FINDING_COUNT}
- Critical: ${CRITICAL_COUNT} | High: ${HIGH_COUNT} | Medium: ${MEDIUM_COUNT} | Low: ${LOW_COUNT}
- Estimated recoverable waste: \$$(printf "%.4f" "$TOTAL_IMPACT")

EOF

if [ "$FINDING_COUNT" -eq 0 ]; then
  cat <<EOF
### Findings

#### 🟢 Healthy
No issues detected. Session looks clean.

### Prescriptions
No action required.
EOF
  exit 0
fi

# Critical findings
if [ "$CRITICAL_COUNT" -gt 0 ]; then
  echo "### Findings"
  echo ""
  echo "#### 🔴 Critical"
  echo ""
  echo "$INPUT" | jq -r '
    .[] | select(.severity == "critical") |
    "**Pattern " + (.pattern_id | tostring) + ": " + .pattern + "**\n" +
    "- Evidence: " + .evidence + "\n" +
    "- Cost impact: $" + (.cost_impact // 0 | tostring) + "\n" +
    "- Prescription: " + .prescription + "\n"
  '
fi

# High findings
if [ "$HIGH_COUNT" -gt 0 ]; then
  if [ "$CRITICAL_COUNT" -eq 0 ]; then
    echo "### Findings"
    echo ""
  fi
  echo "#### 🟠 High"
  echo ""
  echo "$INPUT" | jq -r '
    .[] | select(.severity == "high") |
    "**Pattern " + (.pattern_id | tostring) + ": " + .pattern + "**\n" +
    "- Evidence: " + .evidence + "\n" +
    "- Cost impact: $" + (.cost_impact // 0 | tostring) + "\n" +
    "- Prescription: " + .prescription + "\n"
  '
fi

# Medium findings
if [ "$MEDIUM_COUNT" -gt 0 ]; then
  if [ "$((CRITICAL_COUNT + HIGH_COUNT))" -eq 0 ]; then
    echo "### Findings"
    echo ""
  fi
  echo "#### 🟡 Warning"
  echo ""
  echo "$INPUT" | jq -r '
    .[] | select(.severity == "medium") |
    "**Pattern " + (.pattern_id | tostring) + ": " + .pattern + "**\n" +
    "- Evidence: " + .evidence + "\n" +
    "- Cost impact: $" + (.cost_impact // 0 | tostring) + "\n" +
    "- Prescription: " + .prescription + "\n"
  '
fi

# Low findings
if [ "$LOW_COUNT" -gt 0 ]; then
  if [ "$((CRITICAL_COUNT + HIGH_COUNT + MEDIUM_COUNT))" -eq 0 ]; then
    echo "### Findings"
    echo ""
  fi
  echo "#### 🟢 Low"
  echo ""
  echo "$INPUT" | jq -r '
    .[] | select(.severity == "low") |
    "**Pattern " + (.pattern_id | tostring) + ": " + .pattern + "**\n" +
    "- Evidence: " + .evidence + "\n" +
    "- Cost impact: $" + (.cost_impact // 0 | tostring) + "\n" +
    "- Prescription: " + .prescription + "\n"
  '
fi

# Prescriptions ranked by cost impact
echo ""
echo "### Prescriptions (ranked by cost impact)"
echo ""
echo "$INPUT" | jq -r '
  sort_by(-.cost_impact // 0) | to_entries[] |
  (.key + 1 | tostring) + ". [" +
  (if .value.severity == "critical" then "🔴 CRITICAL"
   elif .value.severity == "high" then "🟠 HIGH"
   elif .value.severity == "medium" then "🟡 MEDIUM"
   else "🟢 LOW" end) + " — Pattern " + (.value.pattern_id | tostring) + "] " +
  .value.prescription
'

# Self-improving-agent integration (opt-in: set CLAWDOC_LEARNINGS=1)
if [ "${CLAWDOC_LEARNINGS:-0}" = "1" ] && [ -d ".learnings" ]; then
  LEARNINGS_FILE=".learnings/LEARNINGS.md"
  echo "" >&2
  echo "[prescribe] .learnings/ directory found — writing to $LEARNINGS_FILE" >&2

  # Get existing DR count to generate next ID
  EXISTING_COUNT=0
  if [ -f "$LEARNINGS_FILE" ]; then
    EXISTING_COUNT=$(grep -c "^### DR-" "$LEARNINGS_FILE" 2>/dev/null || true)
    EXISTING_COUNT=${EXISTING_COUNT:-0}
  fi

  APPENDED=0
  UPDATED=0

  # Process each finding by index
  FINDING_INDICES=$(echo "$INPUT" | jq -r 'to_entries[] | .key')

  for IDX in $FINDING_INDICES; do
    # Build Pattern-Key for this finding (doctor.<pattern_with_underscores>)
    PKEY=$(echo "$INPUT" | jq -r --argjson i "$IDX" '.[$i].pattern | gsub(" "; "_") | gsub("-"; "_") | "doctor." + .')

    # Compute DR number for this entry
    DR_NUM=$(( EXISTING_COUNT + IDX + 1 ))
    if [ "$DR_NUM" -lt 10 ]; then
      DR_PREFIX="DR-00${DR_NUM}"
    elif [ "$DR_NUM" -lt 100 ]; then
      DR_PREFIX="DR-0${DR_NUM}"
    else
      DR_PREFIX="DR-${DR_NUM}"
    fi

    # Check if this Pattern-Key already exists in LEARNINGS.md
    ALREADY_EXISTS=0
    if [ -f "$LEARNINGS_FILE" ] && grep -qF "**Pattern-Key**: $PKEY" "$LEARNINGS_FILE" 2>/dev/null; then
      ALREADY_EXISTS=1
    fi

    if [ "$ALREADY_EXISTS" -eq 0 ]; then
      # Append new entry
      echo "$INPUT" | jq -r --argjson i "$IDX" --arg now "$NOW" --arg prefix "$DR_PREFIX" --arg pkey "$PKEY" '
        .[$i] as $f |
        "### " + $prefix + ": " + $f.pattern + "\n" +
        "- **Logged**: " + $now + "\n" +
        "- **Priority**: " + $f.severity + "\n" +
        "- **Status**: pending\n" +
        "- **Area**: infra\n" +
        "- **Category**: behavioral_failure\n" +
        "- **Pattern-Key**: " + $pkey + "\n" +
        "- **Recurrence-Count**: 1\n" +
        "- **First-Seen**: " + $now + "\n" +
        "- **Last-Seen**: " + $now + "\n" +
        "- **Source**: clawdoc\n" +
        "- **Evidence**: " + $f.evidence + "\n" +
        "- **Prescription**: " + $f.prescription + "\n"
      ' >> "$LEARNINGS_FILE"
      APPENDED=$(( APPENDED + 1 ))
    else
      # Pattern-Key already exists — increment Recurrence-Count and update Last-Seen
      awk -v pkey="$PKEY" -v now="$NOW" '
        BEGIN { in_block = 0; found_key = 0 }
        /^### DR-/ {
          if (found_key) { found_key = 0 }
          in_block = 1
        }
        in_block && /\*\*Pattern-Key\*\*:/ {
          if (index($0, pkey) > 0) found_key = 1
        }
        found_key && /^- \*\*Recurrence-Count\*\*:/ {
          match($0, /[0-9]+/)
          count = substr($0, RSTART, RLENGTH) + 1
          sub(/[0-9]+/, count)
        }
        found_key && /^- \*\*Last-Seen\*\*:/ {
          sub(/- \*\*Last-Seen\*\*: .*/, "- **Last-Seen**: " now)
        }
        { print }
      ' "$LEARNINGS_FILE" > "${LEARNINGS_FILE}.tmp" && mv "${LEARNINGS_FILE}.tmp" "$LEARNINGS_FILE"
      UPDATED=$(( UPDATED + 1 ))
    fi
  done

  echo "[prescribe] wrote $APPENDED new finding(s), updated $UPDATED existing finding(s) in $LEARNINGS_FILE" >&2
fi
