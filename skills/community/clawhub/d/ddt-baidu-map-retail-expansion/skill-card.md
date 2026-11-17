## Description:

使用百度地图复制的地点名称和地址文本，分析零售连锁的机会城市、候选地址竞争和拓店顺序，并基于店店通已发布门店快照生成可核验结论。

This skill is ready for commercial/non-commercial use.

## Publisher:

[horacetu](https://clawhub.ai/user/horacetu)

### License/Terms of Use:

MIT-0

## Use Case:

External retail expansion teams and analysts use this skill to evaluate published retail brands, compare regional store coverage, screen candidate addresses, and organize site-selection conclusions from 店店通 API responses. It is not an official Baidu Maps product and does not claim a Baidu Maps partnership, authorization, or data-source relationship.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Retail queries, copied map addresses, coordinates, and expansion plans may be sent to the configured DDT API service.

Mitigation: Use the skill only when that provider is acceptable for the use case, avoid sharing confidential expansion plans, and keep the DDT API key in environment variables only.

Risk: Candidate-site and nearby-store outputs are limited previews and may not represent a full market list or opening-success probability.

Mitigation: Treat outputs as an initial screen, review coverage indicators, narrow truncated previews, and perform offline validation before making location decisions.

Risk: Missing coverage or unavailable fields could be misread as zero values or business trends.

Mitigation: Report unavailable coverage explicitly and do not infer openings, closures, monthly changes, or missing metrics beyond the current published snapshot.

## Reference(s):

- [店店通 DDT API homepage](https://gotoshop-ai.com/ddtclaw/)
- [ClawHub skill page](https://clawhub.ai/horacetu/skills/ddt-baidu-map-retail-expansion)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and structured site-selection analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries should use only API response fields, include coverage and data-version notes, and avoid exposing API keys, internal identifiers, suppliers, or raw internal fields.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
