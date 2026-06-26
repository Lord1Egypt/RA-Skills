---
name: bugfix-without-test
description: A fix is applied without a reproduction test, leaving no proof the bug is fixed and no regression coverage.
emoji: 🧪
metadata:
  clawdis:
    os: [macos, linux, windows]
---

# bugfix-without-test

Fixing a bug without a test means (a) you don't know the fix actually works, and (b) there's nothing to stop the bug from coming back next refactor. A fix without a regression test is provisional at best.

## Symptoms

- Diff contains code changes but no test changes.
- Existing tests still pass, but none of them would have failed under the original bug.
- PR description describes a bug scenario that no test exercises.
- The fix is a one-liner and no one will remember why it exists six months later.

## What to do

- Reproduce the bug as a failing test first. Run it. Confirm it fails for the right reason.
- Apply the fix. Run the test again. Confirm it passes.
- Keep the test in the suite. It becomes the regression guard.
- If the bug is hard to test (timing, environment, flaky), say so explicitly and describe what manual verification was done. Don't silently skip.
- For bugs discovered in production, add the test at the lowest level that reproduces the issue — unit if possible, integration if not.
