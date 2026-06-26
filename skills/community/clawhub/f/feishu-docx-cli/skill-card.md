## Description: <br>
Feishu Docx CLI helps agents create, read, overwrite, append to, add images to, and manage permissions for Feishu documents through a configured Feishu app. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[songofhawk](https://clawhub.ai/user/songofhawk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to manage Feishu document workflows from an agent or CLI, including document creation, Markdown-based updates, image upload, and collaborator permission changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can overwrite Feishu document contents. <br>
Mitigation: Confirm target document tokens before write operations and keep backups or version history for documents that may be overwritten. <br>
Risk: The skill can upload selected local files into Feishu documents. <br>
Mitigation: Review the file path and document target before upload, and avoid uploading sensitive files unless the destination document is approved for that content. <br>
Risk: The skill can add or remove Feishu document collaborators. <br>
Mitigation: Use least-privilege Feishu app permissions and verify member IDs and intended access levels before running permission changes. <br>


## Reference(s): <br>
- [Feishu Open Platform Documentation](https://open.feishu.cn/document/) <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Text, Markdown] <br>
**Output Format:** [Markdown guidance with CLI commands and human-readable command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured Feishu app and OpenClaw Feishu channel credentials.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
