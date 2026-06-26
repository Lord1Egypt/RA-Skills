## Description: <br>
Post artwork, journals, and status updates to a user's DeviantArt account through the official DeviantArt API using OAuth 2.1 Authorization Code with PKCE, Sta.sh upload, and Sta.sh publish. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stanestane](https://clawhub.ai/user/stanestane) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to authenticate a local DeviantArt app, upload or publish local artwork, and create DeviantArt journals or status updates from an agent-assisted workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish artwork, journals, or status updates to the connected DeviantArt account. <br>
Mitigation: Require explicit user confirmation of the file path, title, body, tags, maturity settings, and destination before any posting command runs. <br>
Risk: OAuth credentials and refresh tokens are sensitive local files. <br>
Mitigation: Store token and app credential files only in private user-local paths, grant only the required scopes, and revoke the DeviantArt app token when the skill is no longer needed. <br>
Risk: Incorrect scopes, redirect URI mismatches, or API validation errors can cause failed or unintended posting attempts. <br>
Mitigation: Use the documented PKCE flow, verify the redirect URI and scopes before authentication, and use dry-run mode to review metadata before upload or publish calls. <br>


## Reference(s): <br>
- [DeviantArt API notes](references/api-notes.md) <br>
- [ClawHub publishing notes](references/clawhub-publish-notes.md) <br>
- [ClawHub release page](https://clawhub.ai/stanestane/deviantart-post) <br>
- [DeviantArt OAuth authorization endpoint](https://www.deviantart.com/oauth2/authorize) <br>
- [DeviantArt OAuth token endpoint](https://www.deviantart.com/oauth2/token) <br>
- [DeviantArt OAuth API base](https://www.deviantart.com/api/v1/oauth2) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and final DeviantArt URLs or IDs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or read local OAuth app credential and token JSON files under the user's configured path.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
