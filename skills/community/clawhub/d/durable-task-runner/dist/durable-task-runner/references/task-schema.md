# Durable Task Runner Schema

## Files

For task id `<task-id>`:

- `state/tasks/<task-id>.json`
- `state/tasks/<task-id>.events.jsonl`
- `state/tasks/<task-id>.progress.log`

## Snapshot schema

Attribution note:
- This schema is original to this repo, but it is influenced by ideas seen in ClawHub `restart-safe-workflow` (action-state / idempotency / reconcile thinking) and `subagent-orchestrator` (controller/worker separation and explicit task-line progression).

```json
{
  "task_id": "email-cleanup-2026-03-20",
  "title": "Thunderbird backup cleanup",
  "goal": "Clean and verify the backup mailbox conservatively",
  "done_criteria": [
    "cleanup frontier exhausted",
    "verification pass complete",
    "final summary written"
  ],
  "constraints": [
    "backup copy only",
    "preserve uncertain mail"
  ],
  "desired_state": "running",
  "execution_priority": "tokens",
  "phase": "verification",
  "health": "healthy",
  "created_at": "2026-03-20T19:40:00Z",
  "updated_at": "2026-03-20T19:55:00Z",
  "status_update_interval_seconds": 300,
  "last_status_update_at": "2026-03-20T19:50:00Z",
  "last_verified_step": "verify-archive-2010",
  "next_step": "verify-archive-2009",
  "operator_note": "",
  "steering_note": "",
  "milestones": [
    {
      "id": "plan",
      "title": "Plan created",
      "status": "done",
      "percent": 100
    },
    {
      "id": "cleanup",
      "title": "Cleanup execution",
      "status": "running",
      "percent": 80
    },
    {
      "id": "verify",
      "title": "Verification",
      "status": "pending",
      "percent": 0
    }
  ],
  "subtasks": [
    {
      "id": "archive-2010",
      "title": "Process 2010 archive",
      "status": "done",
      "owner": "subagent:abc",
      "depends_on": []
    }
  ],
  "artifacts": [],
  "risk_notes": [],
  "pending_actions": [],
  "action_states": {},
  "idempotency_ledger": {},
  "reconcile": {
    "needed": false,
    "reason": "",
    "last_run_at": null,
    "status": "idle"
  }
}
```

### New durable fields

These fields are influenced by ClawHub `restart-safe-workflow` ideas and are intended to support stricter resume/reconcile behavior:

- `pending_actions[]`
  - actions queued but not yet fully processed
- `action_states{}`
  - per-action state, attempts, and result metadata
- `idempotency_ledger{}`
  - records already-applied action keys so resume logic can avoid duplicate side effects
- `reconcile`
  - explicit repair/recheck state after interruption, partial failure, or ambiguous completion

## Event schema

One JSON object per line.

```json
{
  "ts": "2026-03-20T19:55:00Z",
  "type": "step_completed",
  "task_id": "email-cleanup-2026-03-20",
  "phase": "cleanup",
  "step": "archive-2010",
  "status": "ok",
  "details": {
    "messages_moved": 849,
    "bytes_moved": 30828123
  }
}
```

## Recommended event types

- `task_created`
- `task_started`
- `plan_recorded`
- `milestone_started`
- `milestone_completed`
- `subtask_assigned`
- `step_started`
- `step_completed`
- `verification_started`
- `verification_passed`
- `verification_failed`
- `status_reported`
- `pause_requested`
- `pause_acknowledged`
- `resume_started`
- `resume_consistency_check_passed`
- `resume_consistency_check_failed`
- `steer_received`
- `stop_requested`
- `stop_acknowledged`
- `task_completed`
- `task_failed`
- `task_reset_detected`

## Reconstruction rule

If snapshot and events disagree, prefer:
1. append-only event log
2. then latest coherent snapshot
3. never assume successful completion without either a verification event or explicit completion event
