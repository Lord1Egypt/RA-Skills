## Description:

Interrogate a demand forecast before the business commits supply and inventory to it, producing a forecast credibility review with baseline/uplift decomposition, MAPE and bias history, hockey-stick flags, an assumption register, and consensus-vs-statistical divergence analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

Supply planners, demand planners, and operations teams use this skill to challenge demand plans before committing supply, capacity, or inventory. It structures the review around forecast history, baseline versus uplift, anomaly flags, assumption ownership, and an actionable planning verdict.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Forecast review recommendations may influence supply, capacity, or inventory commitments if accepted without business validation.

Mitigation: Require demand owners and supply planners to verify source data, accuracy history, assumptions, and decision lead times before acting on the verdict.

Risk: Missing or incomplete historical accuracy data can weaken forecast credibility judgments.

Mitigation: When accuracy history is unavailable, treat the forecast as unvalidated and use the skill output as a structured question set rather than an approval.

## Reference(s):

- [Demand Forecast Review ClawHub Page](https://clawhub.ai/mohitagw15856/skills/demand-forecast-review)
- [Demand Forecast Review Homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/demand-forecast-review.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Markdown forecast review with verdict, decomposition tables, risk flags, assumption register, divergence analysis, and questions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces planning recommendations based on user-provided forecast inputs and history; does not execute code or perform actions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
