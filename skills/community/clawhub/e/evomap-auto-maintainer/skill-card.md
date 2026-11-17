## Description:

Automatically maintains EvoMap node online status by checking node health and sending periodic heartbeat signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhanglingai](https://clawhub.ai/user/zhanglingai)

### License/Terms of Use:


## Use Case:

External users and operators use this skill to keep an EvoMap node online by configuring node credentials, checking status, sending heartbeats, and optionally installing recurring maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports an indefinite user-level cron job that runs every 15 minutes and sends authenticated EvoMap heartbeat data.

Mitigation: Run setup only when persistent maintenance is intended, inspect the crontab before and after setup, and document how to remove the entry manually.

Risk: The security evidence warns that EVOMAP_SECRET may be exposed through logs, commits, or shell history.

Mitigation: Keep EVOMAP_SECRET in a protected local environment and avoid pasting, committing, or logging the secret.

Risk: The security summary reports no confirmation, removal controls, or reliable duplicate handling for the cron job.

Mitigation: Confirm the installed cron entry manually and remove duplicate or unwanted entries from the user crontab.

## Reference(s):

- [EvoMap](https://evomap.ai)
- [ClawHub Skill Page](https://clawhub.ai/zhanglingai/skills/evomap-auto-maintainer)
- [Publisher Profile](https://clawhub.ai/user/zhanglingai)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and shell output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces commands for status checks, manual heartbeat requests, and cron-based maintenance setup.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
