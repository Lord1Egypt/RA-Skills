#!/bin/bash
# Emergence Agent CEO — Workspace Scaffolder
# Usage: ./scaffold.sh <workspace_dir>
# Creates the full workspace structure for a new CEO agent deployment.

WORKSPACE="${1:-.}"

if [ -z "$WORKSPACE" ]; then
    echo "Usage: ./scaffold.sh <workspace_dir>"
    echo "  workspace_dir  Directory to initialize (default: current directory)"
    exit 1
fi

echo "[1/5] Creating directory structure..."

mkdir -p "$WORKSPACE/pulse"
mkdir -p "$WORKSPACE/publications/blog"
mkdir -p "$WORKSPACE/publications/social"
mkdir -p "$WORKSPACE/strategies"
mkdir -p "$WORKSPACE/research"
mkdir -p "$WORKSPACE/designs"
mkdir -p "$WORKSPACE/ops"
mkdir -p "$WORKSPACE/.github/ISSUE_TEMPLATE"

echo "[2/5] Initializing MEMORY.md..."

if [ ! -f "$WORKSPACE/MEMORY.md" ]; then
cat > "$WORKSPACE/MEMORY.md" <<'EOF'
# MEMORY.md — Organizational Memory

This file accumulates context over time. Each entry is dated and captures
decisions, learnings, and state changes.

<!-- Example:
## 2026-05-06 — Initial deployment
- Workspace initialized for [company name]
- CEO Agent: Hermes, Sub-agents: Growth + DevOps
- Initial focus: [strategic area]
-->
EOF
fi

echo "[3/5] Initializing HEARTBEAT.md..."

if [ ! -f "$WORKSPACE/HEARTBEAT.md" ]; then
cat > "$WORKSPACE/HEARTBEAT.md" <<'EOF'
# HEARTBEAT.md — Cron Schedule & Proactive Tasks

## Daily Heartbeat (cron: 0 9 * * *)
1. Read and synthesize pulse signals from pulse/
2. Analyze market trends and competitor movements
3. Create strategic tasks in GitHub Issues
4. Update organizational memory in MEMORY.md

## Weekly Review (cron: 0 9 * * 1)
1. Synthesize weekly pulse summary
2. Evaluate content performance from publications/
3. Propose strategic pivots if needed
4. Open weekly summary Issue for stakeholder review
EOF
fi

echo "[4/5] Initializing ops/incident-log.md..."

if [ ! -f "$WORKSPACE/ops/incident-log.md" ]; then
cat > "$WORKSPACE/ops/incident-log.md" <<'EOF'
# Incident Log

| Date | Type | Description | Resolution |
| :--- | :--- | :--- | :--- |
<!-- Add incidents here -->
EOF
fi

echo "[5/5] Creating GitHub Issue templates..."

if [ ! -f "$WORKSPACE/.github/ISSUE_TEMPLATE/strategic-directive.md" ]; then
cat > "$WORKSPACE/.github/ISSUE_TEMPLATE/strategic-directive.md" <<'EOF'
---
name: Strategic Directive
description: Provide strategic direction to the CEO Agent
labels: [directive]
---

## Objective
<!-- What do you want the CEO Agent to accomplish? -->

## Context
<!-- Background, constraints, timeline -->

## Success Criteria
<!-- How will we know this is done well? -->
EOF
fi

if [ ! -f "$WORKSPACE/.github/ISSUE_TEMPLATE/content-request.md" ]; then
cat > "$WORKSPACE/.github/ISSUE_TEMPLATE/content-request.md" <<'EOF'
---
name: Content Request
description: Request content creation from the Growth Leader
labels: [content, growth]
---

## Content Type
<!-- Blog post / Social media / Case study / Other -->

## Topic
<!-- What should the content cover? -->

## Target Audience
<!-- Who is this for? -->

## Key Messages
<!-- What should readers take away? -->
EOF
fi

echo ""
echo "[DONE] Workspace initialized at $WORKSPACE"
echo "  Directories: pulse/ publications/ strategies/ research/ designs/ ops/"
echo "  Files:       MEMORY.md HEARTBEAT.md ops/incident-log.md"
echo ""
echo "Next steps:"
echo "  1. Configure .env with your LLM API key and GitHub repo info"
echo "  2. Start your agent runtime (openclaw / claude / etc.)"
echo "  3. Send your first Strategic Directive via GitHub Issue"
