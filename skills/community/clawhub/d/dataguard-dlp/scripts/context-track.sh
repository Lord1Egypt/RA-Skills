#!/bin/bash
# DataGuard DLP — Context Tracker
# Copyright (c) 2026 Jeff Cyprien. Licensed under MIT.
# https://github.com/jeffcGit/dataguard-dlp
#
# Tracks sensitive file reads for context-aware risk scoring
# Pure bash — no python3 dependency
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONTEXT_FILE="$SKILL_DIR/context/sensitive-reads.json"
MAX_ENTRIES=100

# Ensure context directory exists
mkdir -p "$SKILL_DIR/context"

init_context_file() {
  if [ ! -f "$CONTEXT_FILE" ]; then
    echo '{"reads": []}' > "$CONTEXT_FILE"
  fi
}

log_read() {
  local file="$1"
  local patterns="${2:-}"
  
  init_context_file
  
  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  local risk_level="MEDIUM"
  
  # Determine risk level from patterns
  local pat_upper=$(echo "$patterns" | tr '[:lower:]' '[:upper:]')
  for kw in KEY PASSWORD SECRET CRED; do
    if [[ "$pat_upper" == *"$kw"* ]]; then
      risk_level="HIGH"
      break
    fi
  done
  
  # Build JSON entry using simple string manipulation
  local escaped_file=$(echo "$file" | sed 's/"/\\"/g')
  local entry="{\"timestamp\":\"$timestamp\",\"file\":\"$escaped_file\",\"patterns\":["
  
  if [ -n "$patterns" ]; then
    local first=true
    IFS=',' read -ra PATS <<< "$patterns"
    for p in "${PATS[@]}"; do
      p=$(echo "$p" | sed 's/"/\\"/g' | xargs)
      [ "$first" = true ] && first=false || entry+=","
      entry+="\"$p\""
    done
  fi
  
  entry+="],\"risk_level\":\"$risk_level\"}"
  
  # Insert at beginning of reads array
  # Read current file, strip trailing ]}, insert entry
  local tmp=$(mktemp)
  {
    # Read existing content up to the reads array
    sed -n '1,/\["reads"/p' "$CONTEXT_FILE" | head -1
    echo "  \"reads\": ["
    echo "    $entry,"
    # Extract existing entries (skip first [ and last ])
    sed -n '/"reads"/,/\]/p' "$CONTEXT_FILE" | grep -v '"reads"' | grep -v '^\s*[\]]' | head -n $((MAX_ENTRIES - 1)) | sed 's/^/    /'
    echo "  ]"
    echo "}"
  } > "$tmp"
  
  # Validate it's not empty/corrupt, then replace
  if [ -s "$tmp" ]; then
    mv "$tmp" "$CONTEXT_FILE"
  else
    rm -f "$tmp"
  fi
  
  echo "✅ Logged sensitive read: $file"
  [ -n "$patterns" ] && echo "   Patterns: $patterns"
}

check_context() {
  init_context_file
  
  echo "📊 Recent Sensitive File Reads"
  echo "=================================================="
  
  if grep -q '"reads": \[\]' "$CONTEXT_FILE" 2>/dev/null; then
    echo "No recent sensitive reads."
    return 0
  fi
  
  local now_epoch=$(date -u +%s)
  local count=0
  
  # Parse entries using grep/sed (lines with "file" key)
  grep '"file"' "$CONTEXT_FILE" | while IFS= read -r line; do
    count=$((count + 1))
    [ "$count" -gt 10 ] && break
    
    local fpath=$(echo "$line" | grep -oE '"file":"[^"]*"' | sed 's/"file":"//;s/"$//')
    local ts=$(echo "$line" | grep -oE '"timestamp":"[^"]*"' | sed 's/"timestamp":"//;s/"$//')
    local rlevel=$(echo "$line" | grep -oE '"risk_level":"[^"]*"' | sed 's/"risk_level":"//;s/"$//')
    
    # Calculate age
    local ts_epoch=$(date -d "$ts" +%s 2>/dev/null || echo 0)
    local age_sec=$((now_epoch - ts_epoch))
    local age_min=$((age_sec / 60))
    local age_str
    if [ "$age_min" -lt 60 ]; then
      age_str="${age_min}m ago"
    else
      age_str="$((age_min / 60))h ago"
    fi
    
    local risk_icon="🟡"
    [ "$rlevel" = "HIGH" ] && risk_icon="🔴"
    
    echo "$risk_icon $age_str: $fpath"
    
    # Show patterns if any
    local pats=$(echo "$line" | grep -oE '"patterns":\[[^]]*\]' | sed 's/"patterns":\[//;s/\]$//' | tr -d '"' | sed 's/,/, /g')
    [ -n "$pats" ] && echo "   Patterns: $pats"
  done
  
  echo ""
  echo "Current Context Score: +$(get_score)"
}

clear_context() {
  echo '{"reads": []}' > "$CONTEXT_FILE"
  echo "✅ Cleared session context"
}

get_score() {
  init_context_file
  
  local now_epoch=$(date -u +%s)
  local score=0
  
  # Parse timestamps from context file
  grep -oE '"timestamp":"[^"]*"' "$CONTEXT_FILE" | sed 's/"timestamp":"//;s/"$//' | while IFS= read -r ts; do
    local ts_epoch=$(date -d "$ts" +%s 2>/dev/null || echo 0)
    local age_sec=$((now_epoch - ts_epoch))
    local age_min=$((age_sec / 60))
    
    if [ "$age_min" -lt 5 ]; then
      score=$((score + 3))
    elif [ "$age_min" -lt 30 ]; then
      score=$((score + 1))
    fi
  done
  
  echo "$score"
}

usage() {
  cat <<EOF
DataGuard Context Tracker

Usage:
  $0 --log <file> [patterns]   Log a sensitive file read
  $0 --check                   Check recent sensitive reads
  $0 --clear                   Clear session context
  $0 --score                   Get current context risk score

Patterns are comma-separated, e.g.: "AWS_KEY,DB_PASSWORD"

EOF
  exit 0
}

case "${1:-}" in
  --log) log_read "${2:-}" "${3:-}" ;;
  --check) check_context ;;
  --clear) clear_context ;;
  --score) get_score ;;
  *) usage ;;
esac