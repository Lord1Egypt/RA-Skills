# CI Failure Fix Patterns

Common GitHub Actions failure patterns and how to auto-fix them.

## Pattern 1: Dependency Issues

**Symptoms:** `npm ERR! Could not resolve dependency`, `Module not found`, `Cannot find module`

**Fix:**
```bash
cd <project-dir>
npm install
git add package-lock.json
git commit -m "fix: resolve dependency issue"
git push
```

## Pattern 2: Test Snapshot Mismatch

**Symptoms:** `Snapshot mismatch`, `toMatchSnapshot`, `received value does not match`

**Fix:**
```bash
cd <project-dir>
npm test -- --update
git add -A
git commit -m "fix: update test snapshots"
git push
```

## Pattern 3: TypeScript Errors

**Symptoms:** `TS2xxx`, `Type error`, `Property does not exist on type`

**Fix:** Read the error, fix the type issue in source code. Usually requires understanding the code — not auto-fixable for complex cases.

**Auto-fixable cases:**
- Missing `@ts-ignore` → add comment
- Unused imports → remove them
- Missing type exports → add `export type`

## Pattern 4: ESLint / Prettier Errors

**Symptoms:** `Lint errors`, `Formatting issues`, `eslint`

**Fix:**
```bash
cd <project-dir>
npx eslint --fix .
npx prettier --write .
git add -A
git commit -m "fix: resolve lint errors"
git push
```

## Pattern 5: Environment Variable / Token Issues

**Symptoms:** `Unauthorized`, `401`, `VERCEL_TOKEN`, `GITHUB_TOKEN`, `token expired`

**Fix:** Cannot auto-fix — requires human to rotate/update secrets. Report to user with diagnosis.

## Pattern 6: Build Timeout

**Symptoms:** `The job running on runner has exceeded the maximum execution time`

**Fix:** Usually indicates infinite loop or resource exhaustion. Read logs, identify the stuck step. Not auto-fixable.

## Pattern 7: E2E Test Failures (Playwright)

**Symptoms:** `browserType.launch`, `Timeout exceeded`, `locator.click`

**Fix:**
```bash
cd <project-dir>
npx playwright install
npx playwright test --update-snapshots
git add -A
git commit -m "fix: update E2E snapshots"
git push
```

## Decision Tree

```
Failure detected
├── Dependency error? → npm install + push
├── Snapshot mismatch? → npm test --update + push
├── Lint error? → eslint --fix + push
├── E2E snapshot? → playwright --update-snapshots + push
├── Token/Auth error? → REPORT ONLY (human needed)
├── Type error (simple)? → TRY fix, push if confident
└── Unknown? → REPORT ONLY with diagnosis
```

## Reading Build Logs

```bash
# Get the latest failed run's logs
gh run view --repo OWNER/REPO --log 2>&1 | tail -50

# Get specific run by ID
gh run view <run-id> --repo OWNER/REPO --log 2>&1 | grep -A5 "error\|Error\|FAIL"
```

## Cron Integration

Set up as an OpenClaw cron job:
```
Schedule: every 30m
Model: haiku (cheap, sufficient for script + log reading)
Script: scripts/check-ci-failures.sh
```

When failures detected, the agent should:
1. Read build logs (`gh run view --log`)
2. Match against known patterns above
3. Auto-fix if pattern is recognized and safe
4. Report to user with diagnosis if unknown
5. After fix: wait 90s, re-check if build passed
