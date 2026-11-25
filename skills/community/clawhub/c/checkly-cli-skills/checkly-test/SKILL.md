---
name: checkly-test
description: Test Checkly checks locally using npx checkly test command, including filtering, reporters, retry strategies, and debugging workflows. Use when testing checks before deployment, validating changes, debugging failures, or running checks in CI/CD. Triggers on checkly test, test checks, run checks locally, check validation, debug checks.
---

# checkly test

Test Checkly checks locally with `npx checkly test`.

## Quick start

```bash
# Test all checks
npx checkly test

# Test specific check
npx checkly test __checks__/api.check.ts

# Test with verbose output
npx checkly test --verbose

# Test in specific location
npx checkly test --location=eu-west-1

# List recorded test sessions after CI or cloud runs
npx checkly test-sessions list --status failed --limit 10

# Drill into a failed session and a specific result/error group
npx checkly test-sessions get <session-id> --result <result-id>
npx checkly test-sessions get <session-id> --error-group <error-group-id> --full-error
```

## How it works

`npx checkly test` executes your checks in Checkly's runtime environment (same as production) without deploying persistent resources or changing recurring schedules. Perfect for:
- ✅ Pre-deployment validation
- ✅ CI/CD integration
- ✅ Local development iteration
- ✅ Debugging check failures

The CLI dispatches test sessions through Checkly's asynchronous scheduling API and watches scheduling before collecting results. Scheduling failures now fail fast with the server error instead of waiting for the per-check timeout. With `--detach`, the CLI confirms scheduling reached a terminal state before exiting, so dispatch failures still return non-zero.

## Empty selections, timeouts and early stopping

`test` exits 1 if no checks match a file filter, `--grep` or `--tags`. Use `--list` to inspect the selection (exit 0), or `--no-fail-on-no-matching` only when an empty selection is intentional. `pw-test` also exits 1 for no checks; it has no matching opt-out flag. A passing empty selection must not stand in for a test gate.

```bash
npx checkly test --list
npx checkly test --tags smoke --max-failures=2
npx checkly trigger --max-failures=2
# Only for workflows where zero matches are intentionally acceptable
npx checkly test --grep optional --no-fail-on-no-matching
```

`--max-failures=<n>` on `test` and `trigger`, or `cli.maxFailures`, stops waiting once n checks have final failures, writes reports, requests best-effort session cancellation and exits 1. The limit must be an integer of at least 1; omit the setting for no limit. A successful retry does not count as a failure. Unfinished checks report `Not finished`; JSON includes `stoppedEarly`. Some checks may still execute remotely. The flag cannot combine with `--detach`, or with `test --update-snapshots`. A configured `cli.maxFailures` is ignored for detached runs and ignored with a notice for snapshot updates.

For `test`, `trigger` and `pw-test`, `--timeout` measures run time from each check's start and restarts on retries. Scheduling delay is excluded; a check that never starts times out after the configured timeout plus 900 seconds. CLI-side timeouts mean the CLI stopped waiting, not necessarily that the remote check stopped.

Timed-out results use `result: "Timed out"` in JSON, `T` in dot output, and a timeout marker/count in list/CI/GitHub reporters; exit remains 1. Match both `Fail` and `Timed out` if parsing result strings, or use exit status. Reporters show retry counts and count recovered checks as both passed and flaky. The CLI guards against duplicate results at timeout boundaries and retries failed result-stream connections. Cancellation failure no longer crashes Ctrl+C handling; a second Ctrl+C yields shell status 130.

Stdout contains results and summaries. Progress, warnings and errors go to stderr. Default reporter is `ci` in CI and agent mode, `list` otherwise; an explicit flag/config overrides it. Set `CI=false` (or `0`, `no`, `off`) to disable CI detection even on provider hosts. Avoid pinning `reporters: ['list']` in general-purpose configs if automatic selection is desired.


## Command reference

```bash
npx checkly test [file-pattern] [options]
```

### Options

| Flag | Description |
|------|-------------|
| `--location=<location>` | Run in specific datacenter (e.g., `us-east-1`) |
| `--verbose, -v` | Show full check output and logs |
| `--reporter=<type>` | Output format: `list`, `dot`, `ci`, `github`, `json` |
| `--retries=<n>` | Retry failed checks (0-3) |
| `--config=<path>` | Path to checkly.config.ts |
| `--verify-runtime-dependencies` | Validate npm package versions |
| `--refresh-cache` | Force a one-off dependency reinstall for this run |
| `--env-file=<path>` | Load environment variables from file |
| `--grep=<pattern>` | Filter checks by name pattern |
| `--tags=<tags>` | Filter by tags |
| `--list` | List matching checks without running them |
| `--no-fail-on-no-matching` | Accept an intentionally empty test selection |
| `--max-failures=<n>` | Stop after n final failures (integer >= 1) |
| `--timeout=<seconds>` | Per-check running timeout; scheduling delay excluded |

