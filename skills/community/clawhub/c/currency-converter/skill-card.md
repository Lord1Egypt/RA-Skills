## Description:

Provides real-time or near-real-time currency exchange-rate lookup and conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wxsjlrwsj](https://clawhub.ai/user/wxsjlrwsj)

### License/Terms of Use:


## Use Case:

External users ask an agent to convert amounts between supported currencies or answer exchange-rate questions. The skill parses currency names or ISO-style codes, runs the converter, and returns a natural-language answer based on JSON conversion results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Currency lookups contact a third-party exchange-rate service.

Mitigation: Confirm that use of exchangerate-api.com is acceptable for the deployment and avoid sending sensitive context with conversion requests.

Risk: The Python dependency is specified as requests>=2.25.0 rather than pinned to an exact version.

Mitigation: Pin and review dependencies before use in security-sensitive or reproducible deployments.

Risk: The skill depends on network availability and external API responses for current rates.

Mitigation: Handle API failures clearly and verify important financial decisions against an authoritative source.

## Reference(s):

- [ExchangeRate API endpoint used by the skill](https://api.exchangerate-api.com/v4/latest/{from_currency})
- [Currency Converter on ClawHub](https://clawhub.ai/wxsjlrwsj/skills/currency-converter)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Natural-language response derived from JSON conversion results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on live access to the external exchange-rate API and the set of supported currencies in the converter script.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
