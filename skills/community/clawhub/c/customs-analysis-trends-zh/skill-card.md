## Description:

查询指定 HS 编码在最近数月内的进出口贸易趋势数据，返回出口和进口的月度贸易次数、数量、重量、金额、采购商数量和供应商数量。

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Trade analysts, supply-chain managers, and market researchers use this skill to query Upkuajing customs-trade APIs for monthly import and export trends by HS code, including optional country filtering. It supports time-series analysis of product trade activity, seasonality, and import-versus-export changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed because the skill supports storing UPKUAJING_API_KEY in a local plaintext .env file and documents commands that display that file.

Mitigation: Use a secure environment or secret manager where possible, avoid printing the .env file in chat or logs, and restrict permissions on any local credential file.

Risk: Trade queries and account actions can incur charges or create recharge payment URLs.

Mitigation: Confirm billable operations separately before execution, review current pricing through the vendor's pricing reference, and verify payment URLs before opening them.

Risk: The skill can report errors to the platform and may include request context when the user confirms reporting.

Mitigation: Review the report payload before submission and remove unnecessary sensitive or business-confidential context.

Risk: The skill performs version checks and writes version-check cache data under the user's home directory.

Mitigation: Review local files created under ~/.upkuajing and remove cached data if it is not desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/customs-analysis-trends-zh)
- [Upkuajing homepage](https://www.upkuajing.com)
- [Upkuajing developer portal](https://developer.upkuajing.com/)
- [Upkuajing OpenAPI pricing](https://www.upkuajing.com/web/openapi/price.html)
- [Trade trends API reference](references/customs-analysis-trends-api.md)
- [Skill error-report API reference](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and UPKUAJING_API_KEY; billable API calls should be confirmed before execution.]

## Skill Version(s):

1.0.1 (source: server release metadata and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
