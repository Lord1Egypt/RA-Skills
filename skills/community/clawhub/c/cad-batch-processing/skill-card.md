## Description:

Provides CAD batch-processing support for reading DXF content, replacing drawing text, renaming layers, editing block attributes, changing layer colors, generating simple DXF plans, backing up CAD projects, renaming CAD files, and watermarking PDFs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[137984917-cyber](https://clawhub.ai/user/137984917-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

Interior design teams and CAD automation users can use this skill to inspect DXF drawings, apply repeated project-name or standards updates across drawings, generate simple plan geometry, and prepare project files for handoff or archiving.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bulk modify and rename operations can change many CAD files in place.

Mitigation: Run the skill only on copied project folders or verified backups, and confirm target folders and replacement values before execution.

Risk: Backup destinations placed inside the source project can mix copies with originals or expand the backup scope.

Mitigation: Choose a backup destination outside the source folder and verify the resulting archive before deleting or overwriting originals.

Risk: Unpinned Python dependencies can produce different behavior across environments.

Mitigation: Use a virtual environment and pin required packages such as ezdxf, PyPDF2, and reportlab before using the scripts on valuable CAD projects.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/137984917-cyber/skills/cad-batch-processing)
- [Publisher profile](https://clawhub.ai/user/137984917-cyber)
- [Artifact skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python examples and shell commands; scripts may produce JSON, DXF, PDF, or renamed/copied files when executed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include in-place file changes, copied backup files, generated DXF drawings, extracted JSON metadata, and watermarked PDFs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
