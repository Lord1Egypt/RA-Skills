# Escalation / Issue URL Design

`gemini-smart-search` is primarily for agent use, but some failures should escalate cleanly to a human instead of pretending the skill can always self-heal.

## Principle

Normal operational failures should return normal errors.

Exceptional failures that suggest an implementation gap, model-routing mismatch, contract drift, or persistent upstream incompatibility should return an `escalation` object that points a human to file a GitHub issue.

## Baseline issue URL

```text
https://github.com/jas0n1ee/gemini-smart-search/issues/new
```

Future versions may prefill title/body query parameters.

## Suggested escalation kinds

- `bug`
- `model-routing`
- `api-compat`
- `docs-mismatch`
- `qa-gap`

## When escalation SHOULD be suggested

### 1. Implementation / contract failures
- unexpected response schema shape
- grounding metadata shape drift
- internal code path not covered / impossible-state bug
- stable local reproducible failure that is not a user/config mistake

### 2. Model-routing reality mismatch
- UI model label and callable model IDs diverge in a way the skill no longer handles
- preview / non-preview naming flips and breaks routing
- all candidate IDs for a documented display model fail in a suspicious way

### 3. Skill contract drift
- canonical entrypoint no longer matches docs
- `--json` contract breaks for supported usage
- wrapper and Python entrypoints diverge again
- fallback behavior violates documented policy

### 4. Persistent upstream incompatibility
- grounding appears unavailable for a model that should support it
- citations are systematically malformed or unusable
- API behavior changes in a way that requires code or docs updates

## When escalation SHOULD NOT be suggested

Do not tell the human to open a GitHub issue for normal operational cases such as:
- missing API key
- quota exceeded on a single attempted model
- transient network errors on a single attempted model
- weird/low-quality query outcomes
- invalid user CLI arguments
- a single low-signal result set

Current v1 code caveat:
- if the entire fallback chain is exhausted, the script currently returns `error.type=all_models_failed` and marks `escalation.should_open_issue=true`, even when the underlying per-model causes were retryable upstream failures.
- Treat that as the **current shipped contract**, not an idealized policy. Human triage should still inspect `error.attempts` before deciding whether this is a real repo issue versus temporary quota/upstream exhaustion.

## Output shape

Always include `escalation` in the JSON response.

### Non-escalated example

```json
{
  "escalation": {
    "should_open_issue": false,
    "issue_url": null,
    "reason": null,
    "kind": null,
    "recommended_details": []
  }
}
```

### Escalated example

```json
{
  "escalation": {
    "should_open_issue": true,
    "issue_url": "https://github.com/jas0n1ee/gemini-smart-search/issues/new",
    "reason": "Unexpected grounding schema mismatch",
    "kind": "api-compat",
    "recommended_details": [
      "query",
      "mode",
      "display_chain",
      "fallback_chain",
      "model_used",
      "usage.attempted_models",
      "error.type",
      "error.message"
    ]
  }
}
```

## First-version recommendation

V1 should keep the logic simple:
- always include an `escalation` field
- default it to the non-escalated shape
- set it only for clearly suspicious/systemic cases
- avoid issue spam for normal user/runtime failures
