## Description:

Docx Tools helps agents read, write, convert, and combine Word DOCX and Markdown documents through local Python utilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jirboy](https://clawhub.ai/user/jirboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document automation users use this skill to extract text from DOCX files, create DOCX files, convert between DOCX and Markdown, and assemble multi-section Word documents such as proposals or papers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads and writes local document paths supplied by the user.

Mitigation: Use explicit input and output filenames, run it in an isolated environment, and keep backups of important documents before writing or converting files.

Risk: Document conversion can lose complex formatting, tables, or unsupported Markdown constructs.

Mitigation: Review converted DOCX and Markdown outputs before using them as final documents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jirboy/skills/docx-tools)
- [Publisher profile](https://clawhub.ai/user/jirboy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or modifies local DOCX and Markdown files at user-provided paths.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
