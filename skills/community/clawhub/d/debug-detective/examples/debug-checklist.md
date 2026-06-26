# Debugging Workflow Checklist

Step-by-step checklist for systematic bug investigation.

## Phase 1: Reproduce

- [ ] Can you trigger the bug reliably? (Y/N)
- [ ] Minimal steps to reproduce documented?
- [ ] Environment noted? (OS, runtime version, browser, config)
- [ ] Is it deterministic or intermittent?
- [ ] If intermittent: what's the pattern? (load, timing, specific data)

## Phase 2: Gather Information

- [ ] Read the **full** error message and stack trace
- [ ] Check application logs (last 30 minutes)
- [ ] Check monitoring dashboards for anomalies
- [ ] Check recent deployments/changes (`git log --oneline -20`)
- [ ] Check recent config changes
- [ ] Ask: "What changed recently?"

## Phase 3: Isolate

- [ ] Which component is affected? (frontend, backend, database, network, infra)
- [ ] Does it happen in all environments? (local, staging, production)
- [ ] Does it happen for all users or specific ones?
- [ ] Does it happen with all data or specific inputs?
- [ ] Binary search: can you narrow it to a specific module/function?

## Phase 4: Hypothesize

Write down at least 3 possible causes:

1. [ ] Hypothesis: ________________________________
2. [ ] Hypothesis: ________________________________
3. [ ] Hypothesis: ________________________________

For each hypothesis, define a test:
- "If it's [hypothesis], then [this test] should show [this result]"

## Phase 5: Test and Fix

- [ ] Test each hypothesis (30 min timebox per hypothesis)
- [ ] Root cause identified?
- [ ] Fix is minimal and targeted? (don't fix "while you're in there")
- [ ] Fix doesn't introduce new issues? (run full test suite)

## Phase 6: Verify and Prevent

- [ ] Original reproduction steps no longer trigger the bug
- [ ] No regressions in related functionality
- [ ] Added a test that catches this specific bug
- [ ] Updated documentation/runbook if applicable
- [ ] Shared findings with the team (Slack, PR description, post-mortem)

## Quick Reference: Common Bug Categories

| Category | Symptoms | First check |
|----------|----------|-------------|
| **Logic error** | Wrong result, no error | Add logging at decision points |
| **Null/undefined** | TypeError, "cannot read property" | Check data flow, API responses |
| **Race condition** | Intermittent, timing-dependent | Add locks/queuing, check async code |
| **Configuration** | Works locally, fails in staging/prod | Diff environment variables and configs |
| **Dependency** | Broke after update | Check `git diff` on lock files |
| **Memory leak** | Slow degradation over time | Monitor RSS, take heap snapshots |
| **N+1 query** | Slow page load, high DB load | Enable query logging, count queries |
| **Encoding** | Garbled text, broken characters | Check UTF-8 at every boundary |
| **Timezone** | Dates off by hours | Use UTC everywhere, check DB timezone |
| **Permission** | "Access denied", 403 | Check file permissions, IAM roles, CORS |
| **DNS/Network** | "ENOTFOUND", timeouts | `curl -v`, `dig`, check firewall |
| **Disk space** | "ENOSPC", write failures | `df -h`, check log rotation |

## Rubber Duck Protocol

When stuck for more than 30 minutes:

1. Open a blank document
2. Write: "The code should do: ___"
3. Write: "Instead it does: ___"
4. Write: "I've checked: ___"
5. Write: "I haven't checked: ___" ← **Start here**
