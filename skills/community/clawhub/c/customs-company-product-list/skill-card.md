## Description:

Query paginated product trade data for a company, including product names, trade counts, amounts, quantities, weights, trade percentages, and associated HS codes for product-mix analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts, trade operations teams, and agents use this skill to inspect a company's import-export product mix, page through product-level customs trade results, and relate products to HS codes for portfolio analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose or persist an UpKuaJing API key locally.

Mitigation: Keep UPKUAJING_API_KEY out of chat and logs, avoid commands that print ~/.upkuajing/.env, and rotate the key if it is disclosed.

Risk: Product-list queries and account top-up flows may incur costs.

Mitigation: Confirm each paid query or top-up action separately before execution and check current pricing through the provided UpKuaJing pricing reference or price-info command.

Risk: Error reports may include sensitive request or business context.

Mitigation: Submit error reports only after user confirmation and keep the report minimal, excluding secrets and sensitive commercial data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/customs-company-product-list)
- [UpKuaJing homepage](https://www.upkuajing.com)
- [UpKuaJing Open Platform](https://developer.upkuajing.com/)
- [UpKuaJing OpenAPI pricing](https://www.upkuajing.com/web/openapi/price.html)
- [Company Product List API](references/customs-company-product-list-api.md)
- [Skill Error Report API](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and UPKUAJING_API_KEY; paid product-list API calls should be confirmed before execution.]

## Skill Version(s):

1.0.1 (source: skill frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
