## Description:

ClawBrain Boost helps OpenClaw users route model requests through ClawBrain with memory, data-preservation checks, fault tolerance, and writing assistance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michaelfeng](https://clawhub.ai/user/michaelfeng)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to configure ClawBrain as a model provider and default routing option, including model tiers, memory-assisted context recovery, data fidelity checks, and domain-specific response guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill configures a third-party model provider as the default route for OpenClaw requests.

Mitigation: Install only after reviewing the provider terms and use a dedicated, revocable API key.

Risk: Model requests may include text, images, conversation context, and memory-derived information sent to the ClawBrain/FactorHub endpoint.

Mitigation: Avoid regulated, confidential, or secret data unless the publisher's retention, deletion, opt-out, and privacy controls meet your requirements.

Risk: Automatic long-term memory is advertised without enough evidence of data-handling controls.

Mitigation: Keep the existing default model unless intentional global routing and memory behavior are acceptable for the deployment.

## Reference(s):

- [Clawbrain Boost on ClawHub](https://clawhub.ai/michaelfeng/skills/clawbrain-boost)
- [ClawBrain homepage](https://clawbrain.dev)
- [ClawBrain dashboard](https://clawbrain.dev/dashboard)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces installation and configuration guidance for OpenClaw model routing.]

## Skill Version(s):

1.6.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
