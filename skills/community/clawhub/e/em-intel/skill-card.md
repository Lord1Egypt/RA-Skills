## Description: <br>
Engineering Manager Intelligence tracks team performance, engineer contributions, and project health across GitLab or GitHub and Jira or GitHub Issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[larryfang](https://clawhub.ai/user/larryfang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Engineering managers and technical leads use this skill to generate morning briefs, end-of-day reviews, team reports, quiet-engineer alerts, epic health checks, contribution maps, and weekly newsletters from code and ticket-system activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores engineering platform, ticket-system, SMTP, Slack, or Telegram credentials in a generated .env file. <br>
Mitigation: Use narrowly scoped read-only tokens where possible, protect and exclude the .env file from source control, and review generated configuration before running live commands. <br>
Risk: The setup and launcher paths may install dependencies automatically. <br>
Mitigation: Review the setup flow and requirements before execution, and run inside a virtual environment or container. <br>
Risk: Generated reports may contain sensitive engineering activity or project-health information and can be sent to chat or email destinations. <br>
Mitigation: Verify Slack webhook, Telegram chat, SMTP recipient, and project scope settings, then test with dry-run or print delivery before sending reports. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/larryfang/em-intel) <br>
- [Setup guide](artifact/SETUP.md) <br>
- [Skill source](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or terminal text with optional delivery to Slack, Telegram, email, or stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports dry-run mode with synthetic data and configured live API calls for GitLab, GitHub, Jira, and GitHub Issues.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
