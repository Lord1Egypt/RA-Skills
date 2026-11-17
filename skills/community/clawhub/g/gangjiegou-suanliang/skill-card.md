## Description:

钢结构出吨位估算；不识图、不替代结算。触发词：钢结构算量、钢构、H型钢。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lisong2003-lgtm](https://clawhub.ai/user/lisong2003-lgtm)

### License/Terms of Use:

CC BY-NC-SA 4.0

## Use Case:

Developers and structural steel quantity reviewers use this skill to turn an existing steel-geometry contract into a traceable section schedule and draft tonnage estimate for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports a contract-integrity weakness that could allow altered steel quantities to qualify for formal downstream use.

Mitigation: Avoid installation until the weakness is resolved; review contract inputs and keep estimates out of formal quantity records until independently verified.

Risk: ClawScan reports a mismatch between the skill's stated limits and its reported drawing and quantity-estimation capabilities.

Mitigation: Follow the documented input and capability limits, and have a qualified reviewer verify each estimate before relying on it.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/lisong2003-lgtm/skills/gangjiegou-suanliang)
- [Input contract and calculation guidance](references/on-demand.md)
- [lis-skill-bus contract flow](references/bus-contract.md)

## Skill Output:

**Output Type(s):** [Files, Analysis, Guidance]

**Output Format:** [JSON, Markdown, and CSV files containing a steel section schedule, quantity estimate band, and review notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tonnage is an approximately ±15% estimate; final_quantity is false and results require review.]

## Skill Version(s):

0.4.3 (source: frontmatter, CHANGELOG, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
