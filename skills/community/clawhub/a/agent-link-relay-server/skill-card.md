## Description:

Agent Link Relay Server helps OpenClaw instances and agents communicate across devices through a Python relay server that receives, verifies, routes, and forwards agent messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericshpych](https://clawhub.ai/user/ericshpych)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to deploy and configure a WebSocket relay for cross-device OpenClaw agent messaging. It is intended for teams that need agent-to-agent communication across machines through a shared relay service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill's security claims and deployment guidance do not match the relay implementation closely enough for sensitive agent communication.

Mitigation: Review carefully before installing and treat the current implementation as a prototype rather than a production-secure relay.

Risk: The security evidence warns against exposing the relay to the public internet or relaying sensitive agent commands without additional protections.

Mitigation: Add TLS/WSS, restrict firewall access to trusted clients, protect secrets, use per-instance credentials, bind sender identity to authenticated connections, bound replay history, and verify the registered_instances allowlist is loaded.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ericshpych/skills/agent-link-relay-server)
- [Skill definition](artifact/SKILL.md)
- [README](artifact/README.md)
- [Relay installation guide](artifact/docs/install-relay.md)
- [Relay server script](artifact/scripts/relay-server/relay_server.py)
- [Relay configuration example](artifact/scripts/relay-server/relay-config.example.json)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands, Python examples, and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and the websockets package; the OpenClaw metadata also lists python3, python, and openclaw requirements.]

## Skill Version(s):

1.0.0 (source: server release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
