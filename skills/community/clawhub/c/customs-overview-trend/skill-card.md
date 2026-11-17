## Description:

Query import/export trade trend data to retrieve monthly trade volume trends within a specified time range with cursor-based pagination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Trade analysts, supply chain managers, market researchers, and agents acting on their behalf use this skill to retrieve monthly import/export trade volume trends, explore paginated time series data, and identify seasonal or cyclical changes across country trade flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store an UpKuaJing API key in a plaintext home-directory file.

Mitigation: Prefer an environment variable when possible, avoid printing `.env` contents, and restrict permissions on `~/.upkuajing/.env`.

Risk: Trend queries are paid API calls and account top-up flows can create payment orders.

Mitigation: Require explicit user confirmation before paid calls or payment-order creation, and check current pricing and balance before execution.

Risk: Confirmed error reports can send troubleshooting details to the platform.

Mitigation: Send reports only after user confirmation and avoid including sensitive request details beyond what is needed for diagnosis.

Risk: The skill performs version-check behavior and writes a local version cache.

Mitigation: Review the version-check behavior before use and account for the local cache under `~/.upkuajing/`.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/customs-overview-trend)
- [UpKuaJing homepage](https://www.upkuajing.com)
- [UpKuaJing Open Platform](https://developer.upkuajing.com/)
- [UpKuaJing API pricing](https://www.upkuajing.com/web/openapi/price.html)
- [Customs Overview Trend API reference](references/customs-overview-trend-api.md)
- [Skill Error Report API reference](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and an UPKUAJING_API_KEY; successful trend queries return monthly trade data, fee information, request identifiers, and cursor pagination when more results are available.]

## Skill Version(s):

1.0.1 (source: release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
