# Setup — Elasticsearch

Read this on first use to load user preferences. Do not interview the user.

## Your Attitude

Elasticsearch is fast and forgiving right up to the point where it is neither. Most of the damage comes from decisions that cannot be undone later: a field type, a shard count, an index with no alias. Be direct about which choices are one-way doors, work from defaults for everything else, and never make someone answer a questionnaire before getting help.

## How To Load Preferences

1. Read `~/Clawic/data/elasticsearch/config.yaml` if it exists. Apply its values.
2. For anything absent, use the defaults from the Configuration table in `SKILL.md` — do not ask.
   - `deployment: self-managed`, `major_version: 8`, `license_tier: basic`, `client: dev-tools`, `target_shard_size_gb: 40`, `bulk_batch_mb: 10`, `default_replicas: 1`, `destructive_confirm: true`.
3. Read `~/Clawic/data/elasticsearch/memory.md` for prior context (their cluster, their workload, past incidents). Absence is fine; proceed without comment.

If the live cluster is reachable and the user is working against it, one `GET /` and one `GET /_cat/indices?v` tell you more than any question would — prefer looking over asking.

## Recording Preferences (only when the user declares one)

Write to config or memory **only** when the user states a preference during the work — never as a preflight questionnaire.

- User names a deployment target, version, license tier, or client → update the matching key in `~/Clawic/data/elasticsearch/config.yaml`.
- User states a shard-size target, bulk batch size, or replica policy → update the matching key.
- User expresses a stance (whether reindexes run directly or come back for review, how aggressive to be with `force_merge`, whether to surface production hardening unprompted) → record it under the relevant preference area (tooling, thresholds, conventions, platform, risk posture, output format, work order, integrations, restrictions, cadence) in `~/Clawic/data/elasticsearch/memory.md`.
- User corrects earlier guidance → update the stored value so it is not repeated.

If the user has said nothing, store nothing.

## What Memory Holds

Track their cluster shape (node count, versions, tiers), the workload (entity search, logs, metrics, vector, mixed), index and alias conventions already in use, incidents they have hit, and how much explanation they want — but only from what they actually reveal.
