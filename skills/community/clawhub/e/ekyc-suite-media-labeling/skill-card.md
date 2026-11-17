## Description:

Provides structured portrait, behavior, and scene labels for consented images or videos in KYC media review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[carochen112233-commits](https://clawhub.ai/user/carochen112233-commits)

### License/Terms of Use:

MIT-0

## Use Case:

KYC onboarding, fraud review, and identity operations teams use this skill to request supported media labels as signals for human review, not as final identity or risk decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted KYC media and optional attribution details leave the agent for the configured cloud backend.

Mitigation: Use only consented media with a trusted HTTPS backend and an established retention policy; set optional attribution values only when appropriate.

Risk: Media labels may be ambiguous or inaccurate and could influence high-impact decisions.

Mitigation: Treat labels as review signals and escalate sensitive or uncertain results to an authorized human reviewer.

## Reference(s):

- [eKYC Suite Media Labeling on ClawHub](https://clawhub.ai/carochen112233-commits/skills/ekyc-suite-media-labeling)
- [Related eKYC Suite Media Labeling MCP package](https://www.npmjs.com/package/@wefi-ai/ekyc-suite-media-labeling-mcp)

## Skill Output:

**Output Type(s):** [Text, Shell commands, JSON]

**Output Format:** [Guidance and shell commands in Markdown; structured label results in JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports 1–5 requested label codes per call; results are review signals rather than final decisions.]

## Skill Version(s):

1.0.21 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
