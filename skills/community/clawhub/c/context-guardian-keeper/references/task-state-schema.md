# Task State Schema

Canonical durable task state object for context guardian.

```json
{
  "task_id": "string",
  "session_id": "string",
  "goal": "string",
  "status": "idle|running|blocked|complete|failed",
  "current_phase": "string",
  "plan": [
    {
      "id": "step-1",
      "title": "string",
      "status": "pending|in_progress|done|failed|skipped",
      "notes": "string"
    }
  ],
  "completed_steps": ["string"],
  "open_issues": ["string"],
  "decisions": [
    {
      "timestamp": "ISO-8601",
      "decision": "string",
      "reason": "string"
    }
  ],
  "constraints": ["string"],
  "important_facts": ["string"],
  "artifacts": [
    {
      "path": "string",
      "kind": "file|dir|url|result",
      "description": "string"
    }
  ],
  "last_action": {
    "timestamp": "ISO-8601",
    "type": "tool|edit|analysis|message",
    "summary": "string",
    "outcome": "string"
  },
  "next_action": "string",
  "recovery_instructions": [
    "Read task_state.json",
    "Read latest summary",
    "Verify files before editing",
    "Resume from next_action only if constraints still hold"
  ],
  "state_confidence": 0.0,
  "updated_at": "ISO-8601"
}
```

Rules:
- Keep `next_action` single and exact.
- Keep `state_confidence` honest.
- Update `updated_at` on every durable write.
- Never rely on raw chat history as the only recovery source.
