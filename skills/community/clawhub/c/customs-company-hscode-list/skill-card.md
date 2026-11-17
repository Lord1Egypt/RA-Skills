## Description:

Query paginated HS code trade data for a company, including HS codes, trade counts, amounts, quantities, weights, and percentage share for supplier or buyer product-mix analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query UpKuaJing customs trade data for a known company ID, paginate through HS-code breakdowns, and analyze supplier or buyer product mix by trade volume, value, quantity, weight, and share.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HS-code queries incur fees, and account top-up flows can create payment URLs.

Mitigation: Confirm each fee-incurring query and any recharge action with the user before running the related script.

Risk: The integration uses UPKUAJING_API_KEY and may store the API key in ~/.upkuajing/.env.

Mitigation: Prefer a secure environment variable mechanism, restrict file permissions, and do not print or share the local API-key file.

Risk: Error reporting can send troubleshooting context and request details to the platform.

Mitigation: Review the report payload for sensitive data and send it only after explicit user confirmation.

Risk: The skill performs automatic version checks against the UpKuaJing service.

Mitigation: Review outbound network behavior before deployment in restricted environments.

## Reference(s):

- [Company HS Code List API Reference](references/customs-company-hscode-list-api.md)
- [Skill Error Report API Reference](references/skill-error-report-api.md)
- [ClawHub Skill Page](https://clawhub.ai/upkuajing/skills/customs-company-hscode-list)
- [UpKuaJing Homepage](https://www.upkuajing.com)
- [UpKuaJing Open Platform](https://developer.upkuajing.com/)
- [UpKuaJing OpenAPI Pricing](https://www.upkuajing.com/web/openapi/price.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and UPKUAJING_API_KEY; HS-code queries are paginated and fee-incurring.]

## Skill Version(s):

1.0.1 (source: SKILL.md metadata and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
