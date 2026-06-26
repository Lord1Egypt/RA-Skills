#!/usr/bin/env bash
# review.sh — Health check on your learnings (v2)
# Usage: bash review.sh [workspace_path]

set -uo pipefail

WORKSPACE="${1:-.}"
LEARNINGS_DIR="${WORKSPACE}/.learnings"

if [[ ! -d "$LEARNINGS_DIR" ]]; then
  echo "No .learnings/ directory found at ${WORKSPACE}"
  exit 1
fi

echo "🧠 Agent Memory Loop v2 — Review"
echo ""

# Count entries per file (only lines starting with [YYYY- are entries, not header comments)
for file in errors.md learnings.md wishes.md promotion-queue.md; do
  if [[ -f "${LEARNINGS_DIR}/${file}" ]]; then
    count=$(grep -cE '^\[[0-9]{4}-' "${LEARNINGS_DIR}/${file}" 2>/dev/null) || count=0
    echo "  📄 ${file}: ${count} entries"
  fi
done

echo ""

# Pending promotions
echo "  🔺 Pending promotion reviews:"
pending_found=false
if [[ -f "${LEARNINGS_DIR}/promotion-queue.md" ]]; then
  while IFS= read -r line; do
    if [[ -n "$line" ]]; then
      echo "     ${line}"
      pending_found=true
    fi
  done < <(grep "^\[" "${LEARNINGS_DIR}/promotion-queue.md" 2>/dev/null | grep "status: pending" || true)
fi
if [[ "$pending_found" == "false" ]]; then
  echo "     (none)"
fi

echo ""

# Ready for review queue (count:3+ or severity:critical, not yet queued)
echo "  ⚡ Ready for review queue (count:3+ or severity:critical):"
needs_queue=false
for file in errors.md learnings.md; do
  if [[ -f "${LEARNINGS_DIR}/${file}" ]]; then
    while IFS= read -r line; do
      if [[ -n "$line" ]] && ! echo "$line" | grep -q "PROMOTED"; then
        echo "     ${file}: ${line}"
        needs_queue=true
      fi
    done < <(grep "^\[" "${LEARNINGS_DIR}/${file}" 2>/dev/null | grep -E "(count:[3-9][0-9]*|severity:critical)" | grep -v "PROMOTED" || true)
  fi
done
if [[ "$needs_queue" == "false" ]]; then
  echo "     (none)"
fi

echo ""

# Loop closure stats
echo "  🔄 Loop closure (prevention tracking):"
total_prevented=$(grep -h "^\[" "${LEARNINGS_DIR}"/*.md 2>/dev/null | grep -oh "prevented:[0-9]*" 2>/dev/null | awk -F: '{sum+=$2} END {print sum+0}')
echo "     Total prevented: ${total_prevented}"

echo ""

# Stale entries (>6 months, count:1, no prevented)
echo "  ⏰ Potentially stale entries (>6mo, count:1, prevented:0):"
stale_found=false
six_months_ago=$(date -v-6m '+%Y-%m-%d' 2>/dev/null || date -d '6 months ago' '+%Y-%m-%d' 2>/dev/null || echo "")
if [[ -n "$six_months_ago" ]]; then
  for file in errors.md learnings.md; do
    if [[ -f "${LEARNINGS_DIR}/${file}" ]]; then
      while IFS= read -r line; do
        if [[ -n "$line" ]] && echo "$line" | grep -qE "count:1($| )" && ! echo "$line" | grep -q "prevented:[1-9]"; then
          entry_date=$(echo "$line" | grep -oE '^\[[0-9]{4}-[0-9]{2}-[0-9]{2}\]' | tr -d '[]')
          if [[ -n "$entry_date" ]] && [[ "$entry_date" < "$six_months_ago" ]]; then
            echo "     ${file}: ${line}"
            stale_found=true
          fi
        fi
      done < <(grep "^\[" "${LEARNINGS_DIR}/${file}" 2>/dev/null || true)
    fi
  done
fi
if [[ "$stale_found" == "false" ]]; then
  echo "     (none)"
fi

echo ""

# Expired entries
echo "  💀 Expired entries:"
expired_found=false
today=$(date '+%Y-%m-%d')
for file in errors.md learnings.md; do
  if [[ -f "${LEARNINGS_DIR}/${file}" ]]; then
    while IFS= read -r line; do
      if [[ -n "$line" ]]; then
        exp_date=$(echo "$line" | grep -oE 'expires:[0-9]{4}-[0-9]{2}-[0-9]{2}' | cut -d: -f2)
        if [[ -n "$exp_date" ]] && [[ "$exp_date" < "$today" ]]; then
          echo "     ${file}: ${line}"
          expired_found=true
        fi
      fi
    done < <(grep "expires:" "${LEARNINGS_DIR}/${file}" 2>/dev/null || true)
  fi
done
if [[ "$expired_found" == "false" ]]; then
  echo "     (none)"
fi

echo ""

# File sizes
echo "  📏 File sizes:"
for file in errors.md learnings.md wishes.md promotion-queue.md; do
  if [[ -f "${LEARNINGS_DIR}/${file}" ]]; then
    lines=$(wc -l < "${LEARNINGS_DIR}/${file}" 2>/dev/null || echo "0")
    lines=$(echo "$lines" | tr -d ' ')
    status="✅"
    if (( lines > 100 )); then
      status="⚠️  OVER LIMIT"
    fi
    echo "     ${file}: ${lines} lines ${status}"
  fi
done

echo ""

# Source distribution
echo "  🏷️  Source distribution:"
for src in agent user external; do
  src_count=$(grep -h "^\[" "${LEARNINGS_DIR}"/*.md 2>/dev/null | grep -c "source:${src}" 2>/dev/null) || src_count=0
  echo "     source:${src}: ${src_count}"
done

echo ""

# Recent activity
echo "  📅 Last 7 days:"
week_ago=$(date -v-7d '+%Y-%m-%d' 2>/dev/null || date -d '7 days ago' '+%Y-%m-%d' 2>/dev/null || echo "")
if [[ -n "$week_ago" ]]; then
  recent=$(grep -hE '^\[[0-9]{4}-' "${LEARNINGS_DIR}"/*.md 2>/dev/null | awk -v d="$week_ago" '$0 >= "["d' | wc -l)
  recent=$(echo "$recent" | tr -d ' ')
  echo "     ${recent} entries logged"
else
  echo "     (date calculation not available)"
fi
