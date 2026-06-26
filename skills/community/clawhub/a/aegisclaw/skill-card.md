## Description: <br>
Use this skill when the user asks to manage Binance assets, check account security, scan for arbitrage opportunities, or perform automated dust sweeps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hyy2099](https://clawhub.ai/user/hyy2099) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect Binance account security, scan idle assets and dust balances, monitor funding-rate arbitrage opportunities, execute dust sweeps, and generate account reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use live Binance credentials and its dust-sweep command can change account balances by converting assets to BNB. <br>
Mitigation: Use testnet first, run only on a dedicated low-balance sub-account, and execute dust sweeps only when the user explicitly intends to convert those assets. <br>
Risk: API secrets may be supplied through chat commands or command-line parameters in environments that retain logs. <br>
Mitigation: Prefer environment variables or a local .env file, avoid sending secrets through chat, and rotate any key that may have been exposed. <br>
Risk: Overly broad Binance API permissions can increase financial exposure if the key is misused. <br>
Mitigation: Create a least-privilege API key, disable withdrawals and futures unless explicitly needed, enable IP restrictions, and run the included security check before asset operations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hyy2099/aegisclaw) <br>
- [Publisher profile](https://clawhub.ai/user/hyy2099) <br>
- [Project homepage from metadata](https://github.com/hyy2099/aegisclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown and plain text responses with command examples, status reports, scan summaries, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call Binance APIs, persist SQLite snapshots and trade records, and return security, balance, arbitrage, dust-sweep, and weekly-report summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, target metadata, and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
