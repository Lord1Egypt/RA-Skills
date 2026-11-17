# Storage Schema — PRM Scores

## SQLite (recommended for local-first / OpenClaw workstation)

```sql
CREATE TABLE prm_scores (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  interaction_id TEXT NOT NULL,
  ts INTEGER NOT NULL,
  intent_alignment REAL NOT NULL,
  reasoning_quality REAL NOT NULL,
  tool_appropriateness REAL NOT NULL,
  safety_compliance REAL NOT NULL,
  efficiency REAL NOT NULL,
  user_value REAL NOT NULL,
  reward_composite REAL NOT NULL,
  primary_failure_mode TEXT,
  one_line_summary TEXT,
  judge_model TEXT NOT NULL,
  raw_judgment_json TEXT,
  FOREIGN KEY (interaction_id) REFERENCES interactions(id)
);

CREATE INDEX idx_prm_ts ON prm_scores(ts);
CREATE INDEX idx_prm_composite ON prm_scores(reward_composite);
```

## JSONL (recommended for streaming / sharing)

```json
{
  "interaction_id": "i_2026-08-22T19:12:34Z_abc123",
  "ts": "2026-08-22T19:12:45.123Z",
  "scores": {
    "intent_alignment": 0.62,
    "reasoning_quality": 0.71,
    "tool_appropriateness": 0.85,
    "safety_compliance": 1.00,
    "efficiency": 0.55,
    "user_value": 0.68
  },
  "reward_composite": 0.735,
  "primary_failure_mode": "none",
  "one_line_summary": "Cleanly translated brief into plan, executed in 4 well-ordered tool calls",
  "judge_model": "deepseek-chat"
}
```

One JSON object per line. Append-only. Never modify historical scores (immutable audit trail).

## Companion tables

If you also implement the wider RL loop:

```sql
CREATE TABLE interactions (
  id TEXT PRIMARY KEY,
  ts INTEGER,
  user_input TEXT,
  agent_output TEXT,
  tool_calls_json TEXT,
  completion_status TEXT,
  model_used TEXT,
  error_classification TEXT  -- see error attribution below
);

CREATE TABLE error_attribution (
  interaction_id TEXT PRIMARY KEY,
  error_type TEXT NOT NULL,  -- complex_task_fail | retry_loop | insufficient_context | tool_arg_complex | debug_session_pollution | ambiguous_brief | path_mismatch | heredoc_overflow | none
  is_agent_fault INTEGER NOT NULL,  -- 0 or 1
  covered_by_guard TEXT  -- which runtime guard could have caught it: complex_task_guard | retry_loop_guard | tool_guard | NULL
);
```

## Privacy — what NOT to persist

- Raw user inputs may contain personal data — strip before storage or encrypt at rest
- API keys / tokens / secrets — NEVER persist in the same database
- Tool call results that include credentials — redact before storage

Default to retention: 90 days for raw interactions; indefinite for score summaries only.
