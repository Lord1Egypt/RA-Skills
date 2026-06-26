## Description: <br>
Trade on Hyperliquid spot and perpetual futures with market orders, limit orders, leverage setting, WDK wallet support, balance checks, and USDC deposit or withdrawal flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aure-duncan](https://clawhub.ai/user/aure-duncan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect balances and place, manage, deposit, or withdraw USDC-backed Hyperliquid spot and perpetual trades through an AI assistant. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can sign transactions, place trades, and move funds from a wallet. <br>
Mitigation: Use a dedicated low-balance wallet, review transaction previews, and set confirm_trade_usd to 0 to require confirmation for every trade. <br>
Risk: Wallet address and nickname may be shared with xaue.com if activity rankings are enabled. <br>
Mitigation: Decline rankings unless sharing this data is intentional. <br>
Risk: The skill can source or modify ~/.aurehub/.env as part of setup and wallet registration behavior. <br>
Mitigation: Inspect ~/.aurehub/.env before allowing the skill to source or modify it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aure-duncan/aurehub-hyperliquid-trade) <br>
- [Hyperliquid](https://hyperliquid.xyz) <br>
- [Hyperliquid app](https://app.hyperliquid.xyz) <br>
- [Hyperliquid API endpoint](https://api.hyperliquid.xyz) <br>
- [Balance](references/balance.md) <br>
- [Limit Order Flow](references/limit-order.md) <br>
- [Onboarding](references/onboarding.md) <br>
- [Perp Trade](references/perp-trade.md) <br>
- [Spot Trade](references/spot-trade.md) <br>
- [Wallet Modes](references/wallet-modes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and structured JSON parsing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js >= 20.19.0, WDK wallet vault files, Hyperliquid configuration, and explicit confirmation thresholds for higher-risk operations.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
