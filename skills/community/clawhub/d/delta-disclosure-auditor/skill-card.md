## Description:

Helps verify that skill updates publish an auditable record of what changed, including risk-class alignment, chain-of-custody checks, and update eligibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud)

### License/Terms of Use:


## Use Case:

Developers, maintainers, and auditors use this skill to assess whether skill updates disclose material changes across capabilities, dependencies, validation, behavioral scope, risk classification, custody, and update eligibility.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Auditing private registry endpoints or unpublished artifacts may expose information through local comparison workflows.

Mitigation: Use the skill only with targets you intend to inspect, and avoid private registry endpoints or unpublished artifacts unless local tool use is acceptable.

Risk: Delta disclosure reports can be incomplete when version history, signed deltas, or enough comparable artifacts are unavailable.

Mitigation: Treat unresolved custody gaps, incomplete histories, and high-risk disclosures as requiring manual review before update eligibility decisions.

## Reference(s):

- [Delta Disclosure Auditor on ClawHub](https://clawhub.ai/andyxinweiminicloud/skills/delta-disclosure-auditor)
- [andyxinweiminicloud publisher profile](https://clawhub.ai/user/andyxinweiminicloud)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown audit report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports delta disclosure completeness, material undisclosed changes, custody integrity, monitoring tractability, disclosure verdict, and update eligibility.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
