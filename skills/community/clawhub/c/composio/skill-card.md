## Description:

Composio helps agents discover tools, manage app connections, and execute actions across connected services such as Gmail, Slack, GitHub, Notion, Google Workspace, Microsoft apps, and browser or web-search tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wjayesh](https://clawhub.ai/user/wjayesh)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to connect an AI agent to Composio-supported apps, find the right tool schemas, initiate required account connections, and run schema-compliant tool actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents using this skill may gain broad access to connected accounts and can send, post, edit, delete, upload, or bulk-process data through Composio-connected apps.

Mitigation: Require explicit user approval before any externally visible, destructive, upload, or bulk action, and confirm the active connected account before execution.

Risk: Private emails, documents, messages, credentials, or account data could be sent to workbench, web-search, file-upload, or LLM helpers without enough context.

Mitigation: Share sensitive data only when the destination and task need are clear, and minimize or redact private content before remote processing.

## Reference(s):

- [ClawHub Composio Skill](https://clawhub.ai/wjayesh/skills/composio)
- [Composio Platform](https://platform.composio.dev)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance covers API-key setup, tool search, connection management, schema retrieval, tool execution, and remote processing workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata, released 2026-02-09)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
