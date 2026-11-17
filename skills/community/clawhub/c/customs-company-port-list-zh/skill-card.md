## Description:

查询公司海关贸易港口列表数据，获取港口的贸易次数、金额、数量、重量和占比，用于物流通道和进出口港口分布分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External trade and logistics teams use this skill to query a company's customs trade ports, inspect per-port trade counts, amounts, quantities, weights, and percentages, and identify key import or export routes. Developers and agents can use it to run the documented Upkuajing API scripts with user-confirmed paid calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles an API key that may grant access to paid customs data and account functions.

Mitigation: Use a dedicated low-balance API key, avoid exposing ~/.upkuajing/.env, and check local file permissions before use.

Risk: Company port lookups and some account actions can incur charges or create recharge URLs.

Mitigation: Require explicit user confirmation before paid queries, recharge URL creation, or any other account-affecting operation.

Risk: Error reports may include request context or trade-query details.

Mitigation: Submit error reports only after user approval and avoid including unnecessary sensitive business details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/customs-company-port-list-zh)
- [Upkuajing homepage](https://www.upkuajing.com)
- [Upkuajing developer platform](https://developer.upkuajing.com/)
- [Upkuajing OpenAPI pricing](https://www.upkuajing.com/web/openapi/price.html)
- [公司贸易港口列表 API 参考](references/customs-company-port-list-api.md)
- [Agent调用Skill异常上报 API 参考](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Markdown, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and UPKUAJING_API_KEY; successful lookup responses include port records, fee information, and request IDs.]

## Skill Version(s):

1.0.1 (source: artifact frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
