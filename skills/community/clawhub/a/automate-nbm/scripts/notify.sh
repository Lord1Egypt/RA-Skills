#!/usr/bin/env bash
# =============================================================================
# Automate Notification Helper
# =============================================================================
# Posts structured notifications to GitHub issues, webhooks, or console.
#
# Usage:
#   ./scripts/notify.sh <type> <message> [target]
#   ./scripts/notify.sh result "Task completed successfully" github
#   ./scripts/notify.sh error "Build failed" webhook
#   ./scripts/notify.sh progress "Phase 2 of 4 complete" github
#
# Arguments:
#   type    - Notification type: info | success | warning | error | progress | result
#   message - The notification message (plain text or markdown)
#   target  - Delivery target: console | github | webhook | all (default: console)
#
# Environment variables:
#   GITHUB_TOKEN       - Required for github target
#   GITHUB_REPOSITORY  - owner/repo (required for github target)
#   ISSUE_NUMBER       - Issue to comment on (required for github target)
#   WEBHOOK_URL        - URL for webhook target
#   NOTIFY_SILENT      - "true" to suppress console echo on non-console targets
# =============================================================================

set -euo pipefail

# ---------------------------------------------------------------------------
# Parse arguments
# ---------------------------------------------------------------------------
NOTIFY_TYPE="${1:-info}"
NOTIFY_MSG="${2:-No message provided}"
NOTIFY_TARGET="${3:-console}"
TIMESTAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
NOTIFY_SILENT="${NOTIFY_SILENT:-false}"

# ---------------------------------------------------------------------------
# Type → emoji mapping
# ---------------------------------------------------------------------------
type_emoji() {
  case "$1" in
    info)     echo "ℹ️" ;;
    success)  echo "✅" ;;
    warning)  echo "⚠️" ;;
    error)    echo "❌" ;;
    progress) echo "🔄" ;;
    result)   echo "📋" ;;
    *)        echo "📢" ;;
  esac
}

type_label() {
  case "$1" in
    info)     echo "Info" ;;
    success)  echo "Success" ;;
    warning)  echo "Warning" ;;
    error)    echo "Error" ;;
    progress) echo "Progress" ;;
    result)   echo "Result" ;;
    *)        echo "Notice" ;;
  esac
}

EMOJI=$(type_emoji "$NOTIFY_TYPE")
LABEL=$(type_label "$NOTIFY_TYPE")

# ---------------------------------------------------------------------------
# Console output
# ---------------------------------------------------------------------------
notify_console() {
  echo "[$TIMESTAMP] $EMOJI [$LABEL] $NOTIFY_MSG"
}

# ---------------------------------------------------------------------------
# GitHub issue comment
# ---------------------------------------------------------------------------
notify_github() {
  local token="${GITHUB_TOKEN:-}"
  local repo="${GITHUB_REPOSITORY:-}"
  local issue="${ISSUE_NUMBER:-}"

  if [ -z "$token" ]; then
    echo "⚠️ GITHUB_TOKEN not set — cannot post to GitHub" >&2
    return 1
  fi
  if [ -z "$repo" ]; then
    echo "⚠️ GITHUB_REPOSITORY not set — cannot post to GitHub" >&2
    return 1
  fi
  if [ -z "$issue" ] || [ "$issue" = "0" ]; then
    echo "⚠️ ISSUE_NUMBER not set — cannot post to GitHub" >&2
    return 1
  fi

  # Build markdown body
  local body
  body=$(cat <<EOF
${EMOJI} **${LABEL}**

${NOTIFY_MSG}

---
*🤖 Automate — ${TIMESTAMP}*
EOF
)

  # Escape for JSON
  local json_body
  json_body=$(echo "$body" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))' 2>/dev/null || echo "\"$body\"")

  local response
  response=$(curl -sS -w "\n%{http_code}" -X POST \
    -H "Authorization: token ${token}" \
    -H "Accept: application/vnd.github+json" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    "https://api.github.com/repos/${repo}/issues/${issue}/comments" \
    -d "{\"body\": ${json_body}}" 2>&1)

  local http_code
  http_code=$(echo "$response" | tail -1)
  local body_response
  body_response=$(echo "$response" | sed '$d')

  if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
    [ "$NOTIFY_SILENT" != "true" ] && echo "✅ Posted to GitHub issue #${issue}"
  else
    echo "❌ GitHub API returned $http_code" >&2
    echo "$body_response" >&2
    return 1
  fi
}

# ---------------------------------------------------------------------------
# Webhook
# ---------------------------------------------------------------------------
notify_webhook() {
  local url="${WEBHOOK_URL:-}"
  if [ -z "$url" ]; then
    echo "⚠️ WEBHOOK_URL not set — cannot send webhook" >&2
    return 1
  fi

  local payload
  payload=$(cat <<EOF
{
  "type": "${NOTIFY_TYPE}",
  "label": "${LABEL}",
  "message": $(echo "$NOTIFY_MSG" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))' 2>/dev/null || echo "\"$NOTIFY_MSG\""),
  "timestamp": "${TIMESTAMP}",
  "issue_number": ${ISSUE_NUMBER:-0},
  "source": "automate"
}
EOF
)

  local response
  response=$(curl -sS -w "\n%{http_code}" -X POST "$url" \
    -H "Content-Type: application/json" \
    -d "$payload" 2>&1)

  local http_code
  http_code=$(echo "$response" | tail -1)

  if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
    [ "$NOTIFY_SILENT" != "true" ] && echo "✅ Webhook delivered"
  else
    echo "❌ Webhook returned $http_code" >&2
    return 1
  fi
}

# ---------------------------------------------------------------------------
# Dispatch to target(s)
# ---------------------------------------------------------------------------
EXIT_CODE=0

case "$NOTIFY_TARGET" in
  console)
    notify_console
    ;;
  github)
    notify_console
    notify_github || EXIT_CODE=$?
    ;;
  webhook)
    notify_console
    notify_webhook || EXIT_CODE=$?
    ;;
  all)
    notify_console
    notify_github || true
    notify_webhook || true
    ;;
  *)
    echo "❌ Unknown target: $NOTIFY_TARGET" >&2
    echo "   Valid targets: console, github, webhook, all" >&2
    EXIT_CODE=1
    ;;
esac

exit $EXIT_CODE
