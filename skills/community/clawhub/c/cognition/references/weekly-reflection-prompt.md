# Weekly Reflection — Analysis and Recommendations Only

Schedule: `0 4 * * 0` (Sunday 4 AM)
Recommended model: any model with reliable tool use
Timeout: 600 seconds

## Prompt

```text
You are running the Weekly Reflection.

This workflow analyzes the past week and produces recommendations.
It does **not** directly edit durable memory, procedures, AGENTS.md, or other operating files.

## Goal
Review the week, identify patterns, and emit proposals humans can approve.

## Read
1. `memory/YYYY-MM-DD.md` for the last 7 days
2. `MEMORY.md` if present
3. `memory/FUTURE_INTENTS.md` if present
4. `memory/procedures/index.yaml` if present
5. `memory/KNOWLEDGE_MAP.md` if present
6. `memory/bank/cross-references.md` if present
7. `memory/meta/gap_tracker.json` if present
8. previous `memory/summaries/YYYY-WNN.md` if present

## Output
Write a weekly report to:
`memory/summaries/YYYY-WNN.md`

If a report already exists, append a new timestamped reflection block instead of overwriting it.

## Required sections
- Weekly summary
- Recurring themes
- Repeated failures / friction
- Commitment review
- Procedure review
- Confidence / gap review
- Proposed diffs
- Recommendations requiring human approval

## Proposed diff format
When suggesting changes, emit proposals like:
- `Target:` file path
- `Reason:` why the change is recommended
- `Evidence:` cite the relevant daily logs or files
- `Proposed diff:` a small patch, replacement block, or exact text snippet

Do not apply the diff yourself.

## Backup rule for any later mutation workflow
If a separate reviewed workflow chooses to apply a recommendation, it must first create timestamped backups of every file it changes.

## Analysis rules
- Prefer pattern detection over one-off noise
- Do not invent missing evidence
- No automated confidence decay by default
- Use coarse confidence bands (🟢 / 🟡 / 🔴) if discussing knowledge quality
- If evidence is ambiguous, mark the recommendation `[NEEDS_REVIEW]`

## Procedure review rules
- New procedures begin as `draft`
- Recommend promotion to `reviewed` after human review or 3 successful uses
- Recommend promotion to `trusted` only after repeated reliable use
- Flag weak or stale procedures, but do not delete them automatically

## Knowledge / gap review rules
- Surface recurring gaps from `memory/meta/gap_tracker.json`
- Keep `last_verified` where available
- Confidence changes require evidence, not vibes

## Rules
- Do not modify `SOUL.md` or `AGENTS.md` directly
- Do not directly edit `MEMORY.md`, `memory/FUTURE_INTENTS.md`, `memory/KNOWLEDGE_MAP.md`, or procedures in this workflow
- Produce analysis + recommendations only
- If the week was quiet, write a brief report and exit

## Critical: tool use required
You must use read and write tools.
Do not describe the work without producing the report.
```
