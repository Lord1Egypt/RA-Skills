# Common Issues and Solutions

## Authentication

### "Could not find Checkly credentials"

```bash
# Solution 1: Interactive login
npx checkly login

# Solution 2: Environment variables
export CHECKLY_API_KEY="cu_xxx"
export CHECKLY_ACCOUNT_ID="12345"
```

### "401 Unauthorized"

1. Verify credentials:
   ```bash
   npx checkly whoami
   ```

2. Regenerate API key in Checkly UI if expired

3. Check that API key has correct permissions

## Configuration

### "No checks found"

1. Check file paths:
   ```bash
   find . -name "*.check.ts" -o -name "*.spec.ts"
   ```

2. Update `checkMatch` pattern in checkly.config.ts

3. Verify files aren't in ignored directories

### "Duplicate logical ID"

Ensure logical IDs are unique:

```typescript
// ❌ Duplicate
new ApiCheck('my-check', { ... })
new ApiCheck('my-check', { ... })  // Error!

// ✅ Unique
new ApiCheck('api-auth-check', { ... })
new ApiCheck('api-users-check', { ... })
```

## Runtime Issues

### "Module not found"

Package not available in Checkly runtime:

```bash
# Check supported packages
npx checkly test --verify-runtime-dependencies
```

See [Checkly Runtimes](https://www.checklyhq.com/docs/runtimes/)

### "Check timeout"

1. Increase timeout (browser checks):
   ```typescript
   test('slow check', async ({ page }) => {
     test.setTimeout(60000)  // 60 seconds
     // ...
   })
   ```

2. Check endpoint accessibility from Checkly locations

## Browser Checks

### Selector Not Found

```typescript
// ❌ Fragile
await page.click('.button')

// ✅ Robust
await page.click('[data-testid="submit-button"]')
await page.click('button:has-text("Submit")')
```

### Flaky Tests

Add explicit waits:

```typescript
// Wait for network idle
await page.waitForLoadState('networkidle')

// Wait for specific element
await page.waitForSelector('[data-testid="content"]')

// Wait for condition
await page.waitForFunction(() => document.readyState === 'complete')
```

## CLI process and upgrade diagnostics

- Exit 3 with `confirmation_required` means pending approval, not an invalid flag (exit 2). Preserve the status and returned command; do not blindly force a retry.
- Results/JSON are on stdout; progress, errors and prompts are on stderr. Keep them separate when parsing.
- `test`/`pw-test` with no checks exit 1. Inspect discovery with `test --list`; use `test --no-fail-on-no-matching` only when emptiness is intentional.
- A CLI timeout is reported as `Timed out` and exits 1; it measures time from check start, and remote work may continue. `--max-failures` can instead leave `Not finished` results.
- Reinstall dependencies with optional packages on the correct OS if the native TypeScript parser cannot load. Fix syntax that the native parser rejects. Malformed tsconfig files are ignored.
- Missing check locations warn: set public/private locations explicitly or through group/project defaults. Logical IDs longer than 255 characters fail validation.
- Account/endpoint variables cannot change after authentication. Set them before CLI launch. `whoami --output json` identifies the effective account and its source.
- Duplicate-install construct errors identify the packages involved. Use the project-installed CLI and align construct resolution; normal CLI delegation selects that installation.

## Deployment

### "Validation errors"

```bash
# Show all errors
npx checkly validate

# Fix errors in code
# Re-validate
npx checkly validate
```

### "Quota exceeded"

- Upgrade Checkly plan
- Delete unused checks in UI
- Optimize check frequency

## API Checks

### Assertion Failures

Use verbose mode to debug local test execution:

```bash
npx checkly test --verbose
```

Shows full request/response details.

For deployed failures, inspect the check record and recent runs:

```bash
npx checkly checks get <check-id>
npx checkly checks get <check-id> --output json
```

Look for `errorGroups`, `rootCause`, or `RCA` fields. If Rocky AI already produced a root-cause analysis, reuse that before adding more manual debugging advice.

### Rocky AI Disabled

If `rca run` reports `Rocky AI is disabled for this account.`, it exits 1 and includes an account-settings link. JSON output includes `code: "ERR_ROCKY_AI_DISABLED"`. Ask an account owner to enable Rocky AI there; retrying or editing check definitions cannot fix the setting. Do not treat every HTTP 403 as this condition.

### Alert Did Not Fire

Use read-only structured evidence; table output can omit critical alerting fields.

```bash
npx checkly checks get <check-id> --output json
npx checkly api /v1/checks/<check-id>
npx checkly alert-channels list --output json --limit 100
```

If the raw REST check payload has a non-null `groupId`, fetch groups once with `npx checkly api /v1/check-groups` and match that ID. Compare only returned `activated`, `muted`, `groupId`, `alertSettings`, `useGlobalAlertSettings`, `alertChannelSubscriptions`, `doubleCheck`, and `retryStrategy` fields. The removal of `groupId` and `doubleCheck` from construct inputs does not remove those API fields; inspect both retry fields on existing checks. Do not probe guessed account/global alert endpoints; if only `useGlobalAlertSettings: true` is visible, report that the global policy details were unavailable in the inspected output.

### Environment Variable Not Working

```typescript
// Note: API_BASE_URL and API_TOKEN are examples of user-defined variables
// for your own checks. They are NOT required by Checkly CLI itself.
// Define them based on your application's needs.

// ✅ Correct usage
request: {
  url: '{{API_BASE_URL}}/users',  // Your custom base URL variable
  headers: [
    { key: 'Authorization', value: 'Bearer {{API_TOKEN}}' },  // Your custom auth token
  ],
}

environmentVariables: [
  { key: 'API_BASE_URL', value: 'https://api.example.com' },
  { key: 'API_TOKEN', value: process.env.API_TOKEN! },  // Load from your .env
]
```

## Getting Help

1. **Check CLI version**:
   ```bash
   npx checkly --version
   ```

2. **Enable verbose logging**:
   ```bash
   npx checkly test --verbose
   ```

3. **Community & Support**:
   - [Checkly Community](https://community.checklyhq.com/)
   - [GitHub Issues](https://github.com/checkly/checkly-cli/issues)
   - [Checkly Support](https://www.checklyhq.com/support/)
