## Description:

零售品牌门店规模、业态结构、区域覆盖与候选点机会分析；可将腾讯地图中复制出的地点名称和地址文本作为地点输入，并基于店店通已发布门店快照生成可核验结论。

This skill is ready for commercial/non-commercial use.

## Publisher:

[horacetu](https://clawhub.ai/user/horacetu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide agents through retail-chain network analysis, including brand coverage, store distribution, category mix, nearby-store previews, and candidate-site screening from published DDT retail snapshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API bearer token could be sent to an arbitrary inherited endpoint if DDT_OPEN_BASE is overridden.

Mitigation: Use only the official HTTPS DDT endpoint, avoid inheriting or overriding DDT_OPEN_BASE unless it is fully trusted, and use a scoped or rotatable API key.

Risk: Submitted coordinates, addresses, or business-planning queries may be sensitive.

Mitigation: Run the skill only in controlled environments and avoid writing sensitive inputs, API keys, or bearer tokens to chats, logs, or version control.

Risk: Nearby-store and site-screening responses are limited previews and may be mistaken for complete market coverage.

Mitigation: Report coverage and data-version notes, mark unavailable data clearly, and do not treat missing values as zero or infer unsupported business outcomes.

## Reference(s):

- [DDT API homepage](https://gotoshop-ai.com/ddtclaw/)
- [ClawHub skill page](https://clawhub.ai/horacetu/skills/ddt-tencent-map-retail-network)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown analysis with key metrics, coverage notes, data-version notes, limited store details when requested, and optional curl examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should avoid API keys, internal identifiers, supplier fields, source fields, and unsupported inferences.]

## Skill Version(s):

1.0.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
