## Description:

Query on-chain crypto token, DEX, holder, transaction, chart, ranking, and contract-risk data through the AVE Cloud API, with optional pro-plan WebSocket streams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hope-ave](https://clawhub.ai/user/hope-ave)

### License/Terms of Use:


## Use Case:

Developers, analysts, and agents use this skill to resolve tokens, retrieve market and liquidity data, inspect holder and swap activity, monitor pro-plan live streams, and summarize AVE Cloud API results for on-chain crypto analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an AVE API key and outbound network access to AVE REST and WebSocket endpoints.

Mitigation: Install only where AVE credential use and outbound AVE endpoint access are acceptable, and keep AVE_API_KEY scoped and protected.

Risk: Pro-mode operation can control a persistent Docker container named ave-cloud-server on the host.

Mitigation: Avoid pro-mode server commands on shared machines, inspect for an existing ave-cloud-server container before use, and stop the container when monitoring is complete.

Risk: The security scan reports broader credential handling and Docker behavior than users should accept without review.

Mitigation: Review the skill and scan findings before deployment, and prefer pinned dependencies and base images before production use.

## Reference(s):

- [AVE Cloud API Reference](references/api-endpoints.md)
- [Official AVE Cloud Data API Documentation](https://ave-cloud.gitbook.io/data-api)
- [AVE Cloud](https://cloud.ave.ai/)
- [ClawHub Skill Page](https://clawhub.ai/hope-ave/skills/ave-cloud)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries and tables with JSON-derived data and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [REST commands print JSON to stdout; WebSocket commands stream pretty-printed JSON events separated by delimiters.]

## Skill Version(s):

1.2.0 (source: server release metadata; artifact frontmatter states 1.1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
