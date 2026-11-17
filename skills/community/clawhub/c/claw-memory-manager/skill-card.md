## Description:

Manage OpenClaw Agent's built-in memory features: Dreaming memory consolidation and Active Memory injection, with safe configuration updates, dry-run previews, backups, and optional gateway restarts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songhonglei](https://clawhub.ai/user/songhonglei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to inspect, enable, disable, and tune OpenClaw memory features without manually editing nested configuration files. It is intended for environments where changing persistent memory configuration and restarting the OpenClaw gateway are acceptable operational actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change persistent OpenClaw memory configuration and restart the OpenClaw gateway.

Mitigation: Use --dry-run before applying changes, and use --no-restart when automatic restarts are not appropriate for the environment.

Risk: Active Memory and Dreaming may expose or promote sensitive memory content.

Mitigation: Review and limit sensitive memories before enabling these features, and apply the conservative Active Memory preset when minimizing context injection is important.

Risk: Managed-environment mirror writes can overwrite shared configuration files.

Mitigation: Run with appropriate file permissions, avoid elevated privileges when possible, and review writable mirror directories before applying changes.

## Reference(s):

- [Feature Catalog](references/features.md)
- [OpenClaw Docs](https://docs.openclaw.ai)
- [ClawHub Skill Page](https://clawhub.ai/songhonglei/skills/claw-memory-manager)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Text]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands that modify OpenClaw configuration files, create backups, synchronize managed-environment mirrors, and restart the OpenClaw gateway.]

## Skill Version(s):

1.1.1 (source: server release metadata and artifact changelog, released 2026-07-17)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
