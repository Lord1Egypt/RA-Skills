## Description:

Read-only Dropbox integration for browsing, searching, and downloading files from your Dropbox account. Includes automatic OAuth token refresh, secure credential storage, and comprehensive setup guide. Perfect for accessing your Dropbox files from OpenClaw without giving write access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tirandagan](https://clawhub.ai/user/tirandagan)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to connect an agent workflow to their Dropbox account for read-only browsing, searching, and local downloading of files through OAuth-authenticated command-line scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dropbox credentials and refresh tokens are stored locally and can preserve read access if exposed.

Mitigation: Keep credentials.json and token.json out of source control and backups, set restrictive file permissions, and revoke the Dropbox app immediately if either file is exposed.

Risk: Full Dropbox access can expose a broad set of files even when the configured scopes are read-only.

Mitigation: Use Dropbox App Folder access instead of Full Dropbox where possible and enable only the documented read-only scopes.

## Reference(s):

- [Setup Guide](references/setup-guide.md)
- [Dropbox API Documentation](https://www.dropbox.com/developers/documentation)
- [Dropbox OAuth 2.0 Guide](https://www.dropbox.com/developers/reference/oauth-guide)
- [Dropbox JavaScript SDK Reference](https://dropbox.github.io/dropbox-sdk-js/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, code]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and JavaScript helper code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces command-line output for Dropbox browse, search, download, OAuth setup, and connection-test workflows.]

## Skill Version(s):

1.0.1 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
