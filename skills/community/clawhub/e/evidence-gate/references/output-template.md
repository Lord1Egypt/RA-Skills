# Evidence Gate Output Template

Return a single JSON object with this exact top-level shape:

```json
{
  "gate_required": true,
  "gate_reason": "Strong diagnosis with incomplete evidence coverage.",
  "candidate_summary": "Claim: the root cause is a nil dereference in request parsing.",
  "requirements": [
    {
      "id": "req-repro",
      "description": "Show a reliable reproduction path for the claimed failure mode.",
      "mandatory": true,
      "acceptable_kinds": ["test", "reproduction", "log"],
      "status": "missing",
      "evidence_refs": [],
      "notes": "Without reproduction, the diagnosis should remain provisional."
    }
  ],
  "missing_evidence": [
    "A reproduction proving the claimed failure mode"
  ],
  "conflicting_evidence": [],
  "sufficiency_rule": "PASS requires all mandatory requirements satisfied and no unresolved central conflict.",
  "verdict": "SOFT_PASS",
  "allowed_next_actions": [
    "Present the claim as a leading hypothesis"
  ],
  "blocked_next_actions": [
    "Present the claim as a confirmed root cause"
  ],
  "fallback_behavior": "Downgrade to a provisional diagnosis and request targeted checks.",
  "suggested_wording": "Current evidence suggests this diagnosis, but it is not yet established.",
  "next_evidence_actions": [
    "Reproduce the issue on the claimed path",
    "Check at least one competing explanation"
  ]
}
```

## Rules

- Keep every top-level key present.
- Use `[]` for empty lists.
- Use one of `PASS`, `SOFT_PASS`, `BLOCK`, or `CONFLICT` for `verdict`.
- Keep `acceptable_kinds` present on every requirement.
- Keep `next_evidence_actions` bounded to the smallest useful set, usually `1-3` items.
- Keep `suggested_wording` ready to reuse directly in the caller's output.
- If `gate_required` is `false`, use it as a fast exit:
  - set `verdict` to `PASS`
  - keep `requirements`, `missing_evidence`, and `conflicting_evidence` empty
