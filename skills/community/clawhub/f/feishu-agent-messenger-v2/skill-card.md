## Description:

Send private or group Feishu messages through the current agent's Feishu app credentials while handling app-isolated open_id values.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pikaqiuyaya](https://clawhub.ai/user/pikaqiuyaya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let agents report task status or results to Feishu users or chats without routing messages through another coordinating agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send Feishu messages using local app credentials with weak scoping and validation.

Mitigation: Install only for trusted publishers and intended agent identities, restrict access to ~/.openclaw credential files, and use recipient allowlists or confirmation before routine sends.

Risk: Agents may send sensitive or unintended message content to Feishu recipients.

Mitigation: Avoid sensitive content unless explicitly approved, constrain allowed recipient types, and prefer safe JSON construction for message bodies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pikaqiuyaya/skills/feishu-agent-messenger-v2)
- [Publisher profile](https://clawhub.ai/user/pikaqiuyaya)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and command-line text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local OpenClaw Feishu app credentials and returns Feishu message status or message IDs from the send script.]

## Skill Version(s):

2.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
