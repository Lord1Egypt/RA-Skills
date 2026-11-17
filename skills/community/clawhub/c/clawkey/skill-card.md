## Description:

Verifiable human ownership for OpenClaw agents through registration under a human owner via VeryAI palm verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oyyblin](https://clawhub.ai/user/oyyblin)

### License/Terms of Use:


## Use Case:

Developers and agent operators use Clawkey to register an OpenClaw or compatible agent under a verified human owner, then check registration or signature status before presenting ownership claims to third parties.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill shares stable device identifiers, public keys, signed challenge data, and verification status with third-party APIs.

Mitigation: Review ClawKey and VeryAI protocol and privacy practices before installation, and use the skill only where that data sharing is acceptable.

Risk: Recurring heartbeat checks can reveal ongoing agent registration or verification activity.

Mitigation: Run heartbeat or status checks only with clear user intent or an operational need, and avoid automatic recurring lookups by default.

Risk: Human ownership verification may be overused as an authorization signal.

Mitigation: Treat ClawKey status as one identity signal and avoid relying on it alone for high-stakes authorization decisions.

Risk: Registration URLs are single-use, short-lived links intended for the human owner.

Mitigation: Return registration URLs only as text or markdown links for the human owner to open, and do not open a browser automatically.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oyyblin/skills/clawkey)
- [ClawKey homepage](https://clawkey.ai)
- [ClawKey API base](https://api.clawkey.ai/v1)
- [ClawKey skill documentation](https://clawkey.ai/skill.md)
- [ClawKey heartbeat documentation](https://clawkey.ai/heartbeat.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, JavaScript, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs registration URLs as text or markdown links for the human owner; it does not open browsers.]

## Skill Version(s):

1.0.2 (source: evidence release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
