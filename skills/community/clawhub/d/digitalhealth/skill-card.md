## Description:

Implements USDC x402 payments via PayAI (EIP-3009) and DHM x402 payments via EVVM native signed pay for ClawHub/Digital Health EVVM payment flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arunnadarasa](https://clawhub.ai/user/arunnadarasa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add or debug x402 payment flows for USDC via PayAI Echo and DHM via EVVM native pay, including browser-wallet and agent-to-agent payment paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives high-impact crypto payment guidance that could cause unintended transfers if used without review.

Mitigation: Review and harden the integration before installing it in any wallet-enabled environment, and use testnet by default.

Risk: Weak validation or fallback payment-option selection could route payments to unintended contracts, recipients, tokens, networks, executors, or amounts.

Mitigation: Require exact local allowlists for contracts, recipients, tokens, networks, executors, and amounts, and remove fallback option selection.

Risk: Autonomous wallet instructions may allow agent-initiated payments beyond the intended scope.

Mitigation: Keep Privy secrets server-side, pin and inspect the Privy skill before installation, and require human approval or strong policy limits for autonomous payment paths.

## Reference(s):

- [ClawHub Digital Health Skill](https://clawhub.ai/arunnadarasa/skills/digitalhealth)
- [PayAI Echo Base Sepolia Paid Content Endpoint](https://x402.payai.network/api/base-sepolia/paid-content)
- [DHM x402 EVVM Server](https://evvm-x402-dhm.fly.dev)
- [Privy Agentic Wallets Skill](https://github.com/privy-io/privy-agentic-wallets-skill)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with TypeScript types, request examples, checklists, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes payment-flow guidance for Base Sepolia, PayAI Echo, EVVM native pay, and Privy agentic-wallet extensions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
