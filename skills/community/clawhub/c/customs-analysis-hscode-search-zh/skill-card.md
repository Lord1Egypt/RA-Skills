## Description:

Searches customs trade data by product name and HS-code keyword to return matching HS-code lists for downstream trade analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Trade analysts, exporters, importers, and agents use this skill to identify likely HS classifications before running deeper customs trade analyses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a paid Upkuajing API key and paid API calls.

Mitigation: Require explicit user confirmation before each paid query or recharge-order action, and check pricing through the documented price endpoint instead of estimating cost.

Risk: The API key may be stored in a local plaintext `.env` file.

Mitigation: Avoid printing the `.env` file, keep restrictive permissions on `~/.upkuajing/.env`, and treat the key as a secret.

Risk: Product names and HS-code search terms are sent to the Upkuajing platform.

Mitigation: Use the skill only when sending those query terms to the third-party API is acceptable for the user's workflow.

## Reference(s):

- [HS Code Search API Reference](references/customs-analysis-hscode-search-api.md)
- [Skill Error Report API Reference](references/skill-error-report-api.md)
- [ClawHub Skill Page](https://clawhub.ai/upkuajing/skills/customs-analysis-hscode-search-zh)
- [Upkuajing Homepage](https://www.upkuajing.com)
- [Upkuajing Developer Platform](https://developer.upkuajing.com/)
- [Upkuajing OpenAPI Pricing](https://www.upkuajing.com/web/openapi/price.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns matching HS-code lists with optional pagination cursor, fee information, and request ID when the API call succeeds.]

## Skill Version(s):

1.0.1 (source: server release evidence and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
