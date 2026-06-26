# Codex Delegate Routing Notes

## Delegate to Codex
- Deep repository analysis
- Multi-file code edits
- Patch drafting
- Heavy static review
- Skill package inspection
- Focused environment debugging
- Error/log analysis

## Main agent keeps ownership
- User-facing framing
- Risk trade-offs
- Final installation recommendation
- Environment acceptance across shell / gateway / cron / LaunchAgent
- Upgrade timing
- Whether a workaround becomes the standard solution

## Three examples

### 1. Code project manager mode
Main agent:
- clarify goal
- break work into tasks
- assign one technical subtask to Codex
- validate output and sequence next step

Codex:
- inspect repo
- implement subtask
- summarize diff, risks, tests

### 2. Skill review
Main agent:
- decide whether the skill is worth looking at
- decide whether the workflow fit is acceptable
- make final install/no-install call

Codex:
- inspect package contents
- compare docs vs files
- identify dependency/risk complexity

### 3. Environment problem
Main agent:
- decide what counts as truly fixed
- check shell vs gateway vs cron acceptance

Codex:
- inspect config and logs
- compare candidate fixes
- identify likely cause

## Anti-patterns
- Do not delegate the entire conversation.
- Do not let Codex define the user's priorities.
- Do not call something fully fixed just because Codex found a plausible path.
- Do not delegate if the coordination cost is larger than the task itself.
