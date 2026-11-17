## Description:

Generator economic dispatch and cost optimization for power systems. Use when minimizing generation costs, computing optimal generator setpoints, calculating operating margins, or working with generator cost functions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and power-system engineers use this skill to structure economic dispatch calculations, generator cost functions, reserve co-optimization, operating margin checks, and dispatch result summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect power-system models, load data, generator limits, or solver results could lead to unreliable dispatch or cost recommendations.

Mitigation: Validate models, input data, constraints, solver status, and optimization outputs with qualified power-system review before operational or financial use.

Risk: Ill-conditioned optimization problems or unsuitable solver choices may produce failures or misleading results.

Mitigation: Use robust solver settings where appropriate, inspect infeasibility and convergence reports, and compare outputs against known test cases before relying on results.

## Reference(s):

- [Generator Cost Functions Reference](artifact/references/cost-functions.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with Python and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes MATPOWER field mappings, CVXPY optimization examples, dispatch result structure, and solver selection guidance.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
