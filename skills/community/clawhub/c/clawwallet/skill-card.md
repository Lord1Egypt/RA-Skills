## Description:

Clawwallet gives AI agents a multi-chain wallet control surface for wallet creation and import, balances, transfers, DeFi operations, multisig workflows, policies, ENS, identity, webhooks, and wallet activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vibes-me](https://clawhub.ai/user/vibes-me)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect AI agents to a wallet service for multi-chain wallet management, token movement, DeFi workflows, multisig coordination, policy checks, identity registration, and wallet event handling. Because it can move assets and submit secrets, deployments should use trusted wallet infrastructure and explicit human approval for sensitive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move assets and submit wallet secrets through a wallet service without clear local confirmation or transport safeguards.

Mitigation: Use only trusted wallet services over HTTPS or verified local transport, scope API keys, enforce spending limits, and require explicit human approval before asset movement or secret submission.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vibes-me/skills/clawwallet)
- [Publisher Profile](https://clawhub.ai/user/vibes-me)
- [CLAWwallet Documentation](https://clawwallet.pages.dev)

## Skill Output:

**Output Type(s):** [text, code, configuration, guidance]

**Output Format:** [JavaScript module methods returning structured JSON-like operation results and status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calls a configured wallet service and may require CLAW_WALLET_URL, CLAW_WALLET_API_KEY, and CLAW_WALLET_CHAIN environment settings.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
