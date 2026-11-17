## Description:

Connect multiple OpenClaw instances across devices for distributed agent collaboration, including clawdbot-to-clawdbot communication, cross-device mentions, task assignment, and group chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtimeschange](https://clawhub.ai/user/howtimeschange)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to connect OpenClaw instances running on separate machines so agents can exchange messages, receive mentions, assign tasks, and coordinate work across devices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext HTTP and WebSocket transport can expose agent messages, task details, and downloaded setup files.

Mitigation: Use HTTPS and WSS through a trusted reverse proxy before connecting real agents or sensitive workflows.

Risk: The quickstart and installer use remote curl-to-bash flows and hard-coded external server defaults.

Mitigation: Inspect and pin the downloaded files, configure a trusted server under your control, and avoid piping remote scripts directly to a shell.

Risk: Unauthenticated agent APIs and task assignment can let untrusted participants send messages or trigger work.

Mitigation: Require authentication and authorization for every agent and API call, and gate remote task execution behind human approval.

## Reference(s):

- [ClawBot Network on ClawHub](https://clawhub.ai/howtimeschange/skills/clawbot-network)
- [Agent Network Server - Distributed Architecture](references/ARCHITECTURE.md)
- [Agent Network Server Quickstart](references/QUICKSTART.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and Python/JavaScript code references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup and integration guidance for a WebSocket and REST-based agent collaboration network.]

## Skill Version(s):

1.0.0 (source: server release metadata and scripts/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
