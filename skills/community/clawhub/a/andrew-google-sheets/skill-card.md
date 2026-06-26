## Description: <br>
Helps an agent set up OAuth 2.0 access and use the Google Sheets API to read, write, append, clear, create, and list spreadsheets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ibluewind](https://clawhub.ai/user/ibluewind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to connect an agent to Google Sheets for spreadsheet lookup, data entry, updates, creation, and range management through Google APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires OAuth access that can read, write, create, and list spreadsheet data in the user's Google account. <br>
Mitigation: Install only when that Google Sheets access is acceptable, review requested sheet operations before execution, and revoke the Google authorization when the skill is no longer needed. <br>
Risk: The skill stores local OAuth credentials and token files. <br>
Mitigation: Keep ~/.google-credentials.json and ~/.google-sheets-token.pickle private, exclude them from source control, and remove the token file to force reauthorization after credential changes. <br>
Risk: Spreadsheet search and setup can expose spreadsheet names, IDs, and metadata to the local agent session. <br>
Mitigation: Avoid using accounts containing unrelated sensitive spreadsheets, and verify spreadsheet IDs and ranges before read, write, clear, or append operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ibluewind/andrew-google-sheets) <br>
- [Google Sheets OAuth scope](https://www.googleapis.com/auth/spreadsheets) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, read, update, append, clear, list, and format Google Sheets data when invoked with authorized OAuth credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
