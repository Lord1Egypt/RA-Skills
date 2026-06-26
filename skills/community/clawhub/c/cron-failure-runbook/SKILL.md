---
name: cron-failure-runbook
version: 1.0.0
description: "Runbook for diagnosing failed cron jobs, LaunchAgents, heartbeats, and unattended automation by reproducing the scheduler context, preflighting dependencies, and closing with verified evidence."
author: nissan
tags:
  - cron
  - operations
  - runbook
  - automation
metadata:
  openclaw:
    emoji: "⏱️"
    network:
      outbound: false
---

# Cron Failure Runbook

Use when a scheduled job, LaunchAgent, cron task, heartbeat step, or nightly automation fails, silently no-ops, produces incomplete output, or repeatedly generates dream-cycle failure proposals.

## Goal

Turn unattended failures into reproducible evidence and one of three outcomes:

1. Fixed and verified.
2. Deferred with owner/date/reason.
3. Escalated with the exact missing credential, approval, service, or runtime condition.

## Procedure

1. Identify the scheduler context.
   - Job name, plist/cron entry, command, cwd, shell, user, and expected environment.
   - Last successful run and last failed/no-op run.

2. Reproduce in the same runtime lane.
   - Run the exact command manually with the same env source where practical.
   - Capture stdout, stderr, exit code, cwd, PATH, and relevant env variable presence without printing secret values.
   - If the job depends on OpenClaw model calls, verify it uses gateway/Codex routing rather than raw OPENAI_API_KEY.

3. Run preflights before the expensive or external step.
   - Auth: prove the running process can read the needed secret and make the smallest live API call.
   - Files: prove input paths exist and output directories are writable.
   - Network/service: prove target health endpoint or API is reachable.
   - Approval: prove an external write has approval or a preapproved workflow flag.

4. Classify the failure.
   - auth: missing/expired token, wrong vault, wrong runtime env, insufficient scope.
   - runtime: wrong shell, PATH, Python/Node version, cwd, launchd env, permissions.
   - input: missing/stale source files, empty queue, unexpected schema.
   - external: API outage, 401/403, rate limit, deploy provider issue.
   - logic: script exits zero but produces no expected artifact/action.

5. Close the loop.
   - Fix code/config if local and reversible.
   - Add a dry-run or preflight mode if the job cannot be safely tested live.
   - Update the relevant STATUS/runbook/memory with evidence.
   - If unresolved, record blocker, owner, next command, and alert threshold.

## Verification Evidence

Every cron fix needs at least one of:

- Manual reproduction command with exit code and expected output.
- preflight-only or dry-run output proving dependencies are healthy.
- Scheduler log excerpt showing the next run succeeded.
- A deliberate deferred/blocked entry with owner, reason, and next check date.

## Dream-Cycle Specific Checks

For dream-cycle failures:

- bash -n scripts/dream-cycle.sh
- python3 -m py_compile for every Python script touched by the cycle.
- scripts/task-quality-judge.py --since 7 --dry-run
- scripts/skill-evolver.py --since 7 --min-failures 2 --dry-run
- scripts/dream-recurring-issues.py --since 7 --min-count 3 --dry-run
- scripts/dream-cycle-action-summary.py --since-hours 26 --dry-run

Do not mark dream-cycle work complete if proposal files are merely pending. There must be a lifecycle status, a summary, and a next action.
