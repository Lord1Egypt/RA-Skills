## Description: <br>
ClawEmail helps agents use Google Workspace services including Gmail, Drive, Docs, Sheets, Slides, Calendar, and Forms through Google APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cto1](https://clawhub.ai/user/cto1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to connect an agent to Google Workspace tasks such as email search and sending, Drive file management, document editing, spreadsheet updates, presentation changes, calendar scheduling, and form review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad Google Workspace permissions can expose or modify email, files, calendars, documents, and forms. <br>
Mitigation: Use a dedicated or least-privileged Google account, review OAuth scopes before connecting, and install only when the publisher and service are trusted. <br>
Risk: Externally visible or destructive actions such as sending email, sharing files, deleting files, calendar changes, and bulk edits may occur through API calls. <br>
Mitigation: Require explicit preview and confirmation before allowing sends, shares, deletes, calendar changes, or bulk edits. <br>
Risk: Credentials and cached OAuth tokens can grant access to the connected Google account. <br>
Mitigation: Protect the credentials file and token cache, restrict local file permissions, and rotate or revoke credentials if exposed. <br>


## Reference(s): <br>
- [ClawEmail](https://clawemail.com) <br>
- [ClawHub skill page](https://clawhub.ai/cto1/claw) <br>
- [Publisher profile](https://clawhub.ai/user/cto1) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline bash, curl, Python, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ClawEmail credentials via CLAWEMAIL_CREDENTIALS and uses a cached Google OAuth access token.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
