---
name: argus
version: 1.0.0
description: |
  Incremental backend API + frontend browser testing with persistent memory.
  Monitors every commit, enriches insufficient messages, and runs targeted tests
  scoped to changed files. Full-catalog runs on demand.
  Use when: "argus", "run tests", "test my backend", "check this commit".
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
---

# Argus — Automated Testing Skill

> Hundred-eyed. Never sleeps. Every fixed bug becomes a permanent eye.

---

## Command Routing

Parse the user's invocation and jump to the correct phase:

| Command | Action |
|---|---|
| `/argus init` | → Phase 1: Bootstrap |
| `/argus` | → Phase 3 → 4 → 5 → 6 → 7 (full run) |
| `/argus test --backend` | → Phase 5 only |
| `/argus test --frontend` | → Phase 6 only |
| `/argus test --diff` | → Phase 5 + 6, scoped to current branch diff |
| `/argus catalog` | → Phase 3 only (update catalog, no tests) |
| `/argus report` | → Phase 7 only (show last report) |

If no `.argus/catalog.md` exists and command is not `init`, say:
> "Argus has not been initialized. Run `/argus init` first."

---

## File Layout

```
.argus/
  catalog.md          # test knowledge base — source of truth
  baseline.json       # health score history
  reports/
    YYYY-MM-DD.md     # per-run reports
  commit-hook.sh      # installed into .git/hooks/post-commit

tests/
  backend/
    conftest.py
    test_{module}.py
  frontend/
    test_{flow}.py
```

---

## catalog.md Format

First line is always the scan cursor:
```
last_scanned_commit: {SHA}
```

Each test entry:
```markdown
## {test_function_name}
- Type: backend | frontend
- Source: fix commit {SHA} — {description} | generated (routes scan) | manual | adversarial
- Protection: locked | regenerable | deprecated
- Covers: {endpoint or file list}
- File: tests/{path}::{function_name}
- Status: pending | generated | active ✅ | failing ❌ | deprecated
- Last run: {YYYY-MM-DD} {passed|failed}
```

**Protection rules (never violate):**

| Protection | Source | Auto-delete | Auto-modify |
|---|---|---|---|
| `locked` | fix commit / manual | ❌ Never | ❌ Never |
| `regenerable` | generated / adversarial | ✅ Yes | ✅ Yes |
| `deprecated` | endpoint removed | Confirm with user | — |

---

## Phase 1 — Bootstrap (`/argus init`)

**Step 1: Scan routes for endpoints**

Read all files matching `backend/app/routes/*.py` and `backend/app/routers/*.py` (and equivalent paths). For each file extract:
- HTTP method + path (from `@router.get(...)`, `@router.post(...)`, etc.)
- Auth requirement (look for `Depends(get_current_user)` etc.)
- Key business logic (rate limits, SSE, file operations)

Do NOT use OpenAPI spec. Source code is ground truth.

**Step 2: Mine git history for bugs**

```bash
git log --oneline --all | head -100
```

Filter commits whose message contains: `fix`, `bug`, `修复`, `修正`, `hotfix`, `patch`.

For each matched commit:
```bash
git show {SHA} --stat --format="%s%n%b"
```

Extract: changed files, affected endpoints, what broke.

**Step 3: Read bugfix.md if present**

```bash
cat bugfix.md 2>/dev/null || cat BUGFIX.md 2>/dev/null
```

Extract any documented regression risks and key protected files.

**Step 4: Generate catalog.md**

Create `.argus/catalog.md`. For each discovered test case:
- fix commit → Protection: `locked`
- routes scan → Protection: `regenerable`
- Set all Status: `pending`
- Set `last_scanned_commit` to current HEAD SHA

```bash
git rev-parse HEAD
```

**Step 5: Generate tests/backend/conftest.py**

Read existing `tests/` directory if present. If conftest.py exists, do not overwrite.

Generate a conftest.py with:
- `base_url` fixture reading from env `TEST_BASE_URL` (default `http://localhost:8000`)
- `client` fixture using `httpx.AsyncClient`
- `guest_client` fixture (unauthenticated)
- `auth_headers` fixture (reads `TEST_AUTH_TOKEN` from env)

**Step 6: Install git hook**

