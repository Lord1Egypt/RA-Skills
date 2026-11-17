## Description:

Manage Feishu group chats through Feishu server APIs, including create, get details, list members, add members, remove members, and disband chats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wodenwang](https://clawhub.ai/user/wodenwang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Feishu workspace administrators use this skill to manage Feishu group chat lifecycle tasks, including creating chats, retrieving chat details, listing members, adding or removing members, and disbanding chats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform high-impact chat administration actions, including removing members and disbanding chats.

Mitigation: Require explicit user confirmation before member removal or chat disbanding, and verify chat and member identifiers before execution.

Risk: Feishu app credentials may be exposed if supplied directly in command-line arguments.

Mitigation: Use environment variables or a reviewed local config file for credentials, avoid logging secrets, and grant the Feishu app only the scopes needed for the requested chat actions.

Risk: The documented command fetches executable code from a live Git repository.

Mitigation: Prefer a pinned, reviewed release or commit and review the skill before installing or running it.

## Reference(s):

- [Feishu Chat Server API on ClawHub](https://clawhub.ai/wodenwang/skills/feishu-chat-server-api)
- [Project homepage from ClawHub metadata](https://github.com/wodenwang/feishu-extension-skills)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Feishu app credentials and valid chat or member identifiers for applicable actions.]

## Skill Version(s):

0.1.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
