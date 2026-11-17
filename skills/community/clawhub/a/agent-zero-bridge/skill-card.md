## Description:

Delegate complex coding, research, or autonomous tasks to Agent Zero framework.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dowingard](https://clawhub.ai/user/dowingard)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to delegate complex coding, research, long-running build, and self-correction tasks to Agent Zero while keeping Clawdbot available for progress updates, user input, and tool calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent Zero may receive broad access through the Clawdbot gateway.

Mitigation: Use a dedicated least-privilege token, restrict which tools Agent Zero can invoke, and install only when this access model is acceptable.

Risk: Gateway exposure and persistent credentials can expand access beyond the intended local bridge.

Mitigation: Avoid binding the gateway to public or LAN interfaces unless protected, and do not copy broad .env files into the Agent Zero container.

Risk: File attachments can disclose unintended local content.

Mitigation: Review every attachment path before sending files to Agent Zero.

## Reference(s):

- [Agent Zero](https://github.com/frdel/agent-zero)
- [Clawdbot](https://github.com/clawdbot/clawdbot)
- [Agent Zero Bridge on ClawHub](https://clawhub.ai/dowingard/skills/agent-zero-bridge)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text, Markdown, JSON command output, and notebook project Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports optional file attachments, conversation context reuse, status/history commands, notifications, and task breakdown files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
