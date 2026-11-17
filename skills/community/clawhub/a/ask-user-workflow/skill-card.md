## Description:

Structured user consultation workflow that asks clarifying questions for complex or ambiguous tasks, then summarizes the answers into an actionable plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[9438190](https://clawhub.ai/user/9438190)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to pause on complex or ambiguous requests, ask a small set of structured clarifying questions, and turn the response into a clear task plan before implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can add an extra clarification and confirmation step before implementation.

Mitigation: Use it for ambiguous or multi-directional tasks, and skip it when the user has already provided complete requirements or asked the agent to proceed directly.

Risk: Optional follow-up with separate research tools can introduce additional permission and data-handling considerations.

Mitigation: Evaluate any separate research tool under its own permissions and risk guidance before use.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown task summaries with structured clarification questions and concise plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger a structured user consultation step before proceeding with work.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
