---
name: aegis-html-ledger
description: 'Use when project execution needs a durable, current local HTML record that another agent can resume from, with optional authorized cloud copies.'
disable-model-invocation: true
---

# Aegis HTML Ledger

Maintain a current execution record so another agent can resume the work if the
active session fails or becomes unavailable.

## Location and ownership

- Keep the primary HTML ledger in the project. Local-only operation is complete and supported.
- Make an iCloud or other cloud copy only when the operator's authorization covers this project's records, the destination account and folder, and the content being copied. Reuse that authorization while its scope still applies; choosing this skill alone does not authorize a cloud transfer.
- If that authorization is absent, keep the ledger local and record cloud sync as not enabled. A missing optional cloud copy must not block ordinary project work or a local handoff.
- Keep credentials, tokens, private conversations, personal records, and restricted project content out of cloud copies. Use authorized summaries and artifact references; do not copy referenced files or full transcripts by implication. Project disclosure restrictions take precedence over sync convenience.
- Reuse the active project or work-slice ledger. Do not create another ledger for every turn, command, or helper session.
- Update the project ledger first, then refresh an authorized cloud copy from that checkpoint. Identify the project ledger as the primary record.
- When cloud sync is enabled, keep the destination, authorized content scope, checkpoint, and freshness explicit. If copying fails or lags, preserve the project record and report the gap. A local copy does not prove propagation to other devices.
- Keep the ledger dependency-light. Treat it as execution and handoff state, not project canon unless explicitly promoted.

## Current work and resume state

Keep the ledger current throughout execution, not only at turn completion or
handoff. Before starting a work unit or an action that changes project state,
record what is about to run, its scope, and the last confirmed state. Update
immediately when the active work, result, status, or plan changes.

The active checkpoint must make clear:

- what is being worked on now and what is still in progress;
- the last confirmed result, validation, and current state;
- changes made or needed to the plan, including contradictions and unresolved proof gaps;
- what remains and the exact next safe action for a replacement agent;
- references needed to locate the work and its existing artifacts.

Distinguish intended, in-progress, completed, failed, and unverified actions.
If a session fails during an action, a replacement agent must recheck its
actual outcome before repeating it. Do not mark an intended result as achieved.

## Handoff compatibility

Use the current ledger as an input to the selected handoff skill. Reference
existing artifacts rather than duplicating their contents. Keep that skill's
output location, disclosure rules, delivery, and acceptance checks:

- `handoff` (Matt): the compact handoff document stays in the OS temporary directory; the project ledger remains durable in the project.
- `openclaw-handoff`: retain portable context and its path restrictions; include filesystem paths only when that skill's operator-requested exception applies.
- `continuity-handoff`: reference the ledger in the continuity packet and preserve its identity, acknowledgement, Recall, Project Binding, and acceptance requirements. A current ledger alone does not satisfy those gates.
- When `openclaw-team-handoff` is selected, local files are not assumed reachable from the Gateway; use its authorized transport and handoff contract.

## Completion criteria

Another agent can identify the active work and resume point without rereading
the whole chat. The record distinguishes confirmed outcomes from interrupted
or unverified work. Cloud sync is either not enabled or has an authorized
destination, content scope, and known copy freshness.

## Red flags

- The active operation exists only in chat or the agent's context.
- An interrupted action is recorded as completed without checking its result.
- A cloud copy is made without project and destination authorization, or is stale but presented as current.
- HTML polish is treated as validation, or the ledger duplicates project canon.

## Boundary

Use this for ongoing project execution, not standalone ceremony for a tiny
one-shot answer. This skill maintains execution state. It does not define CoS organization or
require `aegis-communication-discipline`; the ledger stays current whether or
not that optional communication skill is in use. Selected handoff skills keep
their own invocation and authorization boundaries.
