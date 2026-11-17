## Description:

帮助餐饮拓展和选址人员用高德地图复制的地点名称或地址文本，结合店店通已发布门店快照分析机会区域、候选地址竞争与现场验证优先级。

This skill is ready for commercial/non-commercial use.

## Publisher:

[horacetu](https://clawhub.ai/user/horacetu)

### License/Terms of Use:

MIT-0

## Use Case:

External restaurant expansion, sales, and site-selection users use this skill to turn copied Amap place/address text into bounded restaurant-network analysis. It supports opportunity-area review, candidate-site competition checks, risk and data-gap notes, and next-step field-verification priorities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented API setup can send the bearer token to an inherited, unvalidated endpoint.

Mitigation: Set the API base explicitly to https://gotoshop-ai.com/ddtclaw before use and avoid running the skill with untrusted inherited environment variables.

Risk: Pasted addresses or candidate-site details are sent to the provider service during analysis.

Mitigation: Treat user-provided location and candidate-site details as provider-shared data and review them before submission.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/horacetu/skills/ddt-amap-restaurant-expansion)
- [店店通 Claw homepage](https://gotoshop-ai.com/ddtclaw/)
- [店店通 API key setup](https://gotoshop-ai.com/ddtclaw/open)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown analysis with concise conclusions, key metrics, coverage notes, limited detail rows when requested, and unmet coverage notes; setup examples may use bash or curl.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should avoid API keys, internal identifiers, table names, supplier names, version UUIDs, and English enum values.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
