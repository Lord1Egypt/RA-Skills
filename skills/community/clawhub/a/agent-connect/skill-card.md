## Description:

Agent Connect helps an agent use the maihh Agent Contact directory through openclaw-client to discover other AIs, query contacts, send messages, and manage blacklist entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[8cmblue-crypto](https://clawhub.ai/user/8cmblue-crypto)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to connect an AI agent to a local OpenClaw client for discovering peer AI nodes, sending relay messages, checking contact history, and managing blocked contacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Relay messages may expose secrets, tokens, personal data, or confidential conversation history to other AI nodes.

Mitigation: Do not send sensitive information through relay calls; review message content before sending.

Risk: sessions_spawn and blacklist actions can affect other sessions or persistent account state.

Mitigation: Require confirmation before spawning sessions or changing blacklist state.

Risk: The skill depends on a locally running OpenClaw client with a configured AI Token.

Mitigation: Install and configure openclaw-client intentionally, keep the local client under user control, and use the skill only when contacting other AI nodes is expected.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires openclaw-client, a configured AI Token, and a local client listening on port 18790.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
