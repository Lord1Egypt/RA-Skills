## Description:

Queries country-level customs trade overview summaries from Upkuajing, including annual trade totals, recent-quarter trade volume, and supplier and buyer counts for selected countries and years.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External trade teams, trade analysts, and market researchers use this skill to retrieve country-level customs trade summaries for market sizing, partner ecosystem review, and strategic planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an API key for billable Upkuajing account actions.

Mitigation: Store the key in the UPKUAJING_API_KEY environment variable or a permissioned credential file, and never expose the full key in chat, logs, screenshots, or support tickets.

Risk: Trade-summary queries, pricing lookups, account-info access, recharge-order creation, and related account actions can affect a paid account.

Mitigation: Require explicit user confirmation before each billable query or account/payment action, and check pricing through the documented pricing command or pricing page instead of estimating costs.

Risk: Error reports can include request context or response details that may contain sensitive business data.

Mitigation: Send error reports only after user confirmation and minimize request, response, and context data included in the report.

Risk: The scanner verdict is suspicious because API-key handling, recharge/payment helpers, account lookup, pricing lookup, update checks, and reporting helpers create credential and account risk.

Mitigation: Review the security summary and guidance before installation, especially when the skill will be connected to a paid Upkuajing account.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/customs-overview-summary-zh)
- [Upkuajing publisher profile](https://clawhub.ai/user/upkuajing)
- [Upkuajing homepage](https://www.upkuajing.com)
- [Upkuajing developer platform](https://developer.upkuajing.com/)
- [Upkuajing OpenAPI pricing](https://www.upkuajing.com/web/openapi/price.html)
- [国家贸易概览-交易汇总 API 参考](references/customs-overview-summary-api.md)
- [Agent调用Skill异常上报 API 参考](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON responses and concise natural-language guidance, with shell commands when an agent needs to run the bundled scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and the UPKUAJING_API_KEY credential; query responses include fee and request identifier fields when returned by the API.]

## Skill Version(s):

1.0.1 (source: evidence release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
