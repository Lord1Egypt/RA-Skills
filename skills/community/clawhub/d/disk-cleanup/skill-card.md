## Description:

Automated disk space cleanup and maintenance for OpenClaw deployments that removes stale SQLite, Docker, log, cache, workspace, delivery queue, journal, git, and migration artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yagebin79386](https://clawhub.ai/user/yagebin79386)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators responsible for OpenClaw deployments use this skill to preview and run storage maintenance when disk usage is high, after long-running deployments, or as scheduled cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live execution has broad destructive authority over logs, caches, Docker artifacts, workspace backups, delivery queue entries, and stale files.

Mitigation: Run with --dry-run first, review the reported targets and environment paths, and execute live cleanup only after confirming the deletion scope.

Risk: Host-level log cleanup can reduce retained system and security logs and can install a persistent journald size limit.

Mitigation: Avoid running as root unless host-wide log retention changes are accepted, and review the script before using unattended cron.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yagebin79386/skills/disk-cleanup)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and a pipe-delimited cleanup summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script supports dry-run, aggressive, and quiet modes; its final line reports CLEAN or CLEANED status.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
