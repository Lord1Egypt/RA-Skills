#!/usr/bin/env bash
# =============================================================================
# Agent Dispatch — Intelligent Agent Selection & Routing
# =============================================================================
# Given a task (title, body, labels), selects the best-fit agent(s) and
# dispatches the task to them via run-task.sh.
#
# Usage:
#   ./scripts/agent-dispatch.sh                          # Uses env vars
#   TASK_BODY="Build a React dashboard" ./scripts/agent-dispatch.sh
#
# Environment variables:
#   AGENT           - Explicit agent name (skips auto-detection)
#   DEPARTMENT      - Explicit department (narrows search)
#   ORCHESTRATE     - "true" to trigger multi-agent orchestration
#   TASK_TITLE      - Short task title
#   TASK_BODY       - Full task description
#   ISSUE_NUMBER    - GitHub issue number (optional)
#   ISSUE_LABELS    - JSON array of label strings (optional)
#   OPENCLAW_TOKEN  - Enables AI-powered processing
#   AUTOMATE_SSH_KEY - SSH key for secure operations
#   RESULT_FILE     - Override output path (default: /tmp/agent-result.md)
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
AGENTS_DIR="$REPO_ROOT/agents"
RESULT_FILE="${RESULT_FILE:-/tmp/agent-result.md}"
TIMESTAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# Inputs
AGENT="${AGENT:-}"
DEPARTMENT="${DEPARTMENT:-}"
ORCHESTRATE="${ORCHESTRATE:-false}"
TASK_TITLE="${TASK_TITLE:-}"
TASK_BODY="${TASK_BODY:-}"
ISSUE_NUMBER="${ISSUE_NUMBER:-0}"
ISSUE_LABELS="${ISSUE_LABELS:-[]}"

