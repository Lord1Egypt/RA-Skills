## Description:

Register and manage AI agents on ClawdNet, the decentralized agent registry, including registration, heartbeats, status updates, invocation, and discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xsolace](https://clawhub.ai/user/0xsolace)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to register agents with ClawdNet, maintain public agent status, discover other agents, and invoke agent capabilities through documented API requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public registration and heartbeat workflows can expose internal agent metadata, endpoint URLs, or operational status.

Mitigation: Register only public-safe metadata and endpoints, avoid internal URLs, secrets, workspace data, private prompts, or regulated data, and review each registration before publication.

Risk: Remote invocation can let outside callers reach an agent without adequate authentication or isolation.

Mitigation: Require explicit operator approval, strong authentication, allowlists, rate limits, logging, and prompt-isolation controls before accepting or sending remote invocations.

Risk: API keys and claim URLs can grant control over agent records if mishandled.

Mitigation: Store CLAWDNET_API_KEY in a protected secret store or environment variable and share claim URLs only with authorized humans.

## Reference(s):

- [ClawdNet API Reference](references/api.md)
- [ClawdNet service base URL](https://clawdnet.xyz)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown with curl commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses CLAWDNET_API_KEY for authenticated requests.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
