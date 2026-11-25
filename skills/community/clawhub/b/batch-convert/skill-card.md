## Description:

Convert many files at once - a whole folder or a list of files - choosing one target format per file type (for example every HEIC photo to JPG, every MOV video to MP4, every DOCX to PDF). Use when the user asks to convert "all", "every", "these" or "the files in this folder", or to clean up a folder of mixed formats. Uses the Converter Studio MCP tools when connected; otherwise ffmpeg, ImageMagick, cwebp or LibreOffice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tariksucu](https://clawhub.ai/user/tariksucu)

### License/Terms of Use:

MIT-0

## Use Case:

People and developers converting a folder or selected list of files use this skill to group files by type, propose target formats, and convert approved items while preserving originals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is benign with medium confidence because one local path-like reference was unresolved, leaving some evidence incomplete.

Mitigation: Review the skill source and confirm any needed local paths before installation or execution.

Risk: Using Converter Studio tools can involve uploading files, including private documents.

Mitigation: Ask the user before uploading private documents, as the skill directs.

## Reference(s):

- [Server-resolved source repository](https://github.com/tariksucu/converter-studio/tree/main/skills/batch-convert)
- [ClawHub release page](https://clawhub.ai/tariksucu/skills/batch-convert)
- [Converter Studio](https://converter.studio)

## Skill Output:

**Output Type(s):** [Files, Markdown, Shell commands, API Calls, Guidance]

**Output Format:** [Converted files, with a Markdown conversion plan and report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Keeps originals unchanged; writes results to a converted/ folder and reports converted, failed, and skipped files.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
