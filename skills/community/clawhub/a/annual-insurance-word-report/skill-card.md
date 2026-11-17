## Description:

Generates annual insurance welfare Word reports from the `gh_hg_bscyearall_dues` MySQL table using a bundled Word template.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lin-shiwu](https://clawhub.ai/user/lin-shiwu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business operations staff use this skill to generate yearly insurance welfare `.docx` reports from a configured MySQL database and template.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles live database credentials and ships unsafe default root credentials.

Mitigation: Run it only with a dedicated read-only MySQL account and replace the default credentials before installation or execution.

Risk: The security guidance identifies under-scoped SQL and executable-invocation behavior around MySQL access.

Mitigation: Validate year, database, and table inputs, and remove or tightly constrain the `mysql` CLI fallback.

Risk: The configured output path may overwrite an existing file.

Mitigation: Confirm the output location before running and restrict writes to an expected report directory.

Risk: The security guidance recommends dependency pinning for isolated installation.

Mitigation: Install in an isolated environment and pin dependencies before using the skill with production data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lin-shiwu/skills/annual-insurance-word-report)
- [Annual insurance configuration](artifact/references/annual-insurance-config.json)
- [Placeholder enums](artifact/references/placeholder-enums.json)
- [Schema comment query](artifact/references/schema-comment-query.sql)
- [Word template mapping](artifact/references/word-template-mapping.md)

## Skill Output:

**Output Type(s):** [Files, JSON, Shell commands, Configuration]

**Output Format:** [Word .docx report with a JSON run summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes to `outputs/annual-insurance-report-<year>.docx` by default unless an output path is supplied.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
