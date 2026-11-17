## Description:

The Economic OS for OpenClaw. Autonomous USDC wallets on Base L2 via x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[horizonflowhq-ai](https://clawhub.ai/user/horizonflowhq-ai)

### License/Terms of Use:


## Use Case:

External users and developers use AgentPayy to let an OpenClaw agent manage a USDC wallet on Base L2, handle x402 micropayments, inspect balances, request test funds, and initiate payouts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create wallets and automatically resolve web paywalls from wallet funds without clear user approval or disclosure.

Mitigation: Require explicit transaction approval, separate wallet spending limits, and clear payment disclosure before allowing paid actions.

Risk: Marketplace and referral behavior may bias tool or sub-agent recommendations toward AgentPayy-enabled options.

Mitigation: Require disclosure of referral incentives and compare non-referral alternatives before acting on recommendations.

Risk: Payment dependencies and wallet integrations affect funds and should not rely on unreviewed package resolution.

Mitigation: Pin and review dependencies such as agentpayy-sdk, coinbase-cdp, and requests before installation or production use.

## Reference(s):

- [AgentPayy ClawHub skill page](https://clawhub.ai/horizonflowhq-ai/skills/agentpayy)
- [AgentPayy homepage](https://agentpayy-platform-production.up.railway.app/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with commands, Python examples, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide wallet setup, balance checks, funding requests, x402 payment retries, payouts, and marketplace or referral-related workflows.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
