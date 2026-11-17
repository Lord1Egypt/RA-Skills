## Description:

Validate CSV, JSON, and JSONL data files for missing values, duplicates, type inconsistencies, statistical outliers, format violations, whitespace problems, empty columns, and schema drift.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data engineers, and analysts use this skill to profile CSV, JSON, and JSONL datasets, surface quality issues, generate severity-ranked reports, and validate data against schemas before using it in downstream workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checker can overwrite a report or generated schema at a user-specified output path.

Mitigation: Choose output paths deliberately and avoid pointing generated reports or schemas at existing files that should be preserved.

Risk: Data quality reports may expose sensitive dataset contents or derived information when run on protected data.

Mitigation: Run the skill only in a local environment appropriate for the dataset sensitivity and handle generated reports under the same controls as the source data.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, code, guidance]

**Output Format:** [Markdown or JSON reports with command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include severity-ranked issues, a 0-100 quality score, and exit codes suitable for local or CI usage.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
