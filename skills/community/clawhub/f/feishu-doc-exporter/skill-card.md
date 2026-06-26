## Description: <br>
Feishu Document Exporter - Batch export Feishu docs to markdown/PDF. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[night556](https://clawhub.ai/user/night556) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and documentation teams use this skill to export Feishu documents or folders to local Markdown files for backup, migration, offline review, or publishing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Feishu document and folder read access. <br>
Mitigation: Install it only for workspaces where that read access is acceptable, and use the minimum Feishu permissions needed for the export task. <br>
Risk: The skill shells out to OpenClaw and writes exported files to a local directory. <br>
Mitigation: Review the CLI behavior before deployment, use a dedicated export directory, and test with a small document or folder first. <br>
Risk: Folder-derived paths may be written without full path sanitization. <br>
Mitigation: Avoid exporting folders you do not fully control until path handling is reviewed or patched. <br>
Risk: PDF, image, and incremental export capabilities are advertised but not fully implemented in this version. <br>
Mitigation: Plan on Markdown export as the supported behavior for version 1.0.0 and verify required output formats before batch use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/night556/feishu-doc-exporter) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files and CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exports document content to a local output directory and can list Feishu folder contents.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
