#!/bin/bash
# DataGuard DLP — False Positive Reporter
# Copyright (c) 2026 Jeff Cyprien. Licensed under MIT.
# https://github.com/jeffcGit/dataguard-dlp
#
# Report patterns that were incorrectly flagged as sensitive
# Pure bash — no python3 dependency
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
FP_FILE="$SKILL_DIR/config/false-positives.json"
FP_LOG="$SKILL_DIR/logs/false-positives.log"

usage() {
  cat <<EOF
DataGuard False Positive Reporter

USAGE:
  $0 --add <pattern> <description>    Add a false positive pattern
  $0 --list                           List all reported false positives
  $0 --check <text>                   Check if text matches known FPs
  $0 --export                         Export false positives for review

EXAMPLES:
  $0 --add "mycompany.internal" "Internal hostname, not AWS key"
  $0 --add "password123" "Test password in examples"
  $0 --list
  $0 --check "Connecting to mycompany.internal"

This helps improve DataGuard's pattern detection accuracy.

EOF
  exit 0
}

# Simple JSON array management in pure bash
# Format: one JSON object per line in the array

init_fp_file() {
  mkdir -p "$(dirname "$FP_FILE")"
  if [ ! -f "$FP_FILE" ]; then
    echo '{"false_positives": []}' > "$FP_FILE"
  fi
}

add_fp() {
  local pattern="$1"
  local description="${2:-No description provided}"
  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  
  init_fp_file
  
  # Check if pattern already exists
  if grep -q "\"$(echo "$pattern" | sed 's/"/\\"/g')\"" "$FP_FILE" 2>/dev/null; then
    echo "Pattern already reported: $pattern"
    return 0
  fi
  
  # Escape for JSON
  local escaped_pattern=$(echo "$pattern" | sed 's/\\/\\\\/g; s/"/\\"/g')
  local escaped_desc=$(echo "$description" | sed 's/\\/\\\\/g; s/"/\\"/g')
  
  local entry="{\"pattern\":\"$escaped_pattern\",\"description\":\"$escaped_desc\",\"reported_at\":\"$timestamp\",\"status\":\"pending_review\"}"
  
  # Insert into the array: replace ] with , entry ]
  local tmp=$(mktemp)
  if grep -q '"false_positives": \[\]' "$FP_FILE" 2>/dev/null; then
    # Empty array
    sed "s/\"false_positives\": \[\]/\"false_positives\": [$entry]/" "$FP_FILE" > "$tmp"
  else
    # Non-empty array — insert before closing ]
    sed "s/\]/,$entry]/" "$FP_FILE" | head -1 > "$tmp" 2>/dev/null || true
    # Simpler approach: rebuild
    {
      echo '{'
      echo '  "false_positives": ['
      # Extract existing entries
      grep -oE '\{[^}]+\}' "$FP_FILE" | while IFS= read -r obj; do
        echo "    $obj,"
      done
      echo "    $entry"
      echo '  ]'
      echo '}'
    } > "$tmp"
  fi
  
  if [ -s "$tmp" ]; then
    mv "$tmp" "$FP_FILE"
  else
    rm -f "$tmp"
    echo "❌ Error updating false positives file"
    return 1
  fi
  
  # Log
  mkdir -p "$(dirname "$FP_LOG")"
  echo "[$timestamp] REPORTED | Pattern: $pattern | Description: $description" >> "$FP_LOG"
  
  echo "✅ False positive reported: $pattern"
  echo "   Description: $description"
  echo "   Status: pending_review"
}

list_fps() {
  init_fp_file
  
  # Extract entries
  local entries=$(grep -oE '\{[^}]+\}' "$FP_FILE" 2>/dev/null || true)
  
  if [ -z "$entries" ]; then
    echo "No false positives reported yet."
    echo ""
    echo "Use: $0 --add <pattern> <description> to report one."
    return 0
  fi
  
  echo "📋 False Positives Report"
  echo "============================================================"
  echo ""
  
  local i=1
  while IFS= read -r entry; do
    local pattern=$(echo "$entry" | grep -oE '"pattern":"[^"]*"' | sed 's/"pattern":"//;s/"$//')
    local desc=$(echo "$entry" | grep -oE '"description":"[^"]*"' | sed 's/"description":"//;s/"$//')
    local reported=$(echo "$entry" | grep -oE '"reported_at":"[^"]*"' | sed 's/"reported_at":"//;s/"$//')
    local status=$(echo "$entry" | grep -oE '"status":"[^"]*"' | sed 's/"status":"//;s/"$//')
    
    local icon="⏳"
    [ "$status" = "approved" ] && icon="✅"
    [ "$status" = "rejected" ] && icon="❌"
    
    echo "$i. $icon $pattern"
    echo "   Description: $desc"
    echo "   Reported: $reported"
    echo "   Status: $status"
    echo ""
    
    i=$((i + 1))
  done <<< "$entries"
  
  echo "Total: $((i - 1)) false positives"
}

check_fp() {
  local text="$1"
  
  if [ ! -f "$FP_FILE" ]; then
    return 1
  fi
  
  # Check approved false positives against text (case-insensitive)
  local text_lower=$(echo "$text" | tr '[:upper:]' '[:lower:]')
  
  while IFS= read -r entry; do
    local status=$(echo "$entry" | grep -oE '"status":"[^"]*"' | sed 's/"status":"//;s/"$//')
    [ "$status" != "approved" ] && continue
    
    local pattern=$(echo "$entry" | grep -oE '"pattern":"[^"]*"' | sed 's/"pattern":"//;s/"$//')
    local pattern_lower=$(echo "$pattern" | tr '[:upper:]' '[:lower:]')
    
    if echo "$text_lower" | grep -qF "$pattern_lower"; then
      echo "FALSE_POSITIVE:$pattern"
      return 0
    fi
  done < <(grep -oE '\{[^}]+\}' "$FP_FILE" 2>/dev/null)
  
  return 1
}

export_fps() {
  local output="${1:-dataguard-false-positives-$(date +%Y%m%d).json}"
  
  if [ ! -f "$FP_FILE" ]; then
    echo "No false positives to export."
    return 0
  fi
  
  cp "$FP_FILE" "$output"
  echo "✅ Exported to: $output"
}

case "${1:-}" in
  --add) add_fp "${2:-}" "${3:-No description}" ;;
  --list) list_fps ;;
  --check) check_fp "${2:-}" ;;
  --export) export_fps "${2:-}" ;;
  *) usage ;;
esac