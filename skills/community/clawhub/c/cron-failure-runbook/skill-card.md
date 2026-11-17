## Description:

Runbook for diagnosing failed cron jobs, LaunchAgents, heartbeats, and unattended automation by reproducing the scheduler context, preflighting dependencies, and closing with verified evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to diagnose failed scheduled jobs, reproduce scheduler context, preflight dependencies, classify failures, and close incidents with evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Troubleshooting may expose secrets while checking scheduler environment or authentication state.

Mitigation: Verify secret presence and access without printing secret values.

Risk: Manual reproduction or fixes could change scheduled automation behavior.

Mitigation: Run the exact command in the scheduler context where practical, keep fixes local and reversible, and close with manual, dry-run, scheduler-log, or deferred evidence.

Risk: Health checks or API probes may touch live external services.

Mitigation: Use the smallest live API call or health endpoint needed to prove reachability and authorization.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nissan/skills/cron-failure-runbook)
- [Publisher profile](https://clawhub.ai/user/nissan)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown runbook guidance with inline shell commands and verification evidence]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No bundled code; guidance may lead the agent to run diagnostics, inspect scheduler configuration, perform small health checks, or apply reversible local fixes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
