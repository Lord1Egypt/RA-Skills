## Description:

将 Markdown 文件发布为飞书（Feishu/Lark）在线文档，支持常见 Markdown 语法、表格列宽自适应渲染、公开分享和发布后文档所有权移交。

This skill is ready for commercial/non-commercial use.

## Publisher:

[happyphper](https://clawhub.ai/user/happyphper)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content publishers use this skill to publish local Markdown documents into Feishu/Lark DocX with preserved rich text, tables, optional sharing settings, and optional ownership transfer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential loading can read broad environment and configuration files, including workspace .env files.

Mitigation: Prefer explicit FEISHU_APP_ID and FEISHU_APP_SECRET environment variables or a dedicated config file, and avoid running the skill in directories with unrelated .env files.

Risk: Markdown image references may cause unintended local files to be uploaded to Feishu.

Mitigation: Use trusted Markdown inputs only and review or remove local image paths before publishing.

Risk: Public sharing and automatic owner transfer can make published content leave the user's control.

Mitigation: Use public sharing or FEISHU_ADMIN owner transfer only for content intended for that audience, and verify the share and owner settings before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/happyphper/skills/feishu-doc-publisher)
- [Feishu Open API](https://open.feishu.cn/open-apis)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration]

**Output Format:** [Markdown guidance with bash command examples and script status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a Feishu DocX document, upload referenced local images, set sharing permissions, and transfer document ownership when configured.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact changelog tops out at 2.0.0 and SKILL.md frontmatter lists 1.1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
