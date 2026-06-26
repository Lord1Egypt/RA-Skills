## Description: <br>
Anchored VWAP Scalper automates BTC-USD scalping on Lighter DEX using anchored VWAP, RSI, MACD, ATR, and volume-based trading signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidm413](https://clawhub.ai/user/davidm413) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to configure and run an automated BTC scalping agent for Lighter DEX, starting in dry-run mode before any live trading. It is intended for users who understand crypto trading risk and can review strategy behavior before funding an account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real BTC market, stop, and limit orders when dry-run mode is disabled. <br>
Mitigation: Keep DRY_RUN=true until the strategy has been reviewed and tested, and enable live trading only after accepting the possibility of automatic financial loss. <br>
Risk: Live trading uses Lighter API credentials and account funds. <br>
Mitigation: Use a dedicated Lighter account with minimal funds and restricted permissions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davidm413/anchored-vwap-scalper) <br>
- [Publisher profile](https://clawhub.ai/user/davidm413) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with command names, environment variable configuration, and Python trading scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, ccxt-mcp, Lighter API credentials, and DRY_RUN configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter states 1.6.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
