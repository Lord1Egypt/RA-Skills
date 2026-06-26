#!/bin/bash
# coding-pipeline Activator Hook
# Triggers on UserPromptSubmit to remind the agent about the 4-phase discipline
# Keep output minimal (~80 tokens) to minimize overhead

set -e

cat << 'EOF'
<coding-pipeline-reminder>
If this task is non-trivial (bug fix, feature, refactor, error investigation):
  1. Phase 1 (Planner) — write hypothesis + scope + success criteria BEFORE code
  2. Phase 2 (Coder) — one focused change, full files, no scope creep
  3. Phase 3 (Validator) — verify root cause, not just build success
  4. Phase 4 (Debugger) — max 3 attempts, each documented, then escalate

Trivial tasks (typos, formatting, one-line config) may skip the pipeline.
Do NOT jump to Phase 2 before Phase 1 is complete.
</coding-pipeline-reminder>
EOF
