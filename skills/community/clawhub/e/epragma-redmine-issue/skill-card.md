## Description:

Read Redmine issues from any Redmine server via REST API with configurable URL and credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agelospanagiotakis](https://clawhub.ai/user/agelospanagiotakis)

### License/Terms of Use:


## Use Case:

Developers and teams use this skill to inspect and manage Redmine issues, projects, statuses, and time entries from an agent workflow. It supports reading records and making live Redmine changes such as creating issues, updating issue fields, posting comments, and adding time entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make live changes to Redmine issues and time entries using the configured API key.

Mitigation: Install it only when write access is intended, review write commands before execution, and use a dedicated least-privilege Redmine API key.

Risk: Redmine credentials and server URLs control which instance the skill can access.

Mitigation: Use HTTPS-only Redmine URLs and verify REDMINE_URL and REDMINE_API_KEY configuration before running commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agelospanagiotakis/skills/epragma-redmine-issue)
- [Publisher profile](https://clawhub.ai/user/agelospanagiotakis)
- [Publisher website](https://epragma.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown/text summaries with Redmine links and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDMINE_URL and REDMINE_API_KEY; write commands modify live Redmine data immediately.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
