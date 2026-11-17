## Description:

餐饮品牌开关店、区域扩张、竞对密度与候选点机会分析，可将高德地图中复制出的地点名称和地址文本作为地点输入，并基于店店通已发布门店快照生成可核验结论。

This skill is ready for commercial/non-commercial use.

## Publisher:

[horacetu](https://clawhub.ai/user/horacetu)

### License/Terms of Use:

MIT-0

## Use Case:

External business analysts, restaurant operators, and agents use this skill to analyze published restaurant brand snapshots for store openings and closures, regional expansion, competitor density, and candidate site opportunities from Amap-style address text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API key or endpoint misuse could send credentials or queries to an unintended service URL.

Mitigation: Create a low-privilege API key when possible, confirm DDT_OPEN_BASE is exactly the intended HTTPS service URL, and keep DDT_API_KEY local.

Risk: Business conclusions can be misleading if generated from incomplete coverage, truncated previews, unsupported brand capabilities, or model memory instead of published snapshots.

Mitigation: Check response status, coverage period, capabilities, and truncation markers; narrow queries when required and stop rather than filling gaps from webpages or model knowledge.

## Reference(s):

- [店店通 ClawHub homepage](https://gotoshop-ai.com/ddtclaw/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown analysis with concise conclusions, key metrics, coverage notes, limited requested details, and unsupported-item notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses published restaurant store snapshots and limited API previews; should not expose API keys, internal IDs, version UUIDs, table names, suppliers, or English enum values.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
