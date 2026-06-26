## Description: <br>
Automatically collects and summarizes recent fund and market news across US, Europe, Japan, gold, and prediction markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YonghaoZhao722](https://clawhub.ai/user/YonghaoZhao722) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Investors and research workflows can use this skill to generate a daily market-news summary for configured funds and markets, including manual requests and scheduled daily runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may run unattended and send market reports to Telegram. <br>
Mitigation: Confirm the intended Telegram recipient and schedule before enabling automatic runs. <br>
Risk: The skill may save reports under /root/clawd/obsidian-vault and perform broad Git pull, commit, and push operations. <br>
Mitigation: Review the repository origin, credentials, branch, and staged files, or require approval before any Git sync. <br>
Risk: The generated financial summaries may be incomplete, stale, or affected by third-party data source failures. <br>
Mitigation: Treat outputs as research notes and verify important market or investment information against primary sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/YonghaoZhao722/fund-news-summary) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files] <br>
**Output Format:** [Markdown-formatted market news report with bullet points and timestamps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send the report to Telegram and save a dated Markdown report before syncing a Git repository when configured.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
