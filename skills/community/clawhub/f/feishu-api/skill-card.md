## Description:

飞书开放平台 API helps agents use Feishu Open APIs for OAuth authorization, Bitable batch operations, Drive permission and file management, and batch data processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noir-hedgehog](https://clawhub.ai/user/noir-hedgehog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to plan and produce Feishu Open API requests, helper code, and operational guidance for tasks outside the standard Feishu plugin surface, including OAuth token workflows, bulk Bitable changes, and Drive permission management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Helper code and examples disable TLS certificate verification while handling Feishu credentials and access tokens.

Mitigation: Remove all ssl._create_unverified_context() usage and keep certificate verification enabled for Feishu HTTPS calls.

Risk: The skill can guide batch deletes, file uploads, file moves, and collaborator permission changes.

Mitigation: Require explicit user confirmation before destructive or permission-changing operations and limit requests to trusted Feishu HTTPS endpoints.

Risk: Feishu app secrets, access tokens, and refresh tokens may be exposed through hardcoding, logging, or overly broad scopes.

Mitigation: Read credentials from secured configuration, avoid printing secrets or tokens, and request only the minimum required Feishu API scopes.

## Reference(s):

- [Feishu Open Platform](https://open.feishu.cn/)
- [OAuth 用户授权流程](references/oauth.md)
- [多维表格（Bitable）API](references/bitable.md)
- [云文档（Drive）API](references/drive.md)
- [创建飞书应用](references/app-creation.md)
- [ClawHub skill page](https://clawhub.ai/noir-hedgehog/skills/feishu-api)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, API calls, Configuration]

**Output Format:** [Markdown with inline Python and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review generated Feishu requests before execution, especially token handling, batch deletion, file upload, move, and permission-change operations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
