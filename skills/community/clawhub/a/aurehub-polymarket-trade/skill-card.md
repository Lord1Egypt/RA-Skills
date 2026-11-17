## Description:

Trade on Polymarket prediction markets on Polygon, including browsing markets, checking wallet and CLOB balances, redeeming winnings, and buying or selling YES/NO shares with safety gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aure-duncan](https://clawhub.ai/user/aure-duncan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to browse Polymarket markets, inspect balances and positions, and submit or simulate prediction-market buy, sell, and redeem flows from an agent.

### Deployment Geography for Use:

Global, subject to Polymarket geographic restrictions and local legal requirements.

## Known Risks and Mitigations:

Risk: The security review flags unrelated rankings registration behavior.

Mitigation: Review or remove that registration flow before installation, and do not opt in unless the destination and data use are acceptable.

Risk: The security review flags geoblocking-bypass guidance.

Mitigation: Follow Polymarket's geographic restrictions and local legal requirements instead of using bypass guidance.

Risk: The security review flags unsafe wallet-related configuration paths.

Mitigation: Use an isolated wallet with minimal funds for testing, and validate file paths and dotenv parsing before connecting a funded wallet.

Risk: The security review flags endpoint and contract-address validation concerns.

Mitigation: Pin or independently verify authenticated endpoints and contract addresses before approving transactions.

Risk: The security review flags dependency installation control.

Mitigation: Review package.json and package-lock.json, then run dependency installation only with explicit user approval.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aure-duncan/skills/aurehub-polymarket-trade)
- [Setup Reference](references/setup.md)
- [Buy Reference](references/buy.md)
- [Sell Reference](references/sell.md)
- [Balance Reference](references/balance.md)
- [Browse Reference](references/browse.md)
- [Polygon Contract Addresses](references/contracts.md)
- [Safety Gates Reference](references/safety.md)
- [Polymarket Geoblocking FAQ](https://docs.polymarket.com/polymarket-learn/FAQ/geoblocking)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell commands, prompts, and command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute local Node.js helper scripts that call Polymarket, Polygon RPC, and related on-chain services.]

## Skill Version(s):

1.1.0 (source: server release metadata, SKILL.md frontmatter, scripts/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
