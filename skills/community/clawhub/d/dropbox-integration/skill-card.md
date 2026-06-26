## Description: <br>
Read-only Dropbox integration for browsing, searching, and downloading files from your Dropbox account. Includes automatic OAuth token refresh, secure credential storage, and comprehensive setup guide. Perfect for accessing your Dropbox files from OpenClaw without giving write access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tirandagan](https://clawhub.ai/user/tirandagan) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to browse Dropbox folders, search Dropbox file names, and download selected files into an agent-accessible local workspace without granting Dropbox write permissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can be configured with broad Dropbox read access, including whole-account search and downloads. <br>
Mitigation: Prefer Dropbox App folder access unless whole-account read access is necessary, and grant only the documented read-only scopes. <br>
Risk: Long-lived Dropbox credentials and refresh tokens are stored locally in credentials.json and token.json. <br>
Mitigation: Keep credentials.json and token.json out of version control, restrict file permissions, and revoke or rotate the Dropbox app credentials if exposure is suspected. <br>
Risk: OAuth setup and token handling can expose sensitive values in shared or logged terminals. <br>
Mitigation: Run setup only in a trusted terminal session and avoid copying credentials or authorization output into logs or shared chats. <br>
Risk: Downloaded Dropbox files are written to local filesystem paths chosen at runtime. <br>
Mitigation: Review each download destination before execution and avoid writing into sensitive or unintended directories. <br>


## Reference(s): <br>
- [Setup Guide](references/setup-guide.md) <br>
- [Dropbox API Documentation](https://www.dropbox.com/developers/documentation) <br>
- [Dropbox OAuth 2.0 Guide](https://www.dropbox.com/developers/reference/oauth-guide) <br>
- [Dropbox JavaScript SDK Documentation](https://dropbox.github.io/dropbox-sdk-js/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and command-line text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May download Dropbox file content to user-selected local paths.] <br>

## Skill Version(s): <br>
1.0.1 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
