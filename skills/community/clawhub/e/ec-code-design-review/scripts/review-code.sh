#!/bin/bash
# Quick code review using Jeff Dean principles
# Usage: review-code.sh [file|git-diff]
#
# Examples:
#   review-code.sh src/auth.ts
#   git diff HEAD~1 | review-code.sh
#   review-code.sh  # reviews staged changes

set -e

if [ -n "$1" ] && [ -f "$1" ]; then
    # Review a specific file
    CODE=$(cat "$1")
    CONTEXT="File: $1"
elif [ ! -t 0 ]; then
    # Read from stdin (piped diff)
    CODE=$(cat)
    CONTEXT="Git diff"
else
    # Review staged changes
    CODE=$(git diff --cached)
    if [ -z "$CODE" ]; then
        CODE=$(git diff HEAD~1)
    fi
    CONTEXT="Recent git changes"
fi

if [ -z "$CODE" ]; then
    echo "No code to review. Provide a file or pipe a diff."
    exit 1
fi

cat << EOF

╔══════════════════════════════════════════════════════════════╗
║  JEFF DEAN CODE REVIEW                                       ║
║  $CONTEXT
╚══════════════════════════════════════════════════════════════╝

Review this code using Jeff Dean's principles:

---
$CODE
---

## Checklist:

□ Design & Architecture
  - Does the overall design make sense?
  - Is code in the right place (here vs library)?
  - Does it align with broader architecture?

□ Functionality & Logic  
  - Is the logic correct and complete?
  - Are edge cases handled?
  - Is error handling appropriate?

□ Clarity & Maintainability
  - Could someone unfamiliar maintain this?
  - Are functions small and focused?
  - Is it well-documented where needed?

□ Integration
  - Does it integrate cleanly with existing code?
  - Are dependencies appropriate?

□ Testing
  - Is it testable?
  - Are tests included/updated?

## Issues Found:

(List any issues here)

## Recommendations:

(Suggest improvements)

EOF
