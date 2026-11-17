# Migrations And Cutovers — Changing Data And Traffic Without Downtime

Two families with the same discipline: schema/data changes inside a running system, and cutovers that move traffic to a new destination. Both are defined by their point of no return.

**Before planning either**, read `## Delivery Setup` in `~/Clawic/data/devops/memory.md` (the database engine and version), plus `## Services` and `## Environments` (the deploy strategy, the environment chain), plus `~/Clawic/data/domains/domains.md` for the current TTL and registrar of any hostname you are about to move. **Read `releases/<year>.md`** to know which artifact is live: the rollback target must be able to run against the schema you are about to create.

**Contents:** [Expand / Contract](#expand--contract) · [Locks And Online DDL](#locks-and-online-ddl) · [Backfills](#backfills) · [Dual-Write Migrations](#dual-write-migrations) · [DNS And Traffic Cutovers](#dns-and-traffic-cutovers) · [The Cutover Plan](#the-cutover-plan) · [Rollback Boundaries](#rollback-boundaries)

## Expand / Contract

Three deploys, never one (SKILL.md Rule 5). At every moment, the version currently deployed *and* the version you would roll back to must both work against the current schema.

| Step | Schema change | Code change | Reversible? |
|---|---|---|---|
| 1. Expand | Add the new column/table/index, nullable, with no constraint that old writes violate | Old code untouched; new code (if deployed) writes both old and new | Yes — drop the addition |
| 2. Migrate | None | Backfill old rows; reads prefer new, fall back to old | Yes — stop the backfill |
| 3. Contract | Drop the old column, add the NOT NULL / constraint | Only the new path remains | **No** — this is the point of no return |

- Renaming a column is expand/contract, always: add new → dual-write → backfill → switch reads → drop old. A direct rename breaks every running instance of the old code within the deploy window.
- Adding a constraint is two steps: add it as NOT VALID (or the engine's equivalent) so new rows are checked immediately, then validate existing rows without holding a write lock.
- Deleting data is expand/contract too: stop writing → verify nothing reads it → keep it for a stated period → drop. Recovering a dropped column from a backup costs an hour of restore, minimum (`recovery.md`).
- **Contract cannot ship in the same release as the last reader.** Wait until the previous release is out of the fleet and out of your rollback window.

## Locks And Online DDL

The failure mode is not a slow migration, it is a lock queue: one blocked DDL statement blocks every subsequent query on that table, and the connection pool fills in seconds.

- Set a short lock timeout on migration sessions (a few seconds) and retry. Without it, the migration waits behind a long-running query while every new query waits behind the migration — the classic "the migration took the site down and the migration hadn't even started".
- `postgres >=11` adds a column with a non-volatile default without rewriting the table; older versions rewrite it, which locks for the duration. Verify the engine version before assuming the cheap path.
- Index creation must be concurrent (`CREATE INDEX CONCURRENTLY` in Postgres, online DDL in MySQL 8) — it takes longer, does not block writes, and can leave an invalid index behind if it fails, which must be dropped before retrying.
- MySQL 8 `ALGORITHM=INSTANT` covers some column additions; anything else copies the table. Check the algorithm the engine chose rather than the one you asked for.
- Long transactions block DDL and bloat replicas. Check for open transactions and replica lag *before* starting, not after.
- Migrations run as their own step with their own timeout, never inside application startup — a boot-time migration means every replica races to run it and a failed migration becomes a crash loop.

## Backfills

Never one statement over the whole table.

- Batch by primary key range, commit each batch, sleep between batches. Size the batch so each transaction stays well under a second; a common starting point is 1,000-10,000 rows, tuned against observed lag.
- **Throttle on replica lag, not on wall clock**: pause when lag exceeds your tolerance (often 1s) and resume when it recovers. A backfill that outruns replication silently breaks every read replica consumer.
- Make it resumable and idempotent: store the last processed key, and write only rows that still need it. A backfill that cannot resume will be restarted from zero at the worst moment.
- Log progress and estimate completion from measured throughput: `remaining_rows ÷ rows_per_second`. A backfill with no ETA gets abandoned mid-way and leaves the system in the dual-write state forever.
- Verify before contract: count rows where the new field is still null, and compare a sample of old vs new values. Contract on an unverified backfill silently deletes data.

## Dual-Write Migrations

Moving a store (or a service) while it stays live:

1. **Write both, read old.** Both destinations receive every write; the old one remains the source of truth. Failures writing to the new store are logged, never fatal.
2. **Backfill history**, then reconcile: compare counts and a sampled diff until the mismatch rate reaches zero and stays there.
3. **Read new, write both.** The moment of truth; the old store is still current, so rollback is one config flip.
4. **Stop writing old**, after a stated soak period. This is the point of no return.

The reconciliation step is the one teams skip and the one that finds the bug — dual-write always has a race somewhere, and the diff is how you learn where.

## DNS And Traffic Cutovers

- **Lower the TTL before you need it.** A record at 86400s TTL must be reduced to 60s at least one full old-TTL ahead (i.e. 24h) — the lowering itself only propagates at the old rate.
- **Cache does not respect you.** Keep the old destination serving for at least 24h after the switch: some resolvers, some corporate proxies, and older JVM defaults cache far past the TTL. Measure residual traffic on the old target instead of guessing.
- Load-balancer or proxy switching beats DNS whenever it is available: seconds instead of hours, and reversible at the same speed.
- For an apex domain and a moving target, alias-type records at the provider avoid the "no CNAME at the apex" trap; the same reversibility rules apply.
- Certificates before traffic: issue and install the certificate on the new destination, verify the chain from outside your network, then move. Certificate expiry dates go in `~/Clawic/data/domains/domains.md` and their renewal cadence in `## Due`.
- Clients that pin (mobile apps, embedded devices, partner integrations) do not follow DNS at all. Enumerate them before assuming a cutover is complete.

## The Cutover Plan

Write it as an artifact before the day, and read it during. Minimum sections:

| Section | Content |
|---|---|
| Preconditions | TTL lowered on <date>, backups verified restorable, freeze on unrelated changes, owner and comms channel named |
| Sequence | Numbered steps with the expected observable after each, and who runs it |
| Point of no return | The exact step after which rollback becomes roll-forward, called out in the text |
| Rollback | Per-step: what to undo and how long it takes; who decides |
| Verification | The checks that say it worked, from outside the system |
| Aftercare | Residual-traffic check on the old destination, decommission date, records to update |

A cutover without a written point of no return is a cutover where somebody discovers it live.

## Rollback Boundaries

| Change | Reversible until |
|---|---|
| Code deploy | Always, while the previous artifact exists (`deploys.md`) |
| Expand step | Until contract |
| Backfill | Always, if the old field still holds truth |
| Contract step | Not reversible without a restore |
| Dual-write cutover | Until writes to the old store stop |
| DNS switch | Until the old destination is decommissioned |
| Deletion of data with no backup | Never — verify the backup restores first (`recovery.md`) |

**Write in the same turn**: the cutover plan and the migration procedure become `~/Clawic/data/devops/artifacts/<kebab-name>.md` with their `## Boxes` line, including the point of no return and the measured durations once it ran. The release row (including the migration step it carried) goes in `releases/<year>.md`; a hostname, TTL, or certificate change goes in `~/Clawic/data/domains/domains.md`; anything the cutover taught that would be re-derived next time goes in `## Pain Points` of `memory.md` (`memory-template.md`).
