## Description:

Calculate construction costs using DDC CWICR resource-based methodology. Break down costs into labor, materials, equipment with transparent pricing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction)

### License/Terms of Use:

MIT

## Use Case:

External construction estimators, project teams, and developers use this skill to calculate and compare construction costs with labor, material, equipment, overhead, profit, and unit-cost breakdowns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency supply-chain exposure from installing pandas and numpy for local cost calculations.

Mitigation: Use a virtual environment and pin pandas and numpy versions from a trusted package index before running calculator code.

Risk: Construction quantity or pricing datasets may contain sensitive project cost information.

Mitigation: Provide only the construction datasets or quantity files needed for the calculation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/datadrivenconstruction/skills/cwicr-cost-calculator)
- [Publisher profile](https://clawhub.ai/user/datadrivenconstruction)
- [Data Driven Construction homepage](https://datadrivenconstruction.io)
- [OpenConstructionEstimate-DDC-CWICR GitHub repository (source-mentioned; server provenance unavailable)](https://github.com/datadrivenconstruction/OpenConstructionEstimate-DDC-CWICR)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown and structured cost breakdowns, with optional Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include per-item costs, resource-category totals, percentages, unit costs, comparisons, and report-style summaries.]

## Skill Version(s):

2.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
