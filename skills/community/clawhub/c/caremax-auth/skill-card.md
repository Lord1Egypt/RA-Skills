## Description: <br>
OAuth Device Flow authentication for the CareMax Health API, used by CareMax skills to obtain and refresh local tokens for health-data API access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kittenyang](https://clawhub.ai/user/kittenyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to authenticate against CareMax and support related CareMax workflows for reading health indicators, querying records, uploading medical files, running OCR, and saving reviewed reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive health data and can read, upload, download, OCR, write, and delete medical records. <br>
Mitigation: Install only in trusted environments, review requested actions before execution, and require explicit user confirmation before uploads, downloads, writes, or deletes. <br>
Risk: The authentication flow stores reusable local tokens and may expose tokens in command output. <br>
Mitigation: Protect the local credentials file with strict file permissions, avoid sharing logs that contain token output, and prefer releases that redact tokens. <br>
Risk: Automatic authentication and token refresh can grant broad API access without repeated user prompts. <br>
Mitigation: Use least-privilege accounts where possible, review OAuth scopes before approval, and revoke tokens when the skill is no longer needed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local OAuth credentials and CareMax API responses; OCR progress is emitted as JSON lines.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
