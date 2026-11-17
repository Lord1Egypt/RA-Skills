## Description:

Use the Health Data AI Analyzer Mac app's read-only local API to generate an Apple Health daily brief and three practical suggestions when the user explicitly requests an analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krumjahn](https://clawhub.ai/user/krumjahn)

### License/Terms of Use:

MIT-0

## Use Case:

People using the Health Data AI Analyzer Mac app can review their imported Apple Health data as a daily brief, recent step and sleep comparisons, and three practical non-medical suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads personal health information from the Health Data AI Analyzer local API.

Mitigation: Run only when the user explicitly asks, read only the minimum endpoint needed, and keep health data local without sending it to external services.

Risk: Health summaries or suggestions could be mistaken for medical advice, and missing measurements could lead to unsupported conclusions.

Mitigation: Do not diagnose or give medical advice, do not invent missing data, and identify absent or null metrics as insufficient data.

## Reference(s):

- [Apple Health Data AI Analyzer on ClawHub](https://clawhub.ai/krumjahn/skills/apple-health-export-analyzer)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Markdown with Status, What changed, Suggestions, and Missing data sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Three practical non-medical suggestions; absent or null health metrics are identified as insufficient data.]

## Skill Version(s):

1.0.9 (source: server-resolved ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
