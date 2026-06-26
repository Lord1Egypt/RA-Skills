# Evidence Gate Input Template

When a caller wants explicit control instead of relying on inference, use this JSON shape:

```json
{
  "claim": "The root cause is a nil dereference in request parsing.",
  "claim_type": "diagnosis",
  "domain": "coding",
  "risk_level": "medium",
  "execution_mode": "advisory",
  "target_strength": "definitive",
  "known_evidence": [
    {
      "id": "ev-1",
      "summary": "A regression test reproduces the crash when request.user is missing.",
      "kind": "test",
      "source": "local test suite",
      "artifact_ref": "tests/auth_test.rb:42",
      "reliability": "high",
      "supports": ["req-repro"],
      "contradicts": []
    }
  ],
  "alternatives_checked": [
    "The crash is caused by a malformed request body instead of a nil user object."
  ],
  "available_tools": ["rg", "tests", "logs"],
  "policy_overrides": []
}
```

## Rules

- `claim` is the only required field for a minimal invocation.
- Use the full template when a caller wants deterministic control over classification and risk.
- Keep `known_evidence` explicit; do not rely on hidden reasoning as evidence.
- Keep `alternatives_checked` concise and concrete.
- Use coarse-grained `domain` values; keep domain details in evidence items and requirements.
