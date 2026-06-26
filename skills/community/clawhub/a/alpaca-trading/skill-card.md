## Description: <br>
Trade stocks, ETFs, options, and crypto through Alpaca's REST API using curl-based commands, with support for account, order, position, watchlist, market data, news, screener, and corporate action workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lacymorrow](https://clawhub.ai/user/lacymorrow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent prepare Alpaca REST API calls for trading, portfolio management, and market data retrieval. It is appropriate only when the user intentionally wants an agent connected to an Alpaca brokerage account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose high-impact brokerage actions through a broad curl wrapper, including POST, PATCH, DELETE, option exercise, cancel-all, and close-all operations. <br>
Mitigation: Install only when Alpaca account access is intended, keep paper trading as the default, use restricted or paper API keys where possible, and require readback plus explicit confirmation before any state-changing command. <br>
Risk: Live trading can cause financial loss if the endpoint is changed from paper trading or if order details are wrong. <br>
Mitigation: Do not switch to the live Alpaca endpoint without explicit user confirmation, show the complete order JSON before submission, and verify symbol, side, quantity, order type, buying power, and market status. <br>
Risk: The skill handles Alpaca API credentials through environment variables. <br>
Mitigation: Keep API keys out of prompts, files, and logs; rotate keys if exposed; and prefer keys scoped to the minimum required account permissions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lacymorrow/alpaca-trading) <br>
- [Alpaca REST API Reference](references/api.md) <br>
- [Alpaca](https://alpaca.markets) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce high-impact Alpaca API calls that require user review and confirmation before execution.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
