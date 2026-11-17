## Description:

Trust scoring for AI agents that logs transactions and submits payment proofs to build a verifiable BOB Score that other agents and services can check before doing business.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bankofbotsandy](https://clawhub.ai/user/bankofbotsandy)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to configure Bank of Bots credentials, inspect wallets and policies, initiate or record payments, submit BTC payment proofs, manage counterparties, and check agent trust history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents through real money movement, including transfers, outbound payments, BTC intents, and proof submission.

Mitigation: Require explicit human approval before any transfer or payment execution, and start with low wallet budgets plus server-side spend limits.

Risk: Operator credentials can create sub-agents, rotate keys, fund agents, and administer payment addresses or webhooks.

Mitigation: Keep operator keys separate from ordinary trust-score workflows and expose only narrowly scoped credentials to agents.

Risk: Payment routing, webhook changes, key rotation, and sub-agent creation can alter account behavior beyond simple trust-score lookup.

Mitigation: Review these commands before deployment and require approval for payment, webhook, key-management, and sub-agent administration actions.

## Reference(s):

- [Bank of Bots agent setup documentation](https://app.bankofbots.ai/docs/agent-setup)
- [Bank of Bots ClawHub skill page](https://clawhub.ai/bankofbotsandy/skills/bank-of-bots)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls]

**Output Format:** [Markdown with inline bash code blocks and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands return structured JSON with ok, data, and next_actions fields.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
