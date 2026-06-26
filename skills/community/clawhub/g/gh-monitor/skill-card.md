## Description: <br>
GitHub repo monitoring that helps track issues, pull requests, CI runs, new activity, label filters, and notifications through cron or messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deliverydriver](https://clawhub.ai/user/deliverydriver) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and repository maintainers use this skill to monitor GitHub repositories for issues, pull requests, CI failures, and activity that may need follow-up or scheduled alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use the agent's GitHub CLI access to inspect repository information. <br>
Mitigation: Install only when repository monitoring is intended, use explicit owner/repo names, and avoid private repositories unless access is expected. <br>
Risk: Scheduled checks can repeatedly query repositories or notify users based on cron configuration. <br>
Mitigation: Review cron schedules before enabling recurring monitoring. <br>
Risk: Alerts can send repository activity to destinations outside GitHub. <br>
Mitigation: Verify message or alert destinations before sending repository activity. <br>


## Reference(s): <br>
- [GH Commands](references/gh-commands.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/deliverydriver/gh-monitor) <br>
- [Publisher Profile](https://clawhub.ai/user/deliverydriver) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with GitHub CLI commands and monitoring guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include repository names, issue or pull request filters, CI run checks, cron schedules, and message or alert destinations.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
