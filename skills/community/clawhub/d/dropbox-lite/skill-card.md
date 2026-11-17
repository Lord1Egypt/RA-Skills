## Description:

Upload, download, and manage files in Dropbox with automatic OAuth token refresh.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thekie](https://clawhub.ai/user/thekie)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and automation users use this skill to let an agent list, search, upload, download, and create folders in Dropbox from Linux, macOS, Windows, servers, or other headless environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Dropbox file read and write access, which may expose or modify Dropbox content according to the app's configured scope.

Mitigation: Prefer a Dropbox App Folder app unless whole-account access is required, and grant only the Dropbox permissions needed for the intended workflow.

Risk: Dropbox OAuth credentials, including a long-lived refresh token, are stored in a plaintext local file.

Mitigation: Restrict ~/.config/atlas to 700 and dropbox.env to 600, keep the credential file out of backups and repositories, and revoke the Dropbox app if the token file may have been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thekie/skills/dropbox-lite)
- [Dropbox Developers](https://www.dropbox.com/developers)
- [Dropbox app console](https://www.dropbox.com/developers/apps)
- [Dropbox OAuth guide](https://developers.dropbox.com/oauth-guide)
- [Dropbox API Explorer](https://dropbox.github.io/dropbox-api-v2-explorer/)
- [Dropbox API documentation](https://www.dropbox.com/developers/documentation)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text and Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include Dropbox file and folder listings, search results, transfer confirmations, account details, and setup guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
