## Description:

Convert a text-based document to markdown following instructions from prompt, or if a documented option is passed, follow the instructions for that option.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhauga](https://clawhub.ai/user/jhauga)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and documentation maintainers use this skill to convert plain text or generic text documentation into structured Markdown, with optional guidance from explicit instructions, predefined formatting options, or a reference Markdown file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create or modify a Markdown file next to the source document.

Mitigation: Review target paths before conversion and use version control or backups for important source documents.

Risk: Finalizing or polishing can apply whole-document whitespace and formatting cleanup.

Mitigation: Review converted documents afterward when exact whitespace, indentation, or literal formatting matters.

## Reference(s):

- [GitHub basic writing and formatting syntax](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
- [Markdown Guide extended syntax](https://www.markdownguide.org/extended-syntax/)
- [Azure DevOps Markdown guidance](https://learn.microsoft.com/en-us/azure/devops/project/wiki/markdown-guidance?view=azure-devops)
- [ClawHub skill page](https://clawhub.ai/jhauga/skills/convert-plaintext-to-md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance and edited Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a .md copy next to the source document or modify an existing .md file when converting or finalizing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
