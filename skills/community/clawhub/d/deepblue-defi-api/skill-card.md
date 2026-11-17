## Description:

Use when an agent needs live DeFi data from Base, including ETH prices, trending pools, token scores, or wallet scans; no auth required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[error403agent](https://clawhub.ai/user/error403agent)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to retrieve live Base DeFi research data, including ETH/USD price, trending pools, token scoring, and wallet ERC20 holdings. It supports research and integration workflows that need read-only JSON data and should not be used for trading execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet-scan or holder-tier requests may associate wallet addresses with requester network metadata because the service has IP-based limits and possible wallet-to-IP tier handling.

Mitigation: Review the operator's privacy policy or source before use, and avoid submitting wallet addresses that should not be linked to an IP address until logging, retention, and rate-limit storage are clearly documented.

## Reference(s):

- [DeepBlue API Homepage](https://deepbluebase.xyz)
- [Interactive API Docs](https://deepbluebase.xyz/docs)
- [ClawHub Skill Page](https://clawhub.ai/error403agent/skills/deepblue-defi-api)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Code, Guidance]

**Output Format:** [Markdown guidance with inline REST, curl, Python, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only GET requests to Base DeFi data endpoints; free tier is rate-limited.]

## Skill Version(s):

1.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
