## Description:

餐饮拓店机会区域、候选地址竞争与现场验证优先级分析。 可将百度地图中复制出的地点名称和地址文本作为地点输入；基于店店通已发布门店快照生成可核验结论。本 Skill 非百度地图官方产品，和百度地图不存在合作、授权或数据来源关系。

This skill is ready for commercial/non-commercial use.

## Publisher:

[horacetu](https://clawhub.ai/user/horacetu)

### License/Terms of Use:

MIT-0

## Use Case:

Restaurant expansion, sales, and site-selection teams use this skill to analyze published DDT store snapshots for brand expansion areas, candidate-site competition, risks, gaps, and field-validation priorities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Restaurant brand, city, district, address, and candidate-site queries may be sent to the DDT/Gotoshop API.

Mitigation: Use the skill only with data appropriate for the DDT/Gotoshop service and keep the API key in a local environment variable.

Risk: Bulk extraction or overbroad location queries could exceed the skill's intended preview behavior.

Mitigation: Keep requests within the documented preview limits, avoid automatic pagination or area enumeration, and narrow queries when responses are truncated.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/horacetu/skills/ddt-baidu-map-restaurant-expansion)
- [DDT Claw homepage](https://gotoshop-ai.com/ddtclaw/)
- [DDT API key setup](https://gotoshop-ai.com/ddtclaw/open)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs prioritize conclusions, key metrics, coverage period and methodology notes, requested limited details, and uncovered items.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
