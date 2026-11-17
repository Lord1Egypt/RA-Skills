## Description:

Extract locational marginal prices (LMPs) from DC-OPF solutions using dual values.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and energy-market analysts use this skill to compute nodal electricity prices, reserve clearing prices, binding-line indicators, and price impacts from DC-OPF optimization outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated optimization code or counterfactual examples may mutate model inputs such as branch limits.

Mitigation: Review generated code and keep a separate baseline model state before running counterfactual analyses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wu-uk/skills/energy-market-pricing-locational-marginal-prices)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code]

**Output Format:** [Markdown with Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses on interpreting optimization dual values and counterfactual pricing results.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
