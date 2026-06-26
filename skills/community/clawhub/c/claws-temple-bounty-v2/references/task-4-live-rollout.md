# Task 4 Live Rollout Runbook

Use this file for maintainer-facing rollout and incident handling for the external Task 4 live skill.

## Goal

Keep Task 4 clearly available or unavailable as a native SHIT Skills flow, without falling back to a local prep-only success path.

## Rollout Modes

- `test rollout`
  - run `scripts/test-rollout-gate.sh`
  - local dependencies must pass
  - remote Task 4 probe must pass
  - authenticated native publish must be available
  - if either prerequisite is missing, Task 4 is unavailable for that window
  - Tasks 1, 2, 3, and 5 may continue normally
- `production rollout`
  - run `scripts/release-gate.sh`
  - local dependencies must pass
  - remote Task 4 probe must pass
  - authenticated native publish must be available
  - only then treat Task 4 as available

## Preflight Checklist

Before announcing a live Task 4 window:

1. run `python3 scripts/validate_skill_repo.py`
2. run `bash scripts/smoke-check.sh`
3. run `bash scripts/task4-live-skill-probe.sh`
4. confirm the current host supports live remote skill loading
5. confirm the current host has authenticated native publishing available

## Availability Matrix

- remote probe fails
  - status: `unavailable`
  - action: close the current Task 4 window
  - user promise: explain the blocker and send the support CTA
- remote probe passes but auth publish is unavailable
  - status: `blocked`
  - action: stop the current Task 4 attempt
  - user promise: explain the missing prerequisite plainly and send the support CTA
- native action succeeds
  - status: `native action complete`
  - action: report the completed SHIT Skills action without claiming local bounty-state completion

## Test Window Guidance

For a testing window, publish this rule to maintainers:

- Task 4 must be treated as unavailable when the remote probe or authenticated publish path fails
- do not simulate a prep-only success path
- Tasks 1, 2, 3, and 5 may continue testing even while Task 4 is unavailable

## Incident Handling

If the remote live skill becomes unstable during testing:

1. rerun `scripts/task4-live-skill-probe.sh`
2. if it still fails, keep the current Task 4 window closed
3. tell testers that Task 4 is unavailable until the native flow is healthy again
4. rerun the probe before reopening Task 4
