## Description:

A French-language agent for calculating, explaining, checking, and exporting daily and weekly work-time results with pauses, overtime thresholds, estimated salary, HH:MM/decimal conversions, duration subtraction, and overnight shifts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nazzal5448](https://clawhub.ai/user/nazzal5448)

### License/Terms of Use:

MIT-0

## Use Case:

External users and employees use this skill to compute French work-hour totals, overtime reference thresholds, simple salary estimates, and export-ready time summaries. It is intended for calculation and verification support, not personalized legal or payroll advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Salary, overtime, or payroll-related outputs may be mistaken for legal or payroll advice.

Mitigation: Present these outputs as estimates and direct users to verify important decisions against their contract, convention collective, HR source, or qualified professional.

Risk: Ambiguous time inputs, pauses, overlapping work periods, or overnight shifts can change the computed result.

Mitigation: Ask for the missing detail before calculating when ambiguity affects the result, and preserve exact minutes before rounding or formatting.

## Reference(s):

- [Calculette Mauricette](https://mauricettecalcul.fr/)
- [ClawHub skill page](https://clawhub.ai/nazzal5448/skills/calculette-mauricette-skill)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text with calculations, tables, and CSV-ready summaries when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should preserve minute-level precision and label salary or overtime results as estimates when inputs do not establish payroll rules.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
