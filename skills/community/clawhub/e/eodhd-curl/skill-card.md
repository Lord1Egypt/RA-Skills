## Description:

Provides access to EODHD financial data APIs for company profiles, market prices, fundamentals, economic data, exchange information, and alternative datasets through curl-based REST API requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mancubus77](https://clawhub.ai/user/mancubus77)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to retrieve financial market, company, fundamentals, calendar, news, sentiment, macroeconomic, options, and exchange data from EODHD APIs. It is most useful when an agent needs concrete curl commands and endpoint-selection guidance for EODHD-backed financial data tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API-token handling can reveal the user's EODHD key in logs, terminal history, transcripts, or full request URLs.

Mitigation: Read the token from EODHD_API_TOKEN, avoid printing full tokenized URLs, prefer constrained tokens, monitor quota usage, and rotate the token if it appears in logs or transcripts.

Risk: Large or broad financial data requests can consume quota or return excessive data.

Mitigation: Use explicit date ranges, limits, filters, and the EODHD usage endpoint to control request size and monitor subscription limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mancubus77/skills/eodhd-curl)
- [EODHD API base URL](https://eodhd.com/api/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline curl command examples and endpoint guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and the EODHD_API_TOKEN environment variable.]

## Skill Version(s):

0.0.1 (source: server release metadata); skill frontmatter reports 1.0.0

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
