## Description:

Convert files between formats - video, audio, images, PDFs, documents, e-books, subtitles, data and archives (for example HEIC to JPG, MOV to MP4, video to MP3, Word to PDF, PDF to images). Use when the user asks to convert, export, extract audio from, or change the format of a file. Uses the Converter Studio MCP tools when they are connected; otherwise local tools such as ffmpeg, ImageMagick or LibreOffice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tariksucu](https://clawhub.ai/user/tariksucu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to convert files between common media, document, data, and archive formats, using Converter Studio when connected or local tools otherwise.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: One reference could not be resolved, leaving the security review evidence incomplete.

Mitigation: Review the available instructions and confirm the referenced material before relying on the skill.

Risk: Remote conversions may consume account credits, with audio and video prices varying by conversion details.

Mitigation: Share the quoted price and get the user's agreement before confirming a conversion that requires approval.

Risk: Private files could be sent to an external conversion service.

Mitigation: Send only files the user asked to convert, and get the user's go-ahead before uploading private documents.

Risk: A local conversion could overwrite the original file if paths are chosen carelessly.

Mitigation: Write the converted result next to the source with its new extension; do not overwrite the original.

## Reference(s):

- [Server-resolved source repository (tariksucu/converter-studio, skills/convert-files)](https://github.com/tariksucu/converter-studio/tree/main/skills/convert-files)
- [Local conversion recipes](artifact/references/recipes.md)
- [Converter Studio developer documentation](https://converter.studio/developers)
- [Converter Studio](https://converter.studio)
- [Converter Studio pricing](https://converter.studio/pricing)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Converted files plus concise Markdown guidance and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves source files and describes the output format, size, and any conversion losses.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
