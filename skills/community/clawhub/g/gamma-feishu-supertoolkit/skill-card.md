## Description:

Feishu SuperToolkit helps agents send Feishu messages and files, including audio cards, and automate calendar, approval, Bitable, contacts, and attendance workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ayden76](https://clawhub.ai/user/ayden76)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Feishu workspace operators use this skill to let an agent send files and text, create or manage calendar events and approvals, work with Bitable records, query contacts, and retrieve attendance information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes a real-looking Feishu app secret in its setup documentation.

Mitigation: Rotate or prove inactive the published secret, replace it with placeholders, and require credentials to come only from a protected runtime environment.

Risk: The skill can perform powerful Feishu actions, including approvals, calendar deletion, table writes, and local file sending.

Mitigation: Add authentication and authorization to every route, limit app scopes and recipients, restrict file sending to an approved upload flow or safe directory, and require explicit confirmation for destructive or sensitive actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ayden76/skills/gamma-feishu-supertoolkit)
- [File sending reference](references/file-sender.md)
- [Feishu Open Platform](https://open.feishu.cn/)
- [Feishu developer documentation](https://open.feishu.cn/document/)
- [Feishu API Explorer](https://open.feishu.cn/api-explorer)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, json]

**Output Format:** [Markdown guidance with shell commands and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger Feishu API actions and local file upload workflows when configured with tenant credentials.]

## Skill Version(s):

1.0.0 (source: frontmatter, pyproject.toml, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
