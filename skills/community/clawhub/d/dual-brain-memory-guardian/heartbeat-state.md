# Dual-Brain Memory Guardian Heartbeat State

last_heartbeat_started_at: never
last_reviewed_change_at: never
last_vector_digest_at: never
last_heartbeat_result: never

## Last actions
- none yet

## Rules

- update `last_heartbeat_started_at` at heartbeat start
- update `last_reviewed_change_at` only after successful local file review
- update `last_vector_digest_at` after digest query completes
- keep `last_actions` short, factual, and append-only for traceability
- do not turn this file into a long-form memory log
