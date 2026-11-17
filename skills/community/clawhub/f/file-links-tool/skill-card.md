## Description:

Uploads confirmed files from an agent workspace to a configured bridge server and returns a direct download or preview URL for the owner.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrbeandev](https://clawhub.ai/user/mrbeandev)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to share generated files, exported results, or selected workspace artifacts with a user by uploading a confirmed file to a configured bridge server and returning a download or preview link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected workspace files may be sent to a server or exposed through a temporary bridge.

Mitigation: Confirm the exact file and destination before each upload; prefer a user-hosted HTTPS endpoint and provide the API key through a secure secret channel.

Risk: Autonomous mode can run external bridge code and open a public tunnel.

Mitigation: Require explicit user approval before starting the server, generating or storing an API key, or opening a tunnel; treat tunnel links as temporary and public.

Risk: API keys can leak if passed in query strings or sent over plain HTTP.

Mitigation: Use the X-API-Key authorization header over HTTPS, avoid query-string keys and plain HTTP, and rotate or delete keys after temporary sessions.

## Reference(s):

- [Agent-to-Owner File Bridge on ClawHub](https://clawhub.ai/mrbeandev/skills/file-links-tool)
- [OpenClaw-File-Links-Tool GitHub Repository](https://github.com/mrbeandev/OpenClaw-File-Links-Tool)
- [API instructions](artifact/api_instructions.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls]

**Output Format:** [Markdown guidance with inline shell, Python, and HTTP examples; upload responses are JSON containing url and view_url.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a preview URL for viewable files and a raw download URL for binaries or explicit download requests.]

## Skill Version(s):

3.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
