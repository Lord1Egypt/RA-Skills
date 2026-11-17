## Description:

Monitors wallet and contract on-chain activity and summarizes balances, transactions, token transfers, and risk flags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinu4you](https://clawhub.ai/user/jinu4you)

### License/Terms of Use:

ISC

## Use Case:

Developers and operators use this skill to monitor Ethereum wallet or contract activity, inspect balances and recent transfers, and receive a concise risk-oriented summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can silently return mock blockchain data when the Etherscan API key is missing.

Mitigation: Require a valid ETHERSCAN_API_KEY for real monitoring, or clearly label and isolate mock-mode output before use.

Risk: Unsupported or unmapped chains can be mislabeled in output.

Mitigation: Reject unsupported chain values or map each supported chain to the correct upstream chain identifier.

Risk: Wallet and transaction context may be shared with outbound LLM providers.

Mitigation: Document outbound LLM data sharing and configure provider use according to the deployment's privacy requirements.

Risk: Dependencies were not reported as audited by the security evidence.

Mitigation: Audit dependencies before installation or production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jinu4you/skills/agent-onchain-watch)
- [Etherscan API endpoint](https://api.etherscan.io/v2/api)
- [Groq OpenAI-compatible API endpoint](https://api.groq.com/openai/v1)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Text]

**Output Format:** [JSON job result containing wallet balance, transactions, token transfers, risk flags, and a Korean Markdown summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an address input; optional chain and event_types values control the query scope.]

## Skill Version(s):

1.0.1 (source: evidence.release.version and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
