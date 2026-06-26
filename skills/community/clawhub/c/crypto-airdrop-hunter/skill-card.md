## Description: <br>
Automated crypto airdrop discovery and daily market analysis. Finds high-funding projects, tracks market structure, support/resistance, and macro news. No API keys required. Self-contained -- no external dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ismaonezain](https://clawhub.ai/user/ismaonezain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and crypto market watchers use this skill to generate local market summaries, support/resistance alerts, and candidate airdrop reports from configured project and market data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can present hard-coded or mock crypto information as automated market and airdrop analysis. <br>
Mitigation: Treat generated market levels, macro headlines, and airdrop opportunities as unverified sample content unless the author replaces mock/static data with clearly sourced live feeds. <br>
Risk: Users might rely on the reports for trading or on-chain activity without wallet safety guidance. <br>
Mitigation: Review report content before acting, add explicit source citations and wallet safety guidance, and avoid treating outputs as financial advice. <br>
Risk: If scheduled automation is enabled, scripts can continue writing local reports until the schedule is removed. <br>
Mitigation: Monitor scheduled runs and remove or disable cron entries when ongoing report generation is no longer wanted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ismaonezain/crypto-airdrop-hunter) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/ismaonezain) <br>
- [CoinGecko API endpoint used for market data](https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports and terminal text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local report files under the skill directory when report scripts are run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
