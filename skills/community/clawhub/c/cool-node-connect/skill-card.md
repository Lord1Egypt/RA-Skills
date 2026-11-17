## Description:

Diagnose OpenClaw node connection and pairing failures for Android, iOS, and macOS companion apps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chuangyinbot-boop](https://clawhub.ai/user/chuangyinbot-boop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to diagnose OpenClaw companion-app connection, routing, pairing, and authorization failures across local, tailnet, and public gateway setups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approving the latest pending device can authorize an unintended device when others can reach the pairing endpoint.

Mitigation: Inspect pending pairing requests and approve only the intended device; avoid relying on --latest when unexpected or competing requests may exist.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces diagnostic questions, route analysis, concrete OpenClaw commands, and configuration repair guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
