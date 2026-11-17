## Description:

餐饮品牌竞对情报专家，分析品牌开关店、月末在营趋势、重点省市与竞争方向。适用于市场、战略和竞品团队监测对手扩张收缩、比较品牌网络并形成月度市场判断。

This skill is ready for commercial/non-commercial use.

## Publisher:

[horacetu](https://clawhub.ai/user/horacetu)

### License/Terms of Use:

MIT-0

## Use Case:

Market, strategy, sales, and competitive-intelligence teams use this skill to analyze published restaurant-brand network changes, compare competitors over a common coverage window, and turn opening, closing, trend, and regional signals into market actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Restaurant brand, address, and market-analysis queries are sent to the disclosed gotoshop-ai.com API.

Mitigation: Confirm the user is comfortable with that data flow before installation or use, and require the user's own DDT API key.

Risk: A DDT API key could be exposed if copied into prompts, outputs, logs, or shared artifacts.

Mitigation: Store the key only in the local environment variable and do not display it in responses.

Risk: Overbroad store extraction could exceed the skill's intended preview and aggregation boundaries.

Mitigation: Use aggregate endpoints first, respect preview limits, avoid automatic pagination or regional enumeration, and ask the user to narrow store-level requests.

Risk: Business conclusions can be misleading when API responses are unavailable, partial, truncated, or missing required capabilities.

Mitigation: Check status, coverage period, truncation markers, and capabilities before drawing conclusions; stop the business conclusion when required evidence is absent.

## Reference(s):

- [DDT Claw Homepage](https://gotoshop-ai.com/ddtclaw/)
- [DDT Claw API Key Setup](https://gotoshop-ai.com/ddtclaw/open)
- [ClawHub Skill Page](https://clawhub.ai/horacetu/skills/ddt-restaurant-competitor-expert)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Shell commands, Guidance]

**Output Format:** [Markdown with concise analysis, key metrics, coverage notes, and optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses aggregate restaurant-network facts by default; only includes limited store-level details when the user explicitly asks for specific stores, addresses, or candidate sites.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
