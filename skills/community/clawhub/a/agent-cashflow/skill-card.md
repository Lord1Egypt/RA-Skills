## Description: <br>
Agent Cashflow tracks ClawHub publisher installs, downloads, stars, and optional ETH wallet balance using live API data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[infectit007](https://clawhub.ai/user/infectit007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ClawHub publishers use this skill to produce cashflow-style portfolio snapshots from ClawHub stats and optional Ethereum wallet data. It is also intended for agents that add a verified cashflow section to a daily briefing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional ETH tracking sends a public wallet address to listed RPC providers. <br>
Mitigation: Enable ETH tracking only when users are comfortable sharing the public wallet address with those providers. <br>
Risk: Cashflow reports may be routed to Telegram or memory, retaining or sharing financial and wallet-related data. <br>
Mitigation: Avoid Telegram or memory destinations unless that retention and sharing is intended. <br>
Risk: The artifact includes multi-account self-starring advice that the security guidance flags for review. <br>
Mitigation: Ignore the multi-account self-starring advice and follow platform rules for promotion. <br>


## Reference(s): <br>
- [Agent Cashflow on ClawHub](https://clawhub.ai/infectit007/agent-cashflow) <br>
- [infectit007 publisher profile](https://clawhub.ai/user/infectit007) <br>
- [LlamaRPC Ethereum endpoint](https://eth.llamarpc.com) <br>
- [Ankr Ethereum endpoint](https://rpc.ankr.com/eth) <br>
- [CoinGecko Ethereum price API](https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline JSON, Python, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports live values when APIs are available and reports unavailable data instead of fabricating figures.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
