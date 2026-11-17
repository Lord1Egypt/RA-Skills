## Description:

Cleans CSV and Excel datasets by removing duplicates, filling missing values, standardizing phone and date fields, and writing cleaned output files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenghoo123-png](https://clawhub.ai/user/shenghoo123-png)

### License/Terms of Use:

MIT-0

## Use Case:

Operations, finance, administrative, and sales users can use this skill to clean CSV or Excel data for reports, customer lists, billing data, employee records, and order datasets. Developers and agents can invoke the included Python cleaner to generate cleaned files and a concise processing report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleaning can remove duplicate rows or alter missing values, phone numbers, and dates in generated outputs.

Mitigation: Use copies of important datasets and inspect cleaned files before relying on them.

Risk: Spreadsheet inputs from untrusted sources may contain formulas or other content that needs additional handling.

Mitigation: Avoid processing untrusted spreadsheets unless formula-injection protections are added.

Risk: The documentation references a batch-cleaning script that is not present in the inspected artifact.

Mitigation: Verify available scripts before running documented batch commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shenghoo123-png/skills/data-cleaner-tool)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell command examples, Python code references, cleaned CSV or Excel files, and console reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may remove duplicate rows and alter missing values, phone numbers, or date formats in generated cleaned datasets.]

## Skill Version(s):

1.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
