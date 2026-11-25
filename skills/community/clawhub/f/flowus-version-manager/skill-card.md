## Description:

按需管理 FlowUs 云端文件版本、历史、人工审批及备份恢复。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jichengkai](https://clawhub.ai/user/jichengkai)

### License/Terms of Use:

MIT-0

## Use Case:

个人和团队可使用此技能，在已有 FlowUs 资料库中整理文件版本、查询最新版和历史、检索原文，并在人工确认后执行重要变更及备份恢复。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security inspection was incomplete, and the skill has shell, file, network, and environment capabilities.

Mitigation: Review the connection behavior and authentication settings before installation, and confirm those capabilities fit the intended FlowUs workspace and client.

Risk: FlowUs access depends on credentials and permissions configured by the user.

Mitigation: Use an authorized FlowUs connection, keep tokens out of chat and skill files, and review proposed high-impact changes before confirming them.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/jichengkai/skills/flowus-version-manager)
- [Cloud connection and home organization](references/cloud-connect.md)
- [Setup and capability checks](references/setup.md)
- [Governance, approvals, and recovery](references/governance.md)
- [FlowUs API overview](https://flowus.cn/developer-api/v2/zh/getting-started/overview)
- [FlowUs file upload documentation](https://flowus.cn/developer-api/v2/zh/advanced/file-upload)
- [FlowUs concurrency conventions](https://flowus.cn/developer-api/v2/zh/reference/conventions)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown summaries and guidance, with structured JSON results and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include document version identifiers, source links, review items, and proposed changes.]

## Skill Version(s):

0.4.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
