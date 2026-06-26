# autoloop_state.json Schema

Persisted at `<state-root>/autoloop_state.json`. Created on first run, updated after each iteration.

## Fields

| Field | Type | Description |
|-------|------|-------------|
| `schema_version` | string | Always `"1.0"`. Used for forward-compatible migrations. |
| `target` | string | Absolute path to the skill being improved. |
| `started_at` | string | ISO 8601 UTC timestamp of the first iteration. |
| `iterations_completed` | int | Number of pipeline runs finished so far. |
| `max_iterations` | int | Hard cap on total iterations (from CLI `--max-iterations`). |
| `total_cost_usd` | float | Cumulative estimated cost across all iterations. |
| `max_cost_usd` | float | Budget ceiling (from CLI `--max-cost`). |
| `current_scores` | dict | Most recent dimension scores (e.g. `{"clarity": 0.85, "coverage": 0.72}`). |
| `score_history` | list[dict] | Per-iteration records: `{iteration, weighted_score, decision, scores, timestamp}`. |
| `plateau_counter` | int | Consecutive iterations without improvement. Reset on score gain. |
| `plateau_window` | int | Threshold; plateau detected when `plateau_counter >= plateau_window`. |
| `status` | string | One of: `running`, `completed`, `stopped_plateau`, `stopped_cost`, `stopped_max_iter`, `stopped_oscillation`, `error`. |
| `last_failure_trace` | string\|null | Traceback from most recent failed iteration, or `null`. |
| `cooldown_minutes` | int | Minutes to sleep between iterations in continuous mode. |
| `next_run_at` | string\|null | ISO 8601 timestamp for next scheduled run (continuous/scheduled mode). |

## Example

```json
{
  "schema_version": "1.0",
  "target": "/Users/sly/.claude/skills/coding-standards",
  "started_at": "2026-04-03T08:00:00Z",
  "iterations_completed": 3,
  "max_iterations": 5,
  "total_cost_usd": 12.50,
  "max_cost_usd": 50.0,
  "current_scores": {"clarity": 0.85, "coverage": 0.72, "actionability": 0.90},
  "score_history": [
    {"iteration": 1, "weighted_score": 0.78, "decision": "keep", "scores": {"clarity": 0.80, "coverage": 0.65, "actionability": 0.88}, "timestamp": "2026-04-03T08:01:00Z"},
    {"iteration": 2, "weighted_score": 0.80, "decision": "keep", "scores": {"clarity": 0.82, "coverage": 0.68, "actionability": 0.89}, "timestamp": "2026-04-03T08:35:00Z"},
    {"iteration": 3, "weighted_score": 0.82, "decision": "keep", "scores": {"clarity": 0.85, "coverage": 0.72, "actionability": 0.90}, "timestamp": "2026-04-03T09:10:00Z"}
  ],
  "plateau_counter": 0,
  "plateau_window": 3,
  "status": "running",
  "last_failure_trace": null,
  "cooldown_minutes": 30,
  "next_run_at": "2026-04-03T09:40:00Z"
}
```

## iteration_log.jsonl

Append-only log. One JSON object per line, written after each iteration completes.

```json
{"iteration": 1, "started_at": "2026-04-03T08:00:00Z", "finished_at": "2026-04-03T08:01:00Z", "decision": "keep", "weighted_score": 0.78, "cost_usd": 4.20, "duration_seconds": 60.0, "candidate_id": "abc123", "artifact_path": "/tmp/state/artifacts/abc123.json"}
```
