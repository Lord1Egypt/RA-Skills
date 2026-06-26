## Description: <br>
Feishu Sheet helps an agent create, read, edit, format, and manage Feishu spreadsheets through a shell-based OpenClaw skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[siyiding](https://clawhub.ai/user/siyiding) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill when they need an OpenClaw agent to automate Feishu spreadsheet workflows, including creating sheets, reading and writing ranges, formatting cells, adding images, managing rows and columns, and finding or replacing values. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can overwrite, replace, delete, or otherwise modify spreadsheet content. <br>
Mitigation: Verify spreadsheet tokens, sheet IDs, ranges, and target operations before running write, replace, or delete commands. <br>
Risk: The skill uses Feishu app credentials and receives tenant access tokens. <br>
Mitigation: Use a minimal-permission Feishu app, protect the OpenClaw configuration file, and rotate credentials if exposure is suspected. <br>
Risk: Image upload and floating-image URL commands can expand data movement beyond basic spreadsheet edits. <br>
Mitigation: Use local image paths and remote image URLs only from trusted sources, and account for Drive media upload permissions when enabling image workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/siyiding/feishu-sheet) <br>
- [Skill homepage](https://clawhub.ai/skills/feishu-sheet) <br>
- [Feishu Open API endpoint](https://open.feishu.cn/open-apis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu app credentials in the OpenClaw configuration and returns Feishu API responses or command output.] <br>

## Skill Version(s): <br>
1.2.0 (source: server evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
