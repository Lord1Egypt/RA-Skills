## Description:

Automates Feishu task-message handling with a background listener that starts per-task Node.js processing and sends acknowledgement, progress, completion, and failure feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[carlzhao007](https://clawhub.ai/user/carlzhao007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace automation maintainers can use this skill to route Feishu task messages into automated processing flows with visible status updates. It is intended for Feishu automation workflows, task progress tracking, batch task handling, and scenarios where users need real-time feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authoritative security scan reports that task text can be passed into shell commands.

Mitigation: Do not install in a real Feishu workspace until shell-command construction is replaced with shell-free argument passing and command inputs are strictly validated.

Risk: The security scan reports that raw task content can be retained in logs.

Mitigation: Redact or remove task text from listener and task logs before use with confidential workspace data.

Risk: The security scan recommends limiting when the listener can process messages.

Mitigation: Restrict triggers to explicit authorized invocations and review workspace permissions before enabling the listener.

Risk: The security guidance says the documentation should distinguish implemented features from placeholders.

Mitigation: Review the artifact documentation and clearly mark placeholder Feishu API and business-logic integrations before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/carlzhao007/skills/feishu-process-feedback)
- [Skill documentation](artifact/SKILL.md)
- [README](artifact/README.md)
- [Feishu Open Platform](https://open.feishu.cn/)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with inline shell commands and environment-variable configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Feishu feedback messages, console output, local listener/task logs, and a local listener state file.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
