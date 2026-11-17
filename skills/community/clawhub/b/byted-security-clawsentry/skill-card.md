## Description:

Installs and configures OpenClaw security plugins, including the ai-assistant-security-openclaw plugins, for an OpenClaw environment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to install and configure security-related OpenClaw plugins and complete the login and enablement flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run local Node.js code, install executable OpenClaw plugin code from an unpinned package, alter OpenClaw configuration, run a detached polling process, and restart the OpenClaw gateway.

Mitigation: Install only in trusted OpenClaw environments after reviewing the skill and approving local command and configuration changes; prefer a release that pins package versions.

Risk: The skill contacts a remote Volcengine or Omni Shield service, uses device fingerprinting, and stores login state and API credentials.

Mitigation: Use only if the publisher and remote service are trusted, obtain explicit user consent for authentication and device fingerprinting, and protect or rotate stored credentials as needed.

Risk: Server security evidence marks the release as suspicious because authentication, credential persistence, background polling, and risky local changes are under-disclosed.

Mitigation: Treat the release as requiring heightened review before deployment and monitor the installation process and resulting OpenClaw security plugin state.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/volcengine-skills/skills/byted-security-clawsentry)
- [Volcengine Official Site](https://www.volcengine.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands and a login URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local configuration changes, login state, and instructions for post-login monitoring.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
