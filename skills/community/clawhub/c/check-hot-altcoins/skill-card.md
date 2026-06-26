## Description: <br>
生成加密货币早报PDF，包含行业动态、FDV排名、热点赛道和风险提示。数据来源于CoinGecko API。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nihaovand](https://clawhub.ai/user/nihaovand) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and analysts use this skill to generate a Chinese daily cryptocurrency morning report focused on altcoin FDV rankings, hot sectors, watchlist projects, and risk reminders. The workflow fetches public CoinGecko market data, creates an HTML/PDF report, and prepares it for Feishu delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public cryptocurrency market data and may create reports from volatile or incomplete data. <br>
Mitigation: Review the generated report and confirm market figures before sharing or relying on it. <br>
Risk: The skill creates temporary local files during report generation. <br>
Mitigation: Inspect or clean temporary files after use when running in shared environments. <br>
Risk: The finished report may be sent through Feishu to an unintended recipient or chat. <br>
Mitigation: Confirm the Feishu recipient or chat before sending and avoid including private knowledge-base notes unless sharing is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nihaovand/check-hot-altcoins) <br>
- [CoinGecko coins markets API](https://api.coingecko.com/api/v3/coins/markets) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Code, Guidance] <br>
**Output Format:** [Chinese HTML/PDF report with supporting bash and Python workflow] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches public market data, writes temporary local files, and may send the finished report through Feishu.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
