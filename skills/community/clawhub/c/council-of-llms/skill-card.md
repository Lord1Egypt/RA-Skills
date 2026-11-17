## Description:

Real multi-model council deliberation for OpenClaw subagents that spawns three parallel subagents with distinct analytical perspectives and synthesizes their independent outputs into a unified verdict.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wahajahmed010](https://clawhub.ai/user/wahajahmed010)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run multi-model reviews, debates, stress tests, and decision analyses by assigning strategic, analytical, and creative perspectives to separate subagents before synthesizing a final verdict.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured council models may be cloud-backed, so copied context can be sent to external model providers.

Mitigation: Review configured models before use and avoid pasting secrets, credentials, customer data, regulated information, or proprietary material unless sharing with those providers is acceptable.

Risk: The skill can create a local council-review markdown file in the workspace.

Mitigation: Review generated files before sharing, committing, or using them as decision records.

Risk: The skill depends on companion subagent orchestration behavior.

Mitigation: Review or pin the companion subagent skill before installing or running the council workflow.

## Reference(s):

- [Council Of Llms on ClawHub](https://clawhub.ai/wahajahmed010/skills/council-of-llms)
- [Subagent Orchestration companion skill](https://github.com/wahajahmed010/subagent-orchestration)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown synthesis with structured verdicts, consensus points, disagreements, blind spots, and action items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a local council-review markdown file in the workspace.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
