## Description:

A WebSocket-based agent-to-agent communication server for registering agents, routing peer messages, handling RPC calls, publishing and subscribing to channels, discovering capabilities, and delivering offline messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent engineers use this skill to run a WebSocket messaging layer for multi-agent systems. It supports local or trusted deployments where agents need registration, peer messaging, RPC-style calls, pub/sub channels, capability discovery, heartbeats, and offline message queues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unauthenticated WebSocket clients can spoof agent identities and route RPC or pub/sub payloads if the server is reachable from untrusted networks.

Mitigation: Use only for local, trusted development unless authentication, authorization, server-bound agent identities, signed messages, and TLS or equivalent transport protection are added.

Risk: Payloads and offline queues can carry sensitive data or grow without production-grade controls in the packaged release.

Mitigation: Do not send secrets through the server as packaged; add rate limits, payload and queue size limits, dependency updates, and operational monitoring before broader deployment.

## Reference(s):

- [ClawHub A2a Server Skill Page](https://clawhub.ai/yuyonghao-123/skills/a2a-server)
- [artifact/SKILL.md](artifact/SKILL.md)
- [artifact/README.md](artifact/README.md)
- [artifact/IMPLEMENTATION-NOTES.md](artifact/IMPLEMENTATION-NOTES.md)
- [WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JavaScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Node.js server and client usage guidance, environment variable configuration, API examples, and test commands.]

## Skill Version(s):

0.1.0 (source: server release metadata, package.json, artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
