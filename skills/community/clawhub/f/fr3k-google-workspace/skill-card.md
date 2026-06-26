## Description: <br>
Google Workspace automation for Gmail, Calendar, Drive, and Sheets via service account or OAuth credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fr3kstyle](https://clawhub.ai/user/fr3kstyle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation operators use this skill to run command-line workflows across Gmail, Google Calendar, Google Drive, and Google Sheets for inbox review, email sending, event management, file operations, sharing, and spreadsheet updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access and modify Gmail, Drive, Calendar, and Sheets data with broad Google scopes. <br>
Mitigation: Use the narrowest possible Google scopes, avoid domain-wide delegation unless an administrator has approved it, and install only where this level of workspace access is intended. <br>
Risk: The skill can send email, delete calendar events, publicly share Drive files, and change spreadsheets. <br>
Mitigation: Require manual confirmation before destructive, public-sharing, or external-message actions. <br>
Risk: Service-account keys and OAuth tokens grant access to sensitive Google Workspace data. <br>
Mitigation: Store credentials and token files securely, restrict filesystem permissions, and rotate credentials if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fr3kstyle/fr3k-google-workspace) <br>
- [Publisher profile](https://clawhub.ai/user/fr3kstyle) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown instructions with bash examples and JSON CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Google credentials, enabled Google APIs, and Google API Python client libraries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
