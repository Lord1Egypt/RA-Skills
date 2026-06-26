## Description: <br>
A-Stock Reporter provides real-time China A-share quotes, market briefs, historical daily reports, and optional cron-triggered trading-session updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laojun509](https://clawhub.ai/user/laojun509) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to query China A-share securities, generate market summaries, review saved historical reports, and configure scheduled trading-session updates. Outputs are informational market data and should not be treated as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled cron execution can continue producing recurring reports after initial setup. <br>
Mitigation: Enable cron only when recurring reports are needed and remove the cron entry when scheduled reporting should stop. <br>
Risk: Market reports may be mistaken for investment advice. <br>
Mitigation: Treat outputs as informational market data and verify decisions with independent financial review. <br>
Risk: A-share routing may be affected by an out-of-scope ticker in the bundled sector list. <br>
Mitigation: Review the bundled sector data and confirm ticker scope before relying on generated reports. <br>


## Reference(s): <br>
- [Strategy rules](references/rules.md) <br>
- [Sector taxonomy](references/sectors.json) <br>
- [Watchlists](references/watchlist.json) <br>
- [ClawHub release page](https://clawhub.ai/laojun509/a-stock-reporter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown-style market reports with shell command and cron examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save daily report files under assets/reports and can be scheduled with cron for recurring updates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
