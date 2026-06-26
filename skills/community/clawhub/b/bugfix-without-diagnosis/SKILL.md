---
name: bugfix-without-diagnosis
description: A fix is proposed without first identifying the root cause; the symptom is masked rather than resolved.
emoji: 🩹
metadata:
  clawdis:
    os: [macos, linux, windows]
---

# bugfix-without-diagnosis

When a fix goes in without understanding why the bug occurred, the symptom disappears but the cause lingers. It will return under a different shape, or the "fix" will mask a more serious problem upstream.

## Symptoms

- Fix adds a null check without explaining why the value was null.
- Retry loop wrapped around a flaky call with no investigation into why it was failing.
- Try/except swallowing a specific exception without stating what conditions produce it.
- Condition tweaked (`>` → `>=`) to make a test pass, with no explanation of the underlying off-by-one.
- PR description says "fix X" with no "because Y".

## What to do

- Before proposing a fix, write one sentence stating the root cause. If you can't, you don't understand the bug well enough to fix it.
- Explain how the symptom follows from the cause — the chain of events from "bad thing happened" to "user saw this".
- Confirm the fix addresses the cause, not just the symptom. A null check is valid only if you know why the value was null and concluded that null is acceptable.
- Where the cause is upstream, fix it upstream. Only patch downstream if upstream is genuinely out of reach, and say so.
- Leave a comment linking the symptom to the cause so future readers don't misread the fix as superficial.
