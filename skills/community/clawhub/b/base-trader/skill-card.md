## Description: <br>
Autonomous crypto trading on Base via Bankr for token trading, launch monitoring, strategy execution, and portfolio management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sp0oby](https://clawhub.ai/user/sp0oby) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to guide crypto trading workflows on Base through Bankr, including portfolio checks, token research, buy and sell execution, stop losses, launch monitoring, and trade journaling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent toward real crypto trades and standing orders that may spend wallet funds. <br>
Mitigation: Use only a dedicated low-balance wallet and require explicit manual confirmation for every buy, sell, DCA, leverage, or order action. <br>
Risk: Autonomous routines such as cron, heartbeat, DCA, leverage, and standing orders can continue acting after the user stops actively monitoring them. <br>
Mitigation: Do not enable autonomous trading until spending limits, cancellation steps, alerts, and regular monitoring are configured. <br>
Risk: Launch sniping, leverage, and low-liquidity token trading can cause rapid or total capital loss. <br>
Mitigation: Keep position sizes small, define stop losses before entry, avoid high leverage, and stop trading after configured daily or consecutive-loss limits. <br>
Risk: The skill depends on a separate Bankr skill and wallet configuration whose permissions are outside this artifact. <br>
Mitigation: Inspect the Bankr skill, wallet permissions, and configured API access before installation or execution. <br>


## Reference(s): <br>
- [Base Trader ClawHub Page](https://clawhub.ai/sp0oby/base-trader) <br>
- [Automation Strategies](references/automation-strategies.md) <br>
- [Trade Execution](references/execution.md) <br>
- [Launch Sniping Guide](references/launch-sniping.md) <br>
- [Leverage Trading Guide](references/leverage-guide.md) <br>
- [Market Analysis](references/market-analysis.md) <br>
- [Market Research via Bankr](references/market-research-bankr.md) <br>
- [Risk Management](references/risk-management.md) <br>
- [Trading Strategies Deep Dive](references/strategies.md) <br>
- [Token Analysis Framework](references/token-analysis.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local trade journal and performance JSON files when the agent follows the skill's logging workflow.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
