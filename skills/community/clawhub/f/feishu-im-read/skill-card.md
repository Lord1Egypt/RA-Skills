## Description:

Guides an agent through reading Feishu IM conversation history, thread replies, cross-chat message search, and message attachment downloads within the user's existing access permissions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a3152557994-ship-it](https://clawhub.ai/user/a3152557994-ship-it)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and authorized operators use this skill to retrieve Feishu chat history, inspect thread context, search across messages, and fetch message resources for conversations they can already access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive Feishu chat content and attachments.

Mitigation: Use the narrowest practical chat, keyword, sender, and time filters, and only expand threads or download files when needed.

Risk: Broad searches or unnecessary resource downloads can expose more conversation data than the task requires.

Mitigation: Keep retrieval scoped to the user's stated purpose and existing Feishu permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/a3152557994-ship-it/skills/feishu-im-read)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Text]

**Output Format:** [Markdown guidance with JSON tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May lead the agent to request Feishu messages, thread replies, search results, or resources according to user-provided filters and access permissions.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
