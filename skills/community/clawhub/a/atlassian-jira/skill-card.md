## Description:

Manage Jira Cloud issues - search, create, update, comment, transition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pejovicvuk](https://clawhub.ai/user/pejovicvuk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to let an agent search, inspect, create, comment on, assign, transition, and update Jira Cloud issues through a shell wrapper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted issue text passed to create, comment, or update commands can make the shell wrapper run local code.

Mitigation: Avoid untrusted issue text until argument handling is fixed, and review proposed text before invoking mutating commands.

Risk: Create, comment, transition, assign, and update commands can change live Jira data without built-in confirmation.

Mitigation: Require explicit human confirmation for mutating commands and use a dedicated low-privilege Jira account or token.

Risk: The skill requires Jira API credentials.

Mitigation: Provide credentials through managed environment variables or secrets and scope Jira permissions to the minimum needed.

## Reference(s):

- [ClawHub Jira skill page](https://clawhub.ai/pejovicvuk/skills/atlassian-jira)
- [Atlassian API tokens](https://id.atlassian.com/manage-profile/security/api-tokens)

## Skill Output:

**Output Type(s):** [shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ATLASSIAN_URL, ATLASSIAN_EMAIL, ATLASSIAN_API_TOKEN, curl, and python3.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
