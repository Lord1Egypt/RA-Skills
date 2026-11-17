## Description:

Manage Jira issues, transitions, and worklogs via the Jira Cloud REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyjus25](https://clawhub.ai/user/kyjus25)

### License/Terms of Use:


## Use Case:

Developers and teams who manage Jira Cloud projects use this skill to search issues, inspect issue details, transition status, assign work, create issues, add comments, and log or summarize work time from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Jira credentials may be sent to an untrusted URL in some pagination or configuration scenarios.

Mitigation: Use only a trusted HTTPS JIRA_URL, prefer a least-privilege Jira API token, and avoid worklog summary commands until pagination URLs are constrained to the configured Jira host.

Risk: Some commands modify Jira data, including status, assignment, comment, issue creation, and worklog updates.

Mitigation: Review the intended issue key, assignee, comment, status, and logged hours before running write commands.

## Reference(s):

- [ClawHub Jira Skill](https://clawhub.ai/kyjus25/skills/clawdbot-jira-skill)
- [Jira Cloud REST API v3 Documentation](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/)
- [Atlassian API Token Management](https://id.atlassian.com/manage-profile/security/api-tokens)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON outputs for worklog summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require curl, jq, bc, python3, JIRA_URL, JIRA_EMAIL, and JIRA_API_TOKEN; JIRA_BOARD can scope searches and issue creation.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
