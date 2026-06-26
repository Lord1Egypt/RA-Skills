## Description: <br>
Chinese mutual fund intelligent advisor with real-time valuation, buy/sell suggestions, profit tracking, SIP planning, OCR recognition, and stock-fund linkage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangepier-crypto](https://clawhub.ai/user/tangepier-crypto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and finance-focused agent operators use Fund Keeper to track Chinese mutual fund portfolios, review valuations and profit/loss, manage SIP plans and alerts, and generate informational buy/sell suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores portfolio amounts and transaction history in local funds files. <br>
Mitigation: Use it only in workspaces where local portfolio records are acceptable, and avoid sharing generated funds files without review. <br>
Risk: OCR inputs can contain account or portfolio details from screenshots. <br>
Mitigation: Crop or redact screenshots before OCR so only the fund data needed for the task is exposed. <br>
Risk: Some market data is fetched over unencrypted HTTP and may be stale or tampered with. <br>
Mitigation: Treat valuations and buy/sell suggestions as informational and verify material decisions against trusted financial sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tangepier-crypto/fund-keeper) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>
- [INSTALL.md](artifact/INSTALL.md) <br>
- [CHANGELOG_v2.4.md](artifact/CHANGELOG_v2.4.md) <br>
- [TTJJ real-time valuation endpoint](http://fundgz.1234567.com.cn/js/{fund_code}.js) <br>
- [EastMoney fund page](http://fund.eastmoney.com/{fund_code}.html) <br>
- [EastMoney fund page by code](https://fund.eastmoney.com/{code}.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and command-oriented guidance with local portfolio and configuration file examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and write local funds/*.json and funds/*.md records and may fetch public market data from declared finance domains when network access is available.] <br>

## Skill Version(s): <br>
2.6.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