# ---------------------------------------------------------------------------
# Keyword → Agent mapping
# ---------------------------------------------------------------------------
# Each line: "keyword|agent-name|department"
# Order matters — first match wins within a category; more specific keywords first.
KEYWORD_MAP=(
  # Engineering
  "react|frontend-developer|engineering"
  "vue|frontend-developer|engineering"
  "angular|frontend-developer|engineering"
  "frontend|frontend-developer|engineering"
  "ui component|frontend-developer|engineering"
  "css|frontend-developer|engineering"
  "tailwind|frontend-developer|engineering"
  "responsive|frontend-developer|engineering"
  "api design|backend-architect|engineering"
  "api|backend-architect|engineering"
  "database|backend-architect|engineering"
  "backend|backend-architect|engineering"
  "microservice|backend-architect|engineering"
  "rest|backend-architect|engineering"
  "graphql|backend-architect|engineering"
  "server|backend-architect|engineering"
  "cloud|backend-architect|engineering"
  "aws|backend-architect|engineering"
  "docker|devops-automator|engineering"
  "kubernetes|devops-automator|engineering"
  "ci/cd|devops-automator|engineering"
  "cicd|devops-automator|engineering"
  "pipeline|devops-automator|engineering"
  "deploy|devops-automator|engineering"
  "infrastructure|devops-automator|engineering"
  "terraform|devops-automator|engineering"
  "ios|mobile-app-builder|engineering"
  "android|mobile-app-builder|engineering"
  "mobile|mobile-app-builder|engineering"
  "react native|mobile-app-builder|engineering"
  "flutter|mobile-app-builder|engineering"
  "machine learning|ai-engineer|engineering"
  "ml |ai-engineer|engineering"
  "deep learning|ai-engineer|engineering"
  "neural|ai-engineer|engineering"
  "ai model|ai-engineer|engineering"
  "mvp|rapid-prototyper|engineering"
  "prototype|rapid-prototyper|engineering"
  "proof of concept|rapid-prototyper|engineering"
  "poc|rapid-prototyper|engineering"

  # Design
  "ui design|ui-designer|design"
  "design system|ui-designer|design"
  "visual design|ui-designer|design"
  "user research|ux-researcher|design"
  "usability|ux-researcher|design"
  "user testing|ux-researcher|design"
  "ux|ux-architect|design"
  "brand|brand-guardian|design"
  "logo|brand-guardian|design"
  "animation|whimsy-injector|design"
  "micro-interaction|whimsy-injector|design"
  "image prompt|image-prompt-engineer|design"
  "midjourney|image-prompt-engineer|design"
  "dall-e|image-prompt-engineer|design"
  "stable diffusion|image-prompt-engineer|design"

  # Marketing
  "growth|growth-hacker|marketing"
  "acquisition|growth-hacker|marketing"
  "conversion|growth-hacker|marketing"
  "viral|growth-hacker|marketing"
  "content|content-creator|marketing"
  "blog|content-creator|marketing"
  "copywriting|content-creator|marketing"
  "editorial|content-creator|marketing"
  "twitter|twitter-engager|marketing"
  "tweet|twitter-engager|marketing"
  "x.com|twitter-engager|marketing"
  "tiktok|tiktok-strategist|marketing"
  "short video|tiktok-strategist|marketing"
  "instagram|instagram-curator|marketing"
  "reddit|reddit-community-builder|marketing"
  "app store|app-store-optimizer|marketing"
  "aso|app-store-optimizer|marketing"
  "social media|social-media-strategist|marketing"
  "social strategy|social-media-strategist|marketing"
  "marketing|growth-hacker|marketing"

  # Product
  "sprint|sprint-prioritizer|product"
  "backlog|sprint-prioritizer|product"
  "prioriti|sprint-prioritizer|product"
  "trend|trend-researcher|product"
  "market research|trend-researcher|product"
  "competitive analysis|trend-researcher|product"
  "feedback|feedback-synthesizer|product"
  "user feedback|feedback-synthesizer|product"
  "nps|feedback-synthesizer|product"

  # Project Management
  "project plan|senior-pm|project-management"
  "task breakdown|senior-pm|project-management"
  "scope|senior-pm|project-management"
  "timeline|senior-pm|project-management"
  "roadmap|senior-pm|project-management"
  "project manage|senior-pm|project-management"
  "coordinate|project-shepherd|project-management"
  "cross-functional|project-shepherd|project-management"
  "a/b test|experiment-tracker|project-management"
  "experiment|experiment-tracker|project-management"
  "operations|studio-operations|project-management"
  "process optimization|studio-operations|project-management"

  # Testing
  "quality|reality-checker|testing"
  "release|reality-checker|testing"
  "production ready|reality-checker|testing"
  "qa|reality-checker|testing"
  "screenshot|evidence-collector|testing"
  "visual test|evidence-collector|testing"
  "test result|test-results-analyzer|testing"
  "test analysis|test-results-analyzer|testing"
  "coverage|test-results-analyzer|testing"
  "performance test|performance-benchmarker|testing"
  "load test|performance-benchmarker|testing"
  "benchmark|performance-benchmarker|testing"
  "api test|api-tester|testing"
  "integration test|api-tester|testing"
  "tool eval|tool-evaluator|testing"
  "workflow|workflow-optimizer|testing"
  "test|reality-checker|testing"

  # Support
  "customer|support-responder|support"
  "support ticket|support-responder|support"
  "analytics|analytics-reporter|support"
  "dashboard|analytics-reporter|support"
  "report|analytics-reporter|support"
  "finance|finance-tracker|support"
  "budget|finance-tracker|support"
  "cost|finance-tracker|support"
  "maintenance|infrastructure-maintainer|support"
  "reliability|infrastructure-maintainer|support"
  "compliance|legal-compliance-checker|support"
  "legal|legal-compliance-checker|support"
  "regulation|legal-compliance-checker|support"
  "executive summary|executive-summary-generator|support"
  "c-suite|executive-summary-generator|support"

  # Specialized
  "data extraction|sales-data-extraction-agent|specialized"
  "sales data|sales-data-extraction-agent|specialized"
  "consolidat|data-consolidation-agent|specialized"
  "lsp|lsp-index-engineer|specialized"
  "code intelligence|lsp-index-engineer|specialized"
  "report distribut|report-distribution-agent|specialized"
)

