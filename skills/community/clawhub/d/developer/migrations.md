# Schema and Data Migrations

Code deploys are reversible in a minute. Data changes are not — a dropped column, a bad backfill, or a lock on a hot table is the class of mistake that produces an incident with no rollback (SKILL.md Rule 8).

**Before writing a migration**, read `## Open Threads` in `~/Clawic/data/developer/memory.md` — an expand-contract sequence someone left half-finished is the most common reason a schema has two columns for one thing — and `## Gotchas` in the repo profile for the migration tool's local quirks.

## Expand, Migrate, Contract

Never change a column and the code that uses it in one deploy. Four releases, each individually revertible:

| Step | What ships | Revertible by |
|---|---|---|
| 1. Expand | Add the new column/table, nullable, no constraint, no default backfill on a large table | Dropping something nothing reads |
| 2. Dual-write | Code writes both old and new; reads still come from old | Reverting the code |
| 3. Backfill + switch reads | Backfill in batches, verify, then read from new | Reverting the read switch |
| 4. Contract | Stop writing old, then drop it — a separate release, after a bake period | Nothing; this is the irreversible one, and by now it is safe |

The bake period between 3 and 4 is at least one full business cycle plus your backup retention window, so that a restore from before the change is still compatible with the running code.

Rename = expand + contract, never `RENAME COLUMN` in a live system. Type change = same. Making a column `NOT NULL` = backfill, then add the constraint (validate separately where the engine supports it).

## Zero-Downtime Rules

- **A migration must be safe against both the old and the new code**, because during a rolling deploy both are running. Additive-only changes satisfy this by construction.
- **Never take a long lock on a hot table.** Know which operations rewrite the table in your engine and which are metadata-only; in modern Postgres, adding a nullable column with no default is instant, adding an index without `CONCURRENTLY` locks writes for its whole build.
- **Set a lock timeout on the migration session** (a few seconds) so a blocked migration fails fast instead of queueing every query behind it. A migration waiting on a lock takes the site down more often than the migration itself.
- **Separate schema migration from data migration.** Schema in the deploy, data in a job you can pause, resume, and observe.
- **Constraints and indexes on large tables** get the concurrent/online variant, and get validated in a second step.

## Backfills

1. **Batch it**: 1,000-10,000 rows per batch, ordered by primary key, with a sleep between batches. One `UPDATE` over 50 million rows is one transaction, one lock, one bloated table, and one rollback you cannot interrupt.
2. **Make it resumable**: track the last processed id in a durable place, so a restart continues instead of starting over.
3. **Make it idempotent**: running it twice must be a no-op — `WHERE new_col IS NULL` rather than unconditional writes.
4. **Rate-limit against replica lag**, not against clock time. Watch lag between batches and back off; the readers fall over before the writer does.
5. **Verify before switching reads**: count mismatches between old and new, and inspect a sample by hand. A backfill that "finished" is not a backfill that is correct.
6. **Dry-run on a copy of production data.** Volume and shape are the whole difficulty; staging with 1,000 rows proves nothing.

Estimate honestly: `duration ≈ rows ÷ batch_size × (batch_time + sleep)`. Ten million rows at 5,000 per batch and 200 ms per batch with a 200 ms sleep is ~2,000 batches × 0.4 s ≈ 13 minutes of pure work — and hours in practice once replica lag pauses it.

## Data Fixes in Production

Everything here applies to the one-off "fix these 300 rows" too, and it is where the worst accidents happen:

- **Write the SELECT first**, run it, read the count. If the count surprises you, stop.
- **Wrap in a transaction** and check the affected-row count before committing, where the engine allows it.
- **Every `UPDATE` and `DELETE` has a `WHERE`** and a `LIMIT` where supported. A `WHERE` clause that came from copy-paste gets re-read out loud.
- **Snapshot what you are about to change** into a scratch table first — the cheapest undo that exists.
- **Governed by `risk_confirm`**: with it true, any destructive statement is emitted with an explicit confirmation step and the expected row count, never inside a copy-paste block.

## Rollback of a Migration

- Every migration has a `down` that has been *run*, not just written. An untested down is documentation.
- The real rollback of a destructive step is a restore, so know your recovery point before the step, not after.
- Once the contract step has run, the rollback path for the code that needs the old column is gone. That is why contract ships last and alone.

## Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| Migration and dependent code in one deploy | Rolling back one leaves the other broken | Expand-contract across releases (Rule 8) |
| `ALTER TABLE` on a hot table at peak | Lock queue takes the site down, not the alter | Off-peak, with a lock timeout, using the online variant |
| One big `UPDATE` for a backfill | One transaction, long lock, table bloat, no progress visibility | Batch, resumable, idempotent, rate-limited |
| Testing on an empty staging database | Every problem here is a volume problem | Copy of production data, or generated data at real scale |
| Adding a column with a default on a large table | Rewrites the whole table in older engines | Add nullable, backfill in batches, then set the default |
| Trusting the ORM's generated migration | It optimizes for expressing your model, not for a live table | Read the emitted SQL before running it |
| Deploying a migration without checking the down path | Discovered during the incident | Run up, down, up locally against real-shaped data |
| Leaving the contract step "for later" | Two sources of truth forever, and the next developer writes to the wrong one | `## Open Threads` until it ships, with a date |
| A data fix run from a shell with no record | Nobody can reconstruct what changed | The statement, the row count and the date go in `releases/<year>.md` |

## Write Down What Ran

- **Every migration and backfill** → a row in `~/Clawic/data/developer/releases/<year>.md`: date, what it did, the rollback target, and whether the **contract step is still pending** (`memory-template.md`).
- **A pending contract step** also goes in `## Open Threads` of `memory.md`, and stays there until it ships. This pair is the mechanism that stops half-finished schema changes from becoming permanent.
- **A non-obvious migration plan** — the batch size that worked, the lag threshold, the verification query → `artifacts/migration-<table>.md`, with its `## Boxes` line, read whenever the same table is touched again.
