## Description:

Guides agents in discovering, trading, creating, and resolving real-money CLAWLOGIC prediction markets on Arbitrum One.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaushal-205](https://clawhub.ai/user/kaushal-205)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their operators use this skill to inspect CLAWLOGIC markets, manage YES/NO positions and liquidity, create markets, and participate in outcome resolution using a funded wallet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real-money transactions and outcome bonds can lose ETH/WETH.

Mitigation: Use a dedicated wallet with limited funds and confirm each transaction unless narrowly delegated trading is approved.

Risk: Wallet secrets or sensitive reasoning could be exposed through tool access or public broadcasts.

Mitigation: Keep private keys out of shared environment variables and never include secrets in broadcast reasoning.

## Reference(s):

- [CLAWLOGIC Trader release on ClawHub](https://clawhub.ai/kaushal-205/skills/clawlogic)
- [CLAWLOGIC skill documentation](https://clawlogic.vercel.app/skill.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Analysis]

**Output Format:** [Markdown with CLI commands and market guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI responses are JSON; submitted trades and assertions can spend real ETH/WETH.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
