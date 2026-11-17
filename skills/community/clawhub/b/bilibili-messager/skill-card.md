## Description:

Sends Bilibili DMs, replies to messages, and reads chat history through a logged-in browser session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moroiser](https://clawhub.ai/user/moroiser)

### License/Terms of Use:

MIT-0

## Use Case:

External users who manage Bilibili conversations use this skill to read selected private-message history and draft, send, or reply to DMs after explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may read selected Bilibili private-message content into its context.

Mitigation: Only read conversations the user is willing to share, avoid highly sensitive or non-consensual private messages, and use a dedicated openclaw browser profile.

Risk: The skill can send DMs from the logged-in Bilibili account.

Mitigation: Confirm the logged-in account, recipient, message body, and message length before sending or replying; require explicit user confirmation.

Risk: A shared browser profile could expose the wrong account or unrelated browsing context.

Mitigation: Use a dedicated openclaw browser profile and clear the Bilibili login state when the skill is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/moroiser/skills/bilibili-messager)
- [Publisher profile](https://clawhub.ai/user/moroiser)
- [Bilibili private messages](https://message.bilibili.com/#/whisper)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code]

**Output Format:** [Markdown guidance with browser tool commands and JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a logged-in openclaw browser profile; outgoing messages require explicit recipient and message confirmation.]

## Skill Version(s):

1.4.8 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
