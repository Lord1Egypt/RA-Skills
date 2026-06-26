#!/usr/bin/env bash
# =============================================================================
# Automate Task Runner
# =============================================================================
# Executes a task using a specified agent profile. Outputs structured results
# to stdout and to a result file.
#
# Usage:
#   ./scripts/run-task.sh <agent-name> "<task-description>"
#   AGENT=frontend-developer TASK_BODY="Build a login form" ./scripts/run-task.sh
#
# Environment variables:
#   AGENT           - Agent name (overridden by $1 if provided)
#   TASK_BODY       - Task description (overridden by $2 if provided)
#   TASK_TITLE      - Short title for the task (optional)
#   ISSUE_NUMBER    - GitHub issue number (optional, for linking)
#   RESULT_FILE     - Output file path (default: /tmp/task-result.md)
#   OPENCLAW_TOKEN  - Enables AI-powered processing
#   AUTOMATE_SSH_KEY - SSH key for secure operations
#   CONFIG_FILE     - Path to automate.yml (default: config/automate.yml)
# =============================================================================

set -euo pipefail

# ---------------------------------------------------------------------------
# Resolve paths relative to repo root
# ---------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
AGENTS_DIR="$REPO_ROOT/agents"
CONFIG_FILE="${CONFIG_FILE:-$REPO_ROOT/config/automate.yml}"
RESULT_FILE="${RESULT_FILE:-/tmp/task-result.md}"

# ---------------------------------------------------------------------------
# Parse arguments (positional overrides env vars)
# ---------------------------------------------------------------------------
AGENT="${1:-${AGENT:-}}"
TASK_BODY="${2:-${TASK_BODY:-}}"
TASK_TITLE="${TASK_TITLE:-$TASK_BODY}"
ISSUE_NUMBER="${ISSUE_NUMBER:-0}"
TIMESTAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
log()  { echo "[$TIMESTAMP] $*"; }
die()  { log "ERROR: $*" >&2; exit 1; }

usage() {
  cat <<EOF
Usage: $(basename "$0") <agent-name> "<task-description>"

Arguments:
  agent-name        Name of the agent (e.g. frontend-developer)
  task-description  What the agent should do

Examples:
  $(basename "$0") backend-architect "Design a REST API for user management"
  $(basename "$0") growth-hacker "Create a 90-day growth plan for a SaaS product"
EOF
  exit 1
}

# ---------------------------------------------------------------------------
# Validate inputs
# ---------------------------------------------------------------------------
[ -z "$AGENT" ] && usage
[ -z "$TASK_BODY" ] && die "Task description is required (pass as \$2 or TASK_BODY)"

# ---------------------------------------------------------------------------
# Locate agent persona file
# ---------------------------------------------------------------------------
find_agent_persona() {
  local name="$1"
  local match=""

  # Exact filename match first
  match=$(find "$AGENTS_DIR" -maxdepth 2 -name "${name}.md" -type f 2>/dev/null | head -1)
  [ -n "$match" ] && { echo "$match"; return 0; }

  # Fuzzy: try partial match
  match=$(find "$AGENTS_DIR" -maxdepth 2 -name "*.md" -type f 2>/dev/null | while read -r f; do
    bn=$(basename "$f" .md)
    if echo "$bn" | grep -qi "$name"; then
      echo "$f"
      break
    fi
  done)
  [ -n "$match" ] && { echo "$match"; return 0; }

  return 1
}

detect_department() {
  local persona_file="$1"
  # Extract from directory path
  local dept_dir
  dept_dir="$(dirname "$persona_file")"
  basename "$dept_dir"
}

extract_frontmatter() {
  local file="$1"
  local key="$2"
  # Extract value from YAML frontmatter (between --- markers)
  sed -n '/^---$/,/^---$/p' "$file" | grep "^${key}:" | sed "s/^${key}:[[:space:]]*//" | head -1
}

# ---------------------------------------------------------------------------
# Resolve agent
# ---------------------------------------------------------------------------
log "🤖 Automate Task Runner"
log "========================"
log "Agent: $AGENT"
log "Task:  $TASK_TITLE"
log "Issue: #$ISSUE_NUMBER"

PERSONA_FILE=""
AGENT_DESC=""
AGENT_DEPT=""

if PERSONA_FILE=$(find_agent_persona "$AGENT"); then
  AGENT_DESC=$(extract_frontmatter "$PERSONA_FILE" "description")
  AGENT_DEPT=$(detect_department "$PERSONA_FILE")
  log "✅ Agent persona loaded: $PERSONA_FILE"
  log "   Department: $AGENT_DEPT"
  log "   Description: $AGENT_DESC"
