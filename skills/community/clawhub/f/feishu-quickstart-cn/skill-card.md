## Description:

飞书快速集成配置 - 5分钟连接 OpenClaw 与飞书，解锁文档管理、知识库、自动化工作流。适合：企业用户、团队协作、飞书生态。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, enterprise users, and collaboration teams use this skill to configure an OpenClaw and Feishu integration for document access, knowledge-base workflows, bitable automation, and optional webhook events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup asks users to grant broad Feishu document, drive, wiki, bitable, and webhook permissions.

Mitigation: Use the narrowest Feishu scopes needed for the intended workflow and avoid write scopes unless they are required.

Risk: The configuration stores Feishu App Secret values in an OpenClaw configuration file.

Mitigation: Store secrets with restricted file permissions or a secrets manager, and keep configuration files out of source control and broad backups.

Risk: Write-capable document, wiki, and bitable automation can affect enterprise content.

Mitigation: Test write-capable workflows in a sandbox tenant or non-production workspace before enabling them in a real Feishu tenant.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/skills/feishu-quickstart-cn)
- [Feishu open platform app console](https://open.feishu.cn/app)
- [Feishu open platform documentation](https://open.feishu.cn/document)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with YAML and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl according to parsed ClawHub metadata.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
