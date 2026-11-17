## Description:

Monitor and auto-fix OpenClaw gateway stability issues on macOS, including launchd throttling, plugin restart loops, hung shutdowns, and power management interference.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimmyclanker](https://clawhub.ai/user/jimmyclanker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to diagnose OpenClaw gateway downtime on macOS and apply stability fixes for launchd throttling, restart loops, hung shutdowns, and Power Nap interference.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The patcher installs a persistent macOS LaunchAgent that watches and modifies the OpenClaw gateway plist.

Mitigation: Review the patcher before installing, back up the affected plist, and document how to unload and remove the LaunchAgent.

Risk: The Power Nap recommendation changes a system-wide macOS power management setting.

Mitigation: Record current pmset values before applying the change and confirm the operational impact is acceptable.

Risk: The skill's security verdict is suspicious because rollback and scoping safeguards are limited.

Mitigation: Run diagnostic-only checks first, review proposed changes manually, and apply persistent or system-level fixes only after approval.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jimmyclanker/skills/gateway-health-monitor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes diagnostic output, launchd plist guidance, OpenClaw configuration changes, and monitoring recommendations.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
