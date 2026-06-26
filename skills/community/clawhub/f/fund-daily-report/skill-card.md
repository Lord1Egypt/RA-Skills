## Description: <br>
Generates a daily fund-market report with ranked 30-day fund performance, ETF attention proxies, industry fund-flow rankings, and stock attention rankings from Tiantian Fund and Eastmoney data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paudyyin](https://clawhub.ai/user/paudyyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and finance analysts use this skill to generate a Chinese-language daily screening report for fund rankings, fund-flow proxies, industry flows, and likely fund-related stock activity. The report is intended for market monitoring and triage, not as verified investment, subscription, redemption, or holdings-change data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports a hard-coded JQData login in the finance-reporting script. <br>
Mitigation: Remove the embedded credential, rotate it before use, and require users to provide their own credential through a secure local configuration or environment variable. <br>
Risk: The release evidence says the report can present proxy metrics as fund-flow or holding-change analysis. <br>
Mitigation: Label the generated rankings as heuristic market screening and verify any investment, fund-flow, subscription, redemption, or holding-change conclusion against authoritative data before acting. <br>
Risk: The skill contacts external market-data services and may depend on services that are delayed, blocked, or unavailable. <br>
Mitigation: Run it in an environment where external data access is expected, review dependency and network access, and treat missing or stale sections as incomplete rather than definitive. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/paudyyin/fund-daily-report) <br>
- [Publisher profile](https://clawhub.ai/user/paudyyin) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Tiantian Fund data source](https://fund.eastmoney.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text report with ranked sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language report; market data can be delayed, approximate, or unavailable when upstream services or networks block access.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
