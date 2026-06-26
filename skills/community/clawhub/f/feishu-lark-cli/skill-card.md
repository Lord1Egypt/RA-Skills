## Description: <br>
Guides an agent in using lark-cli for Feishu/Lark instant messaging, including sending and replying to messages, searching chat history, managing group chats and members, downloading chat files, and managing message reactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[roy-oss1](https://clawhub.ai/user/roy-oss1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent perform Feishu/Lark messaging workflows through lark-cli. It is suited for chat and message lookup, group management, message sending and replies, attachment download, and reaction management when the appropriate user or bot authorization is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authorized use can read and change real Feishu/Lark chat data. <br>
Mitigation: Install only for workspaces where agent messaging access is intended, and grant the narrowest OAuth scopes needed for the task. <br>
Risk: State-changing actions can send messages, modify groups, add members, or create reactions under the selected user or bot identity. <br>
Mitigation: Confirm recipients, group members, identity, and message content before execution, especially when switching between user and bot identity. <br>
Risk: Broad message searches and downloaded attachments can expose sensitive chat content. <br>
Mitigation: Avoid broad all-chat searches unless necessary, and treat downloaded chat attachments as sensitive untrusted files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/roy-oss1/feishu-lark-cli) <br>
- [lark-cli project homepage](https://github.com/larksuite/cli) <br>
- [im +chat-create](references/lark-im-chat-create.md) <br>
- [Group Chat Identity Rules](references/lark-im-chat-identity.md) <br>
- [im +chat-messages-list](references/lark-im-chat-messages-list.md) <br>
- [im +chat-search](references/lark-im-chat-search.md) <br>
- [im +chat-update](references/lark-im-chat-update.md) <br>
- [im +messages-mget](references/lark-im-messages-mget.md) <br>
- [im +messages-reply](references/lark-im-messages-reply.md) <br>
- [im +messages-resources-download](references/lark-im-messages-resources-download.md) <br>
- [im +messages-search](references/lark-im-messages-search.md) <br>
- [im +messages-send](references/lark-im-messages-send.md) <br>
- [im reactions](references/lark-im-reactions.md) <br>
- [im +threads-messages-list](references/lark-im-threads-messages-list.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with lark-cli shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose state-changing messaging actions and file downloads that require Feishu/Lark OAuth authorization and lark-cli installation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