# ---------------------------------------------------------------------------
# Auto-detect agent from task text
# ---------------------------------------------------------------------------
auto_detect_agent() {
  local text
  text="$(echo "${TASK_TITLE} ${TASK_BODY}" | tr '[:upper:]' '[:lower:]')"

  for entry in "${KEYWORD_MAP[@]}"; do
    local keyword agent dept
    keyword="$(echo "$entry" | cut -d'|' -f1)"
    agent="$(echo "$entry" | cut -d'|' -f2)"
    dept="$(echo "$entry" | cut -d'|' -f3)"

    if echo "$text" | grep -qi "$keyword"; then
      echo "$agent"
      return 0
    fi
  done

  return 1
}

# ---------------------------------------------------------------------------
# Get department for an agent
# ---------------------------------------------------------------------------
get_agent_department() {
  local agent_name="$1"
  for entry in "${KEYWORD_MAP[@]}"; do
    local a d
    a="$(echo "$entry" | cut -d'|' -f2)"
    d="$(echo "$entry" | cut -d'|' -f3)"
    if [ "$a" = "$agent_name" ]; then
      echo "$d"
      return 0
    fi
  done
  echo "unknown"
}

# ---------------------------------------------------------------------------
# List agents in a department
# ---------------------------------------------------------------------------
list_department_agents() {
  local dept="$1"
  find "$AGENTS_DIR/$dept/" -maxdepth 1 -name "*.md" -type f 2>/dev/null | while read -r f; do
    basename "$f" .md
  done
}

# ---------------------------------------------------------------------------
# Parse labels for agent:/department: prefixes
# ---------------------------------------------------------------------------
parse_labels() {
  if [ "$ISSUE_LABELS" != "[]" ] && [ -n "$ISSUE_LABELS" ]; then
    # Extract agent: labels
    local label_agent
    label_agent=$(echo "$ISSUE_LABELS" | grep -oP '"agent:\K[^"]+' | head -1 || true)
    [ -n "$label_agent" ] && [ -z "$AGENT" ] && AGENT="$label_agent"

    # Extract department: labels
    local label_dept
    label_dept=$(echo "$ISSUE_LABELS" | grep -oP '"department:\K[^"]+' | head -1 || true)
    [ -n "$label_dept" ] && [ -z "$DEPARTMENT" ] && DEPARTMENT="$label_dept"

    # Check for orchestrate label
    if echo "$ISSUE_LABELS" | grep -q '"orchestrate"'; then
      ORCHESTRATE="true"
    fi
  fi
}

# ---------------------------------------------------------------------------
# Main dispatch logic
# ---------------------------------------------------------------------------
echo "🤖 Agent Dispatch"
echo "=================="
echo "Timestamp: $TIMESTAMP"
echo ""

# Step 1: Parse labels
parse_labels

# Step 2: Determine routing
DETECTED_AGENT=""
DETECTION_METHOD=""

if [ "$ORCHESTRATE" = "true" ]; then
  DETECTION_METHOD="orchestrate"
  echo "🔄 Orchestration mode — multi-agent pipeline"
elif [ -n "$AGENT" ]; then
  DETECTED_AGENT="$AGENT"
  DETECTION_METHOD="explicit"
  echo "🎯 Explicit agent: $AGENT"
