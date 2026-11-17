## Description:

Calculates China individual income tax for monthly salary, annual bonus, special deductions, annual settlement, and multi-income scenarios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jarliao](https://clawhub.ai/user/jarliao)

### License/Terms of Use:

MIT-0

## Use Case:

External users, payroll and HR teams, and compensation planners use this skill to estimate China individual income tax, compare annual bonus taxation methods, model deductions and social insurance, generate salary reports, and export batch payroll calculations.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Generated reports and batch exports can expose payroll, tax, employee name, salary, bonus, and deduction data.

Mitigation: Use the skill only with payroll or tax data the user is authorized to process, avoid unnecessary real names, and check sharing permissions before placing reports in collaboration tools.

Risk: Batch CSV export data may be opened in spreadsheet software where untrusted employee fields can create CSV handling risk.

Mitigation: Sanitize or quote CSV fields before opening batch exports in spreadsheet software when employee-provided data may be untrusted.

Risk: Tax and social insurance calculations can become inaccurate when laws, deduction standards, city rates, or local interpretations change.

Mitigation: Verify calculation assumptions against current official tax and social insurance rules before using outputs for payroll, legal, or financial decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jarliao/skills/china-tax-calculator)

## Skill Output:

**Output Type(s):** [text, markdown, CSV, structured data, guidance]

**Output Format:** [Plain text calculation summaries, Markdown reports, CSV export strings, and structured dictionary data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include sensitive payroll, tax, employee name, salary, bonus, deduction, and report-sharing data.]

## Skill Version(s):

0.1.4 (source: server release evidence; artifact metadata lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
