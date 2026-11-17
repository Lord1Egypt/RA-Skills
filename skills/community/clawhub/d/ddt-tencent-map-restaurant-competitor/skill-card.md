## Description:

使用腾讯地图地址文本和店店通已发布门店快照，为餐饮品牌竞对网络变化、重点区域和市场行动建议提供可核验分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[horacetu](https://clawhub.ai/user/horacetu)

### License/Terms of Use:

MIT-0

## Use Case:

Market, sales, and competitive-intelligence users use this skill to analyze published restaurant brand network snapshots, compare expansion or contraction across brands and regions, and screen nearby stores or candidate locations when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Restaurant brand, address, and candidate-location queries are sent to the DDT/gotoshop-ai third-party API.

Mitigation: Use the skill only when sharing those queries with that service is acceptable, keep the API key private, and avoid confidential business plans or sensitive personal data.

Risk: Published store snapshots may not match official opening dates, closure announcements, revenue, same-store growth, profit, or closure reasons.

Mitigation: Report coverage windows and data definitions with conclusions, and avoid unsupported claims about official status or financial performance.

Risk: Store-level preview endpoints are limited and may return truncated or refinement-required results.

Mitigation: Narrow brand, address, date, province, city, or district inputs instead of paginating, enumerating regions, or reconstructing full store lists.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/horacetu/skills/ddt-tencent-map-restaurant-competitor)
- [DDT Claw homepage](https://gotoshop-ai.com/ddtclaw/)
- [DDT Open API key setup](https://gotoshop-ai.com/ddtclaw/open)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with concise findings, key metrics, coverage notes, and occasional bash curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DDT_API_KEY; responses should avoid API keys, internal IDs, version UUIDs, table names, suppliers, and unsupported revenue or profit claims.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
