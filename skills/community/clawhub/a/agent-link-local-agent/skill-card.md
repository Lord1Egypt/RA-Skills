## Description:

Agent Link Local Agent helps OpenClaw agents connect to a relay server to send and receive cross-device messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericshpych](https://clawhub.ai/user/ericshpych)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure a local OpenClaw agent client for relay-based communication with agents on other devices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The relay-based client may expose messages or metadata if used with an untrusted relay.

Mitigation: Use only a relay you control or trust, and prefer wss:// with valid TLS.

Risk: Sensitive message contents may be visible to relay infrastructure because the guidance does not establish end-to-end encryption.

Mitigation: Avoid sending sensitive content unless end-to-end encryption is added.

Risk: Shared secrets can be exposed through shell history or world-readable configuration files.

Mitigation: Store shared secrets outside shell history and world-readable files.

Risk: Inbound agent messages may be spoofed or replayed if signature verification and replay prevention are incomplete.

Mitigation: Treat inbound agent messages as untrusted unless the client is updated to verify signatures and prevent replay.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ericshpych/skills/agent-link-local-agent)
- [Publisher profile](https://clawhub.ai/user/ericshpych)
- [README](artifact/README.md)
- [Local Agent installation guide](artifact/docs/install-agent.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python examples, shell commands, and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance is oriented around a local WebSocket relay client and configuration file.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
