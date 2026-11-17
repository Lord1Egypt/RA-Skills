## Description:

Lets agents retrieve and summarize stock quotes, disclosures, market themes, financial and macroeconomic data, commodity prices, FDA recalls, and stock graph summaries, prioritizing key-free queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[finxdata](https://clawhub.ai/user/finxdata)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent in natural language for market and company data. The agent selects a supported query, reports the returned dates and coverage, and summarizes results without placing trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: FinXData receives query parameters and client type and can observe the caller's IP address.

Mitigation: Prefer key-free queries, configure an API key only when account data is needed, and check usage limits and returned data dates.

## Reference(s):

- [Quickstart](references/quickstart.md)
- [API Reference](references/api.md)
- [Usage Guide](references/usage.md)
- [FinXData](https://www.finxdata.ai)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Natural-language summaries of API data returned as JSON or Markdown tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarize key fields and data dates; identify missing or partial results.]

## Skill Version(s):

1.0.17 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
