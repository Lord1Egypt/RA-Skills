## Description:

This skill queries Upkuajing customs analysis overview data and returns country-level supplier and buyer counts with cursor pagination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Trade analysts, market researchers, and import/export teams use this skill to query country-level customs overview data, compare supplier and buyer presence, and identify active markets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores or reads an Upkuajing API key locally.

Mitigation: Prefer a securely managed environment variable or secret store, and do not display or share the local API key file.

Risk: Overview queries and account recharge actions involve a paid third-party API.

Mitigation: Confirm every paid query or recharge action explicitly before running the related command.

Risk: Error reports may include sensitive request context or business data.

Mitigation: Review error report contents before sending them to the platform.

Risk: The release is a Chinese-language paid Upkuajing API integration.

Mitigation: Install only when the language, provider, account, and billing model are acceptable for the intended user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/customs-analysis-overview-zh)
- [Upkuajing homepage](https://www.upkuajing.com)
- [Upkuajing developer platform](https://developer.upkuajing.com/)
- [Upkuajing OpenAPI pricing](https://www.upkuajing.com/web/openapi/price.html)
- [Analysis overview API reference](references/customs-analysis-overview-api.md)
- [Skill error report API reference](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Overview queries return paginated country records, fee information, and request IDs when successful.]

## Skill Version(s):

1.0.1 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
