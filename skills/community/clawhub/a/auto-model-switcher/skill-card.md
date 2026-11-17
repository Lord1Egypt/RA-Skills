## Description:

Automatically selects the best model based on task type and requirements. Use when: (1) Task requires specific capabilities (coding, analysis, multimodal, writing, research), (2) Need optimal performance/cost balance, (3) Working with long context or complex reasoning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrcuo](https://clawhub.ai/user/mrcuo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to route tasks to configured models based on task type, context length, multimodal needs, and cost-performance tradeoffs. It also preserves manual model override when a user states a preference.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic model switching can send work to a provider or model with different cost, performance, or data-handling expectations than the user intended.

Mitigation: Review configured providers and costs before installation, and specify a model manually for sensitive tasks.

Risk: A task may be routed to a model that is unavailable or not configured for the current agent environment.

Mitigation: Validate model names against the configured model list before switching and fall back to the current session model when selection fails.

## Reference(s):

- [Project homepage](https://github.com/mrcuo/auto-model-switcher)
- [ClawHub skill page](https://clawhub.ai/mrcuo/skills/auto-model-switcher)

## Skill Output:

**Output Type(s):** [Guidance, Configuration]

**Output Format:** [Markdown guidance with model identifiers and usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes only among configured models and respects explicit user model preferences.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
