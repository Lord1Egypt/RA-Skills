## Description:

查询供应商或采购商 Top N 排名，按国家维度和年份返回贸易量排名列表并支持游标分页。

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement agents, foreign trade teams, and trade analysts use this skill to identify top suppliers or buyers on a country trade route, evaluate market concentration, and support sourcing or sales planning with customs trade data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys can be exposed if ~/.upkuajing/.env is printed, shared, or captured in logs.

Mitigation: Use an environment variable or protected secret store, avoid printing or sharing the env file, and rotate the key if it appears in logs.

Risk: Each customs ranking query can incur paid API charges, including paginated follow-up requests.

Mitigation: Confirm every paid query deliberately before execution and use the pricing command or pricing page for current cost information.

Risk: The skill performs an automatic version check and writes a local cache during API use.

Mitigation: Review this network and local cache behavior before installation in managed or restricted environments.

Risk: Error reports may include raw request or response details.

Mitigation: Ask the user before reporting errors and include only the minimum non-sensitive context needed for troubleshooting.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/upkuajing/skills/customs-overview-top-n-zh)
- [upkuajing publisher profile](https://clawhub.ai/user/upkuajing)
- [Upkuajing homepage](https://www.upkuajing.com)
- [Upkuajing developer portal](https://developer.upkuajing.com/)
- [Customs Top N API reference](references/customs-overview-top-n-api.md)
- [Skill error report API reference](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with formatted JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses UPKUAJING_API_KEY and paid API calls; query results include ranking data, fee details, and request identifiers.]

## Skill Version(s):

1.0.1 (source: SKILL.md metadata and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
