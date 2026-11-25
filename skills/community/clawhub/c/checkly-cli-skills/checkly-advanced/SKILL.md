---
name: checkly-advanced
description: Advanced Checkly CLI features including retry strategies, reporters, GitHub Check re-runs, environment variables, bundling, and custom patterns. Use when implementing complex retry logic, customizing test output, configuring opt-in GitHub Check re-run integration, managing secrets, or troubleshooting advanced scenarios. Triggers on retry strategy, reporter, GitHub Check re-run, Re-run button, repository_dispatch, environment variables, bundling, advanced configuration.
---

# checkly advanced

Advanced Checkly CLI features and patterns.

## Retry Strategies

API/browser/multistep checks and `CheckGroupV1` default to one immediate retry in another region. Monitors and Playwright suites default to no CLI retries. Use `RetryStrategyBuilder.singleRetry({ baseBackoffSeconds: 0, sameRegion: false })` for the immediate cross-region behavior or `RetryStrategyBuilder.noRetries()` to disable it. Bare `singleRetry()` waits 60 seconds in the same region.

### Fixed retry

```typescript
import { RetryStrategyBuilder } from 'checkly/constructs'

retryStrategy: RetryStrategyBuilder.fixedStrategy({
  baseBackoffSeconds: 60,
  maxRetries: 2,
  maxDurationSeconds: 600,
  sameRegion: true,
})
```

### Linear backoff

```typescript
retryStrategy: RetryStrategyBuilder.linearStrategy({
  baseBackoffSeconds: 30,
  maxRetries: 3,
  maxDurationSeconds: 600,
  sameRegion: false,
})
```

### Exponential backoff

```typescript
retryStrategy: RetryStrategyBuilder.exponentialStrategy({
  baseBackoffSeconds: 10,
  maxRetries: 5,
  maxDurationSeconds: 600,
  sameRegion: true,
})
```

### Conditional retries

```typescript
// Retry only on network errors (API checks only)
retryStrategy: RetryStrategyBuilder.fixedStrategy({
  maxRetries: 2,
  onlyOn: 'NETWORK_ERROR',
})
```

## Reporters

File reporters (`github`, `json`) send progress to stderr. Only the first supplies progress when combined; `list`, `dot` or `ci` takes precedence. Stdout is not the JSON report. Keep stderr separate when processing results.

With no explicit reporter, CI and agents use `ci`, other runs use `list`. Results go to stdout, diagnostics to stderr. Timed-out checks produce `Timed out` in JSON / `T` in dot output and exit 1. `--max-failures` on test/trigger reports unfinished checks separately; see `checkly-test`.

### List reporter (default outside CI and agent mode)

```bash
npx checkly test --reporter=list
```

### Dot reporter (compact)

```bash
npx checkly test --reporter=dot
```

### JSON reporter

Parse `./checkly-json-report.json`, or the path in `CHECKLY_REPORTER_JSON_OUTPUT`, rather than piping stdout into a JSON parser.

```bash
npx checkly test --reporter=json
```

### GitHub Markdown reporter

```bash
npx checkly test --reporter=github
```

Writes a Markdown summary to `./checkly-github-report.md`, or the path in
`CHECKLY_REPORTER_GITHUB_OUTPUT`. It does not emit GitHub Actions annotations or
configure a Checkly GitHub Check's Re-run button.

### CI reporter

```bash
npx checkly test --reporter=ci
```

## GitHub Check re-runs

The Markdown summary from `--reporter=github` is separate from test-session repository metadata. With `CHECKLY_GITHUB_REPORT=true` or `1` (case-insensitive and whitespace-trimmed), the CLI includes a `github` object in the session's repository information when repository information is available. It forwards these optional environment values:

