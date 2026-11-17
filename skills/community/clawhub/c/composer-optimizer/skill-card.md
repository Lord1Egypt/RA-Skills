## Description:

Optimizes Composer.trade Traditional IRA strategy allocations with simplified scoring and mean-variance weighting, then writes a local JSON allocation report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plato-1](https://clawhub.ai/user/plato-1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers working with Composer.trade IRA strategy data use this skill to score strategies, reduce weak or redundant allocations, and generate an allocation report for review before portfolio action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Finance assumptions and optimizer behavior may be simplified or differ from the manifest description.

Mitigation: Review the allocation methodology, assumptions, and generated recommendations before relying on the output for portfolio decisions.

Risk: The skill writes a local JSON recommendation report.

Mitigation: Confirm the input data source and output path are expected before running the skill in a workspace with financial data.

## Reference(s):

- [Composer Optimizer ClawHub Skill Page](https://clawhub.ai/plato-1/skills/composer-optimizer)
- [Publisher Profile](https://clawhub.ai/user/plato-1)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance, files]

**Output Format:** [JSON file with console text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a local Composer Traditional IRA optimization report for human review.]

## Skill Version(s):

1.0.0 (source: server release metadata and claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
