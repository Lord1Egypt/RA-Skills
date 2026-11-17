## Description:

Pay for MCP tool calls on Hedera using x402 micropayments, discover AI agents via on-chain registry, check reputation before transacting, and submit ratings after tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emadqureshikhi](https://clawhub.ai/user/emadqureshikhi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to handle paid MCP tool calls on Hedera testnet, including x402 payment retry flows, agent discovery, reputation checks, and post-call ratings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Runtime use of unpinned payment tooling can install a package version that has not been reviewed for the deployment.

Mitigation: Use a reviewed, pinned SDK version through a lockfile or trusted package workflow before deployment.

Risk: The skill handles a Hedera private key and includes a CLI pattern where private key material could appear in command history, logs, or process lists.

Mitigation: Use a dedicated, minimally funded testnet key through HEDERA_PRIVATE_KEY, avoid mainnet keys, and do not pass private keys through command-line arguments.

Risk: Payment flows can spend more than intended if caps or network settings are changed without review.

Mitigation: Keep Hedera testnet defaults, retain spending caps, and increase payment limits only after confirming the recipient, asset, and expected cost.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/emadqureshikhi/skills/clawpay-hedera)
- [x402 Payment Flow on Hedera](references/x402-flow.md)
- [ClawPay-Hedera homepage](https://github.com/aspect-build/clawpay-hedera)
- [Hedera testnet registry contract](https://hashscan.io/testnet/contract/0x411278256411dA9018e3c880Df21e54271F2502b)
- [Reputation HCS topic](https://hashscan.io/testnet/topic/0.0.8107518)
- [Payment history HCS topic](https://hashscan.io/testnet/topic/0.0.8058213)
- [ClawPay agent dashboard](https://clawpay-hedera.vercel.app/agents)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose x402 payment handling, Hedera testnet CLI commands, reputation checks, and environment variable setup.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
