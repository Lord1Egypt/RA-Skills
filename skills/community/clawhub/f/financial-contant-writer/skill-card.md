## Description:

财税审计内容生成器，帮助用户生成适配微信公众号的财税、审计和政策解读文章、标题、大纲与配图建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengbabao0929](https://clawhub.ai/user/fengbabao0929)

### License/Terms of Use:


## Use Case:

External creators, finance and tax professionals, and operators use this skill to draft WeChat-ready finance, tax, audit, policy, risk, guide, tutorial, and industry-insight content. The package also includes configuration guidance for Coze bots and separate financial valuation workflows that should be reviewed before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes financial valuation and investment-recommendation workflows beyond the declared article-writing helper.

Mitigation: Review and scope those workflows before enabling them, especially where outputs could be treated as financial advice.

Risk: The package may collect or process company financial data, tax data, audit data, workbooks, or uploaded files.

Mitigation: Avoid confidential client, tax, audit, or financial workbooks until third-party search, API, document-conversion, and storage behavior has been reviewed.

Risk: The image helper contains an embedded Unsplash API key and downloads images from external services.

Mitigation: Remove or rotate the embedded key and review outbound image download behavior before publishing or running the image feature.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fengbabao0929/skills/financial-contant-writer)
- [Coze Platform](https://www.coze.cn/)
- [Skill Definition](artifact/SKILL.md)
- [Finance Content Command Configuration](artifact/finance-content-skill.json)
- [WeChat Finance Writer Coze Guide](artifact/wechat-finance-writer-coze.md)
- [Financial Valuation Coze Guide](artifact/finance-valuation-coze-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown articles, outlines, title lists, command output, JSON command configuration, and platform setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated content may be saved to local files by commands that use save or output options.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
