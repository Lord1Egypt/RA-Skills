## Description:

Forecast-simulation guides agents through simple math-based trend forecasts, target gap analysis, what-if scenarios, and depletion or saturation predictions using existing metric data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackyujun](https://clawhub.ai/user/jackyujun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business analysts use this skill to help an agent answer future-looking metric questions, evaluate target gaps, model what-if assumptions, and estimate depletion or saturation timing from existing data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on broad future-looking business questions and cause metric-query to retrieve relevant business metrics.

Mitigation: Review activation behavior and data-access expectations before deployment, and ensure metric-query access is appropriate for the intended users.

Risk: Forecasts and simulations are simple estimates that may be mistaken for authoritative predictions.

Mitigation: Require outputs to state assumptions, uncertainty, and review needs before business decisions are made from the results.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/jackyujun/skills/forecast-simulation)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown-style analytical guidance with assumptions, uncertainty notes, and optional Python calculation snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Forecast outputs should be treated as simple estimates based on recent trends, not authoritative predictions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
