## Description:

Deploy the Agent HQ mission-control stack so teams can run a shared board, high-priority watcher, Telegram notifier, and Jarvis summary automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thibautrey](https://clawhub.ai/user/thibautrey)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to install and run the Agent HQ mission-control board, API, alerting, and automation hooks for coordinating agent work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup directs users to install and run external code that is not pinned to a reviewed commit.

Mitigation: Pin the repository to a reviewed commit and use lockfile-based installs before running the service.

Risk: Telegram and API tokens may be exposed if stored in the repository or readable configuration files.

Mitigation: Keep tokens outside the repo where possible and restrict permissions on any local configuration files that contain secrets.

Risk: Recurring cron automation can repeatedly run scripts before their behavior and schedule are reviewed.

Mitigation: Review the exact scripts and schedule before enabling cron jobs.

Risk: Exposing the service broadly can increase access risk for board and API endpoints.

Mitigation: Bind the service to localhost unless intentional external access is required and reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thibautrey/skills/agent-hq)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and curl code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup steps, runtime commands, token handling guidance, and automation notes.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
