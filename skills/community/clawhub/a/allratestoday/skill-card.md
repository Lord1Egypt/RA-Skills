## Description:

Exchange rates and currency conversion ('convert 200 USD to EUR', 'GBP/JPY rate'), plus the official rate a named central bank or tax authority published (ECB, HMRC, RBI, SAMA, 120 more) for invoices, VAT, customs or audit. Fetches with web_fetch, curl fallback. Keyless; API key optional for live mid-market rates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cahthuranag](https://clawhub.ai/user/cahthuranag)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users fetch current currency conversions or rates published by a named central bank or tax authority, then present results with the returned date and source.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An optional API key could be exposed or misused.

Mitigation: Keep the key private and read it from the environment without printing it.

Risk: A returned rate may be stale or tied to a different publication date than expected.

Mitigation: Check and report the returned date or rate_date, including when an institution marks its table stale.

Risk: The provider limits some institutional-rate use to personal, non-commercial use, and attribution terms apply.

Mitigation: Review the provider's usage and attribution terms before commercial use.

## Reference(s):

- [AllRatesToday API documentation](https://allratestoday.com/docs/)
- [Institution codes](references/institutions.md)
- [Published institution list](https://allratestoday.com/central-bank-rates-api/institutions/)
- [AllRatesToday MCP documentation](https://allratestoday.com/mcp/)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Natural-language response with conversion amounts or rates, dates, and publisher/source]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Rate direction and rate type are included where relevant; stale institutional data should be identified by its returned date.]

## Skill Version(s):

1.0.2 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
