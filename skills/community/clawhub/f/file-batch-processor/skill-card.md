## Description:

File Batch Processor helps an agent guide local batch workflows for renaming files, compressing images, converting images or text to PDF, and organizing files by type.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lx19840614](https://clawhub.ai/user/lx19840614)

### License/Terms of Use:


## Use Case:

External users, students, shop owners, professionals, and developers use this skill to plan and run local file batch operations such as file renaming, image compression, PDF conversion, and file organization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can overwrite, move, or corrupt many local files without enough safeguards.

Mitigation: Use copied folders or backed-up data, run dry-run previews first, and avoid using it on important originals.

Risk: Some conversions or compression operations may not preserve GIF/BMP formats or existing PDFs as expected.

Mitigation: Inspect sample outputs before large runs and prefer a version with safer default output folders, pinned dependencies, collision checks, and real backup or rollback support.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lx19840614/skills/file-batch-processor)
- [File Renaming Patterns Guide](references/naming_patterns.md)
- [Image Compression Technical Guide](references/compression_guide.md)
- [File Type Identification Rules](references/file_types.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown guidance with command examples; local scripts may rename, move, compress, or convert files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally and supports preview modes for several operations.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
