## Description:

Monitors remote device online status with periodic heartbeat pings to Healthchecks.io and status checks through local state or the Healthchecks API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[houziershi](https://clawhub.ai/user/houziershi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and device operators use this skill to install and query heartbeat monitoring for macOS devices, including local service status, recent heartbeat state, and remote Healthchecks.io check status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a persistent macOS LaunchAgent that keeps running after login and repeatedly sends network heartbeat requests.

Mitigation: Install it only on devices where continuous heartbeat monitoring is intended, verify the ping URL before setup, and uninstall the LaunchAgent when monitoring is no longer needed.

Risk: Healthchecks.io ping URLs and API keys can act as monitoring secrets and may be exposed through logs, chat, shell history, or command transcripts.

Mitigation: Share only UUID portions when possible, avoid posting full ping URLs or API keys in chat, and rotate exposed URLs or keys promptly.

## Reference(s):

- [Healthchecks Setup Guide](artifact/references/healthchecks-setup.md)
- [Healthchecks.io](https://healthchecks.io/)
- [Healthchecks API Checks Endpoint](https://healthchecks.io/api/v3/checks/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands and JSON status snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include macOS LaunchAgent setup, Healthchecks.io ping/API parameters, local log paths, and state-file status fields.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
