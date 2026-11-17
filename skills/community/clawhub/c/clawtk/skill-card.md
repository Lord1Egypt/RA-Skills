## Description:

Automatically reduce OpenClaw API costs by 60-80%. One-command setup: config optimization, spend caps, retry loop protection, and ClawTK Engine compression.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skl3](https://clawhub.ai/user/skl3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to inspect, apply, restore, and monitor cost-saving configuration changes, spend caps, retry-loop protection, and optional ClawTK Pro compression or cloud sync features.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill modifies OpenClaw configuration and installs persistent hooks.

Mitigation: Run setup only after reviewing the planned changes, keep the generated backup path, and use the restore or uninstall command if the optimizations should be removed.

Risk: Pro activation may run a third-party engine installer and configure additional hooks.

Mitigation: Review the tagged installer or use a manual installation path before activating Pro features in sensitive environments.

Risk: The skill stores a license key locally and can cache local tool outputs that may contain sensitive data.

Mitigation: Avoid Pro cache or cloud sync on workspaces with sensitive command output, and remove local ClawTK state, spend logs, and cache files during cleanup.

## Reference(s):

- [ClawTK Homepage](https://clawtk.co)
- [ClawHub Skill Page](https://clawhub.ai/skl3/skills/clawtk)
- [ClawTK Config Patches](references/config-patches.md)
- [ClawTK Savings Guide](references/savings-guide.md)
- [ClawTK Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and command summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local setup, status, restore, override, activation, sync, uninstall, and troubleshooting commands for OpenClaw environments.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
