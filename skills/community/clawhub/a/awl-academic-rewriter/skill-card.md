## Description:

Rewrite English prose sentence by sentence into a more academic version using the bundled AWL/NAWL vocabulary list while preserving meaning, tense, claims, and document structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[junwugit](https://clawhub.ai/user/junwugit)

### License/Terms of Use:

MIT-0

## Use Case:

External users and writing-focused agents use this skill to revise English prose into a more academic register. It produces a sentence-level change report and a complete revised document while checking selected AWL/NAWL headwords against bundled references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The revised document may unintentionally change meaning because vocabulary substitutions rely on model judgment.

Mitigation: Review the sentence-level change report against the source text before using the revised document.

Risk: Input files are rewritten into saved Markdown outputs.

Mitigation: Provide only source files intended for processing and inspect the generated Markdown before sharing or publishing it.

## Reference(s):

- [AWL/NAWL Headwords](references/awl-headwords.txt)
- [AWL/NAWL CSV Reference](references/awl.csv)
- [ClawHub Skill Page](https://clawhub.ai/junwugit/skills/awl-academic-rewriter)

## Skill Output:

**Output Type(s):** [Markdown, Text, Files, Shell commands, Guidance]

**Output Format:** [Markdown files with sentence-level table output and a complete revised document]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces two Markdown files by default unless the user asks for a different format.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
