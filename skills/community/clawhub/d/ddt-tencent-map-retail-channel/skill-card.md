## Description:

零售渠道的业态结构、城市覆盖、竞品差异与市场机会分析。可将腾讯地图中复制出的地点名称和地址文本作为地点输入；基于店店通已发布门店快照生成可核验结论。本 Skill 非腾讯地图官方产品，和腾讯地图不存在合作、授权或数据来源关系。

This skill is ready for commercial/non-commercial use.

## Publisher:

[horacetu](https://clawhub.ai/user/horacetu)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts and business users use this skill to analyze published retail brand snapshots for channel structure, city coverage, competitor differences, nearby stores, and market opportunities from Tencent Map address text or explicit coordinates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends a bearer token to the configured DDT service endpoint.

Mitigation: Use only a trusted DDT_API_KEY and keep DDT_OPEN_BASE unset or pinned to https://gotoshop-ai.com/ddtclaw/ before use.

Risk: Retail conclusions can be incomplete when coverage fields or preview limits indicate missing or truncated data.

Mitigation: Report coverage and data-version limits, stop unsupported conclusions when coverage is unavailable, and narrow queries when previews are truncated.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/horacetu/skills/ddt-tencent-map-retail-channel)
- [Publisher profile](https://clawhub.ai/user/horacetu)
- [DDT Claw API homepage](https://gotoshop-ai.com/ddtclaw/)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with concise conclusions, key metrics, coverage notes, and optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses published retail snapshots and may include limited store previews only when the user supplies explicit coordinates or a public store ID.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
