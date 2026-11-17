## Description:

Feishu Messaging.Bak2 helps agents send Feishu messages, find chats and users, retrieve group members, upload message media or files, and use Feishu Open Platform API examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[make453](https://clawhub.ai/user/make453)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and employees use this skill to automate Feishu messaging workflows that require finding chats or users, retrieving group members, and retrying or testing message sends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary says the skill ships apparent Feishu app secrets.

Mitigation: Do not use the bundled credentials; rotate them if they belong to you and supply Feishu credentials through a secure environment or secret manager.

Risk: The helper scripts can send Feishu messages and upload message content or files.

Mitigation: Run the scripts only in authorized workspaces, confirm recipient IDs before sending, and limit Feishu app scopes to the minimum required permissions.

Risk: The user-search script can retrieve and print employee contact details.

Mitigation: Use contact lookup only when authorized to view and log employee details, and avoid storing console output that contains personal data.

## Reference(s):

- [Feishu Open Platform API Documentation](https://open.feishu.cn/document/server-docs/api-call-guide/server-api-list)
- [Feishu Web](https://www.feishu.cn/)
- [ClawHub Skill Page](https://clawhub.ai/make453/skills/feishu-messaging-bak2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code examples and JavaScript helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Feishu API requests that send messages, upload files, or retrieve contact and chat data when scripts are executed with credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
