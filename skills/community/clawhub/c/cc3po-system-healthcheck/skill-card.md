## Description:

Three-tier system health monitoring (L1/L2/L3) with heartbeat mechanism, zero external dependencies, i18n support, and console output only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[carloscbrls](https://clawhub.ai/user/carloscbrls)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to run local health checks, review system resource and service status, and configure optional recurring monitoring through cron.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional cron entries keep health checks running in the background.

Mitigation: Enable cron only when recurring monitoring is intended, review paths before installation, and remove the entries when uninstalling.

Risk: Cron service commands and uninstall cleanup can affect system settings or local files.

Mitigation: Avoid sudo cron-service commands unless the system-level change is understood, and preview target directories and log files before removal.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/carloscbrls/skills/cc3po-system-healthcheck)
- [Project Homepage](https://github.com/cc3po/system-healthcheck)
- [README.md](artifact/README.md)
- [INSTALL.md](artifact/INSTALL.md)
- [Crontab Example](artifact/templates/crontab_example.txt)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Console text or JSON from health-check scripts, with Markdown usage and configuration guidance in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts report status through exit codes 0 and 1; heartbeat output can be quiet when healthy or outside configured work hours.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata; artifact frontmatter agrees, artifact changelog also contains 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
