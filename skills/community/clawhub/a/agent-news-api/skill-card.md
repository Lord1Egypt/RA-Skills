## Description:

A set of free and premium AI-enriched global news streams for agents, provided by agentnewsapi.com and powered by $ANA on Solana.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentnewsdev](https://clawhub.ai/user/agentnewsdev)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to fetch free delayed or paid real-time news signals, check credit balances, onboard with Solana-signed authentication, and consume a premium WebSocket firehose.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet-linked authentication and API credentials can expose account or financial value if the runtime environment is compromised.

Mitigation: Use a dedicated low-balance Solana key, store credentials only in a controlled environment, and rotate the API key if exposure is suspected.

Risk: Endpoint override and network behavior can increase credential-routing and replay risk.

Mitigation: Pin AGENT_NEWS_API_URL to https://api.agentnewsapi.com and review network access before installation.

Risk: Paid premium fetches or streaming can consume credits unexpectedly.

Mitigation: Set explicit spending and streaming limits, check the credit balance before long-running use, and monitor credit changes during operation.

Risk: Dependency integrity is harder to verify without a lockfile.

Mitigation: Use pinned dependencies with a reviewed lockfile before production deployment.

## Reference(s):

- [Agent News API ClawHub listing](https://clawhub.ai/agentnewsdev/skills/agent-news-api)
- [Agent News API endpoint](https://api.agentnewsapi.com)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON responses and JSON event streams, with CLI help text for command usage.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Premium endpoints can require API credentials, Solana wallet-linked authentication, and available credit balance.]

## Skill Version(s):

1.2.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
