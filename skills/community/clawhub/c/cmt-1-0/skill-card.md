## Description:

Checks PDF, Word, and Excel files for sensitive or prohibited words using a built-in 65-word library or an external word list, then highlights matching terms in yellow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[betty831221](https://clawhub.ai/user/betty831221)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, compliance reviewers, and document owners use this skill to scan PDF, Word, and Excel documents against a built-in or external sensitive-word list and produce highlighted review copies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script may overwrite files with the same name.

Mitigation: Use a separate output directory and keep backups of source documents before running the checker.

Risk: The skill processes local documents that may contain sensitive information.

Mitigation: Run it only on documents approved for local processing and install dependencies in a virtual environment.

## Reference(s):

- [Usage Guide](references/usage.md)
- [ClawHub Skill Page](https://clawhub.ai/betty831221/skills/cmt-1-0)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Annotated PDF, DOCX, or XLSX files with concise Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Highlights matched sensitive words or cells in yellow; uses local document processing and optional external DOCX word lists.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
