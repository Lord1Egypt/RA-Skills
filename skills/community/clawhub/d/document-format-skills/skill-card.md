## Description:

A Word document formatting toolkit for Chinese DOCX files that helps agents diagnose formatting issues, fix mixed Chinese and English punctuation, and apply standardized document styles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[standman61](https://clawhub.ai/user/standman61)

### License/Terms of Use:

MIT License

## Use Case:

Developers, document automation users, and agent operators use this skill to inspect Chinese DOCX formatting, normalize punctuation, and apply official, academic, or legal formatting presets before sharing or archiving documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Formatting and punctuation rewrites can unintentionally change document appearance or meaning.

Mitigation: Run the skill on copies of documents first and review the generated DOCX before replacing the original.

Risk: The release evidence notes that some advertised options are not actually honored.

Mitigation: Validate important formatting and punctuation choices manually after running the scripts.

Risk: The dependency workflow uses an unpinned python-docx runtime dependency.

Mitigation: Install python-docx from a pinned, trusted environment for repeatable or sensitive workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/standman61/skills/document-format-skills)
- [python-docx Documentation](https://python-docx.readthedocs.io/)
- [uv](https://github.com/astral-sh/uv)
- [Document Format GUI](https://github.com/KaguraNanaga/docformat-gui)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text, Files]

**Output Format:** [Markdown guidance with inline shell commands, terminal diagnostics, and generated DOCX files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports .docx files only; generated documents should be reviewed because formatting and punctuation are rewritten.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
