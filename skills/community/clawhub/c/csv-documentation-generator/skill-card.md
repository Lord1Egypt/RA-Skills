## Description:

Use when generating computer system validation (CSV) documentation for pharmaceutical and medical device industries, including validation plans, URS, FS, IQ/OQ/PQ documents, and traceability matrices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zealot00](https://clawhub.ai/user/zealot00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, validation engineers, and quality teams use this skill to generate GxP computer system validation documents for pharmaceutical and medical device systems. It supports validation plans, URS, FS, risk assessments, IQ/OQ/PQ protocols, traceability matrices, checklists, and validation summary reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes guidance for broad code annotation rules that can affect future agent-generated code when copied into global agent instructions.

Mitigation: Apply annotation rules only to workspaces where GxP traceability markers are intended, and review generated code before use.

Risk: The artifact includes optional Git hook installation that can persist behavior in a repository.

Mitigation: Install hooks only after reviewing the hook script and confirming the repository should enforce those checks.

Risk: Automatic dependency setup may install packages without pinned versions.

Mitigation: Use a reviewed, pinned dependency environment for production or regulated validation workflows.

Risk: Generated validation documents may be incomplete or inappropriate for a specific regulated system.

Mitigation: Have qualified validation and quality personnel review generated documents against the system scope and applicable regulations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zealot00/skills/csv-documentation-generator)
- [Project homepage](https://github.com/zealot00/csv-documentation-generator)
- [GAMP 5 quick reference](artifact/references/gamp-5.md)
- [21 CFR Part 11 quick reference](artifact/references/21cfr-part11.md)
- [EU Annex 11 quick reference](artifact/references/annex-11.md)
- [ALCOA+ data integrity reference](artifact/references/data-integrity.md)
- [Code annotation standards](artifact/STANDARDS.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with shell commands; generated .docx and .xlsx validation documents when scripts are run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports bilingual Chinese/English templates and optional document generation for a full validation package.]

## Skill Version(s):

1.6.4 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
