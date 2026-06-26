## Description: <br>
Free read-only market monitoring for Hyperliquid and LN Markets, including real-time prices, public balances, and positions without private keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nickymick8](https://clawhub.ai/user/nickymick8) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to monitor public crypto market data and, optionally, Hyperliquid balances and positions for a supplied public wallet address. It is intended for read-only market intelligence, not trade execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setting HYPERLIQUID_ACCOUNT_ADDRESS lets the agent and Hyperliquid API query balances and open positions for that public address. <br>
Mitigation: Set HYPERLIQUID_ACCOUNT_ADDRESS only for addresses you are comfortable monitoring through this skill. <br>
Risk: External trading offers mentioned by the artifact may be unrelated to the read-only skill and could create financial or account risk. <br>
Mitigation: Do not provide private keys or trading API secrets, and independently verify any external Claw Pro or Telegram trading offer before engaging. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nickymick8/claw-trader-lite) <br>
- [Hyperliquid Public API](https://api.hyperliquid.xyz) <br>
- [LN Markets Public API](https://api.lnmarkets.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell examples; runtime methods return numbers, dictionaries, and lists.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only HTTP requests to public market APIs; Hyperliquid balance and position lookup requires HYPERLIQUID_ACCOUNT_ADDRESS.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