elif [ -n "$DEPARTMENT" ]; then
  DETECTION_METHOD="department"
  echo "🏢 Department routing: $DEPARTMENT"
  # Pick the best agent from the department based on keywords
  for entry in "${KEYWORD_MAP[@]}"; do
    local kw ag dp
    kw="$(echo "$entry" | cut -d'|' -f1)"
    ag="$(echo "$entry" | cut -d'|' -f2)"
    dp="$(echo "$entry" | cut -d'|' -f3)"
    if [ "$dp" = "$DEPARTMENT" ]; then
      text="$(echo "${TASK_TITLE} ${TASK_BODY}" | tr '[:upper:]' '[:lower:]')"
      if echo "$text" | grep -qi "$kw"; then
        DETECTED_AGENT="$ag"
        break
      fi
    fi
  done
  # Fallback: first agent with a persona file in the department
  if [ -z "$DETECTED_AGENT" ]; then
    DETECTED_AGENT=$(list_department_agents "$DEPARTMENT" | head -1)
  fi
else
  # Auto-detect from task content
  if DETECTED_AGENT=$(auto_detect_agent); then
    DETECTION_METHOD="auto-keyword"
    echo "🔍 Auto-detected agent: $DETECTED_AGENT (keyword match)"
  else
    DETECTED_AGENT="senior-pm"
    DETECTION_METHOD="fallback"
    echo "🤷 No match — falling back to senior-pm for triage"
  fi
fi

echo ""

# ---------------------------------------------------------------------------
# Build result
# ---------------------------------------------------------------------------
if [ "$ORCHESTRATE" = "true" ]; then
  # Delegate to the orchestrator workflow / pipeline
  cat > "$RESULT_FILE" <<EOF
## 🔄 Orchestrator Dispatch

**Task:** ${TASK_TITLE:-$TASK_BODY}
**Mode:** Multi-agent orchestration
**Dispatched:** ${TIMESTAMP}

The orchestrator will:
1. Analyze the project requirements
2. Decompose into agent-sized tasks
3. Assign specialists from the 61-agent roster
4. Run dev ↔ QA quality loops
5. Deliver integrated results

---

### 📋 Project Description

${TASK_BODY}

---
*🤖 Automate Agent Dispatch — orchestration mode*
EOF

  echo "✅ Orchestration dispatch recorded"

elif [ -n "$DETECTED_AGENT" ]; then
  # Dispatch to specific agent via run-task.sh
  echo "🚀 Dispatching to: $DETECTED_AGENT (via $DETECTION_METHOD)"
  echo ""

  export AGENT="$DETECTED_AGENT"
  export TASK_BODY
  export TASK_TITLE
  export ISSUE_NUMBER
  export RESULT_FILE

  # Call run-task.sh
  bash "$SCRIPT_DIR/run-task.sh" "$DETECTED_AGENT" "$TASK_BODY"

  # Prepend dispatch metadata
  TEMP_FILE=$(mktemp)
  cat > "$TEMP_FILE" <<EOF
## 🤖 Agent Dispatch Result

| Field | Value |
|-------|-------|
| **Routing** | ${DETECTION_METHOD} |
| **Selected Agent** | \`${DETECTED_AGENT}\` |
| **Department** | $(get_agent_department "$DETECTED_AGENT") |
| **Issue** | #${ISSUE_NUMBER} |
| **Dispatched** | ${TIMESTAMP} |

---

EOF
  cat "$RESULT_FILE" >> "$TEMP_FILE"
  mv "$TEMP_FILE" "$RESULT_FILE"

else
  cat > "$RESULT_FILE" <<EOF
## ⚠️ Dispatch Failed

Could not determine an appropriate agent for this task.

**Task:** ${TASK_TITLE:-$TASK_BODY}
**Labels:** ${ISSUE_LABELS}
**Timestamp:** ${TIMESTAMP}

### Suggestions
- Add an \`agent:<name>\` label to the issue
- Add a \`department:<name>\` label
- Use more specific keywords in the task description
- See [AGENTS.md](../AGENTS.md) for the full agent roster

---
*🤖 Automate Agent Dispatch*
EOF

  echo "⚠️ Could not determine agent — see result file"
fi

echo ""
echo "✅ Dispatch complete"
echo "   Result: $RESULT_FILE"
