## Description: <br>
Analyzes Binance spot markets, monitors pump signals, reports balances and positions, and can place Binance spot trades through Telegram-driven agent commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[june-kris](https://clawhub.ai/user/june-kris) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze Binance spot markets, receive Telegram pump alerts, inspect balances and positions, and optionally execute Binance spot buy/sell orders after confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use stored Binance credentials to place live spot market orders. <br>
Mitigation: Use a restricted Binance subaccount with limited funds, no withdrawal permission, and IP/API restrictions; review every order before execution. <br>
Risk: Telegram-linked background services can run continuously and may rely on auto-discovered chat IDs. <br>
Mitigation: Configure an explicit Telegram chat_id and stop pump alert or coin push services when finished. <br>
Risk: Broad triggers or pump-alert suggestions can lead to unintended trading actions. <br>
Mitigation: Keep triggers narrow, confirm coin and amount, and avoid executing trades from alerts without user review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/june-kris/binance-trade-hunter) <br>
- [Publisher profile](https://clawhub.ai/user/june-kris) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and formatted text returned by Python helpers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local configuration, call Binance and Telegram APIs, and start or stop long-running background services when requested.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release evidence; artifact frontmatter says 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
