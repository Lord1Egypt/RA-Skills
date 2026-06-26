#!/bin/bash
# Council Builder - Directory Initializer
# Creates the base directory structure for a new agent council
# Usage: ./init-council.sh <workspace-path> <agent-names...>
# Example: ./init-council.sh ~/.openclaw/workspace r2 leia anakin

set -e

WORKSPACE="${1:?Usage: init-council.sh <workspace-path> <agent-name> [agent-name...]}"
shift

if [ $# -eq 0 ]; then
    echo "Error: At least one agent name required"
    echo "Usage: init-council.sh <workspace-path> <agent-name> [agent-name...]"
    exit 1
fi

GREEN='\033[0;32m'
NC='\033[0m'

log() { echo -e "${GREEN}[+]${NC} $1"; }

# Create shared and support directories
mkdir -p "$WORKSPACE/shared/reports"
mkdir -p "$WORKSPACE/shared/learnings"
mkdir -p "$WORKSPACE/memory"
mkdir -p "$WORKSPACE/docs/architecture"
log "Created shared and support directories"

# Initialize weekly learning metrics file
if [ ! -f "$WORKSPACE/memory/learning-metrics.json" ]; then
    cat > "$WORKSPACE/memory/learning-metrics.json" << 'EOF'
{
  "lastWeeklyReview": null,
  "windowDays": 7,
  "counts": {
    "errors": 0,
    "learnings": 0,
    "featureRequests": 0,
    "repeatedMistakes": 0,
    "promotions": 0
  },
  "routing": {
    "fast": 0,
    "think": 0,
    "deep": 0,
    "strategic": 0
  },
  "nextWeekFocus": ""
}
EOF
    log "Created memory/learning-metrics.json"
fi

# Initialize visual architecture doc
if [ ! -f "$WORKSPACE/docs/architecture/ADAPTIVE-ROUTING-LEARNING.md" ]; then
    cat > "$WORKSPACE/docs/architecture/ADAPTIVE-ROUTING-LEARNING.md" << 'EOF'
# Adaptive Routing and Learning

Purpose
- Route tasks to the right model depth
- Improve quality weekly through measured feedback

## Routing Matrix

| Route | Use When | Preferred Model | Reasoning |
|------|----------|-----------------|-----------|
| Fast | direct answer and routine operation | default model | off |
| Think | analysis and structured planning | analysis-tier model | on |
| Deep | long-context synthesis and publication-grade output | long-context model | off |
| Strategic | architecture and high-impact tradeoff decisions | strategic-tier model | on |

## Weekly Metrics Source
`memory/learning-metrics.json`
EOF
    log "Created docs/architecture/ADAPTIVE-ROUTING-LEARNING.md"
fi

# Initialize cross-agent learnings file
if [ ! -f "$WORKSPACE/shared/learnings/CROSS-AGENT.md" ]; then
    cat > "$WORKSPACE/shared/learnings/CROSS-AGENT.md" << 'EOF'
# Cross-Agent Learnings

Learnings that apply across multiple agents. Any agent can write here.

---

<!-- New entries go below this line -->
EOF
    log "Created shared/learnings/CROSS-AGENT.md"
fi

# Create each agent's directory structure
for AGENT in "$@"; do
    AGENT_DIR="$WORKSPACE/agents/$AGENT"
    
    mkdir -p "$AGENT_DIR/memory"
    mkdir -p "$AGENT_DIR/.learnings"
    mkdir -p "$AGENT_DIR/scripts"
    mkdir -p "$AGENT_DIR/hooks"
    mkdir -p "$AGENT_DIR/references"
    mkdir -p "$AGENT_DIR/data"
    
    # Initialize .learnings files if they don't exist
    if [ ! -f "$AGENT_DIR/.learnings/LEARNINGS.md" ]; then
        cat > "$AGENT_DIR/.learnings/LEARNINGS.md" << 'EOF'
# Learnings Log

Corrections, knowledge gaps, and best practices.

**Statuses**: pending | in_progress | resolved | wont_fix | promoted

---

<!-- New entries go below this line -->
EOF
    fi
    
    if [ ! -f "$AGENT_DIR/.learnings/ERRORS.md" ]; then
        cat > "$AGENT_DIR/.learnings/ERRORS.md" << 'EOF'
# Errors Log

Command failures, exceptions, and unexpected behaviors.

**Statuses**: pending | in_progress | resolved | wont_fix

---

<!-- New entries go below this line -->
EOF
    fi
    
    if [ ! -f "$AGENT_DIR/.learnings/FEATURE_REQUESTS.md" ]; then
        cat > "$AGENT_DIR/.learnings/FEATURE_REQUESTS.md" << 'EOF'
# Feature Requests

Capabilities requested that don't currently exist.

**Statuses**: pending | in_progress | resolved | wont_fix

---

<!-- New entries go below this line -->
EOF
    fi

    # Initialize gotchas.md
    if [ ! -f "$AGENT_DIR/gotchas.md" ]; then
        cat > "$AGENT_DIR/gotchas.md" << EOF
# Gotchas — $AGENT

Known pitfalls. Read this before major tasks.

---

<!-- Add gotchas as they surface. Format: ## Title / What goes wrong / The fix -->
EOF
    fi

    # Initialize config.json
    if [ ! -f "$AGENT_DIR/config.json" ]; then
        cat > "$AGENT_DIR/config.json" << EOF
{
  "agent_name": "$AGENT",
  "setup_complete": false,
  "preferences": {},
  "api_keys_ref": [],
  "custom_settings": {}
}
EOF
    fi

    # Initialize scripts/README.md
    if [ ! -f "$AGENT_DIR/scripts/README.md" ]; then
        cat > "$AGENT_DIR/scripts/README.md" << EOF
# Scripts — $AGENT

Executable helpers for recurring tasks.

<!-- List scripts and their purpose as they are created -->
EOF
    fi

    # Initialize references/verification-checklist.md
    if [ ! -f "$AGENT_DIR/references/verification-checklist.md" ]; then
        cat > "$AGENT_DIR/references/verification-checklist.md" << EOF
# Verification Checklist — $AGENT

Run through this before delivering any output.

## Objective Checks
- [ ] Output matches requested format
- [ ] No known gotchas triggered (check gotchas.md)

## Subjective Checks
- [ ] Quality meets the bar for this task type
- [ ] No scope creep beyond what was asked

<!-- Add role-specific checks as patterns emerge -->
EOF
    fi
    
    log "Created agent structure: agents/$AGENT/"
done

echo ""
log "Council structure initialized with ${#@} agents"
echo "  Next: Create SOUL.md and AGENTS.md for each agent"
