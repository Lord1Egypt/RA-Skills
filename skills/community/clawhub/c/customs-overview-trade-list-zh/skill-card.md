## Description:

查询分页的国家级贸易列表数据，返回年度、季度和月度贸易量以及供应商、采购商数量，用于跨国家进出口比较和市场分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External trade teams, market researchers, and trade analysts use this skill to query paginated country-level import and export breakdowns by origin country, arrival country, and year. It supports market comparison, market-penetration analysis, and discovery of growth opportunities across global country and region trade data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid third-party API calls can incur charges, including paginated country-trade queries and recharge flows.

Mitigation: Tell the user a charge may occur and wait for explicit confirmation in a separate message before each paid query, recharge action, or payment flow.

Risk: The skill stores an API key under `~/.upkuajing` and the artifact includes guidance that could expose that credential.

Mitigation: Prefer a safer environment-variable credential mechanism, do not display the credential file contents, and avoid sharing `UPKUAJING_API_KEY` in logs or messages.

Risk: Error reports may include request parameters, response data, or context from failed API calls.

Mitigation: Ask for user confirmation before sending an error report and avoid sending sensitive request or response data.

Risk: The skill includes account, payment, telemetry, and update-check behavior.

Mitigation: Review account and recharge commands before use, confirm chargeable or payment actions separately, and keep request logging disabled unless explicitly needed.

## Reference(s):

- [国家贸易概览-国家贸易列表 API 参考](artifact/references/customs-overview-trade-list-api.md)
- [Agent调用Skill异常上报 API 参考](artifact/references/skill-error-report-api.md)
- [ClawHub Skill Page](https://clawhub.ai/upkuajing/skills/customs-overview-trade-list-zh)
- [Upkuajing Homepage](https://www.upkuajing.com)
- [Upkuajing Developer Platform](https://developer.upkuajing.com/)
- [Upkuajing OpenAPI Pricing](https://www.upkuajing.com/web/openapi/price.html)

## Skill Output:

**Output Type(s):** [text, shell commands, JSON, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires UPKUAJING_API_KEY; trade-list API calls are paid and paginated.]

## Skill Version(s):

1.0.1 (source: server release metadata and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
