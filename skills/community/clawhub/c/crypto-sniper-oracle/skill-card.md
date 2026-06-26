## Description: <br>
Institutional-grade quantitative market oracle with Order Book Imbalance (OBI), VWAP analysis, automated reports, and Telegram alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[georges91560](https://clawhub.ai/user/georges91560) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, analysts, and crypto-market operators use this skill to fetch public Binance market data, calculate OBI, VWAP, and liquidity signals, and generate local or optional Telegram-delivered reports. The skill is for market analysis and reporting; it does not place trades or access private exchange data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes public Binance API calls and writes local cache, report, and log files under /workspace. <br>
Mitigation: Install only if public market-data requests and local report storage are acceptable; review generated files and workspace paths before scheduled use. <br>
Risk: Optional Telegram delivery sends generated market reports off-host using user-provided bot credentials. <br>
Mitigation: Keep Telegram disabled unless off-host delivery is intended, store bot tokens carefully, and rotate credentials if they are exposed. <br>
Risk: Optional cron jobs can keep market monitoring and report delivery running after setup. <br>
Mitigation: Review cron entries before enabling automation and remove them when scheduled monitoring is no longer wanted. <br>
Risk: Generated market reports may contain suggested actions based on quantitative signals. <br>
Mitigation: Treat reports as analysis inputs, not autonomous trading instructions, and require human review before financial decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/georges91560/crypto-sniper-oracle) <br>
- [Project repository](https://github.com/georges91560/crypto-sniper-oracle) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Text, Files] <br>
**Output Format:** [JSON market snapshots, Markdown reports and logs, terminal text, and optional Telegram Markdown messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches public Binance market data, writes local cache, report, and log files under /workspace, and optionally sends reports to a user-configured Telegram chat.] <br>

## Skill Version(s): <br>
3.3.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
