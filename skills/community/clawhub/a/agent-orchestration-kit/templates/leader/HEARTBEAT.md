# HEARTBEAT.md

## Task Status Check (every 3 minutes)

Scan `tasks/` directory for active task files (T-*.md) with `status: in_progress`.

For each active task:

1. **Check for pending callbacks — MUST query session history:**
   For EVERY step that is `[⏳]` (dispatched), run:
   ```
   sessions_history(sessionKey: step.brief_to, limit: 10)
   ```
   Look for a `[TASK_CALLBACK:T-xxx]` message from the agent.
   Do NOT rely solely on the task file icon — the callback may have been
   delivered to a different session and never processed.

2. **Process unhandled callbacks:** If an agent has completed but the task file
   step is still `[⏳]`:
   - Update the task file (step icon, output, files)
   - Edit the original status message using `notification_status_msg` and `route`
     from the task file
   - Cascade: dispatch next step if dependencies are met

3. **Check for undispatched steps:**
   For EVERY step that is `[—]` (waiting), check if ALL its dependencies
   (listed as `after: N`) are now `[✅]`.
   If yes → this step should have been dispatched but wasn't.
   **Before dispatching: update the step icon to `[⏳]` in the task file first,
   then `sessions_send`.** This prevents duplicate dispatch on the next heartbeat cycle.

4. **Stale detection:** If a `[⏳]` step has had no update for 15+ minutes:
   - Check agent session for activity via `sessions_history`
   - If agent is stuck or session is dead → re-dispatch or escalate

5. **Notification recovery:**
   - Task `in_progress` but `notification_status_msg` empty → send kickoff status message to `route`, record messageId, **pin it**
   - Task `in_progress` and `notification_status_msg` exists but `pinned` is false → **pin it**
   - Task `completed` but `notification_result_msg` empty → compose and send result delivery to `route`, record messageId
   - Task `completed` and approved → **unpin** the status message, set `pinned: false`

6. **Nothing pending** → do nothing (no HEARTBEAT_OK noise)

### Key principle
Use `route` and `notification_status_msg` from the task file to update the original status message in the original channel. Do NOT post to a fixed operations channel for routine updates.
