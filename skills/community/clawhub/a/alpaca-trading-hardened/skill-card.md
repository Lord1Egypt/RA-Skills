## Description: <br>
Execute trades, analyze markets, and manage portfolios using the apcacli command-line tool for Alpaca's Trading API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Alpaca trading workflows from an agent, including account review, market data checks, order management, position management, and trading command preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help place real-money trades using Alpaca credentials. <br>
Mitigation: Prefer paper-trading credentials and require explicit confirmation before any live order, cancel-all, close-all, account configuration change, or automated trading workflow. <br>
Risk: Alpaca API credentials grant sensitive account access if exposed. <br>
Mitigation: Never print, echo, log, encode, or otherwise reveal APCA_API_KEY_ID or APCA_API_SECRET_KEY values; refer to credentials by variable name only. <br>
Risk: Trading account data and command output may contain sensitive financial information. <br>
Mitigation: Do not pipe apcacli output, account data, or credential values to network-transmitting commands; keep exports local unless the user separately reviews and authorizes a safe workflow. <br>
Risk: The authoritative scan verdict is suspicious because safeguards are broad for a real-money trading skill. <br>
Mitigation: Install only after reviewing the skill, verifying the apcacli package, and confirming the deployment can enforce pre-trade review and user confirmation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/alpaca-trading-hardened) <br>
- [apcacli repository](https://github.com/d-e-s-o/apcacli) <br>
- [Alpaca documentation](https://docs.alpaca.markets/) <br>
- [Alpaca API reference](https://docs.alpaca.markets/reference/) <br>
- [Alpaca paper trading dashboard](https://app.alpaca.markets/paper/dashboard/overview) <br>
- [apca crate repository](https://github.com/d-e-s-o/apca) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces trading command guidance for apcacli and should require explicit user confirmation before live, destructive, or automated trading actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