## Recorded test sessions

Use `test-sessions` drilldown commands for recorded sessions after `npx checkly test`, `npx checkly trigger`, CI runs, or Playwright Reporter uploads when you need failure details, result IDs, or error-group context for RCA.

For cancelled or timed-out runs started by `checkly test`, `checkly trigger`, or `checkly pw-test`, inspect the recorded session with the existing commands below; cancellation handling is backend/runner wiring rather than a separate public `test-sessions` command or flag.

```bash
# List recent sessions
npx checkly test-sessions list

# List failed sessions from a branch as JSON
npx checkly test-sessions list --status failed --branch main --limit 20 --output json

# Filter sessions by provider or error group
npx checkly test-sessions list --provider github --error-group <error-group-id>

# Inspect a session summary and error-group IDs
npx checkly test-sessions get <session-id>

# Wait for a running session to finish before rendering
npx checkly test-sessions get <session-id> --watch

# Drill into one result or one error group
npx checkly test-sessions get <session-id> --result <result-id>
npx checkly test-sessions get <session-id> --error-group <error-group-id> --full-error
```

### `test-sessions list` flags

| Flag | Description |
|------|-------------|
| `--limit`, `-l` | Number of sessions to return (1-100; default 20). |
| `--cursor` | Cursor from previous output for pagination. |
| `--from` / `--to` | ISO date or Unix timestamp range filters. |
| `--status` | Filter by `running`, `failed`, `passed`, or `cancelled`; repeatable. |
| `--branch` | Filter by Git branch; repeatable. |
| `--user` / `--no-users` | Filter by commit owner/invoking user, or include sessions without users. |
| `--provider` | Filter by `github`, `vercel`, `api`, `trigger`, or `pw_reporter`; repeatable. |
| `--search`, `-s` | Search session text fields (3-200 characters). |
| `--error-group` | Filter by test-session error group ID. |
| `--output`, `-o` | Output format: `table`, `json`, or `md`. |

### `test-sessions get` flags

| Flag | Description |
|------|-------------|
| `--result`, `-r` | Show details for a specific test-session result ID. |
| `--error-group` | Show details for an error group ID from the session. |
| `--error-groups-limit` | Number of error-group IDs to show in the summary (default 5). |
| `--full-error` | Print complete raw error for an error group. |
| `--watch`, `-w` | Watch a running session until it completes before rendering. |
| `--output`, `-o` | Output format: `detail`, `json`, or `md`. |

## Workflows

### Basic testing

```bash
# Test everything
npx checkly test

# Output:
# Parsing your project... done
# Running 3 checks in us-east-1.
# 
# __checks__/api.check.ts
#  ✔ API Status Check (234ms)
# __checks__/homepage.spec.ts  
#  ✔ Homepage Check (2.1s)
# __checks__/login.spec.ts
#  ✔ Login Flow (3.4s)
#
# 3 passed, 3 total
```

### Test specific checks

```bash
# Single file
npx checkly test __checks__/api.check.ts

# Multiple files
npx checkly test __checks__/api.check.ts __checks__/homepage.spec.ts

# Pattern matching
npx checkly test __checks__/api-*.check.ts

# By name (grep)
npx checkly test --grep="Homepage"
```

### Verbose debugging

```bash
npx checkly test --verbose

# Shows:
# - Request/response details (API checks)
# - Console logs (browser checks)
# - Screenshots (on failure)
# - Full stack traces
# - Environment variables used
```

### Testing in different locations

```bash
# Test from EU datacenter
npx checkly test --location=eu-west-1

# Test from multiple locations (requires configuration)
# Set in checkly.config.ts:
checks: {
  locations: ['us-east-1', 'eu-west-1'],
}
```

### CI/CD integration

```yaml
# GitHub Actions
name: Test Checks
on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-node@v7
        with:
          node-version: '22.13.0'
      
      - run: npm ci
      - run: npx checkly test
        env:
          CHECKLY_API_KEY: ${{ secrets.CHECKLY_API_KEY }}
          CHECKLY_ACCOUNT_ID: ${{ secrets.CHECKLY_ACCOUNT_ID }}
```

### GitHub Check re-runs

For optional GitHub Check Re-run integration and the job-ID/re-run-mode metadata forwarded with test sessions, see `checkly-advanced`. The `github` reporter writes a Markdown summary file; it does not emit annotations or enable that integration by itself.

### Test with retries

```bash
# Retry failed checks once
npx checkly test --retries=1

# Useful for flaky tests or network issues
```

### Environment variables

```bash
# Inline
API_BASE_URL=https://staging.example.com npx checkly test

# From .env file
npx checkly test --env-file=.env.test

# .env.test
API_BASE_URL=https://staging.example.com
API_KEY=test-key-123
```

## Reporters

The `github` and `json` file reporters send completed-check counters and retried-attempt progress to stderr, not into the report files. With `list`, `dot` or `ci`, that console reporter supplies progress; with `github,json`, only the first file reporter supplies it. They do not duplicate the startup `Running N checks` line. Stdout summaries and report formats are unchanged.

