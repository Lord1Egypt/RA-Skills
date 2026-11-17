## Description:

Converts Markdown documents into well-typeset DOCX files with structured headings, lists, tables, quote blocks, callouts, and pagination controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jes614753-sketch](https://clawhub.ai/user/jes614753-sketch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and agents use this skill to convert Markdown source files into DOCX documents suitable for reading, printing, or delivery. It is especially useful when documents need clearer visual hierarchy and safer pagination across headings, lists, tables, and callout blocks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The conversion script writes to a user-selected DOCX output path, which could overwrite or place files somewhere unintended.

Mitigation: Confirm the input Markdown file and output DOCX path before running the script, and use a new output filename when reviewing iterations.

Risk: The artifact includes maintainer notes about updating the skill script itself, which is separate from routine document conversion.

Mitigation: Treat changes to the skill or script as explicit maintenance work that requires user intent, review, and scanning before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jes614753-sketch/skills/docx-typesetting-from-markdown)

## Skill Output:

**Output Type(s):** [files, shell commands, guidance]

**Output Format:** [DOCX file generated from Markdown, with Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local Markdown input and a user-selected DOCX output path.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
