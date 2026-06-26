# CPR — Rollback & Removal Guide

If CPR changes your agent's behavior in a way you don't want, this guide gets you back to baseline. No tools required — everything is text you can add or remove.

---

## Step 0: Back Up Before You Install (Do This First)

Before pasting anything from CPR into your agent:

1. **Copy your current system prompt** to a text file. Name it something like `system-prompt-backup-YYYY-MM-DD.txt`.
2. **Save it somewhere you'll find it** — desktop, notes app, wherever.

That's your restore point. If anything goes wrong, paste it back in and you're done.

---

## What CPR Adds (Complete List)

### CPR Lite
- One text block in your system prompt (6 pattern descriptions)
- Nothing else. No files. No monitoring.

### CPR Core
- One text block in your system prompt (6 patterns + pre-send gate checklist)
- Nothing else. No files. No monitoring.

### CPR Extended (Full Install)
- Text blocks in your system prompt (Core + drift monitor instructions)
- **One file:** `DRIFT_MONITOR_STATE.json` in your agent's workspace directory
- Nothing else.

**That's the complete list.** CPR does not install software, does not add dependencies, does not create accounts, does not touch anything outside your system prompt and that one optional file.

---

## Rollback Options

### Option A: Remove Everything (Full Uninstall)

1. Open your system prompt
2. Delete the CPR block (everything between `## Conversational Baseline (CPR` and the end of the checklist)
3. Paste back your backup from Step 0
4. If you used Extended: delete `DRIFT_MONITOR_STATE.json` from your workspace

Done. Agent is back to factory behavior.

---

### Option B: Downgrade from Extended → Core

Remove from your system prompt:
- The drift monitor instructions (the `## Drift Monitor` or `## CPR Extended` section)
- Any reference to `DRIFT_MONITOR_STATE.json`

Delete `DRIFT_MONITOR_STATE.json` from your workspace.

Core pre-send gate stays. Monitoring is gone.

---

### Option C: Downgrade from Core → Lite

Remove from your system prompt:
- The pre-send gate checklist (the numbered list of drift markers to delete)

Keep only the 6 pattern descriptions.

Agent will maintain personality patterns but won't actively audit responses.

---

### Option D: Emergency Kill Switch

If something is very wrong and you just want it gone fast:

**Delete your entire system prompt and start fresh.**

This is nuclear but it works in under 30 seconds. Paste your backup from Step 0 to restore, or start from a blank slate.

---

## Signs You Should Roll Back

- Agent is deleting content it shouldn't (over-applying the pre-send gate)
- Agent feels flat or mechanical after CPR (paradoxically — means the baseline wasn't calibrated right)
- Agent is over-correcting in the wrong direction (wrong personality archetype selected)
- `DRIFT_MONITOR_STATE.json` is growing unexpectedly or contains content you don't recognize

---

## Re-Installing After Rollback

If you roll back and want to try again:

1. Start with **CPR Lite only** (see `QUICKSTART_TIERED.md`)
2. Run it for a few days
3. Only add Core or Extended if you're hitting a problem Lite doesn't solve

The most common mistake is installing the full framework before you need it.

---

## Getting Help

If rollback doesn't resolve the issue, the fastest path to diagnosis:

1. Note exactly what behavior changed
2. Check `DRIFT_PREVENTION.md` — does the pre-send gate explain the behavior?
3. Check `DRIFT_MONITOR_STATE.json` — what score and markers are logged?
4. If neither explains it, the issue is likely in your baseline definition (`BASELINE_TEMPLATE.md`) — the wrong personality archetype produces the wrong corrections

Most "CPR is behaving wrong" issues are baseline calibration problems, not CPR bugs.
