## Description:

Configures and maintains recurring, real-execution automation for the crypto-hedge-backtest project using cron-driven progress, health checks, and status reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evanfirefly](https://clawhub.ai/user/evanfirefly)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to set up recurring project automation that runs real tasks, verifies cron execution, monitors progress, and reports only substantive stage results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended cron automation may continue running scripts or changing project files beyond the intended window.

Mitigation: Confirm schedules, working directory, permitted actions, expiration or run limits, and exact disable or removal commands before enabling recurring jobs.

Risk: Recurring jobs target the main session and can keep modifying the active project without a clear approval checkpoint.

Mitigation: Use the required forced test run and cron status checks before adding additional jobs, and pause for a decision when blocked or when substantive progress is absent.

Risk: Network-dependent crypto data pulls can fail intermittently and interrupt the automation chain.

Mitigation: Apply retry logic with exponential backoff in the data-fetching layer before continuing scan or progression workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/evanfirefly/skills/crypto-auto-progression)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and cron configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces recurring automation instructions, validation steps, troubleshooting guidance, and concise progress-reporting language.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
