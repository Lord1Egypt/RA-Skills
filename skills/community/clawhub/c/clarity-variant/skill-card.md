## Description:

Retrieves Clarity Protocol variant details, AlphaFold confidence data, AI-generated summaries, agent findings, and annotations for specific protein variants.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clarityprotocol](https://clawhub.ai/user/clarityprotocol)

### License/Terms of Use:

MIT

## Use Case:

External developers, analysts, and bioinformatics users use this skill to retrieve variant-level Clarity Protocol data, compare structural, clinical, literature, and synthesis findings, and inspect annotations for a fold ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends lookup requests to clarityprotocol.io and may include CLARITY_API_KEY as an API header when configured.

Mitigation: Use the skill only when this external network destination is acceptable, and manage CLARITY_API_KEY as a secret.

Risk: AI-generated summaries, clinical findings, and literature findings may be incomplete or require domain review.

Mitigation: Verify retrieved findings against appropriate primary sources before using them for clinical, research, or operational decisions.

## Reference(s):

- [Clarity Protocol](https://clarityprotocol.io)
- [Clarity Protocol API](https://clarityprotocol.io/api/v1)
- [Clarity Variant on ClawHub](https://clawhub.ai/clarityprotocol/skills/clarity-variant)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [JSON or human-readable terminal summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a fold ID; optional filters include agent type, agent ID, and annotation type.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
