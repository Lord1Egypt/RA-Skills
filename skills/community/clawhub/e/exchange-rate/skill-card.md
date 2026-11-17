## Description:

Real-time forex and cryptocurrency exchange rate lookup and amount conversion powered by QVeris. Supports multiple providers (Alpha Vantage, Twelve Data) with fallback for reliability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ax2](https://clawhub.ai/user/ax2)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to retrieve current exchange rates, convert amounts between currencies, and optionally request historical rates when the selected QVeris-backed tool supports them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Currency pair, amount, and optional date values are sent to QVeris when the skill runs.

Mitigation: Only set QVERIS_API_KEY and run lookups when sharing that query data with QVeris is acceptable.

Risk: Returned exchange-rate data may be unsuitable for financial, contractual, or trading decisions without confirmation.

Mitigation: Treat results as reference data and verify material decisions against an authoritative rate source.

Risk: An unpinned installer command could install a different release than the reviewed artifact.

Mitigation: Install from a verified source, copy the reviewed skill folder, or pin the installer/release before deployment.

## Reference(s):

- [ClawHub Exchange Rate Skill](https://clawhub.ai/ax2/skills/exchange-rate)
- [QVeris](https://qveris.ai)
- [QVeris API Endpoint](https://qveris.ai/api/v1)
- [Publisher Profile](https://clawhub.ai/user/ax2)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown or JSON exchange-rate results with optional shell command usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns rate, converted amount when requested, currency pair, selected tool identifier, or an error message.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