Write `.argus/commit-hook.sh`:
```bash
#!/bin/bash
# Argus post-commit hook
# Enriches insufficient commit messages and runs incremental tests

COMMIT_MSG=$(git log -1 --format="%s%n%b")
CHANGED_FILES=$(git diff HEAD~1 HEAD --name-only 2>/dev/null || echo "")

# Pass to argus for analysis
echo "[Argus] Analyzing commit..."
# Claude will be invoked here via: claude -p "argus post-commit"
# For now, log for manual review
echo "[Argus] Changed files: $CHANGED_FILES" >> .argus/commit-log.txt
echo "[Argus] Message: $COMMIT_MSG" >> .argus/commit-log.txt
```

Symlink or copy to `.git/hooks/post-commit`:
```bash
cp .argus/commit-hook.sh .git/hooks/post-commit
chmod +x .git/hooks/post-commit
```

**Step 7: Confirm**

Print summary:
```
Argus initialized.
  Endpoints discovered: {N}
  Fix commits mined: {N}
  Catalog entries created: {N}  (locked: {N}, regenerable: {N})
  Hook installed: .git/hooks/post-commit

Next: run /argus to generate test code and execute.
```

---

## Phase 2 — Commit Monitoring + Enrichment

**Triggered by:** `post-commit` hook or manually reviewing the last commit.

**Step 1: Read the last commit**

```bash
git log -1 --format="%H%n%s%n%b"
git diff HEAD~1 HEAD --name-only
git diff HEAD~1 HEAD --stat
```

**Step 2: Score the commit message**

A commit message is INSUFFICIENT if any of these are true:
- Subject line is fewer than 15 characters
- Subject is generic: "update", "fix", "wip", "test", "changes", "misc", "cleanup" with nothing after
- Diff touches ≥ 3 files but message gives no indication of what changed
- Diff contains route/API changes but no endpoint is mentioned
- Message contains "fix" or "bug" or "修复" but describes no specific behavior

**Step 3: If INSUFFICIENT — enrich**

Analyze the diff deeply:
- Which routes/endpoints changed?
- What business logic was added or modified?
- Is there a rate limit, auth check, or data validation change?
- Is this a bug fix? What was the broken behavior?

Generate enrichment block. Amend the commit (only safe before push):

```bash
# Check if already pushed
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/$(git branch --show-current) 2>/dev/null || echo "none")

if [ "$LOCAL" != "$REMOTE" ]; then
  # Safe to amend
  git commit --amend --no-edit -m "$(git log -1 --format='%s%n%n%b')

[Argus] Auto-enriched
Changed:
  {list of changed endpoints or files with brief description}

TESTABLE:
  endpoint: {most testable endpoint changed}
  scenario: {concrete behavior that should be verified}
  risk: {low|medium|high}"
fi
```

If already pushed: write enrichment to `.argus/commit-notes/{SHA}.md` instead, and note:
> "Commit {SHA} already pushed. Enrichment saved to .argus/commit-notes/{SHA}.md"

**Step 4: If SUFFICIENT**

If message already has `TESTABLE:` block: extract and queue for Phase 3.
If message is clear but has no `TESTABLE:` block: generate one and append to the amend.

---

## Phase 3 — Incremental Catalog Update

**Step 1: Determine scan range**

Read `last_scanned_commit` from `.argus/catalog.md`.

```bash
git log {last_scanned_commit}..HEAD --format="%H %s"
```

If `last_scanned_commit` is empty or not found, scan last 20 commits.

**Step 2: Process each new commit**

For each commit in range:
```bash
git show {SHA} --format="%s%n%b" --stat
```

Extract:
- Any `TESTABLE:` block in the message body
- Whether it's a fix/bug commit (even without TESTABLE block)
- Which files changed

**Step 3: For fix commits without TESTABLE block**

Read the diff:
```bash
git show {SHA} --unified=5
```

Infer what should be tested from the code change. Generate a catalog entry with:
- Source: `fix commit {SHA}`
- Protection: `locked`
- Status: `pending`

**Step 4: For TESTABLE blocks**

Parse each field. Create catalog entry:
- Source: `fix commit {SHA} — {commit subject}`
- Protection: `locked`
- Covers: the endpoint from TESTABLE block
- Status: `pending`

**Step 5: Deduplication**

Before appending any entry, check if a test with the same function name or covering the same endpoint already exists in catalog. Skip duplicates.

**Step 6: Update catalog.md**

Append new entries. Update `last_scanned_commit` to HEAD.

Print:
```
Catalog updated.
  New entries: {N}
  Skipped (duplicate): {N}
  last_scanned_commit → {SHA}
```

