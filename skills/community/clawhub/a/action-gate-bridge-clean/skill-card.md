## Description:

Route risky communications next steps through a typed action-intent bridge so external writes, bookings, settings changes, public posts, and spend decisions require explicit policy and approval handling instead of informal reasoning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heyalerio](https://clawhub.ai/user/heyalerio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill in communications workflows to classify risky next steps and route external writes, bookings, settings changes, public posts, and spend decisions through explicit approval handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-impact actions could be routed through unauthenticated local HTTP helpers if the bridge is treated as the approval boundary.

Mitigation: Use only with a trusted, authenticated action-gate sidecar or proxy, restrict endpoint configuration, and require explicit user approval for red actions.

Risk: Sensitive request bodies or credential references could be exposed through routed write intents.

Mitigation: Avoid routing sensitive request bodies or credential references until the bridge validates and authenticates responses.

## Reference(s):

- [Action Bridge](references/action-bridge.md)
- [Approval Matrix](references/approval-matrix.md)
- [ClawHub Skill Page](https://clawhub.ai/heyalerio/skills/action-gate-bridge-clean)
- [ClawHub Publisher Profile](https://clawhub.ai/user/heyalerio)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown guidance with inline shell commands and JSON helper responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes proposals to configured local action-gate endpoints and expects allowed, needs_approval, blocked, or accepted results.]

## Skill Version(s):

0.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
