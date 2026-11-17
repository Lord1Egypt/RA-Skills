---
name: "agent-shell-concurrency-safety"
description: "Fix/avoid background-job races, subshell cwd scoping bugs, and state-restore-after-mutation bugs in agent shell automation"
---

# Agent Shell Concurrency & State-Restore Safety

Use when writing bash that backgrounds multiple jobs with a shared delay, or
code that mutates device/API state and must restore it afterward. These two
failure classes are easy to write wrong, pass a quick look, and fail silently
or partially in production.

## 1. Delayed parallel jobs: subshell scoping

**Trigger**: need two or more commands to fire together after a shared
`sleep`/delay, or any `cd` + command combo that must be backgrounded.

**Broken pattern** (fails silently/partially):
```bash
sleep X && cd dir && cmd1 &
cmd2 &
wait
```
Only `cmd1` is chained to the `sleep`/`cd` — bash backgrounds the *whole*
`sleep X && cd dir && cmd1` as one job. `cmd2` runs immediately, in the
original cwd, not the intended one. With two long-running commands meant to
be synchronized, this produces one on-time job and one broken/early job —
exactly the kind of bug that looks fine in isolation (test `cmd1` alone — ok;
test `cmd2` alone — ok) but breaks the moment you need them synchronized.

**Fix**: give every backgrounded job its own subshell, with the delay and any
`cd` *inside* that subshell:
```bash
( sleep X; cd dir; cmd1 ) &
( sleep X; cd dir; cmd2 ) &
wait
```
Verify: both jobs must start work at the same wall-clock offset, and neither
job's output should show the wrong cwd or an early timestamp. Run the command
with `date` printed before/after each job in a single test invocation to
confirm timing before declaring it correct — a single plain-English read of
the one-liner is not enough, bash job-control scoping bugs read as correct.

## 2. Restore-after-mutation: don't restore keys that are invalid together

**Trigger**: code that reads current device/resource state, mutates it
temporarily (flash, blink, test), then restores the original state from the
saved snapshot.

**Broken pattern**: blindly restoring every key that was present in the
snapshot:
```python
restore = {"state": was_on}
for key in ("dimming", "temp", "sceneId", "r", "g", "b"):
    if key in before:
        restore[key] = before[key]
set_pilot(ip, restore)
```
If the API rejects certain key *combinations* as invalid (e.g. `sceneId: 0`
sent alongside `temp`/`r,g,b` — "no scene" plus a direct color command), the
call fails with a generic invalid-params error. That generic error is easy to
misclassify as a permissions/lock issue (it looks identical to one), wasting
debugging time on the wrong hypothesis and leaving the resource stuck in the
wrong state after every call that exercises this path — not just the new
code path you were testing.

**Fix**: when restoring, skip snapshot keys whose *value* signals "not
applicable" rather than restoring every key that happened to be present:
```python
for key in ("dimming", "temp", "sceneId", "r", "g", "b"):
    if key == "sceneId" and before.get(key) == 0:
        continue
    if key in before:
        restore[key] = before[key]
```
Verify: after the mutate+restore cycle, re-fetch state and diff it against
the pre-call snapshot — don't just check for the absence of an error. A
generic invalid-params/permission-looking error on a restore call is a signal
to check for conflicting key combinations in the payload before assuming a
security/lock issue.

## Checklist before shipping either pattern

- Backgrounded jobs sharing a delay: each one is its own `( ... ) &` subshell
  with the delay and any `cd` inside it. Tested by running the real
  multi-job command once, not just each command alone.
- Mutate-then-restore code: re-fetch and diff state after restore, not just
  check for no error. Any "invalid params" error on a multi-key write is
  checked for conflicting keys before assuming a lock/permission cause.
