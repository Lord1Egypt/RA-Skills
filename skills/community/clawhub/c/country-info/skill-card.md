## Description:

Retrieve detailed country data including population, capital, languages, currencies, flag, and regional information using the REST Countries API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[picaye](https://clawhub.ai/user/picaye)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to answer country, language, currency, capital, population, flag, and regional-information questions. It is also useful for comparing countries or looking up countries by currency, language, code, or region.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Country, language, currency, or region lookup terms are sent to the REST Countries service.

Mitigation: Use only non-sensitive lookup terms and avoid sending internal or confidential context with API requests.

Risk: Country data may be unavailable, delayed, or shaped differently by the public REST Countries API.

Mitigation: Handle empty responses and nested fields carefully, and verify important facts before relying on them.

## Reference(s):

- [REST Countries API](https://restcountries.com/v3.1)
- [ClawHub skill page](https://clawhub.ai/picaye/skills/country-info)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with curl examples and plain-text country summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports optional REST Countries field filtering to reduce response size.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
