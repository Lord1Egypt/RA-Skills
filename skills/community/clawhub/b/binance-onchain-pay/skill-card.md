## Description:

Binance Onchain Pay helps agents prepare and call Binance Onchain-Pay Open API endpoints for fiat-to-crypto purchases, on-chain transfers, merchant payment integration, smart contract interactions, and order monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dexploarer](https://clawhub.ai/user/dexploarer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to guide agents through Binance Onchain-Pay API workflows, including choosing supported payment endpoints, gathering required transaction parameters, signing requests, and returning readable API responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may handle crypto-payment credentials and signed financial API requests that can initiate high-impact transactions.

Mitigation: Use test credentials first, verify the Base URL before each request, and manually confirm every amount, asset, network, destination address, and contract target before execution.

Risk: Credential storage in .local.md can expose API keys or PEM key paths if the skill directory is shared or synced.

Mitigation: Avoid saving secrets in .local.md for shared environments, keep the PEM key outside shared or synced folders, and do not display private key contents or full API keys.

## Reference(s):

- [Authentication Reference](references/authentication.md)
- [ClawHub Skill Page](https://clawhub.ai/dexploarer/skills/binance-onchain-pay)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON examples and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include readable API responses and credential-handling guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
