## Description:

AgentXPay enables AI agents to discover AI services on Monad, make x402 on-chain payments, manage wallets, manage subscriptions, and create escrow-backed tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonruan](https://clawhub.ai/user/jasonruan)

### License/Terms of Use:

MIT

## Use Case:

Developers and external agent builders use this skill to let an agent discover paid AI services, complete x402 payment flows on Monad, and manage agent wallets, subscriptions, and escrow for service access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can spend or lock blockchain funds through payments, subscriptions, escrow creation, wallet funding, spending-limit changes, and agent authorization.

Mitigation: Use test wallets or tightly limited wallets, configure spending caps outside the agent, and require separate human approval before any fund-moving or authorization action.

Risk: The skill can call arbitrary external service URLs during x402 payment flows.

Mitigation: Restrict allowed service endpoints and review target service details, price, chain ID, and payment recipient before payment.

Risk: The skill requires private-key based wallet access.

Mitigation: Avoid production private keys and provide only keys for wallets with limited balances and constrained permissions.

## Reference(s):

- [AgentXPay ClawHub skill page](https://clawhub.ai/jasonruan/skills/agentxpay)
- [AgentXPay publisher profile](https://clawhub.ai/user/jasonruan)
- [AgentXPay homepage](https://github.com/AgentXPay)
- [x402 protocol](https://www.x402.org/)
- [AgentXPay SDK API reference](references/sdk-api.md)
- [x402 protocol reference](references/x402-protocol.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON tool results and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool results may include service metadata, external service responses, wallet balances, transaction hashes, subscription identifiers, and escrow identifiers.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
