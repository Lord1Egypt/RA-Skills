## Description:

Read and send Apple Messages (iMessage, SMS) from the command line on macOS. List chats with unread counts, read a conversation, search all messages, and send, with JSON output for agent use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gopaljigaur](https://clawhub.ai/user/gopaljigaur)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents running on macOS use the CLI to review recent chats, retrieve or search selected messages, and prepare or send iMessage or SMS replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reading Apple Messages can expose private conversation content, and sending can contact an unintended recipient.

Mitigation: Grant macOS permissions only when you want this access; narrow reads by chat, date, and limit; review a dry-run and confirm the exact recipient and message before sending.

## Reference(s):

- [Apple Messages CLI on ClawHub](https://clawhub.ai/gopaljigaur/skills/amcli)
- [Publisher profile: gopaljigaur](https://clawhub.ai/user/gopaljigaur)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [JSON records or formatted terminal text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chat and message results can be narrowed by chat, date or time, unread status, and result limit.]

## Skill Version(s):

0.1.2 (source: server-resolved release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
