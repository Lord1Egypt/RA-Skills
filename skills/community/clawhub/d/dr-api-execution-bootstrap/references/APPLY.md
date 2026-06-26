# Apply checklist — dr-api-execution-bootstrap

Use this when the user says things like:
- Apply dr-api-execution-bootstrap to this workspace
- Enable direct API execution by default
- Bootstrap this workspace for fast API chaining

## Goal
Make direct in-session API execution the default workflow for the workspace.

## Steps
1) Inspect existing startup/default files:
- `AGENTS.md`
- `MEMORY.md`
- any workspace bootstrap/instruction files

2) Persist these rules:
- direct execution first
- no subagents unless explicitly requested
- one upfront preflight only
- fast mode single-run chain
- concise responses
- blocker-only reporting when execution is impossible

3) Patch existing files surgically.
- Do not erase unrelated user instructions.
- Do not duplicate sections if already applied.

4) Validate.
- Prefer a small real dev test if safe.
- Otherwise do the strongest safe validation available.

5) Final response:
- `Configured and validated`
- or `Configured, but blocked by: <reason>`
