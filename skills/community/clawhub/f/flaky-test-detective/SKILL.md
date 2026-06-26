---
name: flaky-test-detective
description: Detect, diagnose, and fix flaky tests. Identify tests with non-deterministic outcomes by analyzing CI history, test timing, shared state, race conditions, and environment dependencies — then provide targeted fixes.
---

# Flaky Test Detective

Hunt down flaky tests — the ones that pass sometimes and fail sometimes with no code change. Analyze CI run history, detect timing-sensitive tests, find shared mutable state, identify race conditions, and generate targeted fixes for each flaky test.

Use when: "find flaky tests", "test keeps failing randomly", "CI is unreliable", "non-deterministic test failures", "test stability", "intermittent failures", or when builds fail but pass on retry.

## Commands

### 1. `detect` — Find Flaky Tests

#### Step 1: Analyze CI History

```bash
# GitHub Actions — get recent test failures
gh run list --limit 30 --json conclusion,headBranch,createdAt,databaseId | \
  python3 -c "
import json, sys
runs = json.load(sys.stdin)
failures = [r for r in runs if r['conclusion'] == 'failure']
retried = [r for r in runs if r['headBranch'] == runs[0]['headBranch'] and r['conclusion'] != failures[0]['conclusion']]
print(f'Total runs: {len(runs)}')
print(f'Failures: {len(failures)} ({len(failures)/len(runs)*100:.0f}%)')
if retried:
    print(f'Flaky signal: same branch has both pass and fail')
"

# Download test results (JUnit XML)
gh run download <RUN_ID> --name test-results 2>/dev/null
```

#### Step 2: Statistical Detection

Run the test suite multiple times and track results:

```bash
# Run tests N times and collect results
RESULTS_FILE="/tmp/flaky-results.json"
echo '[]' > "$RESULTS_FILE"

for i in $(seq 1 5); do
  echo "=== Run $i/5 ==="
  # Capture per-test results (adjust for your framework)
  npm test -- --json 2>/dev/null | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    for suite in data.get('testResults', []):
        for test in suite.get('testResults', []):
            print(f'{test[\"status\"]}\t{test[\"fullName\"]}')
except: pass
" >> "/tmp/run-$i.txt"
done

# Find tests with inconsistent results across runs
python3 -c "
import os, collections
results = collections.defaultdict(list)
for i in range(1, 6):
    path = f'/tmp/run-{i}.txt'
    if os.path.exists(path):
        for line in open(path):
            parts = line.strip().split('\t', 1)
            if len(parts) == 2:
                results[parts[1]].append(parts[0])

for test, outcomes in sorted(results.items()):
    unique = set(outcomes)
    if len(unique) > 1:
        pass_rate = outcomes.count('passed') / len(outcomes) * 100
        print(f'🎯 FLAKY ({pass_rate:.0f}% pass rate): {test}')
        print(f'   Outcomes: {\" → \".join(outcomes)}')
"
```

#### Step 3: Pattern Analysis

For each flaky test, analyze the failure to classify the root cause:

**Timing-dependent:**
```bash
# Check for setTimeout, sleep, waitFor with hardcoded timeouts
rg "setTimeout|sleep|waitFor|delay|\.timeout" --type ts --type js -g '*test*' -g '*spec*' 2>/dev/null
```

**Shared state:**
```bash
# Check for global variables, singletons, shared fixtures
rg "beforeAll|before\(|global\.|singleton|shared" --type ts --type js -g '*test*' -g '*spec*' 2>/dev/null
```

**Test order dependency:**
```bash
# Run tests in random order
npm test -- --randomize 2>/dev/null
pytest --randomly 2>/dev/null
go test -shuffle=on ./... 2>/dev/null
```

**Environment dependency:**
```bash
# Check for hardcoded ports, paths, dates, timezones
rg "localhost:[0-9]+|/tmp/|/var/|new Date\(\)|Date\.now\(\)" --type ts --type js -g '*test*' 2>/dev/null
```

**Network dependency:**
```bash
# Check for real HTTP calls in tests
rg "fetch\(|axios\.|http\.get|requests\.(get|post)" --type ts --type js --type py -g '*test*' 2>/dev/null
```

#### Step 4: Generate Report

```markdown
# Flaky Test Report

## Summary
- Tests analyzed: 342
- Flaky tests found: 7
- Test suite reliability: 98% (target: 99.9%)

## Flaky Tests

### 1. `UserService.test.ts` — "should send welcome email"
- **Pass rate:** 60% (3/5 runs)
- **Root cause:** Timing — test waits 100ms but email service sometimes takes 200ms
- **Fix:** Replace `setTimeout(100)` with `waitFor(() => expect(emailSent).toBe(true))`
- **Category:** ⏱️ Timing

### 2. `OrderController.test.ts` — "should calculate total"
- **Pass rate:** 80% (4/5 runs)
- **Root cause:** Shared state — previous test modifies global discount config
- **Fix:** Reset `DiscountConfig` in `beforeEach()` or isolate with `jest.isolateModules()`
- **Category:** 🔗 Shared State

### 3. `DateFormatter.test.ts` — "should format date correctly"
- **Pass rate:** 40% (2/5 runs)
- **Root cause:** Timezone — test assumes UTC but CI runs in different timezone
- **Fix:** Use `new Date('2024-01-15T00:00:00Z')` instead of `new Date('2024-01-15')`
- **Category:** 🌐 Environment
```

### 2. `fix` — Generate Fixes for Flaky Tests

For each root cause category, apply the appropriate fix pattern:

- **Timing:** Replace fixed delays with polling/retry assertions
- **Shared state:** Add setup/teardown, use test isolation
- **Order dependency:** Make tests independent, reset state
- **Network:** Mock external calls, use test fixtures
- **Environment:** Pin timezone, use deterministic dates, avoid temp paths

### 3. `quarantine` — Manage Flaky Test Quarantine

Move known-flaky tests to a quarantine suite that runs separately:
- Tag with `@flaky` or skip with documentation
- Track quarantined tests in a manifest file
- Alert when quarantine grows beyond threshold
- Automatically un-quarantine after fix is merged and verified stable (5 consecutive passes)
