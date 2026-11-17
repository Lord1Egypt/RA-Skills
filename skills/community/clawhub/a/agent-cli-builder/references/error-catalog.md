# Error Catalog and Status Mapping

Use this reference for standard error categories, subtypes, exit codes, and `errorOnStatus`.

## Contents

1. Categories and subtypes
2. Recommended `errorOnStatus`
3. Typed error examples
4. Wrapping, redaction, and `BareError`

## 1. Categories and subtypes

| Category         | Exit | Standard subtypes                                                                  |
| ---------------- | ---: | ---------------------------------------------------------------------------------- |
| `validation`     |    2 | `invalid_argument`, `missing_required`, `out_of_range`                             |
| `authentication` |    3 | `no_token`, `token_expired`, `token_revoked`, `no_credentials`, `no_refresh_token` |
| `authorization`  |    3 | `missing_scope`, `app_permission_denied`, `forbidden`                              |
| `config`         |    3 | `missing_config`, `invalid_config`, `unbound_env`, `skill_sync_failed`             |
| `network`        |    4 | `timeout`, `connection_refused`, `dns_failure`, `ssl_error`                        |
| `api`            |    1 | `not_found`, `already_exists`, `conflict`, `rate_limited`, `server_error`          |
| `policy`         |    6 | `content_blocked`, `challenge_required`, `access_denied`                           |
| `internal`       |    5 | `decode_failure`, `unknown`, `contract_violation`                                  |
| `confirmation`   |   10 | `high_risk_write`                                                                  |

Use `internal` only for framework or unexpected implementation failures. Business code should not use it as a generic fallback.

Useful semantics:

- `rate_limited` and 5xx `server_error` are retryable.
- `not_found` has the `errs.NotFoundError` convenience constructor.
- `missing_scope` may include a machine-readable `missingScopes` array.
- `high_risk_write` should include a concrete confirmation hint.

## 2. Recommended `errorOnStatus`

```ts
defineCli({
  errorOnStatus: {
    403: "forbidden",
    404: "not_found",
    409: "already_exists",
    429: "rate_limited",
    "5xx": "server_error",
  },
  // ...
});
```

Values are subtype strings, not constructors. `defineCli` validates status keys and registered subtypes during assembly.

401 is reserved for authentication handling. The request runtime attempts one auth refresh and retry; a final 401 becomes `AuthenticationError(token_expired)`. Do not depend on an `errorOnStatus` entry for 401.

Use global mapping when every command gives the status the same meaning. Handle a status inside `run` when its business meaning or hint differs by command. Never configure and manually inspect the same status: mapped responses throw before `ctx.*` returns.

## 3. Typed error examples

```ts
import { errs } from "@renxqoo/agent-cli-sdk";

throw new errs.ValidationError({
  subtype: "out_of_range",
  param: "--limit",
  message: "--limit must be from 1 to 100",
  hint: "Use --limit 20 or another value from 1 to 100",
});

throw new errs.PermissionError({
  subtype: "missing_scope",
  message: "orders:write is required",
  hint: "Ask an administrator to grant orders:write, then sign in again",
  missingScopes: ["orders:write"],
});

throw new errs.NetworkError({
  subtype: "timeout",
  message: "The request timed out after 30 seconds",
  retryable: true,
  cause: originalError,
});

throw new errs.APIError({
  subtype: "rate_limited",
  code: 429,
  message: "Too many requests",
  hint: "Retry-After: 60s",
  retryable: true,
});

throw new errs.ConfirmationRequiredError({
  subtype: "high_risk_write",
  message: "Deleting 100 records requires confirmation",
  hint: "Review the preview and rerun with --yes",
});
```

For structured writes, do not throw this manually. Declare `operation.confirmation: "required"`; the runtime validates input, applies dry-run and idempotency policy, then raises the standard confirmation error before business `run`. Manual confirmation errors remain for non-structured commands.

Prefer standard subtypes. If a genuinely new subtype is required, register it before `defineCli` assembly:

```ts
import { SUBTYPE_REGISTRY } from "@renxqoo/agent-cli-sdk";
SUBTYPE_REGISTRY.my_service_conflict = { category: "api" };
```

Direct global registration is an escape hatch. Document it and test startup validation.

## 4. Wrapping, redaction, and `BareError`

Do not rewrap a typed error and lose its category or subtype:

```ts
try {
  return await ctx.get("/orders");
} catch (error) {
  if (error instanceof errs.CliError) throw error;
  throw new errs.InternalError({
    subtype: "unknown",
    message: "Unexpected order-service failure",
    cause: error,
  });
}
```

Use `observeError` for telemetry and `handleError` to normalize or redact errors. Recovery is possible only through the explicit `{ action: "recover" }` decision.

```ts
const redactErrors = {
  name: "redact-errors",
  async handleError(_ctx, error) {
    if (!(error instanceof errs.CliError)) return { action: "pass" };
    error.message = error.message.replace(/Bearer [A-Za-z0-9._-]+/g, "Bearer [REDACTED]");
    return { action: "replace", error };
  },
};
```

`errs.BareError(exitCode)` is the only error that suppresses the normal stderr envelope. Reserve it for predicate commands whose stdout already contains the complete answer, such as an auth check. Ordinary business commands must use structured errors.