---

## Phase 4 — Test Code Generation

**Step 1: Find pending entries**

Read catalog.md. Collect all entries where `Status: pending`.

Sort by priority:
1. `locked` + `backend` first
2. `locked` + `frontend`
3. `regenerable` + `backend`
4. `regenerable` + `frontend`

**Step 2: Read existing test files**

Before generating, read the target test file if it exists. Identify existing function names. Never write a function that already exists.

**Step 3: Generate backend test functions**

For each pending backend entry:

```python
# [Argus] {test_function_name}
# Source: {source}
# Protection: {protection} — {"DO NOT DELETE OR MODIFY" if locked else "auto-generated"}
# Intent: {what this test verifies}
async def {test_function_name}({fixtures}):
    # Arrange
    {setup}

    # Act
    response = await client.{method}("{path}", {params})

    # Assert
    assert response.status_code == {expected_status}
    {additional assertions derived from intent}
```

Use `httpx.AsyncClient` for all requests. Use fixtures from conftest.py.

For SSE endpoints, use `client.stream()`.

For auth-required endpoints, use `auth_headers` fixture.

**Step 4: Generate frontend test functions**

For each pending frontend entry, generate a Playwright test outline:

```python
# [Argus] {test_function_name}
# Source: {source}
# Protection: {protection}
# Intent: {what user flow this verifies}
def {test_function_name}():
    # This test requires: /argus test --frontend
    # Browser steps:
    # 1. {step}
    # 2. {step}
    # Assert: {what to verify in UI}
    pass  # Implemented via Playwright in Phase 6
```

Frontend test functions are stubs — actual execution uses Playwright in Phase 6.

**Step 5: Write files**

Append generated functions to the appropriate test file. Update catalog entries:
- Status: `generated`
- File: `tests/{path}::{function_name}`

---

## Phase 5 — Backend Test Execution

**Step 1: Check server is running**

```bash
curl -s http://localhost:8000/health || curl -s http://localhost:8000/api/health || curl -s http://localhost:8000/docs
```

If no response: ask user to start the backend server.

**Step 2: Determine which tests to run**

- `/argus` or `/argus test --backend` → all backend tests
- `/argus test --diff` → scoped tests only

For `--diff` mode:
```bash
git diff main...HEAD --name-only
```
Match changed files against catalog `Covers` fields. Run only matched tests.

Special case: if any of these files changed, run ALL backend tests:
- `conftest.py`, `database.py`, `config.py`, `dependencies.py`, `main.py`
(These are foundational — changes affect everything)

**Step 3: Run pytest**

```bash
cd {project_root}
python -m pytest tests/backend/ -v --tb=short --no-header 2>&1
```

Or for scoped run:
```bash
python -m pytest {specific test files} -v --tb=short --no-header 2>&1
```

**Step 4: Parse results**

For each test, extract: function name, passed/failed, error message if failed.

Update catalog.md for each test:
- Status: `active ✅` or `failing ❌`
- Last run: today's date + result

**Step 5: For each FAILING test**

Record in report:
```
BUG-{YYYY-MM-DD}-{NNN}
Test: {function_name}
Intent: {from catalog}
Source: {from catalog}
Error: {pytest output}
Covers: {endpoint}
Severity: high (if locked) | medium (if regenerable)
```

Do NOT attempt to fix bugs. Argus reports, does not repair.

---

## Phase 6 — Frontend Browser Test Execution

**Note:** Frontend tests are NEVER run automatically on commit hook. Only on manual `/argus` or `/argus test --frontend`.

**Step 1: Ensure test environment ready**

Argus manages its own dependencies. Check and install if needed:

```bash
cd {project_root}

# Check if pytest-playwright is available
if ! python -c "import pytest_playwright" 2>/dev/null; then
    echo "[Argus] Installing browser testing dependencies..."
    pip install pytest-playwright playwright -q
    playwright install chromium 2>/dev/null || echo "[Argus] Chromium may need manual install: playwright install chromium"
fi
```

**Step 2: Read frontend test stubs**

Read all files in `tests/frontend/`. Collect test functions and their intent comments.

**Step 3: Generate Playwright tests from stubs**

For each frontend test stub, generate a Playwright test if not already generated:

