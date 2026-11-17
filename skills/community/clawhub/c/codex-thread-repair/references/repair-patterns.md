# Supported and unsupported repair patterns

## Supported: ordinal regression with a stale open turn

The automatic repair is allowed only when all of these are true:

- The rollout is valid JSONL and its `session_meta.payload.id` matches the selected thread.
- The rollout resolves to an absolute path under the selected Codex home's `sessions/` directory.
- Every source record has an integer top-level `ordinal`.
- There is exactly one non-monotonic boundary.
- Ordinals before the boundary are contiguous from zero.
- Ordinals after the boundary are internally contiguous.
- Exactly one open turn began before the boundary and later turns began after it.
- No record after the boundary still belongs to the stale open turn.
- Every lifecycle event has one non-empty turn ID; starts and endings are unique and paired except for the one stale open turn.
- Boundary, start, and completion timestamps are timezone-aware and chronologically ordered.
- Inserting one `turn_aborted` event and shifting the later ordinals produces a unique sequence contiguous from zero.

The patch inserts the missing abort immediately before the regression boundary, then changes only the top-level ordinal values in later records. It compares normalized hashes to prove that original record bodies did not change.

## Healthy or currently active

- `healthy`: ordinals are contiguous and all started turns have a completion or abort event. No mutation is needed.
- `active_latest_turn`: the only open turn is the newest turn and no later turn supersedes it. This may be a currently running task or a normal interrupted latest task; do not synthesize an ending automatically.

## Unsupported: stop and report

Do not automatically mutate when diagnosis finds any of the following:

- More than one ordinal regression.
- Gaps or reordering inside either ordinal segment.
- Multiple stale open turns.
- A stale turn referenced again after the proposed boundary.
- Missing or malformed session metadata.
- Empty or duplicate turn IDs, orphan ending events, malformed timestamps, or negative durations.
- A missing rollout file or a database row without a usable path.
- A provider mismatch, missing project assignment, moved workspace path, or missing SQLite thread row.

Use `recover-codex-project-chats` for the broader state/database cases. For a novel rollout pattern, preserve the source, collect the exact event sequence, and design a repair on a copy before requesting offline mutation.

Rollback accepts only a manifest whose thread ID still resolves to the same rollout under the selected Codex home's `sessions/` directory. This prevents a copied or edited manifest from overwriting an unrelated path.
