## Description:

Posts artwork, journals, and status updates to a user's DeviantArt account through the official DeviantArt API using OAuth 2.1 PKCE and Sta.sh upload/publish workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stanestane](https://clawhub.ai/user/stanestane)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to authenticate a local DeviantArt app and publish local artwork files, journals, or status updates. The workflow is intended for user-approved external posting to a user's own DeviantArt account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable DeviantArt OAuth tokens are stored in a local token file without enforced private file permissions.

Mitigation: Treat the token file as a sensitive login secret, restrict file permissions manually, and use a dedicated DeviantArt developer app with only the scopes needed.

Risk: The documented artwork preview and gallery-name controls do not match the current parser behavior.

Mitigation: Review the artwork command before routine use and repair the --dry-run and --gallery-name handling before relying on preview or gallery selection workflows.

Risk: The skill can publish content to an external DeviantArt account.

Mitigation: Summarize the pending post and obtain explicit user confirmation before any upload, journal creation, status update, or publish call.

## Reference(s):

- [DeviantArt API Notes](references/api-notes.md)
- [ClawHub Publishing Notes](references/clawhub-publish-notes.md)
- [ClawHub Skill Page](https://clawhub.ai/stanestane/skills/deviantart-post)
- [DeviantArt OAuth Authorization Endpoint](https://www.deviantart.com/oauth2/authorize)
- [DeviantArt OAuth Token Endpoint](https://www.deviantart.com/oauth2/token)
- [DeviantArt OAuth API Base](https://www.deviantart.com/api/v1/oauth2)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, Text]

**Output Format:** [Markdown with inline shell commands and script output such as URLs, deviation IDs, and API response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [External posting actions require explicit user confirmation before publishing.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
