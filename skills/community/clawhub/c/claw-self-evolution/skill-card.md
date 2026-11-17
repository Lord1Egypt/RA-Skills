## Description:

Provides OpenClaw maintenance automation for self-checks, architecture scans, introspection reports, isolated experiments, profile updates, service health checks, backups, log cleanup, and directory validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenz1117](https://clawhub.ai/user/kenz1117)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and workspace maintainers use this skill to install scheduled maintenance scripts that produce operational reports and support controlled workspace self-maintenance. It is intended for agents that manage learning logs, experiments, backups, service health checks, and directory hygiene inside an OpenClaw workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled scripts have high-impact authority over persistent memory, workspace files, logs, backups, caches, and service restarts.

Mitigation: Install only in a controlled OpenClaw workspace and disable or narrow scheduled jobs that are not explicitly needed.

Risk: The auto-profile workflow can rewrite persistent user profile memory.

Mitigation: Review profile updates before relying on them and disable the profile updater when persistent preference changes require manual approval.

Risk: Experiment merge, cleanup, backup/cache, and service restart behavior can affect production workspace state.

Mitigation: Require explicit operator review for experiment merges, cleanup actions, service restarts, and backup/cache changes before enabling unattended schedules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kenz1117/skills/claw-self-evolution)
- [Publisher profile](https://clawhub.ai/user/kenz1117)
- [self-improving-agent inspiration](https://github.com/pskoett/self-improving-agent)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown reports, shell commands, Python scripts, and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scheduled scripts can write reports, backups, caches, logs, and workspace maintenance files under an OpenClaw working directory.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
