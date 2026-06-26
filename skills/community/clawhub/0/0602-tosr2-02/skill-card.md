## Description: <br>
Analyze stocks and cryptocurrencies using Yahoo Finance data, including portfolio tracking, watchlist alerts, dividend analysis, 8-dimension stock scoring, Hot Scanner trend detection, and rumor or early-signal detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run stock and cryptocurrency analysis, compare assets, monitor portfolios and watchlists, review dividend metrics, and scan for trending or early market signals. Outputs are informational and should not be treated as financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional Twitter/X scanning handles sensitive session credentials. <br>
Mitigation: Review before enabling social scanning, avoid personal account session cookies, keep AUTH_TOKEN and CT0 out of shared files, logs, and source control, and use the documented no-social mode when social data is not required. <br>
Risk: Market analysis outputs could be mistaken for investment advice. <br>
Mitigation: Keep the documented not-financial-advice disclaimer visible and require users to consult qualified financial professionals before making investment decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yinwuzhe/0602-tosr2-02) <br>
- [Publisher profile](https://clawhub.ai/user/yinwuzhe) <br>
- [Yahoo Finance](https://finance.yahoo.com) <br>
- [Usage Guide](docs/USAGE.md) <br>
- [Technical Architecture](docs/ARCHITECTURE.md) <br>
- [Hot Scanner](docs/HOT_SCANNER.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text reports and optional JSON output with markdown documentation examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv for documented command execution; optional Twitter/X scanning can be avoided with no-social mode.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact skill version 6.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
