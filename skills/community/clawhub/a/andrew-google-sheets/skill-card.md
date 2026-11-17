## Description:

Andrew Google Sheets helps an agent set up OAuth 2.0 access and use the Google Sheets API to list, read, write, append, clear, create, and inspect spreadsheets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ibluewind](https://clawhub.ai/user/ibluewind)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to connect an agent to Google Sheets through OAuth, then read, update, append, clear, create, and list spreadsheets from scripted workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local OAuth token storage uses pickle loading, which can execute code if the token file is tampered with.

Mitigation: Replace pickle token storage with Google's JSON credential serialization before use and protect local credential files.

Risk: The skill requests broad Google Sheets access and can write, append, clear, or overwrite spreadsheet ranges.

Mitigation: Use a dedicated Google account or least-privilege workspace, review target spreadsheet IDs and ranges, and require explicit confirmation before destructive writes or clears.

Risk: Runtime dependencies are installed from package indexes and are not pinned by the artifact.

Mitigation: Pin and review dependencies in a dedicated virtual environment before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ibluewind/skills/andrew-google-sheets)
- [Google Sheets OAuth scope](https://www.googleapis.com/auth/spreadsheets)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Google OAuth credentials and stores a local Sheets token.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
