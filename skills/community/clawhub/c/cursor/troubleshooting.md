# Troubleshooting - Cursor

Use this file when Cursor is behaving inconsistently, reading the wrong context, or producing work that does not match repo intent.

## Fast Triage

Check these in order:
1. active surface
2. repo and folder scope
3. rule hierarchy
4. indexing and ignore posture
5. remote versus local execution
6. verification evidence

## Common Failure Patterns

### Cursor ignores repo conventions
- inspect `.cursor/rules` and repo agent guidance before rewriting prompts
- remove duplicate or conflicting guidance
- narrow context to the files that actually matter

### CLI run widens scope
- confirm the repo path and task boundary
- restate the objective in one sentence
- avoid rerunning vague non-interactive prompts

### Background Agent results feel off
- verify which repo, branch, and integration path the remote run actually used
- separate command failure from bad task framing
- inspect remote output before applying local fixes

### Bugbot noise overwhelms signal
- check whether the PR is too broad
- refine review guidance if `.cursor/BUGBOT.md` exists
- triage findings by severity before changing code

### Privacy assumptions were wrong
- check whether indexing, GitHub integration, or MCP changed the trust boundary
- stop remote workflows until the data path is clear
- move to a smaller local surface if the repo is more sensitive than expected

## Recovery Rule

When in doubt, fall back to the smallest local Cursor surface that can reproduce the issue, confirm repo context and rules, and only then reintroduce automation, indexing, or remote execution.
