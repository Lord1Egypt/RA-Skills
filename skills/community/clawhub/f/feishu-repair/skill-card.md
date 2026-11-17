## Description:

Feishu Repair diagnoses and repairs OpenClaw Feishu gateway, permission configuration, and message delivery issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amd5](https://clawhub.ai/user/amd5)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to diagnose OpenClaw Feishu connectivity, permission, and message delivery failures and to restore configuration from local OpenClaw configuration or backup files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically change OpenClaw Feishu allowlists and restart the OpenClaw Gateway.

Mitigation: Review planned changes before execution, run during a maintenance window, and keep a known-good OpenClaw configuration backup available for rollback.

Risk: The skill can send verification messages to every configured Feishu group and user after validation.

Mitigation: Confirm the target allowlists before repair and notify affected channels or users before running the skill.

Risk: The security scan notes sensitive values handled through shell-interpolated curl and openclaw commands.

Mitigation: Prefer a revised implementation using native HTTP and process APIs, and avoid running it with untrusted or user-controlled configuration values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/amd5/skills/feishu-repair)
- [ClawHub publisher profile](https://clawhub.ai/user/amd5)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Text or JSON diagnostic and repair report with configuration, restart, verification, and messaging results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May restart the OpenClaw Gateway and send Feishu verification messages after applying repairs.]

## Skill Version(s):

2.0.0 (source: frontmatter, skill.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
