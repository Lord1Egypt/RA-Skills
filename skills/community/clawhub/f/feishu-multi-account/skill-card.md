## Description:

Provides a guide for configuring independent Feishu bot accounts for OpenClaw sub-agents so messages route to the correct agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhili007](https://clawhub.ai/user/zhili007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure multiple Feishu bot accounts in OpenClaw and bind each account to the intended sub-agent. It is most useful when setting up multi-agent Feishu routing or troubleshooting messages that are routed to the wrong agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real Feishu appSecret values could be exposed if copied into shared repositories, screenshots, or logs.

Mitigation: Keep real secrets out of shared material, redact configuration examples, and rotate any appSecret that is accidentally exposed.

Risk: Incorrect Feishu account bindings can route messages to the wrong OpenClaw sub-agent.

Mitigation: Verify top-level bindings for every Feishu account and test routing logs before relying on the configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhili007/skills/feishu-multi-account)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON configuration examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup steps, validation commands, troubleshooting notes, and an example openclaw.json configuration.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact config.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
