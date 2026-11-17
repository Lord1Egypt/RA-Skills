## Description:

Queries Eqxiu marketing calendar holidays and builds template mall search URLs via msearch-api.eqxiu.com for future promotional planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eqxiu](https://clawhub.ai/user/eqxiu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing and operations teams use this skill to find future Eqxiu marketing calendar events and prepare matching template search links for promotional planning. It is scoped to future marketing events and Eqxiu template discovery, not official public-holiday, legal, historical, or non-Eqxiu catalog lookups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on live HTTPS responses from msearch-api.eqxiu.com, so results may be unavailable or incomplete if the service is unreachable or changes behavior.

Mitigation: Run the documented CLI commands and disclose API or network errors instead of filling gaps from memory.

Risk: The skill is scoped to Eqxiu marketing events and is not an authoritative source for legal public holidays, historical dates, personal calendars, or non-Eqxiu template catalogs.

Mitigation: Use it only for future Eqxiu marketing planning and route legal, historical, personal calendar, or unrelated design-tool requests to appropriate sources.

## Reference(s):

- [API reference](references/API.md)
- [ClawHub skill page](https://clawhub.ai/eqxiu/skills/eqxiu-market-calendar)
- [Eqxiu current-date API](https://msearch-api.eqxiu.com/yyyymm)
- [Eqxiu monthly holiday API](https://msearch-api.eqxiu.com/m/holiday/queryByMonth)
- [Eqxiu mall search](https://www.eqxiu.com/mall/search?keywords=)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with CLI-derived holiday dates, promotion start dates, priority levels, and Eqxiu mall search links; JSON is available from the helper CLI.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should use the API-reported current date and CLI-provided mall_url values, with only future events returned.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
