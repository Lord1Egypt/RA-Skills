## Description: <br>
Stock and cryptocurrency analysis powered by Yahoo Finance data for ticker analysis, portfolio and watchlist tracking, dividend review, scoring, trend scanning, rumor detection, and SkillPay billing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elevo11](https://clawhub.ai/user/elevo11) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to generate market snapshots, stock scores, portfolio and watchlist summaries, dividend analysis, hot ticker scans, rumor or signal checks, and optional billing actions for finance workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary reports that the skill can silently install yfinance at runtime. <br>
Mitigation: Use the skill only where runtime pip installs are allowed, or preinstall and pin yfinance in the execution environment before use. <br>
Risk: The security summary reports that the billing helper can charge a SkillPay account by default when provided with a valid API key. <br>
Mitigation: Require manual approval before billing commands and provide SKILLPAY_API_KEY only in sessions where charges are intended. <br>
Risk: The security guidance notes that portfolio data may be stored in the local workspace. <br>
Mitigation: Avoid storing real portfolio data unless local workspace persistence is acceptable for the user and environment. <br>


## Reference(s): <br>
- [8-Dimension Stock Scoring Model](references/scoring-model.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with optional JSON and CSV file output from command scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some scripts can persist portfolio, watchlist, and exported batch analysis data in the local workspace.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
