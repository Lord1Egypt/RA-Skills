## Description:

Queries Upkuajing customs data for monthly import and export trade totals over a specified date range with cursor-based pagination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Trade analysts, supply chain managers, and market researchers use this skill to retrieve monthly time-series trade totals, track changes in country-to-country trade volume, and inspect seasonal or cyclical patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store an Upkuajing API key in a plaintext home-directory `.env` file.

Mitigation: Prefer supplying `UPKUAJING_API_KEY` through a protected environment variable or secret manager, and do not ask the agent to print or paste the `.env` file.

Risk: Trade queries and account operations can interact with paid API, balance, and recharge endpoints.

Mitigation: Require explicit user confirmation before any paid query or recharge action, and use the pricing endpoint or published pricing page instead of estimating costs.

Risk: Error reports can include request context and optional request or response data.

Mitigation: Review the error report payload before submission and send it only after the user confirms.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/customs-overview-trend-zh)
- [Upkuajing homepage](https://www.upkuajing.com)
- [Upkuajing developer platform](https://developer.upkuajing.com/)
- [Upkuajing OpenAPI pricing](https://www.upkuajing.com/web/openapi/price.html)
- [国家贸易概览-进出口趋势 API 参考](artifact/references/customs-overview-trend-api.md)
- [Agent调用Skill异常上报 API 参考](artifact/references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and UPKUAJING_API_KEY; successful trade queries include paginated monthly trade data, fee details, and request identifiers.]

## Skill Version(s):

1.0.1 (source: release evidence and frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
