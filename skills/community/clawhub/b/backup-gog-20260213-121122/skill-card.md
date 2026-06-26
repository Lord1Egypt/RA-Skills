## Description: <br>
Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jacobo-create](https://clawhub.ai/user/jacobo-create) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and power users use this skill to run Google Workspace CLI workflows for mail, calendar, Drive, contacts, spreadsheets, and documents after OAuth setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The external gog CLI and Homebrew tap are outside this skill and must be trusted before installation. <br>
Mitigation: Install only after reviewing and trusting the external CLI and tap used by the release metadata. <br>
Risk: Commands can read or change sensitive Google Workspace data, including mail, calendar events, Drive files, contacts, documents, and spreadsheet values. <br>
Mitigation: Use the least-privileged Google account and services needed, and review commands before sending mail, creating events, exporting documents, or updating, appending, or clearing spreadsheet data. <br>


## Reference(s): <br>
- [gog CLI homepage](https://gogcli.sh) <br>
- [ClawHub skill page](https://clawhub.ai/jacobo-create/backup-gog-20260213-121122) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the external gog CLI, OAuth credentials, and access to the selected Google Workspace services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
