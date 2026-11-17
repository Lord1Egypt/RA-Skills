## Description:

ClawEmail gives agents Google Workspace access across Gmail, Drive, Docs, Sheets, Slides, Calendar, and Forms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cto1](https://clawhub.ai/user/cto1)

### License/Terms of Use:


## Use Case:

Employees, external users, and developers can use this skill to let an agent search and send Gmail, manage Drive files, edit Google Docs, Sheets, and Slides, schedule Calendar events, and create or inspect Forms using ClawEmail credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate on a live Google Workspace account with broad read, write, share, send, and delete capability.

Mitigation: Use only credentials approved for this workflow and confirm every send, share, delete, or update action before execution.

Risk: OAuth access tokens are cached locally.

Mitigation: Restrict permissions on both the credentials file and token cache, and revoke or rotate credentials if either location is exposed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cto1/skills/claw)
- [ClawEmail Credentials and OAuth Setup](https://clawemail.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, curl examples, and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLAWEMAIL_CREDENTIALS and a cached Google OAuth access token.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
