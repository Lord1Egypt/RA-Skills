## Description: <br>
从钉钉闪记提取听记数据，包括列表、转写文本、摘要、待办等。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[156554395](https://clawhub.ai/user/156554395) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and developers use this skill to guide agents through DingTalk Shanji meeting-minute workflows, including listing accessible recordings, retrieving transcripts, summaries, todos, keywords, and exporting structured results with the dws CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may access sensitive DingTalk meeting transcripts, summaries, todos, and participant information. <br>
Mitigation: Use it only with authorized DingTalk accounts and confirm that requested records are appropriate to access or export. <br>
Risk: The artifact documents remote code installation through npm and shell installer commands. <br>
Mitigation: Prefer npm installation, review installer sources before execution, and run installation commands only after explicit user approval. <br>
Risk: The documented dws commands include mutating actions such as updating titles, summaries, replacing text, uploading recordings, and creating mind maps. <br>
Mitigation: Require explicit confirmation before any command that changes DingTalk records or uploads files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/156554395/dingtalk-shanji) <br>
- [DingTalk Workspace CLI repository](https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli) <br>
- [DingTalk Workspace CLI command documentation](https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli/blob/main/docs/command-index.md) <br>
- [DingTalk Workspace CLI Chinese documentation](https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli/blob/main/README_zh.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the dws CLI, DingTalk OAuth login, and permission to access the requested meeting records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
