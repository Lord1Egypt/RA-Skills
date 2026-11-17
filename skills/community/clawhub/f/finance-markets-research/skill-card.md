## Description:

Research stocks, crypto, SEC filings, insider/congressional trading, and private-market profiles through Crawlora. Use for one-ticker data, filing lookups, or market snapshots; for matched financial-statement comparisons across public-company peers, use company-fundamentals-comparison.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and other users use this skill to retrieve public market data, SEC filings, trade disclosures, cryptocurrency snapshots, and private-market teaser profiles for research. It supports ticker lookups, filing searches, and market snapshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research queries and the API key are sent to Crawlora; queries may contain confidential information.

Mitigation: Keep the key in CRAWLORA_API_KEY and avoid including confidential information in queries.

Risk: API requests consume service credits.

Mitigation: Monitor request usage against the account's credit allowance.

## Reference(s):

- [Endpoint reference](reference/endpoints.md)
- [Crawlora service](https://crawlora.net)
- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/finance-markets-research)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Normalized JSON research data with agent-facing summaries and guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public data responses. PitchBook profiles are teaser-level and directional; SEC full-text search covers filings from 2001 onward.]

## Skill Version(s):

1.0.21 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
