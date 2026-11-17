## Description: <br>
This skill guides an agent through the two-step Feishu workflow for uploading a local file to obtain a file_key and sending it as a file message to a specified recipient. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when they need an agent to send HTML, ZIP, PDF, code, CSV, or similar local files to a Feishu user through the file upload and file message workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can cause an agent to send local files to a Feishu recipient, including files the user did not mean to share. <br>
Mitigation: Confirm the exact file path and recipient open_id before each send, and use the skill only for intended non-sensitive files. <br>
Risk: The workflow uses app credentials and includes commands that could expose secrets if printed, scraped, or stored in logs. <br>
Mitigation: Provide credentials through a managed secret store or environment controls, and avoid commands that print or extract app secrets from local configuration files. <br>
Risk: Raw shell and curl commands can fail or be modified in ways that send the wrong file or target the wrong recipient. <br>
Mitigation: Review generated commands before execution and verify the selected file, Feishu app credentials, and recipient identifier. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/feishu-send-file-free) <br>
- [Feishu file upload API endpoint](https://open.feishu.cn/open-apis/im/v1/files) <br>
- [Feishu message send API endpoint](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Feishu API request examples, file path checks, credential handling guidance, and troubleshooting steps.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
