## Description:

Clawemail helps agents work with Google Workspace through the ClawEmail.com service, including Gmail, Drive, Docs, Sheets, Slides, Calendar, and Forms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cto1](https://clawhub.ai/user/cto1)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to prepare authenticated Google Workspace API calls for email, files, documents, spreadsheets, presentations, calendars, and forms via ClawEmail credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill grants broad Google Workspace authority across email, Drive, documents, calendars, and forms.

Mitigation: Install only when broad workspace access is acceptable, and prefer a dedicated or least-privileged Google account.

Risk: Credential and cached access-token files could expose workspace access if stored insecurely.

Mitigation: Restrict credential and cache file permissions, and avoid using the skill on shared machines.

Risk: Agent actions can send email, share or delete Drive files, modify documents or sheets, change calendar events, or read sensitive content.

Mitigation: Require explicit confirmation before impactful or sensitive Google Workspace actions.

## Reference(s):

- [Clawemail Skill Page](https://clawhub.ai/cto1/skills/clawemail)
- [ClawEmail Service](https://clawemail.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash, curl, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLAWEMAIL_CREDENTIALS and ClawEmail Google Workspace OAuth credentials; the token helper caches access tokens for 50 minutes.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
