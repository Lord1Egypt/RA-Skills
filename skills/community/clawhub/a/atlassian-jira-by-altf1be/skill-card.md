## Description:

Atlassian Jira Cloud CRUD skill - manage issues, comments, attachments, workflow transitions, and JQL search via Jira REST API v3 with email and API token auth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abdelkrim](https://clawhub.ai/user/abdelkrim)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to manage Jira Cloud issues, comments, attachments, workflow transitions, and JQL searches from an agent-assisted command workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Jira API credentials and issue data can be sent to an untrusted or plaintext host if JIRA_HOST is configured unsafely.

Mitigation: Set JIRA_HOST only to a trusted Jira Cloud tenant such as yourtenant.atlassian.net, avoid http:// URLs, and review configuration before use.

Risk: The skill can create, modify, transition, and delete Jira content.

Mitigation: Use a least-privilege Jira API token, rotate it as needed, and review commands before running destructive operations.

Risk: Attachment commands can upload files passed by the user.

Mitigation: Upload only intended files and keep JIRA_MAX_FILE_SIZE set to an appropriate limit.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abdelkrim/skills/atlassian-jira-by-altf1be)
- [Atlassian API tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
- [Atlassian Jira Cloud](https://www.atlassian.com/software/jira)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Jira host, email, and API token environment variables; optional settings include default project, max results, and max file size.]

## Skill Version(s):

1.1.3 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
