# DevOps Leader Runbook

## Continuous Monitoring

1. **CI/CD Health Check** (every hour)
   - `gh run list --repo ORG/REPO --status failure --limit 5`
   - Read logs for each failure
   - If fixable: create branch, apply fix, open PR
   - If infrastructure issue: escalate to human with diagnosis

2. **Infrastructure Health** (every hour)
   - Check disk usage: `df -h`
   - Check memory: `free -m`
   - Check running processes
   - Log anomalies in `ops/incident-log.md`

3. **Dependency Updates** (weekly)
   - Check for outdated packages
   - Create PRs for safe updates
   - Flag breaking changes for human review

## Incident Response

1. **Detect**: Cron check fails, or CEO agent reports anomaly
2. **Diagnose**: Read logs, check system state, identify root cause
3. **Fix or Escalate**:
   - Fixable by code change → open PR
   - Requires CLI (Railway, Vercel, Yutu) → create issue, request human action
   - Transient → log and monitor
4. **Report**: Write summary to CEO Agent in relevant issue

## Safety Rules

- NEVER deploy directly
- NEVER modify production secrets without human approval
- ALWAYS create a PR for infrastructure changes
- ALWAYS log incidents in `ops/incident-log.md`
