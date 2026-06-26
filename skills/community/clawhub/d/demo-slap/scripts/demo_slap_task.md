# demo-slap task workflow

Recommended OpenClaw runtime pattern:

- do not manage the watchdog through shell cron commands
- prefer OpenClaw's built-in cron tool when a deployment chooses to enable or disable a watchdog for a live run
- treat watchdog configuration and any job id as deployment-specific, not globally hardcoded
- when used, `DEMO_SLAP_WATCHDOG_JOB_ID` should be supplied by the deployment rather than embedded in the skill
- use the shell helper only for local inspection of state/log/job references:

```bash
scripts/demo_slap_watchdog.sh status
scripts/demo_slap_watchdog.sh tail
scripts/demo_slap_watchdog.sh job
```

Suggested runtime workflow for assistants:
1. Before analyze/render -> `cron.update(jobId=<watchdog>, enabled=true)` when a deployment watchdog is being used
2. Start analyze/render
3. Let the watchdog inspect state on a reasonable interval such as every 2 minutes
4. After successful delivery or terminal error -> `cron.update(jobId=<watchdog>, enabled=false)` when the deployment watchdog was enabled for that run
