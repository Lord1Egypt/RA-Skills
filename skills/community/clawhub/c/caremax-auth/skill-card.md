## Description:

CareMax Auth helps agents authenticate to the CareMax Health API with OAuth Device Flow and use bundled shell helpers for token-backed health-data requests, file uploads, OCR sessions, and downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kittenyang](https://clawhub.ai/user/kittenyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to connect a CareMax account, manage OAuth tokens, and run authenticated CareMax health-data workflows such as logging indicators, uploading medical files, and OCR processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use CareMax tokens to read and write health data, upload and OCR medical files, download files, and delete upload sessions.

Mitigation: Install only for trusted CareMax workflows, review the requested OAuth scope before approval, and avoid running data-changing commands unless the requested action is clear.

Risk: Command output and local credential files may expose sensitive OAuth tokens or health data.

Mitigation: Treat terminal output, logs, and ~/.caremax/credentials.json as sensitive; do not share them, and revoke or refresh credentials if exposed.

Risk: Custom base URLs can redirect authentication and health-data requests away from the normal CareMax API.

Mitigation: Use custom base URLs only for trusted local development or approved staging endpoints.

## Reference(s):

- [CareMax Auth ClawHub listing](https://clawhub.ai/kittenyang/skills/caremax-auth)
- [kittenyang publisher profile](https://clawhub.ai/user/kittenyang)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, files, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local OAuth credentials and may download files when the user runs the bundled scripts.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
