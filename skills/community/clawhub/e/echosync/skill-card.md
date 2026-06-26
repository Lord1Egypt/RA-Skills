## Description: <br>
echosync.io helps users authenticate to EchoSync, manage Hyperliquid copy-trade configs, query Hyperliquid market data, and execute Hyperliquid trading actions through its helper script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ly95](https://clawhub.ai/user/ly95) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use EchoSync to sign in, inspect wallet and market state, configure Hyperliquid copy-trading, and submit Hyperliquid order, cancel, leverage, and wallet-default actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place live Hyperliquid trades and change copy-trading, leverage, wallet, and order state. <br>
Mitigation: Require explicit user confirmation before any order, cancel, leverage, wallet-default, or copy-trade change, and review all market, wallet, size, price, and slippage parameters before execution. <br>
Risk: Authentication tokens and verbose command output could expose sensitive account access if shared. <br>
Mitigation: Use the skill only on a trusted machine, do not share token output or logs, and log out when access is no longer needed. <br>
Risk: Endpoint or environment tampering could redirect sensitive requests or trading actions. <br>
Mitigation: Check endpoint-related environment variables before use and avoid running the skill in untrusted shells or modified runtime environments. <br>


## Reference(s): <br>
- [EchoSync on ClawHub](https://clawhub.ai/ly95/echosync) <br>
- [ly95 publisher profile](https://clawhub.ai/user/ly95) <br>
- [OpenClaw](https://openclaw.ai/) <br>
- [Node.js](https://nodejs.org) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and command-oriented text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include authentication status, wallet listings, market data summaries, copy-trade configuration summaries, and trading action results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; skill frontmatter reports 0.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