File: `tests/frontend/test_{flow}.py`
```python
"""Frontend browser tests — generated by Argus."""
import pytest


# [Argus] {test_name}
# Source: {source}
# Protection: {protection}
# Intent: {intent}
@pytest.mark.asyncio
async def test_{name}(page):
    """{intent}"""
    # Navigate to app URL (from TEST_APP_URL env, default: http://localhost:3000)
    base_url = os.environ.get("TEST_APP_URL", "http://localhost:3000")
    await page.goto(base_url)

    # Execute steps from intent:
    # {steps extracted from stub comments}

    # Screenshot on completion
    await page.screenshot(path=f".argus/reports/screenshots/{date}/{test_name}.png")
```

**Step 4: Run Playwright tests**

```bash
cd {project_root}
python -m pytest tests/frontend/ -v --browser chromium --headed=false \
    --screenshot=only-on-failure \
    --output=.argus/reports/screenshots/{date}/ 2>&1
```

**Step 5: Record results**

Parse pytest output:
- Pass: catalog.md → Status: `active ✅`, Last run: today passed
- Fail: catalog.md → Status: `failing ❌`, Last run: today failed, screenshot saved to `.argus/reports/screenshots/{date}/{test_name}_fail.png`

---

## Phase 7 — Report Generation

Generate `.argus/reports/{YYYY-MM-DD}.md`:

```markdown
# Argus Report — {YYYY-MM-DD}

## Health Score: {score}/100

| Category | Score | Weight |
|---|---|---|
| Locked tests passing | {X}/100 | 40% |
| Endpoint coverage | {X}/100 | 25% |
| High-risk paths covered | {X}/100 | 20% |
| Test stability (no flaky) | {X}/100 | 15% |

Previous: {prev_score} ({delta:+d})

## Summary
✅ Passed: {N}
❌ Failed: {N}
⚠️  Skipped: {N}
🔒 Locked tests: {N} ({N} passing)

## Failed Tests

{for each failing test:}
### BUG-{YYYY-MM-DD}-{NNN}
- Test: {function_name}
- Intent: {catalog intent}
- Source: {catalog source}
- Covers: {endpoint}
- Severity: {high|medium|low}
- Error:
  ```
  {pytest error output}
  ```

## New Tests Added This Run
{list of new catalog entries}

## Coverage Gaps
{endpoints in routes with no catalog entry}
```

**Health score calculation:**

```
locked_score   = (locked_passing / total_locked) * 100
coverage_score = (endpoints_with_tests / total_endpoints) * 100
highrisk_score = (highrisk_covered / total_highrisk) * 100
stability_score = 100 if no_flaky else max(0, 100 - (flaky_count * 20))

health = (
  locked_score   * 0.40 +
  coverage_score * 0.25 +
  highrisk_score * 0.20 +
  stability_score * 0.15
)
```

High-risk paths are endpoints that:
- Handle authentication
- Handle payments or subscriptions
- Use SSE streaming
- Write to database

**Update baseline.json:**

```json
{
  "runs": [
    {"date": "YYYY-MM-DD", "score": 78, "passed": 12, "failed": 3},
    ...
  ]
}
```

If score dropped vs previous run, print:
> "⚠️ Health score dropped {delta} points. Check failing tests above."

Print ASCII trend (last 5 runs):
```
Score trend (last 5):
  71 ██████████████
  74 ███████████████
  78 ████████████████ ← today
```

---

## Trigger Matrix

| Trigger | Phases | Tests run | Max time |
|---|---|---|---|
| `post-commit` hook | 2 → 3 | Incremental backend only | 30s |
| `/argus` | 3 → 4 → 5 → 6 → 7 | Full catalog | no limit |
| `/argus test --backend` | 5 → 7 | All backend | ~2min |
| `/argus test --frontend` | 6 → 7 | All frontend | ~5min |
| `/argus test --diff` | 5 → 7 | Diff-scoped | ~1min |
| `/argus catalog` | 3 only | None | ~10s |
| `/argus report` | 7 only | None | instant |
| `/argus init` | 1 only | None | ~30s |

---

## Rules

1. **Never delete a `locked` test.** Ever. Even if the endpoint no longer exists — mark it `deprecated` and ask the user.
2. **Never fix bugs.** Argus finds and reports. `/qa` fixes.
3. **Never run frontend tests in the commit hook.** Too slow.
4. **Never overwrite an existing function.** Check before writing.
5. **Amend only before push.** Check remote SHA before any `git commit --amend`.
6. **Catalog is append-only for locked entries.** Regenerable entries can be rewritten.
7. **If server is down, report clearly and stop.** Do not fail silently.
