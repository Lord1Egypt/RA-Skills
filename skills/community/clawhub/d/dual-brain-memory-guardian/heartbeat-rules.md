# Heartbeat Rules (Dual-Brain)

Use heartbeat to keep `~/dual-brain-memory-guardian/` consistent while avoiding destructive edits.

## Source of Truth

- Keep workspace `HEARTBEAT.md` snippet minimal.
- Keep mutable run markers in `~/dual-brain-memory-guardian/heartbeat-state.md`.
- Keep raw historical episodes in Pinecone DEEP memory instead of local compaction-heavy logs.

## Start of Every Heartbeat

1. Ensure `~/dual-brain-memory-guardian/heartbeat-state.md` exists.
2. Write `last_heartbeat_started_at` immediately (ISO 8601).
3. Read previous `last_reviewed_change_at`.
4. Scan `~/dual-brain-memory-guardian/` for local changes after that timestamp, excluding `heartbeat-state.md`.
5. Read `./operations.md` for the latest trigger contract and command names.
6. Verify enforced trigger commands still exist (`memory:session-start`, `memory:auto-session-start`, `memory:on-correction`, `memory:on-task-complete`, `memory:auto-task-complete`).
7. Review key memory files (`memory.md`, `corrections.md`, `reflections.md`, `index.md`) before deciding `HEARTBEAT_OK`.
8. Run weekly or scheduled vector digest query for last 7 days (`correction`, `reflection`) from Pinecone.

## If Nothing Changed

- Set `last_heartbeat_result: HEARTBEAT_OK`.
- Append short note: no material local change and no promotable digest signal.
- Return `HEARTBEAT_OK`.

## If Something Changed

Do conservative maintenance only:

- Refresh `index.md` if file counts or references drift.
- Keep confirmed Markdown rules intact.
- Promote repeated DEEP signals into concise HOT/WARM Markdown rules only when evidence is strong.
- Update `last_reviewed_change_at` only after successful review.

## Digest Behavior (Vector-Assisted)

- Do not destructively compress raw event history from Pinecone.
- Query recent DEEP memory and detect repeated corrections (for example, 3+ similar events), prioritizing records where `promoted_to_markdown != true`.
- Promote only the distilled rule to Markdown.
- After successful Markdown promotion, mark the source event as promoted (for example via `memory:mark-promoted`).
- Keep raw episodes in Pinecone for future audit and retrieval.

## Safety Rules

- Most heartbeat runs should do little or nothing.
- Prefer append/update over rewrite.
- Never delete uncertain text from Markdown.
- Never reorganize files outside `~/dual-brain-memory-guardian/`.
- If context is ambiguous, write a follow-up suggestion instead of forcing a change.

## State Fields

Keep `~/dual-brain-memory-guardian/heartbeat-state.md` lightweight:

- `last_heartbeat_started_at`
- `last_reviewed_change_at`
- `last_vector_digest_at`
- `last_heartbeat_result`
- `last_actions`

## Behavior Standard

Heartbeat should improve trust, not create churn.
If no clear rule is violated, do nothing.
