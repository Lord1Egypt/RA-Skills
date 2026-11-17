# Databases — Cloud SQL, AlloyDB, Spanner, Firestore, Bigtable, Memorystore

Choosing wrong here is the most expensive mistake on the platform, because three of these have a capacity floor and two have a key design that cannot be changed after data lands.

**Contents:** [Choosing](#choosing) · [Cloud SQL](#cloud-sql) · [Connections Are the Real Limit](#connections-are-the-real-limit) · [HA, Replicas, and Backups Are Three Things](#ha-replicas-and-backups-are-three-things) · [AlloyDB](#alloydb) · [Spanner](#spanner) · [Firestore](#firestore) · [Bigtable](#bigtable) · [Memorystore](#memorystore) · [Migration and Restore Drills](#migration-and-restore-drills)

## Choosing

| Need | Pick | Because |
|---|---|---|
| Relational, normal scale | Cloud SQL for PostgreSQL | Managed Postgres, no floor beyond the smallest tier, everything works |
| Relational, analytics against live OLTP | AlloyDB | Columnar engine over the same rows; the reason to pay more |
| Relational, global writes with strong consistency | Spanner | The only one that does it; priced from a real minimum |
| Document, serverless, mobile/web SDKs | Firestore | Scales to zero, offline sync, per-operation pricing |
| Wide-column, huge scale, single known access pattern | Bigtable | Per-node floor; the row key is the only index |
| Cache, sessions, rate limits | Memorystore | Redis/Valkey semantics, per-hour capacity |
| Anything else | Cloud SQL for PostgreSQL, and revisit when a limit is measured | Reversible; a floor-priced database is not |

Two decisions worth stating explicitly to the user: **Bigtable and Spanner bill from a minimum capacity**, so a small workload pays a subscription rather than a usage bill; and **Firestore's cost is per read, write and delete**, so a design that reads a collection to render a page multiplies traffic into money in a way row-based pricing does not.

## Cloud SQL

- **Editions.** Enterprise is the baseline; Enterprise Plus adds a higher availability target, a data cache, and near-zero-downtime maintenance, at a higher price. The upgrade is worth pricing when maintenance restarts are the pain point, not by default.
- **Storage grows and never shrinks.** Automatic storage increase prevents an outage and permanently raises the bill. Shrinking requires a dump and restore into a new instance. Alert on disk usage and treat every increase as a decision.
- **Maintenance windows** are when the instance restarts. Set one, or Google picks. Enterprise Plus reduces the disruption but does not remove the event.
- **Private IP is a creation-time network decision.** Which VPC an instance is reachable from is set when it is created, via the service networking connection; moving it later means a new instance (`networking.md`).
- **Public IP with authorized networks is not a security posture.** Use private IP plus `constraints/sql.restrictPublicIp`. Where a public path is unavoidable, the Auth Proxy provides IAM-authenticated, encrypted access without opening a network range.
- **Flags, not `postgresql.conf`.** Configuration is set through database flags; some require a restart, and a handful of Postgres settings are simply not exposed. Check availability before designing around a parameter.
- **Query tuning belongs to `pg`** — this file covers the platform. Cloud SQL exposes Query Insights, which is the fastest path from "the database is slow" to the offending statement.

## Connections Are the Real Limit

The most common Cloud SQL outage: a serverless front end exhausts the connection ceiling and every request fails at once.

- The ceiling scales with instance memory, not with a lookup table — a small tier has a small ceiling, and Postgres reserves several connections for superuser access on top.
- **Compute the peak before deploying**: `max_instances × concurrency_per_instance × connections_per_request`. A Cloud Run service at 100 instances × 80 concurrency, opening one connection per request, asks for 8,000 connections from an instance that allows a few hundred (`run.md`).
- **Pool inside the application first.** A per-instance pool with a small maximum turns instance count into a bounded multiplier instead of an unbounded one.
- **Then pool outside it.** PgBouncer in transaction mode, or a managed pooler, collapses many application connections into few database connections. This is what makes serverless plus Postgres viable at all.
- **The Cloud SQL Auth Proxy is not a pooler.** It provides IAM authentication and an encrypted tunnel; each proxied connection is still a database connection. Both are needed.
- The error to recognize: `remaining connection slots are reserved for non-replication superuser connections` — the ceiling is reached, not a network problem (`debug.md`).

## HA, Replicas, and Backups Are Three Things

Conflating them is how data gets lost with high availability enabled.

| Mechanism | Protects against | Does not protect against |
|---|---|---|
| Regional HA (synchronous standby in another zone) | Zone failure, instance failure, maintenance | Your `DROP TABLE`, which replicates in under a second |
| Read replica | Read load; can be promoted for regional disaster | Data corruption, which replicates; and promotion is one-way |
| Automated backups + PITR | Deletion, corruption, bad migration | Nothing — this is the actual recovery mechanism |
| Export to Cloud Storage | Provider-level loss, and the account being closed | Being slow to restore |

- **PITR requires the write-ahead logs to be retained**, and the retention window is a setting with a cost. Know the window before an incident, because it defines the worst case.
- **Backups are attached to the instance.** Deleting the instance deletes them unless an export exists elsewhere. Enable deletion protection at creation, and keep at least one export in a bucket with its own retention.
- **Cross-region disaster recovery** is a cross-region read replica plus a documented promotion procedure — and the procedure has to include DNS or connection-string changes, which is the part everyone forgets until they time it.
- The only trustworthy claim about recovery time is one you measured. Run a restore into a scratch instance quarterly, time it, and record the result in `deploys/<year>.md` under `## Restore Drills`, along with what was missing (`memory-template.md`).

## AlloyDB

Postgres-compatible, with a columnar engine that keeps hot columns in memory for analytical queries against the same live rows.

- The case for paying more than Cloud SQL: dashboards or reports running against operational data, where the alternative is an ETL pipeline into a warehouse plus the staleness that comes with it.
- Not a BigQuery replacement. Warehouse-scale scans over terabytes belong in BigQuery; AlloyDB is for analytical queries over an OLTP-sized dataset (`bigquery.md`).
- Read pools scale reads independently of the primary, which is the other reason teams move from Cloud SQL.
- Migration from Cloud SQL is Postgres-to-Postgres and therefore straightforward, which also means the decision is reversible — a rare property in this file.

## Spanner

- Horizontally scalable, strongly consistent, SQL, with global replication. Nothing else in the list offers all four.
- **Priced from a minimum capacity**, so the entry cost is real and constant. Choosing Spanner for a workload that fits on one Postgres instance is a subscription with extra steps.
- **Schema decisions are structural**: interleaved tables co-locate child rows with their parent and are the mechanism that makes joins fast at scale. Choosing not to interleave, or interleaving the wrong way, is expensive to change later.
- **Monotonically increasing primary keys hotspot a split.** Use a UUID, a hashed prefix, or a reversed timestamp — the same rule as Bigtable and Firestore, for the same reason.
- The honest test for Spanner: do you need writes in more than one region with strong consistency? If not, Cloud SQL or AlloyDB is cheaper and simpler.

## Firestore

- Native mode for anything new. Serverless, scales to zero, priced per document read, write and delete plus storage and egress.
- **Cost follows document reads, so the data model is the cost model.** Rendering a list by reading 200 documents on every page load is 200 billed reads. Denormalize into summary documents; that duplication is the intended design, not a compromise.
- **Sustained writes to a single document cap around one per second.** Counters, leaderboards and "current total" documents hit this immediately. Shard the counter across N documents and sum them.
- **Sequential document IDs hotspot the index** because writes land in one lexicographic region. Use auto-generated IDs, UUIDs, or a reversed timestamp prefix.
- **Ramp traffic gradually** into a new collection rather than launching at full rate; the index splits need time to form.
- **Every query needs an index**, and composite queries need composite indexes that must be declared. The error names the index and offers to create it — capture those declarations in IaC rather than clicking them, or the next environment is missing them.
- Security rules are the access-control layer for direct client access, and they are code with the same review needs as anything else. A rule allowing authenticated reads across a collection is a data export path.

## Bigtable

- **One-node floor**, and nodes are not cheap, so the entry price is a monthly commitment. Correct when the workload is genuinely large and the access pattern is a key lookup or a range scan.
- **The row key is the only index there is.** Design it as the query: concatenate the fields you filter by, most-selective first, and reverse timestamps when you want newest-first ranges. Changing it later means rewriting every row.
- **Hotspotting is the failure mode.** Sequential keys — timestamps, auto-increment ids — put all writes on one tablet. Salt the prefix or field-promote.
- Column families are a storage and GC boundary; keep them few and set garbage-collection policies at creation.
- Key Visualizer shows the hotspot directly. Use it before theorizing about throughput.
- The realistic alternatives before committing: BigQuery for analytics, Firestore for document access, Memorystore for pure key-value at moderate scale.

## Memorystore

- Redis and Valkey, priced by capacity per hour — it bills while idle, so a cache sized for peak costs peak all month.
- Basic tier has no replica: a failure loses the cache. Standard tier adds a replica and a failover. For a pure cache, Basic plus a cold-start plan can be correct; for sessions or rate limits, it is not.
- **Design for the cache being empty.** A stampede when it restarts can take the database down; use jittered TTLs and request coalescing.
- Maintenance causes a failover, which drops connections. Clients need reconnect logic; the ones that do not have it fail once a month for reasons nobody attributes correctly.
- Scaling changes capacity, not the connection endpoint, but it is not instantaneous — plan it like a maintenance event.

## Migration and Restore Drills

- **Database Migration Service** handles the common paths (self-managed or another cloud's Postgres/MySQL into Cloud SQL or AlloyDB) with continuous replication and a cutover. The value is the replication; the risk is always the cutover window and the things outside the database — sequences, extensions, roles, and the application's connection strings.
- **Datastream** is the CDC product for streaming changes into BigQuery or Cloud Storage; it is a pipeline, not a migration (`pipelines.md`).
- **Test the restore, not the backup.** Restores fail on details nobody wrote down: a CMEK grant the new instance lacks, a private-IP peering range that no longer has space, a database flag set by hand two years ago, an extension not installed.
- Quarterly: restore a snapshot or a PITR into a scratch instance, time it end to end, delete it. Record the measured RTO and every missing detail in `deploys/<year>.md` under `## Restore Drills`, and put the next drill in `## Due`.

Whenever an instance is created, resized, given HA, or retired, update `## Current Infrastructure` in `~/Clawic/data/gcp/memory.md` in the same turn. A restore procedure that took a session to work out belongs in `~/Clawic/data/gcp/artifacts/runbook-restore-<instance>.md` with its `## Boxes` line, every secret replaced by its pointer (`memory-template.md`).
