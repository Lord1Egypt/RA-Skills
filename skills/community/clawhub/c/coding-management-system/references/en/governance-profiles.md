# Governance Profiles And Files 2.1

Choose the lightest profile that controls actual risk. File count is not rigor.

## Lite

Use for Small, local, reversible work with no independent QA need.

Required:

- `Docs/ACTIVE_PACKET.md`
- `Docs/LOOP_RUNS.jsonl`

Self-acceptance is possible only when `qa_required: false`, automatic and functional evidence both pass, and no protected boundary or material risk remains. Do not create Program, per-stage dispatch, handoff, or QA files.

## Standard

Use for Medium work, an important user flow, moderate uncertainty, or independent evaluation.

Required:

- `Docs/ACTIVE_PACKET.md`
- `Docs/LOOP_RUNS.jsonl`
- one final `Docs/QA_DECISION_{ID}.md`

Create one consolidated Work Order only when it adds stable scope or ownership. Terminal execution is `Ready for Independent Acceptance`; the execution agent cannot sign final acceptance.

## Full

Use for Large, multi-agent, architecture, migration, production, security, data-integrity, or release work.

Use only the durable artifacts that apply:

- `Docs/TARGET.md` and `Docs/ACCEPTANCE.md`
- `Docs/ACTIVE_PACKET.md`
- one Program and bounded Work Orders where ownership differs
- `Docs/LOOP_RUNS.jsonl`
- independent final QA decision
- `Docs/DECISIONS.md` for Owner choices and risk debt

Separate handoffs or rebaseline files exist only at real authority boundaries.

## File Creation Test

Create a file only when it owns at least one of these:

- a new authority or ownership boundary;
- an independent final QA decision;
- an Owner decision changing authorization;
- a cross-team handoff that the Packet cannot carry;
- an approved target rebaseline;
- an archive boundary.

Otherwise update the canonical Packet or append one Loop record.

## Anti-Bloat Rules

- Keep new Active Packets at roughly 120 lines or fewer.
- Keep exactly one immediate next action.
- A stage is not a Milestone, Work Order, handoff, or file.
- QA failure repairs the same Packet and Work Order.
- Stop expanding duplicate STATUS, NEXT, PENDING, COMPLETED, EVALUATION, and per-stage handoff files after migration.
- Link raw evidence and retain concise command summaries.
- Archive old material; do not rewrite history in bulk.

## Legacy Adoption

Use Legacy Bootstrap once. It indexes names, times, and sizes before reading selected current files. When coherent, create one Active Packet and route new execution evidence to `LOOP_RUNS.jsonl`. When conflicting, write nothing and ask for one consolidated Owner decision.
