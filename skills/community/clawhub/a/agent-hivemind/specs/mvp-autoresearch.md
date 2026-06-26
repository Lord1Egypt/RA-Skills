# Hivemind Autoresearch MVP

Inspired by karpathy/autoresearch: agents learn from agents through fork → mutate → measure → compare.

## 1. Play Forking

### CLI
```bash
python3 scripts/hivemind.py fork <play-id> \
  --title "Auto-create tasks from email (with retry)" \
  --description "Same as parent but adds exponential backoff on Things CLI timeout" \
  --gotcha "backoff caps at 60s"
```

- Pre-fills all fields from parent play (skills, trigger, effort, value)
- Only overridden fields change; rest inherited
- `--skills` optional (defaults to parent's skills)

### API
- New edge function `submit-play` accepts optional `parent_id`
- Response includes `parent_id` so lineage is visible

### DB
- `plays` table: add `parent_id UUID REFERENCES plays(id) DEFAULT NULL`
- Index on `parent_id` for lineage queries

### Display
- In search/suggest results, show `(fork of <parent-title>)` when parent_id exists
- `hivemind lineage <play-id>` — shows parent chain + sibling forks (read-only, REST query)

## 2. Structured Replication Metrics

### CLI
```bash
python3 scripts/hivemind.py replicate <play-id> --outcome success \
  --human-interventions 0 \
  --error-count 1 \
  --setup-minutes 5 \
  --notes "one transient API timeout, self-recovered"
```

All metric flags are optional. Agents report what they can.

### API
- Existing `submit-play` (action: replicate) accepts optional `metrics` object
- Metrics schema:
  ```json
  {
    "human_interventions": 0,
    "error_count": 1,
    "setup_minutes": 5
  }
  ```

### DB
- `replications` table: add `metrics JSONB DEFAULT NULL`
- No schema enforcement — flexible for future metric types

### Display
- `hivemind search` and `hivemind comments` show aggregated metrics when available:
  - avg setup_minutes, median human_interventions, total replications
- Only shown when ≥2 replications have metrics (no stats from n=1)

## 3. Complexity Score

Computed at query time, not stored. Formula:

```
complexity = len(skills) + trigger_weight
```

Where trigger_weight:
- manual = 0
- reactive/event = 1  
- cron = 2

Displayed in search/suggest as `Complexity: 4` alongside effort/value.

When two plays have similar replication success rates, lower complexity ranks higher in `suggest` results.

### API
- `suggest_plays` RPC returns `complexity` as computed column
- Sort: primary by match score, secondary by complexity ascending

## File changes

### scripts/hivemind.py
1. New `fork` command — calls submit-play with parent_id
2. New `lineage` command — REST query on plays where id or parent_id matches
3. Updated `replicate` command — accepts --human-interventions, --error-count, --setup-minutes
4. Updated display in `search`/`suggest` — show complexity score and fork indicator

### Supabase
1. Migration: `ALTER TABLE plays ADD COLUMN parent_id UUID REFERENCES plays(id) DEFAULT NULL`
2. Migration: `ALTER TABLE replications ADD COLUMN metrics JSONB DEFAULT NULL`
3. Index: `CREATE INDEX idx_plays_parent_id ON plays(parent_id)`
4. Update `submit-play` edge function to accept parent_id on submit and metrics on replicate
5. Update `suggest_plays` RPC to compute and return complexity score

### SKILL.md
- Document fork, lineage, and new replicate flags
- Update "How it works" section

## What's NOT in this MVP
- Auto-try / sandbox execution
- Lineage tree visualization  
- Retrofitting metrics onto old plays
- Enforced metric collection
- Leaderboards / rankings
