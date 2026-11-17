## Description:

Produces preliminary MEP quantity takeoff working papers and material plan drafts from drawing contracts or scan indexes; it does not provide pricing or settlement quantities.

This skill is for research and development only.

## Publisher:

[lisong2003-lgtm](https://clawhub.ai/user/lisong2003-lgtm)

### License/Terms of Use:

CC BY-NC-SA 4.0

## Use Case:

MEP engineers, quantity surveyors, and project teams use this skill to turn drawing-derived contracts or scan indexes into preliminary installation quantity schedules and material plan drafts for budgeting and review. The results require human checking and do not replace professional detailing, pricing, or settlement work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence flags a mismatch between the estimating purpose and some reported capabilities, as well as dependency-install and integrity concerns. The scan is partial and does not establish clear malicious intent.

Mitigation: Before installing, review the unexpected capabilities and dependency-install behavior, verify that they fit your needs, and do not treat the partial scan or completed AIG scan as proof of safety.

## Reference(s):

- [Input contract and integration boundaries](references/base-contract.md)
- [Quantity takeoff methods and limits](references/on-demand.md)
- [Standard quantity rules](references/standard_rules.json)
- [Loss and ordering rules](references/loss_rules.json)

## Skill Output:

**Output Type(s):** [Files, JSON]

**Output Format:** [Multi-sheet XLSX quantity and material planning workbook, with JSON scan and contract data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft quantities with evidence, confidence, and review notes; excludes prices and monetary amounts.]

## Skill Version(s):

0.4.38 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
