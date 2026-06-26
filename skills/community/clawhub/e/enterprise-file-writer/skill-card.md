## Description: <br>
Writes content to local files in enterprise security-policy environments, supporting text files, Word documents (.docx), Excel spreadsheets (.xlsx), and other common formats with explicit encoding handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[endcy](https://clawhub.ai/user/endcy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and automation agents use this skill to create, overwrite, or append local text, code, configuration, Word, and Excel files while controlling output encoding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can overwrite or append to any local file the user account can access and has no built-in path restriction or confirmation step. <br>
Mitigation: Use explicit, reviewed paths and avoid sensitive locations such as home dotfiles, startup folders, credential stores, system directories, and important project files unless the write is deliberate. <br>
Risk: Append and overwrite modes can modify existing project, configuration, Office, or log files in ways that are hard to reverse. <br>
Mitigation: Review requested mode, destination path, and content before execution, and keep backups or version control for important files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/endcy/enterprise-file-writer) <br>
- [README](README.md) <br>
- [Verification report](VERIFICATION_REPORT.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Local file content written through shell command execution, with status text reporting the path and bytes written.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports overwrite and append modes, stdin input, UTF-8 by default, GBK, GB2312, Latin-1, and OpenXML .docx/.xlsx output.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
