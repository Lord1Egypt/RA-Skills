## Description: <br>
BigA analyzes China A-share stocks, maintains a dynamic stock pool of up to 30 tickers, scores technical and market signals, and produces buy, hold, reduce, and sell alert summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kobenfang](https://clawhub.ai/user/kobenfang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and investors use BigA to monitor China A-share watchlists, screen technology-oriented small- and mid-cap candidates, and receive market-open, intraday, and market-close alert summaries. The skill provides informational stock analysis and should not be treated as professional investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled scans and automatic alert delivery can post stock-analysis messages to a configured chat target without per-message confirmation. <br>
Mitigation: Review the destination channel or target and the cron schedule before installing; disable, edit, or remove recurring jobs when automatic stock-alert posting is not wanted. <br>
Risk: Broad trigger phrases may cause unintended stock scans or alert workflows in shared conversations. <br>
Mitigation: Use the skill in controlled channels, review the trigger list before enabling it, and avoid shared or public channels unless automatic stock alerts are acceptable. <br>
Risk: Buy, hold, reduce, and sell signals may be incomplete, stale, or incorrect because they depend on market data, news searches, and model-scored catalysts. <br>
Mitigation: Treat outputs as informational, keep the non-investment-advice disclaimer visible, and verify market data and catalysts independently before acting. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kobenfang/biga) <br>
- [BigA Technical Timing Score Framework](references/technical-timing-score.md) <br>
- [BigA User Preferences](references/user-preferences.md) <br>
- [Sector Analysis Framework](references/sector-matrix.md) <br>
- [Cron Templates](references/cron-templates.json) <br>
- [Cron Install Shell Template](references/cron-install-shell.sh) <br>
- [BigA Scan Script](scripts/biga-scan.py) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown alert summaries, JSON scan results, segmented chat messages, and shell commands for scheduled jobs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send segmented chat messages and create recurring cron jobs when installed; generated stock-analysis summaries include an investment-risk disclaimer.] <br>

## Skill Version(s): <br>
6.0.18 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
