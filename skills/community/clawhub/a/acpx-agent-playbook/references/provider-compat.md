# provider and agent compatibility notes

## Current practical conclusion

When the user needs real deliverables such as `.pptx`, reports, generated assets, or local file output, choose the agent by **fresh artifact proof in the current workspace**, not by brand preference alone.

Current workspace status after 2026-03-16 re-validation:

- `acpx codex` is the safest default delivery path.
- `acpx claude` is no longer blanket-blocked in this workspace.
- Claude has now passed:
  - fixed-text response
  - minimal file write
  - real PPTX generation and validation
- The key unblocker was **acpx permission configuration**, not prompt wording alone.

Practical rule:

- If an agent has freshly passed text + minimal write + real artifact generation, it is acceptable for modest delivery work.
- If the task is deadline-sensitive, long-running, or quality-critical, prefer the agent with the strongest recent artifact track record in this environment.
- In this workspace today, that still means **Codex by default**, with **Claude now acceptable after re-verification**.

## Agent selection heuristics

Use these default heuristics unless newer evidence overrides them:

- **Codex**: safest default for multi-step coding and artifact delivery
- **Claude**: acceptable when recently re-verified, especially for presentation/report style work
- **Other agents**: treat as unverified until they pass the same smoke-test ladder

## Fast diagnosis order

When checking a new agent, provider, or relay for delivery work, test in this order:

1. simple fixed-text response
2. minimal file-write task
3. one real artifact task
4. only then trust it for larger multi-step deliverables

If steps 1-3 do not all pass, do not treat that path as production-ready for PPT/report generation.

## Workspace-specific notes for Claude

Observed historical failure modes for `acpx claude` in this environment included:
- `403` with no body
- `401` quota exhausted
- `500 invalid claude code request`
- timeouts / model unavailable

These failures can reflect provider compatibility, relay behavior, quota, or permission setup rather than prompt quality alone.

## ACPX permission notes

Current acpx config behavior matters:

- `nonInteractivePermissions` accepts `deny` or `fail` in this environment.
- Do not assume a value like `allow` is supported.
- In this workspace, Claude file creation was blocked until `~/.acpx/config.json` was changed from:
  - `defaultPermissions: "approve-reads"`
  - `nonInteractivePermissions: "fail"`
  to:
  - `defaultPermissions: "approve-all"`
  - `nonInteractivePermissions: "deny"`
- If an agent can answer text but every write/edit/terminal tool request aborts, inspect acpx permission config before blaming the provider.

## Recommended fallback rule

If the chosen agent can answer text but cannot reliably write files, treat it as a Q&A path only and switch the deliverable task to the currently verified delivery agent.
