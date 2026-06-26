## Description: <br>
Google Workspace via ClawEmail.com service — Gmail, Drive, Docs, Sheets, Slides, Calendar, Forms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cto1](https://clawhub.ai/user/cto1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent developers use this skill to let an agent operate Google Workspace services through ClawEmail.com, including email, files, documents, spreadsheets, presentations, calendars, and forms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad Google Workspace access can expose or modify email, files, documents, calendars, and forms. <br>
Mitigation: Use a dedicated or least-privilege Google account and install only when the publisher and ClawEmail.com are trusted with that access. <br>
Risk: Agent actions such as sending email, sharing files, exporting private content, editing documents, clearing sheets, or deleting files/events can have user-visible or destructive effects. <br>
Mitigation: Require manual review and explicit approval before allowing the agent to perform write, share, export, send, or delete operations. <br>
Risk: Credential files and cached OAuth tokens can grant access outside the immediate agent session. <br>
Mitigation: Protect the credentials file and token cache with appropriate filesystem permissions and rotate credentials if exposure is suspected. <br>


## Reference(s): <br>
- [Clawemail Skill Page](https://clawhub.ai/cto1/clawemail) <br>
- [Publisher Profile](https://clawhub.ai/user/cto1) <br>
- [ClawEmail Service](https://clawemail.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline bash, curl, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLAWEMAIL_CREDENTIALS and uses a helper script to refresh and cache Google OAuth access tokens.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
