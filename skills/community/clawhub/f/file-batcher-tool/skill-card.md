## Description: <br>
Provides batch file operations for renaming files, converting images, organizing files by type, finding duplicates, counting files, and listing large files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yushimohuang](https://clawhub.ai/user/yushimohuang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operators use this skill to generate shell commands and guidance for local bulk file management tasks such as renaming, organizing, image conversion, duplicate detection, file counting, and large-file listing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bulk rename and organize operations can move or rename many local files without enough warning or safeguards. <br>
Mitigation: Use only backed-up or test folders, avoid broad paths such as home or Downloads unless intended, and require preview plus confirmation before executing rename or organize operations. <br>
Risk: Image conversion removes original files after conversion. <br>
Mitigation: Convert copies or backed-up folders first, and require explicit confirmation that removing originals is acceptable. <br>
Risk: The security verdict is suspicious because useful local batching behavior can still cause destructive file changes. <br>
Mitigation: Review the script before installing and limit execution to folders the user explicitly selected. <br>


## Reference(s): <br>
- [File Batcher Tool on ClawHub](https://clawhub.ai/yushimohuang/file-batcher-tool) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and command output text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands act on local folders and can modify files; image conversion requires ImageMagick.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
