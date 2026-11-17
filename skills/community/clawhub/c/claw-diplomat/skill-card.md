## Description:

Enables secure, peer-to-peer task negotiation and commitment tracking between two OpenClaw agents without requiring a central server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[techtanush](https://clawhub.ai/user/techtanush)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect two OpenClaw agents, negotiate reciprocal tasks, record approved commitments, and surface deadlines and check-ins during later sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Peer-provided text can affect persistent agent state and appear in later agent context.

Mitigation: Use trusted peers, review proposals and handoffs before approval, and review or disable the bootstrap and heartbeat hooks if peer-authored text should not be surfaced in future context.

Risk: Task and handoff details are shared with selected peers through a relay-based workflow.

Mitigation: Avoid sensitive details in task or handoff text and use only trusted peers with a trusted WSS relay.

Risk: The skill runs a background listener for inbound peer connections.

Mitigation: Install only where a background listener is acceptable, and disable the gateway listener behavior when inbound peer connections are not needed.

Risk: Runtime dependencies are installed separately.

Mitigation: Prefer pinned dependency versions before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/techtanush/skills/claw-diplomat)
- [ClawHub listing homepage](https://clawhub.io/skills/claw-diplomat)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown and plain-text agent responses with command examples and workspace records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates workspace commitment records and peer connection state.]

## Skill Version(s):

1.0.4 (source: server release metadata and clawhub.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
