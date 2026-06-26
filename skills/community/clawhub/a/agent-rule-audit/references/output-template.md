# Output template for agent-rule-audit

Use this as a default shape. Keep it concise unless the user wants a deep dive.

## Audit scope
- Which files were checked
- Which were treated as core behavior sources
- Which were used only as supporting evidence

## Overall judgment
- Is the behavior layer mostly aligned or not?
- What is the main issue in one or two sentences?

## Highest-priority problems
List the top problems in priority order.
For each one:
- what the problem is
- why it matters
- which file(s) it lives in

## Root cause vs symptoms
Only include when useful.
Clarify what is fundamental vs what is just a visible effect.

## What is already fine
Name the parts that already work.
This prevents unnecessary rewrites.

## Recommended changes
Prefer concrete file-by-file recommendations.
Examples:
- move X from `AGENTS.md` to the workspace's correction / learnings layer
- merge these two sections
- strengthen this rule and move it higher
- remove stale wording
- keep this section as-is

## Optional final recommendation
When useful, end with one of:
- small cleanup is enough
- moderate restructuring recommended
- full behavior-layer cleanup recommended
