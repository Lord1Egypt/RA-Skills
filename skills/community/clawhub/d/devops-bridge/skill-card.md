## Description: <br>
DevOps Bridge connects GitHub, GitHub Actions, Slack, Discord, Linear, Jira, and GitHub Issues into cross-tool workflows for CI alerts, PR review tracking, issue sync, flaky test detection, repository monitoring, and daily development summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ariktulcha](https://clawhub.ai/user/ariktulcha) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to monitor repositories, analyze CI status, coordinate PR reviews, sync linked issues, and send context-rich updates across developer tools and team channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can monitor broad developer systems and team channels. <br>
Mitigation: Limit access to specific repositories, projects, and channels, and use least-privilege credentials. <br>
Risk: The skill can post notifications, update tickets, rerun CI, merge pull requests, or otherwise affect external developer systems. <br>
Mitigation: Require user approval before ticket updates, comments, CI reruns, merges, or outbound messages. <br>
Risk: Workspace memory and cron schedules may persist team mappings or recurring operational checks. <br>
Mitigation: Periodically review stored workspace memory and configured schedules. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/ariktulcha/devops-bridge) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/ariktulcha) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and structured text with optional JSON configuration snippets and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or compose notifications, summaries, issue updates, cron schedules, and repository or team-channel configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
