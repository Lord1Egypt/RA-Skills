## Description: <br>
Manage Jira issues, transitions, and worklogs via the Jira Cloud REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kyjus25](https://clawhub.ai/user/kyjus25) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and teams using Jira Cloud use this skill to search issues, view details, create tasks, update status, assign users, add comments, and review worklogs from an agent shell workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Jira API token and can make persistent issue, comment, assignment, transition, and worklog changes. <br>
Mitigation: Use a least-privilege Jira account or token, set JIRA_BOARD where practical, and review mutating commands before execution. <br>
Risk: Jira searches and worklog commands can expose project data to the agent workflow. <br>
Mitigation: Run the skill only in trusted sessions and limit token and project access to Jira data the agent is allowed to use. <br>


## Reference(s): <br>
- [Jira Cloud REST API v3 documentation](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/) <br>
- [Atlassian API token setup](https://id.atlassian.com/manage-profile/security/api-tokens) <br>
- [ClawHub skill page](https://clawhub.ai/kyjus25/clawdbot-jira-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples; command results are plain text or JSON for worklog summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, bc, python3, JIRA_URL, JIRA_EMAIL, and JIRA_API_TOKEN; JIRA_BOARD is optional for project scoping.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
