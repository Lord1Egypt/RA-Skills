## Description:

Helps U.S. listing agents organize comparable sales, record adjustments, and prepare a seller net sheet while distinguishing a broker's opinion of value from an appraisal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

External U.S. listing agents and team leaders use this skill to organize comparable-sales information and prepare CMA materials for seller consultations.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The quickstart supplies a YAML worksheet to a script that reads CSV input.

Mitigation: Resolve the format mismatch and check rankings and calculations independently before using results with clients.

Risk: MLS data is licensed to the brokerage.

Mitigation: Keep licensed MLS data within brokerage-approved storage.

Risk: The script may overwrite ranking.md in the selected output folder.

Mitigation: Choose an output folder where overwriting ranking.md is acceptable.

Risk: The optional Windows app is a separate download requiring independent review.

Mitigation: Assess the app separately before running it.

## Reference(s):

- [CMA rules and checklist](references/cma-rules.md)
- [ClawHub skill release](https://clawhub.ai/rapidworker1/skills/comparable-market-analysis)

## Skill Output:

**Output Type(s):** [Markdown, Configuration]

**Output Format:** [Markdown comparable-sales ranking and YAML CMA worksheet]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The worksheet includes comparable-sale adjustments, a value range, and seller net-sheet fields. Verify figures and calculations before client use.]

## Skill Version(s):

1.0.7 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
