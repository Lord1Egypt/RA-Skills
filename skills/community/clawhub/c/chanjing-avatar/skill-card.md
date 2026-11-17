## Description:

Use Chanjing Avatar API for lip-syncing video generation by uploading audio or video, creating tasks, and polling for results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binkes](https://clawhub.ai/user/binkes)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to create digital avatar lip-sync videos from text or uploaded audio and video media through Chanjing's Avatar Open API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential-bearing requests can be redirected if CHANJING_OPENAPI_BASE_URL or CHANJING_API_BASE is set to an untrusted endpoint.

Mitigation: Leave those variables unset or set them only to the legitimate Chanjing API before running the skill.

Risk: Chanjing credentials and access tokens are stored in ~/.chanjing/credentials.json or the configured credentials directory.

Mitigation: Protect the credentials file with owner-only permissions and do not commit credentials.json to version control.

Risk: Uploaded audio, video, and text leave the local machine for Chanjing processing.

Mitigation: Use only media and text that are approved for third-party processing.

## Reference(s):

- [Chanjing API Documentation](https://doc.chanjing.cc)
- [Chanjing File Management API](https://doc.chanjing.cc/api/file/file-management.html)
- [Chanjing Avatar on ClawHub](https://clawhub.ai/binkes/skills/chanjing-avatar)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, API calls, JSON, Text]

**Output Format:** [Markdown guidance with shell commands and JSON API examples; scripts print JSON, file IDs, task IDs, or result URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Chanjing credentials from credentials.json and may upload user-provided media to Chanjing for processing.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
