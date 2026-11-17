## Description:

Safely install, uninstall, reinstall, or upgrade the Bamdra OpenClaw memory suite when stale config, existing plugin directories, or partial installs break normal `openclaw plugins install` flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bamdra](https://clawhub.ai/user/bamdra)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to safely install, repair, upgrade, or uninstall the Bamdra memory suite when normal plugin installation is blocked by stale configuration, existing plugin directories, or partial installs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change OpenClaw plugin configuration and move existing Bamdra plugin or skill directories.

Mitigation: Install only when that lifecycle operation is intended, and review the backup path printed by the script after execution.

Risk: Custom `--package` or `--openclaw-home` values control which package is installed and which OpenClaw home is modified.

Mitigation: Confirm those flag values before execution, especially when targeting a non-default OpenClaw home or a specific package version.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes backup-location reporting and restart guidance after install or upgrade operations.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
