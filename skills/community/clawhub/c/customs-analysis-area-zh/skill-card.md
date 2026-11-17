## Description:

查询指定 HS 编码在各国家和地区的贸易区域分布数据，支持按出口国或进口国以及最近月数筛选。

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Trade analysts, market researchers, and import/export operators use this skill to compare product trade activity by country or region for a specified HS code. It helps identify active export or import markets using trade counts, amount, buyer count, and supplier count.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a paid Upkuajing API account and normal query calls can incur charges.

Mitigation: Confirm paid queries separately before execution and review pricing through the documented price command or pricing page.

Risk: API credentials are required and the skill documentation includes a command that can display the local .env file.

Mitigation: Avoid displaying secrets in agent sessions and store the API key with restrictive local permissions or a secret manager.

Risk: Recharge and account-management commands can affect billing workflows.

Mitigation: Review recharge and account commands before use and require explicit user confirmation before payment-related actions.

## Reference(s):

- [区域分布 API Reference](references/customs-analysis-area-api.md)
- [Skill Error Report API Reference](references/skill-error-report-api.md)
- [ClawHub Skill Page](https://clawhub.ai/upkuajing/skills/customs-analysis-area-zh)
- [Upkuajing Homepage](https://www.upkuajing.com)
- [Upkuajing Developer Platform](https://developer.upkuajing.com/)
- [Upkuajing OpenAPI Pricing](https://www.upkuajing.com/web/openapi/price.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns per-country trade distribution records plus fee and request identifier information when API calls succeed.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
