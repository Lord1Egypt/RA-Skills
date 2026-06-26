# Daily Gift Heartbeat

Use heartbeat runs for silent maintenance only.

## Priority

If `workspace/daily-gift/heartbeat-tasks.jsonl` exists and contains pending tasks, process them before any lower-priority maintenance.

## Task File

Read `workspace/daily-gift/heartbeat-tasks.jsonl` as a queue of JSON lines.

Supported task types:

- `write_souljournal`
- `update_taste_profile_layer3`
- `retry_api_config`

Each line should be a JSON object with:

- `task_id`
- `task_type`
- `created_at`
- `status` where pending tasks use `pending`
- optional task-specific fields such as `gift_metadata_path`, `memory_path`, `taste_profile_path`, or `setup_state_path`
- retry tasks should additionally include fields such as `retry_count`, `max_retries`, `cooldown_gifts`, `api_base`, and `test_endpoint`

For each pending task:

1. Read the task payload.
2. Complete the task silently.
3. Rewrite the queue without the completed task.

Do not send user-facing messages for these maintenance tasks.

## Configuration Recovery Tasks

For `retry_api_config` tasks:

1. Check whether the cooldown has passed by comparing `cooldown_gifts` against how many gifts have been sent since the task was created.
2. If the cooldown has not passed, leave the task pending.
3. If the cooldown has passed, silently test the configured API endpoint.
4. If the test succeeds:
   - update setup-state with the working configuration
   - remove the task from the queue
5. If the test fails:
   - increment `retry_count`
   - if `retry_count >= max_retries`, change `status` to `exhausted` and keep the task as a record
   - otherwise leave it pending with the updated retry count
6. Never message the user about retry attempts.

This same recovery pattern can be used for:

- Freesound token detection
- video API availability
- hosting configuration

When a user manually asks to reconfigure something, reset the corresponding retry task's `retry_count` to `0` and `status` to `pending`.

If there are no pending tasks and nothing else needs attention, respond with `HEARTBEAT_OK`.
