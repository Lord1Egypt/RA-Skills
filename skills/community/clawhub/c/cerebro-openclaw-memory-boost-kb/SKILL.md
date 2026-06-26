---
name: cerebro-first
description: Enforce a Cerebro-first operating protocol for continuity across sessions. Use when resuming prior work, handling "what did we do before" questions, making operational decisions, or executing company/project tasks where rules may already exist. Requires: domain identification, reading authoritative Cerebro docs before action, citing decision basis, and writing durable updates back to Cerebro + daily memory.
version: 2.1
---

# Cerebro-First v2.1

## Startup Gate (mandatory)

Before any substantive action, run this sequence:

1. Identify domain:
   - `companies/bda`, `companies/mission`, `companies/bms`, `companies/clawstation`, `personal/trading`, or `operations/*`.
2. Read source docs:
   - Domain `COMPANY.md` first (if present), then the most specific `SKILL.md`/runbook.
3. Read continuity logs:
   - `memory/YYYY-MM-DD.md` for today and yesterday.
4. Build a short **Known State**:
   - Last completed step
   - Current blockers
   - Next action

Do not skip this gate unless the user explicitly requests a one-shot answer unrelated to operations.

## v2.1 Retrieval Model (lightweight)

Use tag-first retrieval with the index at `references/cerebro-index-v2.1.md`:

1. Pick 1-2 tags from the request (examples: `#bms`, `#clawstation`, `#trading`, `#cron`, `#jira`, `#incident`).
2. Open the mapped source-of-truth files from the index.
3. Execute only from explicit documented rules.
4. If missing guidance, create/update the authoritative doc before execution.

## v2.1 Domain Router

Use `references/domain-routing-v2.1.md` to route tasks:

- Company execution → `cerebro/companies/<name>/...`
- Cross-company process/infrastructure → `cerebro/operations/...`
- Personal investing/trading → `cerebro/personal/trading/...`
- Incident handling → `cerebro/runbooks/...`
- Tool specifics → `cerebro/vendors/...`

## Decision Rule

Pass the **"where does it say that?"** test before acting.

- Every action must map to an explicit Cerebro path/section.
- If no authoritative doc exists:
  1) create the missing Cerebro doc first,
  2) add minimal executable guidance,
  3) then execute.

## Conflict Resolution

If chat instruction conflicts with Cerebro:
1. Flag the conflict briefly.
2. Ask for confirmation.
3. Propose exact doc update path.
4. After confirmation, update Cerebro and proceed.

Priority order: **Cerebro > SOUL/AGENTS > MEMORY > chat history**.

## Write-Back Protocol (same action)

When a decision/rule/process changes:

1. Update authoritative Cerebro file.
2. Append to `memory/YYYY-MM-DD.md` with:
   - What changed
   - Why it changed
   - Exact file path updated

Never leave process changes only in chat.

## Continuity on "Continue Previous Work"

Always return a 4-line snapshot before proceeding:

- **Context:** project/domain
- **Last Done:** durable completed step
- **Open Items:** pending work
- **Next Step:** immediate action now

## Missing-Doc Auto-Create Protocol

If needed doc is missing:

1. Create file in correct Cerebro path.
2. Use `references/missing-doc-template.md`.
3. Backfill from recent memory notes only after creating structure.

## Required output sections when this skill is used

- **Source of Truth Used:** exact Cerebro paths read
- **Decision Basis:** 1-3 bullets of applied rule(s)
- **Write-Back:** updated files, or `No durable updates needed.`

## Reference Files

- `references/startup-checklist.md` — fast pre-action checklist
- `references/decision-log-template.md` — standard decision record format
- `references/missing-doc-template.md` — template for new Cerebro docs
- `references/cerebro-index-v2.1.md` — lightweight tag index
- `references/domain-routing-v2.1.md` — task routing matrix
- `references/scenario-profiles-v2.1.md` — setup profiles for solo/agency/multi-agent teams
- `references/enforcement-checklist-v2.1.md` — pre-done anti-drift checks
- `references/done-schema-v2.1.md` — proof-based status output schema
