## Description:

Token on-chain analysis via Gate-Info MCP for holder distribution, on-chain activity, and large or unusual transfers, with Smart Money explicitly unavailable in this version.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request token-level on-chain analysis for holder distribution, activity trends, and large transfer summaries using read-only Gate-Info MCP data. The skill is informational and routes unsupported Smart Money or single-address requests to more appropriate capabilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an external Gate-Info MCP integration for token on-chain data.

Mitigation: Confirm the MCP server source is trusted and available before use; if tools are missing or fail, provide setup guidance or partial output instead of fabricating data.

Risk: On-chain data, exchange labels, and indexing may be delayed, incomplete, or mislabeled.

Mitigation: Report only MCP-returned data, label unavailable dimensions clearly, note data lag where relevant, and avoid overstating address or exchange attribution.

Risk: Users may treat on-chain analysis as trading advice.

Mitigation: Keep outputs neutral and informational, avoid buy or sell recommendations, and include the skill's non-advisory limitation in reports.

## Reference(s):

- [Gate Info Token Onchain Runtime Rules](references/gate-runtime-rules.md)
- [Info & News Common Runtime Rules](references/info-news-runtime-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with tables, metrics, and concise data-driven insights]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses only returned Gate-Info MCP data; notes unavailable scopes, unsupported chains, data lag, and non-advisory limitations.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
