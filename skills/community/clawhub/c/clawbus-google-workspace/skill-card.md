## Description:

Manage Google Calendar, Google Drive, and Google Sheets through MyBrandMetrics-connected Google data sources and the local Google Workspace CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawbus](https://clawhub.ai/user/clawbus)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, developers, and operations teams use this skill to manage Google Calendar events, Google Sheets data, and Google Drive files through MyBrandMetrics-managed Google connections and a local Google Workspace CLI wrapper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles credentials and access tokens for Google Workspace workflows.

Mitigation: Use only trusted installations, keep the API key private, restrict permissions on the API key file, and set GWS_TOKEN_URL only to the official HTTPS token service.

Risk: Calendar, Drive, and Sheets actions can modify or delete user data and sharing permissions.

Mitigation: Require explicit user confirmation before delete, trash, move, overwrite, or sharing-permission changes.

Risk: The security verdict flags the release as suspicious because scoping and guardrail detail are limited.

Mitigation: Review the skill before installing and connect only the Google data sources needed for the intended workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawbus/skills/clawbus-google-workspace)
- [clawbus website](https://www.clawbus.com/)
- [MyBrandMetrics API](https://mybrandmetrics.com/)
- [Google Workspace CLI releases API](https://api.github.com/repos/googleworkspace/cli/releases/latest)
- [Google Workspace CLI release download](https://github.com/googleworkspace/cli/releases/download/${VERSION}/${FILENAME})

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON command parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke local CLI commands that read credentials, request Google access tokens, and perform Calendar, Sheets, or Drive actions.]

## Skill Version(s):

1.2.10 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