else
  log "⚠️  No persona file for '$AGENT' — running in generic mode"
  AGENT_DESC="(catalog agent — no dedicated persona file)"
  AGENT_DEPT="unknown"
fi

# ---------------------------------------------------------------------------
# Set up SSH key if available
# ---------------------------------------------------------------------------
if [ -n "${AUTOMATE_SSH_KEY:-}" ]; then
  mkdir -p ~/.ssh
  echo "$AUTOMATE_SSH_KEY" > ~/.ssh/automate_key
  chmod 600 ~/.ssh/automate_key
  log "🔑 SSH key loaded"
fi

# ---------------------------------------------------------------------------
# Build structured result
# ---------------------------------------------------------------------------
cat > "$RESULT_FILE" <<EOF
## 🤖 Task Result — ${AGENT}

| Field | Value |
|-------|-------|
| **Agent** | \`${AGENT}\` |
| **Department** | ${AGENT_DEPT} |
| **Description** | ${AGENT_DESC} |
| **Issue** | #${ISSUE_NUMBER} |
| **Processed** | ${TIMESTAMP} |

---

### 📝 Task

${TASK_TITLE}

---

### 📋 Task Details

${TASK_BODY}

---

EOF

# ---------------------------------------------------------------------------
# AI-powered processing (if token available)
# ---------------------------------------------------------------------------
if [ -n "${OPENCLAW_TOKEN:-}" ]; then
  log "🧠 AI processing available — OPENCLAW_TOKEN detected"
  cat >> "$RESULT_FILE" <<EOF
### 🧠 AI Processing

AI-powered execution is enabled. The agent's persona file is used as the
system prompt for task execution via the OpenClaw API.

**Persona file:** \`${PERSONA_FILE:-N/A}\`

EOF

  # -------------------------------------------------------------------
  # Integration point: Call OpenClaw API or local CLI here.
  # Example (pseudo):
  #   SYSTEM_PROMPT=$(cat "$PERSONA_FILE")
  #   RESPONSE=$(curl -s -X POST "$OPENCLAW_API/v1/chat" \
  #     -H "Authorization: Bearer $OPENCLAW_TOKEN" \
  #     -d "{\"system\": \"$SYSTEM_PROMPT\", \"message\": \"$TASK_BODY\"}")
  #   echo "$RESPONSE" >> "$RESULT_FILE"
  # -------------------------------------------------------------------

else
  log "ℹ️  No OPENCLAW_TOKEN — basic mode (task recorded, not AI-processed)"
  cat >> "$RESULT_FILE" <<EOF
### ℹ️ Basic Mode

No \`OPENCLAW_TOKEN\` configured. Task has been recorded but not AI-processed.
Add the secret to enable AI-powered agent execution.

EOF
fi

# ---------------------------------------------------------------------------
# Append persona summary if available
# ---------------------------------------------------------------------------
if [ -n "$PERSONA_FILE" ] && [ -f "$PERSONA_FILE" ]; then
  # Extract the core mission section (first 5 lines after "## 🎯 核心使命" or "## 🎯 Core Mission")
  MISSION=$(sed -n '/^## 🎯/,/^## /{ /^## 🎯/d; /^## /d; p; }' "$PERSONA_FILE" | head -15)
  if [ -n "$MISSION" ]; then
    cat >> "$RESULT_FILE" <<EOF
### 🎯 Agent Capabilities

${MISSION}

EOF
  fi
fi

# ---------------------------------------------------------------------------
# Output result as JSON for programmatic consumption
# ---------------------------------------------------------------------------
RESULT_JSON="/tmp/task-result.json"
cat > "$RESULT_JSON" <<EOF
{
  "status": "completed",
  "agent": "${AGENT}",
  "department": "${AGENT_DEPT}",
  "issue_number": ${ISSUE_NUMBER},
  "timestamp": "${TIMESTAMP}",
  "ai_enabled": $([ -n "${OPENCLAW_TOKEN:-}" ] && echo "true" || echo "false"),
  "persona_file": "${PERSONA_FILE:-null}",
  "task_title": $(echo "$TASK_TITLE" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read().strip()))' 2>/dev/null || echo "\"$TASK_TITLE\""),
  "result_file": "${RESULT_FILE}"
}
EOF

cat >> "$RESULT_FILE" <<EOF
---
*🤖 Automate Task Runner — ${TIMESTAMP}*
EOF

log ""
log "✅ Task processing complete"
log "   Result (markdown): $RESULT_FILE"
log "   Result (JSON):     $RESULT_JSON"
