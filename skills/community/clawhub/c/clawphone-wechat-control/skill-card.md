## Description:

Guides an agent through WeChat conversation navigation, chat entry, message sending, in-app popup handling, and failure checks with step-by-step screen verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[be1human](https://clawhub.ai/user/be1human)

### License/Terms of Use:

MIT-0

## Use Case:

External ClawHub users use this skill to help an agent inspect the current WeChat screen, open the requested chat, enter or paste message text, send only after visible confirmation, and verify the sent message appears.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may view private WeChat messages visible on the active screen.

Mitigation: Use the skill only when you are comfortable exposing the current WeChat screen to the agent, and close or navigate away from unrelated chats before invoking it.

Risk: The agent can send messages in the requested chat when instructed.

Mitigation: Confirm the target contact or thread and the exact message content before asking the agent to send, and rely on the skill's screenshot checks before and after sending.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/be1human/skills/clawphone-wechat-control)
- [Publisher profile](https://clawhub.ai/user/be1human)

## Skill Output:

**Output Type(s):** [guidance, shell commands]

**Output Format:** [Markdown instructions with inline command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires confirming the active WeChat page, target contact, input field, send button, and final message state from current screenshots.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
