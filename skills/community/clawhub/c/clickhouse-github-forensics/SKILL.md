---
name: clickhouse-github-forensics
description: Query GitHub event data via ClickHouse for supply chain investigations, actor profiling, and anomaly detection. Use when investigating GitHub-based attacks, tracking repository activity, analyzing actor behavior patterns, detecting tag/release tampering, or reconstructing incident timelines from public GitHub data. Triggers on GitHub supply chain attacks, repo compromise investigations, actor attribution, tag poisoning, or "query github events".
---

# ClickHouse GitHub Forensics

Query 10+ billion GitHub events for security investigations.

**Author:** Rufio @ [Permiso Security](https://permiso.io)  
**Use Case:** Built during the [Trivy supply chain compromise investigation](https://socket.dev/blog/trivy-under-attack-again-github-actions-compromise) (March 2026)

## Quick Start

```bash
curl -s "https://play.clickhouse.com/?user=play" \
  --data "SELECT ... FROM github_events WHERE ... FORMAT PrettyCompact"
```

- **Endpoint:** `https://play.clickhouse.com/?user=play`
- **Table:** `github_events`
- **Auth:** None required (public read-only)
- **Freshness:** Near real-time (~minutes behind)
- **Volume:** 10+ billion events

## Key Columns

| Column | Type | Use |
|--------|------|-----|
| `created_at` | DateTime | Event timestamp |
| `event_type` | Enum | PushEvent, CreateEvent, DeleteEvent, ReleaseEvent, etc. |
| `actor_login` | String | GitHub username |
| `repo_name` | String | `owner/repo` format |
| `ref` | String | Branch/tag name (e.g., `refs/heads/main`, `0.33.0`) |
| `ref_type` | Enum | `branch`, `tag`, `repository`, `none` |
| `action` | Enum | `published`, `created`, `opened`, `closed`, etc. |

For full schema (29 columns): see [references/schema.md](references/schema.md)

## Common Investigation Patterns

### 1. Actor Timeline (Who did what, when?)

```sql
SELECT created_at, event_type, repo_name, ref, action
FROM github_events 
WHERE actor_login = 'TARGET_ACCOUNT'
AND created_at >= '2026-03-01'
ORDER BY created_at
```

### 2. Repo Activity Window (What happened during incident?)

```sql
SELECT created_at, event_type, actor_login, ref, ref_type, action
FROM github_events 
WHERE repo_name = 'owner/repo'
AND created_at >= 'START_TIME'
AND created_at <= 'END_TIME'
ORDER BY created_at
```

### 3. Anomaly Detection (First-time repo access)

```sql
SELECT repo_name,
       countIf(created_at < 'ATTACK_DATE') as before,
       countIf(created_at >= 'ATTACK_DATE') as during
FROM github_events 
WHERE actor_login = 'SUSPECT_ACCOUNT'
AND created_at >= 'LOOKBACK_START'
GROUP BY repo_name
ORDER BY during DESC
```

### 4. Tag/Release Tampering

```sql
SELECT created_at, event_type, actor_login, ref, ref_type
FROM github_events 
WHERE repo_name = 'owner/repo'
AND event_type IN ('CreateEvent', 'DeleteEvent', 'ReleaseEvent')
AND ref_type = 'tag'
ORDER BY created_at
```

### 5. Actor Profile (Is this account legitimate?)

```sql
SELECT toStartOfMonth(created_at) as month,
       count() as events,
       uniqExact(repo_name) as unique_repos
FROM github_events 
WHERE actor_login = 'TARGET_ACCOUNT'
GROUP BY month
ORDER BY month
```

### 6. Org-Wide Activity (All repos in an org)

```sql
SELECT created_at, event_type, actor_login, repo_name, ref
FROM github_events 
WHERE repo_name LIKE 'orgname/%'
AND created_at >= 'START_TIME'
ORDER BY created_at
```

### 7. New Accounts During Incident (Potential attacker alts)

```sql
SELECT actor_login, min(created_at) as first_ever, count() as events
FROM github_events 
WHERE repo_name LIKE 'orgname/%'
GROUP BY actor_login
HAVING first_ever >= 'INCIDENT_START' AND first_ever <= 'INCIDENT_END'
ORDER BY first_ever
```

### 8. Hourly Breakdown (Attack timeline)

```sql
SELECT toStartOfHour(created_at) as hour,
       actor_login,
       count() as events,
       groupArray(distinct repo_name) as repos,
       groupArray(distinct event_type) as types
FROM github_events 
WHERE repo_name LIKE 'orgname/%'
AND created_at >= 'START_TIME'
GROUP BY hour, actor_login
ORDER BY hour
```

## Event Types Reference

| Event | Significance |
|-------|--------------|
| `PushEvent` | Code pushed to branch |
| `CreateEvent` | Branch/tag/repo created |
| `DeleteEvent` | Branch/tag deleted |
| `ReleaseEvent` | Release published/edited |
| `PullRequestEvent` | PR opened/closed/merged |
| `IssueCommentEvent` | Comment on issue |
| `ForkEvent` | Repo forked |
| `WatchEvent` | Repo starred |

## Tips

- **Output formats:** `FORMAT PrettyCompact` for tables, `FORMAT TabSeparated` for parsing
- **macOS curl:** Use `--data` not `-d` for multi-line queries
- **Timestamps:** Use UTC, format `YYYY-MM-DD HH:MM:SS`
- **No payload JSON:** Raw event payloads aren't available; use structured columns
- **Bot accounts:** Filter with `actor_login NOT IN ('github-actions[bot]', 'dependabot[bot]')`

## Security & Privacy

- Uses ClickHouse's **public playground** — all queries sent to `play.clickhouse.com`
- Data queried is GitHub's **public event stream only**
- No private repo data, credentials, or sensitive information is accessible
- Use responsibly: GitHub ToS prohibits scraping for spam or harassment
