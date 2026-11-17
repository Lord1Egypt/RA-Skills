## Description:

Integrates with the Emby Server API so an agent can manage media libraries, users, devices, playback, live TV, and encoding settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xusanhong](https://clawhub.ai/user/xusanhong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Emby server administrators use this skill to let an agent call Emby Server API endpoints for media library queries, user and device administration, playback control, live TV operations, downloads, and server configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad Emby server administration powers, including deletes, backup restore, authentication-key creation, uploads, downloads, environment browsing, and configuration changes.

Mitigation: Require explicit human confirmation for destructive or privileged operations and restrict use to trusted servers and intended administrative workflows.

Risk: The artifact uses an embedded example API key and a configured server URL, which can encourage weak credential handling.

Mitigation: Store a least-privileged Emby API key outside source code and restrict the configured server URL before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xusanhong/skills/emby)

## Skill Output:

**Output Type(s):** [Code, API Calls, Configuration, Guidance]

**Output Format:** [Python module functions returning JSON dictionaries, response streams, bytes, URLs, and text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a configured Emby base URL and API key; stream helpers may read from or write to local file paths.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
