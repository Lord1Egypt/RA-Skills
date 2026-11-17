## Description:

Manage Jira issues on self-hosted or enterprise Jira instances using Personal Access Tokens in SSO/SAML environments where Basic Auth fails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dejanb](https://clawhub.ai/user/dejanb)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to manage issues on trusted self-hosted or enterprise Jira instances when Personal Access Tokens are required for SSO/SAML environments. It provides guidance and shell command patterns for reading, searching, transitioning, commenting on, updating, and creating Jira issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Jira Personal Access Token can grant access to sensitive project data or issue mutation APIs.

Mitigation: Use a short-lived, least-privileged PAT and avoid exposing it in shared shells, logs, prompts, or command history.

Risk: An untrusted or incorrect Jira base URL could send the bearer token to an unintended endpoint.

Mitigation: Set JIRA_URL only to an approved HTTPS Jira base URL and run the skill only in environments where environment variables cannot be altered by untrusted code.

Risk: Transition, comment, update, and create operations can modify Jira state.

Mitigation: Review issue keys, JQL, transition IDs, and JSON payloads before executing mutating commands.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline bash, curl, and jq commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-provided JIRA_URL and JIRA_PAT environment variables; commands target Jira REST API v2.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
