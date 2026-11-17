# Recovery Playbook

Load this reference only when a normal workflow cannot continue.

## Tool Missing or Wrong Schema

1. Call `gemini_get_tool_manifest` or low-token `account(action="manifest")`.
2. Check the current enabled surface/profile.
3. Switch to the narrow primary profile required by the workflow.
4. Do not enable `all` unless the task is repository maintenance or comprehensive verification.

## Authentication Failure

Return the stable error code and the required next action. Do not ask for Cookie values in ordinary prose or copy them into logs.

Authentication recovery is separate from user-facing task design. Resume the original workflow after the runtime is configured.

## Entitlement Unavailable

Classify a missing account entitlement separately from:

- invalid authentication;
- upstream drift;
- implementation failure;
- queued work.

Do not retry a known entitlement failure repeatedly.

## Quick Search Without Sources

If quick search returns an answer but no observed sources:

1. label it `answer_only` or ungrounded;
2. avoid presenting it as verified current-web research;
3. retry with a more explicit sourcing request once;
4. escalate to Deep Research when sources are required.

## Long Operation Timeout

1. preserve every operation/upstream ID;
2. query status or retrieve the result with the same handle;
3. do not restart automatically;
4. if the handle is unknown after process restart, report the current compatibility limitation;
5. when the future SQLite registry is present, recover from it.

## Artifact Missing or Partial

1. inspect structured Artifact state;
2. retain remote URI and operation IDs if present;
3. retry local save without repeating upstream generation when possible;
4. do not claim a file exists until verified;
5. return the next action.

## Accepted but Unverified Mutation

Use the verification state:

```text
not_observed
read_back_error
mismatch
still_present
incomplete
```

Do not show success. Retry read-back or tell the agent what must be checked.

## Upstream Drift

When a parser, RPC, or capability appears to have changed:

1. capture the stable diagnostic stage and code;
2. do not persist raw private responses;
3. run the bounded compatibility probe;
4. classify the failure as transport, envelope, rejection, parser, or entitlement;
5. hand the evidence to `gemini-web-mcp-development`.
