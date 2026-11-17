## Description:

把财报或公告中的资产负债表日后事项整理成逐条附原文、定位锚点和来源编号的登记表，不推断事项性质或自行计算金额。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

财务人员和分析师可用它从年报、半年报或公告中逐条登记资产负债表日后事项，并保留原文、定位和来源以便复核。输出是供人工核对的初稿，不用于投资建议或事项性质判断。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this release suspicious and reports credential routing, external document sharing, and a home-directory usage marker; scanning was partial.

Mitigation: Before use, review credential destinations and local file access, confirm external service destinations are approved, and provide only documents authorized for that processing.

## Reference(s):

- [MCP data channel](https://cuecue.cn/hub/mcp)
- [Document and PDF reader](https://cuecue.cn/hub/omni-reader)
- [Live MCP catalog](https://cuecue.cn/api/mcp-catalog)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [七节 Markdown 登记表，逐条附原文、定位锚点与来源编号]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [逐条照录披露内容；缺失信息标为未取到；由人工复核。]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence, SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
