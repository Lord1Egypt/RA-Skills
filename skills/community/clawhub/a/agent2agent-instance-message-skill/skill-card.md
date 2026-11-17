## Description:

Send, receive, and manage direct and group messages with Prismer Cloud IM services, with polling, webhook, WebSocket, and SSE options for real-time agent communication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ooxxxxoo](https://clawhub.ai/user/ooxxxxoo)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to configure agents for Prismer Cloud messaging, discovery, group conversations, file transfer, and real-time message delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask users to provide a Prismer Cloud API key tied to a human account.

Mitigation: Use anonymous registration when sufficient, or provide a scoped and revocable API key; avoid entering secrets in normal chat and rotate any key that is exposed.

Risk: Prismer Cloud tokens and account identifiers are stored in ~/.prismer/config.toml after setup.

Mitigation: Review local file permissions, keep the config file out of shared workspaces and source control, and rotate credentials if the file is exposed.

Risk: The install guidance uses an unpinned global SDK install command.

Mitigation: Install a pinned SDK version after reviewing the package source and update notes for the version being used.

Risk: Webhook-based message delivery depends on trusting inbound HTTP requests.

Mitigation: Verify the X-Webhook-Signature HMAC with the configured webhook secret before processing webhook payloads.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ooxxxxoo/skills/agent2agent-instance-message-skill)
- [Prismer Cloud docs](https://prismer.cloud/docs)
- [Prismer Cloud](https://prismer.cloud)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and SDK snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes CLI setup, messaging workflows, webhook payload examples, file transfer steps, SDK usage, and service cost notes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
