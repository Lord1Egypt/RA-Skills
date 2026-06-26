# AANA Guardrail Skill Bundled Helper Variant

Use this variant only when the user or administrator wants a bundled, inspectable helper inside the skill package.

This package includes a small Python helper at `bin/aana_guardrail_check.py`. The helper does not implement AANA policy itself. It only sends a minimal review payload to a separately running AANA HTTP bridge on `localhost`.

## Safety Boundary

- Do not run the helper unless the user explicitly approves using the configured AANA bridge for this task.
- Do not send payloads to remote hosts. The bundled helper rejects non-localhost URLs.
- Do not include API keys, bearer tokens, passwords, full payment numbers, unnecessary account records, or unrelated private messages.
- Prefer redacted summaries over raw sensitive content.
- Treat AANA recommendations as advisory unless the bridge and policy are trusted and auditable.
- If the helper or bridge is unavailable, use manual review.

## Review Payload

Use a minimal JSON payload:

```json
{
  "adapter_id": "support_reply",
  "request_summary": "draft a refund support reply",
  "candidate_summary": "reply would promise refund eligibility",
  "evidence_summary": ["refund eligibility is unknown"],
  "allowed_actions": ["accept", "revise", "ask", "defer", "refuse"]
}
```

## Helper Behavior

The helper:

- reads one JSON payload file,
- validates that it is a JSON object,
- blocks obvious secret-like keys,
- sends the payload to a localhost AANA bridge,
- prints the JSON result,
- exits nonzero if the result recommends anything other than `accept`.

The helper does not:

- install dependencies,
- execute other scripts,
- infer checker paths,
- contact remote hosts,
- create event files,
- delete user files.

## Decision Rule

- If `recommended_action` is `accept`, proceed.
- If `recommended_action` is `revise`, revise before acting.
- If `recommended_action` is `ask`, ask the user for missing information.
- If `recommended_action` is `defer`, route to a stronger tool or human review.
- If `recommended_action` is `refuse`, pause, explain the reason, and ask for review when the decision affects important work.

If no trusted bridge is configured, do not use this helper.
