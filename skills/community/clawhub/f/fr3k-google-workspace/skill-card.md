## Description:

Google Workspace automation for Gmail, Calendar, Drive, and Sheets via service account or OAuth, enabling agents to read, write, send, and manage Google Workspace resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fr3kstyle](https://clawhub.ai/user/fr3kstyle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to operate Gmail, Google Calendar, Google Drive, and Google Sheets from command-line workflows. It supports reading and sending email, managing calendar events, listing, uploading, downloading, and sharing Drive files, and reading, writing, or appending Sheets data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can receive broad Google Workspace access through service-account or OAuth credentials.

Mitigation: Use a dedicated least-privilege account, grant only required scopes, and avoid domain-wide delegation unless it is necessary.

Risk: OAuth token files or service-account JSON can expose mailbox, calendar, Drive, and Sheets access if the machine or file is compromised.

Mitigation: Store credentials and token files in private directories, restrict filesystem permissions, and revoke tokens or rotate keys after suspected exposure.

Risk: Commands can send email, delete calendar events, change Sheets, or make Drive files publicly accessible.

Mitigation: Review command arguments before execution, especially email sending, calendar deletion, Sheets writes, and Drive public-sharing operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fr3kstyle/skills/fr3k-google-workspace)
- [Publisher profile](https://clawhub.ai/user/fr3kstyle)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Google Workspace credentials and Google API Python client libraries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
