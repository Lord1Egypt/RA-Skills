## Description: <br>
An on-chain operations hub that combines BlockBeats market intelligence, Hyperliquid trading through hl1m, wallet binding, and optional autonomous trading workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eycuit](https://clawhub.ai/user/eycuit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External traders and developers use this skill to gather crypto market and news signals, configure a Hyperliquid trading wallet, execute DEX/perps commands, and optionally schedule recurring autonomous trading actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous mode can place recurring real-money trades through a scheduled workflow. <br>
Mitigation: Enable it only after reviewing hl1m, confirming wallet/API permissions, and disabling or removing the cron job when autonomous trading is not intended. <br>
Risk: Wallet and API credentials are sensitive and can expose trading authority if mishandled. <br>
Mitigation: Use scoped proxy keys instead of main wallet private keys, keep secrets in the local state file, and avoid pasting or echoing keys in chat. <br>
Risk: Missing prerequisites or incomplete wallet state can cause unsafe or failed execution attempts. <br>
Mitigation: Run the provided preflight check before trading and prefer read-only market analysis until dependencies and encrypted wallet fields are verified. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/eycuit/1m-trade) <br>
- [1M-Trade Wallet and Account Site](https://www.1m-trade.com) <br>
- [BlockBeats Pro API](https://api-pro.theblockbeats.info) <br>
- [hl1m Reference](skills/1m-trade-dex/reference.md) <br>
- [1m-trade DEX Skill](skills/1m-trade-dex/SKILL.md) <br>
- [1m-trade News Skill](skills/1m-trade-news/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API Calls] <br>
**Output Format:** [Markdown reports with inline shell commands, JSON/tool output summaries, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke local trading commands and scheduled workflows; requires configured market-data and wallet credentials.] <br>

## Skill Version(s): <br>
1.1.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
