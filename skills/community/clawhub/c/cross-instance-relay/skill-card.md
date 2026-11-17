## Description:

Connect agents across OpenClaw instances via a relay that can deliver messages through webhooks or queue unreachable messages for up to 7 days.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaravgarg](https://clawhub.ai/user/aaravgarg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure OpenClaw instances for cross-instance agent messaging through a relay, including webhook registration, message publishing, inbox polling, and optional WebSocket delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An external relay can remotely wake agents and deliver untrusted message content.

Mitigation: Install only when the relay operator is trusted, keep webhook-facing agents narrowly permissioned, and treat all relayed messages as untrusted input.

Risk: Shared relay and webhook tokens can expose the message channel if leaked through shell history, URLs, logs, or configuration.

Mitigation: Use narrowly scoped and revocable tokens, keep them out of committed files and logs, and rotate any token that may have been exposed.

Risk: Queued offline messages may be delivered later after the original context has changed.

Mitigation: Have receiving agents verify sender, team, and message freshness before acting on relayed instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaravgarg/skills/cross-instance-relay)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash/curl command examples and configuration variables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires relay URL, team token, team ID, and instance ID environment variables.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
