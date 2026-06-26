## Description: <br>
Generates pre-market, intraday, and post-market China A-share market review reports using Tushare, AKShare, and search fallback data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kooui](https://clawhub.ai/user/kooui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and market-monitoring teams use this skill to generate daily China A-share briefings and recaps covering indices, sentiment, capital flows, sector rotation, and limit-up activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring A-share reports may be delivered automatically to linked messaging channels after installation. <br>
Mitigation: Confirm the destination channels before use and disable or pause auto-push tasks when recurring delivery is not desired. <br>
Risk: Generated financial commentary may include hardcoded or stale claims that appear current. <br>
Mitigation: Verify market data and narrative claims against live sources before acting on a report, and treat reports as informational rather than investment advice. <br>
Risk: The skill uses a user-provided Tushare token for primary data access. <br>
Mitigation: Store the token locally, avoid sharing it in prompts or logs, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kooui/china-stocks-daily-review) <br>
- [Publisher profile](https://clawhub.ai/user/kooui) <br>
- [README](artifact/README.md) <br>
- [Report template](artifact/report_template.md) <br>
- [Tushare Pro token page](https://tushare.pro/user/token) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Plain-text or Markdown market reports, generated report files, setup commands, and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write dated report_YYYYMMDD_*.md files and fetch_data.json; reports may be pushed to linked messaging channels when automation is enabled.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
