## Description:

Helps agents perform data governance tasks including data quality assessment, metadata management, lineage analysis, data standard support, and compliance checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xingjianliu0417](https://clawhub.ai/user/xingjianliu0417)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data engineers, and governance teams use this skill to inspect database tables, generate metadata, analyze table lineage, and produce data quality or compliance reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects to databases using credentials and may expose sensitive schema or field names in generated reports.

Mitigation: Install only in a controlled environment, use a read-only database account limited to the schemas under review, avoid passing passwords in command-line connection strings, and review reports before sharing.

Risk: The security evidence flags dependency and scoping weaknesses, including guidance to upgrade PyMySQL and avoid running the data-quality checker on highly sensitive tables until the row-scope issue is fixed.

Mitigation: Upgrade PyMySQL before use, restrict table access, and run checks first on non-sensitive or representative data.

## Reference(s):

- [ClawHub Data Governance skill page](https://clawhub.ai/xingjianliu0417/skills/data-governance)
- [requirements.txt](artifact/requirements.txt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, Mermaid diagrams, and console text with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write generated metadata reports to a user-specified output file.]

## Skill Version(s):

1.10.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