### List reporter (default outside CI and agent mode)

```bash
npx checkly test --reporter=list

# Detailed output with timings
```

### Dot reporter

```bash
npx checkly test --reporter=dot

# Compact: . = pass, F = fail, T = timed out
```

### CI reporter

```bash
npx checkly test --reporter=ci

# Optimized for CI logs
```

### GitHub reporter

GitHub table cells escape pipes and replace CR/LF line breaks with spaces in check names, types and filenames, including unfinished rows. Like JSON, its progress goes to stderr; see the shared reporter rules above.

```bash
npx checkly test --reporter=github

# Writes ./checkly-github-report.md (override with CHECKLY_REPORTER_GITHUB_OUTPUT)
```

### JSON reporter

JSON is written to `./checkly-json-report.json` (override with `CHECKLY_REPORTER_JSON_OUTPUT`). Parse that file; stdout contains a brief summary, saved-file notice and session URL, not the JSON report. Keep stderr separate for progress and diagnostics.

```bash
npx checkly test --reporter=json

# Writes ./checkly-json-report.json (override with CHECKLY_REPORTER_JSON_OUTPUT)
```

For failed gRPC, SSL, and traceroute monitors, terminal and JSON reporters include type-specific diagnostics when available. Inspect gRPC status/health/metadata, TLS certificate and handshake details, or traceroute hops/latency/packet loss before falling back to generic network troubleshooting.

## Testing strategies

Before running, resolve configuration errors: retired `me-south-1` in locations/defaults is rejected, and `--location me-south-1` fails with exit 2. A `SlackAppAlertChannel` with destinations fails when the account reports the Checkly Slack app as disconnected; connect the app or remove the channel. The same validation applies to `validate`, `deploy` and `pw-test`.

If `test`, `pw-test` or `trigger` cannot connect to the result stream, the error identifies the Checkly connection failure and includes its cause in `Details`, including per-address causes from an aggregate connection error. Diagnose connectivity/proxy/broker configuration; an MQTT transport failure is not a failed assertion. Errors while processing results or reporter callbacks fail the run rather than escaping as unhandled queue/timer errors. Once the run stops, pending timers and queued results are cleared.

### Local-first workflow

```bash
# 1. Write Playwright test
cat > __checks__/new-feature.spec.ts

# 2. Test locally with Playwright (fastest)
npx playwright test __checks__/new-feature.spec.ts

# 3. Validate in Checkly runtime
npx checkly test __checks__/new-feature.spec.ts

# 4. Deploy when passing
npx checkly deploy
```

### Pre-deployment validation

```bash
# Run full test suite before deploy
npx checkly test && npx checkly deploy --force
```

### Debugging failures

```bash
# 1. Run with verbose output
npx checkly test __checks__/failing.spec.ts --verbose

# 2. Check for common issues:
#    - API endpoint changed?
#    - Auth token expired?
#    - Selector changed (browser checks)?
#    - Environment variable missing?

# 3. Test locally first (browser checks)
npx playwright test __checks__/failing.spec.ts --headed

# 4. Compare environments
#    - Local vs Checkly runtime
#    - Check Node.js version
#    - Check npm package versions
```

## Troubleshooting

### "No checks found to test"

**Solution**:
```bash
# Check configuration
npx checkly validate

# Verify files exist
ls -la __checks__/

# Check checkMatch pattern in checkly.config.ts
```

### "Check failed: Connection timeout"

**Causes**:
- Endpoint not accessible from Checkly locations
- Firewall blocking Checkly IPs
- Endpoint genuinely down

**Solution**:
```bash
# Test from different location
npx checkly test --location=eu-west-1

# For private endpoints, use private locations
```

### "Module not found" errors

**Cause**: npm package not available in Checkly runtime

**Solution**:
```bash
# Validate dependencies
npx checkly test --verify-runtime-dependencies

# See supported packages:
# https://www.checklyhq.com/docs/runtimes/
```

### Flaky tests

**Solution**:
```bash
# Enable retries
npx checkly test --retries=2

# Or configure in checkly.config.ts:
checks: {
  retryStrategy: RetryStrategyBuilder.fixedStrategy({
    maxRetries: 2,
    baseBackoffSeconds: 60,
  }),
}
```

## Testing vs Deploying

| Command | Purpose | Scheduled | Billed |
|---------|---------|-----------|--------|
| `npx checkly test` | Validation | ❌ No | ❌ No* |
| `npx checkly deploy` | Production monitoring | ✅ Yes | ✅ Yes |

*Test runs count towards your account's test run limit but are not billed separately.

## Related Skills

- See `checkly-deploy` for deploying checks after testing
- See `checkly-checks` for creating checks to test
- See `checkly-playwright` for Playwright-specific testing
- See `checkly-advanced` for retry strategies and reporters
