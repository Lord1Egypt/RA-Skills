## Description:

Batch exports Feishu documents and folders to local Markdown, with PDF export advertised but not implemented in this release.

This skill is ready for commercial/non-commercial use.

## Publisher:

[night556](https://clawhub.ai/user/night556)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to back up, migrate, or offline-view Feishu documents by exporting individual documents or folders to local Markdown files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recursive folder exports can write files outside the selected output directory when Feishu folder names contain path traversal text.

Mitigation: Avoid recursive exports on folders whose names may be controlled by others, and use a secure local output directory until output-path containment is fixed.

Risk: The skill exports authorized Feishu document contents to local files.

Mitigation: Use it only with Feishu documents you are authorized to export and store outputs in an access-controlled location.

Risk: PDF export is advertised but not implemented in this release.

Mitigation: Plan for Markdown output only and verify output format before depending on exported files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/night556/skills/feishu-doc-exporter)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown files and terminal status text from CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Feishu document and drive read permissions; PDF and image export behavior should be treated as unavailable in this release.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
