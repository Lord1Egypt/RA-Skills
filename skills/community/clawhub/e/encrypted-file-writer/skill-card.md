## Description: <br>
Writes content to local files, including text, code, configuration, Word documents, and Excel spreadsheets, with encoding handling for agent-driven file creation and updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[endcy](https://clawhub.ai/user/endcy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill when an agent needs to create, overwrite, or append local files in common text, code, configuration, .docx, or .xlsx formats. It is most appropriate for explicit, reviewed file-writing tasks where the target path and content are intended by the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is a broad local file writer that can create, overwrite, and append files. <br>
Mitigation: Use it only for explicit file-writing requests, review target paths before execution, and keep backups for important files. <br>
Risk: The skill name and description may imply encryption or protected-file enforcement that the security evidence does not confirm. <br>
Mitigation: Do not assume this skill encrypts output or enforces enterprise protection policies; use separate approved encryption or data-protection controls when needed. <br>
Risk: Writing sensitive configuration, scripts, shell profiles, or environment files can alter system or application behavior. <br>
Mitigation: Avoid those targets unless the change is intentional and reviewed, and inspect resulting diffs or file contents before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/endcy/encrypted-file-writer) <br>
- [README](artifact/README.md) <br>
- [Verification report](artifact/VERIFICATION_REPORT.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, shell commands] <br>
**Output Format:** [Local files plus terminal status lines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can overwrite or append files and can create missing parent directories.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
