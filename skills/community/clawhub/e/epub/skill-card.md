## Description:

Helps agents inspect, extract, convert, and modify EPUB files by treating them as ZIP archives and parsing their navigation, package, content, metadata, and image files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaojizhou](https://clawhub.ai/user/gaojizhou)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to read, inspect, extract, and modify EPUB ebooks, including chapters, tables of contents, metadata, text, images, and EPUB2 or EPUB3 structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends system-level Python package installation with --break-system-packages.

Mitigation: Use a virtual environment or preinstalled packages before running the EPUB parsing workflow.

Risk: The skill recommends extracting user-provided EPUB archives without explicit validation or size limits.

Mitigation: Extract each EPUB into a fresh temporary directory after validating archive paths and applying size limits.

Risk: The skill uses fixed output paths that could overwrite prior work.

Mitigation: Choose unique output filenames or isolated output directories for each EPUB processing run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gaojizhou/skills/epub)
- [Open Packaging Format namespace](http://www.idpf.org/2007/opf)
- [Dublin Core Elements namespace](http://purl.org/dc/elements/1.1/)
- [Navigation Control file for XML namespace](http://www.daisy.org/z3986/2005/ncx/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce extracted text files, copied images, metadata summaries, or repacked EPUB files when an agent follows the workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
