## Description:

Fetches aggregated customs-trade statistics by company ID across more than 220 countries and territories to support supplier screening, buyer validation, and trade-intelligence research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External trade analysts, export teams, and researchers use this skill to retrieve summarized company trade volume, shipment weight, product quantity, transaction value, partner count, and trade date range from UpKuaJing customs data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads or writes an UpKuaJing API key in a plaintext home-directory file.

Mitigation: Use a dedicated environment, restrict permissions on ~/.upkuajing/.env to the owner, and avoid displaying or pasting the key in chat or logs.

Risk: Company statistics queries and account top-up flows can incur fees or initiate payment-order creation.

Mitigation: Confirm each paid query or recharge action explicitly before running scripts, and check current pricing through the provider's pricing page or price-info command.

Risk: Confirmed diagnostic reports and automatic version checks send information to the provider.

Mitigation: Review report contents before submission and use a controlled environment when automatic provider calls are not acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/customs-company-stats)
- [UpKuaJing homepage](https://www.upkuajing.com)
- [UpKuaJing Open Platform](https://developer.upkuajing.com/)
- [Detailed price description](https://www.upkuajing.com/web/openapi/price.html)
- [Company Basic Trade Statistics API](references/customs-company-stats-api.md)
- [Error Report API](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python, httpx, and UPKUAJING_API_KEY; paid API calls require explicit user confirmation before execution.]

## Skill Version(s):

1.0.2 (source: release evidence and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
