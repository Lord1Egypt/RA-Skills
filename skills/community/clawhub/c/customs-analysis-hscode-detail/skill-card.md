## Description:

Retrieves Chinese and English product descriptions for a given HS (Harmonized System) code from customs data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Trade professionals, analysts, and import-export practitioners use this skill to look up HS code meanings and verify product classification details before customs or trade-data analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid external API calls can incur charges.

Mitigation: Inform the user before any fee-incurring action and wait for explicit confirmation in a separate message before running the query.

Risk: The skill stores and reads an UpKuaJing API key locally.

Mitigation: Keep ~/.upkuajing/.env out of chat and logs, and avoid printing or exposing the API key during setup or troubleshooting.

Risk: Support reports can contain raw request or response data.

Mitigation: Send error reports only after user confirmation and sanitize request and response details before reporting them.

## Reference(s):

- [HS Code Detail API Reference](artifact/references/customs-analysis-hscode-detail-api.md)
- [Skill Error Report API Reference](artifact/references/skill-error-report-api.md)
- [ClawHub Skill Page](https://clawhub.ai/upkuajing/skills/customs-analysis-hscode-detail)
- [UpKuaJing Homepage](https://www.upkuajing.com)
- [UpKuaJing Developer Platform](https://developer.upkuajing.com/)
- [UpKuaJing OpenAPI Pricing](https://www.upkuajing.com/web/openapi/price.html)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON API responses with concise natural-language guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and an UPKUAJING_API_KEY; fee-incurring calls require explicit user confirmation before execution.]

## Skill Version(s):

1.0.1 (source: server evidence and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
