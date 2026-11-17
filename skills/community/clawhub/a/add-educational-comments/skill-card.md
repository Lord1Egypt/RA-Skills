## Description:

Add educational comments to the file specified, or prompt asking for file to comment if one is not provided.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boleyn](https://clawhub.ai/user/boleyn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and learners use this skill to add explanatory comments to selected code files while preserving formatting, encoding, and build correctness. It is intended to turn existing code into a clearer learning resource for different experience levels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may substantially increase the length of selected code files and reduce readability in files where additional comments are not desired.

Mitigation: Review the generated diff before keeping changes and apply the skill only to files where educational commentary is useful.

Risk: Added comments could accidentally affect generated output, formatting-sensitive files, or language-specific syntax if not validated.

Mitigation: Run the relevant formatter, syntax check, or test suite after comment insertion, especially for files with strict encoding or indentation rules.

## Reference(s):

- [PEP 263 - Defining Python Source Code Encodings](https://peps.python.org/pep-0263/)
- [ClawHub Skill Page](https://clawhub.ai/boleyn/skills/add-educational-comments)
- [Publisher Profile](https://clawhub.ai/user/boleyn)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown guidance and edited code comments in the target file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May substantially increase file length by adding educational comments; users should review resulting diffs.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
