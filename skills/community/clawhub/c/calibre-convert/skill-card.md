## Description:

Use this skill when the user wants to convert ebook or document files between formats with Calibre, including EPUB to PDF, Markdown to EPUB, MOBI to EPUB, AZW3 to EPUB, HTML to EPUB, DOCX to EPUB, and similar source/target format pairs supported by ebook-convert.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shake](https://clawhub.ai/user/shake)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and content teams use this skill to convert ebook and document files through Calibre's local ebook-convert command. It is suited to direct file-to-file conversions and simple format-specific tuning when users provide the source, output path, and any needed Calibre options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs Calibre's local ebook-convert command on files the user selects.

Mitigation: Install and invoke it only for intended conversions, and confirm the input and output paths before execution.

Risk: A conversion can create or replace a file at the requested output path.

Mitigation: Avoid sensitive directories and ask the agent to check before overwriting an existing output file.

Risk: Conversion output quality can vary by source structure, target format, and installed Calibre version.

Mitigation: Verify that the output file was created, review meaningful Calibre warnings, and inspect the converted result before relying on it.

## Reference(s):

- [Calibre Convert Examples](references/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/shake/skills/calibre-convert)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown with inline bash commands and conversion result paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create converted files at user-specified output paths when Calibre succeeds.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
