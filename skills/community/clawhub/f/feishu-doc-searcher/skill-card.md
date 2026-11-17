## Description:

通用飞书文档搜索助手，根据配置的文档根目录和触发条件，在指定飞书文档空间及其子目录中搜索信息并回答用户问题。

This skill is ready for commercial/non-commercial use.

## Publisher:

[carolyn0719](https://clawhub.ai/user/carolyn0719)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and teams use this skill to configure a Feishu document space and answer questions from that space with source links. It is intended for document search, knowledge lookup, and operational or technical process questions covered by the configured Feishu workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package exposes Feishu app credentials.

Mitigation: Revoke or rotate the exposed secret, remove credentials from the package, and require users to provide credentials through a secure runtime configuration path.

Risk: The skill can automatically forward user questions to another bot.

Mitigation: Require explicit user confirmation before forwarding and make the forwarding target and message visible to the user.

Risk: Configuration output may expose internal Feishu URLs or IDs.

Mitigation: Redact internal URLs, node tokens, user IDs, and bot IDs when displaying configuration or logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/carolyn0719/skills/feishu-doc-searcher)
- [Feishu Open Platform documentation](https://open.feishu.cn/document/)
- [Feishu Docs API overview](https://open.feishu.cn/document/ukTMukTMukTM/uUDN04SN0QjL1QDN/docs-overview)
- [Feishu Wiki API overview](https://open.feishu.cn/document/ukTMukTMukTM/uUDN04SN0QjL1QDN/wiki-overview)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown answers with cited Feishu document links and configuration prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include user-facing setup prompts, not-found responses, and forwarded-question notices.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
