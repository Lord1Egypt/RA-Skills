## Description:

Set up and operate full cross-gateway task delegation between two OpenClaw Discord bots across different PCs/gateways.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jini92](https://clawhub.ai/user/jini92)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure private Discord delegation lanes, structured worker task envelopes, worker intake, status replies, and final-result relay-back between OpenClaw bots on separate gateways.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill forwards DM content and Discord identifiers to another bot or channel.

Mitigation: Use only trusted operator-controlled bots and private worker lanes, and make users aware before DM content or Discord identifiers are forwarded.

Risk: Weak scoping or consent can expose private task content beyond the intended worker lane.

Mitigation: Restrict worker-lane access, keep triggers narrow and owner/operator scoped where possible, and require confirmation for browser, credential, operations, or external-action tasks.

## Reference(s):

- [Setup Checklist](references/setup-checklist.md)
- [Operating Modes](references/operating-modes.md)
- [Full Process](references/full-process.md)
- [Secondary Worker Rollout](references/macjini-rollout.md)
- [Diagnosis](references/diagnosis.md)
- [Task Protocol Examples](examples/task-protocol.md)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions, Markdown, Shell commands]

**Output Format:** [Markdown guidance with structured Discord task envelope examples and configuration path references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operator-facing setup, delegation, troubleshooting, and relay-back guidance; no executable scripts are included.]

## Skill Version(s):

2.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
