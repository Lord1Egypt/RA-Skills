## Description:

Document Organizer helps agents batch-convert legacy Office documents, modern Office files, and PDFs into searchable Markdown while preserving directory structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byteuser1977](https://clawhub.ai/user/byteuser1977)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and knowledge-base maintainers use this skill to convert archives of Office documents and PDFs into searchable Markdown. It is suited for document digitization, project archiving, and knowledge-base preparation where folder structure should be preserved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can unexpectedly delete a local temp directory, including during dry-run setup.

Mitigation: Run it only from a controlled working directory with no valuable `temp_batch` folder, and back up important source and output data before bulk conversion.

Risk: Bulk document conversion can overwrite or produce large output sets and may fail on dependency or file-permission issues.

Mitigation: Use `--dry-run` first, choose an explicit output directory, avoid running as admin/root, and review conversion logs before relying on the output.

Risk: The workflow depends on local CLI and Python tools for document parsing.

Mitigation: Pin LibreOffice, MarkItDown, and Python dependencies in the deployment environment before installing or running the skill.

## Reference(s):

- [API Reference](artifact/references/API_REFERENCE.md)
- [Format Support](artifact/references/FORMATS.md)
- [Configuration Guide](artifact/references/CONFIGURATION.md)
- [Troubleshooting Guide](artifact/references/TROUBLESHOOTING.md)
- [Performance Guide](artifact/references/PERFORMANCE.md)
- [Examples](artifact/references/EXAMPLES.md)
- [LibreOffice](https://zh-cn.libreoffice.org/)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files with command-line guidance and conversion logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Batch conversion may create output directories, logs, and temporary working files.]

## Skill Version(s):

1.0.4 (source: server release metadata, manifest.json, package.json, artifact changelog; released 2026-03-12)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
