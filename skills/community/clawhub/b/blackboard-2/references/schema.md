# Blackboard schema

```json
{
  "schema_version": 1,
  "task_id": "uuid",
  "goal": "",
  "status": "active",
  "policy": {"max_hops": 6},
  "revision": 0,
  "facts": [],
  "inferences": [],
  "user_decisions": [],
  "evidence": [],
  "actions": [],
  "test_results": [],
  "failed_attempts": [],
  "open_questions": [],
  "next": {
    "capability_needed": "",
    "recommended_model": "",
    "instruction": ""
  },
  "hop_count": 0,
  "updated_by": "",
  "updated_at": ""
}
```

No notes blob or untyped top-level extensions.

## Entry envelope

```json
{
  "entry_id": "uuid",
  "content": "one atomic contribution",
  "written_by": {
    "model": "provider/model-or-runtime-name",
    "agent": "optional label"
  },
  "provenance": [{
    "kind": "file|tool|url|user|command|model_output",
    "source": "stable source or absolute path",
    "locator": "line, record, invocation, URL, or result id",
    "sha256": "optional lowercase SHA-256",
    "excerpt": "optional short excerpt"
  }],
  "confidence": 0.0,
  "verified_by": [{
    "model": "different verifier model",
    "at": "RFC3339 timestamp",
    "provenance": []
  }],
  "created_at": "RFC3339 timestamp"
}
```

Rules:

- Required: atomic `content`, `written_by.model`, non-empty provenance, `verified_by`, and timestamp.
- Confidence is optional, 0..1, and useful mainly for facts/inferences.
- Writers cannot self-verify.
- Every user decision requires `written_by.model` beginning `user/` and a provenance item with `kind=user`.
- `APPROVE: <target>` authorizes one destructive action against exactly that normalized target.
- `APPROVE_POLICY: max_hops OLD -> NEW` authorizes one exact policy increase.
- `DO_NOT_TOUCH: <target>` blocks all actions against the exact target or a descendant.
- Regular actions require an explicit target. Route/state/policy audit actions are internal helper records.
- Test results begin `PASS:` or `FAIL:`.
- Route commits carry their normalized route tuple in provenance; duplicate tuples are invalid.
- State commits begin `STATE:`; policy changes begin `POLICY:`.
- `revision` increments once per successful mutation. `--expect-revision` provides optimistic conflict detection in addition to the file lock.
- `policy.max_hops` is authoritative. No command-time override exists after initialization.

## Completion

A completed board has empty `next` and at least one passing test that is independent:

- its writer did not author any tested non-route action; or
- a different model appears in its `verified_by`.

This is a practical independence check, not proof that two model names denote genuinely independent runtimes.
