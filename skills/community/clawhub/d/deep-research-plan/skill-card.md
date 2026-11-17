## Description:

Automated deep research that performs comprehensive multi-source investigation and produces detailed reports with citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bird-frank](https://clawhub.ai/user/bird-frank)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to plan and execute in-depth research workflows, including collaborative scope definition, structured research plans, and cited final reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill delegates execution to a sub-agent that can choose and expand searches within the approved plan.

Mitigation: Review the generated plan carefully before approving execution, especially topic boundaries, research questions, and source expectations.

Risk: Broad trigger wording may cause the skill to be used for open-ended research requests with unclear scope.

Mitigation: Require explicit user confirmation of the research plan before launching the execution phase.

## Reference(s):

- [Research Plan Examples](references/plan-examples.md)
- [ClawHub skill page](https://clawhub.ai/bird-frank/skills/deep-research-plan)
- [Publisher profile](https://clawhub.ai/user/bird-frank)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Guidance]

**Output Format:** [Markdown reports and structured JSON research plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Research plans are saved as JSON files under plans/research-plan-{timestamp}.json after user approval.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
