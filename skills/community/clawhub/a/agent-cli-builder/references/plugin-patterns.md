# Plugin Patterns and Hook Ordering

Use plugins for cross-cutting behavior such as authentication, fixed headers, signing, audit, redaction, and error normalization.

## Contents

1. Hooks and ordering
2. Common patterns
3. Plugin-provided commands and distribution
4. Safe debugging and common mistakes

## 1. Hooks and ordering

| Hook                 | Runs                                 | Typical use                                          |
| -------------------- | ------------------------------------ | ---------------------------------------------------- |
| `apply`              | Once at assembly, before routing     | Resolve `services.localState.store`, fill `provides` |
| `onAppRun`           | Once per `app.run`, before routing   | Best-effort startup awareness                        |
| `afterAppRun`        | Once per `app.run`, after it settles | Best-effort operational notices (update awareness)   |
| `beforeCommand`      | Before command `run`                 | Resolve identity, initialize state, reject execution |
| `observeInput`       | After JSON args validation/redaction | Audit JSON provenance without raw data               |
| `beforeRequest`      | Before each `ctx.*` attempt          | Headers, tenant, signatures                          |
| `observeRequest`     | After each physical attempt          | Metrics and awaited audit side effects               |
| `handleUnauthorized` | After a 401 response                 | Refresh a context-bound credential once              |
| `transformOutput`    | After `run`, before serialization    | Redact or reshape structured data                    |
| `observeError`       | After an error is normalized         | Telemetry that cannot change the result              |
| `handleError`        | After error observers                | Explicitly pass, replace, or recover                 |

`enforce` supports `"pre"`, `"normal"`, and `"post"`; omitting it means `"normal"`. Hooks run pre, normal, then post, preserving registration order inside each tier. `apply` is not a hook: `defineCliApp` runs it for every plugin, in registration order, before routing compiles; a thrown error aborts startup.

Typical order:

- Auth: `pre`, so credentials exist before requests.
- Tenant defaults: `pre` or normal, depending on whether auth needs them.
- HMAC signing: `post`, after headers and body are final.

Write lifecycle tests when two plugins depend on registration order.

`observeInput` receives the route, input metadata and cloned `redactedArgs`; it never receives raw JSON. Register `sensitive` JSON Pointers in the root Zod schema metadata and keep observers telemetry-only. Observer failures are logged and cannot change command execution.

App-level hooks (`onAppRun` / `afterAppRun`) are stricter: they fire exactly once per process run (help, `--version`, unknown routes, and errors included) and failures are silent so they cannot change the exit code or append an ambiguous warning after a machine-readable result. Use them only for optional operational awareness. Do not use them for audit events or any side effect that requires delivery. Prefer `afterAppRun` over per-command observers for run-scoped notices such as update awareness.

## 2. Common patterns

### Fixed headers

```ts
const clientHeaders = {
  name: "client-headers",
  enforce: "pre" as const,
  async beforeRequest(_ctx, request) {
    return { ...request, headers: { ...request.headers, "X-Client": "my-cli" } };
  },
};
```

### Audit status without leaking payloads

```ts
const audit = {
  name: "audit",
  async observeRequest(ctx, event) {
    if (event.outcome.kind === "response" && event.outcome.response.status >= 400) {
      ctx.log.warn(`request failed: status=${event.outcome.response.status}`);
    }
  },
};
```

### Output redaction

```ts
const redact = {
  name: "redact",
  enforce: "post" as const,
  async transformOutput(_ctx, data) {
    if (Array.isArray(data)) return data.map(redactItem);
    if (data && typeof data === "object") return redactItem(data);
    return data;
  },
};

function redactItem(item: Record<string, unknown>) {
  const output = { ...item };
  if ("email" in output) output.email = maskEmail(String(output.email));
  if ("phone" in output) output.phone = maskPhone(String(output.phone));
  return output;
}
```

`transformOutput` must return structured data: object, array, or `null`. A string violates the pipe contract.

### Error normalization

```ts
const normalizeErrors = {
  name: "normalize-errors",
  async handleError(_ctx, error) {
    if (!(error instanceof errs.CliError)) return { action: "pass" };
    error.message = error.message.replace(/Bearer [A-Za-z0-9._-]+/g, "Bearer [REDACTED]");
    if (error instanceof errs.NetworkError && !error.hint) {
      error.hint = "Check connectivity, then retry";
    }
    return { action: "replace", error };
  },
};
```

`observeError` is telemetry-only: returning `void` can never swallow a failure. `handleError` requires an explicit `{ action: "pass" | "replace" | "recover" }` decision; only `recover` can turn the command into success. A handler failure is logged without hiding the current business error. `observeRequest` follows the same observational rule.

## 3. Plugin-provided commands and distribution

Plugins can add top-level or namespaced commands:

```ts
const auditPlugin = {
  name: "audit",
  provides: {
    namespaces: {
      audit: {
        list: defineCommand({
          name: "list",
          description: "List recent audit entries",
          async run() {
            return { data: [] };
          },
        }),
      },
    },
  },
};
```

A plugin-provided route skips that plugin's own `beforeCommand` but still runs other plugins. Route ownership is computed per App and is not part of the public Plugin object. Business commands override an identical plugin route.

Publish reusable cross-cutting plugins as separate npm packages only when multiple business CLIs need the same behavior. Keep their public options small and test every hook order they rely on.

## 4. Safe debugging and common mistakes

The framework does not provide `--verbose`. A diagnostic plugin may use an environment variable, but should log only method, path, status, duration, and a safe request ID. Never log auth headers, query/body values, or complete responses.

Common mistakes:

1. Signing in `pre` before other plugins finalize headers; use `post` for HMAC.
2. Assuming same-tier order without a lifecycle test.
3. Returning a string from `transformOutput`.
4. Using `handleError` recovery for an ordinary failure instead of returning an explicit `pass`.
5. Sharing an undeclared `ctx.state` field instead of using the same State type in `defineCommands<State>`, `Plugin<State>`, and `defineCli<State>`.
6. Reimplementing route ownership instead of using `provides`.
7. Logging request or response payloads that may contain credentials or personal data.
8. Keeping mutable auth state in a plugin closure instead of a context-bound auth session.
