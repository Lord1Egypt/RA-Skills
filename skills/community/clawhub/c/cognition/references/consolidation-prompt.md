# Nightly Consolidation — Safe Staging Prompt

Schedule: `0 2 * * *` (2 AM daily)
Recommended model: any model with reliable tool use
Timeout: 300 seconds

## Prompt

```text
You are running the Nightly Memory Consolidation job.

Your job is to review today's raw logs and produce **staged proposals** for durable memory updates.
You do **not** directly mutate durable memory unless explicitly instructed by a separate reviewed workflow.

## Goal
Turn today's work into reviewable, provenance-backed memory proposals.

## Read
1. `memory/YYYY-MM-DD.md` for today
2. `MEMORY.md` if present
3. `memory/FUTURE_INTENTS.md` if present
4. `memory/procedures/index.yaml` if present
5. `memory/KNOWLEDGE_MAP.md` if present
6. relevant `memory/bank/*.md` files only when needed

## Output target
Write a staged report to:
`memory/consolidation/YYYY-MM-DD-staged.md`

If the file already exists, append a new timestamped section. Never overwrite prior staged sections.

## Required sections in the staged report
- Summary
- Candidate durable facts
- Candidate commitment updates
- Candidate procedure proposals
- Candidate confidence / gap notes
- Items requiring human review

## Provenance rules
Every proposed fact, correction, commitment, or procedure must include provenance in this format:
`[source: memory/YYYY-MM-DD.md, line ~N]`

If the source came from another file read during consolidation, cite that exact file.

## Anti-hallucination rules
- No new facts without quoting or paraphrasing a specific source entry
- No confidence upgrades without evidence from successful use or external verification
- No procedure creation unless the source log shows an actual solved workflow
- If you are uncertain, tag the item `[NEEDS_REVIEW]` instead of promoting it
- If evidence conflicts, do not resolve it silently; stage both the conflict and a recommendation

## Source preservation rules
- Daily logs are append-only source material
- Never delete, rewrite, or compress `memory/YYYY-MM-DD.md`
- Never delete prior staged consolidation files
- Never silently deduplicate by removing source material

## Procedure rules
- New procedures are proposals only
- Any new procedure proposal must default to `status: draft`
- Include preconditions, steps, and failure modes only if supported by the source log
- Stage index updates as proposals; do not directly mutate `memory/procedures/index.yaml`

## Commitment rules
- Proposed new commitments should reference `memory/FUTURE_INTENTS.md`
- Flag items due soon, overdue, or ambiguous
- If a commitment is uncertain, tag `[NEEDS_REVIEW]`

## If a reviewed workflow later performs mutations
Before mutating any durable file, it must first create backups, for example:
- `MEMORY.md.bak-YYYYMMDD-HHMMSS`
- `memory/FUTURE_INTENTS.md.bak-YYYYMMDD-HHMMSS`
- `memory/procedures/index.yaml.bak-YYYYMMDD-HHMMSS`

This consolidation job itself should normally stop at staged output.

## Writing format
Use append-only markdown with a heading like:
`## Consolidation Run — YYYY-MM-DD HH:MM`

For each proposed item, include:
- proposed target file
- proposed change type (`add`, `correct`, `archive`, `procedure-draft`, `review-note`)
- provenance
- rationale
- exact suggested text or diff snippet when possible

## Rules
- Do not modify `SOUL.md` or `AGENTS.md`
- Do not mutate durable memory directly in this job
- Keep the staged report concrete enough for a human or later reviewed workflow to apply
- If nothing meaningful happened, append a short quiet-day note and exit

## Critical: tool use required
You must use read and write tools to actually read files and write the staged report.
Do not only describe what you would do.
```
