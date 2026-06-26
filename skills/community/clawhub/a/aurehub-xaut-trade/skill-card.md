## Description: <br>
Buy or sell XAUT (Tether Gold) on Ethereum using Uniswap V3 market orders or UniswapX limit orders with Foundry keystore or WDK wallet modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aure-duncan](https://clawhub.ai/user/aure-duncan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure a local wallet and execute XAUT/USDT market or limit trades on Ethereum through an agent-guided workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has local wallet-signing authority and can execute on-chain financial transactions. <br>
Mitigation: Install only after reviewing the helper scripts, keep wallet files private, and rely on the documented confirmation thresholds before approving trades. <br>
Risk: An under-documented arbitrary signing capability could authorize unintended EIP-712 payloads. <br>
Mitigation: Do not use generic signing unless the exact payload and authorization effect have been independently verified. <br>
Risk: Wallet vault, seed, or password files expose funds if disclosed or stored with weak permissions. <br>
Mitigation: Keep ~/.aurehub/.env, vault, seed, and password files private with 0600 permissions and avoid sharing or committing them. <br>
Risk: Opting into rankings can link a wallet address to a user-chosen nickname. <br>
Mitigation: Leave rankings disabled unless that identity linkage is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aure-duncan/aurehub-xaut-trade) <br>
- [README](README.md) <br>
- [Environment Initialization](references/onboarding.md) <br>
- [Wallet Modes](references/wallet-modes.md) <br>
- [Balance & Pre-flight Checks](references/balance.md) <br>
- [Quote & Slippage Protection](references/quote.md) <br>
- [Buy Execution](references/buy.md) <br>
- [Sell Execution](references/sell.md) <br>
- [Limit Order Placement](references/limit-order-buy-place.md) <br>
- [Limit Sell Order Placement](references/limit-order-sell-place.md) <br>
- [Limit Order Query](references/limit-order-status.md) <br>
- [Limit Order Cancellation](references/limit-order-cancel.md) <br>
- [Live Trading Runbook](references/live-trading-runbook.md) <br>
- [Skill Delegation](references/skill-delegation.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, configuration examples, and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute on-chain transactions after user confirmation; requires local wallet configuration and external Ethereum RPC and UniswapX services.] <br>

## Skill Version(s): <br>
2.3.0 (source: server release evidence, frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
