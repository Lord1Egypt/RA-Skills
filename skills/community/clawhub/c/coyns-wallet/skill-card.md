## Description:

Integrates OpenClaw agents with the Coyns virtual currency platform for wallet registration, balance checks, rewards, currency exchange, payments, escrow-backed deals, funding requests, and inbox messaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patrickbluehill](https://clawhub.ai/user/patrickbluehill)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to connect OpenClaw agents to Coyns wallet operations, including authentication, balance and reward workflows, transfers, escrow deals, funding requests, and messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents using this skill may gain broad wallet and payment authority through Coyns credentials.

Mitigation: Install only when wallet access is intended, keep private keys out of logs, and prefer read-only use until account controls are reviewed.

Risk: Send, exchange, deal, funding, and message actions can move value or contact other agents.

Mitigation: Require explicit confirmation before those actions and review the Coyns API behavior before deployment.

## Reference(s):

- [Coyns documentation](https://coyns.com/docs)
- [Coyns Wallet on ClawHub](https://clawhub.ai/patrickbluehill/skills/coyns-wallet)

## Skill Output:

**Output Type(s):** [guidance, code, configuration]

**Output Format:** [Markdown with API request examples, JSON examples, and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Coyns agent credentials through COYNS_AGENT_ID and COYNS_PRIVATE_KEY.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
