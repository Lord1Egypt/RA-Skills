## Description:

Provides Feishu/Lark instant messaging CLI guidance for sending, replying to, and searching messages, managing group chats and members, downloading message resources, and managing reactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roy-oss1](https://clawhub.ai/user/roy-oss1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to operate Feishu/Lark IM through lark-cli: identify chats, send or reply to approved messages, inspect or search chat history, download resources, and manage chat metadata or reactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release installs an unpinned executable CLI package.

Mitigation: Install only after trusting the @larksuite/cli npm package and pin or review a specific package version in managed deployments.

Risk: The skill can read or search broad chat history when granted wide Lark scopes.

Mitigation: Use the narrowest Lark scopes possible and search only chats, users, and time ranges that are authorized for the task.

Risk: The skill can send messages or mutate chats, which may affect other users.

Mitigation: Use dry-run before writes and confirm recipient, content, and user-or-bot identity before sending messages or changing chats.

Risk: Lark app credentials and user or tenant tokens may be exposed to the CLI.

Mitigation: Use scoped credentials, avoid unnecessary token exposure, and rotate credentials according to the deployment's normal secret-handling policy.

Risk: Markdown messages with remote images may cause external URLs to be fetched and uploaded by the CLI.

Mitigation: Avoid remote Markdown images unless the URL is trusted and the fetch/upload behavior is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roy-oss1/skills/feishu-lark-cli)
- [Lark CLI GitHub homepage](https://github.com/larksuite/cli)
- [im (v1)](SKILL.md)
- [im +chat-create](references/lark-im-chat-create.md)
- [Group Chat Identity Rules](references/lark-im-chat-identity.md)
- [im +chat-messages-list](references/lark-im-chat-messages-list.md)
- [im +chat-search](references/lark-im-chat-search.md)
- [im +chat-update](references/lark-im-chat-update.md)
- [im +messages-mget](references/lark-im-messages-mget.md)
- [im +messages-reply](references/lark-im-messages-reply.md)
- [im +messages-resources-download](references/lark-im-messages-resources-download.md)
- [im +messages-search](references/lark-im-messages-search.md)
- [im +messages-send](references/lark-im-messages-send.md)
- [im reactions](references/lark-im-reactions.md)
- [im +threads-messages-list](references/lark-im-threads-messages-list.md)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Markdown, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include dry-run commands and output-format flags; command effects depend on the authenticated Lark identity and authorized scopes.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
