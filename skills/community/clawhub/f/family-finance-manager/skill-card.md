## Description:

Family Finance Manager provides family financial analysis, savings goal planning, insurance configuration guidance, risk warnings, and financial health reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to review household income, expenses, assets, liabilities, goals, and insurance coverage, then receive structured planning and financial health guidance. It is intended for rule-based family finance management rather than regulated financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may enter sensitive household income, asset, liability, insurance, and family-member details.

Mitigation: Use approximate values where possible, omit names unless necessary, and avoid sharing outputs beyond the intended household or reviewer.

Risk: The artifact describes this release as an MVP skeleton with stub analysis behavior and simulated rule-based outputs.

Mitigation: Review outputs as planning support only, verify calculations independently, and avoid treating insurance or investment suggestions as professional financial advice.

Risk: The security guidance notes that responses may primarily be in Chinese despite bilingual metadata.

Mitigation: Confirm that users can review Chinese-language financial recommendations accurately before relying on the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/family-finance-manager)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Structured JSON-like financial reports with human-readable recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include savings rates, net worth, goal milestones, insurance coverage gaps, risk factors, financial health scores, and action plans.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