- `CHECKLY_GITHUB_JOB_ID` → `github.jobId`: the numeric job check-run ID from `${{ job.check_run_id }}`, forwarded as a string. This is not `${{ github.job }}` (the job key, used by `CHECKLY_GITHUB_JOB`) or the workflow run ID in `CHECKLY_GITHUB_RUN_ID`. The CLI trims/forwards it without numeric validation, so the caller must supply the correct ID.
- `CHECKLY_GITHUB_RERUN` → `github.rerun`: the re-run mode, such as `repository-dispatch`; this is not a boolean CLI flag.

Both values are trimmed; unset, empty, or whitespace-only values are omitted from the serialized payload. With the action's `github-check-rerun: true` and `github-job-id: ${{ job.check_run_id }}` inputs, a Re-run click causes Checkly to send a `repository_dispatch` event of type `checkly-github-check-rerun`; a separate handler workflow on the repository's default branch invokes `checkly/checkly-action/rerun@v1` to perform the re-run. Forwarding metadata alone does not configure that handler or grant GitHub permissions.

See [complete caller/handler setup and compatibility requirements](references/github-rerun.md) before enabling it. Keep the handler's event-type filter and narrowly scoped `actions: write` permission. This is for detached runs reporting through a Checkly GitHub Check; `reporting: github-actions` and runs that fall back to waiting ignore the opt-in. An older resolved CLI without job-ID forwarding support fails the detached action step before running checks; `job.check_run_id` is unavailable on GitHub Enterprise Server.

Keep re-run opt-in and workflow permissions explicitly reviewed: GitHub re-runs the selected job **and dependent jobs**, using the original run's commit/workflow and original actor privileges. Review network checks, deployments, and every dependent job's other side effects before approval. Do not invent a job ID, add broad permissions, or enable re-runs just to populate metadata. These instructions describe setup; they are not authorization to install an app, change workflow permissions, or trigger a run.

## Environment Variables

### CLI crash reporting

Released CLI builds with reporting configured can send one report per invocation for a detected bug in the CLI's own code, including bugs caught and printed by a command. Set `CHECKLY_NO_ERROR_REPORTING=1` or `DO_NOT_TRACK=1` before invocation to opt out. This control is separate from test execution and authentication.

Reports select error names/messages/stacks and CLI version, command/mode, OS, architecture and runtime information. They do not attach the full environment, command arguments or arbitrary error properties. The scrubber targets Checkly user/service API keys, Basic/Bearer credentials, URL credentials and known project/home/install paths. These targeted transformations are not a guarantee that every secret or user-provided value in an error message is removed.

### Global variables

```typescript
// checkly.config.ts
checks: {
  environmentVariables: [
    { key: 'API_URL', value: 'https://api.example.com' },
    { key: 'API_KEY', value: process.env.API_KEY!, locked: true },
  ],
}
```

### Group-level variables

```typescript
const group = new CheckGroup('api-group', {
  environmentVariables: [
    { key: 'SERVICE', value: 'api' },
  ],
})
```

### Check-level variables

```typescript
new ApiCheck('check', {
  environmentVariables: [
    { key: 'ENDPOINT', value: '/status' },
  ],
})
```

## Validation Options

```bash
# Verify runtime dependencies
npx checkly test --verify-runtime-dependencies

# Show verbose output
npx checkly test --verbose

# Validate without running
npx checkly validate
```

## Custom patterns

### Dynamic check generation

```typescript
const endpoints = ['users', 'products', 'orders']

endpoints.forEach(endpoint => {
  new ApiCheck(`${endpoint}-api`, {
    name: `${endpoint} API`,
    request: {
      url: `https://api.example.com/${endpoint}`,
    },
  })
})
```

### Shared alert configurations

```typescript
// alerts.ts
export const criticalAlerts = [emailChannel, slackChannel, pagerduty]

// check.ts
new ApiCheck('critical-check', {
  alertChannels: criticalAlerts,
})
```

## Related Skills

- See `checkly-constructs` for construct system details
- See `checkly-test` for testing options
- See `checkly-checks` for applying advanced features
