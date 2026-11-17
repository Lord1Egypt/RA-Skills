## Description:

Complete Feishu (Lark) integration toolkit for AI agents to read and write documents, fetch chat history, send files and screenshots, manage permissions, and create scheduled reminders across Wiki, Docs, Sheets, Bitable, and IM operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ye4wzp](https://clawhub.ai/user/ye4wzp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect an AI agent to Feishu or Lark workspaces for document operations, chat review, file delivery, screenshot sharing, permission changes, and scheduled reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access or change sensitive Feishu workspace data, including chat history, documents, files, screenshots, permissions, and scheduled messages.

Mitigation: Review the skill before installing, use a dedicated Feishu app with only the required scopes, and require explicit confirmation before chat-history access, screenshot capture, file upload, permission changes, or scheduled reminders.

Risk: Feishu app secrets and tenant access tokens can grant broad API access if exposed or over-scoped.

Mitigation: Protect and rotate the app secret, store credentials outside shared logs or documents, and grant only the minimum permissions needed for the intended workflow.

Risk: Permission-management and screenshot features can expose private content or alter collaborator access.

Mitigation: Avoid enabling those features unless they are specifically needed, and confirm the target document, recipient, and permission level before taking action.

## Reference(s):

- [Feishu Open Platform](https://open.feishu.cn/app)
- [Feishu API Documentation](https://open.feishu.cn/document)
- [ClawHub Skill Page](https://clawhub.ai/ye4wzp/skills/feishu-toolkit)
- [Publisher Profile](https://clawhub.ai/user/ye4wzp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code blocks, API request examples, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Feishu app credentials and user confirmation for sensitive actions.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
