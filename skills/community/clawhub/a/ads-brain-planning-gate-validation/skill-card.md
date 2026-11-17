## Description:

Defines a common gate and validation protocol for an ad-planning agent framework, including capability gates, scenario gates, business guards, payload validation, execution gates, skipped states, blocked reasons, and next actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lizejia668-code](https://clawhub.ai/user/lizejia668-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators of ad-planning agents use this skill as a protocol reference for deciding when creation or optimization flows should pass, block, ask for clarification, route, warn, or require execution confirmation. It is intended to be consumed by related planning pipeline skills that implement the actual checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is documentation and protocol guidance only; it does not itself enforce ad-planning checks or execution confirmations.

Mitigation: Deploy it with the referenced planning pipelines or services that implement the defined gates, validations, guards, and confirmation steps.

Risk: The protocol includes a Chinese-only customer-facing copy rule that may not match every deployment locale.

Mitigation: Review locale requirements before deployment and adapt customer-facing output validation for the target market.

Risk: The protocol can influence whether ad creation or optimization proceeds, blocks, routes, or asks for clarification.

Mitigation: Validate downstream implementations against the documented decision priority, blocked_reason values, and next_action consistency rules before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lizejia668-code/skills/ads-brain-planning-gate-validation)
- [Publisher profile](https://clawhub.ai/user/lizejia668-code)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown protocol guidance with JSON examples and rule tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defines decision schemas, rule IDs, guard outputs, blocked_reason values, and next_action values for downstream planning pipelines.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
