## Description: <br>
Dailynewsreport fetches news from multiple sources, deduplicates and classifies items, rewrites them into concise daily report entries, and can deliver the report to Telegram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FrankLe1117](https://clawhub.ai/user/FrankLe1117) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to generate scheduled daily news briefs for broad or focused topics such as robotics, real estate, and AI. It is suited for collecting recent items, removing duplicates, ranking by relevance and freshness, and producing a Markdown report with optional Telegram delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram delivery uses shell command execution with settings-derived token and chat ID values, which could allow malformed settings to run unintended commands. <br>
Mitigation: Review before installation; replace shell-based curl execution with a native HTTP client or argument-safe execFile/spawn and strictly validate Telegram token and chat ID values. <br>
Risk: Generated reports and links may be sent to Telegram, exposing collected news selections and configured delivery destinations. <br>
Mitigation: Use test mode before enabling delivery, keep Telegram credentials scoped and secret, and confirm the intended chat or channel before scheduled runs. <br>
Risk: The security verdict is suspicious pending dependency cleanup and Telegram delivery hardening. <br>
Mitigation: Install only after reviewing the security summary and applying the recommended delivery and dependency changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/FrankLe1117/daily-news-report) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact Skill Documentation](artifact/Skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, configuration, shell commands] <br>
**Output Format:** [Markdown daily news report with categorized bullet entries and source links; command output may include logs and configuration status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are capped by the configured maximum item count and Telegram delivery truncates long messages.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata, created 2026-03-09) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
