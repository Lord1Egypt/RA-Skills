## Description:

汽服渠道的品牌规模、省市覆盖、服务类型与竞争格局分析。可将高德地图中复制出的地点名称和地址文本作为地点输入；基于店店通已发布门店快照生成可核验结论。本 Skill 非高德地图官方产品，和高德地图不存在合作、授权或数据来源关系。

This skill is ready for commercial/non-commercial use.

## Publisher:

[horacetu](https://clawhub.ai/user/horacetu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market analysts use this skill to analyze automotive aftermarket brand coverage, regional concentration, service categories, nearby stores, and competitive channel patterns from DDT's published store snapshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends a bearer API key to a configurable DDT API base URL.

Mitigation: Install only if the DDT service and runtime environment are trusted, pin DDT_OPEN_BASE to the official endpoint, and avoid exposing real DDT_API_KEY values in chat, logs, or version control.

## Reference(s):

- [DDT Claw homepage](https://gotoshop-ai.com/ddtclaw/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown analysis with concise metrics, coverage notes, and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses DDT_API_KEY authentication and returns only published aggregate or limited public store-point results.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
