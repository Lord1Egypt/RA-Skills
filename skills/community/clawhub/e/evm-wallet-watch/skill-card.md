## Description:

Checks an EVM wallet's native balance, ENS name, and five recent transactions on Ethereum, Base, or BSC through a paid x402 endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perria080925-bot](https://clawhub.ai/user/perria080925-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and wallet-monitoring agents use this skill to inspect an EVM address's balance, ENS name, wallet flags, and recent activity without operating a node or managing an API key. Each completed lookup requires a wallet-authorized payment to an external service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Each completed wallet lookup uses a paid external x402 endpoint and requires wallet payment authorization.

Mitigation: Verify the endpoint and payment details in the wallet client before signing; approve only intended requests.

## Reference(s):

- [EVM Wallet Watch on ClawHub](https://clawhub.ai/perria080925-bot/skills/evm-wallet-watch)

## Skill Output:

**Output Type(s):** [Text, Shell commands, JSON]

**Output Format:** [Markdown guidance and JSON wallet snapshot]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Snapshot includes native balance, ENS name, wallet flags, and up to five recent transactions.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
