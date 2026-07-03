#!/bin/bash
# Quick UX review using Luke W + Ryan Singer principles
# Usage: review-ux.sh [component-file]

set -e

if [ -n "$1" ] && [ -f "$1" ]; then
    CODE=$(cat "$1")
    CONTEXT="Component: $1"
elif [ ! -t 0 ]; then
    CODE=$(cat)
    CONTEXT="UI Code"
else
    echo "Usage: review-ux.sh <component-file>"
    echo "   or: cat Component.tsx | review-ux.sh"
    exit 1
fi

cat << EOF

╔══════════════════════════════════════════════════════════════╗
║  LUKE W + RYAN SINGER UX REVIEW                              ║
║  $CONTEXT
╚══════════════════════════════════════════════════════════════╝

Review this UI using LukeW and Ryan Singer principles:

---
$CODE
---

## LukeW's UX Principles:

□ Mobile First
  - Is it responsive?
  - Does mobile experience work well?

□ Progressive Disclosure
  - Is complexity hidden until needed?
  - Are advanced options tucked away?

□ Obvious Next Actions
  - Are CTAs clear and prominent?
  - Does user know what to do next?

□ Reduce Cognitive Load
  - Is it simple? Less is more.
  - Can anything be removed?

□ Visual Hierarchy
  - Does the eye flow naturally?
  - Is importance clear visually?

## Ryan Singer / Jobs To Be Done:

□ What's the job?
  - What is user trying to accomplish?

□ What's the outcome?
  - What does success look like?

□ Remove Friction
  - Is the happy path obvious?
  - What obstacles exist?

□ Everything Else is Secondary
  - Are we focused on the core job?

## Issues Found:

(List UX issues here)

## Recommendations:

(Suggest UX improvements)

EOF
