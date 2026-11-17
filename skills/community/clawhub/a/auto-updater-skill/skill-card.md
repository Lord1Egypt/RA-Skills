## Description:

Automatically scans and silently updates OpenClaw Agent and Skill installations across Windows, macOS, and Linux, including offline upgrades and startup auto-checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aahuaxu](https://clawhub.ai/user/aahuaxu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and system operators use this skill to understand or run an updater workflow for OpenClaw installations, including version checks, offline package handling, and startup-based update checks. Review is important because the release security evidence flags privileged installation and silent persistence behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run privileged installers for an updater that can operate silently at startup.

Mitigation: Install only after independently verifying the publisher, download source, signatures, hashes, and the exact persistence changes made by the installer.

Risk: Persistent auto-update behavior can continue running without regular user interaction.

Mitigation: Prefer a manual or user-level updater unless the installer clearly documents how to remove every service, cron entry, log, and system dependency change.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aahuaxu/skills/auto-updater-skill)
- [Publisher profile](https://clawhub.ai/user/aahuaxu)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and installation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Describes updater behavior, installation steps, command usage, dependencies, logs, and uninstall guidance.]

## Skill Version(s):

1.3.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
